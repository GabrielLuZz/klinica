from django.test import TestCase
from attendance.models import Attendance
from users.models import User
from django.forms import model_to_dict
from django.utils import timezone


class TestAttendanceModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.attendance_data = {
            "attendance_type": "test",
            "attendance_info": "Test info",
        }

        cls.doctor = User.objects.create_user(
            {
                "username": "doctor_test",
                "is_doctor": True,
            }
        )

        cls.receptionist = User.objects.create_user(
            {
                "username": "receptionist_test",
                "is_receptionist": True,
            }
        )

        cls.patient = User.objects.create_user(
            {
                "username": "patient_test",
            }
        )

        cls.attendance = Attendance.objects.create(**cls.attendance_data)
        cls.attendance.users.set([cls.doctor, cls.receptionist, cls.patient])

    def test_max_length_fields(self):
        status_max_length = self.attendance._meta.get_field("status").max_length
        attendance_type_max_length = self.attendance._meta.get_field(
            "attendance_type"
        ).max_length

        self.assertEqual(status_max_length, 20)
        self.assertEqual(attendance_type_max_length, 50)

    def test_attendance_fields(self):
        self.assertEqual(self.attendance.status, "Em espera")
        self.assertEqual(
            self.attendance.attendance_type, self.attendance_data["attendance_type"]
        )
        self.assertEqual(
            self.attendance.attendance_info, self.attendance_data["attendance_info"]
        )

    def test_relations(self):
        attendance = model_to_dict(self.attendance)
        self.assertTrue(self.doctor in attendance["users"])
        self.assertTrue(self.receptionist in attendance["users"])
        self.assertTrue(self.patient in attendance["users"])


class TestAttendanceRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.attendance_data = {
            "attendance_type": "test",
            "attendance_info": "Test info",
        }

        cls.doctor_data = {
            "username": "doctor_test",
            "password": "test_password",
            "is_doctor": True,
        }

        cls.doctor = User.objects.create_user(**cls.doctor_data)

        cls.receptionist_data = {
            "username": "receptionist_test",
            "password": "test_password",
            "is_receptionist": True,
        }

        cls.receptionist = User.objects.create_user(**cls.receptionist_data)

        cls.patient_data = {
            "username": "patient_test",
            "last_login": timezone.now(),
            "password": "test_password",
        }

        cls.patient2_data = {
            "username": "patient2_test",
            "last_login": timezone.now(),
            "password": "test_password",
        }

        cls.patient = User.objects.create_user(**cls.patient_data)

        cls.patient2 = User.objects.create_user(**cls.patient2_data)

    def test_create_attendance(self):

        doctor_token = self.client.post(
            "/api/login/",
            {
                "username": self.doctor_data["username"],
                "password": self.doctor_data["password"],
            },
        )

        receptionist_token = self.client.post(
            "/api/login/",
            {
                "username": self.receptionist_data["username"],
                "password": self.receptionist_data["password"],
            },
        )

        patient_token = self.client.post(
            "/api/login/",
            {
                "username": self.patient_data["username"],
                "password": self.patient_data["password"],
            },
        )

        response_no_authenticated = self.client.post(
            "/api/attendance/",
            self.attendance_data,
        )

        self.assertEqual(response_no_authenticated.status_code, 401)
        self.assertEqual(
            response_no_authenticated.json(),
            {"detail": "Authentication credentials were not provided."},
        )

        response_not_receptionist = self.client.post(
            "/api/attendance/",
            {**self.attendance_data},
            HTTP_AUTHORIZATION=f"Token {patient_token.json()['token']}",
        )

        self.assertEqual(response_not_receptionist.status_code, 403)
        self.assertEqual(
            response_not_receptionist.json(),
            {"detail": "You do not have permission to perform this action."},
        )

        response_no_body = self.client.post(
            "/api/attendance/",
            {},
            HTTP_AUTHORIZATION=f"Token {receptionist_token.json()['token']}",
        )

        self.assertEqual(response_no_body.status_code, 400)
        for key in response_no_body.json().keys():
            self.assertEqual(response_no_body.json()[key][0], "This field is required.")

        response_wrong_doctor = self.client.post(
            "/api/attendance/",
            {
                **self.attendance_data,
                "doctor_id": 0,
                "receptionist_id": self.receptionist.id,
                "patient_id": self.patient.id,
            },
            HTTP_AUTHORIZATION=f"Token {receptionist_token.json()['token']}",
        )

        self.assertEqual(response_wrong_doctor.status_code, 404)
        self.assertEqual(response_wrong_doctor.json()["detail"], "Doctor not Found")

        response_correct = self.client.post(
            "/api/attendance/",
            {
                **self.attendance_data,
                "doctor_id": self.doctor.id,
                "receptionist_id": self.receptionist.id,
                "patient_id": self.patient.id,
            },
            HTTP_AUTHORIZATION=f"Token {receptionist_token.json()['token']}",
        )

        self.assertEqual(response_correct.status_code, 201)
        attendance = Attendance.objects.get(attendance_type="test")
        self.assertEqual(response_correct.json()["id"], attendance.id)

    def test_retrieve_attendance(self):
        doctor_token = self.client.post(
            "/api/login/",
            {
                "username": self.doctor_data["username"],
                "password": self.doctor_data["password"],
            },
        )

        receptionist_token = self.client.post(
            "/api/login/",
            {
                "username": self.receptionist_data["username"],
                "password": self.receptionist_data["password"],
            },
        )

        patient_token = self.client.post(
            "/api/login/",
            {
                "username": self.patient_data["username"],
                "password": self.patient_data["password"],
            },
        )

        attendance = self.client.post(
            "/api/attendance/",
            {
                **self.attendance_data,
                "doctor_id": self.doctor.id,
                "receptionist_id": self.receptionist.id,
                "patient_id": self.patient.id,
            },
            HTTP_AUTHORIZATION=f"Token {receptionist_token.json()['token']}",
        )

        response_not_doctor = self.client.get(
            f"/api/attendance/{attendance.json()['id']}/",
            HTTP_AUTHORIZATION=f"Token {patient_token.json()['token']}",
        )

        self.assertEqual(response_not_doctor.status_code, 403)
        self.assertEqual(
            response_not_doctor.json()["detail"],
            "You do not have permission to perform this action.",
        )

        response_correct = self.client.get(
            f"/api/attendance/{attendance.json()['id']}/",
            HTTP_AUTHORIZATION=f"Token {doctor_token.json()['token']}",
        )

        self.assertEqual(response_correct.status_code, 200)

    def test_update_attendance(self):
        doctor_token = self.client.post(
            "/api/login/",
            {
                "username": self.doctor_data["username"],
                "password": self.doctor_data["password"],
            },
        )

        receptionist_token = self.client.post(
            "/api/login/",
            {
                "username": self.receptionist_data["username"],
                "password": self.receptionist_data["password"],
            },
        )

        patient_token = self.client.post(
            "/api/login/",
            {
                "username": self.patient_data["username"],
                "password": self.patient_data["password"],
            },
        )

        attendance = self.client.post(
            "/api/attendance/",
            {
                **self.attendance_data,
                "doctor_id": self.doctor.id,
                "receptionist_id": self.receptionist.id,
                "patient_id": self.patient.id,
            },
            HTTP_AUTHORIZATION=f"Token {receptionist_token.json()['token']}",
        )

        update_invalid_status = self.client.patch(
            f"/api/attendance/{attendance.json()['id']}/",
            {"status": "Finalizados"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {doctor_token.json()['token']}",
        )

        self.assertEqual(update_invalid_status.status_code, 400)
        self.assertEqual(
            update_invalid_status.json()["status"][0],
            '"Finalizados" is not a valid choice.',
        )

        update_not_doctor = self.client.patch(
            f"/api/attendance/{attendance.json()['id']}/",
            {"status": "Finalizado"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {patient_token.json()['token']}",
        )

        self.assertEqual(update_not_doctor.status_code, 403)
        self.assertEqual(
            update_not_doctor.json()["detail"],
            "You do not have permission to perform this action.",
        )

        update_correct = self.client.patch(
            f"/api/attendance/{attendance.json()['id']}/",
            {"status": "Finalizado"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {doctor_token.json()['token']}",
        )

        self.assertEqual(update_correct.status_code, 200)
        self.assertEqual(update_correct.json()["status"], "Finalizado")

    def test_list_user_attendances(self):
        doctor_token = self.client.post(
            "/api/login/",
            {
                "username": self.doctor_data["username"],
                "password": self.doctor_data["password"],
            },
        )

        receptionist_token = self.client.post(
            "/api/login/",
            {
                "username": self.receptionist_data["username"],
                "password": self.receptionist_data["password"],
            },
        )

        patient_token = self.client.post(
            "/api/login/",
            {
                "username": self.patient_data["username"],
                "password": self.patient_data["password"],
            },
        )

        patient2_token = self.client.post(
            "/api/login/",
            {
                "username": self.patient2_data["username"],
                "password": self.patient2_data["password"],
            },
        )

        attendance = self.client.post(
            "/api/attendance/",
            {
                **self.attendance_data,
                "doctor_id": self.doctor.id,
                "receptionist_id": self.receptionist.id,
                "patient_id": self.patient.id,
            },
            HTTP_AUTHORIZATION=f"Token {receptionist_token.json()['token']}",
        )

        list_attendances_not_owner = self.client.get(
            f"/api/attendance/{self.patient.id}/user/",
            HTTP_AUTHORIZATION=f"Token {patient2_token.json()['token']}",
        )

        self.assertEqual(list_attendances_not_owner.status_code, 403)
        self.assertEqual(
            list_attendances_not_owner.json()["detail"],
            "You do not have permission to perform this action.",
        )

        list_attendances_owner = self.client.get(
            f"/api/attendance/{self.patient.id}/user/",
            HTTP_AUTHORIZATION=f"Token {patient_token.json()['token']}",
        )

        self.assertEqual(list_attendances_owner.status_code, 200)

    def test_list_attendances_as_doctor(self):
        doctor_token = self.client.post(
            "/api/login/",
            {
                "username": self.doctor_data["username"],
                "password": self.doctor_data["password"],
            },
        )

        receptionist_token = self.client.post(
            "/api/login/",
            {
                "username": self.receptionist_data["username"],
                "password": self.receptionist_data["password"],
            },
        )

        patient_token = self.client.post(
            "/api/login/",
            {
                "username": self.patient_data["username"],
                "password": self.patient_data["password"],
            },
        )

        attendance = self.client.post(
            "/api/attendance/",
            {
                **self.attendance_data,
                "doctor_id": self.doctor.id,
                "receptionist_id": self.receptionist.id,
                "patient_id": self.patient.id,
            },
            HTTP_AUTHORIZATION=f"Token {receptionist_token.json()['token']}",
        )

        list_attendances_not_doctor = self.client.get(
            f"/api/attendance/{self.patient.id}/doctor/",
            HTTP_AUTHORIZATION=f"Token {patient_token.json()['token']}",
        )

        self.assertEqual(list_attendances_not_doctor.status_code, 403)
        self.assertEqual(
            list_attendances_not_doctor.json()["detail"],
            "You do not have permission to perform this action.",
        )

        list_attendances_doctor = self.client.get(
            f"/api/attendance/{self.patient.id}/doctor/",
            HTTP_AUTHORIZATION=f"Token {doctor_token.json()['token']}",
        )

        self.assertEqual(list_attendances_doctor.status_code, 200)

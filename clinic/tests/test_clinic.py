from rest_framework.test import APITestCase
from users.models import User


class ClinicTests(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.super_user_data = {"username": "super", "password": "1234"}

        cls.doctor_data = {
            "username": "doctor",
            "password": "1234",
            "cpf": "12312312300",
            "is_doctor": True,
            "specialties": [{
                "name": "medico"
            }]
        }

        cls.clinic_data = {"clinic_name": "Consultorio 1", "doctor": 1}

        cls.clinic_data_invalid = {"clinic_name": "Consultorio 1", "doctor": 0}

        cls.login_super_user = {"username": "super", "password": "1234"}

        User.objects.create_superuser(**cls.super_user_data)

    def test_register_clinic_without_valid_doctor(self):

        token = self.client.post(
            "http://localhost:8000/api/login/",
            self.login_super_user,
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        response = self.client.post(
            "http://localhost:8000/api/clinic/register/",
            self.clinic_data_invalid,
            format="json",
        )

        self.assertAlmostEqual(response.status_code, 400)

    def test_register_clinic(self):

        token = self.client.post(
            "http://localhost:8000/api/login/",
            self.login_super_user,
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        doctor = self.client.post(
            "http://localhost:8000/api/doctor/",
            self.doctor_data,
            format="json",
        )

        doctor_id = doctor.json()["id"]

        response = self.client.post(
            "http://localhost:8000/api/clinic/register/",
            {"clinic_name": "Consutorio1", "doctor": doctor_id},
            format="json",
        )

        self.assertAlmostEqual(response.status_code, 201)

    def test_list_clinics(self):

        response = self.client.get(
            "http://localhost:8000/api/clinic/",
        )

        self.assertAlmostEqual(response.status_code, 200)

    def test_edit_clinics(self):

        token = self.client.post(
            "http://localhost:8000/api/login/",
            self.login_super_user,
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        doctor = self.client.post(
            "http://localhost:8000/api/doctor/",
            self.doctor_data,
            format="json",
        )

       
        doctor_id = doctor.json()["id"]

        clinic = self.client.post(
            "http://localhost:8000/api/clinic/register/",
            {"clinic_name": "Consutorio1", "doctor": doctor_id},
            format="json",
        )

        clinic_id = clinic.json()["id"]

        response = self.client.patch(
            f"http://localhost:8000/api/clinic/{clinic_id}/",
            {"clinic_name": "Consultorio 2"},
            format="json",
        )

        self.assertAlmostEqual(response.status_code, 200)

    def test_edit_clinics_withouth_permission(self):

        token = self.client.post(
            "http://localhost:8000/api/login/",
            self.login_super_user,
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        self.client.post(
            "http://localhost:8000/api/clinic/register/",
            self.clinic_data,
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + "token invalido")

        response = self.client.patch(
            "http://localhost:8000/api/clinic/2/",
            {"clinic_name": "Consultorio 2"},
            format="json",
        )

        self.assertAlmostEqual(response.status_code, 401)

    def test_delete_clinics_withouth_permission(self):

        token = self.client.post(
            "http://localhost:8000/api/login/",
            self.login_super_user,
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        self.client.post(
            "http://localhost:8000/api/clinic/register/",
            self.clinic_data,
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + "token invalido")

        response = self.client.delete(
            "http://localhost:8000/api/clinic/2/",
        )

        self.assertAlmostEqual(response.status_code, 401)

    def test_delete_clinics(self):

        token = self.client.post(
            "http://localhost:8000/api/login/",
            self.login_super_user,
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        doctor = self.client.post("http://localhost:8000/api/doctor/", self.doctor_data, format="json")

        doctor_id = doctor.json()["id"]

        clinic = self.client.post(
            "http://localhost:8000/api/clinic/register/",
            {"clinic_name": "Consutorio1", "doctor": doctor_id},
            format="json",
        ).json()

        clinic_id = clinic["id"]

        response = self.client.delete(
            f"http://localhost:8000/api/clinic/{clinic_id}/",
        )

        self.assertAlmostEqual(response.status_code, 204)

from django.test import TestCase
from attendance.models import Attendance
from users.models import User


class TestAttendanceModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.attendance_data = {
            "attendance_type": "eyes",
            "attendance_info": "Paciente apresenta irritação no olho direito",
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
        attendance_type_max_length = self.attendance._meta.get_field("attendance_type").max_length

        self.assertEqual(status_max_length, 20)
        self.assertEqual(attendance_type_max_length, 50)

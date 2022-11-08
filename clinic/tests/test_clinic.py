from rest_framework.test import APITestCase
from users.models import User


class ClinicTests(APITestCase):
    def setUp(self):

        self.super_user_data = {"username": "super", "password": "1234"}

        self.doctor_data = {
            "username": "doctor",
            "password": "1234",
            "is_doctor": True,
        }

        self.clinic_data = {"clinic_name": "Consultorio 1"}

        self.login_super_user = {"username": "super", "password": "1234"}

        User.objects.create_superuser(**self.super_user_data)

    def test_register_clinic_without_authentication(self):

        response = self.client.post(
            "http://localhost:8000/api/clinic/register/",
            self.clinic_data,
            format="json",
        )

        self.assertAlmostEqual(response.status_code, 401)

    def test_register_clinic(self):

        token = self.client.post(
            "http://localhost:8000/api/login/",
            self.login_super_user,
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        response = self.client.post(
            "http://localhost:8000/api/clinic/register/",
            self.clinic_data,
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

        self.client.post(
            "http://localhost:8000/api/clinic/register/",
            self.clinic_data,
            format="json",
        )

        response = self.client.patch(
            "http://localhost:8000/api/clinic/3/",
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

        clinic = self.client.post(
            "http://localhost:8000/api/clinic/register/",
            self.clinic_data,
            format="json",
        ).json()

        response = self.client.delete(
            "http://localhost:8000/api/clinic/1/",
        )

        self.assertAlmostEqual(response.status_code, 204)

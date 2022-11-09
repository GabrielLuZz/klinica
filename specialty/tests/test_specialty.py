from rest_framework.test import APITestCase
from users.models import User


class SpecialtyTests(APITestCase):
    def setUp(cls):
        cls.super_user_data = {
            "username": "teste",
            "password": "1234"
        }

        cls.specialties_data = {
            "name": "Clinico Geral"
        }

        cls.specialty_to_delete = {
            "name": "Medico"
        }

        cls.wrong_specialties_data = {
            "nome": "Clinico Geral"
        }

        cls.new_specialty_name = {
            "name": "Oftalmologista"
        }

        User.objects.create_superuser(**cls.super_user_data)

        cls.token = cls.client.post(
            "http://localhost:8000/api/login/",
            cls.super_user_data,
            format="json",
        )

        cls.client.credentials(HTTP_AUTHORIZATION="Token " + cls.token.data["token"])

    def test_create_specialty(self):
        new_specialty = self.client.post(
            "http://localhost:8000/api/specialty/create/",
            self.specialties_data,
            format="json",
        )

        specialty_id = new_specialty.json()["id"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.data["token"])

        self.assertEqual(new_specialty.status_code, 201)

    def test_create_wrong_specialty_name(self):
        new_specialty = self.client.post(
            "http://localhost:8000/api/specialty/create/",
            self.wrong_specialties_data,
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.data["token"])

        self.assertEqual(new_specialty.status_code, 400)

    def test_edit_specialty_name(self):
        new_specialty = self.client.post(
            "http://localhost:8000/api/specialty/create/",
            self.specialties_data,
            format="json",
        )

        specialty_id = new_specialty.json()["id"]

        new_specialty_name = self.client.patch(
            f'http://localhost:8000/api/specialty/{specialty_id}/',
            {"name": "Teste"},
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.data["token"])

        self.assertEqual(new_specialty_name.status_code, 200)

    def test_edit_specialty_wrong_id(self):
        response = self.client.patch(
            f'http://localhost:8000/api/specialty/4/',
            {"name": "Teste"},
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.data["token"])

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Not found.")

    def test_delete_specialty(self):
        new_specialty = self.client.post(
            "http://localhost:8000/api/specialty/create/",
            self.specialty_to_delete,
            format="json",
        )

        header = {
           "HTTP_AUTHORIZATION": f"Token {self.token}"
        }

        specialty_id = new_specialty.json()["id"]

        delete_specialty = self.client.delete(
            f'http://localhost:8000/api/specialty/{specialty_id}/',
            **header
        )

        self.assertEqual(delete_specialty.status_code, 204)

    def test_delete_specialty_wrong_id(self):
        header = {
           "HTTP_AUTHORIZATION": f"Token {self.token}"
        }

        response = self.client.delete(
            "http://localhost:8000/api/specialty/5/",
            **header
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Not found.")
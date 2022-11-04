# movies/tests.py
import json
from rest_framework.test import APITestCase
from users.models import User
from rest_framework.authtoken.models import Token


class UserViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_url = "/api/"

        cls.receptionist_data = {
            "username": "manoelgome3",
            "password": "1234",
            "birth_date": "2000-11-11",
            "cpf": "11122233344",
            "is_receptionist": True,
            "address": {
                "cep": "11111134",
                "state": "PR",
                "street": "fabio jr",
                "number": "11",
            },
        }

        cls.receptionist_data2 = {
            "username": "gabriel3",
            "password": "1234",
            "birth_date": "2000-11-11",
            "cpf": "11122233344",
            "is_receptionist": True,
            "address": {
                "cep": "11111134",
                "state": "PR",
                "street": "fabio jr",
                "number": "11",
            },
        }

        cls.receptionist_data2_login = {
            "username": "gabriel3",
            "password": "1234",
        }

        cls.receptionist2 = User.objects.create_user(**cls.receptionist_data2)

    def test_can_create_an_receptionist(self):
        response = self.client.post(
            f"{self.base_url}receptionists/",
            self.receptionist_data,
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(len(response.data), 8)

        self.assertTrue(response.data["is_receptionist"])

    def test_try_create_with_wrong_keys(self):
        response = self.client.post(
            f"{self.base_url}receptionists/",
            {},
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.data["username"][0],
            "This field is required.",
        )
        self.assertEqual(
            response.data["password"][0],
            "This field is required.",
        )
        self.assertEqual(
            response.data["first_name"][0],
            "This field is required.",
        )
        self.assertEqual(
            response.data["last_name"][0],
            "This field is required.",
        )

    def test_can_login_with_a_receptionist(self):

        response = self.client.post(
            f"{self.base_url}login/", self.receptionist_data2_login
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn("token", response.data)

    def test_list_users(self):
        response = self.client.get(f"{self.base_url}receptionists/")

        self.assertEqual(200, response.status_code)

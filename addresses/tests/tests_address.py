from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from users.models import User


# Create your tests here.
class AddressesTests(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        
        cls.admin_user = {
            "username": "jorge",
            "password": "1234",
            "first_name": "jor",
            "last_name": "ge",
        }

        cls.admin_login = {
            "username": "jorge",
            "password": "1234",
        }

        cls.admin = User.objects.create_superuser(**cls.admin_user)

        cls.patient_user = {
            "username": "marcelo",
            "password": "1234",
            "birth_date": "2000-11-11",
            "cpf": "11122233344",
            "address": {
                "cep": "11111135",
                "state": "PR",
                "street": "rua",
                "number": "11"
            }
        }

        cls.patient_login = {
            "username": "marcelo",
            "password": "1234",
            "new_password": "1234"
        }

        cls.patient_login_invalid = {
            "username": "marcelo",
            "password": "1234"
        }

        cls.patient_update = {
            "username": "celo"
        }

        cls.update_address = {
            "cep": "88888888"
        }

        cls.base_url = "/api/patients/"
        cls.update_url = "/api/patient/"
        cls.login_url = "/api/login/"
        cls.address_update_url = "/api/address/"


    def test_adm_user_can_update_address(self):

        login = self.client.post(self.login_url, self.admin_login)
        token = login.json()["token"]
        header = {
        "HTTP_AUTHORIZATION": f"Token {token}"
        }

        patient = self.client.post(f"{self.base_url}register/", self.patient_user, **header, format="json")
        patient_address_id = patient.json()["address"]["id"]
        
        response = self.client.patch(f"{self.address_update_url}{patient_address_id}/", self.update_address, **header, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["cep"], "88888888")


    def test_should_not_update_address_if_user_is_not_adm(self):

        login = self.client.post(self.login_url, self.admin_login)
        token = login.json()["token"]
        header = {
        "HTTP_AUTHORIZATION": f"Token {token}"
        }
        
        patient = self.client.post(f"{self.base_url}register/", self.patient_user, **header, format="json")
        patient_login = self.client.post(f"{self.login_url}patient/", self.patient_login)
        patient_token = patient_login.json()["token"]
        patient_address_id = patient.json()["address"]["id"]

        patient_header = {
        "HTTP_AUTHORIZATION": f"Token {patient_token}"
        }
        
        response = self.client.patch(f"{self.address_update_url}{patient_address_id}/", self.patient_update, **patient_header, format="json")

        self.assertEqual(response.status_code, 403)

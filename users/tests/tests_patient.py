from rest_framework.test import APITestCase
from users.models import User


# Create your tests here.
class PatientTests(APITestCase):
    
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

        cls.base_url = "/api/patients/"
        cls.update_url = "/api/patient/"
        cls.login_url = "/api/login/"

    def test_admin_can_list_users(self):

        response = self.client.get(f"{self.base_url}")
        login = self.client.post(self.login_url, self.admin_login)
        token = login.json()["token"]
        header = {
           "HTTP_AUTHORIZATION": f"Token {token}"
        }

        response = self.client.get(self.base_url, **header)


        self.assertEqual(response.status_code, 200)


    def test_cant_list_users_without_token(self):

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 401)


    def test_patient_can_be_created_by_adm_user(self):
        
        login = self.client.post(self.login_url, self.admin_login)
        token = login.json()["token"]
        header = {
           "HTTP_AUTHORIZATION": f"Token {token}"
        }

        response = self.client.post(f"{self.base_url}register/", self.patient_user, **header, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(type(response.json()["id"]), type(1))

    
    def test_patient_should_not_create_if_token_is_invalid(self):
        
        header = {
           "HTTP_AUTHORIZATION": f"Token 123456"
        }

        response = self.client.post(f"{self.base_url}register/", self.patient_user, **header, format="json")

        self.assertEqual(response.status_code, 401)


    def test_patient_should_not_login_without_new_password_key(self):

        login = self.client.post(self.login_url, self.admin_login)
        token = login.json()["token"]
        header = {
           "HTTP_AUTHORIZATION": f"Token {token}"
        }

        self.client.post(f"{self.base_url}register/", self.patient_user, **header, format="json")
        response = self.client.post(f"{self.login_url}patient/", self.patient_login_invalid)

        self.assertEqual(response.status_code, 400)


    def test_patient_login(self):
        login = self.client.post(self.login_url, self.admin_login)
        token = login.json()["token"]
        header = {
           "HTTP_AUTHORIZATION": f"Token {token}"
        }

        self.client.post(f"{self.base_url}register/", self.patient_user, **header, format="json")
        response = self.client.post(f"{self.login_url}patient/", self.patient_login)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["token"])


    def test_patient_should_not_update_if_not_adm_user(self):

        login = self.client.post(self.login_url, self.admin_login)
        token = login.json()["token"]
        header = {
           "HTTP_AUTHORIZATION": f"Token {token}"
        }

        patient = self.client.post(f"{self.base_url}register/", self.patient_user, **header, format="json")

        patient_login = self.client.post(f"{self.login_url}patient/", self.patient_login)

        patient_id = patient.json()["id"]
        patient_token = patient_login.json()["token"]
        patient_header = {
           "HTTP_AUTHORIZATION": f"Token {patient_token}"
        }
        
        response = self.client.patch(f"{self.base_url}{patient_id}/", self.patient_update, **patient_header, format="json")

        self.assertEqual(response.status_code, 403)


    def test_adm_user_can_update_patient(self):

        login = self.client.post(self.login_url, self.admin_login)
        token = login.json()["token"]
        header = {
           "HTTP_AUTHORIZATION": f"Token {token}"
        }

        patient = self.client.post(f"{self.base_url}register/", self.patient_user, **header, format="json")
        patient_login = self.client.post(f"{self.login_url}patient/", self.patient_login)
        patient_id = patient.json()["id"]
        
        response = self.client.patch(f"{self.update_url}{patient_id}/", self.patient_update, **header, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "celo")

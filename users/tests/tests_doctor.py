from rest_framework.test import APITestCase
from users.models import User
from django.test import TestCase


# Create your tests here.
class DoctorTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.admin_user = {
            "username": "matheus",
            "password": "1234",
            "first_name": "matheus",
            "last_name": "willcox",
        }

        cls.admin_login = {
            "username": "matheus",
            "password": "1234",
        }

        cls.admin = User.objects.create_superuser(**cls.admin_user)

        cls.doctor_user = {
	        "username": "Doctor",
	        "password": "1234",
	        "first_name": "matheus",
	        "last_name": "willcox",
	        "cpf": 12312312300,
	        "birth_date": "1988-02-01",
        	"is_doctor": True,
	        "crm": "123123"

        }

        cls.doctor_login = {
            "username": "Doctor",
            "password": "1234"
        }

        cls.doctor_login_invalid = {
            "username": "joao",
            "password": "1234"
        }

        cls.doctor_update = {
            "username": "Felipe"
        }

        cls.base_url = "/api/doctor/"
        cls.update_url = "/api/doctor/"
        cls.login_url = "/api/login/"



    def test_can_list_doctors_without_token(self):

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 200)


    def test_doctor_can_be_created_by_adm_user(self):
        
        login = self.client.post(self.login_url, self.admin_login)
    
        token = login.json()["token"]
        header = {
           "HTTP_AUTHORIZATION": f"Token {token}"
        }
        response = self.client.post(self.base_url, self.doctor_user, **header, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(type(response.json()["id"]), type(1))

    
    def test_doctor_should_not_create_if_token_is_invalid(self):
        
        header = {
           "HTTP_AUTHORIZATION": f"Token 123456"
        }

        response = self.client.post(self.base_url, self.doctor_user, **header, format="json")

        self.assertEqual(response.status_code, 401)


    def test_doctor_login(self):
        
        login = self.client.post(self.login_url, self.admin_login)
    
        token = login.json()["token"]
        header = {
           "HTTP_AUTHORIZATION": f"Token {token}"
        }
        create_doctor = self.client.post(self.base_url, self.doctor_user, **header, format="json")
        response = self.client.post(self.login_url, self.doctor_login)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["token"])


    def test_doctor_should_not_update_if_not_adm_user(self):

        login = self.client.post(self.login_url, self.admin_login)
        token = login.json()["token"]
        header = {
           "HTTP_AUTHORIZATION": f"Token {token}"
        }

        doctor = self.client.post(self.base_url, self.doctor_user, **header, format="json")

        doctor_login = self.client.post(self.login_url, self.doctor_login)

        doctor_id = doctor.json()["id"]
        doctor_token = doctor_login.json()["token"]
        doctor_header = {
           "HTTP_AUTHORIZATION": f"Token {doctor_token}"
        }
        
        response = self.client.patch(f"{self.base_url}{doctor_id}/", self.doctor_update, **doctor_header, format="json")

        self.assertEqual(response.status_code, 403)


    def test_adm_user_can_update_doctor(self):

        login = self.client.post(self.login_url, self.admin_login)
        token = login.json()["token"]
        header = {
           "HTTP_AUTHORIZATION": f"Token {token}"
        }

        doctor = self.client.post(self.base_url, self.doctor_user, **header, format="json")
        doctor_id = doctor.json()["id"]
        
        response = self.client.patch(f'{self.update_url}{doctor_id}/', self.doctor_update, **header,format="json", content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "Felipe")


    def test_adm_user_can_delete_doctor(self):

        login = self.client.post(self.login_url, self.admin_login)
        token = login.json()["token"]
        header = {
           "HTTP_AUTHORIZATION": f"Token {token}"
        }

        doctor = self.client.post(self.base_url, self.doctor_user, **header, format="json")
        doctor_id = doctor.json()["id"]
        
        response = self.client.delete(f'{self.update_url}{doctor_id}/', **header,format="json", content_type='application/json')

        self.assertEqual(response.status_code, 204)



    def test_doctor_login_cant_self_delete(self):

        login = self.client.post(self.login_url, self.admin_login)
        token = login.json()["token"]
        header = {
           "HTTP_AUTHORIZATION": f"Token {token}"
        }

        doctor = self.client.post(self.base_url, self.doctor_user, **header, format="json")
       
        doctor_login = self.client.post(self.login_url, self.doctor_login)
        doctor_id = doctor.json()["id"]

        doctor_token = doctor_login.json()["token"]
        doctor_header = {
           "HTTP_AUTHORIZATION": f"Token {doctor_token}"
        }
        
        response = self.client.delete(f'{self.update_url}{doctor_id}/', **doctor_header,format="json", content_type='application/json')

        self.assertEqual(response.status_code, 403)

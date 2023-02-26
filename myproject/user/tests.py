from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import User


# Create your tests here.

class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
                        name = "testuser",
                        email = 'testuser@test.com',
                        password = 'testuser',
                                            )
        self.success_url = reverse('home')
    
    def test_get_request_returns_200(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_form_rendering(self):
        response = self.client.get('/login/')
        self.assertContains(response,'<form')
        # there are 3 input fields one each for csrf, email and password
        # 
        self.assertContains(response,'<input', 3)

    
        self.assertContains(response, 'type="submit"')

    def test_login_success(self):
        data = {'email':"testuser@test.com", 'password': "testuser"}
        response = self.client.post(self.login_url, data)
        # manually posting the login data does not redirec to the success_url
        # hence we receive a status code 200
        
        self.assertEqual(response.status_code, 200)
        print(self.success_url)
        
        user = authenticate(email="testuser@test.com", password='testuser')
        self.assertEqual(user, self.user)

    def test_login_failure_invalid_creds(self):
        data = {'email':'testuser@test.com','password':'nothing'}
        response = self.client.post(self.login_url, data)
        self.assertContains(response, "Invalid Credentials")


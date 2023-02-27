from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import User

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission, Group
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
        self.change_password = reverse('change_password')

    
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
        
        self.assertRedirects(response, self.success_url)
        print(self.success_url)
        
        user = authenticate(email="testuser@test.com", password='testuser')
        self.assertEqual(user, self.user)

    def test_login_failure_invalid_creds(self):
        data = {'email':'testuser@test.com','password':'nothing'}
        response = self.client.post(self.login_url, data)
        self.assertContains(response, "Invalid Credentials")


class ChangePasswordViewTestCase(TestCase):
    '''
    1. Check if the change_password redirects to success url after successful
    password change
    2. Check if the view renders the same form when the new password and
    confirm password mismatch

    '''
    def setUp(self):
        self.user = get_user_model().objects.create(
            email='test@example.com',
            name = 'Test User',
            password = make_password('password')
        )
        self.client = Client()
        self.success_url = reverse('home')
        self.change_password_url = reverse('change_password')

        change_user_permission = Permission.objects.get(codename='change_user')
        group = Group.objects.create(name='Test Group')
        group.permissions.add(change_user_permission)

        self.user.groups.add(group)

    def test_change_password_successfully(self):
        user = authenticate(email='test@example.com',password='password')
        self.client.login(email='test@example.com',password='password') 

        data = {
        'current_password' : 'password',
        'new_password' : 'new',
        'confirm_password' : 'new'
           
        }
        response = self.client.post(self.change_password_url, data)
        self.assertRedirects(response, self.success_url)
        
        
        
    def test_change_password_mismatch(self):
        user = authenticate(email='test@example.com',password='password')
        self.client.login(email='test@example.com',password='password') 

        data = {
        'current_password' : 'password',
        'new_password' : 'new',
        'confirm_password' : 'old'
           
        }
        response = self.client.post(self.change_password_url, data)
        self.assertContains(response, 'Passwords do not match')

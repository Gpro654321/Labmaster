from django.urls import reverse_lazy
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
        '''
        test if the login url is reachable
        '''
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_form_rendering(self):
        '''
        test if login form contains the elements that are intended
        '''
        response = self.client.get('/login/')
        self.assertContains(response,'<form')
        # there are 3 input fields one each for csrf, email and password
        # 
        self.assertContains(response,'<input', 3)

    
        self.assertContains(response, 'type="submit"')

    def test_login_success(self):
        '''
        Test if a user is able to login with correct credentials
        '''
        data = {'email':"testuser@test.com", 'password': "testuser"}
        response = self.client.post(self.login_url, data)
        # manually posting the login data does not redirec to the success_url
        # hence we receive a status code 200
        
        self.assertRedirects(response, self.success_url)
        print(self.success_url)
        
        user = authenticate(email="testuser@test.com", password='testuser')
        self.assertEqual(user, self.user)

    def test_login_failure_invalid_creds(self):
        '''
        Test if the user is not being logged in if the credentials are not
        correct
        '''
        data = {'email':'testuser@test.com','password':'nothing'}
        response = self.client.post(self.login_url, data)
        self.assertContains(response, "Invalid Credentials")

    
    def test_correct_template_used(self):
        '''
        Test if the designated template is being used
        '''
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'registration/login.html')


class ChangePasswordViewTestCase(TestCase):
    '''
    1. Check if the change_password redirects to success url after successful
    password change
    2. Check if the view renders the same form when the new password and
    confirm password mismatch
    3. Test if the user redirected to login page if not logged in 
    4. Test if a user with no permissions is being forbiddent to view the page

    '''
    def setUp(self):
        self.user = get_user_model().objects.create(
            email='test@example.com',
            name = 'Test User',
            password = make_password('password')
        )

        #this user has no permissions
        self.user1 = User.objects.create_user(
                        name = "testuser1",
                        email = 'testuser1@test.com',
                        password = 'testuser1',
                        )

        self.client = Client()
        self.login_url = reverse('login')
        self.success_url = reverse('home')
        self.change_password_url = reverse('change_password')

        change_user_permission = Permission.objects.get(codename='change_user')
        group = Group.objects.create(name='Test Group')
        group.permissions.add(change_user_permission)

        self.user.groups.add(group)

    def test_change_password_successfully(self):
        '''
        test if the user is able to change the password successfully
        '''
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
        '''
        test if the form is rendered with errors if the new password and
        confirm_password do not match
        '''
        user = authenticate(email='test@example.com',password='password')
        self.client.login(email='test@example.com',password='password') 

        data = {
        'current_password' : 'password',
        'new_password' : 'new',
        'confirm_password' : 'old'
           
        }
        response = self.client.post(self.change_password_url, data)
        self.assertContains(response, 'Passwords do not match')

    def test_change_password_incorrect_current_password(self):
        '''
        test if the form is rendered with errors if the new password and
        confirm_password do not match

        '''
        user = authenticate(email='test@example.com',password='password')
        self.client.login(email='test@example.com',password='password') 

        data = {
        'current_password' : 'password1',
        'new_password' : 'new',
        'confirm_password' : 'new'
           
        }

        #the user will be redirected to the logout page, then from there he
        #will be redirected to the login page after logging out the user
        #so follow=True will render a 200 status on reaching the login page
        response = self.client.post(self.change_password_url, data, follow=True)
        print("I am inside current password mismatch test")
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy('login'), status_code=302)

    

    def test_change_password_not_logged_redirect(self):
        '''
        test to see if the user is redirect to login page if he/she is not
        logged in
        '''
        response = self.client.get(self.change_password_url)
        self.assertRedirects(response, self.login_url+"?next=/change_password/")

    def test_change_password_no_permission_redirect(self):
        '''
        test to see if the user is denied to view if he/she lacks permission
        '''

        user = authenticate(email='testuser1@test.com',password='testuser1')
        self.client.login(email='testuser1@test.com',password='testuser1') 

        response = self.client.get(self.change_password_url)
        self.assertEqual(response.status_code, 403)

    def test_correct_template_used(self):
        '''
        Test if the designated template is being used
        '''

        self.client.login(email='test@example.com',password='password') 
        response = self.client.get(self.change_password_url)
        self.assertTemplateUsed(response, 'change_password.html')


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
                        name = "testuser",
                        email = 'testuser@test.com',
                        password = 'testuser',
                                            )
        self.home_url = reverse('home')

    def test_login_required_to_view(self):
        response = self.client.get(self.home_url)
        self.assertRedirects(response, "/login/?next=/home/")

    def test_never_cache(self):
        '''
        Test if the server instructs the client not to cache
        '''
        self.client.login(email='testuser@test.com',password='testuser')
        response = self.client.get(self.home_url)
        cache_control = response['Cache-Control'].split(',')
        print(cache_control)
        self.assertEqual(cache_control[1].strip(), 'no-cache')

    def test_correct_template_used(self):
        '''
        Test if the designated template is being used
        '''

        self.client.login(email='testuser@test.com',password='testuser')
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'base1.html')
        
        

class TestLogoutView(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
                        name = "testuser",
                        email = 'testuser@test.com',
                        password = 'testuser',
                                            )

    def test_logout_view(self):
        self.client.login(email=self.user.email,password=self.user.password)
        response = self.client.get(reverse_lazy('logout'))
        #test if the session is destroyed
        self.assertNotIn('_auth_user_id', self.client.session)




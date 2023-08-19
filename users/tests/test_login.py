from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group


class LoginTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_path = reverse('users:login')
        self.user_raw_password = "password"

        self.end_user_group = Group.objects.create(name="end_users")
        self.engineers_group = Group.objects.create(name="engineers")

        self.user = User.objects.create_user(username='test-std-user',
                                             password=self.user_raw_password)
        self.superuser = User.objects.create_superuser(username='test-admin-user',
                                                       password=self.user_raw_password)

    def test_get_happy_path_login(self):
        #Ensure Login Page works
        response = self.client.get(self.login_path)
        self.assertEqual(response.status_code, 200)

    def test_post_happy_path_user_login(self):
        #Ensure std user is able to login
        data = {
            "username": self.user.username,
            "password": self.user_raw_password
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        #Ensure user is redirected to the home page
        self.assertTrue(response.client.cookies.get('sessionid') is not None)
        self.assertRedirects(response, "/", status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        #Ensure user cannot access built in django admin page
        response = self.client.get("/admin/", follow=True)
        self.assertRedirects(response, "/admin/login/?next=/admin/", status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_post_happy_path_superuser_login(self):
        #Ensure admin user is able to login
        data = {
            "username": self.superuser.username,
            "password": self.user_raw_password
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        #Ensure admin user is redirected to the home page
        self.assertTrue(response.client.cookies.get('sessionid') is not None)
        self.assertRedirects(response, "/", status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        #Ensure admin user can access built in django admin page
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)

    def test_login_empty_username(self):
        #Ensure site cannot be accessed with no username entered
        data = {
            "username": "",
            "password": self.user_raw_password
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_login_empty_password(self):
        #Ensure site cannot be accessed with no password entered
        data = {
            "username": self.superuser.username,
            "password": ""
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_login_invalid_username(self):
        #Ensure site does not progress if a non-existent username is entered
        data = {
            "username": "ThisUs3rDoes-notExist",
            "password": self.user_raw_password
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        self.assertContains(response,
                            "Please enter a correct username and password. "
                            "Note that both fields may be case-sensitive.",
                            status_code=401)

    def test_login_invalid_password(self):
        #Ensure site does not progress if an incorrect password is entered
        data = {
            "password": self.user.username,
            "username": "ThisIs4BadPa55"
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        self.assertContains(response,
                            "Please enter a correct username and password. "
                            "Note that both fields may be case-sensitive.",
                            status_code=401)

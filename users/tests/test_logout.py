from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class LogoutTests(TestCase):

    def setUp(self):
        #Test user is standard user
        self.client = Client()
        self.logout_path = reverse('users:logout')
        self.user_raw_password = "password"
        self.user = User.objects.create_user(username='test-std-user',
                                             password=self.user_raw_password)

    def test_post_logged_in_user(self):
        #Logged in user is logged out and returned to the login screen
        self.client.login(username=self.user.username, password=self.user_raw_password)
        response = self.client.post(self.logout_path, follow=True)
        self.assertRedirects(response, "/access/login/", status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_post_not_logged_in_user(self):
        #Logged out user should not move from 'unauthenticated' state
        response = self.client.post(self.logout_path, follow=True)
        self.assertEqual(response.status_code, 401)

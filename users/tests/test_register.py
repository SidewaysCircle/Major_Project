from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group


class RegisterTests(TestCase):

    def setUp(self):
        #Users using register page will not be superusers by default
        #Superusers are defined within the 'admin' console
        self.client = Client()
        self.register_path = reverse('users:register')

        self.end_user_group = Group.objects.create(name="end_users")
        self.engineers_group = Group.objects.create(name="engineers")

    def test_get_register_page(self):
        #Ensure register page opens
        response = self.client.get(self.register_path)
        self.assertEqual(response.status_code, 200)

    def test_post_register_page(self):
        #Ensure successful registration of the standard (non-admin) user used for std user testing
        username = "test-std-user"
        password = "TheM0stSecurePa55!"
        data = {
            "username": username,
            "password1": password,
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        user = User.objects.get(username=username)
        self.assertIsNotNone(user)
        self.assertNotEqual(user.password, password)
        #Ensure registered user cannot access Admin page
        response = self.client.get("/admin/", follow=True)
        self.assertRedirects(response, "/admin/login/?next=/admin/", status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_post_empty_username(self):
        #Ensure new user cannot be created without a username
        password = "TheM0stSecurePa55!"
        data = {
            "username": "",
            "password1": password,
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_post_empty_password1(self):
        #Ensure new user cannot be created without the password being confirmed in 1st password field
        username = "test-std-user"
        password = "TheM0stSecurePa55!"
        data = {
            "username": username,
            "password1": "",
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_post_empty_password2(self):
        #Ensure new user cannot be created without the password being confirmed in 2nd password field
        username = "test-std-user"
        password = "TheM0stSecurePa55!"
        data = {
            "username": username,
            "password1": password,
            "password2": ""
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_post_invalid_username(self):
        #Ensure the username can only be alphanumeric with certain special chars
        password = "TheM0stSecurePa55!"
        data = {
            "username": "Th!sUserW0n'tW-rk",
            "password1": password,
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response,
                            "Enter a valid username. This value may contain only letters, "
                            "numbers, and @/./+/-/_ characters.",
                            status_code=401)

    def test_post_invalid_password(self):
        #Ensure complex passwords are required
        username = 'test'
        password = "password"
        data = {
            "username": username,
            "password1": password,
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "This password is too common.", status_code=401)

    def test_post_register_with_same_username(self):
        #Ensure dupliacate users cannot be registered
        username = "test-dupe-user"
        password = "TheM0stSecurePa55!"
        data = {
            "username": username,
            "password1": password,
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertRedirects(response, "/", status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertIsNotNone(User.objects.get(username=username))
        self.client.logout()
        # Register 2nd user with same details
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "A user with that username already exists.", status_code=401)

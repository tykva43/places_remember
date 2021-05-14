from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase


class UnauthViewsTestCase(TestCase):
    """Testcase that checks views in case the user is unauthorized"""

    def test_login_loads_properly(self):
        """The login page loads properly"""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_home_redirects_properly(self):
        """The home page redirects to another (login) page"""
        response = self.client.get('/', follow=True)
        self.assertEqual(response.redirect_chain[-1], ('/login/?next=/', 302))

    def test_logout_redirects_properly(self):
        """The logout page redirects to another (login) page"""
        response = self.client.get('/logout/', follow=True)
        self.assertEqual(response.redirect_chain[-1], ('/login/', 302))

    def test_memory_add_redirects_properly(self):
        """The add_memo page redirects to another (login) page"""
        response = self.client.get('/memory/add/', follow=True)
        self.assertEqual(response.redirect_chain[-1], ('/login/?next=/memory/add/', 302))


class AuthViewsTestCase(TestCase):
    """Testcase that checks views in case the user is authorized"""

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def setUp(cls):
        """Create test user object and authorize it"""

        cls.test_user = User.objects.create(
            username='test',
            email='test@test.com',
            password='testest')
        cls.client.force_login(user=cls.test_user)

    def test_login_redirects_properly(self):
        """The login page redirects to another (home) page"""
        response = self.client.get('/login/', follow=True)
        self.assertEqual(response.redirect_chain[-1], ('/', 302))

    def test_home_loads_properly(self):
        """The home page loads properly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects_properly(self):
        """The logout page redirects to another (login) page and log out the user"""
        response = self.client.get('/logout/', follow=True)
        self.assertEqual(response.redirect_chain[-1], ('/login/', 302))
        # todo: check the user is logged out

    def test_memory_add_loads_properly(self):
        """The add_memo page loads properly"""
        response = self.client.get('/memory/add/')
        self.assertEqual(response.status_code, 200)

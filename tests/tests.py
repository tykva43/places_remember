from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from places_remember.models import Memo


class UnauthViewsTestCase(TestCase):
    """Testcase that checks views in case the user is unauthorized"""

    def test_login_loads_properly(self):
        """The login page loads properly"""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_home_redirects_properly(self):
        """The home page redirects to another (login) page"""
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1], ('/login/?next=/', 302))

    def test_logout_redirects_properly(self):
        """The logout page redirects to another (login) page"""
        response = self.client.get('/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1], ('/login/', 302))

    def test_memory_add_redirects_properly(self):
        """The add_memo page redirects to another (login) page"""
        response = self.client.get('/memory/add/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1], ('/login/?next=/memory/add/', 302))


class AuthViewsTestCase(TestCase):
    """Testcase that checks views in case the user is authorized"""

    @classmethod
    def setUpTestData(cls):
        """Create test user object"""
        cls.client = Client()
        cls.test_user = User.objects.create(
            username='test',
            email='test@test.com',
            password='testest')

    def setUp(self):
        """Authorize test user"""
        self.client.force_login(user=self.test_user)

    def test_login_redirects_properly(self):
        """The login page redirects to another (home) page"""
        response = self.client.get('/login/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1], ('/', 302))

    def test_home_loads_properly(self):
        """The home page loads properly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects_properly(self):
        """The logout page redirects to another (login) page and log out the user"""
        response = self.client.get('/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1], ('/login/', 302))
        # Check the user is logged out
        self.assertFalse(response.context['user'].is_authenticated)

    def test_memory_add_loads_properly(self):
        """The add_memo page loads properly"""
        response = self.client.get('/memory/add/')
        self.assertEqual(response.status_code, 200)


class FunctionalityTestCase(TestCase):
    """Testcase that tests basic functionalities (creating a memory and displaying it)"""

    @classmethod
    def setUpTestData(cls):
        """Create test user"""
        cls.client = Client(enforce_csrf_checks=True)
        cls.test_user1 = User.objects.create_user('test1', 'test@test.com', 'test')
        cls.test_user2 = User.objects.create_user('test2', 'test2@test.com', 'test')

    def setUp(self):
        """Authorize test user"""
        self.client.force_login(user=self.test_user1)

    def test_creating_memos(self):
        data = {'name': 'testname', 'place': 'testplace', 'commentary': 'testcommentary'}
        response = self.client.post('/memory/add/', data=data, follow=True)
        # Check that there is redirected to home page after saving memo
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1], ('/', 302))

        # Check that memory is created
        memories = Memo.objects.filter(user_id=self.test_user1.id)
        new_memo = memories[0]
        self.assertEqual(new_memo.name, data['name'])
        self.assertEqual(new_memo.place, data['place'])
        self.assertEqual(new_memo.commentary, data['commentary'])
        self.assertEqual(new_memo.user.id, self.test_user1.id)

        # Check that user memories data was sent with response
        self.assertQuerysetEqual(response.context['memories'], memories)

    def test_displaying_memos(self):
        # Create memories from two different users
        Memo.objects.create(name='testname1', place='testplace1', commentary='testcommentary1',
                            user_id=self.test_user1.id)
        Memo.objects.create(name='testname2', place='testplace2', commentary='testcommentary2',
                            user_id=self.test_user2.id)
        # Go to home page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check that the page contains only one user data
        memories = Memo.objects.filter(user_id=self.test_user1.id)
        self.assertQuerysetEqual(response.context['memories'], memories)

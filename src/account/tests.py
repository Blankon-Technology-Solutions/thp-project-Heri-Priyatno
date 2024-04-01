from django.contrib.auth import get_user
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from account.models import User


# Create your tests here.

class TestAuthView(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='email@localhost.com',
                                             password='r4h451401')

    def test_login(self):
        with self.subTest('Valid login'):
            data = dict(password='r4h451401', username='email@localhost.com')
            url = reverse('login')
            response = self.client.post(url, data, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(get_user(self.client).is_authenticated)


class TestAccountAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='email@localhost.com',
                                             password='r4h451401')
        self.user_2 = User.objects.create_user(email='email2@localhost.com',
                                               password='r4h451401')

    def test_login_api(self):
        with self.subTest('Valid login'):
            data = dict(password='r4h451401', email='email@localhost.com')
            url = reverse('login-api')
            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, 200)
        with self.subTest('Invalid login'):
            data = dict(password='r4h451401123', email='email@localhost.com')
            url = reverse('login-api')
            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, 400)

    def test_register_api(self):
        with self.subTest('With new account'):
            data = dict(password='r4h451401', email='email3@localhost.com')
            url = reverse('register-api')
            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, 200)

        with self.subTest('With existing account'):
            data = dict(password='r4h451401', email='email2@localhost.com')
            url = reverse('register-api')
            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, 400)


class TestClasses(TestCase):
    def test_user_manager(self):
        email = 'user@localhost'
        test_pass = '12345'
        user = User.objects.create_user(email=email, password=test_pass)

        filter_user = User.objects.filter(email=email)
        self.assertEqual(filter_user.count(), 1)
        data_user = filter_user.first()

    def test_user_manager_create_superuser(self):
        email = 'superuser@localhost'
        test_pass = '12345'
        user = User.objects.create_superuser(email=email, password=test_pass)

        filter_user = User.objects.filter(email=email)
        self.assertEqual(filter_user.count(), 1)
        data_user = filter_user.first()
        self.assertTrue(data_user.is_staff)
        self.assertTrue(data_user.is_superuser)

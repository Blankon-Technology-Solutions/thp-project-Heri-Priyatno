from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from account.models import User


# Create your tests here.


class TestTodoApi(APITestCase):
    def setUp(self):
        self.payload_1 = {
            'title': 'Todo Title',
            'completed': False
        }
        self.payload_2 = {
            'title': 'Todo Title 2',
            'completed': True
        }
        self.user = User.objects.create_user(email='email@localhost.com',
                                             password='r4h451401')
        self.user_2 = User.objects.create_user(email='email2@localhost.com',
                                               password='r4h451401')

    def test_create_api(self):
        url = reverse('todo-list')
        data_todo = {
            'title': 'Todo Title',
        }
        with self.subTest('No user login'):
            response_fail = self.client.post(url, data=self.payload_1)
            self.assertEqual(response_fail.status_code, 403)

        with self.subTest('User is login'):
            self.client.force_login(self.user)
            response = self.client.post(url, data=self.payload_1)
            self.assertEqual(response.status_code, 201)

            response_list = self.client.get(url)
            self.assertEqual(response_list.status_code, 200)
            data = response_list.data
            self.assertEqual(len(data), 1)

            self.client.force_login(self.user_2)
            response_list = self.client.get(url)
            self.assertEqual(response_list.status_code, 200)
            data_list = response_list.data
            self.assertEqual(len(data_list), 0)


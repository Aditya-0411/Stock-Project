from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

class RegisterViewTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.valid_payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }

    def test_registration_success(self):
        response = self.client.post(self.register_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    # def test_registration_failure(self):
    #     invalid_payload = {
    #         'username': 'test',
    #         'email': 'test@example.com',
    #         'password': 'testpassword'
    #     }
    #     response = self.client.post(self.register_url, invalid_payload)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(User.objects.count(), 0)  # No user should be created

    # Add more test cases as needed


class LoginViewTest(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_success(self):
        url = reverse('login')
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertTrue('access_token' in response.data)
        #self.assertTrue('refresh_token' in response.data)
        self.assertTrue('user' in response.data['data'])
        self.assertEqual(response.data['data']['user']['username'], self.username)

    # def test_login_failure(self):
    #     url = reverse('login')
    #     # Incorrect password
    #     data = {'username': self.username, 'password': 'wrongpassword'}
    #     response = self.client.post(url, data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertEqual(response.data['status'], 'error')
    #     self.assertEqual(response.data['data'], 'Invalid credentials')
    #
    #     # Non-existent user
    #     data = {'username': 'nonexistentuser', 'password': 'testpassword'}
    #     response = self.client.post(url, data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertEqual(response.data['status'], 'error')
    #     self.assertEqual(response.data['data'], 'Invalid credentials')
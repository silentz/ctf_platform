from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class AuthenticationTests(APITestCase):

    def register_user(self, username, password):
        """
        Help function for easier user registration during testing
        """
        url = reverse('register')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        return response

    def test_register_account(self):
        """
        Ensure registration works
        """
        response = self.register_user('testuser0', 'test')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'ok')

    def test_log_in(self):
        """
        Ensure authentication works
        """
        url = reverse('login')
        data = {'username': 'testuser1', 'password': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], 'bad')

        self.register_user('testuser1', 'test')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')

    def test_logout(self):
        """
        Ensure logout works
        """
        url_logout = reverse('logout')
        url_login = reverse('login')
        self.register_user('testuser2', 'test')
        data = {'username': 'testuser2', 'password': 'test'}
        response = self.client.post(url_login, data, format='json')
        response_2 = self.client.get(url_logout, cookies=response.cookies, format='json')
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.data['status'], 'ok')

        # test logout without logging in
        response = self.client.get(url_logout, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

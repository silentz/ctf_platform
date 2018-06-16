from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


class UserTests(APITestCase):

    def create_user(self, login, password, is_staff=False):
        user = User(username=login)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()

    def setUp(self):
        self.create_user('test', 'test', False)
        self.create_user('admin', 'admin', True)
        self.create_user('user', 'user', False)

    def test_list_as_anon(self):
        url = reverse('user-list')
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_as_user(self):
        url = reverse('user-list')
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_as_admin(self):
        url = reverse('user-list')
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_as_anon(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_as_user(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'test')

    def test_retrieve_as_admin(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'test')

    def test_create_as_anon(self):
        url = reverse('user-list')
        self.client.logout()
        data = {'username': 'test2', 'password': 'test'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_user(self):
        url = reverse('user-list')
        self.client.login(username='user', password='user')
        data = {'username': 'test2', 'password': 'test'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_as_admin(self):
        url = reverse('user-list')
        self.client.login(username='admin', password='admin')
        data = {'username': 'test2', 'password': 'test'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_as_anon(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'username': 'test_new_username', 'password': 'test'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_user(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'username': 'test_new_username', 'password': 'test'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_as_admin(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'username': 'test_new_username', 'password': 'test'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update_as_anon(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'username': 'test_name'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_user(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'username': 'test_name'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update_as_admin(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'username': 'test_name'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_as_anon(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_user(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_as_admin(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

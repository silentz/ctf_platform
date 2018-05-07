from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Category
from django.contrib.auth.models import User


class CategoryTests(APITestCase):

    def create_instance(self, name, color='#FFFFFF'):
        Category.objects.create(name=name, color=color)

    def create_user(self, login, password, is_staff=False):
        user = User(username=login)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()

    def setUp(self):
        self.create_instance('test1')
        self.create_instance('test2')
        self.create_instance('test3', '#abcdef')
        self.create_instance('test4', '#000000')
        self.create_user('admin', 'admin', True)
        self.create_user('user', 'user', False)

    def test_list_as_anon(self):
        url = reverse('category-list')
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_as_user(self):
        url = reverse('category-list')
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_list_as_admin(self):
        url = reverse('category-list')
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_as_anon(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_as_user(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test1')

    def test_retrieve_as_admin(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test1')

    def test_create_as_anon(self):
        url = reverse('category-list')
        self.client.logout()
        data = {'name': 'test100', 'color': '#aaaaaa'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_user(self):
        url = reverse('category-list')
        self.client.login(username='user', password='user')
        data = {'name': 'test100', 'color': '#aaaaaa'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_admin(self):
        url = reverse('category-list')
        self.client.login(username='admin', password='admin')
        data = {'name': 'test100', 'color': '#aaaaaa'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'test100')
        self.assertEqual(response.data['color'], '#aaaaaa')

    def test_update_as_anon(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'name': 'new name', 'color': '#123211'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_user(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'name': 'new name', 'color': '#123211'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_admin(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'name': 'new name', 'color': '#123211'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'new name')
        self.assertEqual(response.data['color'], '#123211')

    def test_partial_update_as_anon(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'name': 'new name 2'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_user(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'name': 'new name 2'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_admin(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'name': 'new name 2'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'new name 2')

    def test_delete_as_anon(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_user(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_admin(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

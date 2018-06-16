from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User, Group
from api.models import GroupAdditional


class GroupTests(APITestCase):

    def create_instance(self, name, invite_code):
        group = Group.objects.create(name=name)
        GroupAdditional.objects.create(group=group, invite_code=invite_code)

    def create_user(self, login, password, is_staff=False):
        user = User(username=login)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()

    def setUp(self):
        self.create_user('admin', 'admin', True)
        self.create_user('user', 'user', False)
        self.create_instance('test', 'test')
        self.create_instance('test10', 'test')
        self.create_instance('test100', 'test')

    def test_list_as_anon(self):
        url = reverse('group-list')
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_as_user(self):
        url = reverse('group-list')
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_as_admin(self):
        url = reverse('group-list')
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_as_anon(self):
        url = reverse('group-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_as_user(self):
        url = reverse('group-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test')

    def test_retrieve_as_admin(self):
        url = reverse('group-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(response.data['invite_code'], 'test')

    def test_create_as_anon(self):
        url = reverse('group-list')
        self.client.logout()
        data = {'name': 'test2', 'invite_code': 'test'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_user(self):
        url = reverse('group-list')
        self.client.login(username='user', password='user')
        data = {'name': 'test2', 'invite_code': 'test'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_admin(self):
        url = reverse('group-list')
        self.client.login(username='admin', password='admin')
        data = {'name': 'test2', 'invite_code': 'test'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_as_anon(self):
        url = reverse('group-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'name': 'new_name', 'invite_code': 'new_code'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_user(self):
        url = reverse('group-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'name': 'new_name', 'invite_code': 'new_code'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_admin(self):
        url = reverse('group-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'name': 'new_name', 'invite_code': 'new_code'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'new_name')
        self.assertEqual(response.data['invite_code'], 'new_code')

    def test_partial_update_as_anon(self):
        url = reverse('group-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'name': 'new_name_2'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_user(self):
        url = reverse('group-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'name': 'new_name_2'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_admin(self):
        url = reverse('group-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'name': 'new_name_2'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'new_name_2')

    def test_delete_as_anon(self):
        url = reverse('group-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_user(self):
        url = reverse('group-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_admin(self):
        url = reverse('group-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_access_as_anon(self):
        url = reverse('group-access', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.post(url, data={'invite_code': 'test'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_as_user(self):
        url = reverse('group-access', kwargs={'pk': 1})
        self.client.login(username='user', password='user')

        response = self.client.post(url, data={'invite_code': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(url, data={'invite_code': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_as_admin(self):
        url = reverse('group-access', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')

        response = self.client.post(url, data={'invite_code': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(url, data={'invite_code': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Contest, Message
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta


class MessageTests(APITestCase):

    def create_instance(self, name, start_datetime, finish_datetime, allowed_groups, text):
        contest = Contest(name=name, start_datetime=start_datetime, finish_datetime=finish_datetime)
        contest.save()
        contest.allowed_groups.set(allowed_groups)
        contest.save()
        msg = Message(contest=contest, text=text)
        msg.save()

    def create_user(self, login, password, is_staff=False):
        user = User(username=login)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()

    def setUp(self):
        allowed_groups = [Group.objects.create(name='TestGroup')]
        # finished contest message
        self.create_instance('contest1', datetime(2000, 1, 1), datetime(2000, 1, 2), allowed_groups, 'test')
        # not started contest message
        self.create_instance('contest2', datetime.now() + timedelta(10),
                             datetime.now() + timedelta(20), allowed_groups, 'test')
        # opened contest message
        self.create_instance('contest3', datetime(2000, 1, 1), datetime.now() + timedelta(10),
                             allowed_groups, 'test')
        # opened training task
        self.create_instance('contest4', datetime(2000, 1, 1), None, allowed_groups, 'test')

        self.create_user('admin', 'admin', is_staff=True)
        self.create_user('user', 'user', is_staff=False)

    def test_list_as_anon(self):
        url = reverse('message-list')
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_as_user(self):
        url = reverse('message-list')
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertTrue('text' not in response.data[1])

    def test_list_as_admin(self):
        url = reverse('message-list')
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertTrue('text' not in response.data[1])

    def test_retrieve_as_anon(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_as_user(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('message-detail', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('message-detail', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('message-detail', kwargs={'pk': 4})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_as_admin(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('message-detail', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('message-detail', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('message-detail', kwargs={'pk': 4})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_as_anon(self):
        url = reverse('message-list')
        self.client.logout()
        data = {'text': 'test2', 'contest': reverse('contest-detail', kwargs={'pk': 1})}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_user(self):
        url = reverse('message-list')
        self.client.login(username='user', password='user')
        data = {'text': 'test2', 'contest': reverse('contest-detail', kwargs={'pk': 1})}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_admin(self):
        url = reverse('message-list')
        self.client.login(username='admin', password='admin')
        data = {'text': 'test2', 'contest': reverse('contest-detail', kwargs={'pk': 1})}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'test2')

    def test_update_as_anon(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'text': 'test3', 'contest': reverse('contest-detail', kwargs={'pk': 1})}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_user(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'text': 'test3', 'contest': reverse('contest-detail', kwargs={'pk': 1})}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_admin(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'text': 'test3', 'contest': reverse('contest-detail', kwargs={'pk': 1})}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'test3')

    def test_partial_update_as_anon(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'text': 'test4'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_user(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'text': 'test4'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_admin(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'text': 'test4'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'test4')

    def test_delete_as_anon(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_user(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_admin(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

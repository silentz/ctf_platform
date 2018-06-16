from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Contest, Message
from django.contrib.auth.models import User, Group


class MessageTests(APITestCase):

    def create_instance(self, name, start_datetime, finish_datetime, allowed_groups, text, training=False):
        contest = Contest(name=name, start_datetime=start_datetime, finish_datetime=finish_datetime, training=training)
        contest.save()
        contest.allowed_groups.set(allowed_groups)
        contest.save()
        msg = Message(contest=contest, text=text)
        msg.save()
        return contest

    def create_user(self, login, password, is_staff=False):
        user = User(username=login)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()
        return user

    def setUp(self):
        group = Group.objects.create(name='TestGroup')
        allowed_groups = [group]
        # opened training task
        self.contest = self.create_instance('contest4', None, None, allowed_groups, 'test', True)
        self.contest_id = self.contest.id
        self.contest = str(self.contest.id)

        group.user_set.add(self.create_user('admin', 'admin', is_staff=True))
        group.user_set.add(self.create_user('user', 'user', is_staff=False))

    def test_list_as_anon(self):
        url = reverse('message-list') + "?for=" + self.contest
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_as_user(self):
        url = reverse('message-list') + "?for=" + self.contest
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_as_admin(self):
        url = reverse('message-list') + "?for=" + self.contest
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_as_anon(self):
        url = reverse('message-detail', kwargs={'pk': 1}) + "?for=" + self.contest
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_as_user(self):
        url = reverse('message-detail', kwargs={'pk': 1}) + "?for=" + self.contest
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_as_admin(self):
        url = reverse('message-detail', kwargs={'pk': 1}) + "?for=" + self.contest
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_as_anon(self):
        url = reverse('message-list') + "?for=" + self.contest
        self.client.logout()
        data = {'text': 'test2', 'contest': self.contest_id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_user(self):
        url = reverse('message-list') + "?for=" + self.contest
        self.client.login(username='user', password='user')
        data = {'text': 'test2', 'contest': self.contest_id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_admin(self):
        url = reverse('message-list') + "?for=" + self.contest
        self.client.login(username='admin', password='admin')
        data = {'text': 'test2', 'contest': self.contest_id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'test2')

    def test_update_as_anon(self):
        url = reverse('message-detail', kwargs={'pk': 1}) + "?for=" + self.contest
        self.client.logout()
        data = {'text': 'test3', 'contest': self.contest_id}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_user(self):
        url = reverse('message-detail', kwargs={'pk': 1}) + "?for=" + self.contest
        self.client.login(username='user', password='user')
        data = {'text': 'test3', 'contest': self.contest_id}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_admin(self):
        url = reverse('message-detail', kwargs={'pk': 1}) + "?for=" + self.contest
        self.client.login(username='admin', password='admin')
        data = {'text': 'test3', 'contest': self.contest_id}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'test3')

    def test_partial_update_as_anon(self):
        url = reverse('message-detail', kwargs={'pk': 1}) + "?for=" + self.contest
        self.client.logout()
        data = {'text': 'test4'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_user(self):
        url = reverse('message-detail', kwargs={'pk': 1}) + "?for=" + self.contest
        self.client.login(username='user', password='user')
        data = {'text': 'test4'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_admin(self):
        url = reverse('message-detail', kwargs={'pk': 1}) + "?for=" + self.contest
        self.client.login(username='admin', password='admin')
        data = {'text': 'test4'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'test4')

    def test_delete_as_anon(self):
        url = reverse('message-detail', kwargs={'pk': 1}) + "?for=" + self.contest
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_user(self):
        url = reverse('message-detail', kwargs={'pk': 1}) + "?for=" + self.contest
        self.client.login(username='user', password='user')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_admin(self):
        url = reverse('message-detail', kwargs={'pk': 1}) + "?for=" + self.contest
        self.client.login(username='admin', password='admin')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

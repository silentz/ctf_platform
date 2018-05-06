from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Contest, Task
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta


class TaskTests(APITestCase):

    def create_instance(self, name, start_datetime, finish_datetime, allowed_groups, score, description,
                        flag, category, solved=[], use_generator=False, token='tmp'):
        contest = Contest(name=name, start_datetime=start_datetime, finish_datetime=finish_datetime)
        contest.save()
        contest.allowed_groups.set(allowed_groups)
        contest.save()
        task = Task(name=name, score=score, description=description, contest=contest,
                    flag=flag, category=category, use_generator=use_generator, token=token)
        task.save()
        task.solved.set(solved)
        task.save()

    def create_user(self, login, password, is_staff=False):
        user = User(username=login)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()

    def setUp(self):
        allowed_groups = [Group.objects.create(name='TestGroup')]
        # finished contest task
        self.create_instance('task1', datetime(2000, 1, 1), datetime(2000, 1, 2), allowed_groups,
                             100, 'tmp', 'tmp{tmp}', None)
        # not started contest task
        self.create_instance('task2', datetime.now() + timedelta(10),
                             datetime.now() + timedelta(20), allowed_groups, 200, 'tmp', 'tmp{tmp}', None)
        # opened contest task
        self.create_instance('task3', datetime(2000, 1, 1), datetime.now() + timedelta(10), allowed_groups,
                             300, 'tmp', 'tmp{tmp}', None)
        # opened training task
        self.create_instance('task4', datetime(2000, 1, 1), None, allowed_groups, 400, 'tmp', 'tmp{tmp}', None)

        self.create_user('admin', 'admin', is_staff=True)
        self.create_user('user', 'user', is_staff=False)

    def test_list_as_anon(self):
        url = reverse('task-list')
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_as_user(self):
        url = reverse('task-list')
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_as_admin(self):
        url = reverse('task-list')
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_as_anon(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_as_user(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('task-detail', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('task-detail', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('task-detail', kwargs={'pk': 4})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_as_admin(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('task-detail', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('task-detail', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('task-detail', kwargs={'pk': 4})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_as_anon(self):
        url = reverse('task-list')
        self.client.logout()
        data = {'name': 'task5', 'flag': 'tmp', 'score': 100, 'description': 'tmp',
                'use_generator': False, 'token': 'tmp'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_user(self):
        url = reverse('task-list')
        self.client.login(username='user', password='user')
        data = {'name': 'task5', 'flag': 'tmp', 'score': 100, 'description': 'tmp',
                'use_generator': False, 'token': 'tmp'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_admin(self):
        url = reverse('task-list')
        self.client.login(username='admin', password='admin')
        data = {'name': 'task5', 'flag': 'tmp', 'score': 100, 'description': 'tmp',
                'use_generator': False, 'token': 'tmp', 'solved': []}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'task5')

    def test_update_as_anon(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'name': 'task100', 'flag': 'tmp', 'score': 100, 'description': 'tmp',
                'use_generator': False, 'token': 'tmp'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_user(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'name': 'task100', 'flag': 'tmp', 'score': 100, 'description': 'tmp',
                'use_generator': False, 'token': 'tmp'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_admin(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'name': 'task100', 'flag': 'tmp', 'score': 100, 'description': 'tmp',
                'use_generator': False, 'token': 'tmp'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'task100')

    def test_partial_update_as_anon(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'name': 'new_name'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_user(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'name': 'new_name'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_admin(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'name': 'new_name'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'new_name')

    def test_delete_as_anon(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_user(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_admin(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

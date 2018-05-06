from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Flag, Task, Contest
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta


class FlagTests(APITestCase):

    def create_task(self, name, start_datetime, finish_datetime, allowed_groups, score, description,
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
        return task

    def create_instance(self, task, flag, used):
        obj = Flag(task=task, flag=flag, used=used)
        obj.save()

    def create_user(self, login, password, is_staff=False):
        user = User(username=login)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()

    def setUp(self):
        allowed_groups = [Group.objects.create(name='TestGroup')]
        self.task = self.create_task('task', datetime(2000, 1, 1), None,
                                     allowed_groups, 400, 'tmp', 'tmp{tmp}', None)
        self.create_instance(self.task, 'tmp{tmp}', False)

        self.create_user('admin', 'admin', is_staff=True)
        self.create_user('user', 'user', is_staff=False)

    def test_list_as_anon(self):
        url = reverse('flag-list')
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_as_user(self):
        url = reverse('flag-list')
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_as_admin(self):
        url = reverse('flag-list')
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_as_anon(self):
        url = reverse('flag-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_as_user(self):
        url = reverse('flag-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_as_admin(self):
        url = reverse('flag-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_as_anon(self):
        url = reverse('flag-list')
        self.client.logout()
        task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'task': task_url, 'flag': 'created{flag}', 'used': False}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_user(self):
        url = reverse('flag-list')
        self.client.login(username='user', password='user')
        task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'task': task_url, 'flag': 'created{flag}', 'used': False}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_admin(self):
        url = reverse('flag-list')
        self.client.login(username='admin', password='admin')
        task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'task': task_url, 'flag': 'created{flag}', 'used': False}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['flag'], 'created{flag}')

    def test_update_as_anon(self):
        url = reverse('flag-detail', kwargs={'pk': 1})
        self.client.logout()
        task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'task': task_url, 'flag': 'updated{flag}', 'used': False}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_user(self):
        url = reverse('flag-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'task': task_url, 'flag': 'updated{flag}', 'used': False}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_admin(self):
        url = reverse('flag-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'task': task_url, 'flag': 'updated{flag}', 'used': False}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['flag'], 'updated{flag}')

    def test_partial_update_as_anon(self):
        url = reverse('flag-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'flag': 'new_flag'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_user(self):
        url = reverse('flag-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'flag': 'new_flag'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_admin(self):
        url = reverse('flag-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'flag': 'new_flag'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['flag'], 'new_flag')

    def test_delete_as_anon(self):
        url = reverse('flag-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_user(self):
        url = reverse('flag-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_admin(self):
        url = reverse('flag-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

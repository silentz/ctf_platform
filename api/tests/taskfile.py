from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Contest, Task, TaskFile
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta
import io
import pytz
from django.core.files import File


class TaskFileTests(APITestCase):

    def create_task(self, name, start_datetime, finish_datetime, allowed_groups, score, description,
                    flag, category, training=False):
        contest = Contest(name=name, start_datetime=start_datetime, finish_datetime=finish_datetime, training=training)
        contest.save()
        contest.allowed_groups.set(allowed_groups)
        contest.save()
        task = Task(name=name, score=score, description=description, contest=contest,
                    flag=flag, category=category)
        task.save()
        return task

    def create_instance(self, name, task, file):
        tfile = TaskFile(task=task, name=name, file=File(file))
        tfile.save()

    def create_user(self, login, password, is_staff=False):
        user = User(username=login)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()
        return user

    def setUp(self):
        group = Group.objects.create(name='TestGroup')
        allowed_groups = [group]
        self.task = self.create_task('task4', None, None, allowed_groups, 400, 'tmp', 'tmp{tmp}', None, True)
        self.create_instance(task=self.task, name='test.test', file=io.StringIO("some initial text data"))
        group.user_set.add(self.create_user('admin', 'admin', is_staff=True))
        group.user_set.add(self.create_user('user', 'user', is_staff=False))

    def test_list_as_anon(self):
        url = reverse('taskfile-list')
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_as_user(self):
        url = reverse('taskfile-list')
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_as_admin(self):
        url = reverse('taskfile-list')
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_as_anon(self):
        url = reverse('taskfile-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_as_user(self):
        url = reverse('taskfile-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_as_admin(self):
        url = reverse('taskfile-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_as_anon(self):
        url = reverse('taskfile-list')
        self.client.logout()
        data = {'name': 'test2.test', 'task': self.task.id, 'file': io.StringIO('test')}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_user(self):
        url = reverse('taskfile-list')
        self.client.login(username='user', password='user')
        data = {'name': 'test2.test', 'task': self.task.id, 'file': io.StringIO('test')}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_admin(self):
        url = reverse('taskfile-list')
        self.client.login(username='admin', password='admin')
        data = {'name': 'test2.test', 'task': self.task.id, 'file': io.StringIO('test')}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_as_anon(self):
        url = reverse('taskfile-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'name': 'test3.test', 'task': self.task.id, 'file': io.StringIO('test')}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_user(self):
        url = reverse('taskfile-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'name': 'test3.test', 'task': self.task.id, 'file': io.StringIO('test')}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_admin(self):
        url = reverse('taskfile-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'name': 'test3.test', 'task': self.task.id, 'file': io.StringIO('test')}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test3.test')

    def test_partial_update_as_anon(self):
        url = reverse('taskfile-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'name': 'new_name'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_user(self):
        url = reverse('taskfile-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'name': 'new_name'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_admin(self):
        url = reverse('taskfile-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'name': 'new_name'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'new_name')

    def test_delete_as_anon(self):
        url = reverse('taskfile-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_user(self):
        url = reverse('taskfile-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_admin(self):
        url = reverse('taskfile-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Contest, Task, Hint
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta
import io
from django.core.files import File


class HintTests(APITestCase):

    def create_task(self, name, start_datetime, finish_datetime, allowed_groups, score, description,
                    flag, category):
        contest = Contest(name=name, start_datetime=start_datetime, finish_datetime=finish_datetime)
        contest.save()
        contest.allowed_groups.set(allowed_groups)
        contest.save()
        task = Task(name=name, score=score, description=description, contest=contest,
                    flag=flag, category=category)
        task.save()
        return task

    def create_instance(self, task, text):
        tfile = Hint(task=task, text=text)
        tfile.save()

    def create_user(self, login, password, is_staff=False):
        user = User(username=login)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()

    def setUp(self):
        allowed_groups = [Group.objects.create(name='TestGroup')]
        self.task = self.create_task('task4', datetime(2000, 1, 1), None,
                                     allowed_groups, 400, 'tmp', 'tmp{tmp}', None)
        self.create_instance(task=self.task, text='test')
        self.create_user('admin', 'admin', is_staff=True)
        self.create_user('user', 'user', is_staff=False)

    def test_list_as_anon(self):
        url = reverse('hint-list')
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_as_user(self):
        url = reverse('hint-list')
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('text' not in response.data[0])

    def test_list_as_admin(self):
        url = reverse('hint-list')
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('text' not in response.data[0])

    def test_retrieve_as_anon(self):
        url = reverse('hint-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_as_user(self):
        url = reverse('hint-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_as_admin(self):
        url = reverse('hint-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_as_anon(self):
        url = reverse('hint-list')
        self.client.logout()
        task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'text': 'test2', 'task': task_url}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_user(self):
        url = reverse('hint-list')
        self.client.login(username='user', password='user')
        task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'text': 'test2', 'task': task_url}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_admin(self):
        url = reverse('hint-list')
        self.client.login(username='admin', password='admin')
        task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'text': 'test2', 'task': task_url}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_as_anon(self):
        url = reverse('hint-detail', kwargs={'pk': 1})
        self.client.logout()
        task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'text': 'test3', 'task': task_url}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_user(self):
        url = reverse('hint-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'text': 'test3', 'task': task_url}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_as_admin(self):
        url = reverse('hint-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'text': 'test3', 'task': task_url}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'test3')

    def test_partial_update_as_anon(self):
        url = reverse('hint-detail', kwargs={'pk': 1})
        self.client.logout()
        data = {'text': 'test4'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_user(self):
        url = reverse('hint-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        data = {'text': 'test4'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_as_admin(self):
        url = reverse('hint-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        data = {'text': 'test4'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'test4')

    def test_delete_as_anon(self):
        url = reverse('hint-detail', kwargs={'pk': 1})
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_user(self):
        url = reverse('hint-detail', kwargs={'pk': 1})
        self.client.login(username='user', password='user')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_as_admin(self):
        url = reverse('hint-detail', kwargs={'pk': 1})
        self.client.login(username='admin', password='admin')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

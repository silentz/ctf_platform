from django.db import models
from django.contrib.auth.models import User, Group


class Contest(models.Model):
    start_datetime = models.DateTimeField()
    finish_datetime = models.DateTimeField(null=True)
    allowed_groups = models.ManyToManyField(Group, related_name='allowed_contests')


class Category(models.Model):
    name = models.CharField(max_length=512)
    color = models.CharField(max_length=7)  # format: #RRGGBB


class Task(models.Model):
    name = models.CharField(max_length=512)
    score = models.IntegerField()
    description = models.TextField()  # TODO: markdown support
    contest = models.ForeignKey(Contest, related_name='tasks', null=True, on_delete=models.SET_NULL)
    flag = models.CharField(max_length=512, null=True)
    category = models.ForeignKey(Category, related_name='tasks', null=True, on_delete=models.SET_NULL)
    solved = models.ManyToManyField(User, related_name='solved_tasks')
    # for flag generator support
    use_generator = models.BooleanField(default=False)
    token = models.CharField(max_length=512)


class Flag(models.Model):
    task = models.ForeignKey(Task, related_name='generator_flags', on_delete=models.CASCADE)
    flag = models.CharField(max_length=512)
    used = models.BooleanField()


class TaskFile(models.Model):
    task = models.ForeignKey(Task, related_name='files', null=True, on_delete=models.SET_NULL)
    file = models.FileField(upload_to='media/')

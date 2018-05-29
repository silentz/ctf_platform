from django.db import models
from django.contrib.auth.models import User, Group


class Contest(models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)
    start_datetime = models.DateTimeField()
    finish_datetime = models.DateTimeField(null=True)
    allowed_groups = models.ManyToManyField(Group, related_name='allowed_contests', blank=True)


class Category(models.Model):
    name = models.CharField(max_length=512)
    color = models.CharField(max_length=7)  # format: #RRGGBB


class Task(models.Model):
    name = models.CharField(max_length=512)
    score = models.IntegerField()
    description = models.TextField()  # TODO: markdown support
    contest = models.ForeignKey(Contest, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL)
    flag = models.CharField(max_length=512, null=True)
    category = models.ForeignKey(Category, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL)

    def check_flag(self, flag):
        return flag == self.flag


class TaskSolved(models.Model):
    class Meta:
        unique_together = ('task', 'user')

    task = models.ForeignKey(Task, related_name='solved', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='solved_tasks', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)


class TaskFile(models.Model):
    task = models.ForeignKey(Task, related_name='files', null=True, blank=True, on_delete=models.SET_NULL)
    file = models.FileField(max_length=512)
    name = models.CharField(max_length=512, null=True)


class GroupAdditional(models.Model):
    group = models.OneToOneField(Group, related_name='options', on_delete=models.CASCADE)
    invite_code = models.CharField(max_length=512)

from django.db import models
from django.contrib.auth.models import User, Group


class Contest(models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)
    training = models.BooleanField(default=True)
    start_datetime = models.DateTimeField(null=True)
    finish_datetime = models.DateTimeField(null=True)
    allowed_groups = models.ManyToManyField(Group, related_name='allowed_contests', blank=True)

    def scoreboard(self):
        entries = TaskSolved.objects.filter(task__contest=self)
        users = {entry.user for entry in entries}
        result = []
        for user in users:
            solved_by_user = entries.filter(user=user)
            score = sum([entry.task.score for entry in solved_by_user])
            last_accepted = max([int(entry.time.timestamp()) for entry in solved_by_user])
            result.append({'username': user.username, 'score': score, "last_accepted": last_accepted})
        result = sorted(result, key=lambda x: (x['score'], x['last_accepted']))
        return result


class Category(models.Model):
    name = models.CharField(max_length=512)


class Task(models.Model):
    class Meta:
        ordering = ('score', 'id')

    name = models.CharField(max_length=512)
    score = models.IntegerField()
    description = models.TextField()  # TODO: markdown support
    contest = models.ForeignKey(Contest, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL)
    flag = models.CharField(max_length=512, null=True)
    category = models.ForeignKey(Category, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL)
    hidden = models.BooleanField(default=False)

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


class Hint(models.Model):
    class Meta:
        ordering = ('id',)
    task = models.ForeignKey(Task, related_name='hints', on_delete=models.CASCADE)
    text = models.TextField()


class Message(models.Model):
    class Meta:
        ordering = ('-time',)
    contest = models.ForeignKey(Contest, related_name='messages', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class GroupAdditional(models.Model):
    group = models.OneToOneField(Group, related_name='options', on_delete=models.CASCADE)
    invite_code = models.CharField(max_length=512)


class News(models.Model):
    class Meta:
        ordering = ('-time',)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

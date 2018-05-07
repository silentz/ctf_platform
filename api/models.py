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
    solved = models.ManyToManyField(User, related_name='solved_tasks', blank=True)
    # for flag generator support
    use_generator = models.BooleanField(default=False)
    token = models.CharField(max_length=512)

    def check_flag_using_generator(self, flag):
        try:
            generated_flag = Flag.objects.get(flag=flag, used=False)
        except Flag.DoesNotExist:
            return False
        generated_flag.used = True
        generated_flag.save()
        return True

    def check_flag(self, flag):
        if self.use_generator:
            return self.check_flag_using_generator(flag)
        else:
            return flag == self.flag


class Flag(models.Model):
    task = models.ForeignKey(Task, related_name='generator_flags', on_delete=models.CASCADE)
    flag = models.CharField(max_length=512)
    used = models.BooleanField()


class TaskFile(models.Model):
    task = models.ForeignKey(Task, related_name='files', null=True, blank=True, on_delete=models.SET_NULL)
    file = models.FileField(max_length=512)
    name = models.CharField(max_length=512, null=True)

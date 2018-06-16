# Generated by Django 2.0.4 on 2018-05-04 19:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskfile',
            name='name',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='solved',
            field=models.ManyToManyField(blank=True, related_name='solved_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='taskfile',
            name='file',
            field=models.FileField(max_length=512, upload_to=''),
        ),
    ]

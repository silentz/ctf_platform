# Generated by Django 2.0.5 on 2018-06-30 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_task_hidden'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': ('id',)},
        ),
    ]
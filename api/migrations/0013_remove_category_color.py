# Generated by Django 2.0.5 on 2018-06-12 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20180610_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='color',
        ),
    ]

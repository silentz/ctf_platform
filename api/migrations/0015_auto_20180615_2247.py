# Generated by Django 2.0.5 on 2018-06-15 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20180613_2112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('score', 'id')},
        ),
    ]

# Generated by Django 2.0.5 on 2018-06-06 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_hint_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='training',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 4.0.5 on 2022-10-11 07:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0009_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='last_submit',
        ),
        migrations.AddField(
            model_name='account',
            name='last_submit_follow',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 11, 19, 14, 22, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='account',
            name='last_submit_like',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 11, 19, 14, 22, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='account',
            name='last_submit_rapid',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 11, 19, 14, 22, tzinfo=utc)),
        ),
    ]

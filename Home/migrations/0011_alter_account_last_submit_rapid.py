# Generated by Django 4.0.5 on 2022-10-11 08:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0010_remove_account_last_submit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_submit_rapid',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 11, 19, 13, 22, tzinfo=utc)),
        ),
    ]

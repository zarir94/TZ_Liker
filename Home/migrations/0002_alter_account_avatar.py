# Generated by Django 4.0.5 on 2022-07-07 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.URLField(default='/files/img/avatar.png'),
        ),
    ]

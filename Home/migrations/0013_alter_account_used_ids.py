# Generated by Django 4.1.4 on 2022-12-13 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0012_alter_account_cookie_alter_account_full_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='used_ids',
            field=models.TextField(blank=True, default=''),
        ),
    ]

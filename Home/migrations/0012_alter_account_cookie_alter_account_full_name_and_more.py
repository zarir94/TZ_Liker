# Generated by Django 4.1.4 on 2022-12-13 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0011_alter_account_last_submit_rapid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='cookie',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_id',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='token',
            field=models.TextField(blank=True, null=True),
        ),
    ]

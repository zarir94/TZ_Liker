# Generated by Django 4.0.5 on 2022-07-13 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0008_alter_account_last_submit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
            ],
        ),
    ]

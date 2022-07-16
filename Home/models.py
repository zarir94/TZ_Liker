from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
import pytz
# Create your models here.

class AccountManager(BaseUserManager):
	def create_user(self, email, username, password):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have an username')
		if not password:
			raise ValueError('Users must have a password')
		user=self.model(email=self.normalize_email(email),username=username)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user=self.create_user(email=email,username=username, password=password)
		user.is_admin=True
		user.is_staff=True
		user.is_superuser=True
		user.save(using=self._db)
		return user

class Account(AbstractBaseUser):
	full_name=models.CharField(max_length=200, null=True)
	username=models.CharField(max_length=200, unique=True)
	email=models.CharField(max_length=200, unique=True)
	password=models.CharField(max_length=200, null=True)
	cookie=models.TextField(null=True)
	profile_id=models.CharField(max_length=200, null=True, unique=True)
	has_cookie=models.BooleanField(default=False)
	is_verified=models.BooleanField(default=False)
	token=models.TextField(null=True)
	used_ids=models.TextField(default='')
	last_submit=models.DateTimeField(default=datetime(2022, 7, 11, 19, 14, 22, tzinfo=pytz.UTC))

	date_joined=models.DateTimeField(auto_now_add=True)
	last_login=models.DateTimeField(auto_now=True)
	is_admin=models.BooleanField(default=False)
	is_active=models.BooleanField(default=True)
	is_staff=models.BooleanField(default=False)
	is_superuser=models.BooleanField(default=False)

	USERNAME_FIELD='username'
	REQUIRED_FIELDS=['email', 'password']

	objects=AccountManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

class Site_Info(models.Model):
	id=models.IntegerField(primary_key=True)
	likes=models.IntegerField()
	follows=models.IntegerField()
	users=models.IntegerField()

	def __str__(self):
		return f'Likes: {self.likes}, Follows: {self.follows}, Users: {self.users}'

class Contact(models.Model):
	name=models.CharField(max_length=200)
	email=models.CharField(max_length=200)
	subject=models.CharField(max_length=200)
	message=models.TextField()

	def __str__(self):
		return f'{self.name} - {self.email}'


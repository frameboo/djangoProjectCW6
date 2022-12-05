import enum
from datetime import date

from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE

from users.managers import UserManager, UserRoles


class User(AbstractBaseUser):
	ROLES = [
		(UserRoles.USER.value, 'Пользователь'),
		(UserRoles.ADMIN.value, 'Администратор'),
	]

	role = models.CharField(max_length=9, choices=ROLES, default=UserRoles.USER.value)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=12)
	first_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50, blank=True)
	image = models.ImageField(upload_to='user_images/', blank=True, null=True)
	is_active = models.BooleanField(default=True, blank=True, null=True)

	@property
	def is_superuser(self):
		return self.is_admin

	@property
	def is_staff(self):
		return self.is_admin

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return self.is_admin

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]
	objects = UserManager()

	@property
	def is_admin(self):
		return self.role == UserRoles.ADMIN.value

	@property
	def is_user(self):
		return self.role == UserRoles.USER.value

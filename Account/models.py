from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import (
	BaseUserManager , AbstractBaseUser
)


class MyUserManager(BaseUserManager):
	def create_user(self,name,phone_number,password = None):
		if not phone_number:
			raise ValueError('User must have PHONE NUMBER ')

		user = self.model(
			name=name,
			phone_number=phone_number,

		)
		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_superuser(self,name,phone_number,password=None):
		user = self.create_user(name,phone_number,password= password)
		user.is_admin = True
		user.is_staff = True
		user.is_active = True


		user.save(using = self._db)
		return user



class MyUser(AbstractBaseUser):
	name = models.CharField(max_length=300)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	phone_number = models.CharField(max_length=11,unique=True)
	national_number = models.CharField(max_length=11,unique=True,null=True,blank=True)
	city = models.CharField(max_length=32)
	province = models.CharField(max_length=32)
	area = models.CharField(max_length=64)
	forget_password_code = models.TextField()
	activation_code = models.TextField()
	api_token = models.TextField()
	is_code_active = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)




	objects = MyUserManager()

	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = ['name']

	def has_perm(self,perm,obj =None):
		"Does the user have a specific permission?"
		return True


	def has_module_perms(self,app_label):
		"Does the user have permissions to viwe the app 'app_label' ?"
		return True


	def __str__(self):
		return self.phone_number




class Profile (models.Model):
	id = models.AutoField(primary_key=True)
	avatar = models.ImageField(upload_to='avatar/')
	user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE)


	def __str__(self):
		return self.user_id.name



@receiver(post_save,sender = MyUser)
def create_profile (sender ,instance, created,**kwargs):
	if created:
		Profile.objects.create(user_id= instance)
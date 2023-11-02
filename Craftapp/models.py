from django.db import models
from Craftapp.manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.


class AbstractTimestampedModel(models.Model):
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
      abstract = True
      


class User(AbstractBaseUser,PermissionsMixin,AbstractTimestampedModel):
    username=models.CharField(default="test",max_length=255)
    first_name  = models.CharField(max_length=30,default="")
    last_name  = models.CharField(max_length=30,default="")
    email 		= models.EmailField(_('email'),unique=True)
    password    = models.CharField(max_length=255,default="")
    is_staff 	= models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active 	= models.BooleanField(default=True,
		help_text='Designates whether this user should be treated as active.\
		Unselect this instead of deleting accounts.')
    brewery=models.CharField(max_length=30,blank=True,null=True,unique=True)
    status=models.BooleanField(default=False)

    USERNAME_FIELD 	='email'
    
    objects 		= CustomUserManager()
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email
    

class WeekParticipants(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    weeknumber=models.CharField(blank=True,null=True,max_length=20)
    participant=models.IntegerField(blank=True,null=True)
    weekname=models.CharField(blank=True,null=True,max_length=20)

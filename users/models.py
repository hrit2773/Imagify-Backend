from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from .managers import CustomUserManager

class User(AbstractUser,PermissionsMixin):
    username=None
    email=models.EmailField('email address',unique=True, blank=True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=CustomUserManager()
    
    def __str__(self):
        return self.email
    
    
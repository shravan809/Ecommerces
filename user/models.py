from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,null=True,blank=True) 
    phone = models.CharField(max_length=12, null=True,blank=True)
    Address=models.TextField(max_length=100,null=True,blank=True)
    pan_number=models.CharField(max_length=12,null=True,blank=True,unique=True)
    Adhar_number=models.IntegerField(null=True,blank=True,unique=True)
    photo=models.ImageField(upload_to='images',null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects =UserManager()

    def name(self):
        return self.first_name +' '+ self.last_name

    def __str__(self):

        return self.email


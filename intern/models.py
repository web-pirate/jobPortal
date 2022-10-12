import email
from email import message
from email.policy import default
from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=500)
    message = models.TextField()

    def __str__(self):
        return self.name


class Company_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    cname = models.CharField(max_length=100)
    cemail = models.EmailField(max_length=100)
    clocation = models.CharField(max_length=1000)
    cphone = models.IntegerField(null=True, blank=False)
    cimage = models.ImageField(
        null=True, blank=False, upload_to='cprofile_img')
    cdescription = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)



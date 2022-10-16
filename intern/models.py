from email.policy import default
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
        blank=False, upload_to='cprofile_img')
    cdescription = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cname


class Newsletters(models.Model):
    nemail = models.EmailField(max_length=100)


class Job(models.Model):
    cname = models.ForeignKey(Company_profile, on_delete=models.CASCADE)
    job_position = models.CharField(max_length=100, blank=False)
    salary = models.IntegerField()
    job_description = models.CharField(max_length=1000, blank=False)
    job_experience = models.CharField(max_length=100, default="Fresher")
    job_type = models.CharField(max_length=100, default="Full-Time")
    
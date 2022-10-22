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
    message = models.CharField(max_length=5000, blank=True)

    def __str__(self):
        return self.name


class Company_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    cname = models.CharField(max_length=100)
    cemail = models.EmailField(max_length=100)
    clocation = models.CharField(max_length=1000)
    cphone = models.CharField(null=True, blank=False, max_length=12)
    cimage = models.ImageField(
        blank=True, upload_to='cprofile_img')
    cdescription = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cname


class Newsletter(models.Model):
    nemail = models.EmailField(max_length=100)


class Job(models.Model):
    jcname = models.ForeignKey(Company_profile, on_delete=models.CASCADE)
    jposition = models.CharField(max_length=100)
    jtype = models.CharField(max_length=50)
    jcreated = models.DateTimeField(auto_now_add=True)
    jlocation = models.CharField(max_length=500, default="Work From Home")
    jsalary = models.IntegerField(default="7000")
    jdesc = models.CharField(max_length=1000)

    def __str__(self):
        return self.jposition

from email.policy import default
from sre_constants import CATEGORY
from unicodedata import category
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


class UserDetails(models.Model):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    username = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    about = models.CharField(max_length=1000)
    gender = models.CharField(max_length=6, choices=GENDER)
    phone = models.IntegerField(default="0000000000")
    category = models.CharField(max_length=50, default="Web Developer")
    language = models.CharField(max_length=60, default="English")
    address = models.CharField(max_length=500, default="my home")
    dob = models.CharField(max_length=50, default="00/00/0000")

    edu_type_1 = models.CharField(max_length=50)
    edu_marks_1 = models.FloatField(max_length=4)
    edu_percentage_1 = models.CharField(max_length=12)
    edu_branch_1 = models.CharField(max_length=100)
    edu_year_1 = models.CharField(max_length=50)
    edu_inst_1 = models.CharField(max_length=100)
    edu_location_1 = models.CharField(max_length=100)
    edu_about_1 = models.CharField(max_length=1000, default="my home")

    edu_type_2 = models.CharField(max_length=25)
    edu_marks_2 = models.FloatField(max_length=4)
    edu_percentage_2 = models.CharField(max_length=12)
    edu_branch_2 = models.CharField(max_length=100)
    edu_year_2 = models.CharField(max_length=50)
    edu_inst_2 = models.CharField(max_length=100)
    edu_location_2 = models.CharField(max_length=100)
    edu_about_2 = models.CharField(max_length=1000, default="my home")

    user_img = models.FileField(upload_to="userProfile")
    resume = models.FileField(upload_to="userResume")


def __str__(self):
    return self.username


class UserExperience(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=10)

    exp_position_1 = models.CharField(max_length=50)
    exp_from_1 = models.CharField(max_length=50)
    exp_to_1 = models.CharField(max_length=50)
    exp_comp_1 = models.CharField(max_length=50)
    exp_location_1 = models.CharField(max_length=50)
    exp_about_1 = models.CharField(max_length=50)

    exp_position_2 = models.CharField(max_length=50)
    exp_from_2 = models.CharField(max_length=50, default="00/00/0000")
    exp_to_2 = models.CharField(max_length=50)
    exp_comp_2 = models.CharField(max_length=50)
    exp_location_2 = models.CharField(max_length=50)
    exp_about_2 = models.CharField(max_length=50)


class UserApply(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aname = models.CharField(max_length=50)

    acategory = models.CharField(max_length=50)
    aemail = models.CharField(max_length=50)
    aphone = models.CharField(max_length=50)

    ajob_name = models.CharField(max_length=50)
    acomp_name = models.CharField(max_length=50)

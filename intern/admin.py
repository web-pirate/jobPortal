from django.contrib import admin
from .models import *


class DataAdmin(admin.ModelAdmin):
    list_display = ('cname', 'cemail', 'cphone', 'clocation')
    list_filter = ('clocation', 'created_at')


class JobFilter(admin.ModelAdmin):
    list_display = ('jposition', 'jlocation', 'jcname', 'jcreated')


class JobFilter(admin.ModelAdmin):
    list_display = ('jposition', 'jlocation', 'jcname', 'jcreated')


class User_Filter(admin.ModelAdmin):
    list_display = ('username', 'gender', 'edu_type_1')
    list_filter = ('gender', 'edu_type_1')


admin.site.register(Profile)
admin.site.register(Newsletter)
admin.site.register(Company_profile, DataAdmin)
admin.site.register(Contact)
admin.site.register(Job, JobFilter)
admin.site.register(UserDetails, User_Filter)

from django.contrib import admin
from .models import *


class DataAdmin(admin.ModelAdmin):
    list_display = ('cname', 'cemail', 'cphone', 'clocation')
    list_filter = ('clocation', 'created_at')


class JobFilter(admin.ModelAdmin):
    list_display = ('cname', 'job_position', 'salary', 'job_type')


admin.site.register(Profile)
admin.site.register(Newsletters)
admin.site.register(Company_profile, DataAdmin)
admin.site.register(Job, JobFilter)

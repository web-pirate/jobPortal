from django.contrib import admin
from .models import Profile, Company_profile


class DataAdmin(admin.ModelAdmin):
    list_display = ('cname', 'cemail', 'cphone', 'clocation')
    list_filter = ('clocation', 'created_at')


admin.site.register(Profile)
admin.site.register(Company_profile, DataAdmin)

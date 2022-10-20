from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    # Accounts Management
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # Extra's
    path('contact/', views.contact, name='contact'),

    # Pages associated with email
    path('token/', views.token_send, name='token'),
    path('success/', views.success, name='success'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('error/', views.error, name='error'),
    path('email/', views.email_template, name='email_template'),

    # Company Associated Pages
    path('company_profile/', views.company_profile, name='company_profile'),
    path('company_registration/', views.company_registration,
         name='company_registration'),
    path('edit_company/<company_obj>', views.edit_company, name='edit_company'),

    # User Associated Pages
    path('user_list/', views.user_list, name='user_list'),
    path('user_view/<pk>', views.user_view, name='user_view'),

    # Job Associated Pages
    path('remove_job/<job_id>', views.remove_job, name='remove_job'),



    # Newsletter email collection
    # path('newsletter/', views.newsletter, name='newsletter'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

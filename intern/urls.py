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
    path('about/', views.about, name='about'),
    path('blog_content/', views.blog_content, name='blog_content'),
    path('email_verify/', views.email_verify, name='email_verify'),



    # Pages associated with email
    path('token/', views.token_send, name='token'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('error/', views.error, name='error'),
    path('email/', views.email_template, name='email_template'),

    # Company Associated Pages
    path('company_profile/', views.company_profile, name='company_profile'),
    path('company_registration/', views.company_registration,
         name='company_registration'),
    path('edit_company/<company_obj>', views.edit_company, name='edit_company'),
    path('company_view/<cname>', views.company_view, name='company_view'),

    # User Associated Pages
    path('user_list/', views.user_list, name='user_list'),
    path('user_view/<pk>', views.user_view, name='user_view'),
    path('user_details/', views.user_details, name='user_details'),
    path('user_update/', views.user_update, name='user_update'),
    path('profile/', views.profile, name='profile'),
    path('experience/', views.experience, name='experience'),
    path('exp_update/<user_obj>', views.exp_update, name='exp_update'),
    path('apply_now/', views.user_apply_now, name='apply_now'),


    # Job Associated Pages
    path('remove_job/<job_id>', views.remove_job, name='remove_job'),
    # path('job_view/', views.job_view, name='job_view'),
    path('jobs/', views.jobs, name='jobs'),
    path('job_create/', views.job_create, name='job_create'),
    path('job_apply/', views.job_apply, name='job_apply'),



    # Newsletter email collection
    # path('newsletter/', views.newsletter, name='newsletter'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

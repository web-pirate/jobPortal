from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Accounts Management
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # Extra's
    path('contact/', views.contact, name='contact'),
]

"""
URL configuration for BitBucket_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView 
from django.contrib.auth import views as auth_views
from celeryApp import view
app_name = 'BitBucket_site'

# urls.py

   # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
   # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
   # path('', views.index, name='index'),
   # path('request-access/', views.request_access, name='request_access'),
   # path('access-requests/', views.access_request_list, name='access_request_list'),
    #path('request-access/<slug:repo_slug>/', views.request_access_form, name='request_access_form'),
   # path('request-access/<slug:repo_slug>/', views.request_access_form, name='request_access_form'),
   # path('custom-login/', views.custom_login, name='custom_login'),
  #  path('grant-access/<slug:repo_slug>/', views.grant_access, name='grant_access'),
   # path('login/', views.custom_login, name='custom_login'),
    #path('logout/', views.custom_logout, name='custom_logout'),
   # path('register/', views.register, name='register'),
   # path('user_login/', views.login, name='user_login'),
    #path('logout/', views.logout, name='logout'),
urlpatterns = [
    path('accounts/login/', views.custom_login, name='login'),
    path('admin/', admin.site.urls),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('request-access/', views.request_access, name='request_access'),
    path('access-requests/', views.access_request_list, name='access_request_list'),
    path('request-access/<slug:repo_slug>/', views.request_access_form, name='request_access_form'),
    path('grant-access/<slug:repo_slug>/', views.grant_access, name='grant_access'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('approve_or_deny/<int:access_request_id>/<str:decision>/', views.approve_or_deny, name='approve_or_deny'),
    path('register/', views.custom_login, name='register'),]
    #path('test/', view.test, name='test'),  ]

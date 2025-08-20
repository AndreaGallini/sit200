from django.contrib.auth import views as auth_views

from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('user/logs/', views.access_logs_view, name='logs'),
    path('logout/', views.logout_view, name='logout'),


]

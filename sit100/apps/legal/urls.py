from django.contrib.auth import views as auth_views

from django.urls import path

from . import views


urlpatterns = [
    path('cookies/', views.cookies, name='cookies'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms-and-condition/', views.terms, name='terms_conditions'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
]

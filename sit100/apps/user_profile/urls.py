from django.contrib.auth import views as auth_views

from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.user_profile, name='home'),
    path('user_dashboard/', views.user_homepage, name='user_homepage'),
    path('sicurezza/', views.change_password, name='sicurezza'),
    path('assistenza/', views.send_email, name='assistence'),
    path('save_designer_data/', views.save_designer_data,
         name='save_designer_data'),
    path('get_designers_data/', views.get_designers_data,
         name='get_designers_data'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('questionario/', views.questionario, name='questionario'),
]

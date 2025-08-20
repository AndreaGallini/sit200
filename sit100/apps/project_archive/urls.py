
from django.urls import path

from . import views

urlpatterns = [

    path('archivio_progetti/', views.project_archive, name='project_archive'),

]



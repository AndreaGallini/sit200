
from django.urls import path

from . import views

from .processing_views import *

urlpatterns = [
    path('save_session_to_db/', views.save_session_to_db,
         name='save_session_to_db'),
    path('project_pipeline/', views.project_pipeline, name='project_pipeline'),
    path('pvgis/', views.pvgis, name='pvgis'),
    path('preparing_data/', preparing_data, name='preparing_data'),
    path('solar_calculator/', solar_calculator, name='solar_calculator'),
    path('sizing/', sizing, name='sizing'),
    path('pv_generator/', pv_generator, name='pv_generator'),
    path('technical_checks/', technical_checks, name='technical_checks'),
    path('graph_generator/', graph_generator, name='graph_generator'),
    path('project_compilation/', project_compilation, name='project_compilation'),
    path('validation/', validation, name='validation'),
    path('file_save/', file_save, name='file_save'),
    # path('generate_word_and_pdf/', generate_word_and_pdf, name='generate_word_and_pdf'),
    path('cashflow/', cashflow, name='cashflow'),


]

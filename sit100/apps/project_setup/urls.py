from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_map, name='project_map'),
    path('clear_session/', views.clear_session, name='clear_session'),
    path('area/', views.area_init, name='area_init'),
    path('dove/', views.where, name='where'),
    path('tipo/', views.typology, name='type'),
    path('subfields_conf/', views.subfields_conf, name='subfields_conf'),
    path('solare_ed_ombreggiamento/', views.solar_and_dark, name='solar_and_dark'),
    path('configurazione_impianto/',
         views.config_structure, name='config_structure'),
    path('project_data/', views.project_data, name='project_data'),
    path('anagrafy_data/', views.anagrafy_data, name='anagrafy_data'),
    path('anagrafy_data_2/', views.anagrafy_data_2, name='anagrafy_data_2'),
    path('add_designer/', views.add_designer, name='add_designer'),
    path('clear_coordinates/', views.clear_coordinates, name='clear_coordinates'),
    path('user_choise/', views.user_choise, name='user_choise'),
    path('display_session_data/', views.display_session_data,
         name='display_session_data'),
    path('report_page/', views.report_page, name='report_page'),
]

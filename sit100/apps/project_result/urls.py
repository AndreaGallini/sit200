from django.urls import path

from . import views

urlpatterns = [
    path('dashboard_result/', views.dashboard_result, name='dashboard_result'),
    path('dashboard/result/<int:project_code>/', views.dashboard_result, name='dashboard_result'),
    path('download/<str:secure_hash>/', views.secure_download, name='secure_download'),
    path('generate_secure_link/<int:project_code>/<str:file_type>/', views.generate_secure_link, name='generate_secure_link'),
    path('download_word_file/<int:project_code>', views.download_word_file, name='secure_word_download'),
    path('download_design_word_file/<int:project_code>', views.download_design_word_file, name='secure_design_download'),

]

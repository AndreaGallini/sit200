from django.urls import path
from .save_views import *
from .designer_views import *

urlpatterns = [
    path('update_session/', update_session, name='update_session'),
    path('update_polygon/', update_polygon, name='update_polygon'),
    path('save_generator_structure/', save_generator_structure,
         name='save_generator_structure'),
    path('save_where/', save_where, name='save_where'),
    path('save_type/', save_type, name='save_type'),

    path('save_solar_data/', save_solar_data, name='save_solar_data'),
    path('save_configuration/', save_configuration, name='save_configuration'),
    path('save_general_data/', save_general_data, name='save_general_data'),
    path('save_anagrafy_data_1/', save_anagrafy_data_1,
         name='save_anagrafy_data_1'),
    path('save_designers_and_collaborators/', save_designers_and_collaborators,
         name='save_designers_and_collaborators'),
    path('upload_image/', upload_image, name='upload_image'),
    path('get_designers_data/', get_designers_data, name='get_designers_data'),
    path('save_subfields_configuration/', save_subfields_configuration,
         name='save_subfields_configuration'),
]

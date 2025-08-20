# context_processors.py
from django.conf import settings
import time
import json


def session_data(request):
    """Context processor per i dati di sessione comuni a tutte le view"""
    project = request.session.get('project', {})
    num_polygons = len(project.get('polygons', []))

    return {
        'session_data': request.session.items(),
        'num_polygons': num_polygons,
        'time': time
    }


def app_settings(request):
    """Context processor per le impostazioni dell'applicazione"""
    return {
        'APP_NAME': getattr(settings, 'APP_NAME', ''),
        'APP_DARK_LOGO': getattr(settings, 'APP_DARK_LOGO', ''),
        'APP_LIGHT_LOGO': getattr(settings, 'APP_LIGHT_LOGO', ''),
        'time': time
    }


def project_common_data(request):
    """Context processor per i dati comuni del progetto utilizzati in tutte le view"""
    project = request.session.get('project', {})

    # Dati base del progetto
    base_data = {
        'project': project,
        'project_code': project.get('project_code', ''),
        'latitude': request.session.get('latitude', ''),
        'longitude': request.session.get('longitude', ''),
        'required_fields': getattr(settings, 'REQUIRED', [])
    }

    # Dati del generatore e subfields
    generator = project.get('generator', {})
    subfields = []
    for field_name, field_data in generator.items():
        for subfield_name in field_data.keys():
            subfields.append(subfield_name)

    base_data.update({
        'generator': generator,
        'subfields': json.dumps(subfields),
        'subfields_list': subfields
    })

    # Dati generali del progetto
    general_data = project.get('general_data', {})
    base_data.update({
        'general_data': general_data,
        'project_title': general_data.get('project_title', ''),
        'municipality': general_data.get('municipality', ''),
        'province': general_data.get('province', ''),
        'region': general_data.get('region', ''),
        'plant_scope': general_data.get('plant_scope', ''),
        'auto_consumption': general_data.get('auto_consumption', ''),
        'private_house': general_data.get('private_house', ''),
        'cadastral_references': general_data.get('cadastral_references', ''),
        'project_acronym': general_data.get('project_acronym', ''),
        'identification_code': general_data.get('identification_code', ''),
        'address': general_data.get('address', ''),
        'revision_date': general_data.get('revision_date', ''),
        'revision_number': general_data.get('revision_number', ''),
        'edit_by': general_data.get('edit_by', ''),
        'verified_by': general_data.get('verified_by', ''),
        'approved_by': general_data.get('approved_by', ''),
        'site_information': general_data.get('site_information', ''),
        'intervention_scope': general_data.get('intervention_scope', ''),
        'cover_image': general_data.get('cover_image', ''),
        'cover_logo_1': general_data.get('cover_logo_1', ''),
        'cover_logo_2': general_data.get('cover_logo_2', ''),
        'cover_logo_3': general_data.get('cover_logo_3', ''),
        'copertina': general_data.get('copertina', '')
    })

    # Dati di configurazione del progetto
    base_data.update({
        'mounting': project.get('mounting', ''),
        'grid_connected': project.get('grid_connected', ''),
        'storage': project.get('storage', ''),
        'self_consumption': project.get('self_consumption', ''),
        'rid': project.get('rid', ''),
        'albedo': project.get('albedo', ''),
        'ombreggiamento_ostacoli': project.get('ombreggiamento_ostacoli', ''),
        'ombreggiamento_clinometrico': project.get('ombreggiamento_clinometrico', ''),
        'shading_obstacles': project.get('shading_obstacles', ''),
        'shading_horizon': project.get('shading_horizon', 0),
    })

    # Dati dei progettisti e collaboratori
    base_data.update({
        'designers_data': project.get('designers_data', []),
        'collaborators_data': project.get('collaborators_data', []),
    })

    return base_data


def project_specialized_data(request):
    """Context processor per dati specializzati utilizzati in alcune view specifiche"""
    project = request.session.get('project', {})

    # Dati per solar_and_dark view
    angles = range(0, 100, 5)

    # Estrai le coordinate dai subfields per compatibilità con il vecchio formato polygons
    polygons = []
    generator = project.get('generator', {})
    for field_name, field_data in generator.items():
        for subfield_name, subfield_data in field_data.items():
            if 'coordinates' in subfield_data:
                polygons.append({
                    'name': subfield_data.get('name', subfield_name),
                    'coordinates': subfield_data['coordinates'],
                    'area': subfield_data.get('area', 0)
                })

    return {
        'angles': angles,
        'polygons': polygons,  # Aggiungi i polygons estratti dai subfields
        'polygons_json': json.dumps(polygons),
        'project_json': json.dumps(project)
    }

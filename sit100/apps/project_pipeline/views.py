from django.shortcuts import render, get_object_or_404
from apps.project.models import Project
import ast
from .processing_views import *
import logging
from django.conf import settings

APP_NAME = settings.APP_NAME
logger = logging.getLogger('django')


def project_pipeline(request):
    project_session_data = request.session.get('project')
    project_code = int(project_session_data['project_code'])
    if not project_session_data:
        logger.warning(
            f'project_pipeline, codice progetto mancante, {project_code}')
        return render(request, 'project/error.html', {'message': 'Nessun progetto trovato nella sessione.'})
    project_code = project_session_data.get('project_code')
    save_session_to_db(request, project_session_data)
    project = get_object_or_404(Project, project_code=project_code)
    try:
        input_data = ast.literal_eval(project.input_data)
    except (ValueError, SyntaxError):
        logger.warning(
            f'project_pipeline, errore nel parsign dei dati, {project_code}')
        return render(request, 'project_pipeline/error.html', {'message': 'Errore nel parsing dei dati del progetto.'})

    latitude = input_data.get('latitude')
    longitude = input_data.get('longitude')
    project_code = input_data.get('project_code')

    if not latitude or not longitude:
        logger.warning(
            f'project_pipeline, latitude e longitude mancanti nei dati di progetto, {project_code}')
        return render(request, 'project_pipeline/error.html', {'message': 'Latitudine o longitudine mancanti nei dati del progetto.'})
    context = {
        'project': project,
        'latitude': latitude,
        'longitude': longitude,
        'APP_NAME': APP_NAME,
        'project_code': project_code
    }
    logger.info(f'project_pipeline funzionante, {project_code}')
    return render(request, 'project_pipeline/project_pipeline.html', context)


def save_session_to_db(request, project_session_data):
    project_code = int(project_session_data['project_code'])
    Project.objects.update_or_create(
        project_code=project_code,
        defaults={
            'user_id': request.user,  # Passa l'istanza dell'utente
            # Salva i dati della sessione
            'input_data': str(project_session_data)
        }
    )

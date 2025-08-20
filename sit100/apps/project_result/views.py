import json

from django.shortcuts import render, get_object_or_404
from apps.project.models import Project
import time
from django.utils.safestring import mark_safe
from .download_views import *
import logging
from django.conf import settings

APP_NAME = settings.APP_NAME
logger = logging.getLogger('django')


def dashboard_result(request, project_code=None):
    if project_code is None:
        # Prova a recuperare il project_code dalla sessione
        project_session_data = request.session.get('project')
        if project_session_data:
            project_code = project_session_data.get('project_code')
        else:
            # Gestisci il caso in cui il project_code non sia disponibile
            logger.warning(
                f'dashboard_project, codice progetto mancante, {project_code}')
            return render(request, 'project_result/error.html', {'message': 'Codice progetto mancante.'})

    project = get_object_or_404(Project, project_code=project_code)
    if project.user_id_id != request.user.id:
        return render(request, 'project_result/error.html', {'message': 'Non sei autorizzato ad accedere al progetto.'})
    ao1_data = json.dumps(project.keopebank)
    try:
        pvgis_data = json.loads(project.pvgis_data)
    except (TypeError, json.JSONDecodeError):
        pvgis_data = {}
    outputs_data = pvgis_data.get('outputs', {})
    outputs_data_json = json.dumps(outputs_data)

    # Passa i dati al template
    context = {
        'time': time,
        'project': project,
        'project_code': project_code,
        'outputs_data_json': mark_safe(outputs_data_json),
        'APP_NAME': APP_NAME,
        'ao1_data': ao1_data
    }
    return render(request, 'project_result/dashboard_result.html', context)

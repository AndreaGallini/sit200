
from django.http import JsonResponse
import json
from django.shortcuts import render, get_object_or_404, redirect
from apps.project.models import Project
import time
from django.utils.safestring import mark_safe
import ast
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
import json
import logging
from django.conf import settings

APP_NAME = settings.APP_NAME
logger = logging.getLogger('django')
# Create your views here.


def project_archive(request):
    # Recupera i progetti dell'utente con status=1 e li ordina per data di creazione (più recente per primo)
    projects = Project.objects.filter(status=1, user_id=request.user.id).order_by('-created_at')
    projects_data = []

    for project in projects:
        try:
            input_data = ast.literal_eval(project.input_data)
        except (ValueError, SyntaxError):
            input_data = {}

        project_title = input_data.get('general_data', {}).get(
            'project_title', 'Titolo non disponibile')
        project_date = project.created_at
        projects_data.append({
            'project_code': project.project_code,
            'project_title': project_title,
            'project_date': project_date
        })
    context = {
        'time': time,
        'APP_NAME': APP_NAME,
        'projects': projects_data
    }
    return render(request, 'project_archive/project_archive.html', context)


def delete_project(request, project_code):
    if request.method == 'POST':
        try:
            # Usa update() invece di save() per evitare di caricare l'intero oggetto
            Project.objects.filter(project_code=project_code).update(status=9)
            return JsonResponse({
                'status': 'success',
                'message': 'Progetto eliminato con successo.'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

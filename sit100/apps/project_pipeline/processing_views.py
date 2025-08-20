import os
import tempfile
from django.conf import settings
from django.http import JsonResponse
import time
from ast import literal_eval
from ai.keope.pipeline_context import PipelineContext
from apps.project.models import Project
import logging

logger = logging.getLogger('django')


def pipeline_init(request):
    project_code = request.POST.get("project_code")
    project = Project.objects.get(project_code=project_code)
    pipeline_context = PipelineContext(project_code)
    pipeline_context.initialize()
    return pipeline_context, project


def path_project_composer(project_code):
    project_folder = os.path.join(settings.PROJECT_ROOT, str(project_code))
    relative_project_path = f'media/project_files/{str(project_code)}'
    return relative_project_path, project_folder


def preparing_data(request):
    project_code = request.POST.get("project_code")
    project = Project.objects.get(project_code=project_code)
    project.keopebank = {}
    project.save()
    pipeline_context, project = pipeline_init(request)
    user_data = literal_eval(project.input_data)
    result = pipeline_context.user_input_preparation(user_data)
    if result:
        return JsonResponse({'success': True, 'message': 'Operazione completata', 'status': 200}, status=200)
    else:
        return JsonResponse({'success': False, 'message': 'Operazione Errore', 'status': 500}, status=500)


def sizing(request):
    pipeline_context, project = pipeline_init(request)
    result = pipeline_context.pv_sizing()
    if result:
        return JsonResponse({'success': True, 'message': 'Operazione completata', 'status': 200}, status=200)
    else:
        return JsonResponse({'success': False, 'message': 'Operazione Errore', 'status': 500}, status=500)


def solar_calculator(request):
    pipeline_context, project = pipeline_init(request)
    result = pipeline_context.solar_calculator()
    if result:
        return JsonResponse({'success': True, 'message': 'Operazione completata', 'status': 200}, status=200)
    else:
        return JsonResponse({'success': False, 'message': 'Operazione Errore', 'status': 500}, status=500)


def pvgis(request):
    pipeline_context, project = pipeline_init(request)
    max_attempts = 3
    attempt = 0
    while attempt < max_attempts:
        result = pipeline_context.api_pvgis()
        if result:
            return JsonResponse({'success': True, 'message': 'Operazione completata', 'status': 200}, status=200)
        attempt += 1

    return JsonResponse({'success': False, 'message': 'Operazione Errore', 'status': 405}, status=405)


def cashflow(request):
    pipeline_context, project = pipeline_init(request)
    result = pipeline_context.cashflow_calculator()
    if result:
        return JsonResponse({'success': True, 'message': 'Operazione completata', 'status': 200}, status=200)
    else:
        return JsonResponse({'success': False, 'message': 'Operazione Errore', 'status': 500}, status=500)


def pv_generator(request):
    time.sleep(1)
    return JsonResponse({
        'success': True,
        'message': 'Operazione completata',
        'status': 200
    }, status=200)


def technical_checks(request):
    time.sleep(1)
    return JsonResponse({
        'success': True,
        'message': 'Operazione completata',
        'status': 200
    }, status=200)


def graph_generator(request):
    """Genera i grafici del progetto utilizzando la pipeline."""
    pipeline_context, project = pipeline_init(request)

    if not pipeline_context:
        return JsonResponse({
            'success': False,
            'message': 'Errore nell\'inizializzazione della pipeline',
            'status': 500
        }, status=500)

    try:
        # Esegui la generazione dei grafici
        result = pipeline_context.graphs_generator()

        if result:
            return JsonResponse({
                'success': True,
                'message': 'Grafici generati con successo',
                'status': 200
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Errore nella generazione dei grafici',
                'status': 500
            }, status=500)

    except Exception as e:
        logger.error(f'Errore durante la generazione dei grafici: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Errore durante la generazione dei grafici: {str(e)}',
            'status': 500
        }, status=500)


def project_compilation(request):
    pipeline_context, project = pipeline_init(request)
    output_formatter = pipeline_context.xml_formatter()
    if output_formatter:
        result = pipeline_context.xml_compiler()
        if result:
            return JsonResponse({'success': True, 'message': 'Operazione completata', 'status': 200}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Operazione Errore', 'status': 500}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Operazione Errore', 'status': 500}, status=500)


def validation(request):
    pipeline_context, project = pipeline_init(request)
    result = pipeline_context.xml_validator()
    if result:
        return JsonResponse({'success': True, 'message': 'Operazione completata', 'status': 200}, status=200)
    else:
        return JsonResponse({'success': False, 'message': 'Operazione Errore', 'status': 500}, status=500)


def file_save(request):
    pipeline_context, project = pipeline_init(request)
    '''
    project_data = request.session.get('project')
    word_name = f"Report_{project_code}.docx"
    # Create temporary file path for the Word document
    temp_dir = tempfile.mkdtemp()
    temp_word_path = os.path.join(temp_dir, word_name)
    file_dest_path = project_data.get('project_dir', {}).get('path')
    word_dest_path = os.path.join(file_dest_path, word_name)
    '''
    result = pipeline_context.xml_converter_in_word_and_save()
    if result:
        return JsonResponse({'success': True, 'message': 'Operazione completata', 'status': 200}, status=200)
    else:
        return JsonResponse({'success': False, 'message': 'Operazione Errore', 'status': 500}, status=500)

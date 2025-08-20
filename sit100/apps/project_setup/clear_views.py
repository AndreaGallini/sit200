from django.shortcuts import render, get_object_or_404, redirect
import requests
from django.http import JsonResponse
import logging
from django.http import HttpResponse
logger = logging.getLogger('django')


def clear_session(request):
    # Clear session data
    if 'project' in request.session:
        del request.session['project']

    logger.info('Sessione svuotata')

    # Add JavaScript to clear localStorage items before redirect
    response = HttpResponse('''
        <script>
            // Clear all localStorage items that start with "visited_"
            Object.keys(localStorage).forEach(key => {
                if (key.startsWith('visited_')) {
                    localStorage.removeItem(key);
                }
            });
            // Redirect after clearing
            window.location.href = '/project/area';
        </script>
    ''')
    return response


def clear_coordinates(request):
    if request.method == 'POST':
        project = request.session.get('project', {})

        # Rimuovi le chiavi specifiche dal dizionario 'project'
        project.pop('latitude', None)
        project.pop('longitude', None)
        project.pop('altitude', None)

        # Aggiorna la sessione con il dizionario modificato
        request.session['project'] = project
        logger.info('Coordinate eliminate con successo')
        return JsonResponse({'message': 'Coordinates cleared from project'})
    logger.warning('clear_coordinates , error method')
    return JsonResponse({'error': 'Invalid request'}, status=400)


def clear_polygons(request):
    if request.method == 'POST':
        project = request.session.get('project', {})

        # Rimuovi le chiavi specifiche dal dizionario 'project'
        project.pop('polygons', None)

        # Aggiorna la sessione con il dizionario modificato
        request.session['project'] = project
        logger.info('Poligoni eliminate con successo')
        return JsonResponse({'message': 'Polygons cleared from project'})
    logger.warning('clear_coordinates , error method')
    return JsonResponse({'error': 'Invalid request'}, status=400)

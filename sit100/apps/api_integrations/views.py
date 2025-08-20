from django.http import JsonResponse
import requests
from apps.project.models import Counter,Project
from django.utils import timezone
import logging
from ast import literal_eval
logger = logging.getLogger('django')


def pvgis(request):
    pvgis_counter = Counter.objects.get(name='Pvgis_code')
    pvgis_code = pvgis_counter.value
    pvgis_time_at = pvgis_counter.time_at
    time = timezone.now()
    interval = time - pvgis_time_at
    minutes = interval.seconds // 60 % 60
    if(pvgis_code != 200):
        if(minutes > 20):
            pvgis_counter.value = 200
            pvgis_counter.save()

    if request.method == 'POST':
        try:
            # Extract parameters from the POST request
            project_code = request.POST.get('project_code')
            project = Project.objects.get(project_code=project_code)
            input_data = literal_eval(project.input_data)
            latitude = input_data['latitude']
            longitude = input_data['longitude']
            project_code = input_data['project_code']
            peakpower = 3
            pvtechchoice = "crystSi"
            fixed = 1
            plant_type = input_data['type']
            loss = 14
            polygons = input_data['polygons']
            first_polygon = input_data['polygons'][0]
            tilt = first_polygon['tilt']
            orientation = first_polygon['orientation']
            azimuth = first_polygon['azimuth']
            # Controlla prima il tipo di impianto
            if plant_type == 'off-grid':
                logger.info(f'get_pvgis_data skipped for off-grid, {project_code}')
                return JsonResponse({'success': False,
                    'message': 'Operazione completata',
                    'status': 405,}, status=405)

            # Se non è off-grid, procedi con la richiesta PVGIS
            url = f'https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?lat={latitude}&lon={longitude}&peakpower={peakpower}&loss={loss}&pvtechchoice={pvtechchoice}&fixed={fixed}&angle={tilt}&aspect={azimuth}&outputformat=json'
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()
            
            logger.info(f'get_pvgis_data success, {project_code}')
            
            try:
                project = Project.objects.get(project_code=project_code, user_id=request.user.id)
                project.pvgis_data = data
                project.save()
                logger.info(f'save_pvgis_data , successo, {project_code}')
                return JsonResponse({
                    'success': True,
                    'message': 'Operazione completata',
                    'status': 200,
                    'data': data
                }, status=200)
            except Project.DoesNotExist:
                logger.warning(f'get_pvgis_data, il progetto non esiste, {project_code}')
                return JsonResponse({
                    'success': False, 
                    'error': 'Progetto non trovato o accesso non autorizzato'
                }, status=405)

        except requests.exceptions.RequestException as e:
            logger.warning(f'get_pvgis_data error, {project_code}')
            pvgis_counter.value = 405
            pvgis_counter.save()
            return JsonResponse({'error': str(e)}, status=405)

    else:
        logger.warning('get_pvgis_data method invalid')
        pvgis_counter.value = 405
        pvgis_counter.save()
        return JsonResponse({'error': 'Invalid request method'}, status=405)
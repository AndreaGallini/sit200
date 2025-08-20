from django.shortcuts import render
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
import json
import os
from django.conf import settings
import logging
from bucket_operator import upload_project_image
import tempfile
from apps.project.models import Counter
from django.db import transaction, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
import posixpath
from storage.factory import StorageFactory
from functools import wraps
from .views import get_image_url


logger = logging.getLogger('django')
load_dotenv()


# =============================================================================
# FUNZIONI DI UTILITÀ
# =============================================================================

def get_project_data(request):
    """Recupera i dati del progetto dalla sessione in modo sicuro."""
    project = request.session.get('project', {})
    project_code = project.get('project_code', 'unknown')
    project_path = project.get('project_dir', {}).get('path', '')
    return project, project_code, project_path


def update_project_session(request, project_data):
    """Aggiorna i dati del progetto nella sessione."""
    request.session['project'] = project_data
    request.session.modified = True


def success_response(message="Operazione completata con successo", data=None):
    """Crea una risposta JSON di successo standardizzata."""
    response = {'status': 'success', 'message': message}
    if data:
        response['data'] = data
    return JsonResponse(response)


def error_response(message="Errore durante l'operazione", status=400):
    """Crea una risposta JSON di errore standardizzata."""
    return JsonResponse({'status': 'error', 'message': message}, status=status)


def handle_image_upload(image_file, project_path, custom_name=None):
    """Gestisce l'upload di un'immagine in modo standardizzato."""
    if not image_file:
        return None

    try:
        # Crea file temporaneo
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        for chunk in image_file.chunks():
            temp_file.write(chunk)
        temp_file.close()

        # Upload su S3
        if custom_name:
            # Usa il nome personalizzato se fornito
            image_name = custom_name
        else:
            # Usa il nome originale del file
            image_name = image_file.name.replace(' ', '_')
        
        key = upload_project_image(temp_file.name, image_name, project_path)
        # Cleanup
        os.unlink(temp_file.name)

        return key
    except Exception as e:
        logger.error(f"Errore upload immagine: {e}")
        raise


def require_project_session(func):
    """Decoratore che assicura la presenza dei dati del progetto nella sessione."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        project, project_code, project_path = get_project_data(request)
        if not project_code or project_code == 'unknown':
            logger.warning(
                f"{func.__name__}: project_code mancante nella sessione")
            return error_response("Dati del progetto non trovati nella sessione", 400)
        return func(request, *args, **kwargs)
    return wrapper


def log_operation(operation_name):
    """Decoratore per il logging automatico delle operazioni."""
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            _, project_code, _ = get_project_data(request)
            try:
                result = func(request, *args, **kwargs)
                logger.info(
                    f"{operation_name}: successo per progetto {project_code}")
                return result
            except Exception as e:
                logger.error(
                    f"{operation_name}: errore per progetto {project_code}: {str(e)}")
                return error_response(f"Errore in {operation_name}: {str(e)}", 500)
        return wrapper
    return decorator


# =============================================================================
# FUNZIONI DI GENERAZIONE E GESTIONE PROGETTO
# =============================================================================

def generate_unique_code():
    """Genera un codice univoco leggendo e aggiornando il contatore."""
    try:
        with transaction.atomic():
            counter = Counter.objects.select_for_update().get(name='project_code')
            project_code = counter.value
            counter.value += 1
            counter.save()
        logger.info(f'Project code generato: {project_code}')
        return project_code
    except ObjectDoesNotExist:
        logger.critical(
            "Il contatore 'project_code' non esiste. Crealo nel database.")
        raise RuntimeError(
            "Errore critico: contatore 'project_code' mancante.")
    except DatabaseError as e:
        logger.critical(
            f"Errore nel database durante la generazione del codice univoco: {e}")
        raise RuntimeError(
            "Errore del database durante la generazione del codice univoco.")
    except Exception as e:
        logger.critical(f"Errore imprevisto in generate_unique_code: {e}")
        raise RuntimeError(
            "Errore sconosciuto durante la generazione del codice univoco.")


def create_project_directory(project_code):
    """Crea la cartella di progetto nello storage."""
    dir_path = posixpath.join(settings.PROJECT_ROOT, str(project_code))
    dir_url = os.path.join(settings.PROJECT_URL, str(project_code))
    storage = StorageFactory.get_storage_service()
    try:
        storage.create_folder(dir_path)
        logger.info(f"Cartella '{dir_path}' creata con successo.")
        return dir_path, dir_url
    except RuntimeError as e:
        logger.error(f"Errore nella creazione della cartella di progetto: {e}")
        raise
    except Exception as e:
        logger.critical(
            f"Errore critico in create_project_directory: {e}", exc_info=True)
        raise


# =============================================================================
# VIEW FUNCTIONS SEMPLIFICATE
# =============================================================================

@csrf_exempt
@require_POST
def generate_code_and_create_dir(request):
    """Genera codice progetto e crea directory."""
    project = request.session.get('project', {})
    try:
        project_unique_code = generate_unique_code()
        project_path, project_url = create_project_directory(
            project_unique_code)

        project.update({
            'project_dir': {'path': project_path, 'url': project_url},
            'project_code': project_unique_code
        })
        update_project_session(request, project)

    except RuntimeError as e:
        logger.error(f"Errore nella generazione del codice progetto: {e}")
        return render(request, 'project_setup/error.html', {})


@csrf_exempt
@require_POST
@log_operation("update_session")
def update_session(request):
    """Aggiorna i dati di sessione con informazioni geografiche."""
    generate_code_and_create_dir(request)

    # Dati geografici
    geo_data = {
        'latitude': request.POST.get('latitude'),
        'longitude': request.POST.get('longitude'),
        'altitude': request.POST.get('altitude', 'N.D.') if request.POST.get('altitude') != 'undefined' else 'N.D.',
        'address': request.POST.get('address', ''),
        'address_component': request.POST.get('address_component', '')
    }

    if not (geo_data['latitude'] and geo_data['longitude']):
        logger.warning('update_session: Dati geografici mancanti')
        return error_response('Dati geografici mancanti', 400)

    project = request.session.get('project', {})
    project.update(geo_data)

    # Gestione componenti indirizzo
    if geo_data['address_component']:
        try:
            address_dict = json.loads(geo_data['address_component'])
            project.setdefault('general_data', {}).update({
                'address': f"{address_dict.get('street', '')} {address_dict.get('streetNumber', '')}, {address_dict.get('locality', '')}",
                'municipality': address_dict.get('municipality', ''),
                'province': address_dict.get('province', ''),
                'region': address_dict.get('region', '')
            })
        except json.JSONDecodeError:
            logger.warning(
                'update_session: Errore nel parsing address_component')

    update_project_session(request, project)
    return success_response('Dati di sessione aggiornati')


@require_http_methods(["POST"])
@log_operation("update_polygon")
def update_polygon(request):
    """Aggiorna i poligoni nel generatore del progetto."""
    try:
        data = json.loads(request.body)
        polygons_by_subfield = data.get('polygons_by_subfield', {})

        project, _, _ = get_project_data(request)
        generator = project.get('generator', {})

        # Aggiorna i poligoni nei subfield
        for subfield_name, polygon_data in polygons_by_subfield.items():
            for field_data in generator.values():
                if subfield_name in field_data:
                    field_data[subfield_name].update(polygon_data)
                    break

        project['generator'] = generator
        update_project_session(request, project)

        return success_response('Poligoni salvati con successo nel generatore')

    except json.JSONDecodeError:
        return error_response('Errore nel parsing dei dati JSON', 400)


@csrf_exempt
@require_project_session
@log_operation("upload_image")
def upload_image(request):
    """Gestisce l'upload di immagini."""
    if request.method != 'POST':
        return error_response('Metodo non valido', 400)

    image = request.FILES.get('image')
    if not image:
        return error_response('Nessuna immagine caricata', 400)

    _, project_code, project_path = get_project_data(request)

    try:
        key = handle_image_upload(image, project_path)
        return JsonResponse({
            'success': True,
            'message': 'Immagine caricata con successo',
            'path': key
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@log_operation("save_where")
def save_where(request):
    """Salva la localizzazione del progetto."""
    if request.method != 'POST':
        return error_response('Metodo non valido', 400)

    location = request.POST.get('mounting')
    if not location:
        return error_response('Parametro mounting mancante', 400)

    project = request.session.get('project', {})
    project['mounting'] = location
    update_project_session(request, project)

    return success_response('Localizzazione salvata con successo')


@log_operation("save_type")
def save_type(request):
    """Salva il tipo dell'impianto."""
    if request.method != 'POST':
        return error_response('Metodo non valido', 400)

    # Dati del tipo di impianto
    type_data = {
        'grid_connected': request.POST.get('grid_connected'),
        'storage': request.POST.get('storage'),
        'self_consumption': request.POST.get('self_consumption'),
        'rid': request.POST.get('rid')
    }

    # Logica speciale per RID
    if type_data['grid_connected'] in ['0', 0]:
        type_data['rid'] = '0'

    if type_data['storage'] in ['1', 1]:
        type_data['self_consumption'] = '1'

    project = request.session.get('project', {})
    project.update(type_data)
    update_project_session(request, project)

    return success_response('Tipo di impianto salvato con successo')


@log_operation("save_solar_data")
def save_solar_data(request):
    """Salva i dati solari."""
    if request.method != 'POST':
        return error_response('Metodo non valido', 400)

    try:
        data = json.loads(request.body)
        solar_data = {
            'albedo': data.get('albedo', ''),
            'shading_horizon': data.get('rangeValueHorizon', '')
        }

        project = request.session.get('project', {})
        project.update(solar_data)
        update_project_session(request, project)

        return success_response('Dati solari salvati con successo')

    except json.JSONDecodeError:
        return error_response('Errore nel parsing dei dati JSON', 400)


@log_operation("save_configuration")
def save_configuration(request):
    """Salva la configurazione dell'impianto."""
    if request.method != 'POST':
        return error_response('Metodo non valido', 400)

    try:
        # Parse form data
        data = request.body.decode('utf-8')
        form_data = dict(item.split('=') for item in data.split('&'))
        config_data = {
            'peak_power': {
                'value': form_data.get('peak_power_value', ''),
                'unit': form_data.get('peak_power_unit', '')
            },
            'plant_scope': form_data.get('scope_1', ''),
            'auto_consumption': form_data.get('scope_2', ''),
            'private_house': form_data.get('scope_3', ''),
        }

        project = request.session.get('project', {})
        project.update(config_data)
        update_project_session(request, project)

        return success_response('Configurazione salvata con successo')

    except Exception as e:
        return error_response(f'Errore nel parsing dei dati: {str(e)}', 400)


@csrf_exempt
@require_project_session
@log_operation("save_general_data")
def save_general_data(request):
    """Salva i dati generali del progetto."""
    if request.method != 'POST':
        return error_response('Metodo non valido', 400)

    project, project_code, project_path = get_project_data(request)

    # Gestione immagini
    image_fields = ['cover_image', 'cover_logo_1',
                    'cover_logo_2', 'cover_logo_3']
    
    # Mappa dei nomi personalizzati per le immagini
    image_names = {
        'cover_image': 'cover_image',
        'cover_logo_1': 'cover_logo_1',
        'cover_logo_2': 'cover_logo_2', 
        'cover_logo_3': 'cover_logo_3'
    }
    
    general_data = project.setdefault('general_data', {})
    
    # Inizializza i dizionari per URL e percorsi delle immagini se non esistono
    if 'images_url' not in project:
        project['images_url'] = {}
    if 'images_paths' not in project:
        project['images_paths'] = {}

    for image_field in image_fields:
        image_file = request.FILES.get(image_field)
        if image_file:
            try:
                # Ottieni l'estensione del file originale
                file_extension = os.path.splitext(image_file.name)[1].lower()
                # Crea il nome personalizzato con l'estensione originale
                custom_name = f"{image_names[image_field]}{file_extension}"
                
                key = handle_image_upload(image_file, project_path, custom_name)
                general_data[image_field] = key
                
                # Salva il percorso di DigitalOcean e genera l'URL presigned
                project['images_paths'][image_field] = key
                project['images_url'][image_field] = get_image_url(key)
            except Exception as e:
                return error_response(f'Errore salvando {image_field}: {str(e)}', 500)

    # Gestisce le immagini già esistenti (rigenera URL per quelle non ricaricate)
    for image_field in image_fields:
        if image_field in general_data and image_field not in request.FILES:
            # L'immagine esiste già nei dati ma non è stata ricaricata
            key = general_data[image_field]
            project['images_paths'][image_field] = key
            project['images_url'][image_field] = get_image_url(key)

    # Aggiorna campi testuali
    text_fields = [
        'project_title', 'municipality', 'province', 'region', 'cadastral_references',
        'project_acronym', 'identification_code', 'address', 'revision_date',
        'revision_number', 'edit_by', 'verified_by', 'approved_by',
        'site_information', 'intervention_scope', 'copertina'
    ]

    for field in text_fields:
        general_data[field] = request.POST.get(field, '')

    update_project_session(request, project)
    return success_response('Dati generali salvati con successo')


@csrf_exempt
@require_project_session
@log_operation("save_anagrafy_data_1")
def save_anagrafy_data_1(request):
    """Salva i dati anagrafici di cliente e proponente."""
    if request.method != 'POST':
        return error_response('Metodo non valido', 400)

    project, project_code, project_path = get_project_data(request)

    # Inizializza sezioni dati
    client_data = project.setdefault('client_data', {})
    proposer_data = project.setdefault('proposer_data', {})
    
    # Inizializza i dizionari per URL e percorsi delle immagini se non esistono
    if 'images_url' not in project:
        project['images_url'] = {}
    if 'images_paths' not in project:
        project['images_paths'] = {}

    # Gestione loghi
    # Mappa dei nomi personalizzati per i loghi
    logo_names = {
        'client_logo': 'client_logo',
        'proposer_logo': 'proposer_logo'
    }
    
    for logo_field, data_section in [('client_logo', client_data), ('proposer_logo', proposer_data)]:
        logo_file = request.FILES.get(logo_field)
        if logo_file:
            try:
                # Ottieni l'estensione del file originale
                file_extension = os.path.splitext(logo_file.name)[1].lower()
                # Crea il nome personalizzato con l'estensione originale
                custom_name = f"{logo_names[logo_field]}{file_extension}"
                
                key = handle_image_upload(logo_file, project_path, custom_name)
                data_section[logo_field] = key
                
                # Genera l'URL presigned
                logo_url = get_image_url(key)
                
                # Salva il percorso e URL nei dizionari centralizzati
                project['images_paths'][logo_field] = key
                project['images_url'][logo_field] = logo_url
                
                # Salva l'URL anche direttamente nei dati specifici
                if logo_field == 'client_logo':
                    client_data['client_logo_url'] = logo_url
                elif logo_field == 'proposer_logo':
                    proposer_data['proposer_logo_url'] = logo_url
            except Exception as e:
                return error_response(f'Errore salvando {logo_field}: {str(e)}', 500)

    # Gestisce i loghi già esistenti (rigenera URL per quelli non ricaricati)
    for logo_field, data_section in [('client_logo', client_data), ('proposer_logo', proposer_data)]:
        if logo_field in data_section and logo_field not in request.FILES:
            # Il logo esiste già nei dati ma non è stato ricaricato
            key = data_section[logo_field]
            logo_url = get_image_url(key)
            
            # Salva nei dizionari centralizzati
            project['images_paths'][logo_field] = key
            project['images_url'][logo_field] = logo_url
            
            # Salva l'URL anche direttamente nei dati specifici
            if logo_field == 'client_logo':
                client_data['client_logo_url'] = logo_url
            elif logo_field == 'proposer_logo':
                proposer_data['proposer_logo_url'] = logo_url

    # Aggiorna campi cliente
    client_fields = [
        'client_name', 'client_additional_info'
    ]
    for field in client_fields:
        client_data[field] = request.POST.get(field, '')

    # Aggiorna campi proponente
    proposer_fields = [
        'proposer_name', 'proposer_additional_info'
    ]
    for field in proposer_fields:
        proposer_data[field] = request.POST.get(field, '')

    update_project_session(request, project)
    return success_response('Dati anagrafici salvati con successo')


@require_project_session
@log_operation("save_designers_and_collaborators")
def save_designers_and_collaborators(request):
    # Funzione per salvare i dati dei progettisti e collaboratori con gestione del logo
    """Salva progettisti e collaboratori con struttura semplificata."""
    if request.method != 'POST':
        return error_response('Metodo non valido', 400)

    try:
        project, project_code, project_path = get_project_data(request)

        # Inizializza array se non esistono
        project.setdefault('designers_data', [])
        project.setdefault('collaborators_data', [])
        
        # Inizializza i dizionari per URL e percorsi delle immagini se non esistono
        if 'images_url' not in project:
            project['images_url'] = {}
        if 'images_paths' not in project:
            project['images_paths'] = {}

        # Gestione eliminazioni progettisti
        deleted_designers = [request.POST.get(f'deleted_designer_{i}') for i in range(
            len([key for key in request.POST.keys() if key.startswith('deleted_designer_')]))]
        project['designers_data'] = [d for d in project['designers_data']
                                     if str(d.get('id')) not in deleted_designers]

        # Gestione eliminazioni collaboratori (manteniamo per compatibilità)
        deleted_collaborators = [request.POST.get(f'deleted_collaborator_{i}') for i in range(
            len([key for key in request.POST.keys() if key.startswith('deleted_collaborator_')]))]
        project['collaborators_data'] = [c for c in project['collaborators_data']
                                         if str(c.get('id')) not in deleted_collaborators]

        # Gestione progettisti con struttura semplificata
        designers = []
        designer_count = len(
            [key for key in request.POST.keys() if key.startswith('designer_name_')])

        for i in range(designer_count):
            # Dati progettista semplificati
            designer_data = {
                'id': request.POST.get(f'designer_id_{i}', None),
                'designer_name': request.POST.get(f'designer_name_{i}', ''),
                'designer_additional_info': request.POST.get(f'designer_additional_info_{i}', '')
            }

            # Gestione del logo
            logo_file = request.FILES.get(f'designer_logo_{i}')
            existing_logo = request.POST.get(f'designer_logo_existing_{i}')

            if logo_file:
                # Salva il nuovo file logo usando la funzione esistente
                try:
                    # Crea nome personalizzato per il logo del progettista
                    file_extension = os.path.splitext(logo_file.name)[1].lower()
                    custom_name = f"designer_logo_{i}{file_extension}"
                    
                    logo_key = handle_image_upload(logo_file, project_path, custom_name)
                    designer_data['designer_logo'] = logo_key
                    
                    # Salva il percorso di DigitalOcean e genera l'URL presigned
                    designer_logo_key = f"designer_logo_{i}"
                    project['images_paths'][designer_logo_key] = logo_key
                    project['images_url'][designer_logo_key] = get_image_url(logo_key)
                    designer_data['designer_logo_url'] = get_image_url(logo_key)
                except Exception as e:
                    logger.error(
                        f"Errore nel salvataggio del logo per progettista {i}: {e}")
                    designer_data['designer_logo'] = '#'
                    designer_data['designer_logo_url'] = '#'
            elif existing_logo and existing_logo != '#':
                # Mantieni il logo esistente
                designer_data['designer_logo'] = existing_logo
                # Genera l'URL presigned per il logo esistente
                try:
                    designer_logo_key = f"designer_logo_{i}"
                    project['images_paths'][designer_logo_key] = existing_logo
                    project['images_url'][designer_logo_key] = get_image_url(existing_logo)
                    designer_data['designer_logo_url'] = get_image_url(existing_logo)
                except Exception as e:
                    logger.error(
                        f"Errore nel generare l'URL per il logo esistente del progettista {i}: {e}")
                    designer_data['designer_logo_url'] = '#'
            else:
                # Nessun logo
                designer_data['designer_logo'] = '#'
                designer_data['designer_logo_url'] = '#'

            designers.append(designer_data)

        # Gestione collaboratori (manteniamo per compatibilità)
        collaborators = []
        collaborator_count = len(
            [key for key in request.POST.keys() if key.startswith('collaborator_name_')])

        for i in range(collaborator_count):
            collaborators.append({
                'id': request.POST.get(f'collaborator_id_{i}', None),
                'name': request.POST.get(f'collaborator_name_{i}', '')
            })

        # Aggiorna progetto
        project['designers_data'] = designers
        project['collaborators_data'] = collaborators
        update_project_session(request, project)

        return JsonResponse({
            'success': True,
            'message': 'Progettisti salvati con successo'
        })

    except Exception as e:
        return error_response(f'Errore nel salvataggio: {str(e)}', 500)


@csrf_exempt
@require_POST
@log_operation("save_generator_structure")
def save_generator_structure(request):
    """Salva la struttura del generatore."""
    try:
        data = json.loads(request.body)
        project = request.session.get('project', {})

        # Inizializza generatore
        generator = {}
        fields = data.get('fields', [])
        letters = ['A', 'B', 'C', 'D']

        for i, field in enumerate(fields):
            if i >= len(letters):
                break

            field_name = letters[i]
            subfields_count = int(field.get('subfields', 1))

            # Crea sottocampi
            subfields = {}
            for j in range(subfields_count):
                subfield_name = f"{letters[i]}{j+1}"
                subfields[subfield_name] = {}

            generator[field_name] = subfields

        # Aggiorna sessione
        project['generator'] = generator
        update_project_session(request, project)

        return success_response('Struttura generatore salvata con successo', generator)

    except json.JSONDecodeError:
        return error_response('Errore nel formato dei dati', 400)


@require_http_methods(["POST"])
@log_operation("save_subfields_configuration")
def save_subfields_configuration(request):
    """Salva la configurazione dei sottocampi."""
    try:
        data = json.loads(request.body)
        subfields_data = data.get('subfields_data', {})

        project = request.session.get('project', {})
        generator = project.get('generator', {})

        # Aggiorna configurazione sottocampi
        for field_name, field_data in generator.items():
            for subfield_name, subfield_data in field_data.items():
                if subfield_name in subfields_data:
                    subfield_data.update(subfields_data[subfield_name])

        project['generator'] = generator
        update_project_session(request, project)

        return success_response('Configurazione sottocampi salvata con successo')

    except json.JSONDecodeError:
        return error_response('Errore nel parsing dei dati JSON', 400)

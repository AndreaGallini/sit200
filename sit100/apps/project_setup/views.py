import time
from storage.factory import StorageFactory
from .save_views import *
from .clear_views import *
from .designer_views import *
import logging
from dotenv import load_dotenv
from django.conf import settings
from django.shortcuts import render

APP_NAME = settings.APP_NAME

logger = logging.getLogger('django')
load_dotenv()


def area_init(request):
    """Gestisce la visualizzazione della mappa iniziale del progetto."""
    logger.info('Mappa iniziale caricata con successo')
    return render(request, 'project_setup/area_init.html')


def project_map(request):
    """Gestisce la visualizzazione della mappa di progetto."""
    logger.info('Mappa di progetto caricata con successo')
    return render(request, 'project_setup/new_map.html')


def where(request):
    """Gestisce la visualizzazione della pagina dove."""
    logger.info('Pagina dove caricata con successo')
    return render(request, 'project_setup/where.html')


def typology(request):
    """Gestisce la visualizzazione della pagina tipologia."""
    return render(request, 'project_setup/type.html')


def subfields_conf(request):
    """Gestisce la configurazione dei sottocampi."""
    return render(request, 'project_setup/subfield_conf.html')


def solar_and_dark(request):
    """Gestisce la visualizzazione della pagina solar and dark."""
    return render(request, 'project_setup/solar_and_dark.html')


def config_structure(request):
    """Gestisce la configurazione della struttura."""
    return render(request, 'project_setup/config_structure.html')


def project_data(request):
    """Gestisce la visualizzazione dei dati del progetto con percorsi DigitalOcean."""
    project = request.session.get('project', {})
    project_code = project.get('project_code', '')
    


    logger.info(
        f'project_data, caricamento dati per il progetto {project_code}')
    return render(request, 'project_setup/project_data.html')


def anagrafy_data(request):
    """Gestisce la visualizzazione dei dati anagrafici con percorsi DigitalOcean."""
    project = request.session.get('project', {})
    project_code = project.get('project_code', '')
    
    logger.info(f'anagrafy_data, caricamento dati per il progetto {project_code}')
    return render(request, 'project_setup/anagrafy_data.html')


def anagrafy_data_2(request):
    """Visualizza la pagina anagrafy_data_2, pre-caricando i progettisti dalla sessione se presenti."""
    try:
        logger.info("Starting anagrafy_data_2 view")

        project = request.session.get('project', {})

        designers_data = []
        collaborators_data = []

        # Pre-carica i progettisti dalla sessione se presenti
        session_designers = project.get('designers_data', [])
        if session_designers:
            for designer in session_designers:
                designer_entry = {
                    'id': designer.get('id', None),
                    'designer_name': designer.get('designer_name', ''),
                    'designer_additional_info': designer.get('designer_additional_info', ''),
                    'designer_logo': designer.get('designer_logo', '#'),
                    'designer_logo_url': designer.get('designer_logo_url', '#'),
                }

                designers_data.append(designer_entry)

        # Pre-carica i collaboratori dalla sessione se presenti (manteniamo per compatibilità)
        session_collaborators = project.get('collaborators_data', [])
        if session_collaborators:
            for collaborator in session_collaborators:
                collaborator_entry = {
                    'id': collaborator.get('id', None),
                    'name': collaborator.get('name', ''),
                }
                collaborators_data.append(collaborator_entry)



        # Context specifico per questa view
        context = {
            'designers': designers_data,
            'collaborators': collaborators_data,
        }

        logger.info(f"Context prepared: {context}")
        return render(request, 'project_setup/anagrafy_data_2.html', context)

    except Exception as e:
        logger.error(f"Error in anagrafy_data_2: {str(e)}", exc_info=True)
        raise


def display_session_data(request):
    """Visualizza i dati della sessione per debug."""
    session_data = request.session.items()
    context = {
        'session_data': session_data
    }
    return render(request, 'project_setup/display_session_data.html', context)


def user_choise(request):
    """Gestisce la scelta dell'utente per procedere."""
    return render(request, 'project_setup/proceed.html')


def get_image_url(key, exp_time=3600):
    """Recupera l'URL dell'immagine visualizzabile su web. Per Spaces deve essere una presigned_url."""
    storage = StorageFactory.get_storage_service()
    try:
        url = storage.get_presigned_url(key, exp_time=exp_time)
        if url:
            return url
        else:
            logger.warning(
                f"Impossibile generare l'URL presigned per la chiave '{key}'.")
            return None
    except RuntimeError as e:
        logger.error(
            f"Errore durante la generazione dell'URL per la chiave '{key}': {e}")
        return None
    except Exception as e:
        logger.critical(
            f"Errore critico durante il recupero dell'URL per la chiave '{key}': {e}")
        return None


def report_page(request):
    """Gestisce la visualizzazione della pagina di report."""
    project = request.session.get('project', {})

    # Context specifico per questa view
    context = {
        'project': project  # Sovrascrive il project dal context processor con quello aggiornato
    }

    return render(request, 'project_setup/report_page.html', context)

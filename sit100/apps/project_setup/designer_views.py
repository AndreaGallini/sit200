from django.http import JsonResponse
from apps.project.models import Designer
import logging
logger = logging.getLogger('django')


def add_designer(request):
    """
    Aggiunge un nuovo progettista alla lista dei progettisti nella sessione dell'utente.
    """
    project = request.session.get('project', {})
    project_code = project['project_code']

    try:
        # Recupera i dati dal form
        designer_name = request.POST.get('designer_name', '').strip()
        designer_person = request.POST.get('designer_person', '').strip()
        designer_address_1 = request.POST.get('designer_address_1', '').strip()
        designer_address_2 = request.POST.get('designer_address_2', '').strip()
        designer_fiscal_code = request.POST.get(
            'designer_fiscal_code', '').strip()
        designer_phone_number = request.POST.get(
            'designer_phone_number', '').strip()
        designer_fax_number = request.POST.get(
            'designer_fax_number', '').strip()
        designer_email = request.POST.get('designer_email', '').strip()
        designer_pec = request.POST.get('designer_pec', '').strip()
        designer_albo = request.POST.get('designer_albo', '').strip()
        logo = request.FILES.get('logo', None)

        # Validazione dei dati (puoi aggiungere ulteriori controlli)
        if not designer_name:
            logger.warning(
                f"Errore nell'inserimento dei dati designer , {project_code}")
            return JsonResponse({'success': False, 'error': 'Il campo Denominazione è obbligatorio.'}, status=400)

        # Prepara i dati del progettista
        designer_entry = {
            'designer_name': designer_name,
            'designer_person': designer_person,
            'designer_address_1': designer_address_1,
            'designer_address_2': designer_address_2,
            'designer_fiscal_code': designer_fiscal_code,
            'designer_phone_number': designer_phone_number,
            'designer_fax_number': designer_fax_number,
            'designer_email': designer_email,
            'designer_pec': designer_pec,
            'designer_albo': designer_albo,
            'designer_logo': logo  # Placeholder, verrà aggiornato dopo il salvataggio del logo
        }

        # Gestione del logo
        if logo:
            designer_entry['designer_logo'] = '/media/temp/' + logo.name
        designers = project.get('designers', [])

        # Aggiungi il nuovo progettista alla lista
        designers.append(designer_entry)

        # Aggiorna l'oggetto project nella sessione
        project['designers'] = designers
        # Salva i cambiamenti nella sessione
        request.session['project'] = project
        logger.info(f'Designer aggiunto , {project_code}')
        return JsonResponse({'success': True, 'designer': designer_entry})
    except Exception as e:
        logger.warning(f'Errore add_designer {e} , {project_code}')
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def get_designers_data(request):
    """
    Recupera tutti i progettisti associati all'utente corrente dalla sessione se presenti,
    altrimenti dal database, e restituisce i dati in formato JSON.
    Ora supporta la struttura semplificata con solo nominativo e ulteriori informazioni.
    """
    try:
        project = request.session.get('project', {})
        # Cambiato da 'designers' a 'designers_data'
        session_designers = project.get('designers_data', [])
        project_code = project.get('project_code', '')

        if session_designers:
            # Pre-carica i progettisti dalla sessione
            designers_list = []
            for designer in session_designers:
                designer_entry = {
                    'id': designer.get('id', None),
                    'designer_name': designer.get('designer_name', ''),
                    'designer_additional_info': designer.get('designer_additional_info', ''),
                    'designer_logo': designer.get('logo', '')
                }
                designers_list.append(designer_entry)
        else:
            # Carica i progettisti dal database (mantenendo compatibilità con struttura vecchia)
            designers = Designer.objects.filter(user=request.user)
            designers_list = []
            for designer in designers:
                data = designer.designer_data.copy() if designer.designer_data else {}
                # Gestione sicura del campo logo - estrai solo il nome/path
                logo_path = None
                if designer.logo and hasattr(designer.logo, 'name') and designer.logo.name:
                    logo_path = designer.logo.name

                # Adatta la struttura vecchia a quella nuova
                designer_entry = {
                    'id': designer.id,
                    'designer_name': data.get('designer_name', ''),
                    'designer_additional_info': data.get('designer_additional_info', ''),
                    'designer_logo': data.get('designer_logo')
                }
                designers_list.append(designer_entry)

        return JsonResponse({'designers': designers_list}, status=200)

    except Exception as e:
        logger.warning(
            f'Errore get_designer_data: {e}, project_code: {project_code}')
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

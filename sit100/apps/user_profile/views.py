from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UsernameChangeForm
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import time
from .forms import EmailForm
from django.core.mail import send_mail
from apps.project.models import Designer
from .forms import DesignerForm
from django.http import JsonResponse
import os
import tempfile

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from dotenv import load_dotenv
from django.conf import settings
from storage.do_spaces import SpacesStorageService
from django.utils.timezone import now
from django.core.exceptions import ValidationError

APP_NAME = settings.APP_NAME

load_dotenv()


@login_required
def delete_account(request):
    if request.method == 'POST':
        try:
            # Store the user object before deleting it
            user = request.user

            # Log the user out - must be done before deletion
            logout(request)

            # Delete the user (this will cascade to related models)
            user.delete()

            # Redirect to the login page with a message
            messages.success(
                request, 'Il tuo account è stato eliminato con successo.')
            return redirect('login')

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    else:
        # Display confirmation page
        return render(request, 'user_profile/delete_account.html')


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nome utente cambiato con successo!')
            # Redirigi alla stessa pagina dopo il salvataggio
            return redirect('/user/')
    else:
        form = UsernameChangeForm(instance=request.user)

    context = {
        'form': form,
        'user': request.user,
        'APP_NAME': APP_NAME,
        'time': time
    }
    return render(request, 'user_profile/user_info.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Mantiene l'utente loggato dopo il cambio di password
            update_session_auth_hash(request, user)
            messages.success(request, 'Password cambiata con successo!')
            return redirect('/user/sicurezza')
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        'form': form,
        'APP_NAME': APP_NAME,
        'time': time
    }
    return render(request, 'user_profile/security.html', context)


@login_required
def user_homepage(request):
    context = {
        'time': time
    }
    return render(request, 'user_profile/user_homepage.html', context)


@login_required
def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            dropdown = form.cleaned_data['dropdown']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            user_email = request.user.email
            email_body = f"Problema: {dropdown}\n\nDescrizione problema:\n{message}\n\nEmail utente: {user_email}"

            try:
                # Get email config values before sending
                from_email = os.getenv('DEFAULT_FROM_EMAIL')
                to_email = os.getenv('ASSISTANCE_EMAIL')
                email_host = os.getenv('EMAIL_HOST')
                email_port = os.getenv('EMAIL_PORT', 465)
                # Check if email variables are properly set
                if not from_email:
                    raise ValueError(
                        "EMAIL_HOST_USER environment variable is not set")

                # Use send_mail which is compatible with the custom backend
                result = send_mail(
                    subject,
                    email_body,
                    from_email,  # From email
                    [to_email],  # To email (sending to the system email)
                    fail_silently=False,
                )

                messages.success(request, 'Email inviata con successo!')
                return redirect('/user/assistenza/')
            except Exception as e:
                # More detailed error message
                error_msg = f'Errore nell\'invio dell\'email: {str(e)}'
                messages.error(request, error_msg)
                # Don't redirect on error, so user can see the error message
                return render(request, 'user_profile/assistance.html', {'form': form, 'time': time})
    else:
        form = EmailForm()

    context = {
        'form': form,
        'APP_NAME': APP_NAME,
        'time': time
    }

    return render(request, 'user_profile/assistance.html', context)

# views.py


@login_required
def save_designer_data(request):
    """
    Gestisce l'aggiunta e la modifica dei dati del progettista semplificati.
    Campi supportati: designer_name, designer_additional_info, designer_logo
    """
    try:
        designer = Designer.objects.get(user=request.user)
    except Designer.DoesNotExist:
        designer = None

    if request.method == 'POST':
        temp_logo_path = None
        try:
            # Estrai i dati specifici del form semplificato
            designer_name = request.POST.get('designer_name', '').strip()
            designer_additional_info = request.POST.get(
                'designer_additional_info', '').strip()
            logo = request.FILES.get('designer_logo', None)

            # Validazione base
            if not designer_name:
                return JsonResponse({'success': False, 'error': 'Il campo Nominativo è obbligatorio.'}, status=400)

            # Crea il dizionario con i dati semplificati
            designer_data_dict = {
                'designer_name': designer_name,
                'designer_additional_info': designer_additional_info
            }

            # Crea o aggiorna il designer
            if designer is None:
                designer = Designer(user=request.user)

            # Aggiorna i dati
            designer.designer_data = designer_data_dict
            # Gestione del logo utilizzando il sistema di storage
            if logo:
                # Elimina il logo precedente se esiste
                if designer.logo:
                    try:
                        designer.logo.delete(save=False)
                    except Exception:
                        pass  # Ignora errori nella cancellazione del file precedente

                # Salva il nuovo logo utilizzando il sistema di storage
                try:
                    # Sanitizzazione del nome file
                    username_safe = "".join(
                        c for c in request.user.username if c.isalnum() or c in ('_', '-'))
                    file_extension = logo.name.split('.')[-1]
                    timestamp = int(now().timestamp())
                    logo_filename = f"logo_{username_safe}.{file_extension}"

                    # Creazione file temporaneo
                    temp_dir = tempfile.gettempdir()
                    temp_logo_path = f"{temp_dir}/{logo_filename}"

                    # Scrivi il contenuto del logo nel file temporaneo
                    with open(temp_logo_path, 'wb') as f:
                        for chunk in logo.chunks():
                            f.write(chunk)

                    # Upload su storage utilizzando il percorso corretto per i file utente
                    storage = SpacesStorageService()
                    destination_path = f"user_{request.user.id}/{logo_filename}"
                    
                    uploaded_key = storage.upload_image(
                        temp_logo_path, destination_path)
                    designer.logo.name = uploaded_key
                    
                    # Genera anche l'URL firmato di DigitalOcean per il campo designer_logo
                    try:
                        logo_full_url = storage.get_presigned_url(uploaded_key, exp_time=864000000000)  # 24 ore
                        # Salva l'URL firmato nel campo designer_logo del designer_data
                        if not designer.designer_data:
                            designer.designer_data = {}
                        designer.designer_data['designer_logo'] = logo_full_url
                        designer.save()
                    except Exception as e:
                        print(f"Errore nel generare l'URL firmato del logo: {e}")
                        # Se non riesce a generare l'URL, salva comunque il percorso
                        if not designer.designer_data:
                            designer.designer_data = {}
                        #designer.designer_data['designer_logo'] = uploaded_key

                except Exception as e:
                    return JsonResponse({'success': False, 'error': f'Errore nel salvataggio del logo: {str(e)}'}, status=500)

                finally:
                    # Pulisci il file temporaneo
                    if temp_logo_path and os.path.exists(temp_logo_path):
                        os.remove(temp_logo_path)

            # Salva il designer
            designer.save()
            return redirect('/user/save_designer_data')

        except Exception as e:
            # Pulisci il file temporaneo in caso di errore
            if temp_logo_path and os.path.exists(temp_logo_path):
                os.remove(temp_logo_path)
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        # GET request - mostra il form
        try:
            designer = Designer.objects.get(user=request.user)
            initial_data = designer.designer_data or {}
        except Designer.DoesNotExist:
            designer = None
            initial_data = {}

        # Genera URL presigned per le immagini se esistono
        images_url = {}
        if designer and designer.logo and hasattr(designer.logo, 'name') and designer.logo.name:
            try:
                storage = SpacesStorageService()
                logo_url = storage.get_presigned_url(designer.logo.name, exp_time=3600)
                images_url['designer_logo'] = logo_url
            except Exception as e:
                images_url['designer_logo'] = None
        else:
            images_url['designer_logo'] = None

        context = {
            'form': initial_data,
            'designer': designer,
            'APP_NAME': APP_NAME,
            'images_url': images_url
        }
        return render(request, 'user_profile/designer_data.html', context)


@login_required
def get_designers_data(request):
    """
    Restituisce i dati dei designer dell'utente corrente in formato JSON.
    Utilizzato per precompilare i form con i dati esistenti.
    Segue la stessa struttura di designer_views.py
    """
    if request.method == 'GET':
        try:
            # Carica tutti i progettisti dal database (come in designer_views.py)
            designers = Designer.objects.filter(user=request.user)
            designers_list = []
            for designer in designers:
                data = designer.designer_data.copy() if designer.designer_data else {}

                # Gestione sicura del campo logo - estrai solo il nome/path
                logo_path = None
                logo_url = None

                if designer.logo and hasattr(designer.logo, 'name') and designer.logo.name:
                    logo_path = designer.logo.name
                    try:
                        storage = SpacesStorageService()
                        # Genera un URL diretto e permanente per accedere al logo
                        logo_url = storage.get_direct_url(logo_path)
                    except Exception as e:
                        logo_url = None
                # Adatta la struttura seguendo il pattern di designer_views.py
                designer_entry = {
                    'id': designer.id,
                    'designer_name': data.get('designer_name', ''),
                    'designer_additional_info': data.get('designer_additional_info', ''),
                    'designer_logo': data.get('designer_logo', logo_path if logo_path else '#'),
                    'designer_logo_url': logo_url if logo_url else '#'
                }
                designers_list.append(designer_entry)
            return JsonResponse({'designers': designers_list})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Metodo non consentito'}, status=405)


@login_required
def questionario(request):
    """
    Gestisce il form del questionario di feedback.
    """
    if request.method == 'POST':
        temp_path = None
        try:
            # Raccolta dati dal form
            form_data = {
                'intuitivita': request.POST.get('intuitivita', ''),
                'difficolta_navigazione': request.POST.get('difficolta_navigazione', ''),
                'difficolta_dettagli': request.POST.get('difficolta_dettagli', ''),
                'problemi_tecnici': request.POST.get('problemi_tecnici', ''),
                'problemi_dettagli': request.POST.get('problemi_dettagli', ''),
                'consiglio_piattaforma': request.POST.get('consiglio_piattaforma', ''),
                'consiglio_dettagli': request.POST.get('consiglio_dettagli', ''),
                'suggerimenti': request.POST.get('suggerimenti', ''),
                'user': request.user.username,
                'user_email': request.user.email,
                'timestamp': now().strftime('%Y-%m-%d_%H-%M-%S')
            }

            # Sanitizzazione del nome file
            username_safe = "".join(
                c for c in request.user.username if c.isalnum() or c in ('_', '-'))
            feedback_file = f"feedback_{username_safe}_{form_data['timestamp']}.txt"

            # Creazione file temporaneo
            temp_dir = tempfile.gettempdir()
            temp_path = f"{temp_dir}/{feedback_file}"

            with open(temp_path, 'w', encoding='utf-8') as f:
                for key, value in form_data.items():
                    f.write(f"{key}: {value}\n")

            # Upload su storage
            storage = SpacesStorageService()
            storage.upload_file(temp_path, f"feedback/{feedback_file}")

            messages.success(
                request, "Grazie per il tuo feedback! Le tue opinioni sono molto importanti per noi.")

        except ValidationError as ve:
            messages.error(request, f"Errore di validazione: {ve}")

        except Exception as e:
            messages.error(
                request, f"Si è verificato un errore durante l'invio del feedback: {str(e)}")

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    # Renderizza il template del questionario
    context = {
        'APP_NAME': APP_NAME,
        'time': time
    }
    return render(request, 'user_profile/questionario.html', context)

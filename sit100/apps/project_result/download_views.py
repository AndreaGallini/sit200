# views.py
import mimetypes
import os
import uuid
import hashlib

from django.core.cache import cache
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse, JsonResponse
from django.conf import settings

from apps.project.models import Project
from storage.factory import StorageFactory


@login_required
def download_word_file(request, project_code):
    """Restituisce il file Word associato a un progetto, solo se l'utente è il proprietario."""

    project = get_object_or_404(Project, project_code=project_code)
    if project.user_id_id != request.user.id:
        return HttpResponse("Non sei autorizzato ad accedere al sistema.", status=404)

    if not project.word_file:
        return HttpResponse("Non sei autorizzato ad accedere.", status=404)

    file_key = project.word_file  # Prende il percorso salvato nel database
    storage = StorageFactory.get_storage_service()
    try:
        file_data = storage.download_file(file_key)
        # Determina il tipo MIME
        content_type, _ = mimetypes.guess_type(os.path.basename(file_key))
        content_type = content_type or "application/octet-stream"
        response = HttpResponse(file_data, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_key)}"'
        return response
    except Exception as e:
        return HttpResponse(f"Errore durante il download", status=500)


@login_required
def download_design_word_file(request, project_code):
    """Restituisce il file Design associato a una distinta base di configurazione, solo se utente è proprietario."""

    project = get_object_or_404(Project, project_code=project_code)
    if project.user_id_id != request.user.id:
        return HttpResponse("Non sei autorizzato ad accedere al sistema.", status=404)

    if not project.word_file:
        return HttpResponse("Non sei autorizzato ad accedere.", status=404)
    
    file_key = project.keopebank['data']['word_design_path']  # Prende il percorso salvato nel database
    storage = StorageFactory.get_storage_service()
    try:
        file_data = storage.download_file(file_key)
        # Determina il tipo MIME
        content_type, _ = mimetypes.guess_type(os.path.basename(file_key))
        content_type = content_type or "application/octet-stream"
        response = HttpResponse(file_data, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_key)}"'
        return response
    except Exception as e:
        return HttpResponse(f"Errore durante il download", status=500)


def generate_secure_link(project_code, file_type):
    """Generate a secure random URL for file downloads"""
    # Create a unique token
    unique_id = str(uuid.uuid4())

    # Create a hash combining project code, file type and unique id
    hash_input = f"{project_code}-{file_type}-{unique_id}".encode('utf-8')
    secure_hash = hashlib.sha256(hash_input).hexdigest()[:12]

    # Store the mapping in cache for 1 hour (3600 seconds)
    cache_key = f"download_{secure_hash}"
    cache_value = {
        'project_code': project_code,
        'file_type': file_type
    }
    cache.set(cache_key, cache_value, 3600)
    return secure_hash


def secure_download(request, secure_hash):
    """Handle secure download requests"""
    # Get the cached information
    cache_key = f"download_{secure_hash}"
    cached_data = cache.get(cache_key)

    if not cached_data:
        return HttpResponse("Link non valido o scaduto", status=404)

    project_code = cached_data['project_code']
    file_type = cached_data['file_type']

    # Delete the used hash
    cache.delete(cache_key)

    # Redirect to appropriate download function
    if file_type == 'word':
        return download_word(request, project_code)
    elif file_type == 'pdf':
        return download_pdf(request, project_code)
    else:
        return HttpResponse("Tipo file non valido", status=400)


def download_word(request, project_code):
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, 'project_files', str(
            project_code), f'Report_{project_code}.docx')
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response = HttpResponse(
                    file.read(),
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                response['Content-Disposition'] = f'attachment; filename="Report_{project_code}.docx"'
                return response
        else:
            return HttpResponse("File non trovato", status=404)

    except Exception as e:
        return HttpResponse("Errore nel download del file", status=500)


def download_pdf(request, project_code):
    try:
        # Costruisci il path del file
        file_path = os.path.join(settings.MEDIA_ROOT, 'project_files', str(
            project_code), 'documento_di_testo.pdf')

        if not os.path.exists(file_path):
            return HttpResponse("File non trovato", status=404)

        # Importante: non chiudere il file, FileResponse se ne occuperà
        file = open(file_path, 'rb')

        response = FileResponse(
            file,
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="documento_di_testo.pdf"'
        return response

    except Exception as e:
        return HttpResponse("Errore nel download del file", status=500)

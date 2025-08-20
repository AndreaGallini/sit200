import os
import shutil

from django.conf import settings

from storage.base import StorageService


class LocalStorageService(StorageService):
    """Gestisce il salvataggio e recupero di file nel filesystem locale."""

    def __init__(self, base_path="media/"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def create_folder(self, project_path):
        """Crea la cartella di progetto nello storage."""
        pass

    def get_presigned_url(self, key, exp_time=3600):
        """Genera un URL firmato per accedere a un file privato."""
        pass

    def get_direct_url(self, key):
        """Genera un URL diretto e permanente per accedere a un file."""
        # Per lo storage locale, restituisce il path relativo
        return f"/media/{key}"

    def file_exists(self, object_name):
        """Verifica se un file esiste nello storage."""
        pass

    def download_image(self, download_path):
        """Scarica una immagine dallo storage."""
        pass

    def upload_image(self, source_image_path, destination_pathh):
        """Carica un'immagine in uno specifico percorso nello storage."""
        pass

    def upload_file(self, source_path: str, dest_path: str) -> str:
        """Copia un file nel percorso locale simulando un upload."""
        full_path = os.path.join(self.base_path, dest_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        shutil.copy2(source_path, full_path)
        print(f"File salvato localmente: {full_path}")
        return full_path

    def download_file(self, file_path: str) -> None:
        """Copia un file dalla cartella locale a un'altra destinazione."""
        pass

    def list_files_matching_pattern(self, folder, pattern):
        """Cerca i file che in una cartella che rispettano un determinato pattern."""
        pass

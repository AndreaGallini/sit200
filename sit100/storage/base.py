import tempfile
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger('django')


class StorageService(ABC):
    """Classe astratta per definire un'interfaccia comune tra diversi storage."""

    @abstractmethod
    def create_folder(self, folder_path):
        """Crea la cartella di progetto nello storage."""
        pass

    @abstractmethod
    def get_presigned_url(self, key, exp_time=3600):
        """Genera un URL firmato per accedere a un file privato."""
        pass

    @abstractmethod
    def get_direct_url(self, key):
        """Genera un URL diretto e permanente per accedere a un file."""
        pass

    @abstractmethod
    def file_exists(self, object_name):
        """Verifica se un file esiste nello storage."""
        pass

    @abstractmethod
    def download_image(self, download_path):
        """Scarica una immagine dallo storage."""
        pass

    @abstractmethod
    def upload_image(self, source_image_path, destination_path):
        """Carica un'immagine in uno specifico percorso nello storage."""
        pass

    @abstractmethod
    def upload_file(self, file_path, object_name):
        """Carica un file nello storage."""
        pass

    @abstractmethod
    def download_file(self, download_path):
        """Scarica un file dallo storage."""
        pass

    @abstractmethod
    def list_files_matching_pattern(self, folder, pattern):
        """Cerca i file che in una cartella che rispettano un determinato pattern."""
        pass

    @staticmethod
    def save_obj_image_to_tempfile(img_obj, dpi=0, file_format=None):
        """Salva l'oggetto PIL.Image in un file temporaneo e restituisce il percorso del file."""
        try:
            if file_format is None:
                file_format = img_obj.format if img_obj.format else 'PNG'
            with tempfile.NamedTemporaryFile(delete=False, mode='wb') as tmp_file:
                if dpi == 0:
                    img_obj.save(tmp_file, format=file_format)
                else:
                    img_obj.save(tmp_file, dpi=(dpi, dpi), format=file_format)
                tmp_file.seek(0)
                return tmp_file.name
        except Exception as e:
            logger.error(
                f"Errore nel salvataggio dell'oggetto immagine in un file temporaneo: {e}")
            raise

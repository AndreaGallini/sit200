"""Classe che gestisce tutte le operazioni con lo spaces di Digital Ocean."""
import os
import mimetypes
import re

from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError, ClientError


from storage.base import StorageService


class SpacesStorageService(StorageService):
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            endpoint_url=os.getenv('AWS_ENDPOINT_URL')
        )
        self.bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

    def create_folder(self, folder_path):
        """Crea una cartella nello storage Spaces. Solleva eccezioni in caso di errore."""
        key = f"{folder_path}/"
        try:
            self.s3.put_object(Bucket=self.bucket_name, Key=key)
        except NoCredentialsError as e:
            raise RuntimeError("Credenziali AWS non valide o mancanti.") from e
        except ClientError as e:
            raise RuntimeError(f"Errore AWS S3: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Errore imprevisto: {e}") from e

    def get_presigned_url(self, key, exp_time=3600):
        """Genera un URL firmato per accedere a un file privato."""
        try:
            clean_key = (
                key.lstrip('/')
                .replace(f'{self.bucket_name}/', '', 1)
                .replace(f'{self.bucket_name}', '', 1)
                .replace('//', '/')
            ).strip('/')

            # Genera l'URL firmato per ottenere il file da S3
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': clean_key
                },
                ExpiresIn=exp_time
            )
            return url
        except Exception as e:
            error_message = f"Errore nel generare l'URL firmato per '{key}': {e}"
            raise RuntimeError(error_message) from e

    def get_direct_url(self, key):
        """Genera un URL diretto e permanente per accedere a un file su DigitalOcean Spaces."""
        try:
            clean_key = (
                key.lstrip('/')
                .replace(f'{self.bucket_name}/', '', 1)
                .replace(f'{self.bucket_name}', '', 1)
                .replace('//', '/')
            ).strip('/')
            
            # Costruisce l'URL diretto usando l'endpoint di DigitalOcean Spaces
            endpoint_url = os.getenv('USER_URL')
            print(endpoint_url)
            if endpoint_url:
                # Rimuovi il protocollo se presente
                endpoint_url = endpoint_url.replace('https://', '').replace('http://', '')
                # Costruisce l'URL completo
                direct_url = f"https://{endpoint_url}{clean_key}"
                return direct_url
            else:
                raise RuntimeError("AWS_ENDPOINT_URL non configurato")
        except Exception as e:
            error_message = f"Errore nel generare l'URL diretto per '{key}': {e}"
            raise RuntimeError(error_message) from e

    def file_exists(self, object_name):
        """Verifica se un file esiste già su Spaces."""
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=object_name)
            return True
        except self.s3.exceptions.ClientError:
            return False

    def download_image(self, image_path):
        """Scarica l'immagine dallo storage (Spaces) e restituisce file-like object in memoria."""
        try:
            response = self.s3.get_object(
                Bucket=self.bucket_name, Key=image_path)
            image_data = response['Body'].read()  # dati binari
            image_stream = BytesIO(image_data)
            return image_stream
        except Exception as e:
            error_message = f"Errore nel download dell'immagine da '{image_path}': {e}"
            raise RuntimeError(error_message) from e

    def upload_image(self, source_image_path, destination_path):
        """Carica un file immagine nello storage su S3."""
        key = f"{destination_path}"
        content_type = mimetypes.guess_type(destination_path)[
            0] or "application/octet-stream"
        try:
            self.s3.upload_file(
                source_image_path,
                self.bucket_name,
                key,
                ExtraArgs={
                    "ACL": "private",
                    "ContentType": content_type
                }
            )
            return key
        except FileNotFoundError as e:
            error_message = f"Errore: Il file '{source_image_path}' non è stato trovato."
            raise RuntimeError(error_message) from e
        except NoCredentialsError as e:
            error_message = "Errore: Credenziali AWS non valide o mancanti."
            raise RuntimeError(error_message) from e
        except ClientError as e:
            error_message = f"Errore AWS S3: {e}"
            raise RuntimeError(error_message) from e
        except Exception as e:
            error_message = f"Errore imprevisto durante il caricamento del file: {e}"
            raise RuntimeError(error_message) from e

    def upload_file(self, source_file_path, dest_file_path):
        """Carica un file su Spaces."""
        key = f"{dest_file_path}"
        try:
            self.s3.upload_file(
                source_file_path,
                self.bucket_name,
                key,
                ExtraArgs={"ACL": "private"}
            )
            return key
        except FileNotFoundError:
            error_message = f"Errore: Il file '{source_file_path}' non esiste."
            raise RuntimeError(error_message)
        except NoCredentialsError:
            error_message = "Errore: Credenziali AWS non trovate o non valide."
            raise RuntimeError(error_message)
        except ClientError as e:
            error_message = f"Errore AWS S3: {e}"
            raise RuntimeError(error_message) from e
        except Exception as e:
            error_message = f"Errore imprevisto durante il caricamento di '{source_file_path}': {e}"
            raise RuntimeError(error_message) from e

    def download_file(self, download_path):
        """Scarica un file da Spaces."""
        if self.file_exists(download_path):
            try:
                response = self.s3.get_object(
                    Bucket=self.bucket_name, Key=download_path)
                file_data = response['Body'].read()
                return file_data
            except NoCredentialsError:
                print("Errore: Credenziali non valide.")
            except Exception as e:
                print(f"Errore nel download del file: {e}")
        else:
            return None

    def list_files_matching_pattern(self, folder: str, pattern: str):
        """Lista i file in una cartella di Spaces che rispettano un pattern."""
        try:
            response = self.s3.list_objects_v2(
                Bucket=self.bucket_name, Prefix=folder)
            if 'Contents' not in response:
                return []
            matching_files = [
                obj['Key']
                for obj in response['Contents']
                if re.match(pattern, obj['Key'].split('/')[-1])
            ]
            return matching_files
        except Exception as e:
            error_message = f"Errore durante il recupero dei file: {e}"
            raise RuntimeError(error_message) from e

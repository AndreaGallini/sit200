import boto3
import os
from dotenv import load_dotenv
import requests
from io import BytesIO
from botocore.exceptions import ClientError
load_dotenv()

USER_FOLDER = 'media/user_files'
s3 = boto3.client(
    's3',
    endpoint_url=os.getenv('AWS_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
)


def upload_to_spaces(dest_file_path, source_file_path):
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    key = f"{dest_file_path}"  # Percorso dinamico
    s3.upload_file(
        source_file_path,
        bucket_name,
        key,
        ExtraArgs={"ACL": "private"}
    )

    return key  # Ritorna solo il percorso del file nel bucket


def create_folder(folder_name):
    """
    Create a folder in S3 bucket

    Args:
        folder_name (str): Name of the folder to create

    Returns:
        str: Key of the created folder
    """
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    key = folder_name
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
    )
    return key


def upload_project_image(image_path, image_name, project_path):
    """
    Upload an image file to the project's images folder in S3 bucket

    Args:
        image_path (str): Local path of image file to upload
        project_code (str): Project code/folder name
        image_name (str): Name to give image in S3

    Returns:
        str: S3 key (path) where image was uploaded
    """
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    key = f"{project_path}/{image_name}"

    # Validate file is an image
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    if not any(image_name.lower().endswith(ext) for ext in valid_extensions):
        raise ValueError("File must be an image (jpg, jpeg, png, gif, or bmp)")

    s3.upload_file(
        image_path,
        bucket_name,
        key,
        ExtraArgs={
            "ACL": "private",
            "ContentType": "image/jpeg"  # Set appropriate content type for images
        }
    )

    return key


def get_image_url(key, exp_time=360000):
    """
    Get a presigned URL for accessing a private image in DigitalOcean Spaces bucket
    """
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    try:
        # Rimuovi qualsiasi riferimento al bucket_name e pulisci il path
        clean_key = (
            key.lstrip('/')
            .replace(f'{bucket_name}/', '', 1)
            .replace(f'{bucket_name}', '', 1)
            .replace('//', '/')  # Rimuove eventuali double slashes
        ).strip('/')
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': clean_key
            },
            ExpiresIn=exp_time
        )
        return url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None


def get_image_from_presigned_url(presigned_url):
    """
    Get an image from a presigned URL.
    """
    response = requests.get(presigned_url)
    if response.status_code == 200:
        return response.content
    else:
        return None


def get_image_from_path(path):
    """
    Get an image from a path.
    """
    try:
        response = s3.get_object(Bucket=os.getenv(
            'AWS_STORAGE_BUCKET_NAME'), Key=path)
        image_data = BytesIO(response['Body'].read())
        return image_data
    except ClientError as e:
        # Gestisci errori di client (es. file non trovato)
        if e.response['Error']['Code'] == 'NoSuchKey':
            print(
                f"File '{path}' non trovato nel bucket '{os.getenv('AWS_STORAGE_BUCKET_NAME')}'.")
        else:
            # Gestisci altri errori generici
            print(f"Errore durante il recupero del file: {e}")
        return None
    except Exception as e:
        print(f"Error getting image from path: {e}")
        return None


def file_exists_in_spaces(file_path):
    """
    Verifica se un file esiste su DigitalOcean Spaces.
    """
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

    try:
        s3.head_object(Bucket=bucket_name, Key=file_path)
        return True
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise  # Altro errore (es. permessi negati)

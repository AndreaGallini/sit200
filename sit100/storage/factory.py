import os

from storage.base import StorageService
from storage.do_spaces import SpacesStorageService
from storage.locale_storage import LocalStorageService


class StorageFactory:
    """Factory per scegliere il tipo di storage."""

    _instance = None  # Singleton storage instance

    @staticmethod
    def get_storage_service() -> StorageService:
        if StorageFactory._instance is None:
            storage_type = os.getenv('STORAGE_TYPE', 'spaces').lower()

            if storage_type == 'spaces':
                StorageFactory._instance = SpacesStorageService()
            elif storage_type == 'local':
                StorageFactory._instance = LocalStorageService()
            else:
                raise ValueError(
                    f"STORAGE_TYPE '{storage_type}' non valido. Usa 'spaces' o 'local'.")

        return StorageFactory._instance

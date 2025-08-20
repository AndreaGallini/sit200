"""
datasheet.py
Classe che gestisce la costruzione delle stringhe xml relative ai datasheet
delle componenti del generatore fotovoltaico.
"""
import os
import re
import logging

from storage.factory import StorageFactory
from .common import Common

logger = logging.getLogger('django')


class Datasheet:

    def __init__(self, data):
        self.data = data
        self.storage = StorageFactory.get_storage_service()

    def get_datasheet(self, component_id):
        """Restituisce la lista dei path delle immagini dei datasheet del componente."""

        # datasheet_path = self.data.get('datasheet_complete_path')
        # if not datasheet_path:
        #    logger.warning(
        #        f"Percorso datasheet non trovato per il componente {component_id}.")
        #    return []

        datasheet_path = 'datasheets'

        # Debug: log del component_id e del pattern
        # Gestione del component_id che può essere una lista o una stringa
        if isinstance(component_id, list):
            if len(component_id) == 0:
                return []

            # Se è una lista con più elementi, prendiamo tutti i datasheet di tutti i componenti
            all_matching_files = []

            for comp_id in component_id:
                actual_component_id = str(comp_id)

                escaped_component_id = re.escape(actual_component_id)
                pattern = rf"^{escaped_component_id}_datasheet_\d+\.png$"
                datasheet_path_with_slash = f"{datasheet_path}/"
                try:
                    matching_files = self.storage.list_files_matching_pattern(
                        datasheet_path_with_slash, pattern)

                    all_matching_files.extend(matching_files)
                except RuntimeError as e:
                    logger.error(
                        f"Errore nel cercare i datasheet per {actual_component_id}: {e}")

            # Ordina i file per mantenere l'ordine dei componenti nella lista
            sorted_files = []
            for comp_id in component_id:
                comp_id_str = str(comp_id)
                for file_path in all_matching_files:
                    if file_path.startswith(f"{datasheet_path}/{comp_id_str}_datasheet_"):
                        sorted_files.append(file_path)
            return sorted_files
        else:
            actual_component_id = str(component_id)

        # Escape dei caratteri speciali regex nel component_id per evitare errori di parsing
        escaped_component_id = re.escape(actual_component_id)
        pattern = rf"^{escaped_component_id}_datasheet_\d+\.png$"

        datasheet_path = f"{datasheet_path}/"
        try:
            matching_files = self.storage.list_files_matching_pattern(datasheet_path, pattern)
            return matching_files
        except RuntimeError as e:
            logger.error(f"Errore nel cercare i datasheet nello storage: {e}")
            return []

    def create_image_photovoltaic_module(self):
        """X120: Crea il paragrafo con le immagini delle schede tecniche dei pannelli fotovoltaici."""

        module_id = self.data.get('component_ids', {}).get('module', None)
        datasheet_paths = self.get_datasheet(module_id)

        result = Common.create_images_paragraph(
            datasheet_paths, width_cm=16, alignment="center")

        return result

    def create_image_for_datasheet(self, component_id):
        """Crea il paragrafo con le immagini delle schede tecniche dei componenti."""

        datasheet_paths = self.get_datasheet(component_id)
        return Common.create_images_paragraph(datasheet_paths, width_cm=16, alignment="center")

    def create_image_support_structure(self):
        """X121: Crea il paragrafo con le immagini delle schede tecniche delle strutture di supporto."""

        support_id = self.data.get('component_ids', {}).get('support', None)
        datasheet_paths = self.get_datasheet(support_id)
        return Common.create_images_paragraph(datasheet_paths, width_cm=16, alignment="center")

    def create_image_inverter(self):
        """X122: Crea il paragrafo con le immagini delle schede tecniche dell'inverter."""

        inverter_id = self.data.get('component_ids', {}).get('inverter', None)
        datasheet_paths = self.get_datasheet(inverter_id)
        return Common.create_images_paragraph(datasheet_paths, width_cm=16, alignment="center")

    def create_image_storage(self):
        """X123: Crea il paragrafo con le immagini delle schede tecniche delle batterie di accumulo."""

        storage_id = self.data.get('component_ids', {}).get('storage', None)
        datasheet_paths = self.get_datasheet(storage_id)
        return Common.create_images_paragraph(datasheet_paths, width_cm=16, alignment="center")

    def create_image_cables(self):
        """X124: Crea il paragrafo con le immagini delle schede tecniche dei cavi."""

        cables_id = self.data.get('component_ids', {}).get('cables', None)
        datasheet_paths = self.get_datasheet(cables_id)
        return Common.create_images_paragraph(datasheet_paths, width_cm=16, alignment="center")

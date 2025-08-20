"""
user_input_processor.py
Classe che processa gli input dell'input utente e li prepara per i modelli o per il testo.
"""
import os
import logging

from PIL import Image, ImageOps, UnidentifiedImageError

import tempfile

from .params import ALBEDO, ALBEDO_MAPPING, CLINOMETRIC_CLASS, OBSTACLES_CLASS, IMAGE_NAMES
from storage.factory import StorageFactory

logger = logging.getLogger('django')


class UserInputProcessor:

    def __init__(self, data):
        self.data = data
        self.storage = StorageFactory.get_storage_service()

    @staticmethod
    def update_dictionary(dictionary, changes):
        """Aggiorna un sottodizionario con nuovi valori."""

        if isinstance(dictionary, dict):
            updated_subdict = dictionary.copy()
            updated_subdict.update(changes)
            return updated_subdict
        return dictionary

    @staticmethod
    def load_image(image):
        """Carica un'immagine (da path o BytesIO) da un percorso specificato con gestione degli errori."""

        try:
            # Se è già un oggetto PIL.Image, restituiscilo
            if hasattr(image, 'size'):
                return image

            # Se è un path string, gestisci lo storage
            if isinstance(image, str):
                storage_service = StorageFactory.get_storage_service()

                # Se è storage locale, usa il metodo originale
                if hasattr(storage_service, 'download_image'):
                    # Storage DigitalOcean Spaces
                    try:
                        # Per DigitalOcean Spaces, usa il path completo senza rimuovere 'media/'
                        # Se il path non inizia con 'media/', aggiungilo
                        if not image.startswith('media/'):
                            spaces_path = f"media/{image}"
                        else:
                            spaces_path = image

                        logger.debug(
                            f"Tentativo di caricamento immagine da Spaces: {spaces_path}")
                        image_stream = storage_service.download_image(
                            spaces_path)
                        image_obj = Image.open(image_stream)
                        logger.debug(
                            f"Immagine caricata con successo da Spaces: {spaces_path}")
                        return image_obj
                    except Exception as e:
                        logger.error(f"Errore nel caricamento da Spaces: {e}")
                        return None
                else:
                    # Storage locale
                    image_obj = Image.open(image)
                    return image_obj
            else:
                # Se è un file-like object (BytesIO, etc.)
                image_obj = Image.open(image)
                return image_obj

        except FileNotFoundError:
            logger.debug(f"Errore: File non trovato -> {image}")
            return None
        except UnidentifiedImageError:
            logger.error(
                f"Errore: Il file non è un'immagine valida -> {image}")
            return None
        except Exception as e:
            logger.error(
                f"Errore inatteso durante il caricamento dell'immagine: {e}")
            return None

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

    @staticmethod
    def resize_image(image, max_width_cm, max_height_cm):
        """Ridimensiona l'immagine da un file temporaneo e restituisce l'immagine ridimensionata."""

        # Converti i limiti da cm a pixel (1 cm ≈ 37.7953 pixel)
        max_width_px = max_width_cm * 37.7953
        max_height_px = max_height_cm * 37.7953
        try:
            with Image.open(image) as img:
                original_width, original_height = img.size
                width_ratio = max_width_px / original_width
                height_ratio = max_height_px / original_height
                scale_ratio = min(width_ratio, height_ratio)
                new_width_px = int(original_width * scale_ratio)
                new_height_px = int(original_height * scale_ratio)
                return img.resize((new_width_px, new_height_px), Image.Resampling.LANCZOS)
        except Exception as e:
            logger.error(f"Errore nel ridimensionamento dell'immagine: {e}")
            raise

    def generate_resized_filename(self, path, prefix="ok_"):
        """Genera il nome del file ridimensionato partendo dal percorso dell'immagine."""

        filename = os.path.basename(path).split('?')[0]
        resized_filename = f"{prefix}{filename}"
        project_path = self.data['project_complete_path']
        return f"{project_path}/{resized_filename}"

    def cover_logos_preparation(self):
        """
        Restituisce una lista dei nuovi path delle immagini caricate in cover_logo_1, cover_logo_2, cover_logo_3,
        solo se il file esiste nel percorso specificato e ridimensionate opportunamente.
        """

        images_path = self.data.get("general_data", {})
        logo_fields = ["cover_logo_1", "cover_logo_2", "cover_logo_3"]
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        resized_logos = []

        for field in logo_fields:
            logo_path = images_path.get(field)
            if logo_path and any(logo_path.lower().endswith(ext) for ext in valid_extensions):
                # se esiste il file nello storage
                if self.storage.file_exists(logo_path):
                    try:
                        # scarica l'immagine dallo storage come file-like object in memoria
                        image_data = self.storage.download_image(logo_path)
                        # ridimensiona l'immagine (restituisce un oggetto pillow)
                        resized_image = self.resize_image(
                            image_data, max_width_cm=2, max_height_cm=2)
                        # salva l'immagine ridimensionata in un file temporaneo
                        resized_temp_file_path = self.save_obj_image_to_tempfile(
                            resized_image)
                        # nuovo nome
                        new_image_key = self.generate_resized_filename(
                            logo_path, prefix="ok_logo_")
                        # carica l'immagine ridimensionata sullo storage
                        self.storage.upload_image(
                            resized_temp_file_path, new_image_key)
                        # rimuove file temporanei
                        os.remove(resized_temp_file_path)
                        # carica il nuovo nome dell'immagine
                        resized_logos.append(new_image_key)
                    except RuntimeError as e:
                        logger.error(f"Errore nei loghi con lo storage: {e}")
                    except Exception as e:
                        logger.error(f"Errore nel processo di gestione dell'immagine dei loghi: {e}")
        return resized_logos

    def cover_image_preparation(self):
        """Restituisce il path dell'immagine di copertina, se esiste, e ridimensionata opportunamente."""

        images_path = self.data.get("general_data", {})
        cover_image_path = images_path.get("cover_image")
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        if cover_image_path and any(cover_image_path.lower().endswith(ext) for ext in valid_extensions):
            # se esiste il file nello storage
            if self.storage.file_exists(cover_image_path):
                try:
                    # scarica l'immagine dallo storage come file-like object in memoria
                    image_data = self.storage.download_image(cover_image_path)
                    # ridimensiona l'immagine (restituisce un oggetto pillow)
                    resized_image = self.resize_image(
                        image_data, max_width_cm=16, max_height_cm=4)
                    # salva l'immagine ridimensionata in un file temporaneo
                    resized_temp_file_path = self.save_obj_image_to_tempfile(
                        resized_image)
                    # nuovo nome completo di path
                    new_image_key = self.generate_resized_filename(cover_image_path, prefix="ok_")
                    # carica l'immagine ridimensionata sullo storage
                    self.storage.upload_image(
                        resized_temp_file_path, new_image_key)
                    # rimuove file temporanei
                    os.remove(resized_temp_file_path)
                    return new_image_key
                except RuntimeError as e:
                    logger.error(f"Errore nell'immagine di copertina con lo storage: {e}")
                except Exception as e:
                    logger.error(f"Errore nel processo di gestione dell'immagine di copertina: {e}")
        return ""

    def map_images_preparation(self):
        """Prende dalla cartella le immagini delle mappe e restituisce il path."""

        project_path = self.data['project_complete_path']
        map_1 = map_2 = map_3 = ""

        # MAPPA 1: fusione di mappa_zoom_5 e mappa_zoom_5
        image_A = f"{project_path}/mappa_zoom_5.png"
        image_B = f"{project_path}/mappa_zoom_9.png"
        path_map_1 = f"{project_path}/{IMAGE_NAMES['map_1']}"
        
        image_a = self.load_image(image_A)
        image_b = self.load_image(image_B)

        if image_a and image_b:
            merged_image = self.create_location_map(
                image_a, image_b, output_width_cm=16, dpi=300)
            success = self.save_image(merged_image, path_map_1, dpi=300)
            map_1 = path_map_1 if success else ""

        # MAPPA 2: mappa con cerchio
        image_C = f"{project_path}/mappa_zoom_15.png"
        path_map_2 = f"{project_path}/{IMAGE_NAMES['map_2']}"

        image_c = self.load_image(image_C)
        if image_c:
            image = self.map_accessibility(
                image_c, output_width_cm=16, dpi=300)
            success = self.save_image(image, path_map_2, dpi=300)
            map_2 = path_map_2 if success else ""

        # MAPPA 3: mappe dei sottocampi separate (non più combinate)
        subfield_images = {}
        generator = self.data.get('generator', {})

        logger.debug(f"=== DEBUG MAPPA 3 - SOTTOCAMPI SEPARATI ===")
        logger.debug(f"Project path: {project_path}")
        logger.debug(f"Generator keys: {list(generator.keys()) if generator else 'None'}")

        # Debug: lista tutte le immagini disponibili
        available_images = self.list_available_map_images(project_path)
        logger.debug(f"Immagini disponibili trovate: {available_images}")

        # Cerca tutte le immagini dei sottocampi disponibili
        available_subfield_images = []
        for img_name in available_images:
            if img_name.startswith('mappa_zoom_20_campo_') and img_name.endswith('.png'):
                # Estrai il nome del sottocampo (es. 'A1' da 'mappa_zoom_20_campo_A1.png')
                subfield_name = img_name.replace(
                    'mappa_zoom_20_campo_', '').replace('.png', '')
                available_subfield_images.append(subfield_name)

        logger.debug(f"Sottocampi disponibili dalle immagini: {available_subfield_images}")

        # Processa ogni sottocampo individualmente
        for subfield_name in sorted(available_subfield_images):
            subfield_image_path = f"{project_path}/mappa_zoom_20_campo_{subfield_name}.png"
            logger.debug(f"Caricamento sottocampo {subfield_name}: {subfield_image_path}")

            subfield_image = self.load_image(subfield_image_path)
            if subfield_image:
                logger.debug(f"Immagine {subfield_name} caricata con successo, dimensioni: {subfield_image.size}")
                processed_image = self.map_positioning(
                    subfield_image, output_width_cm=16, dpi=300)

                # Salva l'immagine processata con un nome specifico per il sottocampo
                processed_image_path = f"{project_path}/map_subfield_{subfield_name}.png"
                success = self.save_image(processed_image, processed_image_path, dpi=300)

                if success:
                    subfield_images[subfield_name] = processed_image_path
                    logger.debug(f"Immagine {subfield_name} processata e salvata in: {processed_image_path}")
                else:
                    logger.error(f"Errore nel salvataggio dell'immagine processata per {subfield_name}")
            else:
                logger.error(f"Errore nel caricamento dell'immagine {subfield_name}")

        # Se non ci sono immagini dei sottocampi, prova il fallback con generator
        if not subfield_images and generator:
            logger.debug("Nessuna immagine sottocampo trovata, tentativo con generator")

            # Usa i sottocampi definiti nel generator
            logger.debug("Usando sottocampi dal generator")
            for field_name, field_data in generator.items():  # "A", "B"
                for subfield_name, subfield_data in field_data.items():  # "A1", "A2", "B1", "B2"
                    subfield_image_path = f"{project_path}/mappa_zoom_20_campo_{subfield_name}.png"
                    logger.debug(f"Tentativo caricamento: {subfield_image_path}")
                    
                    # Verifica se l'immagine esiste
                    exists = self.check_image_exists_on_spaces(subfield_image_path)
                    logger.debug(f"Immagine {subfield_name} esiste: {exists}")

                    if exists:
                        subfield_image = self.load_image(subfield_image_path)
                        if subfield_image:
                            logger.debug(f"Immagine {subfield_name} caricata con successo sizes: {subfield_image.size}")
                            processed_image = self.map_positioning(subfield_image, output_width_cm=16, dpi=300)

                            # Salva l'immagine processata con un nome specifico per il sottocampo
                            processed_image_path = f"{project_path}/map_subfield_{subfield_name}.png"
                            success = self.save_image(processed_image, processed_image_path, dpi=300)

                            if success:
                                subfield_images[subfield_name] = processed_image_path
                                logger.debug(f"Immagine {subfield_name} processata e salvata in {processed_image_path}")

        # Se ancora non ci sono immagini, prova il fallback con i campi standard
        if not subfield_images:
            logger.debug("Usando fallback con campi standard A, B, C, D")
            for campo in ['A', 'B', 'C', 'D']:
                campo_image_path = f"{project_path}/mappa_zoom_20_campo_{campo}.png"
                logger.debug(f"Tentativo caricamento fallback: {campo_image_path}")

                # Verifica se l'immagine esiste
                exists = self.check_image_exists_on_spaces(campo_image_path)
                logger.debug(f"Immagine {campo} esiste: {exists}")

                if exists:
                    campo_image = self.load_image(campo_image_path)
                    if campo_image:
                        logger.debug(f"Immagine {campo} caricata con successo, dimensioni: {campo_image.size}")
                        processed_image = self.map_positioning(campo_image, output_width_cm=16, dpi=300)

                        # Salva l'immagine processata con un nome specifico per il campo
                        processed_image_path = f"{project_path}/map_subfield_{campo}.png"
                        success = self.save_image(processed_image, processed_image_path, dpi=300)

                        if success:
                            subfield_images[campo] = processed_image_path
                            logger.debug(f"Immagine {campo} processata e salvata in: {processed_image_path}")
                        else:
                            logger.error(f"Errore nel salvataggio dell'immagine processata per {campo}")
                    else:
                        logger.error(f"Errore nel caricamento dell'immagine {campo}")
                else:
                    logger.warning(f"Immagine {campo} non trovata")

        logger.debug(f"Numero totale di immagini sottocampi processate: {len(subfield_images)}")
        logger.debug(f"Sottocampi processati: {list(subfield_images.keys())}")

        # Restituisce il dizionario delle immagini dei sottocampi invece di un'unica immagine combinata
        map_3 = subfield_images

        return [map_1, map_2, map_3]

    @staticmethod
    def create_location_map(image_a, image_b, output_width_cm, dpi=300):
        """Sovrappone una seconda immagine a una prima immagine a larghezza definita: in alto dx."""

        try:
            # Calcola larghezza finale in pixel
            output_width_px = int(output_width_cm * dpi / 2.54)
            # Immagine A
            original_width, original_height = image_a.size
            image_a = image_a.crop((550, 220, original_width - 400, original_height - 200))
            width_a, height_a = image_a.size
            # Calcola altezza proporzionale
            scale_factor = output_width_px / width_a
            new_width = output_width_px
            new_height = int(height_a * scale_factor)
            # Ridimensiona immagine A mantenendo proporzioni
            image_a = image_a.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Immagine B
            width_b, height_b = image_b.size
            image_b = image_b.crop((200, 150, width_b - 200, height_b - 150))
            image_b_resized = image_b.resize((int(6 * dpi / 2.54), int(4.51 * dpi / 2.54)), Image.Resampling.LANCZOS)
            image_b_with_border = ImageOps.expand(image_b_resized, border=3, fill="white")
            # Posizione in alto a destra (assicurati che l'immagine A sia abbastanza alta)
            position = (new_width - image_b_with_border.width - 2, 2)
            image_a.paste(image_b_with_border, position, mask=None)
            return image_a
        except Exception as e:
            logger.error(f"Errore durante l'elaborazione delle immagini: {e}")
            raise RuntimeError(
                "Errore durante l'elaborazione delle immagini") from e

    @staticmethod
    def save_image(image, save_path, dpi=300):
        """
        Salva un'immagine in un percorso specificato a 300 dpi.
        Gestisce sia lo storage locale che DigitalOcean Spaces.
        """
        try:
            storage_service = StorageFactory.get_storage_service()

            if hasattr(storage_service, 'upload_image'):
                # Storage DigitalOcean Spaces
                try:
                    # Assicurati che la directory /tmp esista
                    os.makedirs('/tmp', exist_ok=True)

                    # Salva temporaneamente l'immagine in locale
                    temp_path = f"/tmp/{os.path.basename(save_path)}"
                    logger.debug(f"Salvando temporaneamente in: {temp_path}")
                    image.save(temp_path, dpi=(dpi, dpi))

                    # Verifica che il file temporaneo sia stato creato
                    if not os.path.exists(temp_path):
                        logger.error(f"File temporaneo non creato: {temp_path}")
                        return False

                    # Per DigitalOcean Spaces, usa il path completo senza rimuovere 'media/'
                    # Se il path non inizia con 'media/', aggiungilo
                    if not save_path.startswith('media/'):
                        spaces_path = f"media/{save_path}"
                    else:
                        spaces_path = save_path

                    logger.debug(
                        f"Tentativo di salvataggio immagine su Spaces: {spaces_path}")
                    # Carica su Spaces
                    storage_service.upload_image(temp_path, spaces_path)

                    # Rimuovi il file temporaneo
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

                    # Verifica che l'immagine sia stata effettivamente salvata
                    if hasattr(storage_service, 'file_exists') and storage_service.file_exists(spaces_path):
                        logger.debug(
                            f"Immagine salvata con successo su Spaces: {spaces_path}")
                        return True
                    else:
                        logger.warning(
                            f"Immagine potrebbe non essere stata salvata correttamente: {spaces_path}")
                        return True  # Ritorna True comunque perché l'upload potrebbe essere asincrono
                except Exception as e:
                    logger.error(f"Errore nel salvataggio su Spaces: {e}")
                    # Pulisci il file temporaneo in caso di errore
                    temp_path = f"/tmp/{os.path.basename(save_path)}"
                    if os.path.exists(temp_path):
                        try:
                            os.remove(temp_path)
                        except:
                            pass
                    return False
            else:
                # Storage locale
                directory = os.path.dirname(save_path)
                if not os.path.isdir(directory):
                    logger.error(
                        f"La directory di salvataggio non esiste: {directory}")
                    return False
                image.save(save_path, dpi=(dpi, dpi))
                return True

        except FileNotFoundError as e:
            logger.debug(f"Errore: {e}")
            return False
        except PermissionError:
            logger.error(
                f"Errore: Permessi insufficienti per salvare il file -> {save_path}")
            return False
        except Exception as e:
            logger.error(f"Errore inatteso durante il salvataggio: {e}")
            return False

    @staticmethod
    def map_accessibility(image_a, output_width_cm, dpi=300):
        """Prepara l'immagine dell'accessibilità a larghezza definita."""

        # Calcola larghezza finale in pixel
        output_width_px = int(output_width_cm * dpi / 2.54)

        # Immagine A
        original_width, original_height = image_a.size
        image_a = image_a.crop(
            (500, 300, original_width - 500, original_height - 300))
        width_a, height_a = image_a.size

        # Calcola altezza proporzionale
        scale_factor = output_width_px / width_a
        new_width = output_width_px
        new_height = int(height_a * scale_factor)

        # Ridimensiona immagine A mantenendo proporzioni
        image_a = image_a.resize(
            (new_width, new_height), Image.Resampling.LANCZOS)

        return image_a

    @staticmethod
    def map_positioning(image_a, output_width_cm, dpi=300):
        """Prepara l'immagine del posizionamento a larghezza definita."""

        # Calcola larghezza finale in pixel
        output_width_px = int(output_width_cm * dpi / 2.54)

        # Immagine A
        # original_width, original_height = image_a.size
        # image_a = image_a.crop((500, 500, original_width - 500, original_height - 500))
        width_a, height_a = image_a.size

        # Calcola altezza proporzionale
        scale_factor = output_width_px / width_a
        new_width = output_width_px
        new_height = int(height_a * scale_factor)

        # Ridimensiona immagine A mantenendo proporzioni
        image_a = image_a.resize(
            (new_width, new_height), Image.Resampling.LANCZOS)

        return image_a

    def client_data_preparation(self):
        """Compone i dati del committente."""

        client_data = self.data.get("client_data", {})
        short_client = ""
        long_client = ""
        if client_data:
            short_client = client_data.get('client_name', '')
            additional_info = client_data.get('client_additional_info', '')
            if additional_info:
                clenead_text = additional_info.replace("\n\n", "\n")
                long_client = f"{short_client}\n{clenead_text}"
            else:
                long_client = short_client
        return short_client, long_client

    def proposer_data_preparation(self):
        """Compone i dati del proponente."""

        proposer_data = self.data.get("proposer_data", {})
        short_proposer = ""
        long_proposer = ""
        if proposer_data:
            short_proposer = proposer_data.get('proposer_name', '')
            additional_info = proposer_data.get('proposer_additional_info', '')
            if additional_info:
                clenead_text = additional_info.replace("\n\n", "\n")
                long_proposer = f"{short_proposer}\n{clenead_text}"
            else:
                long_proposer = short_proposer
        return short_proposer, long_proposer

    def collaborators_data_preparation(self):
        """Compone i dati dei collaboratori."""

        collaborators = self.data.get("collaborators_data", [])
        collaborators_list = [item.get("name", "") for item in collaborators]
        collaborators_names = "\n".join(collaborators_list) if collaborators_list else ""

        return collaborators_list, collaborators_names

    def designers_data_preparation(self):
        """Compone i dati dei progettisti."""

        designers = self.data.get("designers_data", [])

        designer_logos = [designer.get(
            "designer_logo", "") for designer in designers if designer.get("designer_logo")]
        person_list = [designer.get('designer_name', '')
                       for designer in designers if designer.get('designer_name')]
        designers_names = "\n".join(person_list) if person_list else ""

        # Costruisci i dettagli dei progettisti
        designers_list = []
        for designer in designers:
            details = [
                designer.get("designer_name", ""),
                designer.get("designer_additional_info", ""),
            ]
            # Filtra i valori vuoti e aggiungili alla lista
            designers_list.append("\n".join(filter(None, details)))

        designer_details = "\n".join(designers_list)

        return designers_list, designers_names, designer_logos, designer_details

    def get_rounded_coordinates(self):
        """Restituisce le coordinate a un numero specifico di cifre decimali o una stringa vuota."""

        def round_coordinate(value):
            try:
                return round(float(value), 6)
            except (ValueError, TypeError):
                return ""

        latitude = round_coordinate(self.data.get("latitude", ""))
        longitude = round_coordinate(self.data.get("longitude", ""))

        return latitude, longitude

    @staticmethod
    def get_class_for_value(value, limits):
        """Restituisce l'indice del range in cui il valore rientra."""

        for i, limit in enumerate(limits):
            if value <= limit:
                return i + 1
        return len(limits) + 1

    def get_shadow_classes(self):
        """Restituisce la classe di appartenenza dell'ombreggiamento per ogni sottocampo"""

        # Ombreggiamento clinometrico (valore globale)
        clinometric_value = self.data.get("shading_horizon", 0)
        clinometric_str = f"{clinometric_value}%"
        clinometric_limits = [5, 10, 20]
        posit = str(self.get_class_for_value(
            clinometric_value, clinometric_limits))
        clinometric_class = CLINOMETRIC_CLASS[posit]
        clino = {
            "value": float(clinometric_value),
            "value_str": clinometric_str,
            "class": clinometric_class
        }

        # Ombreggiamento ostacoli per ogni sottocampo
        generator = self.data.get('generator', {})
        subfield_shadows = {}

        if generator:
            for field_name, field_data in generator.items():  # "A", "B"
                for subfield_name, subfield_data in field_data.items():  # "A1", "A2", "B1", "B2"
                    obstacles_value = subfield_data.get("shading_obstacles", 0)
                    obstacles_str = f"{obstacles_value}%"
                    obstacles_limits = [5, 15, 25]
                    posit = str(self.get_class_for_value(
                        obstacles_value, obstacles_limits))
                    obstacles_class = OBSTACLES_CLASS[posit]

                    subfield_shadows[subfield_name] = {
                        "shado_value": float(obstacles_value),
                        "shado_value_str": obstacles_str,
                        "shado_class": obstacles_class
                    }

        return clino, subfield_shadows

    def get_total_area(self):
        generator = self.data.get('generator', {})
        if not generator:
            return ""

        # Calcola l'area totale di tutti i sottocampi
        total_area = 0.0
        subfield_areas = {}

        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data in field_data.items():  # "A1", "A2", "B1", "B2"
                area = float(subfield_data.get('area', 0.0))
                subfield_areas[subfield_name] = area
                total_area += area

        if total_area == 0:
            return ""

        return round(total_area, 2)

    def build_fields_info(self):
        generator = self.data.get('generator', {})
        if not generator:
            return '', '', ''

        n_fields = len(generator)
        if n_fields == 1:
            n_fields_str = f"n. 1 area di installazione"
        else:
            n_fields_str = f"n. {n_fields} aree di installazione"

        subfields_str = ""
        for field, subfield in generator.items():
            subfields_str += f"Campo {field} - {len(subfield)} sottocampi:\n"
            for key, details in subfield.items():
                subfields_str += f"- {key}: {details['name']}\n"

        return n_fields, n_fields_str, subfields_str

    def process_input_data(self):
        """Processamento degli input dati da utente."""

        changes = {}

        # -------------------------------------------- # path delle cartelle e dei file

        # Path alla cartella del progetto: completo
        project_path = self.data.get('project_dir', {}).get('path', None)
        if not project_path:
            logger.error("Path alla cartella del progetto non trovato (def user_input_data)")
            return False

        self.data['project_complete_path'] = project_path

        # Path alla cartella dei datasheets
        self.data['datasheet_complete_path'] = 'datasheets'

        # Path alla cartella dei layouts
        self.data['layout_complete_path'] = 'layouts'

        # Path di destinazione del word e pdf
        project_code = self.data.get('project_code')
        if not project_code:
            logger.error("Non c'è il project_code")
            return False

        word_name = f"Report_{project_code}.docx"
        pdf_name = f"Report_{project_code}.pdf"
        design_name = f"Design_{project_code}.docx"

        self.data['word_project_path'] = f"{project_path}/{word_name}"
        self.data['pdf_project_path'] = f"{project_path}/{pdf_name}"
        self.data['word_design_path'] = f"{project_path}/{design_name}"
        self.data['word_dir_and_file'] = f"{project_code}/{word_name}"
        self.data['pdf_dir_and_file'] = f"{project_code}/{pdf_name}"
        self.data['word_design_dir_and_file'] = f"{project_code}/{design_name}"

        # Path al grafico di cashflow
        self.data['path_cashflow_storage'] = f"{project_path}/cashflow_with_storage.png"
        self.data['path_cashflow_nostorage'] = f"{project_path}/cashflow_without_storage.png"

        # -------------------------------------------- # Immagini: mappe di progetto

        # Immagini: loghi di copertina (da 0 a 3)
        changes['cover_logos'] = self.cover_logos_preparation()

        # Immagini: immagine di copertina
        changes['cover_image'] = self.cover_image_preparation()

        # Immagini:Loghi dei progettisti                        # TODO

        # Immagini:immagini della mappa
        changes['map_images'] = self.map_images_preparation()

        # --------------------------------------------  # Coordinate con u.m.

        lat, lng = self.get_rounded_coordinates()
        changes['latitude_str'] = f"{lat}°"
        changes['longitude_str'] = f"{lng}°"
        changes['altitude_str'] = f"{self.data.get('altitude', '')} m" if self.data.get('altitude') else ""

        changes['latitude_float'] = float(lat)
        changes['longitude_float'] = float(lng)

        changes['latitude_ext'] = f"Latitudine: {lat} WGS84 in gradi decimali [°]"
        changes['longitude_ext'] = f"Longitudine: {lng} WGS84 in gradi decimali [°]"

        # -------------------------------------------- Componenti

        changes['component_ids'] = {
            'module': [],
            'inverter': [],
            'storage': [],
            'support': [],
        }

        # -------------------------------------------- Input di progetto

        generator = self.data.get('generator', '')
        if generator:
            for field_name, field_data in generator.items():  # "A", "B"
                for subfield_name, subfield_data in field_data.items():  # "A1", "A2", "B1", "B2"
                    # Estrai inclinazione e azimuth per ogni sottocampo
                    inclination = subfield_data.get('inclination', 0)
                    azimuth = subfield_data.get('azimuth', 0)
                    # Se devi salvare questi valori per ogni sottocampo
                    changes[f'{subfield_name}_tilt_ext'] = f"Inclinazione pannelli {subfield_name}: {inclination}°"
                    changes[f'{subfield_name}_azimuth_ext'] = f"Orientamento {subfield_name}: {azimuth}°"

        albedo = self.data.get('albedo', '')
        changes['albedo_ext'] = f"Riflettanza del terreno: {ALBEDO[albedo]} ({ALBEDO_MAPPING[albedo]})"
        changes['albedo_str'] = f"{ALBEDO[albedo]} ({ALBEDO_MAPPING[albedo]})"
        changes['albedo_float'] = float(ALBEDO_MAPPING[albedo])

        # -------------------------------------------- Area ed eventuale potenza

        changes['total_area'] = self.get_total_area()
        changes['total_area_str'] = f"{changes['total_area']} mq"

        # -------------------------------------------- Aree e campi

        n_fields, n_fields_str, subfields_str = self.build_fields_info()

        changes['n_fields'] = n_fields
        changes['n_fields_str'] = n_fields_str
        changes['subfields_str'] = subfields_str

        # -------------------------------------------- Titolo esteso del progetto

        project_title = self.data.get("general_data", {}).get("project_title", "")
        project_acronym = self.data.get("general_data", {}).get("project_acronym", "")
        if project_acronym:
            changes['project_full_title'] = project_title + " '" + project_acronym + "'"
        else:
            changes['project_full_title'] = project_title

        # -------------------------------------------- Team di progetto

        short_client, long_client = self.client_data_preparation()
        short_proposer, long_proposer = self.proposer_data_preparation()
        changes['short_client'] = short_client
        changes['long_client'] = long_client

        changes['short_proposer'] = short_proposer
        changes['long_proposer'] = long_proposer

        designers_list, designers_names, designers_logos, designers_details = self.designers_data_preparation()
        changes['designers_list'] = designers_list
        changes['designers_names'] = designers_names
        changes['designers_logos'] = designers_logos
        changes['designers_details'] = designers_details

        collaborators_list, collaborators_names = self.collaborators_data_preparation()
        changes['collaborators_list'] = collaborators_list
        changes['collaborators_names'] = collaborators_names

        # -------------------------------------------- Posizione

        address = self.data.get("general_data", {}).get("address", "")
        municipality = self.data.get("general_data", {}).get("municipality", "")
        province = self.data.get("general_data", {}).get("province", "")
        region = self.data.get("general_data", {}).get("region", "")
        location = f"Italia nel comune di {municipality}, provincia di {province}, nella regione {region} in {address}"
        address = f"{address}, {municipality} - {province}"
        changes['plant_location'] = location
        changes['plant_address'] = address

        # -------------------------------------------- Ombreggiamento
        clino, subfield_shadows = self.get_shadow_classes()
        changes['clinometry'] = clino

        # Aggiungi le shadow classes per ogni sottocampo
        for subfield_name, shadow_data in subfield_shadows.items():
            changes[f'{subfield_name}_shadows'] = shadow_data

        # Mantieni anche un valore di default per compatibilità (usa il primo sottocampo)
        if subfield_shadows:
            first_shadow = list(subfield_shadows.values())[0]
            changes['shadows'] = first_shadow

        # Step finale: aggiornare general data con i cambiamenti apportati
        return self.update_dictionary(self.data, changes)

    # -------------------------------------- funzioni di validazione

    def check_image_exists_on_spaces(self, image_path):
        """
        Verifica se un'immagine esiste su DigitalOcean Spaces utilizzando head_object.
        """
        try:
            storage_service = StorageFactory.get_storage_service()

            if hasattr(storage_service, 'file_exists'):
                # Per DigitalOcean Spaces, usa il path completo senza rimuovere 'media/'
                # Se il path non inizia con 'media/', aggiungilo
                if not image_path.startswith('media/'):
                    spaces_path = f"media/{image_path}"
                else:
                    spaces_path = image_path

                logger.debug(f"Verifica esistenza immagine su Spaces: {spaces_path}")
                # Usa file_exists che fa head_object invece di scaricare l'intera immagine
                exists = storage_service.file_exists(spaces_path)
                logger.debug(f"Risultato verifica esistenza: {exists}")
                return exists
            else:
                # Storage locale
                return os.path.exists(image_path)
        except Exception as e:
            logger.error(f"Errore nella verifica esistenza immagine: {e}")
            return False

    def list_all_png_images(self, project_path):
        """
        Lista tutte le immagini .png disponibili nella cartella del progetto.
        """

        available_images = []

        try:
            storage_service = StorageFactory.get_storage_service()

            if hasattr(storage_service, 'list_files'):
                # Storage DigitalOcean Spaces - usa list_files per ottenere tutti i file
                try:
                    # Determina il prefisso per la cartella del progetto
                    if not project_path.startswith('media/'):
                        spaces_prefix = f"media/{project_path}"
                    else:
                        spaces_prefix = project_path

                    # Assicurati che il prefisso finisca con '/'
                    if not spaces_prefix.endswith('/'):
                        spaces_prefix += '/'

                    logger.debug(f"Cercando file con prefisso: {spaces_prefix}")

                    # Lista tutti i file nella cartella
                    all_files = storage_service.list_files(spaces_prefix)
                    logger.debug(f"File trovati: {all_files}")

                    # Filtra solo i file .png
                    for file_path in all_files:
                        filename = os.path.basename(file_path)
                        if filename.lower().endswith('.png'):
                            available_images.append(filename)

                except Exception as e:
                    logger.error(f"Errore nel listing dei file da Spaces: {e}")
                    # Fallback alla lista predefinita
                    return self.list_available_map_images_fallback(project_path)
            else:
                # Storage locale - usa os.listdir
                try:
                    if os.path.exists(project_path):
                        for filename in os.listdir(project_path):
                            if filename.lower().endswith('.png'):
                                available_images.append(filename)

                    else:
                        return []
                except Exception as e:
                    return []

        except Exception as e:
            return []
        return available_images

    def list_available_map_images_fallback(self, project_path):
        """
        Fallback per la lista delle immagini quando list_files non è disponibile.
        """

        # Lista delle immagini che potrebbero esistere
        possible_images = [
            "mappa_zoom_5.png",
            "mappa_zoom_9.png",
            "mappa_zoom_15.png",
            "mappa_zoom_20.png"
        ]

        # Aggiungi immagini per i campi
        generator = self.data.get('generator', {})
        if generator:
            for field_name in generator.keys():
                possible_images.append(f"mappa_zoom_20_campo_{field_name}.png")
        else:
            # Campi standard
            for campo in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                possible_images.append(f"mappa_zoom_20_campo_{campo}.png")

        # Aggiungi altre possibili immagini
        possible_images.extend([
            "map_location.png",
            "map_accessibility.png",
            "map_positioning.png",
            "plant_layout.png",
            "cover_image.png"
        ])

        available_images = []
        for img_name in possible_images:
            img_path = f"{project_path}/{img_name}"
            if self.check_image_exists_on_spaces(img_path):
                available_images.append(img_name)

        return available_images

    def list_available_map_images(self, project_path):
        """
        Wrapper per compatibilità - usa il nuovo metodo list_all_png_images.
        """
        return self.list_all_png_images(project_path)

"""
Modulo per il dimensionamento di impianti fotovoltaici.

Contiene la classe PlantSizer, che calcola la configurazione ottimale di un impianto FV
a partire dalla posizione, dalle aree disponibili e da eventuali requisiti di potenza o storage.

Funzionalità principali:
- Calcolo del numero di moduli FV per area disponibile
- Selezione della configurazione inverter ottimale
- Assegnazione dello storage compatibile se richiesto
- Supporto per layout con più sottocampi

Dipendenze:
- django.db.connection

"""
import copy
import logging
from django.db import connection
from storage.factory import StorageFactory
from ..keope.params import GROUND_COVERAGE_RATIO, MQ_PER_MODULE, SUPPORT, MQ_PER_MODULE_LARGE

logger = logging.getLogger('django')


class PlantSizer:

    def __init__(self, fv_position, user_subfields, user_total_power=None, fv_with_storage=False, storage_level=1):
        self.fv_position = fv_position
        self.user_subfields = user_subfields
        self.user_total_power = user_total_power
        self.fv_with_storage = fv_with_storage
        self.storage_level = storage_level
        self.n_subfields = 0
        self.total_available_area = None
        self.total_real_area = None
        self.desired_subfield_powers = None

    @staticmethod
    def execute_query(query, params=None, fetch_one=False):
        """Esegue una query SQL utilizzando il cursore di Django."""
        try:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                if query.strip().lower().startswith("select"):
                    if fetch_one:
                        columns = [col[0] for col in cursor.description]
                        row = cursor.fetchone()
                        return dict(zip(columns, row)) if row else None
                    else:
                        columns = [col[0] for col in cursor.description]
                        return [dict(zip(columns, row)) for row in cursor.fetchall()]
                return None
        except Exception as e:
            logger.info(f"Errore durante l'esecuzione della query: {e}")
            return None

    def _calculate_n_subfields(self):
        """Calcola il numero di sottocampi totali."""
        self.n_subfields = sum(
            len(subfield_dict)
            for subfield_dict in self.user_subfields.values()
        )

    def _calculate_total_available_area(self):
        """Calcola la superficie totale selezionata dall'utente (somma area di tutti i sottocampi)."""
        total_area = sum(
            subfield.get("area", 0)
            for group in self.user_subfields.values()
            for subfield in group.values()
        )
        if total_area <= 0:
            print(f"Area totale nulla o non valida - Area totale calcolata: {total_area} m²")

        self.total_available_area = round(total_area, 2)

    def _distribute_power_by_area_if_needed(self):
        """Distribuisce la potenza proporzionalmente all'area dei sottocampi."""
        if not self.user_total_power or not self.total_available_area:
            return

        distributed_power = {}
        for field_key, subfield_dict in self.user_subfields.items():
            distributed_power[field_key] = {}
            for subfield_key, data in subfield_dict.items():
                area = data.get("area", 0)
                power = self.user_total_power * area / self.total_available_area
                distributed_power[field_key][subfield_key] = {
                    "area": area,
                    "power": round(power, 2)
                }
        self.desired_subfield_powers = distributed_power

    def _calculate_real_area(self):
        gcr = GROUND_COVERAGE_RATIO.get(self.fv_position, 0.8)
        self.total_real_area = self.total_available_area * gcr

    def _estimate_provisional_modules(self):
        total_modules = int(self.total_real_area / MQ_PER_MODULE)
        return total_modules

    @staticmethod
    def _build_final_configuration(config_data):
        """Costruisce il dizionario di configurazione finale a partire da config_data, se valido."""
        if not config_data:
            logger.error(f"Attenzione: config_data è vuoto o None: {config_data}.")
            return None

        keys = [
            "n_temp_modules", "position", "n_modules", "series", "n_strings", "n_inverters",
            "module_power", "total_power", "inverter_power", "modules_map",
            "modules_per_string_per_inverter", "module_id", "module_manufacturer", "module_model"
        ]
        return {
            **{k: config_data.get(k) for k in keys}
        }

    def _get_configuration_b(self):
        """Calcola la configurazione FV per un impianto utility-scale da 100 a 1000kW: unica area (somma sottocampi)."""
        fv_series = 'B'

        # Step B1. Calcolo n. provvisorio di moduli grandi (3.1 mq per modulo)
        provisional_modules = int(self.total_real_area / MQ_PER_MODULE_LARGE)
        provisional_modules = max(200, min(provisional_modules, 1500))

        # Step B2. Query per ottenere configurazione per la posizione e il numero provvisorio di moduli
        sql_query = """
            SELECT * FROM configuration_scheme
            WHERE n_temp_modules <= %s AND position = %s AND series = %s
            ORDER BY total_power DESC
            LIMIT 1
        """

        config_data = {}
        row_data = self.execute_query(sql_query,
                                      (str(provisional_modules), self.fv_position, fv_series),
                                      fetch_one=True)
        if not row_data:
            logger.error(f"Nessuna configurazione per {provisional_modules} moduli e posizione {self.fv_position}")
        else:
            config_data = dict(row_data)

        # Step B3. Query per ottenere configurazione se utente ha specificato la potenza desiderata
        desired_power = self.user_total_power
        if desired_power and config_data:
            if config_data.get('total_power', 0) > desired_power:
                sql_query = """
                    SELECT * FROM configuration_scheme
                    WHERE position = %s AND series = %s AND total_power <= %s 
                    ORDER BY total_power DESC LIMIT 1
                """
                row_data = self.execute_query(sql_query,
                                              (self.fv_position, fv_series, desired_power),
                                              fetch_one=True)
                if row_data:
                    config_data = dict(row_data)
                else:
                    # registro errore ma lascio la configurazione calcolata con l'area
                    logger.error(f"Nessuna configurazione per {desired_power} potenza e posizione {self.fv_position}")

        final_config = self._build_final_configuration(config_data)

        # aggiunge la configurazione ottimale al generator_configuration
        if final_config:
            # se c'è solo 1 campo ritorna subito
            if len(self.user_subfields) == 1:
                return {'A': {'A1': final_config}}

            # altrimenti ripartisco la configurazione per le diverse sottocampi # TODO: soluzione temporanea NO BUONA
            n_temp_modules = 0
            n_modules = 0
            n_strings = 0
            n_inverters = 0

            generator_configuration = {}
            count = 0
            tot_area = self.total_available_area

            for field_key, subfield_dict in self.user_subfields.items():
                generator_configuration[field_key] = {}
                for subfield_key, subfield in subfield_dict.items():
                    copied_dict = copy.deepcopy(final_config)
                    if count < self.n_subfields-1:
                        ntm = round(final_config['n_temp_modules'] / tot_area * subfield.get('area'), 0)
                        n_temp_modules += ntm
                        copied_dict['n_temp_modules'] = int(ntm)

                        nm = round(final_config['n_modules'] / tot_area * subfield.get('area'), 0)
                        n_modules += nm
                        copied_dict['n_modules'] = int(nm)

                        ns = round(final_config['n_strings'] / tot_area * subfield.get('area'), 0)
                        n_strings += ns
                        copied_dict['n_strings'] = int(ns)

                        ni = round(final_config['n_inverters'] / tot_area * subfield.get('area'), 0)
                        n_inverters += ni
                        copied_dict['n_inverters'] = int(ni)

                        copied_dict['total_power'] = round(nm * final_config['module_power'] / 1000, 5)
                    else:
                        n_mods = int(round(final_config['n_modules'] - n_modules, 0))
                        copied_dict['n_temp_modules'] = int(round(final_config['n_temp_modules'] - n_temp_modules, 0))
                        copied_dict['n_modules'] = n_mods
                        copied_dict['n_strings'] = int(round(final_config['n_strings'] - n_strings, 0))
                        copied_dict['n_inverters'] = int(round(final_config['n_inverters'] - n_inverters, 0))
                        copied_dict['total_power'] = (round(n_mods * final_config['module_power'] / 1000, 5))
                    count += 1
                    generator_configuration[field_key][subfield_key] = copied_dict

            return generator_configuration  # {'A': {'A1': final_config}}
        else:
            return {}

    def _get_configuration_a(self):
        """Calcola la configurazione FV per un impianto serie A: per sottocampi."""
        fv_series = 'A'

        generator_configuration = {}

        for field_key, subfield_dict in self.user_subfields.items():
            generator_configuration[field_key] = {}

            for subfield_key, subfield in subfield_dict.items():

                # Step A1. Area disponibile del sottocampo selezionata dall'utente
                available_area = subfield.get("area", 0.0)

                # Step A2. Calcolo dell'area totale realmente disponibile per l'impianto (bordi, camminamenti, ecc.)
                gcr = GROUND_COVERAGE_RATIO.get(self.fv_position, 0.8)
                real_area = available_area * gcr

                # Step A3. Calcolo del n. provvisorio di moduli
                provisional_modules = int(real_area / MQ_PER_MODULE)
                provisional_modules = max(6, min(provisional_modules, 224))

                # Step A4. Query per ottenere configurazione per la posizione e il numero provvisorio di moduli
                sql_query = """
                    SELECT * FROM configuration_scheme
                    WHERE n_temp_modules = %s AND position = %s AND series = %s 
                    LIMIT 1
                """
                row_data = self.execute_query(sql_query,
                                              (str(provisional_modules), self.fv_position, fv_series),
                                              fetch_one=True)
                if not row_data:
                    logger.error(f"No configurazioni per {provisional_modules} moduli e posizione {self.fv_position}")
                    continue
                config_data = dict(row_data)

                # Se specificata potenza totale, cerca configurazione compatibile
                if self.user_total_power:
                    desired_power = self.desired_subfield_powers[field_key][subfield_key]["power"]
                    if desired_power is None:
                        logger.error(f"Potenza desiderata mancante per campo {field_key} sottocampo {subfield_key}")
                        continue

                    if config_data['total_power'] > desired_power:
                        sql_query = """
                            SELECT * FROM configuration_scheme
                            WHERE position = %s AND series = %s AND total_power <= %s 
                            ORDER BY total_power DESC LIMIT 1
                        """
                        row_data = self.execute_query(sql_query,
                                                      (self.fv_position, fv_series, desired_power),
                                                      fetch_one=True)
                        if not row_data:
                            logger.error(f"Nel db nessuna configurazione per la potenza {desired_power} desiderata")
                        else:
                            config_data = dict(row_data)

                final_config = self._build_final_configuration(config_data)
                if not final_config:
                    logger.error("Nessuna configurazione valida disponibile.")
                    continue

                # aggiunge altre chiavi
                final_config["area"] = available_area

                # CASO A: presenza di accumulo
                if self.fv_with_storage:
                    final_config["inverter_id"] = config_data["inverter_id_storage"]
                    final_config["inverter_manufacturer"] = config_data["inverter_manufacturer_storage"]
                    final_config["inverter_model"] = config_data["inverter_model_storage"]
                    final_config["e_compliance"] = config_data["compliance_storage"]

                    inverter_powers = config_data.get('inverter_power', [])
                    inverter_powers = [float(p) for p in inverter_powers]
                    compatible_storage = config_data.get('compatible_storage', {})

                    if inverter_powers and compatible_storage:
                        max_inverter_power = max(inverter_powers) * self.storage_level
                        best_key = self._find_closest_storage_key(compatible_storage, max_inverter_power)
                        if best_key:
                            best_storage_capacity, n_storages_per_inverter = self._find_best_storage(
                                compatible_storage,
                                max_inverter_power
                            )
                            n_storages = n_storages_per_inverter * config_data['n_inverters']
                            storage_data = compatible_storage[best_key]
                            final_config.update({
                                'storage_id': storage_data.get('storage_id'),
                                'n_storages': n_storages,
                                'storage_manufacturer': storage_data.get('manufacturer'),
                                'storage_model': storage_data.get('model')
                            })

                # CASO B: assenza di accumulo
                else:
                    final_config["inverter_id"] = config_data["inverter_id_nostorage"]
                    final_config["inverter_manufacturer"] = config_data["inverter_manufacturer_nostorage"]
                    final_config["inverter_model"] = config_data["inverter_model_nostorage"]
                    final_config["e_compliance"] = config_data["compliance_nostorage"]

                # prepara l'immagine di layout
                layout_image_path = self._prepare_plant_layout_images(final_config)
                if layout_image_path:
                    final_config['layout_png'] = layout_image_path

                # aggiunge la configurazione ottimale al generator_configuration
                generator_configuration[field_key][subfield_key] = final_config

        return generator_configuration

    @staticmethod
    def _compute_generator_power(configurations):
        """Calcola la potenza totale del generatore sommando il campo 'total_power'
         di ciascuna configurazione in input."""
        total = 0.0
        for group in configurations.values():
            for config in group.values():
                total += config.get("total_power", 0)
        # Arrotonda la potenza finale del generatore, per evitare float molto lunghi
        total = round(total, 5)
        return total

    @staticmethod
    def _get_first_module_power(configurations):
        """Restituisce il valore 'module_power' del primo sottoelemento trovato nel dizionario annidato. """
        for group in configurations.values():
            for config in group.values():
                module_power = config.get("module_power")
                if module_power is not None:
                    return int(module_power)
        return None

    def _collect_component_ids(self, configurations):
        """
        Crea un dizionario con liste di ID (module, inverter, storage, support)
        estratti dalle configurazioni del dizionario annidato.
        """
        module_ids = []
        inverter_ids = []
        storage_ids = []
        support_ids = []

        for field in configurations.values():  # A, B, ...
            for config in field.values():  # A1, A2, B1, ...
                module_id = config.get("module_id")
                if module_id:
                    module_ids.append(module_id)

                inverter_id = config.get("inverter_id")
                if inverter_id:
                    inverter_ids.append(inverter_id)

                storage_id = config.get("storage_id")
                if storage_id:
                    storage_ids.append(storage_id)

        support_id = SUPPORT.get(self.fv_position, '')
        if support_id:
            support_ids.append(support_id)

        # Conversione da set a liste per la compatibilità JSON
        component_ids = {
            'module': list(set(module_ids)),
            'inverter': list(set(inverter_ids)),
            'storage': list(set(storage_ids)),
            'support': list(set(support_ids)),
        }
        return component_ids

    @staticmethod
    def _find_closest_storage_key(storages, value):
        """Trova la capacità storage più vicina al valore richiesto."""
        try:
            return min(storages.keys(), key=lambda k: abs((value / float(k)) - 1))
        except Exception as e:
            logger.error(f"Errore nel calcolo dello storage più vicino: {e}")
            return False

    @staticmethod
    def _find_best_storage(storages, max_inverter_power):
        """Trova lo storage più adatto rispetto alla potenza dell'inverter.
        Vincoli:
        1) max_inverter_power / capacità più vicino ad 1
        2) calcola il numero di sistemi cessar che non eccedano il 'max_systems'
        3) se non trova restituisce il più piccolo
        Restituisce la chiave (capacità) e il numero di sistemi necessari controllando di non eccedere il
        """
        best_diff = float('inf')
        best_capacity = None
        best_ratio = None

        for k_str in storages:
            try:
                k_float = float(k_str)
                ratio = max_inverter_power / k_float
                diff = abs(ratio - 1)

                if diff < best_diff:
                    best_diff = diff
                    best_capacity = k_str
                    best_ratio = ratio

            except (ValueError, ZeroDivisionError):
                continue

        # Se non trovato nulla, scegli la capacità minima disponibile
        if best_capacity is None and storages:
            min_key = min(storages.keys(), key=lambda k: float(k))
            best_capacity = min_key
            best_ratio = max(1, round(max_inverter_power / float(min_key)))
        elif best_capacity is not None:
            best_ratio = max(1, round(best_ratio))

        return best_capacity, best_ratio

    @staticmethod
    def _calculate_generator_sizes(final_configuration):
        """Calcolo delle principali dimensioni totali del generatore fotovoltaico."""
        total_modules = 0
        total_strings = 0
        total_inverters = 0

        for field in final_configuration.values():  # A, B, ...
            for subfield in field.values():  # A1, A2, B1, ...
                total_modules += subfield.get('n_modules', 0)
                total_strings += subfield.get('n_strings', 0)
                total_inverters += subfield.get('n_inverters', 0)
        return total_modules, total_strings, total_inverters

    @staticmethod
    def round_nearest_10(n):
        """Arrotonda i valori superiori a 10 alle decine."""
        if n < 10:
            return n
        return round(n / 10) * 10

    def _calculate_cable_lengths(self, generator_power, total_modules, total_strings, total_inverters):
        """Calcola la lunghezza dei cavi necessari: dizionario usato nel cap cavi. (5-10% margine sicurezza)"""

        # distanza tra moduli (1m x modulo + 5% margine) e moduli e scatola di giunzione (5m x stringa)
        modules_between_1 = int((total_modules * 1) * 1.05)
        modules_between_2 = int((total_modules * 1) * 1.1)
        string_junction_1 = int(total_strings * 3)
        string_junction_2 = int(total_strings * 5)
        modules_junction_1 = self.round_nearest_10(modules_between_1 + string_junction_1)
        modules_junction_2 = self.round_nearest_10(modules_between_2 + string_junction_2)

        # distanza tra scatola di giunzione e inverter (30 m per inverter) lato DC
        junction_inverter_1 = self.round_nearest_10(generator_power * 0.1 * total_strings * 1.1)
        junction_inverter_2 = self.round_nearest_10(generator_power * 0.2 * total_strings * 1.1)

        # distanza tra inverter e quadro elettrico (potenza impianto * 10-20% * n. inverter * margine) lato AC
        inverter_panel_1 = self.round_nearest_10(generator_power * 0.1 * total_inverters * 1.1)
        inverter_panel_2 = self.round_nearest_10(generator_power * 0.2 * total_inverters * 1.1)

        # distanza tra inverter e accumulo se c'è
        if self.fv_with_storage:
            inverter_storage = "1-5"
        else:
            inverter_storage = ""

        cable_lengths = {
            "modules_junction": f'{modules_junction_1}-{modules_junction_2}',
            "junction_inverter": f'{junction_inverter_1}-{junction_inverter_2}',
            "inverter_panel": f"{inverter_panel_1}-{inverter_panel_2}",
            "inverter_storage": f"{inverter_storage}",
            "grounding_system": '10-30',
            "communication": '10-50',
        }

        return cable_lengths

    @staticmethod
    def _prepare_plant_layout_images(final_config):
        """Funzione che recupera l'immagine di layout corretta da DigitalOcean Spaces
        Il nome del file è composto da n_temp_modules e fv_series, es: 37_A.png, nella cartella 'layouts'"""

        n_temp_modules = final_config.get('n_temp_modules')
        fv_series = final_config.get('series')
        if not n_temp_modules or not fv_series:
            return None
        image_name = f"{n_temp_modules}_{fv_series}.png"
        image_path = f"layouts/{image_name}"
        # Verifica che l'immagine esista su DigitalOcean Spaces
        storage_service = StorageFactory.get_storage_service()
        try:
            if storage_service.file_exists(image_path):
                return image_path  # Restituisce il path invece dello stream
            else:
                return None
        except Exception as e:
            logger.error(f"Errore nel recupero dell'immagine di layout: {e}")
            return None

    def run(self):
        """Gestisce il workflow del dimensionamento."""

        # Step 1. Calcola il numero totale di sottocampi
        self._calculate_n_subfields()

        # Step 1. Calcolo l'area totale dell'area selezionata dall'utente
        self._calculate_total_available_area()
        if not self.total_available_area:
            return False

        # Step 2. Calcolo della potenza desiderata dei sottocampi se immessa dall'utente la potenza complessiva
        self._distribute_power_by_area_if_needed()

        # Step 3. Calcolo dell'area totale realmente disponibile per l'impianto (bordi, camminamenti, ecc.)
        self._calculate_real_area()

        # Step 4. Calcolo n. provvisorio di moduli medi (2.1 mq per modulo) anche se agri così vedo se config serie A
        total_provisional_modules = self._estimate_provisional_modules()

        # Step 5. Percorso per ottenere la configurazione ottimale e Trova la configurazione ottimale
        # generator_configuration = {}

        # Caso A: meno di 224 moduli -> configurazioni serie A
        print_report = True
        if total_provisional_modules <= 224:
            generator_configuration = self._get_configuration_a()
        else:
            # Caso B: tanti moduli su agrivoltaico a terra -> configurazioni serie B
            if self.fv_position == 'AG':
                generator_configuration = self._get_configuration_b()
                print_report = False
            # Caso C: tanti moduli non su agrivoltaico -> configurazioni serie A
            else:
                generator_configuration = self._get_configuration_a()

        # Step 6. Calcola component_ids
        component_ids = self._collect_component_ids(generator_configuration)

        # Step 7. Trova la potenza del modulo (W)
        single_module_power = self._get_first_module_power(generator_configuration)

        # Step 8. Calcola potenza globale dell'impianto
        generator_power = self._compute_generator_power(generator_configuration)

        # Step 9. calcolo del totale n. inverter, n. moduli e numero stringhe
        total_modules, total_strings, total_inverters = self._calculate_generator_sizes(generator_configuration)

        # Step 10. Calcola lunghezza cavi
        cable_lengths = self._calculate_cable_lengths(generator_power, total_modules, total_strings, total_inverters)

        # Step 11. Dizionario restituito
        output = {
            'sizing': generator_configuration,
            'component_ids': component_ids,
            'generator_power': generator_power,
            'cable_lengths': cable_lengths,
            'sizing_global': {
                "total_modules": total_modules,
                "total_strings": total_strings,
                "total_inverters": total_inverters,
                "module_power": single_module_power
            },
            "single_module_power": single_module_power,
            "print_report": print_report
        }
        return output

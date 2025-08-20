"""
graphs_generator.py
Classe che gestisce la generazione dei grafici per il progetto fotovoltaico.
Genera i grafici richiesti per il calcolatore solare e la producibilità.
"""
import logging
from storage.factory import StorageFactory
from ..graphs_generator.chart_generator import Chart_Generator
import matplotlib.pyplot as plt
import os
import tempfile
from typing import Dict, List, Optional
from lxml import etree
from .sections.common import Common
import matplotlib
# Usa il backend non-GUI per evitare problemi con i thread
matplotlib.use('Agg')

logger = logging.getLogger('django')


class GraphsGenerator:
    """
    Classe per generare i grafici del progetto fotovoltaico.
    Gestisce la generazione e il salvataggio dei grafici su storage.
    """

    def __init__(self, data):
        self.data = data
        self.chart_generator = Chart_Generator()
        self.project_complete_path = self.data.get('project_complete_path', '')
        self.graphs_paths = {}  # Dizionario per memorizzare i path dei grafici generati

    def generate_all_graphs(self):
        """
        Genera tutti i grafici richiesti per il progetto.

        Returns:
            dict: Dizionario contenente i path dei grafici generati e i placeholder
        """
        result = {}

        try:
            # Genera i grafici del calcolatore solare (arancioni)
            solar_graphs = self.generate_solar_calculator_graphs()
            result.update(solar_graphs)

            # Genera i grafici della producibilità (verdi)
            productivity_graphs = self.generate_productivity_graphs()
            result.update(productivity_graphs)

            # Genera i grafici del cashflow (blu)
            cashflow_graphs = self.generate_cashflow_graphs()
            result.update(cashflow_graphs)

            # Salva i path dei grafici nel keopebank
            result['graphs_paths'] = self.graphs_paths

            return result

        except Exception as e:
            logger.error(f"Errore nella generazione dei grafici: {e}")
            return {}

    def convert_monthly_data_to_chart_format(self, monthly_data):
        """
        Converte i dati mensili dal formato italiano (GEN, FEB, ecc.) al formato numerico (1, 2, ecc.)
        per l'uso nei grafici.

        Args:
            monthly_data: Dizionario con chiavi in formato italiano e valori come tuple o valori singoli

        Returns:
            dict: Dizionario con chiavi numeriche (1-12) e valori float
        """
        mesi_mapping = {
            'GEN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAG': 5, 'GIU': 6,
            'LUG': 7, 'AGO': 8, 'SET': 9, 'OTT': 10, 'NOV': 11, 'DIC': 12
        }

        chart_data = {}
        for month_str, data_tuple in monthly_data.items():
            if month_str in mesi_mapping:
                month_num = mesi_mapping[month_str]
                if isinstance(data_tuple, (list, tuple)) and len(data_tuple) >= 2:
                    value = data_tuple[0]
                    chart_data[month_num] = float(value)
                else:
                    chart_data[month_num] = float(data_tuple)

        return chart_data

    def generate_solar_calculator_graphs(self):
        """
        Genera i grafici per il capitolo Calcolatore solare (arancioni).

        Returns:
            dict: Dizionario con i placeholder dei grafici generati
        """
        graphs_data = {}

        # 1) Irradiazione solare orizzontale (kWh/m²/giorno)
        horizontal_irradiation_graph = self.generate_horizontal_irradiation_graph()
        if horizontal_irradiation_graph:
            logger.debug("OK horizontal_irradiation_graph OK")

        # 2) Irradiazione solare mensile sul piano dei moduli (kWh/m²/mese)
        plane_irradiation_graph = self.generate_module_plane_irradiation_graph()
        if plane_irradiation_graph:
            logger.debug("OK Irradiazione solare mensile sul piano dei moduli (kWh/m²/mese) OK")

        return graphs_data

    def generate_productivity_graphs(self):
        """
        Genera i grafici per il capitolo Producibilità (verdi).

        Returns:
            dict: Dizionario con i placeholder dei grafici generati
        """
        graphs_data = {}

        # 3) Valori di producibilità mensile (kWh/kWp)
        result = self.generate_monthly_productivity_graph()
        if result:
            logger.debug("OK Producibilità specifica mensile (kWh/kWp) OK")

        # 4) Valori di produzione elettrica mensile (kWh/mese)
        # monthly_production_graph = self.generate_monthly_production_graph()
        # if monthly_production_graph:
        #   graphs_data['g004'] = monthly_production_graph

        return graphs_data

    def generate_horizontal_irradiation_graph(self):
        """
        Genera il grafico dell'irradiazione solare orizzontale (kWh/m²/giorno).

        Returns:
            str: Path del grafico salvato o None se errore
        """
        try:
            # Estrai i dati dall'ao1
            ao1_data = self.data.get('ao1', {}).get('first_subfield', {})

            # Prova diverse chiavi possibili per l'irradiazione orizzontale
            horizontal_irradiation_data = (
                ao1_data.get('monthly_avg_daily_horizontal_irradiance', {}) or
                ao1_data.get('monthly_avg_daily_horizontal_solar_irradiance_summary', {}).get('monthly_avg_daily_horizontal_irradiance', {}) or
                {}
            )

            if not horizontal_irradiation_data:
                logger.warning("Dati irradiazione orizzontale non disponibili")
                logger.warning(f"Chiavi disponibili in ao1: {list(ao1_data.keys())}")
                return None

                # Prepara i dati per il grafico
            chart_data = self.convert_monthly_data_to_chart_format(
                horizontal_irradiation_data)

            if not chart_data:
                logger.warning("Nessun dato valido per irradiazione orizzontale")
                return None

            # Genera il grafico
            filename = "horizontal_irradiance.png"
            file_path = f"{self.project_complete_path}/{filename}"

            fig = self.chart_generator.crea_grafico(
                dati=chart_data,
                titolo="Irradiazione solare orizzontale",
                label_x="Mese",
                label_y="Irradiazione (kWh/m²/giorno)",
                stile="moderno",
                tipo_grafico="barre",
                unita_misura_tempo='mesi',
                dimensioni=(6.69, 3.9)  # 17cm x 8.5cm convertiti in pollici
            )

            # Salva il grafico
            saved_path = self.save_chart_to_storage(fig, file_path)
            if saved_path:
                logger.debug(f"file salvato {file_path}")

            return True

        except Exception as e:
            logger.error(f"Errore nella generazione del grafico irradiazione orizzontale: {e}")
            return None

    def generate_module_plane_irradiation_graph(self):
        """
        Genera il grafico dell'irradiazione solare mensile sul piano dei moduli.
        Se ci sono più sottocampi, crea un grafico multibarra.

        Returns:
            str: Path del grafico salvato o None se errore
        """
        try:
            # Estrai i dati dei sottocampi
            ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
            generator = self.data.get('generator', {})

            if not ao1_subfields or not generator:
                logger.warning("Dati sottocampi non disponibili per irradiazione piano moduli")
                return None

            for field_name, field_data in generator.items():
                subfields_data = {}
                for subfield_name, subfield_data_gen in field_data.items():
                    if subfield_name in ao1_subfields:
                        display_name = f"{subfield_name}"

                        subfield_data = ao1_subfields[subfield_name]
                        monthly_irradiation = subfield_data.get('monthly_plane_of_array_irradiance', {})

                        if monthly_irradiation:
                            chart_data = self.convert_monthly_data_to_chart_format(monthly_irradiation)
                            if chart_data:
                                subfields_data[display_name] = chart_data

                if not subfields_data:
                    logger.warning("Nessun dato valido per irradiazione piano moduli")
                    return None

                # Genera il grafico
                filename = f"{field_name}_irradiance_plane.png"
                file_path = f"{self.project_complete_path}/{filename}"

                if len(subfields_data) == 1:
                    # Un solo sottocampo - grafico semplice
                    single_data = list(subfields_data.values())[0]
                    fig = self.chart_generator.crea_grafico(
                        dati=single_data,
                        titolo="",
                        label_x="Mese",
                        label_y="Irradiazione (kWh/m²/mese)",
                        stile="moderno",
                        tipo_grafico="barre",
                        unita_misura_tempo='mesi',
                        # 17cm x 10cm convertiti in pollici
                        dimensioni=(6.69, 3.93)
                    )
                else:
                    # Più sottocampi - grafico di confronto
                    fig = self.chart_generator.crea_grafico_confronto(
                        dati_multipli=subfields_data,
                        titolo="",
                        label_x="Mese",
                        label_y="Irradiazione (kWh/m²/mese)",
                        stile="moderno",
                        unita_misura_tempo='mesi',
                        # 17cm x 8.5cm convertiti in pollici
                        dimensioni=(6.69, 3.35)
                    )

                # Salva il grafico
                saved_path = self.save_chart_to_storage(fig, file_path)
                if saved_path:
                    logger.debug(f"file salvato {file_path}")
                #    self.graphs_paths['g002'] = saved_path
                #    return saved_path

            return True

        except Exception as e:
            logger.error(f"Errore nella generazione del grafico irradiazione piano moduli: {e}")
            return None

    def generate_monthly_productivity_graph(self):
        """
        Genera il grafico dei valori di producibilità mensile (kWh/kWp).
        Se ci sono più sottocampi, crea un grafico multibarra.

        Returns:
            str: Path del grafico salvato o None se errore
        """
        try:
            # Estrai i dati dei sottocampi
            ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
            generator = self.data.get('generator', {})

            if not ao1_subfields or not generator:
                logger.warning("Dati sottocampi non disponibili per producibilità mensile")
                return None

            for field_name, field_data in generator.items():
                subfields_data = {}
                for subfield_name, subfield_data_gen in field_data.items():
                    if subfield_name in ao1_subfields:
                        display_name = f"{subfield_name}"

                        subfield_data = ao1_subfields[subfield_name]
                        monthly_yield = subfield_data.get('monthly_energy_yield', {})

                        if monthly_yield:
                            chart_data = self.convert_monthly_data_to_chart_format(monthly_yield)
                            if chart_data:
                                subfields_data[display_name] = chart_data

                if not subfields_data:
                    logger.warning("Nessun dato valido per producibilità mensile")
                    return None

                # Genera il grafico
                filename = f"{field_name}_energy_yield.png"
                file_path = f"{self.project_complete_path}/{filename}"

                if len(subfields_data) == 1:
                    # Un solo sottocampo - grafico semplice
                    single_data = list(subfields_data.values())[0]
                    fig = self.chart_generator.crea_grafico(
                        dati=single_data,
                        titolo="",
                        label_x="Mese",
                        label_y="Producibilità (kWh/kWp)",
                        stile="elegante",
                        tipo_grafico="barre",
                        unita_misura_tempo='mesi',
                        # 17cm x 10cm convertiti in pollici
                        dimensioni=(6.69, 3.93)
                    )
                else:
                    # Più sottocampi - grafico di confronto
                    fig = self.chart_generator.crea_grafico_confronto(
                        dati_multipli=subfields_data,
                        titolo="",
                        label_x="Mese",
                        label_y="Producibilità (kWh/kWp)",
                        stile="elegante",
                        unita_misura_tempo='mesi',
                        # 17cm x 8.5cm convertiti in pollici
                        dimensioni=(6.69, 3.35)
                    )

                # Salva il grafico
                saved_path = self.save_chart_to_storage(fig, file_path)
                if saved_path:
                    logger.debug(f"file salvato {file_path}")

            return True

        except Exception as e:
            logger.error(f"Errore nella generazione del grafico producibilità mensile: {e}")
            return None

    def generate_monthly_production_graph(self):
        """
        Genera il grafico dei valori di produzione elettrica mensile (kWh/mese).
        Se ci sono più sottocampi, crea un grafico multibarra.

        Returns:
            str: Path del grafico salvato o None se errore
        """
        try:
            # Estrai i dati dei sottocampi
            ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
            generator = self.data.get('generator', {})

            if not ao1_subfields or not generator:
                logger.warning(
                    "Dati sottocampi non disponibili per produzione mensile")
                return None

            # Prepara i dati per il grafico multibarra
            subfields_data = {}

            for field_name, field_data in generator.items():
                for subfield_name, subfield_data_gen in field_data.items():
                    if subfield_name in ao1_subfields:
                        user_subfield_name = subfield_data_gen.get('name', '')
                        display_name = f"{subfield_name} {user_subfield_name}" if user_subfield_name else subfield_name

                        subfield_data = ao1_subfields[subfield_name]
                        monthly_production = subfield_data.get(
                            'monthly_net_energy', {})

                        if monthly_production:
                            chart_data = self.convert_monthly_data_to_chart_format(
                                monthly_production)

                            if chart_data:
                                subfields_data[display_name] = chart_data

            if not subfields_data:
                logger.warning("Nessun dato valido per produzione mensile")
                return None

            # Genera il grafico
            filename = "grafico_produzione_mensile.png"
            file_path = f"{self.project_complete_path}/{filename}"

            if len(subfields_data) == 1:
                # Un solo sottocampo - grafico semplice
                single_data = list(subfields_data.values())[0]
                fig = self.chart_generator.crea_grafico(
                    dati=single_data,
                    titolo="Produzione elettrica mensile",
                    label_x="Mese",
                    label_y="Produzione (kWh/mese)",
                    stile="elegante",
                    tipo_grafico="barre",
                    unita_misura_tempo='mesi',
                    # 17cm x 8.5cm convertiti in pollici
                    dimensioni=(6.69, 3.9)
                )
            else:
                # Più sottocampi - grafico di confronto
                fig = self.chart_generator.crea_grafico_confronto(
                    dati_multipli=subfields_data,
                    titolo="Produzione elettrica mensile per sottocampo",
                    label_x="Mese",
                    label_y="Produzione (kWh/mese)",
                    stile="elegante",
                    unita_misura_tempo='mesi',
                    # 17cm x 10cm convertiti in pollici
                    dimensioni=(6.69, 3.9)
                )

            # Salva il grafico
            saved_path = self.save_chart_to_storage(fig, file_path)
            if saved_path:
                self.graphs_paths['g004'] = saved_path
                return saved_path

            return None

        except Exception as e:
            logger.error(
                f"Errore nella generazione del grafico produzione mensile: {e}")
            return None

    def generate_cashflow_graphs(self):
        """
        Genera i grafici per il capitolo Cashflow (blu).

        Returns:
            dict: Dizionario con i placeholder dei grafici generati
        """
        graphs_data = {}

        # Genera il grafico del cashflow cumulativo
        cashflow_graph = self.generate_cashflow_cumulative_graph()
        if cashflow_graph:
            graphs_data['X155'] = cashflow_graph

        return graphs_data

    def generate_cashflow_cumulative_graph(self):
        """
        Genera il grafico del cashflow cumulativo netto.

        Returns:
            str: Path del grafico salvato o None se errore
        """
        try:
            # Estrai i dati dal ecofin
            ecofin_data = self.data.get('ecofin', {})
            euros_storage = ecofin_data.get('cumulative_cashflow_with_storage', [])
            euros_nostorage = ecofin_data.get('cumulative_cashflow_without_storage', [])

            if not euros_storage or not euros_nostorage:
                logger.warning("Dati cashflow non disponibili")
                return None

            # Converte i dati in formato dizionario per il grafico
            # I dati sono una lista di 25 valori (anni 1-25)
            storage_data = {i+1: float(value)
                            for i, value in enumerate(euros_storage)}
            nostorage_data = {i+1: float(value)
                              for i, value in enumerate(euros_nostorage)}

            # Determina quale grafico generare in base alla configurazione storage
            if self.data.get('storage') == '1':
                # Con storage
                chart_data = storage_data
                filename = "cashflow_with_storage.png"
                title = "Cashflow cumulativo netto (con accumulo)"
            else:
                # Senza storage
                chart_data = nostorage_data
                filename = "cashflow_without_storage.png"
                title = "Cashflow cumulativo netto (senza accumulo)"

            file_path = f"{self.project_complete_path}/{filename}"

            # Genera il grafico
            fig = self.chart_generator.crea_grafico(
                dati=chart_data,
                titolo=title,
                label_x="Anno",
                label_y="Cashflow cumulativo netto (€)",
                stile="cashflow",
                tipo_grafico="barre",
                unita_misura_tempo='anni',
                dimensioni=(6.5, 3.9)  # 16.5cm x 10cm convertiti in pollici
            )

            # Salva il grafico
            saved_path = self.save_chart_to_storage(fig, file_path)
            if saved_path:
                self.graphs_paths['X155'] = saved_path
                return saved_path

            return None

        except Exception as e:
            logger.error(f"Errore nella generazione del grafico cashflow: {e}")
            return None

    def save_chart_to_storage(self, fig, file_path):
        """
        Salva il grafico su storage (locale o DigitalOcean Spaces).

        Args:
            fig: Figura matplotlib
            file_path: Path di destinazione

        Returns:
            str: Path del file salvato o None se errore
        """
        try:
            storage_service = StorageFactory.get_storage_service()

            if hasattr(storage_service, 'upload_file'):
                # Storage DigitalOcean Spaces
                try:
                    # Crea un file temporaneo
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                        temp_path = temp_file.name

                    # Salva il grafico nel file temporaneo
                    fig.savefig(temp_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
                    plt.close(fig)  # Chiudi la figura per liberare memoria

                    # Prepara il path per Spaces
                    if not file_path.startswith('media/'):
                        spaces_path = f"media/{file_path}"
                    else:
                        spaces_path = file_path

                    # Carica su Spaces
                    storage_service.upload_file(temp_path, spaces_path)

                    # Pulisci il file temporaneo
                    os.unlink(temp_path)

                    logger.debug(f"Grafico salvato su Spaces: {spaces_path}")
                    return file_path

                except Exception as e:
                    logger.error(f"Errore nel salvataggio su Spaces: {e}")
                    # Pulisci il file temporaneo in caso di errore
                    if 'temp_path' in locals() and os.path.exists(temp_path):
                        os.unlink(temp_path)
                    return None
            else:
                # Storage locale
                directory = os.path.dirname(file_path)
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)

                fig.savefig(file_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
                plt.close(fig)  # Chiudi la figura per liberare memoria

                logger.debug(f"Grafico salvato localmente: {file_path}")
                return file_path

        except Exception as e:
            logger.error(f"Errore nel salvataggio del grafico: {e}")
            return None

    def create_graph_placeholders(self):
        """
        Crea i placeholder XML per i grafici generati.

        Returns:
            dict: Dizionario con i placeholder XML
        """
        placeholders = {}

        for graph_id, graph_path in self.graphs_paths.items():
            if graph_path:
                # Crea il placeholder XML per l'immagine
                placeholders[graph_id] = self.create_image_xml_placeholder(
                    graph_path, graph_id)

        return placeholders

    def create_image_xml_placeholder(self, image_path, graph_id):
        """
        Crea il placeholder XML per un'immagine.

        Args:
            image_path: Path dell'immagine
            graph_id: ID del grafico

        Returns:
            str: Stringa XML per il placeholder
        """

        # Definisci le didascalie per ogni grafico
        captions = {
            'g001': 'Irradiazione solare orizzontale mensile (kWh/m²/giorno)',
            'g002': 'Irradiazione solare mensile sul piano dei moduli (kWh/m²/mese)',
            'g003': 'Producibilità mensile (kWh/kWp)',
            'X155': 'Cashflow cumulativo netto (€)'
        }

        try:
            image_node = etree.Element("image", src=image_path, style="center")

            return Common.generate_string_xml(image_node)

        except Exception as e:
            logger.error(
                f"Errore nella creazione del placeholder XML per {graph_id}: {e}")
            return ""

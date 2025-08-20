"""
common.py
Classe che include funzioni utili a più moduli per creare il progetto in formato xml.
"""
import datetime
import locale

from lxml import etree
from PIL import Image, UnidentifiedImageError

from ..params import POSITION, SUPPORT_TYPE, STORAGE


class Common:

    @staticmethod
    def get_month_name(num):
        """Restituisce il nome del mese in base alla posizione."""

        months = {
            '1': 'Gennaio', '2': 'Febbraio', '3': 'Marzo', '4': 'Aprile', '5': 'Maggio', '6': 'Giugno',
            '7': 'Luglio', '8': 'Agosto', '9': 'Settembre', '10': 'Ottobre', '11': 'Novembre', '12': 'Dicembre',
        }
        return months[str(num)]

    @staticmethod
    def generate_string_xml(element):
        """Verifica se un nodo xml è valido e ben formattato."""

        try:
            xml_string = etree.tostring(
                element, pretty_print=True, encoding="utf-8").decode("utf-8")
            return xml_string
        except (TypeError, ValueError) as e:
            # logger.error(f"Errore durante la generazione della stringa XML: {e}")
            return ""

    @staticmethod
    def format_value(value, decimals=2):
        """Restituisce un valore numerico formattato con un numero specifico di decimali."""

        try:
            return f"{float(value):.{decimals}f}"
        except (ValueError, TypeError) as e:
            return ""

    @staticmethod
    def add_row_to_table(table, cells_content):
        """Aggiunge una riga a una tabella XML con il contenuto specificato per le celle."""

        row = etree.SubElement(table, "row")
        for cell_content in cells_content:
            cell = etree.SubElement(row, "cell")
            cell.text = cell_content

    @staticmethod
    def create_title_section(node, data):
        """Logica per creare la sezione del titolo."""

        project_title = data.get("general_data", {}).get("project_title", "")
        project_acronym = data.get("general_data", {}).get("project_acronym", "")
        project_acronym = f", denominato {project_acronym}" if project_acronym else ""
        generator_power = data.get('generator_power')
        power = f"\nPotenza: {generator_power} kWp" if generator_power else ''
        title = etree.SubElement(node, "title")
        title.text = f"{project_title}{project_acronym}{power}"

        return title

    @staticmethod
    def create_today_date_section(node, data):
        """Crea la sezione della data odierna in italiano con fallback sicuro"""
        try:
            # Prova a impostare il locale italiano
            locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
            today = datetime.date.today()
            formatted_today = f"{today.day} {today.strftime('%B %Y')}"
        except locale.Error:
            # Fallback: usa i nomi dei mesi italiani manualmente
            today = datetime.date.today()
            mesi_italiani = {
                1: 'gennaio', 2: 'febbraio', 3: 'marzo', 4: 'aprile',
                5: 'maggio', 6: 'giugno', 7: 'luglio', 8: 'agosto',
                9: 'settembre', 10: 'ottobre', 11: 'novembre', 12: 'dicembre'
            }
            nome_mese = mesi_italiani[today.month]
            formatted_today = f"{today.day} {nome_mese} {today.year}"

        date = etree.SubElement(node, "today")
        date.text = f"{formatted_today}"

        return date

    @staticmethod
    def create_design_title_section(node, data):
        """Logica per creare la sezione del titolo."""

        title = etree.SubElement(node, "h0")
        title.text = f"Distinta base di configurazione"

        return title

    @staticmethod
    def create_location_section(node, data):
        """Logica per creare la sezione localizzazione."""

        address = data.get("general_data", {}).get("address", "")
        municipality = data.get("general_data", {}).get("municipality", "")
        province = data.get("general_data", {}).get("province", "")
        region = data.get("general_data", {}).get("region", "")

        subtitle = etree.SubElement(node, "subtitle")
        text0 = etree.SubElement(subtitle, "text")
        text0.text = f"Località: {address}"
        text1 = etree.SubElement(subtitle, "text")
        text1.text = f"Regione {region.upper()}"
        text2 = etree.SubElement(subtitle, "text")
        text2.text = f"Provincia di {province.upper()}"
        text3 = etree.SubElement(subtitle, "text")
        text3.text = f"Comune di {municipality.upper()}"

        return subtitle

    @staticmethod
    def create_document_type_section(node, data):
        """Logica per creare la sezione tipo di documento."""

        text1 = etree.SubElement(node, "doc-type")
        text1.text = "PROGETTO DEFINITIVO/ESECUTIVO\nRELAZIONE TECNICA IMPIANTO FOTOVOLTAICO"

        return text1

    @staticmethod
    def generate_xml_table(data, table_style):
        """Genera una tabella XML a partire da una lista di liste (data) e uno stile personalizzato."""

        table_node = etree.Element("table", style=table_style)
        for row_data in data:
            row_node = etree.SubElement(table_node, "row")
            for cell_data in row_data:
                cell_node = etree.SubElement(row_node, "cell")
                cell_node.text = str(cell_data)

        return table_node

    @staticmethod
    def create_revision_section(node, data):
        """Logica per creare la sezione revisione."""

        general_data = data.get("general_data", {})
        rev_number = general_data.get("revision_number", "0")
        rev_date = general_data.get("revision_date", "")
        edit_by = general_data.get("edit_by", "")
        verified_by = general_data.get("verified_by", "")
        approved_by = general_data.get("approved_by", "")

        table = etree.SubElement(node, "table", position="revision",
                                 style="borders:TRBL;font-size:9;padding:0;width-cols:2-4.5;")

        # Aggiunta intestazioni
        headers = ["Rev.", "Descrizione", "Data",
                   "Redatto", "Verificato", "Approvato"]
        Common.add_row_to_table(table, headers)

        # Aggiunta dati revisione
        row = [rev_number, "Progetto definito/esecutivo",
               rev_date, edit_by, verified_by, approved_by]
        Common.add_row_to_table(table, row)
        # Aggiungi una riga con il primo valore come indice e il resto come celle vuote
        # for row_index in range(2):
        #    Common.add_row_to_table(table, [str(row_index)] + [""] * 5)

        return table

    @staticmethod
    def create_file_references_section(node, data):
        """Logica per creare la sezione riferimenti file."""

        project_code = data.get("project_code", "")
        references = [(f"Report_{project_code}.docx", f"Codice elaborato: {project_code}")] if project_code else [
            ("Nome del file", "Codice elaborato:")
        ]

        table = etree.SubElement(
            node, "table", position="file-code", style="borders:TRBL;font-size:9;padding:0")

        for file_name, file_code in references:
            row = etree.SubElement(table, "row")
            etree.SubElement(row, "cell").text = file_name
            etree.SubElement(row, "cell").text = file_code

        return table

    @staticmethod
    def load_image(image_path):
        """Carica un'immagine da un percorso specificato con gestione degli errori."""

        try:
            # Se è già un oggetto PIL.Image, restituiscilo
            if hasattr(image_path, 'size'):
                return image_path

            # Se è un path string, gestisci lo storage
            if isinstance(image_path, str):
                from storage.factory import StorageFactory
                storage_service = StorageFactory.get_storage_service()

                # Se è storage remoto (DigitalOcean Spaces), usa il metodo download_image
                if hasattr(storage_service, 'download_image'):
                    try:
                        # Per DigitalOcean Spaces, il path restituito da list_files_matching_pattern
                        # è già il Key completo su S3, quindi non serve aggiungere 'media/'
                        spaces_path = image_path
                        image_stream = storage_service.download_image(
                            spaces_path)
                        image_obj = Image.open(image_stream)
                        return image_obj
                    except Exception as e:
                        print(f"Errore nel caricamento da Spaces: {e}")
                        return None
                else:
                    # Storage locale
                    image_obj = Image.open(image_path)
                    return image_obj
            else:
                # Se è un file-like object (BytesIO, etc.)
                image_obj = Image.open(image_path)
                return image_obj
        except FileNotFoundError:
            print(f"Errore: File non trovato -> {image_path}")
            return None
        except UnidentifiedImageError:
            print(f"Errore: Il file non è un'immagine valida -> {image_path}")
            return None
        except Exception as e:
            print(f"Errore inatteso durante il caricamento dell'immagine: {e}")
            return None

    @staticmethod
    def create_images_paragraph(image_paths, width_cm=None, alignment="center"):
        """Crea un paragrafo con le immagini, opzionalmente con larghezza e allineamento specificato."""

        images = [Common.load_image(path) for path in image_paths]

        tag_node = etree.Element('tag_to_remove')

        for image, path in zip(images, image_paths):
            if image:
                image_element = etree.SubElement(tag_node, "image", src=path)
                image_element.set("style", alignment)
                if width_cm:
                    image_element.set("width", str(width_cm))

        if any(images):
            string = Common.generate_string_xml(tag_node)
            result = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")
            return result
        else:
            print("Nessuna immagine caricata, ritornando stringa vuota")
            return ''

    @staticmethod
    def create_table_location(data):
        """Crea la tabella relativa alla località di installazione dell'impianto."""

        rows = [
            ["Località specifica", data.get("plant_address", "")],
            ["Latitudine", data.get("latitude_str", "")],
            ["Longitudine", data.get("longitude_str", "")],
            ["Altitudine", data.get("altitude_str", "")],
            ["Riferimenti catastali", data.get("general_data", {}).get("cadastral_references", "")]
        ]
        valid_data = [row for row in rows if row[1]]
        return Common.generate_xml_table(valid_data, table_style="borders:TRBL;width-cols:8")

    @staticmethod
    def create_table_base_features_generator(data):
        """Crea la tabella relativa alle caratteristiche del generatore fotovoltaico."""

        rows = [
            ["Potenza nominale", f"{data.get('generator_power', '')} kWp"],
            ["Posizionamento", POSITION.get(data.get('mounting'), "")],
            ["Sistema di supporto", SUPPORT_TYPE.get(data.get('mounting'), "")],
            ["Accumulo", STORAGE.get(data.get('storage'), "")],
        ]
        valid_data = [row for row in rows if row[1]]
        return Common.generate_xml_table(valid_data, table_style="borders:TRBL;width-cols:8")

    @staticmethod
    def create_table_solar_produciblity(data):
        """Crea la tabella relativa all'energia solare e producibilità."""

        ao1 = data.get("ao1", {})
        data = [
            ["Fonte dati climatici", "UNI 10349-1: 2016; PVgis"],
            ["Fattore di albedo", data.get('albedo_str', "")],
            ["Irraggiamento solare annuo sul piano dei moduli", ao1.get('range_module_solar_radiation', '')],
            ["Energia utile annua", ao1.get('range_net_energy', '')],
            ["Efficienza percentuale del sistema", ao1.get('range_system_efficiency', '')],
            ["Perdite totali di sistema", ao1.get('range_losses_percentage', '')],
            ["Producibilità annuale specifica", ao1.get('range_specific_producibility', '')],
            ["Produzione energetica", f"{ao1.get('total_energy_production', "")} kWh/anno"],
            ["Riduzione di tonnellate di CO2", f"{ao1.get('ghg_co2_reduction', "")} t CO2/anno"],
            ["Tonnellate Equivalenti di Petrolio evitate in 20 anni di esercizio", f"{ao1.get('tep_reduction', "")} TEP"]
        ]
        valid_data = [row for row in data if row[1]]
        return Common.generate_xml_table(valid_data, table_style="borders:TRBL;width-cols:8")

    @staticmethod
    def create_table_components_configuration(data):
        """Crea la tabella relativa alle componenti e configurazione del generatore fotovoltaico."""

        sizing_global = data.get('sizing_global', {})
        data_table = [
            ["Superficie totale disponibile per l'installazione", data.get('total_area_str')],
            ["Numero di aree di installazione", data.get('n_fields_str')],
            ["Potenza nominale moduli", f"{sizing_global.get('module_power', '')} W"],
            ["Numero totale di moduli", f"{sizing_global.get('total_modules', "")} moduli"],
            ["Numero di stringhe", f"{sizing_global.get('total_strings', "")} stringhe"],
            ["Numero di inverter", f"{sizing_global.get('total_inverters', "")} inverter"],
            ["Vita utile stimata senza degrado significativo", "oltre 20 anni"],
        ]
        valid_data = [row for row in data_table if row[1]]
        return Common.generate_xml_table(valid_data, table_style="borders:TRBL;width-cols:8")

    @staticmethod
    def create_table_detailed_configuration(data):
        """Crea una tabella con il riepilogo dei sottocampi: moduli, stringhe e inverter."""

        subfields_primary = data.get("generator", {})
        subfields_data = data.get("sizing", {})
        data_table = [["Sottocampo", "Tot. Moduli", "N. Stringhe", "N. Inverter"]]

        total_modules = 0
        total_strings = 0
        total_inverters = 0

        for section in subfields_data.values():
            for key_name, subfield in section.items():
                n_mod = subfield.get("n_modules", 0)
                n_str = subfield.get("n_strings", 0)
                n_inv = subfield.get("n_inverters", 0)

                total_modules += n_mod
                total_strings += n_str
                total_inverters += n_inv

                # stampo i singoli sottocampi solo se devo stampare il progetto
                # escludo serie B (agrivoltaico) per la quale non stampo il report progetto ma solo distinta
                if data.get("print_report", True):
                    data_table.append([
                        f"{key_name}",
                        f"{n_mod}",
                        f"{n_str}",
                        f"{n_inv}"
                    ])

        # Aggiunta riga finale con i totali
        data_table.append([
            "Totale",
            f"{total_modules}",
            f"{total_strings}",
            f"{total_inverters}"
        ])
        return Common.generate_xml_table(data_table, table_style="borders:TRBL;column-alignments:L-C-C-C;")

    @staticmethod
    def create_table_economic_feasibility(data):
        """Crea la tabella relativa alla convenienza economica-finanziaria."""

        ecofin = data.get('ecofin', {})

        if data['storage'] == "1":
            roi_value = ecofin.get('roi_with_storage')
            pbp_value = ecofin.get('payback_period_with_storage')
            revenues = ecofin.get('yearly_total_revenues_with_storage', [])
            lifetime_revenues = ecofin.get('total_revenue_lifetime_with_storage')
            gianetto = ecofin.get('cumulative_cashflow_with_storage', [])
        else:
            roi_value = ecofin.get('roi_without_storage')
            pbp_value = ecofin.get('payback_period_without_storage')
            revenues = ecofin.get('yearly_total_revenues_without_storage', [])
            lifetime_revenues = ecofin.get('total_revenue_lifetime_without_storage')
            gianetto = ecofin.get('cumulative_cashflow_without_storage', [])

        rev_first_value = revenues[0] if revenues else 0
        gianetto_value = gianetto[-1] if gianetto else 0

        roi = f"{roi_value:.0f}%" if roi_value is not None else ""
        payback_period = f"{pbp_value:.0f}" if pbp_value is not None else ""
        rev_first_year = f"{rev_first_value:.0f} €/primo anno" if rev_first_value is not None else ""
        revenues_str = f"{lifetime_revenues:.0f} €" if lifetime_revenues is not None else ""
        gianetto_str = f"{gianetto_value:.0f} €" if gianetto_value is not None else ""

        rows = [
            ["Ricavi primo anno (risparmio + ev. vendite + ev. incentivi)", rev_first_year],
            ["Payback Period", payback_period],
            ["ROI (Return on Investment)", roi],
            ["Ricavi in 25 anni (entrate + risparmi)", revenues_str],
            ["Guadagno netto in 25 anni = entrate meno investimento iniziale e costi di esercizio", gianetto_str],
        ]
        valid_data = [row for row in rows if row[1]]
        return Common.generate_xml_table(valid_data, table_style="borders:TRBL;width-cols:12")

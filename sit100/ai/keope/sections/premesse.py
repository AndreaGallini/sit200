"""
premesse.py
Classe che gestisce la costruzione delle stringhe xml relative alle premesse.
Le premesse includono i capitoli da inizio progetto fino a calcolatore solare.
"""
from lxml import etree

from ..params import SYSTEM_PURPOSE_LONG, POSITION, SYSTEM_PURPOSE_SHORT, GRID_CONNECTED, SELF_CONSUMPTION, RID
from .common import Common


class Premesse:

    def __init__(self, data):
        self.data = data

    def create_intervention_scope(self):
        """X1: Crea una stringa XML che descrive lo scopo dell'installazione, se presente nei dati."""

        intervention_scope = self.data.get(
            "general_data", {}).get("intervention_scope", "")
        if intervention_scope:
            text_node = etree.Element("text")
            text_node.text = f"L’intervento proposto è sviluppato nell’ambito del seguente " \
                f"strumento di promozione del fotovoltaico:\n{intervention_scope}"
            return Common.generate_string_xml(text_node)
        else:
            return ""

    def create_plant_purpose(self):
        """X2: Crea una stringa XML che descrive la finalità dell'installazione, se presente nei dati."""

        system_purpose = self.data.get("plant_scope", "")
        if system_purpose:
            text_node = etree.Element("text")
            text_node.text = f"{SYSTEM_PURPOSE_LONG[system_purpose]}"
            return Common.generate_string_xml(text_node)
        else:
            return ""

    def create_main_feature_table(self):
        """X3: Genera una stringa XML per la tabella delle principali caratteristiche dell'impianto."""

        generator_power = f"{self.data.get('generator_power', '')} kWp"
        data = [
            ["Potenza nominale totale dell'impianto", generator_power],
            ["Numero di aree di installazione", self.data.get('n_fields_str', '')],
            ["Aree di installazione", self.data.get('subfields_str', '')],
            ["Superficie totale disponibile per l'installazione", self.data.get("total_area_str", "")],
            ["Potenza unitaria per singolo modulo", f"{self.data.get('single_module_power', '')} W"],
            ["Posizionamento dei moduli", POSITION.get(self.data.get('mounting'), "")],
            ["Tipologia di connessione alla rete", GRID_CONNECTED.get(self.data.get('grid_connected'), "")],
            ["Energia venduta alla rete", RID.get(self.data.get('rid'), "")],
            ["Autoconsumo", SELF_CONSUMPTION.get(self.data.get('self_consumption'), "")],
            ["Utilizzo dell'energia", SYSTEM_PURPOSE_SHORT.get(self.data.get('plant_scope'), "")],
        ]
        valid_data = [row for row in data if row[1]]
        table = Common.generate_xml_table(valid_data, table_style="borders:TB")

        return Common.generate_string_xml(table)

    def create_project_team(self):
        """X4: Crea una stringa XML che descrive la tabella committente, proponente, responsabile."""

        client = self.data.get("long_client", "")
        proposer = self.data.get("long_proposer", "")
        designers = self.data.get('designers_details', '')

        table = etree.Element(
            "table", style="borders:TB;font-style:BI-N;width-cols:5")

        row_client = etree.SubElement(table, "row")
        etree.SubElement(row_client, "cell").text = "Committente"
        etree.SubElement(row_client, "cell").text = client

        if proposer:
            row_proposer = etree.SubElement(table, "row")
            etree.SubElement(row_proposer, "cell").text = "Proponente"
            etree.SubElement(row_proposer, "cell").text = proposer

        if designers:
            row_designers = etree.SubElement(table, "row")
            etree.SubElement(row_designers, "cell").text = "Progettazione tecnica"
            etree.SubElement(row_designers, "cell").text = designers

        return Common.generate_string_xml(table)

    def create_plant_location(self):
        """X5: Crea una stringa XML che descrive la tabella della localizzazione dell'impianto."""

        location = self.data.get("plant_address", "")
        cadastral_references = self.data.get("general_data", {}).get("cadastral_references", "")
        latitude = self.data.get("latitude_str", "")
        longitude = self.data.get("longitude_str", "")
        altitude = self.data.get("altitude_str", "")

        table = etree.Element("table", style="borders:TB;width-cols:5;space-after:1")

        row1 = etree.SubElement(table, "row")
        etree.SubElement(row1, "cell").text = "Località"
        etree.SubElement(row1, "cell").text = location

        row2 = etree.SubElement(table, "row")
        etree.SubElement(row2, "cell").text = "Coordinate geografiche WGS84"
        etree.SubElement(row2,
                         "cell").text = f"Latitudine: {latitude}\nLongitudine: {longitude}\nAltitudine: {altitude}"

        if cadastral_references:
            row3 = etree.SubElement(table, "row")
            etree.SubElement(row3, "cell").text = "Riferimenti catastali"
            etree.SubElement(row3, "cell").text = cadastral_references

        return Common.generate_string_xml(table)

    def create_plant_logistics(self):
        """X7: Restituisce la stringa XML con le informazioni sul sito, se presenti."""

        site_information = self.data.get("general_data", {}).get("site_information", "")

        if site_information:
            text_node = etree.Element("text")
            text_node.text = site_information
            return Common.generate_string_xml(text_node)
        else:
            return ''

    def create_image_location(self):
        """X6: Genera una stringa XML per l'immagine della mappa, se disponibile."""

        map_images = self.data.get('map_images', [])

        if map_images:
            map_image = map_images[0]
            image_node = etree.Element("image", src=map_image, style="center")
            caption_node = etree.SubElement(image_node, "caption")
            caption_node.text = "Area di localizzazione dell'impianto fotovoltaico."
            return Common.generate_string_xml(image_node)
        else:
            return ""

    def create_image_marker_cicle(self):
        """Genera una stringa XML per l'immagine del cerchio sull'area della mappa, se disponibile."""

        map_images = self.data.get('map_images', [])

        if map_images:
            map_image = map_images[1]
            image_node = etree.Element("image", src=map_image, style="center")
            caption_node = etree.SubElement(image_node, "caption")
            caption_node.text = "Ubicazione dell’impianto fotovoltaico."
            return Common.generate_string_xml(image_node)
        else:
            return ""

    def create_image_polygon(self):
        """Genera una stringa XML per le immagini dei poligoni sulla mappa per ogni sottocampo, se disponibili."""

        map_images = self.data.get('map_images', [])
        if map_images and len(map_images) > 2:
            # map_images[2] ora contiene un dizionario delle immagini per ogni sottocampo
            subfield_maps = map_images[2]

            if isinstance(subfield_maps, dict) and subfield_maps:
                # Ottieni i dati del generator per i nomi dei sottocampi
                generator = self.data.get('generator', {})

                # Crea una sezione per ogni immagine di sottocampo
                xml_sections = []

                # Ordina i sottocampi per una presentazione coerente
                sorted_subfields = sorted(subfield_maps.keys())

                for subfield_name in sorted_subfields:
                    subfield_image_path = subfield_maps[subfield_name]

                    if subfield_image_path:  # Solo se il percorso dell'immagine non è vuoto
                        # Cerca il nome personalizzato del sottocampo nel generator
                        user_subfield_name = ""
                        for field_name, field_data in generator.items():
                            if subfield_name in field_data:
                                user_subfield_name = field_data[subfield_name].get('name', '')
                                break

                        # Crea l'elemento immagine
                        image_node = etree.Element(
                            "image", src=subfield_image_path, style="center")
                        caption_node = etree.SubElement(image_node, "caption")

                        # Crea la didascalia con il formato richiesto
                        if user_subfield_name:
                            caption_node.text = \
                                f"Posizionamento del campo fotovoltaico - Campo {subfield_name} ({user_subfield_name})"
                        else:
                            caption_node.text = \
                                f"Posizionamento del campo fotovoltaico - Campo {subfield_name}"

                        xml_sections.append(Common.generate_string_xml(image_node))

                return "\n".join(xml_sections)
        return ""

    def create_subfields_arrangement(self):
        """X9a: Descrizione di come sono strutturati i sottocampi."""

        generator = self.data.get('generator', {})

        tag_node = etree.Element('tag_to_remove')
        
        # <text> introduttiva
        n_fields = len(generator)
        text_node = etree.SubElement(tag_node, "text")
        # , installati su
        # L'impianto fotovoltaico è installato sulla falda del tetto dell’edificio.
        # La copertura sarà complanare alla pendenza della falda.
        if n_fields == 1:
            text_node.text = f"L’impianto fotovoltaico è organizzato in 1 campo principali:"
        else:
            text_node.text = f"L’impianto fotovoltaico è suddiviso in {n_fields} campi principali:"

        for field_label, fields in generator.items():
            n_fields = len(fields)
            subfield_text = "sottocampo" if n_fields == 1 else "sottocampi"

            txt_main = etree.SubElement(tag_node, "text")
            txt_main.text = f"Campo {field_label} è composto da {n_fields} {subfield_text}:"

            ul_sub = etree.SubElement(tag_node, "ul")

            for sub_label, data in fields.items():
                name = data.get("name", "").strip()

                # Conversione orientamento (azimut da nord → rispetto al sud)
                orientation = data.get("orientation")
                if orientation is not None:
                    azimuth_relative_to_south = orientation - 180
                    if azimuth_relative_to_south > 180:
                        azimuth_relative_to_south -= 360
                    elif azimuth_relative_to_south < -180:
                        azimuth_relative_to_south += 360

                    sign = "+" if azimuth_relative_to_south > 0 else ""
                    orientation_text = f"{sign}{azimuth_relative_to_south}° rispetto al sud"
                    desc = f"{sub_label} ({name}, orientato a {orientation_text})"
                else:
                    desc = f"{sub_label} ({name})"

                etree.SubElement(ul_sub, "li").text = desc

        empty_line = etree.Element('empty-line')
        tag_node.append(empty_line)

        string = Common.generate_string_xml(tag_node)

        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_dashboard_executive_summary_table(self):
        """X11: Genera una stringa XML per la tabella composta dal dashboard dell'esecutive summary."""

        generator_power = self.data.get('generator_power', '')
        total_energy_production = self.data.get('ao1', {}).get("total_energy_production")
        sf = self.data.get('ao1', {}).get('range_specific_producibility', '')
        subfields_specific = sf.replace("kWh/kWp", "")

        ecofin = self.data.get('ecofin', {})
        if self.data.get("storage") == "1":
            roi_value = ecofin.get('roi_with_storage')
            pbp_value = ecofin.get('payback_period_with_storage')
            revenues = ecofin.get('yearly_total_revenues_with_storage', [])
        else:
            roi_value = ecofin.get('roi_without_storage')
            pbp_value = ecofin.get('payback_period_without_storage')
            revenues = ecofin.get('yearly_total_revenues_without_storage', [])

        rev_first_value = revenues[0] if revenues else 0

        total_energy_production = f"{total_energy_production:.0f}" if total_energy_production is not None else ""

        roi = f"{roi_value:.0f}%" if roi_value is not None else ""
        payback_period = f"{pbp_value:.0f}" if pbp_value is not None else ""
        rev_first_year = f"{rev_first_value:.0f}" if rev_first_value is not None else ""

        tag_node = etree.Element('tag_to_remove')

        data = [[generator_power, total_energy_production, subfields_specific]]
        valid_data = [row for row in data if row[1]]
        table = Common.generate_xml_table(valid_data, table_style="borders:T;font-size:30;column-alignments:C-C-C;")
        tag_node.append(table)

        data = [[
            'kW\nPotenza nominale di picco',
            "kWh/anno\nProduzione annua di energia elettrica",
            'kWk/kWp\nProducibilità annuale specifica'
        ]]
        valid_data = [row for row in data if row[1]]
        table = Common.generate_xml_table(valid_data, table_style="column-alignments:C-C-C;")
        tag_node.append(table)

        data = [[payback_period, roi, rev_first_year]]
        valid_data = [row for row in data if row[1]]
        table = Common.generate_xml_table(valid_data, table_style="borders:T;font-size:30;column-alignments:C-C-C;")
        tag_node.append(table)

        data = [[
            'anni\nPayback Period',
            "ROI\nRitorno dell'investimento",
            '€/anno\nRicavi + risparmio, primo anno'
        ]]
        valid_data = [row for row in data if row[1]]
        table = Common.generate_xml_table(valid_data, table_style="borders:B;column-alignments:C-C-C;")
        tag_node.append(table)

        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_general_description_table(self):
        """X12: Genera una stringa XML per la tabella composta della descrizione generale dell'impianto."""

        tag_node = etree.Element('tag_to_remove')

        tables_data = [
            ([['LOCALITÀ DI INSTALLAZIONE']], "borders:TRBL;column-alignments:C;"),
            ([['CARATTERISTICHE DEL GENERATORE FOTOVOLTAICO']], "borders:TRBL;column-alignments:C"),
            ([['ENERGIA SOLARE E PRODUCIBILITÀ']], "borders:TRBL;column-alignments:C"),
            ([['COMPONENTI E CONFIGURAZIONE']], "borders:TRBL;column-alignments:C"),
            ([['CONFIGURAZIONE DEL GENERATORE FOTOVOLTAICO']], "borders:TRBL;column-alignments:C"),
        ]

        # località di installazione
        tag_node.append(Common.generate_xml_table(*tables_data[0]))
        tag_node.append(Common.create_table_location(self.data))
        # caratteristiche del generatore fotovoltaico
        tag_node.append(Common.generate_xml_table(*tables_data[1]))
        tag_node.append(Common.create_table_base_features_generator(self.data))
        # energia solare e producibilità
        tag_node.append(Common.generate_xml_table(*tables_data[2]))
        tag_node.append(Common.create_table_solar_produciblity(self.data))
        # componenti e configurazione
        tag_node.append(Common.generate_xml_table(*tables_data[3]))
        tag_node.append(Common.create_table_components_configuration(self.data))
        # linea vuota
        empty_line = etree.Element('empty-line')
        tag_node.append(empty_line)
        # componenti e configurazione
        tag_node.append(Common.generate_xml_table(*tables_data[4]))
        tag_node.append(Common.create_table_detailed_configuration(self.data))

        # finalizzazione
        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_economic_convenience_table(self):
        """X13: Genera una stringa XML per la tabella della convenienza economica."""

        tag_node = etree.Element('tag_to_remove')

        tag_node.append(Common.generate_xml_table([['CONVENIENZA ECONOMICA']], "borders:TRBL;column-alignments:C;"))
        tag_node.append(Common.create_table_economic_feasibility(self.data))

        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_location_solar_table(self):
        """X14: Genera una stringa XML per la tabella composta dai dati di location e solari."""

        tag_node = etree.Element('tag_to_remove')

        tables_data = [
            ([['LOCALITÀ DI INSTALLAZIONE']], "borders:TRBL;column-alignments:C;"),
            ([['ENERGIA SOLARE E PRODUCIBILITÀ']], "borders:TRBL;column-alignments:C"),
        ]

        # località di installazione
        tag_node.append(Common.generate_xml_table(*tables_data[0]))
        tag_node.append(Common.create_table_location(self.data))
        # energia solare e producibilità
        tag_node.append(Common.generate_xml_table(*tables_data[1]))
        tag_node.append(Common.create_table_solar_produciblity(self.data))

        # finalizzazione
        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

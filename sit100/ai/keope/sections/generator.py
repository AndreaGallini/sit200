"""
generator.py
Classe che gestisce la costruzione delle stringhe xml relative al generatore fotovoltaico.
"""
from lxml import etree

from .common import Common


class Generator:

    def __init__(self, data):
        self.data = data

    def create_image_plant_layout(self):
        """X70: Crea immagini layouts"""

        sizing = self.data.get('sizing', {})

        # Raccoglie tutte le immagini di layout
        all_images_xml = []
        
        for field_name, field_data in sizing.items():
            # field_data è un dizionario, non una lista
            for subfield_name, subfield_data in field_data.items():
                image = subfield_data.get('layout_png')
                if image:
                    image_node = etree.Element("image", src=image, style="center")
                    caption_node = etree.SubElement(image_node, "caption")
                    caption_node.text = f"Configurazione del layout dell'impianto fotovoltaico - Sottocampo {subfield_name}."
                    all_images_xml.append(Common.generate_string_xml(image_node))

        # Restituisce tutte le immagini concatenate
        return "\n".join(all_images_xml) if all_images_xml else ""

    def create_technical_features_table(self):
        """X71: Genera una stringa XML per la tabella composta della descrizione generale dell'impianto."""

        tag_node = etree.Element('tag_to_remove')

        tables_data = [
            ([['CARATTERISTICHE DEL GENERATORE FOTOVOLTAICO']], "borders:TRBL;column-alignments:C"),
            ([['ENERGIA SOLARE E PRODUCIBILITÀ']], "borders:TRBL;column-alignments:C"),
            ([['COMPONENTI E CONFIGURAZIONE']], "borders:TRBL;column-alignments:C"),
        ]

        # caratteristiche del generatore fotovoltaico
        tag_node.append(Common.generate_xml_table(*tables_data[0]))
        tag_node.append(Common.create_table_base_features_generator(self.data))
        # energia solare e producibilità
        tag_node.append(Common.generate_xml_table(*tables_data[1]))
        tag_node.append(Common.create_table_solar_produciblity(self.data))
        # componenti e configurazione
        tag_node.append(Common.generate_xml_table(*tables_data[2]))
        tag_node.append(Common.create_table_components_configuration(self.data))
        # finalizzazione
        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_technical_configuration_table(self):
        """X72: Genera una stringa XML per la tabella composta della descrizione generale dell'impianto."""

        tag_node = etree.Element('tag_to_remove')

        tables_data = [
            ([['CARATTERISTICHE DEL GENERATORE FOTOVOLTAICO']], "borders:TRBL;column-alignments:C"),
            ([['COMPONENTI E CONFIGURAZIONE']], "borders:TRBL;column-alignments:C"),
            ([['CONFIGURAZIONE DEL GENERATORE FOTOVOLTAICO']], "borders:TRBL;column-alignments:C"),
        ]

        # caratteristiche del generatore fotovoltaico
        tag_node.append(Common.generate_xml_table(*tables_data[0]))
        tag_node.append(Common.create_table_base_features_generator(self.data))
        # componenti e configurazione
        tag_node.append(Common.generate_xml_table(*tables_data[1]))
        tag_node.append(Common.create_table_components_configuration(self.data))
        # linea vuota
        empty_line = etree.Element('empty-line')
        tag_node.append(empty_line)
        # componenti e configurazione
        tag_node.append(Common.generate_xml_table(*tables_data[2]))
        tag_node.append(Common.create_table_detailed_configuration(self.data))

        # finalizzazione
        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

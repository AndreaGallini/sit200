"""
CLasse che compila un template xml di progetto.
Sostituisce i placeholder con valori singoli o nodi xml.
"""

from lxml import etree

from .sections.common import Common
from .t3_composer import T3Composer
from .pv_design_composer import PvDesignComposer


class XMLCompiler:

    def __init__(self, data, string_placeholders, xml_placeholders):
        self.data = data
        self.string_placeholders = string_placeholders
        self.xml_placeholders = xml_placeholders
        self.xml_template = None
        self.xml_pv_design_template = None
        self.create_xml_templates()

    def create_xml_templates(self):
        self.get_xml_t3()
        self.get_xml_design()

    def get_xml_t3(self):
        """Genera il template T3."""
        component_ids = self.data.get('component_ids')
        generator_power = self.data.get('generator_power')
        fv_position = self.data.get('mounting')
        has_storage = False if self.data.get('storage') == '0' else True
        grid_connected = 1 if self.data.get('grid_connected') == '1' else 9

        composer = T3Composer(component_ids, has_storage, generator_power, fv_position, grid_connected)
        self.xml_template = composer.processing()

    def get_xml_design(self):
        """Genera il template XMl della Distinta Base di Configurazione dell'impianto fotovoltaico."""
        composer = PvDesignComposer()
        self.xml_pv_design_template = composer.processing()

    def replace_string_placeholders(self, element, replacements):
        """Sostituisce i placeholder nel testo di un elemento e nei suoi figli."""

        # Verifica se l'elemento ha del testo con placeholder
        if element.text:
            for placeholder, value in replacements.items():
                placeholder_tag = f"{{{{{placeholder}}}}}"
                if placeholder_tag in element.text:
                    if self.is_xml(value):
                        # Se il valore è un pezzo di XML, lo convertiamo in un nodo
                        new_element = etree.fromstring(value)
                        # Dividiamo il testo attuale prima e dopo il segnaposto
                        parts = element.text.split(placeholder_tag, 1)
                        # Modifichiamo l'elemento corrente, chiudendo il primo blocco di testo
                        element.text = parts[0]
                        # Aggiungiamo il nuovo nodo XML
                        element.addnext(new_element)
                        # Se c'è altro testo dopo il segnaposto, lo inseriamo nel tail
                        if len(parts) > 1 and parts[1].strip():
                            new_element.tail = parts[1]
                    else:
                        # Sostituzione semplice di testo
                        element.text = element.text.replace(
                            placeholder_tag, value)

        # Ricorri nei figli dell'elemento
        for child in list(element):
            self.replace_string_placeholders(child, replacements)

        # Gestisci i placeholder nel tail
        if element.tail:
            for placeholder, value in replacements.items():
                placeholder_tag = f"{{{{{placeholder}}}}}"
                if placeholder_tag in element.tail:
                    if self.is_xml(value):
                        new_element = etree.fromstring(value)
                        parts = element.tail.split(placeholder_tag, 1)
                        element.tail = parts[0]
                        element.addnext(new_element)
                        if len(parts) > 1 and parts[1].strip():
                            new_element.tail = parts[1]
                    else:
                        element.tail = element.tail.replace(
                            placeholder_tag, value)

    @staticmethod
    def is_xml(string):
        """Verifica se una stringa è un pezzo di XML valido."""

        try:
            etree.fromstring(string)
            return True
        except etree.XMLSyntaxError:
            return False

    @staticmethod
    def replace_xml_placeholders(root, replacements):
        """Sostituisce tutti i placeholder nel documento XML con i contenuti forniti in un dizionario."""

        for placeholder_node in root.xpath("//placeholder"):
            placeholder_name = placeholder_node.get("name")

            if placeholder_name in replacements:
                # Crea i nuovi nodi da inserire
                replacement_nodes = etree.fromstring(
                    f"<wrapper>{replacements[placeholder_name]}</wrapper>")
                parent = placeholder_node.getparent()
                index = parent.index(placeholder_node)

                # Inserisce i nuovi nodi al posto del placeholder
                for node in replacement_nodes:
                    parent.insert(index, node)
                    index += 1

                # Rimuove il nodo <placeholder>
                parent.remove(placeholder_node)

        return root

    def create_final_project_xml_string(self):
        """Crea il xml del progetto sostituendo tutti i placeholder."""

        if not self.xml_template:
            return ""

        # Converti la stringa XML in bytes per evitare l'errore di encoding
        # xml_bytes = self.xml_template.encode('utf-8')
        # Parse l'XML esistente con lxml
        # parser = etree.XMLParser(remove_blank_text=True)
        # root = etree.fromstring(xml_bytes, parser)
        # Carica il contenuto XML in un albero XML
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.XML(self.xml_template.encode('utf-8'), parser)

        # Sostituisci i placeholder in formato stringa
        self.replace_string_placeholders(root, self.string_placeholders)
        # Sostituisci i placeholder in formato xml string
        updated_root = self.replace_xml_placeholders(root, self.xml_placeholders)
        # print(etree.tostring(updated_root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8'))
        # Converti l'XML modificato in stringa

        return Common.generate_string_xml(updated_root)

    def create_final_design_xml_string(self):
        """Crea il xml della distinta base di configurazione dell'impianto sostituendo tutti i placeholder."""
        if not self.xml_pv_design_template:
            return ""

        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.XML(self.xml_pv_design_template.encode('utf-8'), parser)

        # Sostituisci i placeholder in formato stringa
        self.replace_string_placeholders(root, self.string_placeholders)
        # Sostituisci i placeholder in formato xml string
        updated_root = self.replace_xml_placeholders(root, self.xml_placeholders)
        # Converti l'XML modificato in stringa

        return Common.generate_string_xml(updated_root)

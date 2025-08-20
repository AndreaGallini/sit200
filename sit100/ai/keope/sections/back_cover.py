"""
Classe per costruire la back cover page del progetto in formato xml
"""
from lxml import etree

from .common import Common


class BackCoverGenerator:

    def __init__(self, data):
        self.data = data
        self.main_node = etree.Element("back-cover")

    def create_client_proposer_section(self):
        """Logica per creare la sezione committente e proponente."""

        client = self.data.get('long_client', '').strip()
        proposer = self.data.get("long_proposer", '').strip()

        table = etree.SubElement(self.main_node, "table", position="client")
        table.set("style", "borders:TB;space-after:1")

        if proposer:
            Common.add_row_to_table(table, ["Committente", "Proponente"])
            Common.add_row_to_table(table, [client, proposer])
        else:
            Common.add_row_to_table(table, ["Committente"])
            Common.add_row_to_table(table, [client])

        return table

    def create_designer_section(self):
        """Logica per creare la sezione progettazione tecnica."""

        table = etree.SubElement(self.main_node, "table", position="designer")
        table.set("style", "borders:TB")

        Common.add_row_to_table(table, ["Progettazione tecnica", ""])
        designers_details = self.data.get('designers_details', '')
        designers = self.data.get("designers_names", '')
        collaborators = self.data.get("collaborators_names", '')
        Common.add_row_to_table(table, [designers_details, "Progettista(i):\n"+designers+"\n\n"+"Collaboratori:\n" + collaborators])

        return table

    def generate_back_cover_page(self):
        """Genera il nodo "cover-page" che è la copertina di progetto. Il nodo è xml in formato stringa."""

        try:
            sections = [
                ('title', Common.create_title_section(self.main_node, self.data)),
                ('location', Common.create_location_section(self.main_node, self.data)),
                ('doc_type', Common.create_document_type_section(self.main_node, self.data)),
                ('client', self.create_client_proposer_section()),
                ('designer', self.create_designer_section()),
            ]

            for section_name, section in sections:
                if section is None:
                    print(
                        f"Errore nella generazione della sezione {section_name}. "
                        f"La back-cover-page non è stata creata correttamente.")

            return etree.tostring(self.main_node, pretty_print=True, encoding='utf-8').decode('utf-8')

        except Exception as e:
            # logger.error(f"Errore durante la generazione della copertina: {e}")
            return ""

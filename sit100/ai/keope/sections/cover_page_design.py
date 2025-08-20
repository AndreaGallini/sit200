"""
Classe per costruire la cover page della distinta base di configurazione in formato xml
"""
from lxml import etree

from .common import Common


class CoverPageDesignGenerator:

    def __init__(self, data):
        self.data = data
        self.cover_page_node = etree.Element("design-cover-page")

    def generate_cover_page(self):
        """Genera il nodo "cover-page" che è la copertina di progetto. Il nodo è xml in formato stringa utf-8."""

        sections = [
            ('h0', Common.create_design_title_section(self.cover_page_node, self.data)),
            ('title', Common.create_title_section(self.cover_page_node, self.data)),
            ('location', Common.create_location_section(self.cover_page_node, self.data)),
            ('today', Common.create_today_date_section(self.cover_page_node, self.data)),
        ]

        for section_name, section in sections:
            if section is None:
                print(
                    f"Errore nella generazione della sezione {section_name}. "
                    f"La cover page non è stata creata correttamente.")

        return Common.generate_string_xml(self.cover_page_node)

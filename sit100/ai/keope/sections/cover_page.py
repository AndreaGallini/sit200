"""
Classe per costruire la cover page del progetto in formato xml
"""
from lxml import etree

from .common import Common


class CoverPageGenerator:

    def __init__(self, data):
        self.data = data
        self.cover_page_node = etree.Element("cover-page")

    def create_header_logos_section(self):
        """Logica per creare la sezione dei loghi: tabella XML di una riga contenente i path dei loghi."""

        logos = self.data.get("cover_logos")
        if logos:
            table = etree.SubElement(self.cover_page_node, "table", position="logos")
            row = etree.SubElement(table, "row")
            for image_path in logos[:3]:
                cell = etree.SubElement(row, "cell")
                etree.SubElement(cell, "image", src=image_path)
            return table
        else:
            etree.SubElement(self.cover_page_node, "empty-line")
            etree.SubElement(self.cover_page_node, "empty-line")
            return ""

    def create_cover_image_section(self):
        """Logica per creare la sezione immagine di copertina."""

        cover_image_path = self.data.get("cover_image")
        if cover_image_path:
            image = etree.SubElement(self.cover_page_node, "image", src=cover_image_path)
            image.set("position", "after_title")
            return image
        else:
            etree.SubElement(self.cover_page_node, "empty-line")
            etree.SubElement(self.cover_page_node, "empty-line")
            return ""

    def create_stakeholders_section(self):
        """Logica per creare la sezione committente e progettisti."""

        client = self.data.get("short_client", '')
        designers = self.data.get("designers_names", '')

        table = etree.SubElement(self.cover_page_node, "table", position="project_team")
        table.set("style", "borders:TB;space-after:1")

        rows = [
            ["Committente", "Progettista(i)", "Timbro"],
            [client, designers, ""]
        ]

        for row_data in rows:
            row = etree.SubElement(table, "row")
            for cell_data in row_data:
                cell = etree.SubElement(row, "cell")
                cell.text = cell_data

        return table

    def generate_cover_page(self):
        """Genera il nodo "cover-page" che è la copertina di progetto. Il nodo è xml in formato stringa utf-8."""

        sections = [
            ('loghi', self.create_header_logos_section()),
            ('title', Common.create_title_section(self.cover_page_node, self.data)),
            ('cover_image', self.create_cover_image_section()),
            ('location', Common.create_location_section(self.cover_page_node, self.data)),
            ('doc_type', Common.create_document_type_section(self.cover_page_node, self.data)),
            ('stakeholders', self.create_stakeholders_section()),
            ('revision', Common.create_revision_section(self.cover_page_node, self.data)),
            ('file_references', Common.create_file_references_section(self.cover_page_node, self.data)),
        ]

        for section_name, section in sections:
            if section is None:
                print(
                    f"Errore nella generazione della sezione {section_name}. "
                    f"La cover page non è stata creata correttamente.")

        return Common.generate_string_xml(self.cover_page_node)

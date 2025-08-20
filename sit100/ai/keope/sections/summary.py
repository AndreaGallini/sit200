"""
Classe per costruire l'indice dei capitoli del progetto in formato xml
"""
from lxml import etree

from .common import Common


class SummaryGenerator:

    def __init__(self, data):
        self.data = data
        self.summary_node = etree.Element("summary")

        # Lista base dei titoli dei capitoli
        self.base_chapter_titles = [
            "Premesse",
            "Definizioni",
            "Normativa di riferimento",
            "Sito di installazione",
            "Quadro ambientale",
            "Executive summary",
            "Calcolatore solare",
            "Perdite",
            "Producibilità",
            "Riduzione delle emissioni",
            "Generatore fotovoltaico",
            "Moduli fotovoltaici",
            "Strutture di supporto",
            "Inverter",
            "Cavi",
            "Quadri elettrici",
            "Impianto di messa a terra",
            "Protezione",
            "Verifiche",
            "Collaudo",
            "Messa in esercizio",
            "Dismissione",
            "Analisi finanziaria e convenienza economica",
            "Conclusione",
            "Schema unifilare"
        ]

    def get_dynamic_chapter_titles(self):
        """Genera la lista dinamica dei capitoli in base ai dati ricevuti"""
        chapter_titles = self.base_chapter_titles.copy()

        # Aggiungi "Sistema di accumulo" se storage è '1'
        if self.data.get('storage') == '1':
            # Inserisci "Sistema di accumulo" dopo "Inverter"
            inverter_index = chapter_titles.index("Inverter")
            chapter_titles.insert(inverter_index + 1, "Sistema di accumulo")

        # Aggiungi "Sistema di collegamento alla rete" se grid_connected è '1'
        if self.data.get('grid_connected') == '1':
            # Inserisci "Sistema di collegamento alla rete" dopo "Protezione"
            protezione_index = chapter_titles.index("Protezione")
            chapter_titles.insert(protezione_index + 1,
                                  "Sistema di collegamento alla rete")

        # Aggiungi "Pvgis" se pvgis non è un oggetto vuoto
        pvgis_data = self.data.get('pvgis', {})
        if pvgis_data and isinstance(pvgis_data, dict) and pvgis_data:
            # Inserisci "Pvgis" dopo "Producibilità"
            producibilita_index = chapter_titles.index("Producibilità")
            chapter_titles.insert(producibilita_index + 1, "Pvgis")

        return chapter_titles

    def create_chapters_list(self):
        """Crea la lista dei capitoli numerata in base al numero di chapter_titles."""

        # Ottieni la lista dinamica dei capitoli
        chapter_titles = self.get_dynamic_chapter_titles()

        # Aggiungi una riga vuota prima della lista
        etree.SubElement(self.summary_node, "empty-line")

        # Crea una lista numerata in base al numero di chapter_titles
        for index, chapter_title in enumerate(chapter_titles, 1):
            text = etree.SubElement(self.summary_node, "text")
            text.text = f"{index}. {chapter_title}"

        return True

    def generate_summary(self):
        """Genera il nodo 'summary' che contiene l'indice dei capitoli. 
        Il nodo è xml in formato stringa utf-8."""

        sections = [
            ('chapters_list', self.create_chapters_list()),
        ]

        for section_name, section in sections:
            if section is None:
                print(
                    f"Errore nella generazione della sezione {section_name}.")

        xml_string = Common.generate_string_xml(self.summary_node)
        return xml_string

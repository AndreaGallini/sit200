import logging

from lxml import etree

logger = logging.getLogger('django')


class PvDesignComposer:
    """
    Compone l'XML della distinta base di configurazione dell'impianto fotovoltaico.
    """

    def __init__(self):
        self.component_chapters = ['module', 'support', 'inverter', 'storage']
        self.chapters = {}
        self.root = None
        self.chapters_node = None

    def initialize_root(self):
        """Crea la root del xml e il nodo chapters."""
        self.root = etree.Element("document")
        etree.SubElement(self.root, "placeholder", name="design-meta")
        etree.SubElement(self.root, "placeholder", name="design-cover-page")
        self.chapters_node = etree.SubElement(self.root, "chapters")

    def _solar_radiation_chapter(self):
        xml_string = ('<chapter>'
                      '<h1>Irraggiamento solare e produzione</h1>'
                      '<title>Irradiazione solare giornaliera orizzontale</title>'
                      '<placeholder name="X20"/><empty-line/>'
                      '<title>Energia irraggiata annua sul piano dei moduli</title>'
                      '<placeholder name="X23"/><empty-line/>'
                      '<title>Producibilità e produzione energetica annuale</title>'
                      '<placeholder name="X53"/>'
                      '</chapter>'
                      )
        chapter_xml = etree.fromstring(xml_string)
        self.chapters_node.append(chapter_xml)

    def _project_data_chapter(self):
        xml_string = ('<chapter>'
                      '<h1>Generatore fotovoltaico</h1>'
                      '<title>Dati generali di progetto</title>'
                      '<placeholder name="X14"/><empty-line/>'
                      '<title>Distinta di configurazione</title>'
                      '<placeholder name="X72"/><empty-line/>'
                      '<title>Convenienza economica</title>'
                      '<placeholder name="X13"/>'
                      '</chapter>'
                      )
        chapter_xml = etree.fromstring(xml_string)
        self.chapters_node.append(chapter_xml)

    def get_string_final_xml(self):
        try:
            xml_string = etree.tostring(self.root,
                                        pretty_print=True,
                                        xml_declaration=True,
                                        encoding="utf-8").decode("utf-8")
            return xml_string
        except (TypeError, ValueError) as e:
            logger.error(f"Errore durante la generazione della stringa XML della distinta base: {e}")
            return ""

    def processing(self):
        """Crea xml della distinta base di configurazione dell'impianto."""

        # inizializza la root del documento
        self.initialize_root()
        # aggiunge i dati di irraggiamento e produzione
        self._solar_radiation_chapter()
        # aggiunge i dati di progetto (località, generatore, componenti, configurazione e convenienza)
        self._project_data_chapter()
        final_xml_string = self.get_string_final_xml()

        return final_xml_string

import logging

import lxml.etree
from lxml import etree
from django.db import connection

from .sections.datasheet import Datasheet

logger = logging.getLogger('django')


class T3Composer:

    def __init__(self, component_ids, has_storage, generator_power, fv_position, grid_connected):
        """Costruttore del composer"""

        # ATTENZIONE: potenza dell'impianto: fisso a 100 per poter estrarre i capitoli dal DB
        self.generator_power = 100 if generator_power > 100 else generator_power   # TODO: correggere con più potenza
        self.fv_position = fv_position
        self.component_ids = component_ids
        self.has_storage = has_storage
        self.grid_connected = grid_connected
        # Correzione: aggiunta virgola mancante dopo 'generator'
        self.universal_chapter_codes = [
            'premises', 'definitions', 'regulation', 'location', 'executive',
            'solar', 'losses', 'energy', 'emissions', 'generator', 'cables', 'e-panels', 'grounding', 'protections', 'generator',
            'grid', 'e-checks', 'testing', 'commissioning', 'decommissioning', 'feasibility', 'conclusion', 'sld']
        self.component_chapters = ['module', 'support', 'inverter', 'storage']
        self.chapters = {}
        self.root = None
        self.chapters_node = None

    @staticmethod
    def get_data_with_parameters(query, parameters):
        """Esegue una query parametrizzata e restituisce i risultati come lista di tuple."""
        with connection.cursor() as cursor:
            cursor.execute(query, parameters)
            rows = cursor.fetchall()
            if rows:
                columns = [desc[0] for desc in cursor.description]
                result = [dict(zip(columns, row)) for row in rows]
                return result
        return []

    @staticmethod
    def get_data(query):
        """Esegue una query senza parametri e restituisce i risultati come lista di tuple."""
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                columns = [desc[0] for desc in cursor.description]
                results = []
                for row in rows:
                    result = {}
                    for i, value in enumerate(row):
                        result[columns[i]] = value
                    results.append(result)
                return results
        return []

    def get_universal_chapters(self):
        query = """SELECT DISTINCT ON (chapter_code) *
                FROM chapter_universal
                WHERE chapter_code = ANY(%s)
                    AND min_power <= %s
                    AND max_power > %s
                    AND (grid = %s OR grid = 5)
                    AND EXISTS (
                    SELECT 1 FROM unnest(string_to_array(trim(both '"' from typo[1]::text), ',')) AS t
                    WHERE t = %s
                )
                ORDER BY chapter_code, RANDOM();"""
        result = self.get_data_with_parameters(
            query, (self.universal_chapter_codes, self.generator_power, self.generator_power, self.grid_connected, self.fv_position))

        chapters = {row['chapter_code']: row['xml'] for row in result}

        return chapters

    def get_component_chapters(self):
        compo_ids = self.component_ids['module'] + self.component_ids['inverter'] + \
            self.component_ids['storage'] + self.component_ids['support']

        query = "SELECT DISTINCT ON (component_id) * FROM chapter_component WHERE component_id = ANY(%s) ORDER BY component_id, RANDOM();"
        result = self.get_data_with_parameters(query, (compo_ids,))

        # Mappatura dei chapter_code ai nomi leggibili
        COMPONENT_TITLE_MAPPING = {
            'module': 'Moduli fotovoltaici',
            'inverter': 'Inverter',
            'storage': 'Sistema di accumulo',
            'support': 'Supporti'
        }

        chapters = {}
        ds = Datasheet({})

        for component_code, list_ids in self.component_ids.items():
            component_list = [d for d in result if d.get('component_id') in list_ids]
            # component_list è una lista di dizionari estratti dal db
            # list_ids è una lista id di un dato componente (es. module)

            chapter = etree.Element('chapter')
            title = etree.SubElement(chapter, 'h1')
            title.text = COMPONENT_TITLE_MAPPING.get(component_code)

            for row in component_list:
                component_id = row['component_id']

                xml_content = etree.fromstring(row['xml'])
                for child in xml_content:
                    chapter.append(child)

                images_str = ds.create_image_for_datasheet(component_id)
                if images_str:
                    wrapped_string = f"<root>{images_str}</root>"
                    imageroot = etree.fromstring(wrapped_string)
                    for image_node in imageroot:
                        chapter.append(image_node)

            chapter_str = etree.tostring(chapter).decode("utf-8")
            chapters[component_code] = chapter_str

        return chapters

    @staticmethod
    def generate_string_xml(element):
        """Verifica se un nodo xml è valido e ben formattato."""
        try:
            return etree.tostring(element, pretty_print=True, encoding="utf-8").decode("utf-8")
        except (TypeError, ValueError) as e:
            logger.error(
                f"Errore durante la generazione della stringa XML: {e}")
            return ""

    @staticmethod
    def merge_chapters(*chapters):
        """Funzione per unire i dizionari."""
        result = {}
        for d in chapters:
            if d:
                result.update(d)
        return result

    def initialize_root(self):
        """Crea la root del xml e il nodo chapters."""
        self.root = etree.Element("document")
        etree.SubElement(self.root, "placeholder", name="meta")
        etree.SubElement(self.root, "placeholder", name="cover-page")
        etree.SubElement(self.root, "placeholder", name="back-cover")
        etree.SubElement(self.root, "placeholder", name="summary")
        self.chapters_node = etree.SubElement(self.root, "chapters")

    def add_chapter(self, chapter_group):
        """Aggiunge al nodo 'chapters' il capitolo."""
        for chapter_code in chapter_group:
            chapter_xml_str = self.chapters.get(chapter_code)
            if chapter_xml_str:
                chapter_xml = etree.fromstring(chapter_xml_str)
                self.chapters_node.append(chapter_xml)

    def get_string_final_xml_t3(self):
        try:
            xml_string = etree.tostring(self.root,
                                        pretty_print=True,
                                        xml_declaration=True,
                                        encoding="utf-8").decode("utf-8")
            return xml_string
        except (TypeError, ValueError) as e:
            logger.error(
                f"Errore durante la generazione della stringa XML: {e}")
            return ""

    def processing(self):
        """Processore che recupera i capitoli dal database e crea il template T3."""

        # ------------------------------------------------- universal chapters

        universal_chapters = self.get_universal_chapters()
        # controllo presenza di tutti i capitoli chapter_component
        # print('Nessuna chiave universale mancante')
        # missing_keys = set(self.universal_chapter_codes) - \
        #    universal_chapters.keys()
        # if missing_keys:
        #     print(f"Universal chapters: Chiavi mancanti: {missing_keys}")

        # ------------------------------------------------- component chapters

        component_chapters = self.get_component_chapters()
        # controllo presenza di tutti i capitoli chapter_component
        # print('Nessuna chiave componenti mancante')
        # missing_keys = set(self.component_ids) - component_chapters.keys()
        # if missing_keys:
        #    print(f"Component chapters: Chiavi mancanti: {missing_keys}")

        # print(json.dumps(component_chapters, indent=4, ensure_ascii=False))

        # ================================================== compositore vero e proprio

        self.chapters = self.merge_chapters(
            universal_chapters, component_chapters)
        self.initialize_root()

        # --- universali
        chapters_part_1 = ['premises', 'definitions', 'regulation', 'location',
                           'environment', 'executive', 'solar', 'losses', 'energy']
        self.add_chapter(chapters_part_1)

        # --- pvgis
        etree.SubElement(self.chapters_node, 'placeholder',
                         name="X100", ref="pvgis")

        # --- universali + componenti
        chapters_part_2 = ['emissions', 'generator',
                           'module', 'support', 'inverter']
        self.add_chapter(chapters_part_2)

        # --- storage
        if self.has_storage:
            self.add_chapter(['storage'])

        # --- base + universali
        chapters_part_3 = ['cables', 'e-panels', 'grounding', 'protections',
                           'grid', 'e-checks', 'testing', 'commissioning',
                           'decommissioning', 'feasibility', 'conclusion', 'sld']
        self.add_chapter(chapters_part_3)

        t3_xml_string = self.get_string_final_xml_t3()

        return t3_xml_string

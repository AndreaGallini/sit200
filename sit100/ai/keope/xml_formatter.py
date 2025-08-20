"""
xml_formatter.py
Classe che si occupa di creare i placeholders associando come valore i contenuti (stringhe o stringhe di xml).
"""
from lxml import etree

from .sections.cables import Cables
from .sections.common import Common
from .sections.cover_page import CoverPageGenerator
from .sections.back_cover import BackCoverGenerator
from .sections.cover_page_design import CoverPageDesignGenerator
from .sections.feasibility import Feasibility
from .sections.generator import Generator
from .sections.premesse import Premesse
from .sections.solar import Solar
from .sections.pvgis import Pvgis
from .sections.summary import SummaryGenerator


class XMLFormatter:

    def __init__(self, data):
        self.data = data

    @staticmethod
    def format_list_to_table_string(data):
        """Converte una lista di liste in una stringa XML che rappresenta una tabella."""

        root = etree.Element('table')
        for row_data in data:
            row = etree.SubElement(root, 'row')
            for cell_data in row_data:
                cell = etree.SubElement(row, 'cell')
                cell.text = str(cell_data)
        return Common.generate_string_xml(root)

    def create_metadata_node(self):
        """Crea il nodo xml dei matadati"""

        metadata = etree.Element("metadata")
        etree.SubElement(metadata, "title").text = "Relazione tecnica"
        etree.SubElement(metadata, "author").text = "Fidia"
        etree.SubElement(metadata, "version").text = "0.1"
        return Common.generate_string_xml(metadata)

    def create_footer_cover_page(self):
        """Crea il nodo xml del footer della cover page."""

        footer_cover_page = etree.Element("footer-cover-page")
        Common.create_revision_section(footer_cover_page, self.data)
        Common.create_file_references_section(footer_cover_page, self.data)
        return Common.generate_string_xml(footer_cover_page)

    def create_cover_page(self):
        generator = CoverPageGenerator(self.data)
        xml_string = generator.generate_cover_page()
        return xml_string

    def create_cover_page_design(self):
        generator = CoverPageDesignGenerator(self.data)
        xml_string = generator.generate_cover_page()
        return xml_string

    def create_back_cover_page(self):
        generator = BackCoverGenerator(self.data)
        xml_string = generator.generate_back_cover_page()
        return xml_string

    def create_summary(self):
        """Crea il nodo xml dell'indice dei capitoli."""
        generator = SummaryGenerator(self.data)
        xml_string = generator.generate_summary()
        return xml_string

    def generate_placeholders_content(self):
        """Crea tutti i contenuti dei placeholders."""

        string_placeholders = {}
        xml_placeholders = {}

        # -------------------------------------------- stringhe
        string_placeholders['S1'] = self.data.get("real_peak_power", '')
        string_placeholders['S2'] = self.data.get("plant_location", '')

        string_placeholders['S3'] = f"{self.data.get('latitude_ext', '')}\n" \
            f"{self.data.get('longitude_ext', '')}\n" \
            f"{self.data.get('albedo_ext', '')}"

        # -------------------------------------------- meta e cover del progetto
        xml_placeholders['meta'] = self.create_metadata_node()
        xml_placeholders['cover-page'] = self.create_cover_page()
        xml_placeholders['back-cover'] = self.create_back_cover_page()
        # xml_placeholders['footer-cover-page'] = self.create_footer_cover_page()

        # -------------------------------------------- cover della distinta base
        xml_placeholders['design-cover-page'] = self.create_cover_page_design()

        # -------------------------------------------- indice

        xml_placeholders['summary'] = self.create_summary()

        # -------------------------------------------- premesse

        premesse = Premesse(self.data)
        xml_placeholders['X1'] = premesse.create_intervention_scope()
        xml_placeholders['X2'] = premesse.create_plant_purpose()
        xml_placeholders['X3'] = premesse.create_main_feature_table()
        xml_placeholders['X4'] = premesse.create_project_team()

        xml_placeholders['X5'] = premesse.create_plant_location()
        xml_placeholders['X6'] = premesse.create_image_location()
        xml_placeholders['X7'] = premesse.create_plant_logistics()
        xml_placeholders['X8'] = premesse.create_image_marker_cicle()
        xml_placeholders['X9'] = premesse.create_image_polygon()
        xml_placeholders['X9a'] = premesse.create_subfields_arrangement()

        xml_placeholders['X11'] = premesse.create_dashboard_executive_summary_table()
        xml_placeholders['X12'] = premesse.create_general_description_table()
        xml_placeholders['X13'] = premesse.create_economic_convenience_table()
        xml_placeholders['X14'] = premesse.create_location_solar_table()

        # -------------------------------------------- solar calculator

        solar = Solar(self.data)
        xml_placeholders['X20'] = solar.create_table_irr_horizontal_plane_irradiation()
        xml_placeholders['g001'] = solar.create_image_horizontal_irradiation()
        # xml_placeholders['X21'] = solar.create_table_horizontal_plane_irradiation()     # sospesa
        # Tabella unificata per sottocampi (sostituisce X22 e X23)
        xml_placeholders['X22'] = solar.create_table_unified_module_plane_irradiation_by_subfield()
        # Tabella riassuntiva sottocampi
        xml_placeholders['X23'] = solar.create_table_subfields_summary()
        xml_placeholders['X24'] = solar.create_text_yearly_module_plane_irradiation()

        xml_placeholders['X31'] = solar.create_text_clinometric_classification()
        xml_placeholders['X32'] = solar.create_table_all_losses()
        xml_placeholders['X33'] = solar.create_table_subfields_total_losses()
        xml_placeholders['X34'] = solar.create_text_for_total_losses_classification()

        xml_placeholders['X41'] = solar.create_table_subfields_annual_net_energy()
        xml_placeholders['X42'] = solar.create_slogan_annual_net_energy()
        # xml_placeholders['X43'] = solar.create_text_annual_net_energy_classification()
        xml_placeholders['X44'] = solar.create_table_monthly_net_energy()

        xml_placeholders['X45'] = solar.create_text_annual_energy_yield()
        # xml_placeholders['X46'] = solar.create_slogan_annual_energy_yield()
        xml_placeholders['X47'] = solar.create_table_monthly_energy_yield()
        xml_placeholders['X48'] = solar.create_table_annual_energy_production()

        xml_placeholders['X49'] = solar.create_table_system_efficiency()
        xml_placeholders['X50'] = solar.create_slogan_system_efficiency()
        # xml_placeholders['X51'] = solar.create_text_system_efficiency_classification()
        xml_placeholders['X52'] = solar.create_table_monthly_efficiency_percentage()
        xml_placeholders['X53'] = solar.create_table_yearly_summary_production()
        # xml_placeholders['X54'] = solar.create_table_montly_summary_production()
        xml_placeholders['X60'] = solar.create_table_emission_reduction()

        # -------------------------------------------- generator

        generator = Generator(self.data)
        xml_placeholders['X70'] = generator.create_image_plant_layout()
        # in parte uguale in executive summary
        xml_placeholders['X71'] = generator.create_technical_features_table()
        xml_placeholders['X72'] = generator.create_technical_configuration_table()

        # -------------------------------------------- pvgis

        pvgis = Pvgis(self.data)
        xml_placeholders['X100'] = pvgis.create_pvgis_chapter()

        # -------------------------------------------- cavi
        cables = Cables(self.data)
        xml_placeholders['X110'] = cables.create_table_cable_sections()
        xml_placeholders['X111'] = cables.create_table_cable_lengths()

        # -------------------------------------------- grounding (messa a terra)

        # xml_placeholders['X130'] =

        # -------------------------------------------- feasibility: cashflow

        feasibility = Feasibility(self.data)
        if self.data.get('ecofin'):
            xml_placeholders['X159'] = feasibility.create_table_yearly_energy_production()
            xml_placeholders['X150'] = feasibility.create_section_revenue_from_self_consumption()
            xml_placeholders['X153'] = feasibility.create_section_fiscal_deduction()
            xml_placeholders['X160'] = feasibility.create_section_rid()
            xml_placeholders['X161'] = feasibility.create_section_cer()
            xml_placeholders['X151'] = feasibility.create_text_generator_total_cost()
            xml_placeholders['X152'] = feasibility.create_text_routine_maintenance_costs()
            xml_placeholders['X154'] = feasibility.create_table_yearly_cash_flow()
            xml_placeholders['X155'] = feasibility.create_image_cashflow()
            xml_placeholders['X156'] = feasibility.create_text_payback_period()
            xml_placeholders['X157'] = feasibility.create_text_roi()
            xml_placeholders['X158'] = feasibility.create_text_gianetto()

        # -------------------------------------------- datasheet

        # datasheet = Datasheet(self.data)
        # xml_placeholders['X120'] = datasheet.create_image_photovoltaic_module()
        # xml_placeholders['X121'] = datasheet.create_image_support_structure()
        # xml_placeholders['X122'] = datasheet.create_image_inverter()
        # xml_placeholders['X123'] = datasheet.create_image_storage()
        # xml_placeholders['X124'] = datasheet.create_image_cables()

        return string_placeholders, xml_placeholders

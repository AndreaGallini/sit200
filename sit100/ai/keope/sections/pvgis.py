"""
pvgis.py
Classe che gestisce la costruzione del capitolo con i dati di PVGIS.
"""
from lxml import etree

from .common import Common


class Pvgis:

    def __init__(self, data):
        self.data = data
        self.pvgis_chapter = etree.Element("chapter")

    @staticmethod
    def create_input_table(inputs):
        """Crea una tabella XML per i dati di input."""

        table = etree.Element("table", name="input_table",
                              style="width-cols:6;space-after:1;borders:TRBL")

        latitude = inputs.get('location', {}).get('latitude', '')
        longitude = inputs.get('location', {}).get('longitude', '')
        radiation_db = inputs.get('meteo_data', {}).get('radiation_db', '')
        horizon_db = inputs.get('meteo_data', {}).get('horizon_db', '')
        peak_power = inputs.get('pv_module', {}).get('peak_power', '')
        system_loss = inputs.get('pv_module', {}).get('system_loss', '')
        slope = inputs.get('mounting_system', {}).get(
            'fixed', {}).get('slope', '').get('value', '')
        azimuth = inputs.get('mounting_system', {}).get(
            'fixed', {}).get('azimuth', '').get('value', '')

        data = {
            "Latitude/Longitude": f"{latitude} , {longitude}",
            "Horizon": f"{horizon_db}",
            "Database used": f"{radiation_db}",
            "PV installed": f"{peak_power} kWp",
            "System loss": f"{system_loss} %",
            "Slope angle": f"{slope}°",
            "Azimuth angle:": f"{azimuth}°"
        }

        for param, value in data.items():
            row = etree.SubElement(table, "row")
            cell1 = etree.SubElement(row, "cell")
            cell1.text = param
            cell2 = etree.SubElement(row, "cell")
            cell2.text = value

        return table

    @staticmethod
    def create_output_table(outputs):
        """Crea una tabella XML per i dati di output."""

        table = etree.Element("table", name="output_table",
                              style="width-cols:6;space-after:1")

        data = {
            "E_d": f"{outputs.get('E_d', '')} kWh/giorno",
            "E_m": f"{outputs.get('E_m', '')} kWh/mese",
            "E_y": f"{outputs.get('E_y', '')} kWh/anno",
            "H(i)_d": f"{outputs.get('H(i)_d', '')} kWh/m²/giorno",
            "H(i)_m": f"{outputs.get('H(i)_m', '')} kWh/m²/mese",
            "H(i)_y": f"{outputs.get('H(i)_y', '')} kWh/m²/anno",
            "SD_d": f"{outputs.get('SD_d', '')} kWh/giorno",
            "SD_m": f"{outputs.get('SD_m', '')} kWh/mese",
            "SD_y": f"{outputs.get('SD_y', '')} kWh/anno",
        }

        for param, value in data.items():
            row = etree.SubElement(table, "row")
            cell1 = etree.SubElement(row, "cell")
            cell1.text = param
            cell2 = etree.SubElement(row, "cell")
            cell2.text = value

        return table

    @staticmethod
    def create_energy_table(monthly_data):
        """Crea una tabella XML per i dati energetici mensili."""

        table = etree.Element("table", name="energy_table",
                              style="width-cols:4;space-after:1;borders:TRBL;padding:0;")

        # Header
        header_row = etree.SubElement(table, "row")
        headers = ["Month", "E_m", "H(i)_m", "SD_m"]
        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        # Mappa dei mesi in inglese
        month_names = {
            1: "Gennaio", 2: "Febbraio", 3: "Marzo", 4: "Aprile",
            5: "Maggio", 6: "Giugno", 7: "Luglio", 8: "Agosto",
            9: "Settembre", 10: "Ottobre", 11: "Novembre", 12: "Dicembre"
        }

        # Dati mensili
        for month_data in monthly_data:
            row = etree.SubElement(table, "row")

            # Mese (convertito da numero a nome)
            month_num = month_data.get('month', 1)
            month_name = month_names.get(month_num, str(month_num))
            etree.SubElement(row, "cell").text = month_name

            # E_m (solo il numero, formattato con 2 decimali)
            e_m = month_data.get('E_m', 0)
            etree.SubElement(row, "cell").text = f"{e_m:.2f}"

            # H(i)_m (solo il numero, formattato con 2 decimali)
            h_m = month_data.get('H(i)_m', 0)
            etree.SubElement(row, "cell").text = f"{h_m:.2f}"

            # SD_m (solo il numero, formattato con 2 decimali)
            sd_m = month_data.get('SD_m', 0)
            etree.SubElement(row, "cell").text = f"{sd_m:.2f}"

        return table

    def create_solar_report_node_for_subfield(self, subfield_name, pvgis_data):
        """Crea un nodo XML per un singolo sottocampo con le tre tabelle: energy, input, e output."""

        # Ottieni i dati del sottocampo dal generatore per il nome utente
        generator = self.data.get('generator', {})
        user_subfield_name = ""

        for field_name, field_data in generator.items():
            for sf_name, sf_data in field_data.items():
                if sf_name == subfield_name:
                    user_subfield_name = sf_data.get('name', '')
                    break

        # Sottotitolo per il sottocampo
        subtitle = etree.SubElement(self.pvgis_chapter, "subtitle")
        display_name = f"{subfield_name} - {user_subfield_name}" if user_subfield_name else subfield_name
        subtitle.text = f"Dati PVGIS per sottocampo {display_name}"

        # Tabella: Dati di input
        input_table = self.create_input_table(pvgis_data['inputs'])
        self.pvgis_chapter.append(input_table)

        # Tabella: Dati di output totali
        output_table = self.create_output_table(
            pvgis_data['outputs']['totals']['fixed'])
        self.pvgis_chapter.append(output_table)

        # Tabella: Dati energetici mensili
        energy_table = self.create_energy_table(
            pvgis_data['outputs']['monthly']['fixed'])
        self.pvgis_chapter.append(energy_table)

    def create_solar_report_node(self):
        """Crea i nodi XML per tutti i sottocampi o per il dato aggregato."""

        # Verifica se ci sono dati per sottocampi
        pvgis_subfields = self.data.get('pvgis_subfields', {})

        if pvgis_subfields:
            # Processa ogni sottocampo separatamente
            for subfield_name, pvgis_data in pvgis_subfields.items():
                self.create_solar_report_node_for_subfield(
                    subfield_name, pvgis_data)
        else:
            # Fallback al comportamento originale per compatibilità
            pvgis_data = self.data.get('pvgis', {})
            if pvgis_data:
                # Tabella: Dati di input
                input_table = self.create_input_table(pvgis_data['inputs'])
                self.pvgis_chapter.append(input_table)

                # Tabella: Dati di output totali
                output_table = self.create_output_table(
                    pvgis_data['outputs']['totals']['fixed'])
                self.pvgis_chapter.append(output_table)

                # Tabella: Dati energetici mensili
                energy_table = self.create_energy_table(
                    pvgis_data['outputs']['monthly']['fixed'])
                self.pvgis_chapter.append(energy_table)

        return self.pvgis_chapter

    def create_texts(self):
        """Crea un paragrafo con del testo. Include il copyright"""

        node = etree.SubElement(self.pvgis_chapter, "text")
        node.text = f"E_m: Average monthly electricity production from the defined system [kWh]."
        node = etree.SubElement(self.pvgis_chapter, "text")
        node.text = f"H(i)_m: Average monthly sum of global irradiation per square meter received by the modules of the given system [kWh/m²]."
        node = etree.SubElement(self.pvgis_chapter, "text")
        node.text = f"SD_m: Standard deviation of the monthly electricity production due to year-to-year variation [kWh]."
        copy_node = etree.SubElement(self.pvgis_chapter, "text")
        copy_node.text = 'PVGIS ©Union Européenne, 2001-2024.'

    def create_results_paragraph(self):
        """Paragrafo con i risultati restituiti da PVGIS."""

        subtitle = etree.SubElement(self.pvgis_chapter, "subtitle")
        subtitle.text = "Stima dei parametri energetici dell'impianto mediante PVGIS"
        self.create_solar_report_node()
        self.create_texts()

    def create_introduction_paragraph(self):
        """Paragrafo introduttivo del capitolo."""

        texts = [
            "PVGIS (Photovoltaic Geographical Information System) è uno strumento sviluppato dal "
            "Centro Comune di Ricerca (JRC) della Commissione Europea, progettato per fornire informazioni "
            "dettagliate sulle risorse solari e sulla potenziale produzione di energia fotovoltaica per diverse "
            "località in tutto il mondo.",
            "PVGIS utilizza un vasto database di irraggiamento solare, che include dati satellitari e misurazioni "
            "a terra per fornire stime accurate dell'irraggiamento solare globale, diretto e diffuso.",
            "Il sistema può calcolare la produzione potenziale di energia elettrica di un impianto fotovoltaico "
            "in base alla posizione geografica, alle specifiche tecniche dei moduli fotovoltaici, all'orientamento "
            "e all'inclinazione dei pannelli. PVGIS può eseguire simulazioni avanzate che includono fattori come "
            "le perdite di sistema, l'efficienza degli inverter e l'effetto della temperatura sui moduli fotovoltaici."
        ]
        for text in texts:
            etree.SubElement(self.pvgis_chapter, "text").text = text

    def create_chapter_title(self):
        """Crea il nodo del titolo di capitolo."""
        title = etree.SubElement(self.pvgis_chapter, "h1")
        title.text = "PVGIS"

    def create_pvgis_chapter(self):
        """X100: Costruisce i nodi xml relativi al capitolo di PVGIS."""

        # Verifica se ci sono dati PVGIS (per sottocampi o aggregati)
        pvgis_subfields = self.data.get('pvgis_subfields', {})
        pvgis_data = self.data.get('pvgis', {})

        if pvgis_subfields or pvgis_data:
            self.create_chapter_title()
            self.create_introduction_paragraph()
            self.create_results_paragraph()
            return Common.generate_string_xml(self.pvgis_chapter)
        else:
            return ""

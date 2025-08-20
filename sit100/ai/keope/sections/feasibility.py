"""
feasibility.py
Classe che gestisce la costruzione delle stringhe xml relative all'analisi della convenienza economica-finanziaria.
"""
import os

from lxml import etree

from .common import Common
from ..params import TABLE_CAPTION, IMAGE_CAPTION


class Feasibility:

    def __init__(self, data):
        self.data = data

    def create_table_yearly_energy_production(self):
        """X159: Crea la tabella con i valori di produzione di energia elettrica annuale."""
        yearly_energy = self.data.get('ecofin', {}).get('yearly_energy_produced', [])
        if not yearly_energy:
            return ""

        table_node = etree.Element("table",
                                   attrib={"style": "borders:TRBL;alignment:center; width-cols:3-7;"
                                                    "column-alignments:C-C;space-after:1;padding:1"}
                                   )

        row_node = etree.SubElement(table_node, "row")
        etree.SubElement(row_node, "cell").text = "Anno"
        etree.SubElement(row_node, "cell").text = "Energia prodotta (kWh/anno)"

        for i, value in enumerate(yearly_energy):
            row_node = etree.SubElement(table_node, "row")
            etree.SubElement(row_node, "cell").text = str(i + 1)
            etree.SubElement(row_node, "cell").text = str(int(value))

        return Common.generate_string_xml(table_node)

    def create_section_revenue_from_self_consumption(self):
        """X150: Crea una sezione di testo per le entrate derivanti dai risparmi da autoconsumo (se ci sono)."""

        ecofin = self.data.get('ecofin', {})

        # creazione della sezione solo se ci sono risparmi da autoconsumo
        if ecofin.get("lifetime_savings_revenues", 0) > 0:
            tag_node = etree.Element('tag_to_remove')

            # subtitle
            subtitle_node = etree.SubElement(tag_node, "subtitle")
            subtitle_node.text = "Risparmio derivante dall'autoconsumo"

            # testo introduttivo
            texts = [
                "L'analisi considera:",
                f"Percentuale di autoconsumo diretto: {ecofin.get("autoconsumption_percentage", "")}%",
                f"Prezzo medio dell'energia elettrica: {ecofin.get("str_energy_cost_per_kwh")}"
            ]
            for txt in texts:
                text_node = etree.SubElement(tag_node, "text")
                text_node.text = txt

            txt = "I valori stimati sono riportati nella seguente tabella riepilogativa che riporta le entrate " \
                  "derivanti dall’autoconsumo, a fronte dei costi operativi annuali dell’impianto fotovoltaico. " \
                  "La tabella evidenzia l'energia prodotta dall’impianto fotovoltaico e i risparmi " \
                  "ottenuti grazie all’autoconsumo."
            etree.SubElement(tag_node, "text").text = txt

            table_node = etree.SubElement(tag_node, "table", attrib={"style": "borders:TB;alignment:center;"
                                                                              "width-cols:9-7;column-alignments:L-C;"})

            table_content = [
                ["Ricavi da autoconsumo per risparmio in bolletta, primo anno",
                 f"{ecofin['yearly_savings_revenues'][0]} €/ primo anno"],
                ["Costo dell’energia", f"{ecofin["str_energy_cost_per_kwh"]}"],
                ["Energia totale prodotta in 25 anni", f"{ecofin["str_lifetime_total_energy_produced"]}"],
                ["Risparmi da autoconsumo in 25 anni", f"{ecofin["str_lifetime_savings_revenues"]}"],
            ]
            for content in table_content:
                row_node = etree.SubElement(table_node, "row")
                etree.SubElement(row_node, "cell").text = content[0]
                etree.SubElement(row_node, "cell").text = content[1]

            string = Common.generate_string_xml(tag_node)
            cleaned_string = string.replace(
                "<tag_to_remove>", "").replace("</tag_to_remove>", "")

            return cleaned_string
        else:
            return ""

    def create_section_fiscal_deduction(self):
        """X153: Crea una sezione di testo per le entrate derivanti dai incentivi fiscali (se ci sono)."""

        ecofin = self.data.get('ecofin', {})

        # creazione della sezione solo se ci sono incentivi fiscali
        if ecofin.get("lifetime_incentive_with_storage", 0) > 0 or ecofin.get("lifetime_incentive_without_storage",
                                                                              0) > 0:
            tag_node = etree.Element('tag_to_remove')
            # subtitle
            subtitle_node = etree.SubElement(tag_node, "subtitle")
            subtitle_node.text = "Incentivi fiscali"
            # text
            txt = ("Gli incentivi rappresentano una parte importante del ritorno economico. "
                   "Tra i principali strumenti disponibili:")
            text_node = etree.Element('text')
            text_node.text = txt
            # text
            if self.data['storage'] == "1":
                text_node = etree.Element('text')
                text_node.text = ecofin['str_incentive_without_storage_comment']
                text_node = etree.Element('text')
                text_node.text = f"Il bonus fiscale annuale per l’impianto con accumulo è pari a {ecofin['incentive_with_storage']} €/anno"
            else:
                text_node = etree.Element('text')
                text_node.text = ecofin['str_incentive_with_storage_comment']
                text_node = etree.Element('text')
                text_node.text = f"Il bonus fiscale annuale per l’impianto senza accumulo è pari a {ecofin['incentive_without_storage']} €/anno"

            string = Common.generate_string_xml(tag_node)
            cleaned_string = string.replace(
                "<tag_to_remove>", "").replace("</tag_to_remove>", "")

            return cleaned_string
        else:
            return ""

    def create_section_rid(self):
        """X160: Crea una sezione di testo per le entrate derivanti dalla vendita (Ritiro Dedicato) (se ci sono)."""

        ecofin = self.data.get('ecofin', {})

        # creazione della sezione solo se ci sono entrate da rid
        if ecofin.get("lifetime_rid_revenues", 0) > 0:
            tag_node = etree.Element('tag_to_remove')
            # subtitle
            subtitle_node = etree.SubElement(tag_node, "subtitle")
            subtitle_node.text = "Entrate dalla vendita dell'energia (Ritiro Dedicato)"
            # testo introduttivo
            texts = [
                "L'analisi considera i seguenti parametri:",
                f"Percentuale di energia prodotta che viene venduta: {ecofin.get("rid_percentage", "")}%",
                f"Prezzo medio vendita energia alla rete: {ecofin.get("str_rid_revenue_per_kwh", "")}"
            ]
            for txt in texts:
                text_node = etree.SubElement(tag_node, "text")
                text_node.text = txt

            txt = "I valori stimati sono riportati nella seguente tabella riepilogativa che riporta le entrate " \
                  "derivanti dalla vendita dell'energia prodotta alla rete."
            etree.SubElement(tag_node, "text").text = txt

            table_node = etree.SubElement(tag_node, "table", attrib={"style": "borders:TB;alignment:center;"
                                                                              "width-cols:9-7;column-alignments:L-C;"})

            table_content = [
                ["Ricavi dalla vendita RID, primo anno", f"{ecofin['yearly_rid_revenues'][0]} €/ primo anno"],
                ["Costo dell’energia ceduta", f"{ecofin.get("str_rid_revenue_per_kwh", "")}"],
                ["Ricavi dalla vendita RID in 25 anni", f"{ecofin["str_lifetime_rid_revenues"]}"],
            ]
            for content in table_content:
                row_node = etree.SubElement(table_node, "row")
                etree.SubElement(row_node, "cell").text = content[0]
                etree.SubElement(row_node, "cell").text = content[1]

            string = Common.generate_string_xml(tag_node)
            cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

            return cleaned_string
        else:
            return ""

    def create_section_cer(self):
        """X161: Crea una sezione di testo per le entrate derivanti dai CER(se ci sono)."""

        ecofin = self.data.get('ecofin', {})

        # creazione della sezione solo se ci sono entrate da cer
        if ecofin.get("lifetime_cer_revenues", 0) > 0:
            tag_node = etree.Element('tag_to_remove')
            # subtitle
            subtitle_node = etree.SubElement(tag_node, "subtitle")
            subtitle_node.text = "Entrate derivanti dalla partecipazione alla CER (Comunità Energetiche Rinnovabile)"
            # testo introduttivo
            texts = [
                "L'analisi considera i seguenti parametri:",
                f"Percentuale di energia prodotta che viene ceduta: {ecofin.get("cer_percentage", "")}%",
                f"Valore medio dell'energia ceduta alla CER: {ecofin.get("str_cer_revenue_per_kwh", "")}"
            ]
            for txt in texts:
                text_node = etree.SubElement(tag_node, "text")
                text_node.text = txt

            txt = "I valori stimati sono riportati nella seguente tabella riepilogativa che riporta le entrate " \
                  "derivanti dalla partecipazione alla Comunità Energetica Rinnovabile."
            etree.SubElement(tag_node, "text").text = txt

            table_node = etree.SubElement(tag_node, "table", attrib={"style": "borders:TB;alignment:center;"
                                                                              "width-cols:9-7;column-alignments:L-C;"})

            table_content = [
                ["Ricavi dalla vendita RID, primo anno", f"{ecofin['yearly_rid_revenues'][0]} €/ primo anno"],
                ["Costo dell’energia ceduta", f"{ecofin.get("str_rid_revenue_per_kwh", "")}"],
                ["Ricavi dalla vendita RID in 25 anni", f"{ecofin["str_lifetime_cer_revenues"]}"],
            ]
            for content in table_content:
                row_node = etree.SubElement(table_node, "row")
                etree.SubElement(row_node, "cell").text = content[0]
                etree.SubElement(row_node, "cell").text = content[1]

            string = Common.generate_string_xml(tag_node)
            cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

            return cleaned_string

        else:
            return ""

    def create_text_generator_total_cost(self):
        """X151: Crea un testo per il costo totale dell'impianto (H2)."""

        ecofin = self.data.get('ecofin', {})

        if self.data['storage'] == "1":
            txt = ecofin.get("str_plant_with_storage_cost", "")
        else:
            txt = ecofin.get("str_plant_without_storage_cost", "")

        tag_node = etree.Element('tag_to_remove')
        etree.SubElement(tag_node, "text").text = txt

        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_text_routine_maintenance_costs(self):
        """X152: Crea un testo per il costo totale dell'impianto (H4)."""

        ecofin = self.data.get('ecofin', {})

        tag_node = etree.Element('tag_to_remove')

        maintenance_with_storage = ecofin.get('yearly_maintenance_with_storage', [])[1]
        maintenance_without_storage = ecofin.get('yearly_maintenance_without_storage', [])[1]
        insurance_with_storage = ecofin.get('yearly_insurance_with_storage', [])[1]
        insurance_without_storage = ecofin.get('yearly_insurance_without_storage', [])[1]

        if self.data['storage'] == "1":
            texts = [
                f"Manutenzione: il costo annuale per la manutenzione ordinaria è pari a {maintenance_with_storage} €/anno",
                f"Assicurazione: il costo annuale per l'assicurazione è pari a {insurance_with_storage} €/anno",
            ]
        else:
            texts = [
                f"Manutenzione: il costo annuale per la manutenzione ordinaria è pari a {maintenance_without_storage} €/anno",
                f"Assicurazione: il costo annuale per l'assicurazione è pari a {insurance_without_storage} €/anno",
            ]
        for txt in texts:
            text_node = etree.SubElement(tag_node, "text")
            text_node.text = txt

        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace(
            "<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_table_yearly_cash_flow(self):
        """X154: Crea la tabella con i valori di cash flow annuale (H5)."""

        ecofin = self.data.get('ecofin', {})

        """
'yearly_total_revenues_with_storage': [11763, 11680, 11603, 11520, 11435, 11360, 11276, 11200, 11124, 11049, 10974, 10897, 10822, 10747, 10670, 10603, 10528, 10453, 10386, 10309, 10242, 10175, 10108, 10033, 9965], 
'yearly_total_revenues_without_storage': [11763, 11680, 11603, 11520, 11435, 11360, 11276, 11200, 11124, 11049, 10974, 10897, 10822, 10747, 10670, 10603, 10528, 10453, 10386, 10309, 10242, 10175, 10108, 10033, 9965],
'yearly_net_cashflow_with_storage': [11219, 10048, 9971, 9888, 9803, 9728, 9644, 9568, 9492, 9417, 9342, 9265, 9190, 9115, 9038, 8971, 8896, 8821, 8754, 8677, 8610, 8543, 8476, 8401, 8333], 
'yearly_net_cashflow_without_storage': [11434, 10693, 10616, 10533, 10448, 10373, 10289, 10213, 10137, 10062, 9987, 9910, 9835, 9760, 9683, 9616, 9541, 9466, 9399, 9322, 9255, 9188, 9121, 9046, 8978], 
'cumulative_cashflow_with_storage': [-97594, -87546, -77575, -67687, -57884, -48156, -38512, -28944, -19452, -10035, -693, 8572, 17762, 26877, 35915, 44886, 53782, 62603, 71357, 80034, 88644, 97187, 105663, 114064, 122397], 
'cumulative_cashflow_without_storage': [-54448, -43755, -33139, -22606, -12158, -1785, 8504, 18717, 28854, 38916, 48903, 58813, 68648, 78408, 88091, 97707, 107248, 116714, 126113, 135435, 144690, 153878, 162999, 172045, 181023], 
'yearly_total_costs_with_storage': [544, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632, 1632], 
'yearly_total_costs_without_storage': [329, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987], 
        """

        if self.data['storage'] == "1":
            costs_euros = ecofin['yearly_total_costs_with_storage']
            revenues_euros = ecofin['yearly_total_revenues_with_storage']
            net_cashflow = ecofin['yearly_net_cashflow_with_storage']
            cumulative_euros = ecofin['cumulative_cashflow_with_storage']
            plant_cost = ecofin['plant_with_storage_cost']
        else:
            costs_euros = ecofin['yearly_total_costs_without_storage']
            revenues_euros = ecofin['yearly_total_revenues_without_storage']
            net_cashflow = ecofin['yearly_net_cashflow_without_storage']
            cumulative_euros = ecofin['cumulative_cashflow_without_storage']
            plant_cost = ecofin['plant_without_storage_cost']

        table_node = etree.Element("table",
                                   attrib={"style": "borders:TB;alignment:center;"
                                                    " width-cols:2;column-alignments:C-C-C-C-C; "
                                                    "space-after:1;padding:1"})
        caption = etree.SubElement(table_node, "caption")
        caption.text = TABLE_CAPTION['x154']

        row_node = etree.SubElement(table_node, "row")
        etree.SubElement(row_node, "cell").text = "Anno"
        etree.SubElement(row_node, "cell").text = "Ricavi (€)"
        etree.SubElement(row_node, "cell").text = "Costi (€)"
        etree.SubElement(row_node, "cell").text = "Flussi netti (€)"
        etree.SubElement(row_node, "cell").text = "Cashflow (€)"

        row_node = etree.SubElement(table_node, "row")
        etree.SubElement(row_node, "cell").text = "0"
        etree.SubElement(row_node, "cell").text = ""
        etree.SubElement(row_node, "cell").text = ""
        etree.SubElement(row_node, "cell").text = ""
        etree.SubElement(row_node, "cell").text = f"-{plant_cost}"

        n_years = len(cumulative_euros)
        for i in range(n_years):
            row_node = etree.SubElement(table_node, "row")
            etree.SubElement(row_node, "cell").text = str(i + 1)
            etree.SubElement(row_node, "cell").text = str(revenues_euros[i])
            etree.SubElement(row_node, "cell").text = str(costs_euros[i])
            etree.SubElement(row_node, "cell").text = str(net_cashflow[i])
            etree.SubElement(row_node, "cell").text = str(cumulative_euros[i])

        return Common.generate_string_xml(table_node)

    def create_image_cashflow(self):
        """X155: Crea l'immagine del plot del cash flow, creato e salvato dalla pipeline cashflow (H5)."""

        filename_storage = "cashflow_with_storage.png"
        filename_nostorage = "cashflow_without_storage.png"
        path_storage = f"{self.data['project_complete_path']}/{filename_storage}"
        path_nostorage = f"{self.data['project_complete_path']}/{filename_nostorage}"

        if self.data['storage'] == "1":
            image_src = path_storage
        else:
            image_src = path_nostorage

        if image_src:
            image_node = etree.Element("image", src=image_src, style="center")
            caption_node = etree.SubElement(image_node, "caption")
            caption_node.text = IMAGE_CAPTION['x155']
            return Common.generate_string_xml(image_node)
        else:
            return ""

    def create_text_payback_period(self):
        """X155: Crea un testo per il Payback Period (H6 e H8)."""

        ecofin = self.data.get('ecofin', {})

        if self.data['storage'] == "1":
            payback_period = f"{ecofin.get('payback_period_with_storage', '')}"
            cmm = f"{ecofin.get('payback_comment_with_storage', '')}"
        else:
            payback_period = f"{ecofin.get('payback_period_without_storage', '')}"
            cmm = f"{ecofin.get('payback_comment_without_storage', '')}"

        tag_node = etree.Element('tag_to_remove')

        texts = [
            f"Il progetto in esame presenta un Payback Period di {payback_period} anni.",
            f"{cmm}",
        ]
        for txt in texts:
            text_node = etree.SubElement(tag_node, "text")
            text_node.text = txt

        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace(
            "<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_text_roi(self):
        """X157: Crea un testo per il valore di Return on Investment (ROI) (H7 e H8)."""

        ecofin = self.data.get('ecofin', {})

        if self.data['storage'] == "1":
            roi_value = f"{ecofin.get('roi_with_storage', '')}"
            cmm = f"{ecofin.get('roi_comment_with_storage', '')}"
        else:
            roi_value = f"{ecofin.get('roi_without_storage', '')}"
            cmm = f"{ecofin.get('roi_comment_without_storage', '')}"

        tag_node = etree.Element('tag_to_remove')

        texts = [
            f"Nel caso in esame si ottiene un ROI pari a {roi_value}%",
            f"{cmm}"
        ]
        for txt in texts:
            text_node = etree.SubElement(tag_node, "text")
            text_node.text = txt

        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace(
            "<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_text_gianetto(self):
        """X158: Crea un testo per il valore di Guadagno Netto dopo 25 anni (H7 e H8)."""

        ecofin = self.data.get('ecofin', {})

        if self.data['storage'] == "1":
            gianetto = f"{ecofin.get('cumulative_cashflow_with_storage', [])[-1]}"
        else:
            gianetto = f"{ecofin.get('cumulative_cashflow_without_storage', [])[-1]}"

        txt = (
            f"Guadagno netto = valore cumulativo finale delle Entrate al 25° anno - valore cumulativo finale "
            f"delle Uscite al 25° anno. Quindi il guadagno netto è pari a {gianetto} €."
        )

        text_node = etree.Element('text')
        text_node.text = txt

        return Common.generate_string_xml(text_node)

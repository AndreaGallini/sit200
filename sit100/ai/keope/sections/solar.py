"""
solar.py
Classe che gestisce la costruzione delle stringhe xml relative al calcolatore.
Il calcolatore include i capitoli da calcolatore solare a riduzione delle emissioni.
"""
from lxml import etree

from ..params import MESI, TABLE_CAPTION
from .common import Common
from ..solar_calculator import SolarCalculator


class Solar:

    def __init__(self, data):
        self.data = data

    def create_table_irr_horizontal_plane_irradiation(self):
        """
        X20: Crea una tabella XML con cinque colonne:
        1. Mesi
        2. Valori di monthly_avg_daily_horizontal_irradiance
        3. Valori di monthly_avg_daily_beam_horizontal_irradiance
        4. Valori di monthly_avg_daily_diffuse_horizontal_irradiance
        5. Valori di monthly_reflected_solar_radiation
        """
        table = etree.Element("table", style="borders:TRBL;column-alignments: L-C-C-C-C;padding:2")

        caption = etree.SubElement(table, "caption")
        caption.text = TABLE_CAPTION['x20']

        data = self.data.get('ao1', {}).get('first_subfield').get(
            'monthly_avg_daily_horizontal_solar_irradiance_summary', {})

        headers = ["Mese",
                   "Irradiazione solare orizzontale (kWh/m²/giorno)",
                   "Irradiazione solare diretta (kWh/m²/giorno)",
                   "Irradiazione solare diffusa (kWh/m²/giorno)",
                   "Irradiazione solare riflessa (kWh/m²/giorno)"]

        header_row = etree.SubElement(table, "row")
        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        months = MESI.keys()
        for month in months:
            row = etree.SubElement(table, "row")

            # Prima colonna: nome del mese
            month_cell = etree.SubElement(row, "cell")
            month_cell.text = MESI[month]

            # Seconda colonna: horizontal irradiance
            hor_irr = Common.format_value(
                data['monthly_avg_daily_horizontal_irradiance'].get(month, ('', ''))[0])
            hor_cell = etree.SubElement(row, "cell")
            hor_cell.text = str(hor_irr)

            # Terza colonna: beam horizontal irradiance
            beam_irr = Common.format_value(
                data['monthly_avg_daily_beam_horizontal_irradiance'].get(month, ('', ''))[0])
            beam_cell = etree.SubElement(row, "cell")
            beam_cell.text = str(beam_irr)

            # Quarta colonna: diffuse horizontal irradiance
            diff_irr = Common.format_value(
                data['monthly_avg_daily_diffuse_horizontal_irradiance'].get(month, ('', ''))[0])
            diff_cell = etree.SubElement(row, "cell")
            diff_cell.text = str(diff_irr)

            # Quinta colonna: reflected solar radiation
            refl_irr = Common.format_value(
                data['monthly_avg_daily_reflected_horizontal_irradiance'].get(month, ('', ''))[0])
            refl_cell = etree.SubElement(row, "cell")
            refl_cell.text = str(refl_irr)

        return Common.generate_string_xml(table)

    def create_image_horizontal_irradiation(self):
        """g001: Crea l'immagine dell'irradianza orizzontale."""

        filename = "horizontal_irradiance.png"
        image_src = f"{self.data['project_complete_path']}/{filename}"

        image_node = etree.Element("image", src=image_src, style="center")
        caption_node = etree.SubElement(image_node, "caption")
        caption_node.text = ("Valori di irradiazione solare giornaliera media mensile "
                             "su un piano orizzontale (kWh/m² giorno).")
        return Common.generate_string_xml(image_node)

    def create_table_horizontal_plane_irradiation(self):
        """X21: Crea una tabella XML di due colonne con i valori di monthly_avg_daily_horizontal_irradiance."""

        table = etree.Element("table", style="borders:TRBL;column-alignments: L-C;"
                                             "padding:2;width-cols:3-5;alignment:center;")

        caption = etree.SubElement(table, "caption")
        caption.text = TABLE_CAPTION['x21']

        data = self.data.get('ao1', {}).get('monthly_avg_daily_horizontal_irradiance', {})

        header_row = etree.SubElement(table, "row")
        headers = ["Mese", "Irradiazione solare orizzontale (kWh/m²/giorno)"]

        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        months = MESI.keys()
        for month in months:
            value = data.get(month)
            row = etree.SubElement(table, "row")
            etree.SubElement(row, "cell").text = MESI[month]
            etree.SubElement(row, "cell").text = str(Common.format_value(value[0]))

        return Common.generate_string_xml(table)

    def create_table_module_plane_irradiation(self):
        """X22: Crea tabella XML di tre colonne con i valori di monthly_avg_daily_array_irradiance_classification."""

        table = etree.Element("table", style="borders:TRBL;column-alignments: L-C;"
                                             "padding:2;width-cols:3-5;alignment:center;")

        caption = etree.SubElement(table, "caption")
        caption.text = TABLE_CAPTION['x22']

        data = self.data.get('ao1', {}).get(
            'monthly_avg_daily_array_irradiance_classification', {})

        header_row = etree.SubElement(table, "row")
        headers = ["Mese", "Irradiazione solare sul piano dei moduli (kWh/m²/giorno)", "Classificazione"]

        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        months = MESI.keys()
        for month in months:
            values = data.get(month)
            row = etree.SubElement(table, "row")
            irradiance_value = values.get("monthly_avg_daily_array_irradiance_classification_value", "")
            threshold_name = values.get("monthly_avg_daily_array_irradiance_classification_threshold_name", "")
            etree.SubElement(row, "cell").text = MESI[month]
            etree.SubElement(row, "cell").text = str(
                Common.format_value(irradiance_value))
            etree.SubElement(row, "cell").text = threshold_name

        return Common.generate_string_xml(table)

    def create_table_monthly_module_plane_irradiation(self):
        """X23: Crea tabella XML di tre colonne con i valori di monthly_avg_daily_array_irradiance_classification."""

        table = etree.Element("table", style="borders:TRBL;column-alignments: L-C-C-C-C;padding:2")

        caption = etree.SubElement(table, "caption")
        caption.text = TABLE_CAPTION['x23']

        daily_data = self.data.get('ao1', {}).get('monthly_avg_daily_array_irradiance', {})
        monthly_data = self.data.get('ao1', {}).get('monthly_plane_of_array_irradiance', {})

        header_row = etree.SubElement(table, "row")
        headers = [
            "Mese",
            "Irradiazione solare giornaliera sul piano dei moduli (kWh/m²/giorno)",
            "Irradiazione solare mensile sul piano dei moduli (kWh/m²/mese)"
        ]

        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        for month in MESI.keys():
            if month in daily_data or month in monthly_data:
                row = etree.SubElement(table, "row")
                # Mesi
                etree.SubElement(row, "cell").text = MESI[month]
                # Irradiazione giornaliera
                daily_value, daily_unit = daily_data.get(month, (None, None))
                daily_text = f"{Common.format_value(daily_value)}" if daily_value is not None else ""
                etree.SubElement(row, "cell").text = daily_text
                # Irradiazione mensile
                monthly_value, monthly_unit = monthly_data.get(
                    month, (None, None))
                monthly_text = f"{Common.format_value(monthly_value)}" if monthly_value is not None else ""
                etree.SubElement(row, "cell").text = monthly_text
        return Common.generate_string_xml(table)

    def create_table_unified_module_plane_irradiation_by_subfield(self):
        """
        Crea una tabella unificata per ogni sottocampo che combina:
        - Irradiazione giornaliera sul piano dei moduli
        - Classificazione
        - Irradiazione mensile sul piano dei moduli
        """

        # Ottieni i dati dei sottocampi
        ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
        generator = self.data.get('generator', {})
        # Crea una tabella per ogni sottocampo, organizzata per campo
        all_content = []

        # Organizza i sottocampi per campo
        for field_name, field_data in generator.items():  # "A", "B"
            # Aggiungi sottotitolo per il campo
            field_subtitle = etree.Element("subtitle")
            field_subtitle.text = f"Campo {field_name}"
            all_content.append(Common.generate_string_xml(field_subtitle))

            # Crea tabelle per tutti i sottocampi di questo campo
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    user_subfield_name = subfield_data_gen.get('name', '')
                    field_subtitle = etree.Element("subtitle")
                    field_subtitle.text = f"Sottocampo {subfield_name} - {user_subfield_name}"
                    all_content.append(Common.generate_string_xml(field_subtitle))

                    # Aggiungi i parametri di simulazione
                    tilt = subfield_data_gen.get('inclination', 'N/A')
                    azimuth = subfield_data_gen.get('azimuth', 'N/A')
                    shading = subfield_data_gen.get('shading_obstacles', 'N/A')

                    parameters_text = etree.Element("text")
                    parameters_text.text = f"Parametri di simulazione: Tilt: {tilt}°, Azimuth: {azimuth}°, Ombreggiamento da ostacoli: {shading}%"
                    all_content.append(Common.generate_string_xml(parameters_text))

                    subfield_data = ao1_subfields[subfield_name]

                    table = etree.Element("table", style="borders:TRBL;column-alignments: L-C-C-C-C;padding:2")
                    caption = etree.SubElement(table, "caption")
                    # Includi il nome del sottocampo accanto al codice
                    caption.text = f"Irradiazione solare sul piano dei moduli - Sottocampo {user_subfield_name} ({subfield_name})"

                    # Dati per questo sottocampo
                    daily_data = subfield_data.get('monthly_avg_daily_array_irradiance', {})
                    classification_data = subfield_data.get('monthly_avg_daily_array_irradiance_classification', {})
                    monthly_data = subfield_data.get('monthly_plane_of_array_irradiance', {})

                    # Header
                    header_row = etree.SubElement(table, "row")
                    headers = [
                        "Mese",
                        "Irradiazione solare giornaliera sul piano dei moduli (kWh/m²/giorno)",
                        "Classificazione",
                        "Irradiazione solare mensile sul piano dei moduli (kWh/m²/mese)"
                    ]

                    for header in headers:
                        cell = etree.SubElement(header_row, "cell")
                        cell.text = header

                    # Righe dati
                    for month in MESI.keys():
                        row = etree.SubElement(table, "row")

                        # Mese
                        etree.SubElement(row, "cell").text = MESI[month]

                        # Irradiazione giornaliera
                        daily_value, daily_unit = daily_data.get(month, (None, None))
                        daily_text = f"{Common.format_value(daily_value)}" if daily_value is not None else ""
                        etree.SubElement(row, "cell").text = daily_text

                        # Classificazione
                        classification_values = classification_data.get(month, {})
                        threshold_name = classification_values.get("monthly_avg_daily_array_irradiance_classification_threshold_name", "")
                        etree.SubElement(row, "cell").text = threshold_name

                        # Irradiazione mensile
                        monthly_value, monthly_unit = monthly_data.get(month, (None, None))
                        monthly_text = f"{Common.format_value(monthly_value)}" if monthly_value is not None else ""
                        etree.SubElement(row, "cell").text = monthly_text

                    all_content.append(Common.generate_string_xml(table))

            # a livello di campo disegno il suo grafico
            all_content.append('<empty-line/>')
            img_path = f"{self.data['project_complete_path']}/{field_name}_irradiance_plane.png"
            img_str = f"<image src='{img_path}' width='17' style='center'/>"
            all_content.append(img_str)

        # Unisci tutto il contenuto
        return "\n\n".join(all_content)

    def create_table_unified_module_plane_irradiation_single(self):
        """
        Versione singola della tabella unificata
        """

        table = etree.Element("table", style="borders:TRBL;"
                                             "column-alignments: L-C-C-C;"
                                             "padding:1;"
                                             "width:14;"
                                             "width-cols:4;"
                                             "alignment:center;"
                                             "space-after:1")

        caption = etree.SubElement(table, "caption")
        caption.text = "Irradiazione solare sul piano dei moduli"

        # Dati principali
        daily_data = self.data.get('ao1', {}).get(
            'monthly_avg_daily_array_irradiance', {})
        classification_data = self.data.get('ao1', {}).get(
            'monthly_avg_daily_array_irradiance_classification', {})
        monthly_data = self.data.get('ao1', {}).get(
            'monthly_plane_of_array_irradiance', {})

        # Header
        header_row = etree.SubElement(table, "row")
        headers = [
            "Mese",
            "Irradiazione solare giornaliera sul piano dei moduli (kWh/m²/giorno)",
            "Classificazione",
            "Irradiazione solare mensile sul piano dei moduli (kWh/m²/mese)"
        ]

        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        # Righe dati
        for month in MESI.keys():
            row = etree.SubElement(table, "row")

            # Mese
            etree.SubElement(row, "cell").text = MESI[month]

            # Irradiazione giornaliera
            daily_value, daily_unit = daily_data.get(month, (None, None))
            daily_text = f"{Common.format_value(daily_value)}" if daily_value is not None else ""
            etree.SubElement(row, "cell").text = daily_text

            # Classificazione
            classification_values = classification_data.get(month, {})
            threshold_name = classification_values.get(
                "monthly_avg_daily_array_irradiance_classification_threshold_name", "")
            etree.SubElement(row, "cell").text = threshold_name

            # Irradiazione mensile
            monthly_value, monthly_unit = monthly_data.get(month, (None, None))
            monthly_text = f"{Common.format_value(monthly_value)}" if monthly_value is not None else ""
            etree.SubElement(row, "cell").text = monthly_text

        return Common.generate_string_xml(table)

    def create_text_yearly_module_plane_irradiation(self):
        """X24: Crea un testo per la irradiazione annuale sul piano dei moduli (annual_solar_radiation)."""

        value, unit = self.data.get('ao1', {}).get('annual_solar_radiation', (None, None))
        # Accesso corretto al valore total_annual_irradiance
        ao1_data = self.data.get('ao1', {})
        irrad_list = []
        ao1_subfields = ao1_data.get('ao1_subfields', {})
        if ao1_subfields:
            for subfield_name, subfield_data in ao1_subfields.items():
                annual_solar_radiation = subfield_data.get('annual_solar_radiation')
                if annual_solar_radiation[0]:
                    irrad_list.append(annual_solar_radiation[0])

        if irrad_list:
            irradiance_list_set = sorted(set(float(i) for i in irrad_list))
            if len(irradiance_list_set) > 1:
                # Lista con più valori
                min_value = irradiance_list_set[0]
                max_value = irradiance_list_set[-1]
                text_range = f"{min_value:.0f}-{max_value:.0f}"
            else:
                # Lista con un solo valore
                text_range = f"{irradiance_list_set[0]:.0f}"

            text_node = etree.Element("text")
            text_node.text = f"Totale energia irraggiata annua sul piano dei moduli = {text_range} kWh/m²/anno."

            return Common.generate_string_xml(text_node)
        else:
            return ""

    def create_text_clinometric_classification(self):
        """X31: Crea un testo per la classificazione dell'ombreggiamento clinometrico."""

        clinometry = self.data.get('clinometry', {})
        text_node = etree.Element("text")
        text = f"Le perdite di produzione a causa delle ombre mattutine e serali sono stimate " \
            f"in {clinometry['value']}.\n " \
            f"Secondo la seguente classificazione l’impianto si colloca nella classe di " \
            f"ombreggiamento clinometrico {clinometry['class']}"
        text_node.text = text

        return Common.generate_string_xml(text_node)

    def create_table_all_losses(self):
        """X32: Crea la tabella delle perdite."""

        labels_losses_keys = [
            ("Perdite per temperatura", "fixed_sys_monthly_temp_loss"),
            ("Perdite per riflessione", "fixed_sys_monthly_reflection_loss"),
            ("Perdite per sporcamento", "fixed_sys_monthly_soiling_loss"),
            ("Perdite per livello di irraggiamento",
             "fixed_sys_monthly_low_irradiance_loss"),
            ("Perdite per mismatching", "fixed_sys_monthly_mismatching_loss"),
            ("Perdite nei cavi", "fixed_sys_monthly_cable_loss"),
            ("Perdite inverter", "fixed_sys_monthly_inverter_loss"),
            ("Altre perdite di sistema", "fixed_sys_monthly_other_loss"),
            ("Perdite per ombreggiamento",
             "fixed_sys_monthly_shading_loss_percentage")
        ]

        # Accedi alla struttura corretta dei dati
        ao1_data = self.data.get('ao1', {})
        ao1_subfields = ao1_data.get('ao1_subfields', {})

        # Prendi il primo subfield disponibile (es. 'A1')
        first_subfield = None
        for subfield_key in ao1_subfields.keys():
            first_subfield = ao1_subfields[subfield_key]
            break
        losses = []
        if first_subfield:
            for label, key in labels_losses_keys:
                loss_value = 0.0
                loss_data = first_subfield.get(key, {})

                if isinstance(loss_data, dict) and 'GEN' in loss_data:
                    if isinstance(loss_data['GEN'], list) and len(loss_data['GEN']) > 0:
                        loss_value = loss_data['GEN'][0]

                losses.append((label, loss_value))

        else:
            # Se non trovo subfields, usa valori di default
            losses = [(label, 0.0) for label, _ in labels_losses_keys]
            print("Nessun subfield trovato, usando valori di default")

        table = etree.Element("table",
                              style="borders:TRBL;column-alignments:L-C;"
                              "padding:1;width-cols:6-5;alignment:center")
        etree.SubElement(table, "caption").text = TABLE_CAPTION["x32"]
        row = etree.SubElement(table, "row")
        etree.SubElement(row, "cell").text = 'Tipo di perdita'
        etree.SubElement(row, "cell").text = 'Valore della perdita (%)'

        for label, loss in losses:
            row = etree.SubElement(table, "row")
            etree.SubElement(row, "cell").text = label
            etree.SubElement(row, "cell").text = f"{loss:.2f}"

        return Common.generate_string_xml(table)

    def create_text_for_total_losses(self):
        """X33: Crea un testo per la definizione delle perdite totali."""

        value, unit = self.data.get('ao1', {}).get(
            'annual_loss_percentage', (0.0, "%"))
        text_node = etree.Element("text")
        text_node.text = f"La percentuale totale delle perdite di sistema è pari a {value}{unit}."

        return Common.generate_string_xml(text_node)

    def create_table_subfields_total_losses(self):
        """
        X33: Crea una tabella delle perdite totali per ogni sottocampo con:
        - Sottocampi
        - Percentuale totale delle perdite di sistema [%]
        """

        # Ottieni i dati dei sottocampi
        ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
        generator = self.data.get('generator', {})

        table = etree.Element(
            "table", style="borders:TRBL;column-alignments: L-C;padding:2")

        caption = etree.SubElement(table, "caption")
        caption.text = "Perdite totali di sistema per sottocampo"

        # Header
        header_row = etree.SubElement(table, "row")
        headers = [
            "Sottocampi",
            "Percentuale totale delle perdite di sistema [%]"
        ]

        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        # Righe dati per ogni sottocampo, organizzate per campo
        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    subfield_data = ao1_subfields[subfield_name]
                    user_subfield_name = subfield_data_gen.get('name', '')

                    # Ottieni le perdite totali dal sottocampo
                    annual_loss_percentage = subfield_data.get(
                        'annual_loss_percentage', (0.0, "%"))

                    # Se è una tupla (valore, unità), prendi il valore
                    if isinstance(annual_loss_percentage, (list, tuple)) and len(annual_loss_percentage) > 0:
                        loss_value = annual_loss_percentage[0]
                    else:
                        loss_value = annual_loss_percentage

                    # Formatta il valore delle perdite
                    try:
                        loss_str = f"{float(loss_value):.2f} %"
                    except (ValueError, TypeError):
                        loss_str = "N/A"

                    # Crea la riga con nome e codice del sottocampo
                    row = etree.SubElement(table, "row")
                    etree.SubElement(
                        row, "cell").text = f"{subfield_name} - {user_subfield_name}"
                    etree.SubElement(row, "cell").text = loss_str

        return Common.generate_string_xml(table)

    def create_text_for_total_losses_classification(self):
        """X34: Crea un testo per la classificazione delle perdite totali per ogni sottocampo."""

        # Ottieni le classificazioni delle perdite totali per ogni sottocampo
        subfields_classifications = self.data.get('ao1', {}).get(
            'subfields_annual_loss_percentage_classifications', [])

        if not subfields_classifications:
            # Fallback al comportamento originale se non ci sono sottocampi
            losses = self.data.get('ao1', {}).get(
                'annual_loss_percentage_classification', {})
            classify = losses.get('annual_loss_percentage_class', '')
            comment = losses.get('annual_loss_percentage_comment', '')
            text_node = etree.Element("text")
            text = f"La classificazione delle perdite di sistema dell'impianto di progetto associa l'impianto alla classe di perdite di sistema: {classify}.\n{comment}"
            text_node.text = text
            return Common.generate_string_xml(text_node)

        # Crea un contenitore per tutti i testi delle classificazioni
        all_content = []

        for subfield_name, loss_value, loss_class, loss_comment in subfields_classifications:
            text_node = etree.Element("text")
            text = f"{subfield_name}: La classificazione delle perdite di sistema dell'impianto di progetto associa questo sottocampo alla classe di perdite di sistema: {loss_class}.\n{loss_comment}"
            text_node.text = text
            all_content.append(Common.generate_string_xml(text_node))

        # Unisci tutto il contenuto
        return "\n\n".join(all_content)

    def create_text_annual_net_energy(self):
        """X41: Crea un testo per il valore di energia utile annua (senza ombreggiamenti)."""

        value, unit = self.data.get('ao1', {}).get(
            'annual_net_energy', (None, None))
        text_node = etree.Element("text")
        text_node.text = f"Il valore energia utile annua stimato per l’impianto in progettazione è pari a {value} kWh/m²/anno."

        return Common.generate_string_xml(text_node)

    def create_slogan_annual_net_energy(self):
        """X42: Crea slogan per ogni sottocampo con la classificazione dell'energia utile annua."""

        # Ottieni gli slogan generati per ogni sottocampo
        subfields_slogans = self.data.get('ao1', {}).get('subfields_annual_net_energy_slogans', [])

        # Crea un contenitore per tutti gli slogan
        container = etree.Element("container")

        # Aggiungi ogni slogan come elemento text separato
        for slogan in subfields_slogans:
            text_node = etree.SubElement(container, "text")
            text_node.text = slogan

        # Genera la stringa XML rimuovendo il container wrapper
        xml_string = Common.generate_string_xml(container)
        # Rimuovi i tag container per avere solo i testi
        xml_string = xml_string.replace('<container>', '').replace('</container>', '')

        return xml_string

    def create_text_annual_net_energy_classification(self):
        """X43: Crea un testo per la classificazione dell'energia utile annua."""

        values = self.data.get('ao1', {}).get(
            'annual_net_energy_classification', {})

        value = values.get('annual_net_energy_value', '')
        classify = values.get('annual_net_energy_class', '')
        comment = values.get('annual_net_energy_comment', '')

        text_node = etree.Element("text")
        text = f"Un valore di {value} kWh/m²/anno rientra nella classe {classify}. {comment}"
        text_node.text = text

        return Common.generate_string_xml(text_node)

    def create_table_monthly_net_energy(self):
        """X44: Crea una tabella con i valori di energia utile mensile per tutti i sottocampi, organizzata per campo."""

        # Ottieni i dati dei sottocampi
        ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
        generator = self.data.get('generator', {})

        all_content = []

        # Organizza i sottocampi per campo
        for field_name, field_data in generator.items():  # "A", "B"
            # Crea la lista dei sottocampi per questo campo
            subfield_list = []
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    user_subfield_name = subfield_data_gen.get('name', '')
                    display_name = f"Sottocampo: {subfield_name} - {user_subfield_name}" if user_subfield_name else subfield_name
                    subfield_list.append((subfield_name, display_name))

            if not subfield_list:
                continue

            # Aggiungi sottotitolo per il campo
            field_subtitle = etree.Element("subtitle")
            field_subtitle.text = f"Campo {field_name}"
            all_content.append(Common.generate_string_xml(field_subtitle))

            # Calcola l'allineamento delle colonne dinamicamente
            # Prima colonna per mese + N colonne per i sottocampi
            column_alignments = "L-" + "C-" * len(subfield_list)
            column_alignments = column_alignments.rstrip(
                '-')  # Rimuovi l'ultimo trattino

            table = etree.Element("table", style=f"borders:TRBL;column-alignments:{column_alignments};padding:2")

            caption = etree.SubElement(table, "caption")
            caption.text = f"Valori di energia utile mensile (kWh/m²/mese) - Campo {field_name}"

            # Header con "Mese" e tutti i sottocampi
            header_row = etree.SubElement(table, "row")
            etree.SubElement(header_row, "cell").text = "Mese"

            # Aggiungi i sottocampi come colonne
            for subfield_name, display_name in subfield_list:
                cell = etree.SubElement(header_row, "cell")
                cell.text = display_name

            # Righe dati per ogni mese
            months = list(MESI.keys())
            for month in months:
                row = etree.SubElement(table, "row")
                # Prima colonna: nome del mese
                etree.SubElement(row, "cell").text = MESI[month]

                # Colonne successive: valori per ogni sottocampo
                for subfield_name, display_name in subfield_list:
                    subfield_data = ao1_subfields.get(subfield_name, {})
                    monthly_net_energy = subfield_data.get(
                        'monthly_net_energy', {})

                    # Ottieni il valore per questo mese
                    monthly_value = monthly_net_energy.get(month, (0, ''))

                    # Se è una tupla (valore, unità), prendi il valore
                    if isinstance(monthly_value, (list, tuple)) and len(monthly_value) > 0:
                        value = monthly_value[0]
                    else:
                        value = monthly_value

                    # Formatta il valore
                    try:
                        formatted_value = f"{float(value):.2f}"
                    except (ValueError, TypeError):
                        formatted_value = "N/A"

                    etree.SubElement(row, "cell").text = formatted_value

            all_content.append(Common.generate_string_xml(table))

        # Unisci tutto il contenuto
        return "\n\n".join(all_content)

    def create_text_annual_energy_yield(self):
        """X45: Crea un testo e una tabella per la producibilità annua per sottocampi."""

        # Ottieni i dati dei sottocampi
        ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
        generator = self.data.get('generator', {})

        # Crea il testo introduttivo per i sottocampi
        text_node = etree.Element("text")
        text_node.text = ("Le simulazioni hanno stimato i seguenti valori di"
                          " producibilità annua (kWh/kWp) dell'impianto nei diversi sottocampi.")

        # Crea una singola tabella unificata
        table = etree.Element("table",
                              style="borders:TRBL;column-alignments: L-C;padding:2;width-cols:8-5;alignment:center;")

        caption = etree.SubElement(table, "caption")
        caption.text = "Producibilità annua per sottocampo"

        # Header
        header_row = etree.SubElement(table, "row")
        headers = [
            "Sottocampo",
            "Producibilità annua [kWh/kWp/anno]"
        ]

        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        # Righe dati per tutti i sottocampi
        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    user_subfield_name = subfield_data_gen.get('name', '')
                    subfield_data = ao1_subfields[subfield_name]

                    # Ottieni la producibilità annua dal sottocampo
                    annual_energy_yield = subfield_data.get('annual_energy_yield', (0, ''))

                    # Se è una tupla (valore, unità), prendi il valore
                    if isinstance(annual_energy_yield, (list, tuple)) and len(annual_energy_yield) > 0:
                        energy_value = annual_energy_yield[0]
                    else:
                        energy_value = annual_energy_yield

                    # Formatta il valore dell'energia
                    try:
                        energy_str = f"{float(energy_value):.2f}"
                    except (ValueError, TypeError):
                        energy_str = "N/A"

                    # Crea la riga per il sottocampo
                    row = etree.SubElement(table, "row")
                    etree.SubElement(
                        row, "cell").text = f"{subfield_name} - {user_subfield_name}" if user_subfield_name else subfield_name
                    etree.SubElement(row, "cell").text = energy_str

        # Combina testo introduttivo e tabella
        container = etree.Element("container")
        container.append(text_node)
        container.append(table)

        # Genera la stringa XML rimuovendo il container wrapper
        xml_string = Common.generate_string_xml(container)
        xml_string = xml_string.replace('<container>', '').replace('</container>', '')

        return xml_string

    def create_slogan_annual_energy_yield(self):
        """X46: Crea uno slogan per il valore di energia annua (senza ombreggiamenti)."""

        value, unit = self.data.get('ao1', {}).get('annual_energy_yield', (None, None))
        text_node = etree.Element("text")
        text_node.text = f"Producibilità annua: {value} kWh/m²/anno."

        return Common.generate_string_xml(text_node)

    def create_table_monthly_energy_yield(self):
        """X47: Crea una tabella con i valori di producibilità mensile per tutti i sottocampi, organizzata per campo."""

        # Ottieni i dati dei sottocampi
        ao1_subfields = self.data.get('ao1').get('ao1_subfields', {})
        generator = self.data.get('generator', {})
        all_content = []

        # Organizza i sottocampi per campo
        for field_name, field_data in generator.items():  # "A", "B"
            # Crea la lista dei sottocampi per questo campo
            subfield_list = []
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    user_subfield_name = subfield_data_gen.get('name', '')
                    display_name = f"Sottocampo: {subfield_name} - {user_subfield_name}" if user_subfield_name else subfield_name
                    subfield_list.append((subfield_name, display_name))

            if not subfield_list:
                continue

            # Aggiungi sottotitolo per il campo
            field_subtitle = etree.Element("subtitle")
            field_subtitle.text = f"Campo {field_name}"
            all_content.append(Common.generate_string_xml(field_subtitle))

            # Calcola l'allineamento delle colonne dinamicamente
            # Prima colonna per mese + N colonne per i sottocampi
            column_alignments = "L-" + "C-" * len(subfield_list)
            column_alignments = column_alignments.rstrip('-')  # Rimuovi l'ultimo trattino

            table = etree.Element(
                "table", style=f"borders:TRBL;column-alignments:{column_alignments};padding:2;")

            caption = etree.SubElement(table, "caption")
            caption.text = f"Valori di producibilità mensile (kWh/kWp) - Campo {field_name}"

            # Header con "Mese" e tutti i sottocampi
            header_row = etree.SubElement(table, "row")
            etree.SubElement(header_row, "cell").text = "Mese"

            # Aggiungi i sottocampi come colonne
            for subfield_name, display_name in subfield_list:
                cell = etree.SubElement(header_row, "cell")
                cell.text = display_name

            # Righe dati per ogni mese
            months = list(MESI.keys())
            for month in months:
                row = etree.SubElement(table, "row")
                # Prima colonna: nome del mese
                etree.SubElement(row, "cell").text = MESI[month]

                # Colonne successive: valori per ogni sottocampo
                for subfield_name, display_name in subfield_list:
                    subfield_data = ao1_subfields.get(subfield_name, {})
                    monthly_energy_yield = subfield_data.get('monthly_energy_yield', {})

                    # Ottieni il valore per questo mese
                    monthly_value = monthly_energy_yield.get(month, (0, ''))

                    # Se è una tupla (valore, unità), prendi il valore
                    if isinstance(monthly_value, (list, tuple)) and len(monthly_value) > 0:
                        value = monthly_value[0]
                    else:
                        value = monthly_value

                    # Formatta il valore
                    try:
                        formatted_value = f"{float(value):.2f}"
                    except (ValueError, TypeError):
                        formatted_value = "N/A"

                    etree.SubElement(row, "cell").text = formatted_value

            all_content.append(Common.generate_string_xml(table))

            # a livello di campo disegno il suo grafico
            all_content.append('<empty-line/>')
            img_path = f"{self.data['project_complete_path']}/{field_name}_energy_yield.png"
            img_str = f"<image src='{img_path}' width='17' style='center'/>"
            all_content.append(img_str)

        # Unisci tutto il contenuto
        return "\n\n".join(all_content)

    def create_table_annual_energy_production(self):
        """X48: Crea una tabella con i valori di energia elettrica teoricamente ottenibile per tutti i sottocampi."""

        ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
        sizing = self.data.get('sizing', {})
        generator = self.data.get('generator', {})

        # Crea la tabella
        table_node = etree.Element("table", style="borders:TRBL;column-alignments: L-C-C;padding:2")

        caption = etree.SubElement(table_node, "caption")
        caption.text = "Energia elettrica teoricamente ottenibile per ciascun sottocampo (kWh/anno)."

        header = etree.SubElement(table_node, "row")
        etree.SubElement(header, "cell").text = "Sottocampo"
        etree.SubElement(header, "cell").text = "Potenza installata [kWp]"
        etree.SubElement(header, "cell").text = "Energia elettrica teoricamente ottenibile [kWh/anno]"

        for field_key, subfields in sizing.items():
            for subfield_key, subfield in subfields.items():
                row_node = etree.SubElement(table_node, "row")
                subfield_name = generator.get(field_key, {}).get(subfield_key, {}).get('name', '')
                if subfield_name:
                    subfield_name = subfield_key
                energy_prod = ao1_subfields.get(subfield_key, {}).get('annual_energy_production', [''])[0]

                etree.SubElement(row_node, "cell").text = str(subfield_name)
                etree.SubElement(row_node, "cell").text = str(subfield.get('total_power', ''))
                etree.SubElement(row_node, "cell").text = str(energy_prod)

        row_node = etree.SubElement(table_node, "row")
        etree.SubElement(row_node, "cell").text = "Totale"
        etree.SubElement(row_node, "cell").text = str(self.data.get('generator_power', ''))
        etree.SubElement(row_node, "cell").text = str(self.data.get('ao1', {}).get('total_energy_production', ''))

        return Common.generate_string_xml(table_node)

    def create_table_system_efficiency(self):
        """X49: Crea una tabella con l'efficienza percentuale del sistema fotovoltaico per tutti i sottocampi."""

        # Ottieni i dati dei sottocampi
        ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
        generator = self.data.get('generator', {})
        # Crea una tabella per tutti i sottocampi
        table = etree.Element(
            "table", style="borders:TRBL;column-alignments: L-C;padding:2")

        caption = etree.SubElement(table, "caption")
        caption.text = "Efficienza percentuale del sistema fotovoltaico per sottocampo"

        # Header
        header_row = etree.SubElement(table, "row")
        headers = ["Sottocampo", "Efficienza percentuale del sistema fotovoltaico [%]"]

        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        # Righe dati per tutti i sottocampi
        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    user_subfield_name = subfield_data_gen.get('name', '')
                    subfield_data = ao1_subfields[subfield_name]

                    # Ottieni l'efficienza del sistema dal sottocampo
                    system_efficiency = subfield_data.get('system_efficiency', (0, ''))

                    # Se è una tupla (valore, unità), prendi il valore
                    if isinstance(system_efficiency, (list, tuple)) and len(system_efficiency) > 0:
                        efficiency_value = system_efficiency[0]
                    else:
                        efficiency_value = system_efficiency

                    # Formatta il valore dell'efficienza
                    try:
                        efficiency_str = f"{float(efficiency_value):.2f}%"
                    except (ValueError, TypeError):
                        efficiency_str = "N/A"

                    # Crea la riga per il sottocampo
                    row = etree.SubElement(table, "row")
                    etree.SubElement(
                        row, "cell").text = f"{subfield_name} - {user_subfield_name}" if user_subfield_name else subfield_name
                    etree.SubElement(row, "cell").text = efficiency_str

        return Common.generate_string_xml(table)

    def create_slogan_system_efficiency(self):
        """X50: Crea uno slogan per il valore di system_efficiency_classification per ogni sottocampo."""

        # Ottieni gli slogan generati per ogni sottocampo
        subfields_slogans = self.data.get('ao1', {}).get(
            'subfields_system_efficiency_slogans', [])

        # Crea un contenitore per tutti gli slogan
        container = etree.Element("container")

        # Aggiungi ogni slogan come elemento text separato
        for slogan in subfields_slogans:
            text_node = etree.SubElement(container, "text")
            text_node.text = slogan

        # Genera la stringa XML rimuovendo il container wrapper
        xml_string = Common.generate_string_xml(container)
        # Rimuovi i tag container per avere solo i testi
        xml_string = xml_string.replace(
            '<container>', '').replace('</container>', '')

        return xml_string

    def create_text_system_efficiency_classification(self):
        """X51: Crea un testo per la classificazione del system_efficiency_classification."""

        values = self.data.get('ao1', {}).get('system_efficiency_classification', {})

        value = values.get('system_efficiency_value', '')
        classify = values.get('system_efficiency_energy_class', '')
        comment = values.get('system_efficiency_energy_comment', '')

        text_node = etree.Element("text")
        text = f"Un valore di efficienza percentuale del {value}% rientra nella classe {classify}. {comment}"
        text_node.text = text

        return Common.generate_string_xml(text_node)

    def create_table_monthly_efficiency_percentage(self):
        """X52: Crea una tabella con i valori di efficienza percentuale mensile per tutti i sottocampi, organizzata per campo."""

        # Ottieni i dati dei sottocampi
        ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
        generator = self.data.get('generator', {})
        all_content = []

        # Organizza i sottocampi per campo
        for field_name, field_data in generator.items():  # "A", "B"
            # Crea la lista dei sottocampi per questo campo
            subfield_list = []
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    user_subfield_name = subfield_data_gen.get('name', '')
                    display_name = f"Sottocampo: {subfield_name} - {user_subfield_name}" if user_subfield_name else subfield_name
                    subfield_list.append((subfield_name, display_name))

            if not subfield_list:
                continue

            # Aggiungi sottotitolo per il campo
            field_subtitle = etree.Element("subtitle")
            field_subtitle.text = f"Campo {field_name}"
            all_content.append(Common.generate_string_xml(field_subtitle))

            # Calcola l'allineamento delle colonne dinamicamente
            # Prima colonna per mese + N colonne per i sottocampi
            column_alignments = "L-" + "C-" * len(subfield_list)
            column_alignments = column_alignments.rstrip(
                '-')  # Rimuovi l'ultimo trattino

            table = etree.Element(
                "table", style=f"borders:TRBL;column-alignments:{column_alignments};padding:2;")

            caption = etree.SubElement(table, "caption")
            caption.text = f"Valori di efficienza percentuale mensile (%) - Campo {field_name}"

            # Header con "Mese" e tutti i sottocampi
            header_row = etree.SubElement(table, "row")
            etree.SubElement(header_row, "cell").text = "Mese"

            # Aggiungi i sottocampi come colonne
            for subfield_name, display_name in subfield_list:
                cell = etree.SubElement(header_row, "cell")
                cell.text = display_name

            # Righe dati per ogni mese
            months = list(MESI.keys())
            for month in months:
                row = etree.SubElement(table, "row")
                # Prima colonna: nome del mese
                etree.SubElement(row, "cell").text = MESI[month]

                # Colonne successive: valori per ogni sottocampo
                for subfield_name, display_name in subfield_list:
                    subfield_data = ao1_subfields.get(subfield_name, {})
                    monthly_efficiency_percentage = subfield_data.get('monthly_efficiency_percentage', {})

                    # Ottieni il valore per questo mese
                    monthly_value = monthly_efficiency_percentage.get(
                        month, (0, ''))

                    # Se è una tupla (valore, unità), prendi il valore
                    if isinstance(monthly_value, (list, tuple)) and len(monthly_value) > 0:
                        value = monthly_value[0]
                    else:
                        value = monthly_value

                    # Formatta il valore
                    try:
                        formatted_value = f"{float(value):.2f}"
                    except (ValueError, TypeError):
                        formatted_value = "N/A"

                    etree.SubElement(row, "cell").text = formatted_value

            all_content.append(Common.generate_string_xml(table))

        # Unisci tutto il contenuto
        return "\n\n".join(all_content)

    def create_table_yearly_summary_production(self):
        """X53: Crea una tabella con i valori di produzione su base annuale per tutti i sottocampi."""

        ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
        sizing = self.data.get('sizing', {})
        generator = self.data.get('generator', {})

        # Crea la tabella
        # Crea la tabella per tutti i sottocampi
        table_node = etree.Element("table", style="borders:TRBL;column-alignments: L-C-C-C-C-C;padding:2")

        caption = etree.SubElement(table_node, "caption")
        caption.text = "Riassunto dei valori di producibilità su base annuale del generatore fotovoltaico."

        # Header
        header_row = etree.SubElement(table_node, "row")
        headers = [
            "Sottocampo",
            "Energia sul piano moduli [kWh/m²/anno]",
            "Energia utile [kWh/m²/anno]",
            "Efficienza del sistema [%]",
            "Producibilità specifica [kWh/kWp]",
            "Energia elettrica prodotta [kWh/anno]"
        ]

        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        for field_key, subfields in sizing.items():
            for subfield_key, subfield in subfields.items():
                row_node = etree.SubElement(table_node, "row")
                subfield_name = generator.get(field_key, {}).get(subfield_key, {}).get('name', '')
                if subfield_name:
                    subfield_name = subfield_key

                energy_module = ao1_subfields.get(subfield_key, {}).get('annual_solar_radiation', [''])[0]
                energy_net = ao1_subfields.get(subfield_key, {}).get('annual_net_energy', [''])[0]
                efficiency = ao1_subfields.get(subfield_key, {}).get('system_efficiency', [''])[0]
                prod_spec = ao1_subfields.get(subfield_key, {}).get('annual_energy_yield', [''])[0]
                energy_prod = ao1_subfields.get(subfield_key, {}).get('annual_energy_production', [''])[0]

                etree.SubElement(row_node, "cell").text = str(subfield_name)
                etree.SubElement(row_node, "cell").text = str(energy_module)
                etree.SubElement(row_node, "cell").text = str(energy_net)
                etree.SubElement(row_node, "cell").text = str(efficiency)
                etree.SubElement(row_node, "cell").text = str(prod_spec)
                etree.SubElement(row_node, "cell").text = str(energy_prod)

        return Common.generate_string_xml(table_node)

    # Crea una tabella mensile di sintesi della produzione per ogni sottocampo
    def create_table_montly_summary_production(self):
        """
        X54: Crea una tabella a 4 colonne per i valori di produzione mensili per ogni sottocampo.
        """
        ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
        generator = self.data.get('generator', {})
        all_content = []

        # Organizza i sottocampi per campo
        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    user_subfield_name = subfield_data_gen.get('name', '')
                    display_name = f"Sottocampo: {subfield_name} - {user_subfield_name}" if user_subfield_name else subfield_name

                    # Sottotitolo per il sottocampo
                    subtitle = etree.Element("subtitle")
                    subtitle.text = display_name
                    all_content.append(Common.generate_string_xml(subtitle))

                    subfield_data = ao1_subfields[subfield_name]
                    monthly_energy_yield = subfield_data.get('monthly_energy_yield', {})
                    monthly_efficiency_percentage = subfield_data.get('monthly_efficiency_percentage', {})
                    monthly_net_energy = subfield_data.get('monthly_net_energy', {})

                    table = etree.Element("table", style="borders:TB")
                    caption = etree.SubElement(table, "caption")
                    caption.text = "Sintesi mensile della produzione"

                    header_row = etree.SubElement(table, "row")
                    headers = [
                        "Mese",
                        "Producibilità mensile (kWh/kWp)",
                        "Valori di energia utile mensile [kWh/m2 mese]",
                        "Efficienza percentuale mensile (%)"
                    ]
                    for header in headers:
                        cell = etree.SubElement(header_row, "cell")
                        cell.text = header

                    for month in MESI.keys():
                        row = etree.SubElement(table, "row")
                        # Nome del mese
                        etree.SubElement(row, "cell").text = MESI[month]
                        etree.SubElement(row, "cell").text = str(
                            Common.format_value(monthly_energy_yield.get(month, (0.0,))[0]))
                        etree.SubElement(row, "cell").text = str(
                            Common.format_value(monthly_net_energy.get(month, (0.0,))[0]))
                        etree.SubElement(row, "cell").text = str(
                            Common.format_value(monthly_efficiency_percentage.get(month, (0.0,))[0]))

                    all_content.append(Common.generate_string_xml(table))

        return "\n\n".join(all_content)

    def create_table_emission_reduction(self):
        """X60: Crea una tabella con i valori di riduzione delle emissioni per tutti i sottocampi."""

        # Ottieni i dati della tabella di riduzione delle emissioni
        emission_reduction_table_data = self.data.get(
            'ao1', {}).get('emission_reduction_table_data', [])

        # Crea la tabella per tutti i sottocampi
        table = etree.Element(
            "table", style="borders:TRBL;column-alignments: L-C-C;padding:2")

        caption = etree.SubElement(table, "caption")
        caption.text = "Riduzione stimata (20 anni)"

        # Header
        header_row = etree.SubElement(table, "row")
        headers = [
            "Sottocampi",
            "Tonnellate equivalenti di petrolio [TEP]",
            "Riduzione di gas serra CO2-eq. [t. di CO2]"
        ]

        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        # Righe dati per tutti i sottocampi (inclusa la riga totale)
        for subfield_name, tep_value, co2_value in emission_reduction_table_data:
            row = etree.SubElement(table, "row")

            # Nome del sottocampo
            etree.SubElement(row, "cell").text = subfield_name

            # Valore TEP
            try:
                tep_str = f"{float(tep_value):.2f}"
            except (ValueError, TypeError):
                tep_str = "N/A"
            etree.SubElement(row, "cell").text = tep_str

            # Valore CO2
            try:
                co2_str = f"{float(co2_value):.2f}"
            except (ValueError, TypeError):
                co2_str = "N/A"
            etree.SubElement(row, "cell").text = co2_str

        return Common.generate_string_xml(table)

    def create_table_subfields_summary(self):
        """
        Crea una tabella riassuntiva per ogni sottocampo con:
        - Sottocampo
        - Orientamento (rispetto al sud) [gradi]
        - Inclinazione [gradi]
        - Totale energia irraggiata annua sul piano dei moduli [kWh/m²/anno]
        """

        # Ottieni i dati dei sottocampi
        ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
        generator = self.data.get('generator', {})
        table = etree.Element(
            "table", style="borders:TRBL;column-alignments: L-C-C-C;padding:2")

        caption = etree.SubElement(table, "caption")
        caption.text = "Riepilogo parametri sottocampi"

        # Header
        header_row = etree.SubElement(table, "row")
        headers = [
            "Sottocampo",
            "Orientamento (rispetto al sud) [gradi]",
            "Inclinazione [gradi]",
            "Totale energia irraggiata annua sul piano dei moduli [kWh/m²/anno]"
        ]

        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        # Righe dati per tutti i sottocampi (senza divisione per campo)
        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    user_subfield_name = subfield_data.get('name', '')
                    # Ottieni i parametri del sottocampo
                    azimuth = subfield_data.get('azimuth', 0)
                    inclination = subfield_data.get('inclination', 0)
                    if azimuth == 0:
                        orientation = 180
                    elif azimuth == 180:
                        orientation = 0
                    elif azimuth > 180:
                        orientation = azimuth - 180
                    else:
                        orientation = azimuth - 180

                    orientation_str = f"{orientation:+.0f}°" if orientation != 0 else "0°"

                    subfield_ao1 = ao1_subfields.get(subfield_name, {})
                    annual_energy = subfield_ao1.get('annual_solar_radiation', 0)

                    if isinstance(annual_energy, (list, tuple)) and len(annual_energy) > 0:
                        annual_energy = annual_energy[0]

                    try:
                        annual_energy_str = f"{float(annual_energy):.2f}"
                    except (ValueError, TypeError):
                        annual_energy_str = "N/A"

                    row = etree.SubElement(table, "row")
                    etree.SubElement(
                        row, "cell").text = f"{subfield_name} - {user_subfield_name}"
                    etree.SubElement(row, "cell").text = orientation_str
                    etree.SubElement(row, "cell").text = f"{inclination}°"
                    etree.SubElement(row, "cell").text = annual_energy_str

        return Common.generate_string_xml(table)

    def create_table_subfields_annual_net_energy(self):
        """
        X41
        Crea una tabella con l'energia utile annua per ogni sottocampo:
        - Sottocampo
        - Energia utile annua [kWh/m²/anno]
        """

        # Ottieni i dati dei sottocampi
        ao1_subfields = self.data.get('ao1', {}).get('ao1_subfields', {})
        generator = self.data.get('generator', {})
        # Crea il testo introduttivo
        intro_text = etree.Element("text")
        intro_text.text = ("Il valore energia utile annua stimato per l'impianto in progettazione "
                           "nei diversi sottocampi è riportato nella seguente tabella.")

        # Crea una singola tabella unificata
        table = etree.Element("table", style="borders:TRBL;column-alignments: L-C;padding:2")

        caption = etree.SubElement(table, "caption")
        caption.text = "Energia utile annua per sottocampo (kWh/m²/anno)."

        # Header
        header_row = etree.SubElement(table, "row")
        headers = [
            "Sottocampo",
            "Energia utile annua [kWh/m²/anno]"
        ]

        for header in headers:
            cell = etree.SubElement(header_row, "cell")
            cell.text = header

        # Righe dati per tutti i sottocampi
        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name not in ao1_subfields:
                    continue

                user_subfield_name = subfield_data_gen.get('name', '')
                subfield_data = ao1_subfields[subfield_name]

                # Ottieni l'energia utile annua dal sottocampo
                annual_net_energy = subfield_data.get('annual_net_energy', (0, ''))

                # Se è una tupla (valore, unità), prendi il valore
                if isinstance(annual_net_energy, (list, tuple)) and len(annual_net_energy) > 0:
                    energy_value = annual_net_energy[0]
                else:
                    energy_value = annual_net_energy

                # Formatta il valore dell'energia
                try:
                    energy_str = f"{float(energy_value):.2f}"
                except (ValueError, TypeError):
                    energy_str = "N/A"

                # Crea la riga per il sottocampo
                row = etree.SubElement(table, "row")
                etree.SubElement(row, "cell").text = f"{subfield_name} - {user_subfield_name}"
                etree.SubElement(row, "cell").text = energy_str

        return Common.generate_string_xml(table)

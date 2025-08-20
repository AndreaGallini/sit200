"""
e_checks.py
Classe che gestisce la costruzione delle stringhe xml relative alle verifiche.
"""
from lxml import etree

from .common import Common


class EChecks:

    def __init__(self, data):
        self.data = data

    def create_text_power_compatibility(self):
        """X140: Crea un testo per la Compatibilità della potenza tra generatore fotovoltaico e inverter (J3)."""

        '''
        {'generator_inverter_ratio': ['tasso', 1.004], 
        'dc_ac_ratio': ['tasso', 0.996], 
        'rp_compatibility': ['verità', 1], 
        'ac_dc_compatibility': ['verità', 0], 
        'power_compliance': ['verità', 1],
         'rp_comment': ['commento', 'Conforme. Per l’impianto fotovoltaico in esame il rapporto Rp tra la potenza dell’inverter e la potenza del generatore fotovoltaico è pari a 1.00.'], 
         'dc_ac_ratio_comment': ['commento', 'NON conforme. L’inverter non è adeguatamente dimensionato rispetto ai moduli.']}
        '''
        compat = self.data.get('echecks', {}).get('generatorinvertercompatibility', {})
        if compat:
            ac_dc_compatibility = compat.get('ac_dc_compatibility', [])
            power_compliance = compat.get('power_compliance', [])
            if len(power_compliance) < 2 or len(ac_dc_compatibility) < 2:
                return ""
        else:
            return ""

        # Crea il nodo principale
        tag_node = etree.Element('tag_to_remove')

        if ac_dc_compatibility[1]:
            ratio = compat['dc_ac_ratio'][1]

            txt = "Solitamente, per dimensionare correttamente un sistema fotovoltaico generatore-inverter " \
                  "si tiene conto di un rapporto tra potenza nominale del generatore e potenza nominale dell’inverter " \
                  "(denominato rapporto DC/AC ratio) compreso tra 1.0 e 1.2."
            etree.SubElement(tag_node, "text").text = txt

            table_node = etree.SubElement(tag_node, "table", attrib={"style": "column-alignments:C"})
            row_node = etree.SubElement(table_node, "row")
            cell_node = etree.SubElement(row_node, "cell")
            cell_node.text = "1.0 <= DC/AC Ratio <= 1.2"

            texts = [
                "Un DC/AC ratio compreso tra 1 e 1.2 indica un sovradimensionamento moderato del campo fotovoltaico "
                "rispetto alla potenza nominale dell’inverter, permettendo di ottimizzare la produzione energetica "
                "nelle ore di bassa irradiazione e massimizzare l’utilizzo dell’inverter, "
                "con un rischio limitato di clipping nelle ore di picco.",
                f"Per l’impianto fotovoltaico in esame il rapporto DC/AC ratio tra potenza potenza del generatore fotovoltaico e "
                f"potenza dell’inverter è pari a {ratio}.",
                "Quindi si può considerare pienamente compatibile l'accoppiamento tra generatore e inverter, "
                "garantendo la massima efficienza dell'inverter nella maggior parte delle condizioni operative. "

            ]
            for txt in texts:
                text_node = etree.SubElement(tag_node, "text")
                text_node.text = txt

        elif power_compliance[1]:
            ratio = compat['generator_inverter_ratio'][1]

            txt = "Solitamente, per dimensionare correttamente un sistema fotovoltaico generatore-inverter " \
                  "si tiene conto di un rapporto tra potenza nominale dell’inverter e potenza nominale del generatore " \
                  "(denominato rapporto P%) compreso tra 0.78 e 1.15."
            etree.SubElement(tag_node, "text").text = txt

            table_node = etree.SubElement(tag_node, "table", attrib={"style": "column-alignments:C"})
            row_node = etree.SubElement(table_node, "row")
            cell_node = etree.SubElement(row_node, "cell")
            cell_node.text = "0.78 < P% < 1.15"

            texts = [
                f"Per l’impianto fotovoltaico in esame il rapporto P% tra potenza dell’inverter e "
                f"potenza del generatore fotovoltaico è pari a {ratio}.",

                "Quindi si può considerare pienamente compatibile l'accoppiamento tra generatore e inverter, "
                "garantendo la massima efficienza dell'inverter nella maggior parte delle condizioni operative. "
                "La riduzione delle perdite minime per clipping, con un generatore che lavora in modo stabile e sicuro "
                "e un buon sfruttamento del generatore anche in condizioni di irraggiamento più deboli."
            ]

            for txt in texts:
                text_node = etree.SubElement(tag_node, "text")
                text_node.text = txt
        else:
            return ""

        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_text_voltage_subfields(self):
        """X141: Crea un testo per la Compatibilità della finestra MPPT per i sottocampi (J5)."""

        '''
        {'inverter_max_input_voltage': ['V', 530], 
        'inverter_min_input_voltage': ['V', 650], 
        'max_voltage_operating_string_min_temperature': ['V', [449.5, 449.5]], 
        'min_voltage_operating_string_max_temperature': ['V', [371.11, 371.11]], 
        'inverter_string_mpp_vmin_compatibility': ['verità', [0, 0]], 
        'inverter_string_mpp_vmin_compatibility_comment': ['verità', ['NON Conforme. La tensione massima della 
        stringa supera la tensione massima accettata dall’inverter o è inferiore alla tensione minima d’ingresso
         accettata dal MPPT dell’inverter.', 'NON Conforme. La tensione massima della stringa supera la tensione 
         massima accettata dall’inverter o è inferiore alla tensione minima d’ingresso accettata dal MPPT 
         dell’inverter.']], 
         'inverter_string_mpp_vmax_compatibility': ['verità', [0, 0]], 
         'inverter_string_mpp_vmax_compatibility_comment': ['verità', ['NON Conforme. La tensione minima della 
         stringa supera la tensione massima accettata dall’inverter o è inferiore alla tensione minima d’ingresso 
         accettata dal MPPT dell’inverter. ', 'NON Conforme. La tensione minima della stringa supera la tensione 
         massima accettata dall’inverter o è inferiore alla tensione minima d’ingresso accettata dal MPPT 
         dell’inverter. ']]}
        '''
        compat = self.data.get('echecks', {}).get('stringoperatingmpptcompatibility', {})

        tag_node = etree.Element('tag_to_remove')

        txt = "Nell’impianto in progetto i valori per la verifica della compatibilità con l'inverter sono i seguenti:"
        etree.SubElement(tag_node, "text").text = txt

        texts = []
        for i, max_voltages in enumerate(compat['max_voltage_operating_string_min_temperature'][1]):
            texts.append(
                f"Stringa {i+1} VstringaTmin,i ≤ VmppMax,inv = {max_voltages} V ≤ {compat['inverter_max_input_voltage'][1]} V = compatibile"
            )
        for i, min_voltages in enumerate(compat['min_voltage_operating_string_max_temperature'][1]):
            texts.append(
                f"Stringa {i+1} VstringaTmax,i ≥ VmppMin,inv = {min_voltages} V ≥ {compat['inverter_min_input_voltage'][1]} V = compatibile"
            )
        for txt in texts:
            text_node = etree.SubElement(tag_node, "text")
            text_node.text = txt

        txt = "L'inverter è compatibile con la stringa poiché le tensioni rientrano nella finestra " \
              "di lavoro MPPT dell’inverter."
        etree.SubElement(tag_node, "text").text = txt

        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_text_current_compatibility(self):
        """X142:rea un testo per la Compatibilità della Corrente Massima Ingresso MPPT Inverter (J7)."""

        '''
        {'module_max_current_tmax': ['A', 6.72], 
        'tracker_max_current': ['A', 22.0], 
        'current_mppt': ['A', 6.72], 
        'required_parallel_strings': ['numero', 1], 
        'current_mppt_compatibility': ['boolean', 1], 
        'current_mppt_compatibility_comment': ['string', "Conforme. La corrente generata dalla stringa 
        rispetta il limite massimo di ingresso del MPPT dell'inverter, garantendo il corretto funzionamento 
        del sistema senza rischio di sovraccarico."]}
        '''
        compat = self.data.get('echecks', {}).get('currentmpptcompatibility', {})

        tag_node = etree.Element('tag_to_remove')

        texts = [
            "I valori dell’impianto fotovoltaico previsto relativi alla verifica della corretta compatibilità tra "
            "corrente massima di ingresso per l'inverter e le caratteristiche dell’inverter stesso sono i seguenti:",

            f"Corrente massima di ingresso all’inverter, come riportato nella scheda tecnica "
            f"dell'inverter per ogni ingresso MPPT: {compat['tracker_max_current'][1]} A",
            f"Corrente totale in ingresso all’inverter: {compat['module_max_current_tmax'][1]} A",
            f"Numero di stringhe in parallelo necessarie per MPPT: {compat['required_parallel_strings'][1]}",

            "Quindi si può considerare pienamente compatibile l'accoppiamento tra generatore e inverter, "
            "garantendo la massima efficienza dell'inverter nella maggior parte delle condizioni operative. "
            "La riduzione delle perdite minime per clipping, con un generatore che lavora in modo stabile e sicuro "
            "e un buon sfruttamento del generatore anche in condizioni di irraggiamento più deboli."
        ]
        for txt in texts:
            text_node = etree.SubElement(tag_node, "text")
            text_node.text = txt

        table_node = etree.SubElement(tag_node, "table", attrib={"style": "column-alignments:C"})
        row_node = etree.SubElement(table_node, "row")
        cell_node = etree.SubElement(row_node, "cell")
        cell_node.text = f"Imax,PV ≤ Imax,inv = {compat['module_max_current_tmax'][1]} A ≤ {compat['tracker_max_current'][1]} A"

        texts = [
            "Dove:",
            "Imax,PV = Max corrente generatore [A]",
            "Imax,inv = Max corrente CC in ingresso inverter [A], fornita dalla scheda tecnica",
            "Il sistema è compatibile poiché la corrente totale non supera il limite massimo gestibile dall'inverter.",
        ]
        for txt in texts:
            text_node = etree.SubElement(tag_node, "text")
            text_node.text = txt

        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_text_n_inputs_compatibility(self):
        """X143: crea un testo per la Compatibilità del numero di ingressi dell'inverter (J6)."""

        '''
        {'string_group_number': ['number', 1.0], 
        'mppt_input_number': ['number', 2], 
        'mppt_input_compatibility': ['boolean', 1], 
        'mppt_input_compatibility_comment': ['string', 'Conforme. Gli ingressi MPPT dell’inverter sono adeguati per gestire tutti i gruppi di stringhe.'], 'inverter_mppt_compatibility': ['boolean', 1], 'inverter_mppt_compatibility_comment': ['string', 'Conforme. Gli ingressi MPPT dell’inverter sono adeguati per gestire tutti i gruppi di stringhe.']}
        '''
        compat = self.data.get('echecks', {}).get('stringgroupinverterinputcompatibility', {})

        tag_node = etree.Element('tag_to_remove')

        texts = [
            "Considerando il presente impianto fotovoltaico otteniamo:",
            f"Numero di ingressi inverter MPPT: {compat['mppt_input_number'][1]}\n"
            f"Numero di paralleli: {int(compat['string_group_number'][1])}",
            "Il numero di paralleli è inferiore o uguale al numero di ingressi MPPT dell’inverter."
        ]
        for txt in texts:
            text_node = etree.SubElement(tag_node, "text")
            text_node.text = txt

        table_node = etree.SubElement(tag_node, "table", attrib={"style": "column-alignments:C"})
        row_node = etree.SubElement(table_node, "row")
        cell_node = etree.SubElement(row_node, "cell")
        cell_node.text = f"{int(compat['string_group_number'][1])} ≤ {compat['mppt_input_number'][1]}"

        txt = "Gli ingressi MPPT dell’inverter sono adeguati per gestire tutti i gruppi di stringhe."
        etree.SubElement(tag_node, "text").text = txt

        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

    def create_text_voc_compatibility(self):
        """X144: Crea un testo per la Compatibilità della tensione a vuoto Voc delle stringhe (J4)."""

        '''
        {'max_voc_string_min_temperature': ['V', 527.44], 
        'voltage_at_closed_circuit': 
        'string_configuration_compliance': ['verità', 1], 
        'string_configuration_compliance_comment': ['commento', 'Conforme: La tensione massima della stringa in 
        condizioni di freddo estremo è inferiore o uguale alla tensione massima d’ingresso dell’inverter.']}
        '''
        compat = self.data.get('echecks', {}).get('stringvocmpptcompatibility', {})

        tag_node = etree.Element('tag_to_remove')

        texts = [
            f"Tensione massima di ingresso dell'inverter specificata dal produttore: {compat['voltage_at_closed_circuit'][1]} V",
            f"Tensione a vuoto della stringa in condizioni di freddo estremo: {compat['max_voc_string_min_temperature'][1]} V",
        ]
        for txt in texts:
            text_node = etree.SubElement(tag_node, "text")
            text_node.text = txt

        table_node = etree.SubElement(tag_node, "table", attrib={"style": "column-alignments:C"})
        row_node = etree.SubElement(table_node, "row")
        cell_node = etree.SubElement(row_node, "cell")
        cell_node.text = f"Vmax,PV ≤ Vmax,inv = {int(compat['max_voc_string_min_temperature'][1])} ≤ {compat['voltage_at_closed_circuit'][1]}"

        texts = [
            "Dove:",
            "Vmax,PV = Max tensione di stringa in condizioni di temperatura minima [V];",
            "Vmax,inv = Max tensione in ingresso dell'inverter [V], fornita dalla scheda tecnica.",
            "Poiché il valore di tensione VOC è inferiore alla massima tensione in ingresso inverter "
            "la configurazione della stringa è compatibile con l'inverter.",
        ]
        for txt in texts:
            text_node = etree.SubElement(tag_node, "text")
            text_node.text = txt

        string = Common.generate_string_xml(tag_node)
        cleaned_string = string.replace("<tag_to_remove>", "").replace("</tag_to_remove>", "")

        return cleaned_string

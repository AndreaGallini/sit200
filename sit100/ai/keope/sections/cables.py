"""
ccables.py
Classe che gestisce la costruzione delle tabelle xml relative ai cavi.
"""
import os

from lxml import etree

from .common import Common


class Cables:

    def __init__(self, data):
        self.data = data

    def create_table_cable_sections(self):
        """X110: Crea la tabella delle tipologie di cavi e loro caratteristiche, in base a potenza."""
        # ATTENZIONE: fisso a 100 il max potenza impianto per scrivere
        generator_power = min(self.data.get("generator_power", 0), 100)
        content = ""
        if generator_power < 6:
            content = """<table style="borders:TRBL;width-cols:2-2-5;font-size:9">
            <row>
                <cell>Tipo di cavi</cell>
                <cell>Denominazione</cell>
                <cell>Caratteristiche tecniche</cell>
                <cell>Utilizzi</cell>
                <cell>Criteri di qualità</cell>
            </row>
            <row>
                <cell>Cavi solari</cell>
                <cell>PV1-F</cell>
                <cell>Cavo solare 4-6 mm². Doppio isolamento, resistenza ai raggi UV, temperatura di esercizio da -40°C a +90°C, tensione nominale 600/1000V AC e 1800V DC, resistente agli agenti atmosferici.</cell>
                <cell>Collegamento tra moduli fotovoltaici e verso le scatole di giunzione o i connettori MC4.</cell>
                <cell>Certificazione TÜV e/o IEC 62930, alta durabilità, buona resistenza meccanica, durata attesa ≥ 25 anni.</cell>
            </row>
            <row>
                <cell>Cavi DC</cell>
                <cell>Solar DC Cable</cell>
                <cell>6-10 mm² cavo unipolare. Isolamento XLPE o EPR, temperatura da -40°C a +120°C, tensione nominale 1000V DC, resistente ai raggi UV e agli agenti chimici.</cell>
                <cell>Collegamento tra stringhe fotovoltaiche e inverter, o tra scatole di campo e inverter.</cell>
                <cell>Conformità IEC 62930, alta flessibilità e resistenza all’abrasione, adatto a posa fissa e mobile.</cell>
            </row>
            <row>
                <cell>Cavi AC</cell>
                <cell>Solar AC Cable</cell>
                <cell>10-16 mm² tipo NYY. Isolamento PVC o XLPE, tensione nominale 600/1000V AC, temperatura da -40°C a +90°C, resistenza moderata a UV e agenti chimici.</cell>
                <cell>Collegamento tra inverter e quadro elettrico di campo o contatore di scambio.</cell>
                <cell>Certificazione CE, buona conduttività elettrica, resistenza all’umidità e raggi UV, idoneità per uso residenziale.</cell>
            </row>
            <row>
                <cell>Cavi di messa a terra</cell>
                <cell>H07V-K</cell>
                <cell>6-16 mm². Isolamento in PVC, tensione nominale 450/750V, temperatura da -25°C a +70°C, struttura flessibile a fili sottili.</cell>
                <cell>Collegamento tra le strutture di supporto, i moduli e il nodo di messa a terra generale.</cell>
                <cell>Certificazione CE,facilità di posa anche in spazi ristretti, buona resistenza meccanica e corrosiva.</cell>
            </row>
            <row>
                <cell>Cavi accumulo</cell>
                <cell>Solar battery cable</cell>
                <cell>16-25 mm². Isolamento resistente a temperature elevate (fino a 90°C), raggi UV, con classe di isolamento secondo IEC 62930 o IEC 60228.</cell>
                <cell>Connessione tra inverter ibrido e batterie di accumulo (lato DC o AC).</cell>
                <cell>Sezione adeguata per le correnti di carica/scarica, bassa caduta di tensione, isolamento rinforzato per impieghi in sicurezza.</cell>
            </row>
            <row>
                <cell>Cavi per comunicazione</cell>
                <cell>Solar Communication Cable</cell>
                <cell>Cavo CAT5e/CAT6. Isolamento in PVC o LSZH, tensione nominale 300V, temperatura da -20°C a +70°C, schermatura anti-EMI.</cell>
                <cell>Collegamento tra inverter, datalogger, contatore di energia e sistemi di monitoraggio locale o remoto.</cell>
                <cell>Conformità RS485 o Modbus, schermatura per evitare disturbi, posa semplificata, compatibilità con monitoraggio residenziale.</cell>
            </row>
        </table>"""
        elif generator_power < 10:
            content = """<table style="borders:TRBL;width-cols:2-2-5;font-size:9">
            <row>
                <cell>Tipo di cavi</cell>
                <cell>Denominazione</cell>
                <cell>Caratteristiche tecniche</cell>
                <cell>Utilizzi</cell>
                <cell>Criteri di qualità</cell>
            </row>
            <row>
                <cell>Cavi solari</cell>
                <cell>PV1-F</cell>
                <cell>Cavo solare 6–10 mm². Doppio isolamento, resistente ai raggi UV, temperatura di esercizio da -40°C a +90°C, tensione nominale 600/1000V AC, 1800V DC, resistenza ad agenti atmosferici e trazione.</cell>
                <cell>Collegamento tra moduli FV e verso le scatole di giunzione, adatto a correnti superiori a 15 A per stringhe più lunghe.</cell>
                <cell>Certificazione TÜV e/o IEC 62930, alta durabilità, lunga vita operativa (≥25 anni), adatto a posa esterna anche in zone critiche.</cell>
            </row>
            <row>
                <cell>Cavi DC</cell>
                <cell>Solar DC Cable</cell>
                <cell>10–16 mm² cavo unipolare. Isolamento XLPE o EPR, tensione nominale 1500V DC, temperatura da -40°C a +120°C, elevata resistenza UV e chimica, ottima flessibilità.</cell>
                <cell>Collegamento tra stringhe e inverter, o tra quadri di campo e inverter in configurazioni centralizzate.</cell>
                <cell>Conformità a IEC 62930, buona resistenza meccanica, indicato per impianti medio-piccoli con distanze fino a 40 m.</cell>
            </row>
            <row>
                <cell>Cavi AC</cell>
                <cell>Solar AC Cable</cell>
                <cell>16–25 mm² tipo NYY o FG7OR. Isolamento PVC o XLPE, tensione nominale 600/1000V AC, temperatura da -40°C a +90°C, resistenza ai raggi UV e all’umidità elevata.</cell>
                <cell>Collegamento tra inverter e quadro di distribuzione, o verso il punto di connessione alla rete elettrica.</cell>
                <cell>Certificazione CE, bassa impedenza, idoneo alla distribuzione trifase, verificabile secondo CEI 64-8 o CEI 0-21.</cell>
            </row>
            <row>
                <cell>Cavi di messa a terra</cell>
                <cell>H07V-K</cell>
                <cell>16–25 mm². Isolamento in PVC, tensione nominale 450/750V, temperatura di esercizio da -25°C a +70°C, alta flessibilità, struttura a fili sottili, resistente alla corrosione.</cell>
                <cell>Collegamenti equipotenziali tra strutture metalliche, moduli, inverter e nodo di terra generale.</cell>
                <cell>Certificazione CE, sezione adeguata alla corrente di guasto, conforme a CEI 64-8 e protezioni SPD.</cell>
            </row>
            <row>
                <cell>Cavi accumulo</cell>
                <cell>Solar battery cable</cell>
                <cell>25–35 mm². Isolamento rinforzato per alte temperature (fino a 120°C), elevata resistenza ai raggi UV, sezione idonea a correnti elevate di carica/scarica.</cell>
                <cell>Collegamento tra inverter ibrido e sistema di accumulo, o tra quadri DC e batterie.</cell>
                <cell>Conforme a IEC 60228 e 62930, sezione verificata in base a intensità di corrente e caduta di tensione ammessa.</cell>
            </row>
            <row>
                <cell>Cavi per comunicazione</cell>
                <cell>Solar Communication Cable</cell>
                <cell>Cavo CAT6 FTP o RS485 schermato. Isolamento LSZH o PVC, tensione nominale 300V, temperatura da -20°C a +70°C, schermatura per eliminare interferenze EMI.</cell>
                <cell>Collegamento tra inverter, sensori ambientali, sistemi di monitoraggio remoto e dispositivi SCADA.</cell>
                <cell>Conformità a RS485, Modbus o Ethernet TCP/IP. Ottimizzato per tracciamento, controllo e diagnosi remota.</cell>
            </row>
        </table>"""
        elif generator_power < 20:
            content = """<table style="borders:TRBL;width-cols:2-2-5;font-size:9">
            <row>
                <cell>Tipo di cavi</cell>
                <cell>Denominazione</cell>
                <cell>Caratteristiche tecniche</cell>
                <cell>Utilizzi</cell>
                <cell>Criteri di qualità</cell>
            </row>
            <row>
                <cell>Cavi solari</cell>
                <cell>PV1-F</cell>
                <cell>Cavo solare 6–10 mm². Doppio isolamento, resistenza UV, temperatura da -40°C a +90°C, tensione nominale 600/1000V AC – 1800V DC, resistente ad agenti atmosferici e adatto a posa esterna prolungata.</cell>
                <cell>Collegamento tra i moduli fotovoltaici e tra i moduli e le scatole di giunzione.</cell>
                <cell>Certificazione TÜV/IEC 62930, durata ≥ 25 anni, resistenza a trazione e abrasione, elevata affidabilità in ambienti industriali o agricoli.</cell>
            </row>
            <row>
                <cell>Cavi DC</cell>
                <cell>Solar DC Cable</cell>
                <cell>16–25 mm², cavo unipolare. Isolamento XLPE/EPR, tensione nominale 1500V DC, temperatura -40°C a +120°C, resistenza a raggi UV, ozono e agenti chimici.</cell>
                <cell>Collegamenti tra le stringhe fotovoltaiche, quadri di parallelo (string combiner box) e inverter centralizzato o multistringa.</cell>
                <cell>Conformità IEC 62930, alta flessibilità, bassa caduta di tensione anche su distanze fino a 50–60 m, adatto a impianti semi-industriali.</cell>
            </row>
            <row>
                <cell>Cavi AC</cell>
                <cell>Solar AC Cable</cell>
                <cell>25–35 mm² tipo N2XY, FG7OR o equivalente. Isolamento XLPE o PVC, tensione nominale 600/1000V AC, temperatura di esercizio -40°C a +90°C, resistente a umidità e raggi UV.</cell>
                <cell>Collegamento tra inverter trifase e quadro elettrico generale, o tra quadro e rete BT pubblica.</cell>
                <cell>Certificazione CE e conformità CEI 64-8/CEI 0-21, bassa impedenza, adatto per correnti fino a 60–70 A.</cell>
            </row>
            <row>
                <cell>Cavi di messa a terra</cell>
                <cell>H07V-K</cell>
                <cell>25 mm² o superiore. Isolamento PVC, tensione nominale 450/750V, temperatura da -25°C a +70°C, flessibile, resistente all’abrasione e alla corrosione.</cell>
                <cell>Collegamento equipotenziale tra strutture metalliche, quadri, inverter e dispersori di terra.</cell>
                <cell>Certificazione CE, sezione verificata in base alla corrente di guasto presunta (secondo CEI 64-8), compatibile con SPD e protezione fulmini.</cell>
            </row>
            <row>
                <cell>Cavi accumulo</cell>
                <cell>Solar battery cable</cell>
                <cell>35 mm² o superiore. Isolamento rinforzato (LSZH o XLPE), temperatura fino a 120°C, resistenza UV e chimica, classe di isolamento secondo IEC 62930/60228.</cell>
                <cell>Collegamento tra sistema di accumulo e inverter ibrido o quadri DC dedicati.</cell>
                <cell>Verifica della sezione sulla base delle correnti nominali di carica/scarica (fino a 80–100 A), bassa caduta di tensione, posa sicura.</cell>
            </row>
            <row>
                <cell>Cavi per comunicazione</cell>
                <cell>Solar Communication Cable</cell>
                <cell>CAT6 FTP o RS485 schermato. Isolamento LSZH, tensione 300V, temperatura -20°C a +70°C, schermatura per EMI, guaina esterna antifiamma.</cell>
                <cell>Collegamenti tra inverter, sensori ambientali, sistemi di monitoraggio remoto, datalogger o interfacce con BMS/EMS.</cell>
                <cell>Conformità RS485, Modbus o Ethernet industriale. Installazione in canalina separata, schermatura continua, compatibilità ambienti industriali.</cell>
            </row>
        </table>"""
        elif generator_power < 30:
            content = """<table style="borders:TRBL;width-cols:2-2-5;font-size:9">
            <row>
                <cell>Tipo di cavi</cell>
                <cell>Denominazione</cell>
                <cell>Caratteristiche tecniche</cell>
                <cell>Utilizzi</cell>
                <cell>Criteri di qualità</cell>
            </row>
            <row>
                <cell>Cavi solari</cell>
                <cell>PV1-F</cell>
                <cell>Cavo solare 6–10 mm². Doppio isolamento, resistenza UV, temperatura da -40°C a +90°C, tensione nominale 600/1000V AC – 1800V DC, resistente ad agenti atmosferici e adatto a posa esterna prolungata.</cell>
                <cell>Collegamento tra i moduli fotovoltaici e tra i moduli e le scatole di giunzione.</cell>
                <cell>Certificazione TÜV/IEC 62930, durata ≥ 25 anni, resistenza a trazione e abrasione, elevata affidabilità in ambienti industriali o agricoli.</cell>
            </row>
            <row>
                <cell>Cavi DC</cell>
                <cell>Solar DC Cable</cell>
                <cell>16–25 mm², cavo unipolare. Isolamento XLPE/EPR, tensione nominale 1500V DC, temperatura -40°C a +120°C, resistenza a raggi UV, ozono e agenti chimici.</cell>
                <cell>Collegamenti tra le stringhe fotovoltaiche, quadri di parallelo (string combiner box) e inverter centralizzato o multistringa.</cell>
                <cell>Conformità IEC 62930, alta flessibilità, bassa caduta di tensione anche su distanze fino a 50–60 m, adatto a impianti semi-industriali.</cell>
            </row>
            <row>
                <cell>Cavi AC</cell>
                <cell>Solar AC Cable</cell>
                <cell>25–35 mm² tipo N2XY, FG7OR o equivalente. Isolamento XLPE o PVC, tensione nominale 600/1000V AC, temperatura di esercizio -40°C a +90°C, resistente a umidità e raggi UV.</cell>
                <cell>Collegamento tra inverter trifase e quadro elettrico generale, o tra quadro e rete BT pubblica.</cell>
                <cell>Certificazione CE e conformità CEI 64-8/CEI 0-21, bassa impedenza, adatto per correnti fino a 60–70 A.</cell>
            </row>
            <row>
                <cell>Cavi di messa a terra</cell>
                <cell>H07V-K</cell>
                <cell>25 mm² o superiore. Isolamento PVC, tensione nominale 450/750V, temperatura da -25°C a +70°C, flessibile, resistente all’abrasione e alla corrosione.</cell>
                <cell>Collegamento equipotenziale tra strutture metalliche, quadri, inverter e dispersori di terra.</cell>
                <cell>Certificazione CE, sezione verificata in base alla corrente di guasto presunta (secondo CEI 64-8), compatibile con SPD e protezione fulmini.</cell>
            </row>
            <row>
                <cell>Cavi accumulo</cell>
                <cell>Solar battery cable</cell>
                <cell>35 mm² o superiore. Isolamento rinforzato (LSZH o XLPE), temperatura fino a 120°C, resistenza UV e chimica, classe di isolamento secondo IEC 62930/60228.</cell>
                <cell>Collegamento tra sistema di accumulo e inverter ibrido o quadri DC dedicati.</cell>
                <cell>Verifica della sezione sulla base delle correnti nominali di carica/scarica (fino a 100 A), bassa caduta di tensione, posa sicura.</cell>
            </row>
            <row>
                <cell>Cavi per comunicazione</cell>
                <cell>Solar Communication Cable</cell>
                <cell>CAT6 FTP o RS485 schermato. Isolamento LSZH, tensione 300V, temperatura -20°C a +70°C, schermatura per EMI, guaina esterna antifiamma.</cell>
                <cell>Collegamenti tra inverter, sensori ambientali, sistemi di monitoraggio remoto, datalogger o interfacce con BMS/EMS.</cell>
                <cell>Conformità RS485, Modbus o Ethernet industriale. Installazione in canalina separata, schermatura continua, compatibilità ambienti industriali.</cell>
            </row>
        </table>"""
        elif generator_power < 50:
            content = """<table style="borders:TRBL;width-cols:2-2-5;font-size:9">
            <row>
                <cell>Tipo di cavi</cell>
                <cell>Denominazione</cell>
                <cell>Caratteristiche tecniche</cell>
                <cell>Utilizzi</cell>
                <cell>Criteri di qualità</cell>
            </row>
            <row>
                <cell>Cavi solari</cell>
                <cell>PV1-F</cell>
                <cell>Cavo solare 10–16 mm². Doppio isolamento, resistenza UV, temperatura da -40°C a +90°C, tensione nominale 600/1000V AC – 1800V DC, resistente ad agenti atmosferici.</cell>
                <cell>Collegamento tra moduli fotovoltaici e scatole di giunzione.</cell>
                <cell>Certificazione TÜV/IEC 62930, durata ≥ 25 anni, alta resistenza meccanica e chimica.</cell>
            </row>
            <row>
                <cell>Cavi DC</cell>
                <cell>Solar DC Cable</cell>
                <cell>25–35 mm² unipolari. Isolamento XLPE o EPR, tensione nominale 1500V DC, temperatura da -40°C a +120°C, resistenza UV e chimica.</cell>
                <cell>Collegamento stringhe fotovoltaiche, quadri di parallelo e inverter.</cell>
                <cell>Conformità IEC 62930, elevata flessibilità, bassa caduta di tensione su lunghe distanze.</cell>
            </row>
            <row>
                <cell>Cavi AC</cell>
                <cell>Solar AC Cable</cell>
                <cell>35–50 mm² tipo N2XY, FG7OR o equivalente. Isolamento XLPE o PVC, tensione nominale 600/1000V AC, temperatura da -40°C a +90°C, resistenza UV e all’umidità.</cell>
                <cell>Collegamento inverter trifase a quadro elettrico e rete di distribuzione.</cell>
                <cell>Certificazione CE, bassa resistenza elettrica, resistenza meccanica e chimica.</cell>
            </row>
            <row>
                <cell>Cavi di messa a terra</cell>
                <cell>H07V-K</cell>
                <cell>35 mm² o superiore. Isolamento PVC, tensione nominale 450/750V, temperatura da -25°C a +70°C, alta flessibilità.</cell>
                <cell>Collegamento tra strutture metalliche, inverter, quadri e sistema di terra.</cell>
                <cell>Certificazione CE, resistenza alla corrosione, sezione dimensionata per corrente di guasto.</cell>
            </row>
            <row>
                <cell>Cavi accumulo</cell>
                <cell>Solar battery cable</cell>
                <cell>50 mm² o superiore. Isolamento LSZH o XLPE, temperatura fino a 120°C, resistenza UV e agenti chimici.</cell>
                <cell>Collegamento sistema di accumulo a inverter e quadri dedicati.</cell>
                <cell>Sezione dimensionata su correnti di carica/scarica fino a 150 A, alta affidabilità e sicurezza.</cell>
            </row>
            <row>
                <cell>Cavi per comunicazione</cell>
                <cell>Solar Communication Cable</cell>
                <cell>CAT6 FTP o RS485 schermato. Isolamento LSZH, tensione nominale 300V, temperatura da -20°C a +70°C, schermatura contro EMI.</cell>
                <cell>Collegamenti inverter, monitoraggio, sensori ambientali e sistemi di controllo.</cell>
                <cell>Conformità RS485 o Ethernet industriale, elevata immunità a interferenze elettromagnetiche.</cell>
            </row>
        </table>"""
        elif generator_power < 75:
            content = """<table style="borders:TRBL;width-cols:2-2-5;font-size:9">
            <row>
                <cell>Tipo di cavi</cell>
                <cell>Denominazione</cell>
                <cell>Caratteristiche tecniche</cell>
                <cell>Utilizzi</cell>
                <cell>Criteri di qualità</cell>
            </row>
            <row>
                <cell>Cavi solari</cell>
                <cell>PV1-F</cell>
                <cell>Cavo solare 16–25 mm². Doppio isolamento, resistenza UV, temperatura da -40°C a +90°C, tensione nominale 600/1000V AC – 1800V DC, resistente ad agenti atmosferici.</cell>
                <cell>Collegamento tra moduli fotovoltaici e scatole di giunzione.</cell>
                <cell>Certificazione TÜV/IEC 62930, durata ≥ 25 anni, elevata resistenza meccanica e chimica.</cell>
            </row>
            <row>
                <cell>Cavi DC</cell>
                <cell>Solar DC Cable</cell>
                <cell>35–50 mm² unipolari. Isolamento XLPE o EPR, tensione nominale 1500V DC, temperatura da -40°C a +120°C, resistenza UV e chimica.</cell>
                <cell>Collegamento stringhe fotovoltaiche, quadri di parallelo e inverter.</cell>
                <cell>Conformità IEC 62930, elevata flessibilità, bassa caduta di tensione su lunghe distanze.</cell>
            </row>
            <row>
                <cell>Cavi AC</cell>
                <cell>Solar AC Cable</cell>
                <cell>50–70 mm² tipo N2XY, FG7OR o equivalente. Isolamento XLPE o PVC, tensione nominale 600/1000V AC, temperatura da -40°C a +90°C, resistenza UV e all’umidità.</cell>
                <cell>Collegamento inverter trifase a quadro elettrico e rete di distribuzione.</cell>
                <cell>Certificazione CE, bassa resistenza elettrica, resistenza meccanica e chimica.</cell>
            </row>
            <row>
                <cell>Cavi di messa a terra</cell>
                <cell>H07V-K</cell>
                <cell>50 mm² o superiore. Isolamento PVC, tensione nominale 450/750V, temperatura da -25°C a +70°C, alta flessibilità.</cell>
                <cell>Collegamento tra strutture metalliche, inverter, quadri e sistema di terra.</cell>
                <cell>Certificazione CE, resistenza alla corrosione, sezione dimensionata per corrente di guasto.</cell>
            </row>
            <row>
                <cell>Cavi accumulo</cell>
                <cell>Solar battery cable</cell>
                <cell>70 mm² o superiore. Isolamento LSZH o XLPE, temperatura fino a 120°C, resistenza UV e agenti chimici.</cell>
                <cell>Collegamento sistema di accumulo a inverter e quadri dedicati.</cell>
                <cell>Sezione dimensionata su correnti di carica/scarica fino a 200 A, alta affidabilità e sicurezza.</cell>
            </row>
            <row>
                <cell>Cavi per comunicazione</cell>
                <cell>Solar Communication Cable</cell>
                <cell>CAT6 FTP o RS485 schermato. Isolamento LSZH, tensione nominale 300V, temperatura da -20°C a +70°C, schermatura contro EMI.</cell>
                <cell>Collegamenti inverter, monitoraggio, sensori ambientali e sistemi di controllo.</cell>
                <cell>Conformità RS485 o Ethernet industriale, elevata immunità a interferenze elettromagnetiche.</cell>
            </row>
        </table>"""
        elif generator_power < 101:
            content = """<table style="borders:TRBL;width-cols:2-2-5; font-size:9">
            <row>
                <cell>Tipo di cavi</cell>
                <cell>Denominazione</cell>
                <cell>Caratteristiche tecniche</cell>
                <cell>Utilizzi</cell>
                <cell>Criteri di qualità</cell>
            </row>
            <row>
                <cell>Cavi solari</cell>
                <cell>PV1-F</cell>
                <cell>Cavo solare 25–35 mm². Doppio isolamento, resistenza UV, temperatura da -40°C a +90°C, tensione nominale 600/1000V AC – 1800V DC, resistente ad agenti atmosferici.</cell>
                <cell>Collegamento tra moduli fotovoltaici e scatole di giunzione.</cell>
                <cell>Certificazione TÜV/IEC 62930, durata ≥ 25 anni, elevata resistenza meccanica e chimica.</cell>
            </row>
            <row>
                <cell>Cavi DC</cell>
                <cell>Solar DC Cable</cell>
                <cell>50–70 mm² unipolari. Isolamento XLPE o EPR, tensione nominale 1500V DC, temperatura da -40°C a +120°C, resistenza UV e chimica.</cell>
                <cell>Collegamento stringhe fotovoltaiche, quadri di parallelo e inverter.</cell>
                <cell>Conformità IEC 62930, elevata flessibilità, bassa caduta di tensione su lunghe distanze.</cell>
            </row>
            <row>
                <cell>Cavi AC</cell>
                <cell>Solar AC Cable</cell>
                <cell>70–95 mm² tipo N2XY, FG7OR o equivalente. Isolamento XLPE o PVC, tensione nominale 600/1000V AC, temperatura da -40°C a +90°C, resistenza UV e all’umidità.</cell>
                <cell>Collegamento inverter trifase a quadro elettrico e rete di distribuzione.</cell>
                <cell>Certificazione CE, bassa resistenza elettrica, resistenza meccanica e chimica.</cell>
            </row>
            <row>
                <cell>Cavi di messa a terra</cell>
                <cell>H07V-K</cell>
                <cell>70 mm² o superiore. Isolamento PVC, tensione nominale 450/750V, temperatura da -25°C a +70°C, alta flessibilità.</cell>
                <cell>Collegamento tra strutture metalliche, inverter, quadri e sistema di terra.</cell>
                <cell>Certificazione CE, resistenza alla corrosione, sezione dimensionata per corrente di guasto.</cell>
            </row>
            <row>
                <cell>Cavi accumulo</cell>
                <cell>Solar battery cable</cell>
                <cell>95 mm² o superiore. Isolamento LSZH o XLPE, temperatura fino a 120°C, resistenza UV e agenti chimici.</cell>
                <cell>Collegamento sistema di accumulo a inverter e quadri dedicati.</cell>
                <cell>Sezione dimensionata su correnti di carica/scarica fino a 250 A, alta affidabilità e sicurezza.</cell>
            </row>
            <row>
                <cell>Cavi per comunicazione</cell>
                <cell>Solar Communication Cable</cell>
                <cell>CAT6 FTP o RS485 schermato. Isolamento LSZH, tensione nominale 300V, temperatura da -20°C a +70°C, schermatura contro EMI.</cell>
                <cell>Collegamenti inverter, monitoraggio, sensori ambientali e sistemi di controllo.</cell>
                <cell>Conformità RS485 o Ethernet industriale, elevata immunità a interferenze elettromagnetiche.</cell>
            </row>
        </table>"""

        try:
            table_node = etree.fromstring(content)
        except etree.XMLSyntaxError as e:
            table_node = ""
        return Common.generate_string_xml(table_node)

    def create_table_cable_lengths(self):
        """X111: Crea la tabella delle lunghezze stimate dei cavi."""
        table_node = etree.Element("table", attrib={
            "style": "borders:TRBL;width-cols:14;padding:1;column-alignments:L-C; font-size:9"
        })

        input_lengths = self.data.get("cable_lengths", {})

        # Mappa descrizione -> chiave dati
        connections = [
            ("Collegamento tra moduli fotovoltaici e tra moduli e scatole di giunzione", "modules_junction"),
            ("Collegamento tra stringhe di moduli e inverter, tra scatole di giunzione e inverter",
             "junction_inverter"),
            ("Collegamento tra inverter e quadro elettrico, tra quadro elettrico e rete di distribuzione",
             "inverter_panel"),
            ("Collegamento tra inverter e sistema di accumulo", "inverter_storage"),
            ("Collegamenti per il sistema di messa a terra.", "grounding_system"),
            ("Collegamenti per i sistemi di monitoraggio, tra sensori ambientali e sistema di controllo.",
             "communication"),
        ]

        row_node = etree.SubElement(table_node, "row")
        etree.SubElement(row_node, "cell").text = "Tipo di collegamento e utilizzo dei cavi"
        etree.SubElement(row_node, "cell").text = "Lunghezza stimata dei cavi (m)"

        for description, key in connections:
            value = input_lengths.get(key, '')
            if value:
                row_node = etree.SubElement(table_node, "row")
                etree.SubElement(row_node, "cell").text = description
                etree.SubElement(row_node, "cell").text = str(value)

        return Common.generate_string_xml(table_node)

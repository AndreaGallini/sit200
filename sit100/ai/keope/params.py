"""
params.py
Costanti e valori fissi
"""

IMAGE_NAMES = {
    "map_1": "map_location.png",
    "map_2": "map_accessibility.png",
    "map_3": "map_positioning.png",
}

SYSTEM_PURPOSE_SHORT = {
    "autoconsumo-residenziale": "Autoconsumo residenziale",
    "autoconsumo-industriale": "Autoconsumo industriale",
    "cer": "Partecipazione a una Comunità Energetica Rinnovabile (CER)",
    "produzione-vendita-industriale": "Produzione per la vendita e uso industriale",
    "vendita": "Vendita dell'energia prodotta senza autoconsumo"
}

SYSTEM_PURPOSE_LONG = {
    "autoconsumo-residenziale": "Inoltre l’installazione è destinata a coprire il fabbisogno energetico "
                                "domestico, riducendo i costi in bolletta. Ideale per abitazioni unifamiliari "
                                "o piccoli condomini con consumi standard.",

    "autoconsumo-industriale": "Inoltre l’impianto è progettato per coprire parte del fabbisogno energetico "
                               "di attività produttive o commerciali. La finalità è ridurre i costi energetici "
                               "e aumentare l’autonomia dell’azienda, ottimizzando l’uso dell’energia generata "
                               "durante le ore lavorative.",

    "cer": "Inoltre l’installazione è inserita in una Comunità Energetica Rinnovabile (CER), "
           "favorendo la condivisione dell’energia tra più utenti locali. Questo modello consente "
           "di massimizzare l’autoconsumo collettivo e di accedere a incentivi specifici per l’energia condivisa.",

    "produzione-vendita-industriale": "Inoltre la produzione energetica per la vendita e per "
                                      "l’uso industriale è tipica di progetti su larga scala per "
                                      "stabilimenti industriali o impianti dedicati alla vendita di energia. "
                                      "Obiettivo primario è generare reddito attraverso la produzione "
                                      "e vendita costante di energia.",

    "vendita": "Inoltre l’impianto è pensato principalmente per la produzione e la vendita di energia "
               "alla rete. Si tratta di una configurazione orientata al profitto, spesso adottata "
               "in contesti agricoli, industriali o da investitori che operano nel settore energetico."
}

POSITION = {
    'TL': 'Tetto a falda su laterizio',
    'TG': 'Tetto a falda su lamiera grecata',
    'TF': 'Tetto a falda su lamiera aggraffata',
    'TP': 'Tetto a copertura piana',
    'SP': 'Installazione a terra su superficie piana',
    'AG': 'Installazione a terra su superficie piana',
}

SUPPORT = {
    'TL': 4001,
    'TG': 4006,
    'TF': 4007,
    'TP': 4008,
    'SP': 4004,
    'AG': 4004,
}

SUPPORT_TYPE = {
    'TL': 'Profili in alluminio anodizzato',
    'TG': 'Profili in alluminio anodizzato',
    'TF': 'Profili in alluminio anodizzato',
    'TP': 'Sistema autoposante in cemento armato',
    'SP': 'Strutture in alluminio o in acciaio direzionate verso il sole',
    'AG': 'Strutture in alluminio o in acciaio direzionate verso il sole'
}

MQ_PER_MODULE = 2.1         # m² occupati da ogni modulo FV
MQ_PER_MODULE_LARGE = 3.1   # m² occupati da ogni modulo FV a terra

GROUND_COVERAGE_RATIO = {
    "TL": 0.85,
    "TG": 0.85,
    "TF": 0.85,
    "TP": 0.6,
    "SP": 0.5,
    "AG": 0.5,
}

STORAGE_CONSTANT_LEVEL = {
    'auto-ultra': 2,
    'auto-high': 1.5,
    'auto-med': 1,
    'auto-low': 0.5,
}

RID = {
    '0': '',
    '1': 'Ritiro Dedicato - RID',
}

GRID_CONNECTED = {
    '0': 'Off-grid',
    '1': 'Grid-connected',
}

SELF_CONSUMPTION = {
    '0': 'Senza autoconsumo',
    '1': 'Con autoconsumo',
}

STORAGE = {
    '0': 'Senza sistema di accumulo',
    '1': 'Con sistema di accumulo',
}

ALBEDO = {
    'standard': 'Standard',
    'neve': 'Neve (caduta di fresco / film di ghiaccio)',
    'superfici-acquose': 'Superfici acquose',
    'suolo': 'Suolo (creta,marne)',
    'strada-sterrata': 'Strade sterrate',
    'bosco-conifere-inverno': "'Bosco di conifere d'inverno",
    'bosco-autunno-campi-raccolti': 'Bosco in autunno / campi con raccolti maturi e piante',
    'asfalto-invecchiato': 'Asfalto invecchiato',
    'calcestruzzo-invecchiato': 'Calcestruzzo invecchiato',
    'foglie-morte': 'Foglie morte',
    'erba-secca': 'Erba secca',
    'erba-verde': 'Erba verde',
    'tetti-terrazzi-bitume': 'Tetti o terrazzi in bitume',
    'pietrisco': 'Pietrisco',
    'superfici-scure': 'Superfici scure di edifici (mattoni scuri, vernice scura, ecc.)',
    'superfici-chiare': 'Superfici chiare di edifici (mattoni chiari, vernici chiare, ecc.)'
}

ALBEDO_MAPPING = {
    'standard': '0.20',
    'neve': '0.75',
    'superfici-acquose': '0.07',
    'suolo': '0.14',
    'strada-sterrata': '0.04',
    'bosco-conifere-inverno': '0.07',
    'bosco-autunno-campi-raccolti': '0.26',
    'asfalto-invecchiato': '0.10',
    'calcestruzzo-invecchiato': '0.22',
    'foglie-morte': '0.30',
    'erba-secca': '0.20',
    'erba-verde': '0.26',
    'tetti-terrazzi-bitume': '0.13',
    'pietrisco': '0.20',
    'superfici-scure': '0.27',
    'superfici-chiare': '0.60'
}

MESI = {
    'GEN': 'Gennaio',
    'FEB': 'Febbraio',
    'MAR': 'Marzo',
    'APR': 'Aprile',
    'MAG': 'Maggio',
    'GIU': 'Giugno',
    'LUG': 'Luglio',
    'AGO': 'Agosto',
    'SET': 'Settembre',
    'OTT': 'Ottobre',
    'NOV': 'Novembre',
    'DIC': 'Dicembre',
}

OBSTACLES_CLASS = {
    "1": 'Classe A: ombreggiamento minimo, perdite: <5%. Ombreggiamento dovuto a piccoli ostacoli come pali della '
         'luce o antenne che non incidono significativamente sulla produzione energetica.',
    "2": 'Classe B: ombreggiamento moderato, perdite: 5% - 15%. Ombreggiamento intermittente, causato da ostacoli '
         'di medie dimensioni come alberi piccoli o edifici a distanza media.',
    "3": 'Classe C: ombreggiamento significativo, perdite: 15% - 25%. Ombreggiamento frequente e significativo, '
         'spesso dovuto a edifici vicini, grandi alberi o altre strutture che causano ombre durante '
         'diverse ore del giorno.',
    "4": 'Classe D: ombreggiamento grave, perdite: >25%. Ombreggiamento grave e continuo, che compromette '
         'fortemente la produzione energetica causato da ostacoli molto vicini o grandi strutture che bloccano '
         'la luce solare per periodi prolungati.'
}

CLINOMETRIC_CLASS = {
    "1": 'Minimo tipico delle aree aperte e pianeggianti senza rilievi significativi; '
         'conformazione del terreno uniforme e priva di ostacoli naturali o artificiali; pianure agricole, '
         'deserti, praterie e superfici piane ad alta quota.',
    "2": 'Moderato tipico dei terreni leggermente ondulati o collinari con lievi variazioni altimetriche; '
         'aree suburbane con poche costruzioni o alberi di altezza media; colline basse, aree periferiche '
         '"di città con spazi aperti, campi coltivati con alberi sparsi.',
    "3": 'Significativo tipico delle aree con rilievi più pronunciati e variazioni altimetriche evidenti; '
         'zone montuose di media altitudine, aree urbane dense con edifici alti; '
         'terreni montuosi, valli profonde, aree urbane con edifici di media altezza, boschi densi.',
    "4": 'Grave tipico delle aree con rilievi estremamente pronunciati e profondi, presenza di ostacoli alti e '
         'vicini che causano ombreggiamento prolungato; valli profonde e strette, aree urbane molto dense '
         'con grattacieli; valli strette e profonde, pendii montuosi ripidi, centri urbani con grattacieli, '
         'aree forestali molto fitte con alberi molto alti.'
}

TABLE_CAPTION = {
    "x12": "Caratteristiche tecniche del generatore fotovoltaico.",
    "x20": "Valori di irradiazione solare giornaliera media mensile su un piano orizzontale, insieme ai "
           "valori di irradiazione diretta, diffusa e riflessa per la località in esame secondo UNI 10349-1:2016. "
           "Irradiazione solare orizzontale: media giornaliera mensile dell'irradiazione solare totale ricevuta "
           "su un piano orizzontale. Irradiazione solare diretta: media giornaliera mensile dell'irradiazione "
           "solare diretta ricevuta su un piano orizzontale. Irradiazione solare diffusa: media giornaliera mensile "
           "dell'irradiazione solare diffusa ricevuta su un piano orizzontale. Irradiazione solare riflessa: "
           "è calcolata moltiplicando l'irradiazione solare orizzontale per l'albedo.",
    "x21": "Valori irradiazione solare giornaliera media mensile su un piano orizzontale.",
    "x22": "Valori di irradiazione solare giornaliera media mensile sul piano dei moduli.",
    "x23": "Valori di irradiazione solare mensile sul piano dei moduli.",
    "x32": "Tabella delle perdite dell’impianto fotovoltaico.",
    "x44": "Valori di energia utile mensile (kWh/m²/mese).",
    "x47": "Valori di producibilità mensile (kWh/kWp)",
    "x52": "Valori di efficienza percentuale mensile (%).",
    "x53": "Valori stimati di produzione su base annuale.",
    "x54": "Visione dettagliata della producibilità mensile dell’impianto fotovoltaico.",
    "x60": "Stima della riduzione di alcuni parametri ambientali chiave su un periodo di 20 anni per "
           "l’impianto fotovoltaico previsto nel sito di installazione.",
    "x71": "Caratteristiche tecniche del generatore fotovoltaico.",
    'x150': "Entrate derivanti da autoconsumo.",
    'x154': "Andamento del cash flow netto annuale dell’impianto fotovoltaico dal 1° al 25° anno di vita.",
}

IMAGE_CAPTION = {
    'x155': "Grafico dell'andamento del cashflow generato dell'impianto fotovoltaico in 25 anni di vita.",
}

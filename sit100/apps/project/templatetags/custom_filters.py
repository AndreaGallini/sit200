from django import template

register = template.Library()


@register.filter
def split(value, arg):
    return value.split(arg)[-1] if value else ''


@register.filter
def extract_filename(value):
    """
    Estrae il nome del file dal percorso di storage.
    Gestisce sia percorsi locali che percorsi di storage remoto.
    """
    if not value:
        return ''

    # Se il valore contiene '/', prendi l'ultima parte
    if '/' in str(value):
        return str(value).split('/')[-1]

    # Se non contiene '/', restituisci il valore così com'è
    return str(value)


@register.filter
def format_location(value):
    locations = {
        'tetto-a-falde': 'Tetto a falde',
        'case-residenziali': 'Case residenziali',
        'case-a-schiera': 'Case a schiera',
        'piccoli-condomini': 'Piccoli condomini',
        'copertura-piana': 'Copertura piana',
        'grandi-condomini': 'Grandi condomini',
        'ospedali-e-cliniche': 'Ospedali e Cliniche',
        'alberghi-e-resort': 'Alberghi e Resort',
        'scuole-e-universita': 'Scuole e Università',
        'capannoni': 'Capannoni',
        'strutture-ricreative': 'Strutture ricreative',
        'stadi-e-palazzetti': 'Stadi e Palazzetti',
        'centri-commerciali': 'Centri commerciali',
        'centri-di-logistica': 'Centri di logistica',
        'aree-parcheggio': 'Aree di parcheggio',
        'strade-e-autostrade': 'Strade ed autostrade',
        'aeroporti-e-porti': 'Aeroporti e porti',
        'stazioni-ferroviarie': 'Stazioni ferroviarie',
        'pensiline-fotovoltaiche': 'Pensiline fotovoltaiche',
        'impianto-a-terra': 'Impianto a terra',
        'terreni-agricoli-e-rurali': 'Terreni agricoli e rurali',
        'serre-fotovoltaiche': 'Serre fotovoltaiche',
        'cave-e-miniere-esauste': 'Cave e miniere esauste',
        'discarica': 'Discarica',
        'terreni-non-produttivi': 'Terreni non produttivi',
        # up is ex value of the radiobox
        'TL': 'Tetto a falda su laterizio',
        'TG': 'Tetto a falda su lamiera grecata',
        'TP': "Tetto piano",
        'TF': 'Tetto a falda su lamiera aggraffata',
        'SP': "A terra su superficie piana",
        'AG': 'Agrivoltaico',
        'condomini-multiutenza': 'Condomini multiutenza',
        'tetto-su-cappannone-industriale-a-cupoline': 'Tetto su cappannone industriale a cupoline',
        'tetto-a-shed': 'Tetto a shed',
        'tetto-a-volte': 'Tetto a volte',
        'pensilina-solare-carport': 'Pensilina solare (carport)',

    }
    return locations.get(value, value)


@register.filter
def format_type(value):
    types = {
        'grid-connected': 'Impianto collegato alla rete',
        'battery': 'Impianto con sistema di accumulo',
        'self-use': 'Impianto con autoconsumo',
        'ssp': 'Impianto con SSP'
    }
    return types.get(value, value)


@register.filter
def format_albedo(value):
    albedo = {
        'standard': 'Standard',
        'neve': 'Neve (caduta di fresco / film di ghiaccio)',
        'superfici-acquose': 'Superfici acquose',
        'suolo': 'Suolo(creta,marne)',
        'strada-sterrata': 'Strade sterrate',
        'bosco-conifere-inverno': "Bosco di conifere d'inverno",
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
    return albedo.get(value, value)


@register.filter
def format_albedo_short(value):
    albedo = {
        'standard': 'Standard',
        'neve': 'Neve',
        'superfici-acquose': 'Superfici acquose',
        'suolo': 'Suolo(creta,marne)',
        'strada-sterrata': 'Strade sterrate',
        'bosco-conifere-inverno': "Bosco di conifere d'inverno",
        'bosco-autunno-campi-raccolti': 'Bosco in autunno...',
        'asfalto-invecchiato': 'Asfalto invecchiato',
        'calcestruzzo-invecchiato': 'Calcestruzzo invecchiato',
        'foglie-morte': 'Foglie morte',
        'erba-secca': 'Erba secca',
        'erba-verde': 'Erba verde',
        'tetti-terrazzi-bitume': 'Tetti o terrazzi ...',
        'pietrisco': 'Pietrisco',
        'superfici-scure': 'Superfici scure...',
        'superfici-chiare': 'Superfici chiare...'
    }
    return albedo.get(value, value)


@register.filter
def format_shading_obstacle(value):
    try:
        rangeValue = float(value)
        if 0 <= rangeValue < 5:
            return 'Minimo'
        elif 5 <= rangeValue < 15:
            return 'Moderato'
        elif 15 <= rangeValue < 25:
            return 'Significativo'
        elif rangeValue >= 25:
            return 'Grave'
        else:
            return 'Non definito'
    except (ValueError, TypeError):
        return 'Non definito'


@register.filter
def format_shading_horizon(value):
    try:
        rangeValue = float(value)
        if 0 <= rangeValue < 5:
            return 'Minimo'
        elif 5 <= rangeValue < 15:
            return 'Moderato'
        elif 15 <= rangeValue < 25:
            return 'Significativo'
        elif rangeValue >= 20:
            return 'Grave'
        else:
            return 'Non definito'
    except (ValueError, TypeError):
        return 'Non definito'


@register.filter
def format_plant_scope(value):
    plant_scope = {
        "autoconsumo-residenziale": "Autoconsumo residenziale",
        "autoconsumo-industriale": "Autoconsumo industriale",
        "cer": "Partecipazione a una Comunità Energetica Rinnovabile (CER)",
        "produzione-vendita-industriale": "Produzione e vendita industriale",
        "vendita": "Vendita energia",
        "autosufficienza-permanente": "Autosufficienza energetica permanente",
        "abitazione-isolata": "Abitazione isolata dalla rete",
        "uso-stagionale": "Uso stagionale",
        "backup-energetico": "Backup energetico",
        "utenze-mobili": "Utenze mobili",
        "auto-ultra": "Uso continuativo alta autosufficienza",
        "auto-high": "Massimizzare autosufficienza / Uso stagionale/saltuario",
        "auto-med": "Risparmio con consumi serali/notturni / Uso temporaneo con backup",
        "auto-low": "Autoconsumo con consumi diurni / Uso prevalentemente diurno",
        "si": "Sì",
        "no": "No"
    }
    return plant_scope.get(value, value)


@register.filter
def calculate_total_area(generator):
    """
    Calcola l'area totale di tutti i sottocampi nel generatore.
    La struttura del generatore è: 
    {'A': {'A1': {'area': 100}}, 'B': {'B1': {'area': 200}}}
    """
    total_area = 0
    if generator:
        for field in generator.values():  # Itera sui campi (A, B, etc.)
            for subfield in field.values():  # Itera sui sottocampi (A1, A2, etc.)
                area = subfield.get('area', 0)
                if isinstance(area, (int, float)):
                    total_area += area
    return total_area

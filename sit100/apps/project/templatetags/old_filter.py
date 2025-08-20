from django import template

register = template.Library()


@register.filter
def get_selected_angles_value(polygons, polygon_name):
    """
    Restituisce il valore dell'angolo per un dato poligono.
    Se il poligono non ha un angolo selezionato, restituisce 0.
    """
    for polygon in polygons:
        if polygon.get('name') == polygon_name:
            tilt_value = polygon.get('tilt', 30)
            return tilt_value
    return 30


@register.filter
def get_orientation_value(polygons, polygon_name):
    """
    Restituisce il valore dell'orientamento per un dato poligono.
    Se il poligono non ha un orientamento selezionato o l'orientamento è zero, restituisce 180.
    """
    for polygon in polygons:
        if polygon.get('name') == polygon_name:
            orientation = polygon.get('orientation')
            if orientation is None or orientation == 0:
                return 180  # Valore di default
            else:
                return orientation
    return 180  # Valore di default se il poligono non è trovato


@register.filter
def subtract_180(value):
    try:
        return int(value) - 180
    except (ValueError, TypeError):
        return value


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def int_trunc(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return ''

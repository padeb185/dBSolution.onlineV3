"""
Filtre « milliers » (chargé automatiquement dans tous les gabarits, voir TEMPLATES › builtins) :
nombre entier ou décimal affiché avec le séparateur des milliers de la langue (espace fine en français).
    {{ km|milliers }}            → 194 666
    {{ montant|milliers:2 }}     → 12 345,60
Une valeur non numérique (« — », texte vide…) est renvoyée telle quelle.
"""
from decimal import Decimal, InvalidOperation

from django import template
from django.template.defaultfilters import floatformat

register = template.Library()


@register.filter
def milliers(valeur, decimales=0):
    if valeur is None or valeur == "" or isinstance(valeur, bool):
        return valeur
    try:
        Decimal(str(valeur))
    except (InvalidOperation, ValueError, TypeError):
        return valeur
    return floatformat(valeur, f"{int(decimales)}g")

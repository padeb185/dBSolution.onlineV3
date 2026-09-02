import re

from django import template
from django.utils.translation import gettext

register = template.Library()


@register.filter
def db_trans(value):
    if not value:
        return value

    value = str(value)

    # ---------------------------------------------------------
    # Actions contenant une immatriculation
    # Exemple :
    # "Modification du check-up piste - 1-ABC-321"
    # ---------------------------------------------------------
    if " - " in value:
        action, suffixe = value.split(" - ", 1)

        traduction = gettext(action)

        return f"{traduction} - {suffixe}"

    # ---------------------------------------------------------
    # Texte simple
    # ---------------------------------------------------------
    return gettext(value)
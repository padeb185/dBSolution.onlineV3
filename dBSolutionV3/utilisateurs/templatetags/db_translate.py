from django import template
from django.utils.translation import gettext

register = template.Library()


@register.filter
def db_trans(value):
    if not value:
        return ""

    value = str(value)

    # Exemple :
    # "Contrôle de l'ABS - 1-ABC-123"
    if " - " in value:
        action, info = value.split(" - ", 1)
        return f"{gettext(action)} - {info}"

    return gettext(value)
from django import template
from django.utils.translation import gettext

register = template.Library()


@register.filter
def db_trans(value):
    if not value:
        return value

    value = str(value).strip()

    # Cas des logs de type :
    # "Modification du check-up piste - 1-ABC-321"
    if " - " in value:
        texte, suffixe = value.split(" - ", 1)

        texte_traduit = gettext(texte)

        return f"{texte_traduit} - {suffixe}"

    return gettext(value)
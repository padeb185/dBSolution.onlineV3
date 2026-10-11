from django import template
from django.utils.translation import gettext

register = template.Library()

# Séparateurs utilisés dans UserLog.action entre le libellé de l'action et le détail :
#   "Modification du check-up piste - 1-ABC-321"
#   "Suppression d'une maintenance planifiée : Allumage – 2-EJH-815 (11/10/2026) – Jean Dupont"
SEPARATEURS = (" : ", " - ")
SEPARATEUR_DETAIL = " – "


@register.filter
def db_trans(value):
    if not value:
        return value

    value = str(value)

    # Premier séparateur présent dans le texte (le plus à gauche)
    positions = [(value.find(sep), sep) for sep in SEPARATEURS if sep in value]
    if not positions:
        # Texte simple
        return gettext(value)

    _, sep = min(positions)
    action, suffixe = value.split(sep, 1)

    # Le premier élément du détail peut être un libellé traduisible
    # (ex. le type de maintenance « Allumage ») ; le reste (immatriculation, date, nom) est conservé tel quel.
    premier, reste = (suffixe.split(SEPARATEUR_DETAIL, 1) + [None])[:2]
    premier = gettext(premier) if premier else premier
    suffixe = premier if reste is None else f"{premier}{SEPARATEUR_DETAIL}{reste}"

    return f"{gettext(action)}{sep}{suffixe}"

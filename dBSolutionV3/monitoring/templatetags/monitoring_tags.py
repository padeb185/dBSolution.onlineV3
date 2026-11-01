from django import template
from django.utils.translation import gettext as _

register = template.Library()


@register.filter
def duree_humaine(secondes):
    """93784 → « 1 j 2 h 3 min »."""
    if secondes in (None, ""):
        return "—"
    s = int(secondes)
    j, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m = s // 60
    morceaux = []
    if j:
        morceaux.append(_("%(n)s j") % {"n": j})
    if h or j:
        morceaux.append(_("%(n)s h") % {"n": h})
    morceaux.append(_("%(n)s min") % {"n": m})
    return " ".join(morceaux)


@register.filter
def couleur_jauge(valeur, seuils="70,85"):
    """Classe Tailwind de la barre selon le pourcentage (vert / orange / rouge)."""
    try:
        v = float(valeur)
    except (TypeError, ValueError):
        return "bg-gray-300"
    orange, rouge = (float(x) for x in str(seuils).split(","))
    if v >= rouge:
        return "bg-red-600"
    if v >= orange:
        return "bg-amber-500"
    return "bg-green-600"


@register.filter
def largeur(valeur):
    """Pourcentage borné 0–100 pour un style width."""
    try:
        return max(0, min(100, round(float(valeur))))
    except (TypeError, ValueError):
        return 0

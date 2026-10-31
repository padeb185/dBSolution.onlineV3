from django import template
from django.utils.translation import gettext

register = template.Library()

# Séparateurs utilisés dans UserLog.action entre le libellé de l'action et le détail :
#   "Modification du check-up piste - 1-ABC-321"
#   "Suppression d'une maintenance planifiée : Allumage – 2-EJH-815 (11/10/2026) – Jean Dupont"
SEPARATEURS = (" : ", " - ")
SEPARATEUR_DETAIL = " – "


def traduire_debut(texte):
    """
    Traduit un texte de journal : le texte entier s'il est connu, sinon son plus long début traduisible
    (« Création paie 10/2026 – Jean Dupont » → « Payslip created 10/2026 – Jean Dupont »).
    Les détails variables (dates, montants, noms, immatriculations) restent tels quels.
    """
    texte = texte or ""
    if not texte.strip():
        return texte
    traduit = gettext(texte)
    if traduit != texte:
        return traduit
    mots = texte.split(" ")
    for k in range(len(mots) - 1, 0, -1):
        debut = " ".join(mots[:k]).rstrip(" :-–")
        if len(debut) < 3:
            break
        traduit = gettext(debut)
        if traduit != debut:
            return traduit + texte[len(debut):]
    return texte


@register.filter
def db_trans(value):
    if not value:
        return value

    value = str(value)

    # Premier séparateur présent dans le texte (le plus à gauche)
    positions = [(value.find(sep), sep) for sep in SEPARATEURS if sep in value]
    if not positions:
        # Texte simple (ou libellé suivi de détails sans séparateur)
        return traduire_debut(value)

    _, sep = min(positions)
    action, suffixe = value.split(sep, 1)

    # Le premier élément du détail peut être un libellé traduisible
    # (ex. le type de maintenance « Allumage ») ; le reste (immatriculation, date, nom) est conservé tel quel.
    premier, reste = (suffixe.split(SEPARATEUR_DETAIL, 1) + [None])[:2]
    premier = traduire_debut(premier) if premier else premier
    suffixe = premier if reste is None else f"{premier}{SEPARATEUR_DETAIL}{reste}"

    return f"{traduire_debut(action)}{sep}{suffixe}"

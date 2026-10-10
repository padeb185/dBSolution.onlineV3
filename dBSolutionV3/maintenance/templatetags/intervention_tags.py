from django import template

register = template.Library()


@register.filter
def premier(obj, cles):
    """
    Renvoie la première valeur non vide parmi plusieurs clés/attributs.
    Usage : {{ ligne|premier:"champ,nom,label" }}
    Contrairement à |default, une clé absente ne provoque pas d'erreur.
    """
    if obj is None:
        return ""
    for cle in str(cles).split(","):
        cle = cle.strip()
        if isinstance(obj, dict):
            valeur = obj.get(cle)
        else:
            valeur = getattr(obj, cle, None)
        if callable(valeur):
            try:
                valeur = valeur()
            except TypeError:
                continue
        if valeur not in (None, "", [], ()):
            return valeur
    return ""


# Libellés des codes d'état les plus courants, utilisés quand le rapport
# renvoie le code brut (ex. "REMPLACE") au lieu d'un libellé lisible.
from django.utils.translation import gettext_lazy as _  # noqa: E402

LIBELLES_ETATS = {
    "OK": _("OK"),
    "BON": _("Bon"),
    "NOT_OK": _("À remplacer"),
    "A_REMPLACER": _("À remplacer"),
    "REMPLACER": _("Remplacé"),  # NiveauxEtat : REMPLACER = « Remplacé »
    "REMPLACE": _("Remplacé"),
    "REPARE": _("Réparé"),
    "A_REPARER": _("À réparer"),
    "A_FAIRE": _("À faire"),
    "FAIT": _("Fait"),
    "AJOUTER": _("Ajouté"),
    "AJOUTE": _("Ajouté"),
    "A_CONTROLER": _("À contrôler"),
    "CONTROLE": _("Contrôlé"),
    "REPORTER": _("Reporté"),
    "NETTOYE": _("Nettoyé"),
    "PROPRE": _("Propre"),
    "NON_PRESENT": _("Non présent"),
}


@register.filter
def libelle_etat(ligne):
    """
    Libellé lisible de l'état d'une ligne de rapport.
    Si le rapport ne fournit que le code (ex. "REMPLACE"), il est traduit.
    """
    code = premier(ligne, "etat")
    libelle = premier(ligne, "etat_label,etat_display")

    if not libelle or str(libelle) == str(code):
        if code in LIBELLES_ETATS:
            return LIBELLES_ETATS[code]
        if code:
            return str(code).replace("_", " ").capitalize()
        return "-"

    # Libellé fourni mais resté sous forme de code (ex. "A_REMPLACER")
    texte = str(libelle)
    if texte in LIBELLES_ETATS:
        return LIBELLES_ETATS[texte]
    return libelle


# Couleur de l'état dans les tableaux de rapport.
# Attention : REMPLACER signifie « Remplacé » et AJOUTER « Ajouté » (travail fait).
ETATS_FAITS = {"REMPLACE", "REMPLACER", "AJOUTER", "AJOUTE", "REPARE"}
ETATS_A_FAIRE = {"NOT_OK", "A_REMPLACER", "A_FAIRE", "A_REPARER", "A_CONTROLER"}
ETATS_OK = {"OK", "BON", "FAIT", "PROPRE", "NETTOYE", "CONTROLE"}


@register.filter
def classe_etat(ligne):
    """Classe Tailwind de couleur pour l'état d'une ligne de rapport."""
    code = str(premier(ligne, "etat") or "")

    if code in ETATS_FAITS:
        return "text-blue-700"
    if code in ETATS_A_FAIRE:
        return "text-red-700"
    if code in ETATS_OK:
        return "text-green-700"
    return ""

"""
Validation et normalisation des plaques d'immatriculation par pays.

Chaque pays définit une liste de formats : (libellé, regex, gabarit de sortie).
La saisie est d'abord normalisée : majuscules, et tout séparateur
(espace, tiret, tiret long, point…) devient un espace simple. Les regex
sont écrites sur cette forme normalisée avec des séparateurs facultatifs
(« ?»), le gabarit reconstruit la forme officielle à partir des groupes.

Pour ajouter un format : ajouter une ligne dans FORMATS[<pays>].
"""
import re

from django.core.exceptions import ValidationError
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

LONGUEUR_MAX = 12  # = VoitureExemplaire.immatriculation.max_length

# Séparateurs acceptés à la saisie
_SEPARATEURS = re.compile(r"[\s\-‐-―._·/]+")

S = r"[ ]?"  # séparateur facultatif


def _rx(motif):
    return re.compile(r"^" + motif + r"$")


# Belgique — plaque personnalisée : nombre de caractères accepté
BE_PERSO_MIN = 5
BE_PERSO_MAX = 5


def _sidecodes(codes, sep="-"):
    """Formats néerlandais/portugais : 'XX-99-99' → regex + gabarit."""
    resultat = []
    for code in codes:
        blocs = code.split("-")
        motif = S.join(
            "([A-Z]{%d})" % len(b) if b[0] == "X" else r"(\d{%d})" % len(b)
            for b in blocs
        )
        gabarit = sep.join("{%d}" % i for i in range(len(blocs)))
        resultat.append((code.replace("X", "A").replace("9", "1"), _rx(motif), gabarit))
    return resultat


FORMATS = {
    "Belgique": [
        (_("Standard (1-ABC-123)"), _rx(r"([1-9])" + S + r"([A-Z]{3})" + S + r"(\d{3})"), "{0}-{1}-{2}"),
        (_("Oldtimer / Youngtimer (O-ABC-123)"), _rx(r"(O)" + S + r"([A-Z]{3})" + S + r"(\d{3})"), "{0}-{1}-{2}"),
        (_("Taxi (T-ABC-123)"), _rx(r"(T)" + S + r"([A-Z]{3})" + S + r"(\d{3})"), "{0}-{1}-{2}"),
        (_("Remorque (Q-ABC-123)"), _rx(r"(Q)" + S + r"([A-Z]{3})" + S + r"(\d{3})"), "{0}-{1}-{2}"),
        (_("Ancien format (ABC-123)"), _rx(r"([A-Z]{3})" + S + r"(\d{3})"), "{0}-{1}"),
        (_("Ancien format (123-ABC)"), _rx(r"(\d{3})" + S + r"([A-Z]{3})"), "{0}-{1}"),
        (
            format_lazy(
                _("Personnalisée ({n} caractères)"),
                n=BE_PERSO_MIN if BE_PERSO_MIN == BE_PERSO_MAX else f"{BE_PERSO_MIN}-{BE_PERSO_MAX}",
            ),
            _rx(r"(?=[A-Z0-9]*[A-Z])([A-Z0-9]{%d,%d})" % (BE_PERSO_MIN, BE_PERSO_MAX)),
            "{0}",
        ),
    ],
    "Luxembourg": [
        (_("Standard (AB 1234)"), _rx(r"([A-Z]{2})" + S + r"(\d{3,4})"), "{0} {1}"),
        (_("Numérique (12345)"), _rx(r"(\d{1,6})"), "{0}"),
    ],
    "France": [
        (_("SIV (AB-123-CD)"), _rx(r"([A-Z]{2})" + S + r"(\d{3})" + S + r"([A-Z]{2})"), "{0}-{1}-{2}"),
        (_("FNI (123 ABC 45)"), _rx(r"(\d{1,4})" + S + r"([A-Z]{1,3})" + S + r"(\d{2,3}|2A|2B)"), "{0} {1} {2}"),
    ],
    "Allemagne": [
        (
            _("Standard (B-AB 1234, suffixe E/H)"),
            _rx(r"([A-ZÄÖÜ]{1,3}) ([A-Z]{1,2})" + S + r"(\d{1,4})([EH]?)"),
            "{0}-{1} {2}{3}",
        ),
    ],
    "Pays-Bas": _sidecodes([
        "XX-99-99", "99-99-XX", "99-XX-99", "XX-99-XX", "XX-XX-99", "99-XX-XX",
        "99-XXX-9", "9-XXX-99", "XX-999-X", "X-999-XX", "XXX-99-X", "X-99-XXX",
        "9-XX-999", "999-XX-9",
    ]),
    "Portugal": _sidecodes(["XX-99-XX", "99-XX-99", "99-99-XX", "XX-99-99"]),
    "Italie": [
        (_("Standard (AB 123 CD)"), _rx(r"([A-Z]{2})" + S + r"(\d{3})" + S + r"([A-Z]{2})"), "{0} {1} {2}"),
    ],
    "Espagne": [
        (_("Standard (1234 BCD)"), _rx(r"(\d{4})" + S + r"([A-Z]{3})"), "{0} {1}"),
        (_("Provincial (M 1234 AB)"), _rx(r"([A-Z]{1,2})" + S + r"(\d{4})" + S + r"([A-Z]{1,2})"), "{0} {1} {2}"),
    ],
    "Royaume-Uni": [
        (_("Actuel (AB12 CDE)"), _rx(r"([A-Z]{2}\d{2})" + S + r"([A-Z]{3})"), "{0} {1}"),
        (_("Préfixe (A123 BCD)"), _rx(r"([A-Z]\d{1,3})" + S + r"([A-Z]{3})"), "{0} {1}"),
        (_("Suffixe (ABC 123D)"), _rx(r"([A-Z]{3})" + S + r"(\d{1,3}[A-Z])"), "{0} {1}"),
    ],
    "Suisse": [
        (_("Standard (ZH 123456)"), _rx(r"([A-Z]{2})" + S + r"(\d{1,6})"), "{0} {1}"),
    ],
}

# Pays sans format précis : alphanumérique libre, espaces et tirets conservés
_GENERIQUE = re.compile(r"^[A-Z0-9ÄÖÜÅÆØ]+([ -][A-Z0-9ÄÖÜÅÆØ]+)*$")


def normaliser_saisie(valeur):
    """Majuscules + séparateurs ramenés à un espace simple."""
    return _SEPARATEURS.sub(" ", (valeur or "").strip().upper()).strip()


def exemples(pays):
    """Libellés des formats acceptés pour un pays (aide à la saisie)."""
    return [str(libelle) for libelle, _r, _g in FORMATS.get(pays, [])]


def exemples_par_pays():
    return {pays: exemples(pays) for pays in FORMATS}


def valider_immatriculation(valeur, pays=None):
    """
    Retourne l'immatriculation au format officiel du pays.
    Lève ValidationError si elle ne correspond à aucun format connu.
    """
    saisie = normaliser_saisie(valeur)
    if not saisie:
        raise ValidationError(_("Indiquez l'immatriculation."))

    formats = FORMATS.get(pays)
    if formats:
        for _libelle, regex, gabarit in formats:
            m = regex.match(saisie)
            if m:
                resultat = gabarit.format(*m.groups())
                break
        else:
            raise ValidationError(
                _("Immatriculation invalide pour %(pays)s. Formats acceptés : %(formats)s."),
                params={"pays": pays, "formats": " ; ".join(exemples(pays))},
                code="format_pays",
            )
    else:
        saisie = re.sub(r"\s+", " ", (valeur or "").strip().upper())
        saisie = re.sub(r"[\u2010-\u2015]", "-", saisie)
        saisie = re.sub(r" ?- ?", "-", saisie)
        if not _GENERIQUE.match(saisie):
            raise ValidationError(
                _("L'immatriculation ne peut contenir que des lettres, des chiffres, des espaces et des tirets."),
                code="caracteres",
            )
        resultat = saisie

    if len(resultat) > LONGUEUR_MAX:
        raise ValidationError(
            _("L'immatriculation ne peut pas dépasser %(max)s caractères."),
            params={"max": LONGUEUR_MAX},
            code="longueur",
        )
    return resultat

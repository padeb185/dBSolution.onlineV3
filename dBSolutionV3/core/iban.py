"""
IBAN : nettoyage, mise en forme (groupes de 4) et contrôle.

Le contrôle d'un IBAN n'est pas l'algorithme de Luhn (réservé aux cartes bancaires) :
c'est la clé ISO 7064 « mod 97-10 » (les 2 chiffres après le code pays), plus la
longueur propre à chaque pays (BE = 16, FR = 27, DE = 22, NL = 18, LU = 20…).
"""
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Longueurs officielles (registre SWIFT) des principaux pays
LONGUEURS = {
    "AD": 24, "AT": 20, "BE": 16, "BG": 22, "CH": 21, "CY": 28, "CZ": 24, "DE": 22, "DK": 18,
    "EE": 20, "ES": 24, "FI": 18, "FR": 27, "GB": 22, "GI": 23, "GR": 27, "HR": 21, "HU": 28,
    "IE": 22, "IS": 26, "IT": 27, "LI": 21, "LT": 20, "LU": 20, "LV": 21, "MC": 27, "MT": 31,
    "NL": 18, "NO": 15, "PL": 28, "PT": 25, "RO": 24, "SE": 24, "SI": 19, "SK": 24, "SM": 27,
    "VA": 22, "MA": 28, "TN": 24, "TR": 26,
}


def normaliser_iban(valeur):
    """'be68 5390-0754 7034' → 'BE68539007547034'."""
    return re.sub(r"[^A-Za-z0-9]", "", valeur or "").upper()


def formater_iban(valeur):
    """'BE68539007547034' → 'BE68 5390 0754 7034' (groupes de 4, tout l'IBAN)."""
    v = normaliser_iban(valeur)
    return " ".join(v[i:i + 4] for i in range(0, len(v), 4))


def cle_mod97_valide(iban):
    v = normaliser_iban(iban)
    if len(v) < 5:
        return False
    deplace = v[4:] + v[:4]
    reste = 0
    for car in deplace:
        if car.isdigit():
            reste = (reste * 10 + int(car)) % 97
        elif car.isalpha():
            reste = (reste * 100 + (ord(car) - 55)) % 97
        else:
            return False
    return reste == 1


def erreur_iban(valeur):
    """Message d'erreur précis, ou None si l'IBAN est valide."""
    v = normaliser_iban(valeur)
    if not v:
        return None
    if not re.match(r"^[A-Z]{2}[0-9]{2}[A-Z0-9]+$", v):
        return _("L'IBAN doit commencer par le code pays (2 lettres) suivi de 2 chiffres de contrôle.")
    attendu = LONGUEURS.get(v[:2])
    if attendu and len(v) != attendu:
        return _("Un IBAN %(pays)s compte %(attendu)s caractères (%(saisi)s saisis).") % {
            "pays": v[:2], "attendu": attendu, "saisi": len(v)}
    if not (15 <= len(v) <= 34):
        return _("Longueur d'IBAN invalide.")
    if not cle_mod97_valide(v):
        return _("Clé de contrôle IBAN incorrecte (mod 97) : vérifiez le numéro saisi.")
    return None


def validate_iban(valeur):
    """Validateur Django (formulaires / modèles)."""
    message = erreur_iban(valeur)
    if message:
        raise ValidationError(message, code="iban_invalide")


def nettoyer_iban_formulaire(valeur):
    """À utiliser dans clean_<champ> : renvoie l'IBAN compact (ou None) ou lève ValidationError."""
    v = normaliser_iban(valeur)
    if not v:
        return None
    validate_iban(v)
    return v

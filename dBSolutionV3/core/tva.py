"""
Numéro de TVA : nettoyage et mise en forme à l'affichage.

Le numéro est enregistré tel quel (format compact conseillé : BE0123456789, utilisé par Peppol) ;
seul l'affichage est mis en forme selon l'usage du pays :
  BE 0123.456.789   FR 12 345 678 901   NL 123456789 B01   DE 123 456 789   LU 12345678 …
"""
import re

PAYS_UE = {
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR", "HR", "HU", "IE", "IT",
    "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK", "XI", "CH", "GB", "NO",
}


def normaliser_tva(valeur):
    """'be 0123.456.789' → 'BE0123456789'."""
    return re.sub(r"[^A-Za-z0-9]", "", str(valeur or "")).upper()


def _grouper(chiffres, tailles, sep=" "):
    morceaux, i = [], 0
    for t in tailles:
        if i >= len(chiffres):
            break
        morceaux.append(chiffres[i:i + t])
        i += t
    if i < len(chiffres):
        morceaux.append(chiffres[i:])
    return sep.join(morceaux)


def _belge(chiffres):
    if len(chiffres) == 9:          # ancien format à 9 chiffres → 0 devant
        chiffres = "0" + chiffres
    if len(chiffres) == 10 and chiffres.isdigit():
        return f"{chiffres[:4]}.{chiffres[4:7]}.{chiffres[7:]}"
    return chiffres


def formater_tva(valeur):
    """Numéro de TVA mis en forme pour l'affichage (valeur d'origine si non reconnu)."""
    if not valeur:
        return valeur
    v = normaliser_tva(valeur)
    pays, reste = v[:2], v[2:]
    if not (pays.isalpha() and pays in PAYS_UE):
        # sans préfixe pays : numéro d'entreprise belge (0123.456.789) reconnu, sinon inchangé
        if v.isdigit() and len(v) in (9, 10):
            return _belge(v)
        return str(valeur).strip()

    if pays == "BE":
        corps = _belge(reste)
    elif pays == "FR" and len(reste) == 11:
        corps = f"{reste[:2]} {_grouper(reste[2:], [3, 3, 3])}"
    elif pays == "NL" and len(reste) == 12 and reste[9] == "B":
        corps = f"{reste[:9]} {reste[9:]}"
    elif pays == "DE" and len(reste) == 9 and reste.isdigit():
        corps = _grouper(reste, [3, 3, 3])
    elif pays == "GB" and len(reste) in (9, 12) and reste.isdigit():
        corps = _grouper(reste, [3, 4, 2, 3])
    elif pays == "CH" and reste.startswith("E") and len(reste) >= 10:
        # Suisse : CHE-123.456.789 (+ MWST / TVA / IVA éventuel)
        return f"CHE-{_grouper(reste[1:10], [3, 3, 3], '.')}" + (f" {reste[10:]}" if reste[10:] else "")
    else:
        corps = reste
    return f"{pays} {corps}"

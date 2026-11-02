"""
Comptabilisation par pays.

Toutes les écritures de l'application sont produites sur des comptes internes (numérotation PCMN belge,
utilisée aussi par le bilan). À l'affichage et à l'export (journal général, balance), elles sont
converties dans le plan comptable national du pays de la société :

    BE → PCMN (inchangé)
    DE → SKR03 (DATEV Standardkontenrahmen 03, le plus répandu dans les PME et garages)

    from compta.plans_comptables import convertir_ecritures, plan_du_pays
    E = convertir_ecritures(E, "DE")   # e["compte"] devient le compte SKR03, e["compte_pcmn"] garde l'origine

⚠ Correspondance proposée pour les comptes utilisés par l'application : à valider par le Steuerberater.
"""
from django.utils.translation import gettext_lazy as _

# PCMN (interne) → (SKR03, intitulé allemand)
SKR03 = {
    # Classe 1 – fonds propres, provisions, dettes à long terme
    "100000": ("0800", "Gezeichnetes Kapital"),
    "130000": ("0846", "Gesetzliche Rücklage"),
    "140000": ("0860", "Gewinnvortrag vor Verwendung"),
    "170000": ("0650", "Verbindlichkeiten gegenüber Kreditinstituten (Restlaufzeit > 5 Jahre)"),
    "173000": ("0640", "Verbindlichkeiten gegenüber Kreditinstituten (Restlaufzeit 1–5 Jahre)"),
    # Classe 2 – immobilisations
    "200000": ("0010", "Konzessionen, gewerbliche Schutzrechte"),
    "210000": ("0027", "EDV-Software"),
    "220000": ("0065", "Unbebaute Grundstücke"),
    "221000": ("0090", "Geschäftsbauten"),
    "221900": ("0090", "Geschäftsbauten"),
    "230000": ("0210", "Maschinen"),
    "230900": ("0210", "Maschinen"),
    "235500": ("0440", "Werkzeuge"),
    "240000": ("0420", "Technische Büroeinrichtung"),
    "240900": ("0420", "Technische Büroeinrichtung"),
    "241000": ("0320", "Pkw"),
    "241900": ("0320", "Pkw"),
    "260000": ("0400", "Betriebsausstattung"),
    "260900": ("0400", "Betriebsausstattung"),
    "280000": ("0510", "Beteiligungen"),
    # Classe 3 – stocks
    "340000": ("3980", "Bestand Waren"),
    # Classe 4 – créances et dettes à un an au plus
    "400000": ("1400", "Forderungen aus Lieferungen und Leistungen"),
    "411000": ("1576", "Abziehbare Vorsteuer 19 %"),
    "416000": ("1500", "Sonstige Vermögensgegenstände"),
    "416100": ("1500", "Sonstige Vermögensgegenstände"),
    "430000": ("0630", "Verbindlichkeiten gegenüber Kreditinstituten (Restlaufzeit bis 1 Jahr)"),
    "440000": ("1600", "Verbindlichkeiten aus Lieferungen und Leistungen"),
    "451000": ("1776", "Umsatzsteuer 19 %"),
    "453000": ("1741", "Verbindlichkeiten aus Lohn- und Kirchensteuer"),
    "454000": ("1742", "Verbindlichkeiten im Rahmen der sozialen Sicherheit"),
    "454100": ("1742", "Verbindlichkeiten im Rahmen der sozialen Sicherheit"),
    "455000": ("1740", "Verbindlichkeiten aus Lohn und Gehalt"),
    "456000": ("0970", "Sonstige Rückstellungen (Urlaub)"),
    "459000": ("1742", "Verbindlichkeiten im Rahmen der sozialen Sicherheit"),
    "460000": ("1710", "Erhaltene Anzahlungen auf Bestellungen"),
    "480000": ("1700", "Sonstige Verbindlichkeiten"),
    "489000": ("1700", "Sonstige Verbindlichkeiten"),
    "490000": ("0980", "Aktive Rechnungsabgrenzung"),
    "492000": ("1700", "Sonstige Verbindlichkeiten (antizipative Abgrenzung)"),
    "499000": ("1590", "Durchlaufende Posten"),
    # Classe 5 – trésorerie
    "550000": ("1200", "Bank"),
    "570000": ("1000", "Kasse"),
    "580000": ("1360", "Geldtransit"),
    # Classe 6 – charges
    "600000": ("3400", "Wareneingang 19 % Vorsteuer"),
    "604000": ("3400", "Wareneingang 19 % Vorsteuer"),
    "604100": ("3400", "Wareneingang 19 % Vorsteuer"),
    "609400": ("3960", "Bestandsveränderungen"),
    "610000": ("4900", "Sonstige betriebliche Aufwendungen"),
    "612700": ("4500", "Fahrzeugkosten"),
    "612710": ("4500", "Fahrzeugkosten"),
    "612720": ("4500", "Fahrzeugkosten"),
    "613000": ("3100", "Fremdleistungen"),
    "618000": ("4127", "Geschäftsführergehälter"),
    "620200": ("4120", "Gehälter"),
    "620300": ("4110", "Löhne"),
    "621000": ("4130", "Gesetzliche soziale Aufwendungen"),
    "625000": ("4120", "Gehälter (Zuführung Urlaubsrückstellung)"),
    "630200": ("4830", "Abschreibungen auf Sachanlagen"),
    "640000": ("4900", "Sonstige betriebliche Aufwendungen"),
    "650000": ("2100", "Zinsen und ähnliche Aufwendungen"),
    "663000": ("2310", "Anlagenabgänge Sachanlagen (Restbuchwert bei Buchverlust)"),
    "670000": ("2200", "Körperschaftsteuer"),
    # Classe 7 – produits
    "700000": ("8400", "Erlöse 19 % USt"),
    "750000": ("2650", "Sonstige Zinsen und ähnliche Erträge"),
    "763000": ("2720", "Erträge aus dem Abgang von Gegenständen des Anlagevermögens"),
}

# Compte non listé : compte SKR03 par défaut selon le début du numéro PCMN
SKR03_DEFAUT = [
    ("10", ("0800", "Gezeichnetes Kapital")), ("13", ("0855", "Andere Gewinnrücklagen")),
    ("14", ("0860", "Gewinnvortrag vor Verwendung")), ("16", ("0970", "Sonstige Rückstellungen")),
    ("17", ("0650", "Verbindlichkeiten gegenüber Kreditinstituten")), ("2", ("0400", "Betriebsausstattung")),
    ("3", ("3980", "Bestand Waren")), ("40", ("1400", "Forderungen aus Lieferungen und Leistungen")),
    ("41", ("1500", "Sonstige Vermögensgegenstände")), ("44", ("1600", "Verbindlichkeiten aus Lieferungen und Leistungen")),
    ("45", ("1700", "Sonstige Verbindlichkeiten")), ("4", ("1700", "Sonstige Verbindlichkeiten")),
    ("55", ("1200", "Bank")), ("57", ("1000", "Kasse")), ("5", ("1360", "Geldtransit")),
    ("60", ("3400", "Wareneingang")), ("61", ("4900", "Sonstige betriebliche Aufwendungen")),
    ("62", ("4100", "Löhne und Gehälter")), ("63", ("4830", "Abschreibungen auf Sachanlagen")),
    ("64", ("4900", "Sonstige betriebliche Aufwendungen")), ("65", ("2100", "Zinsen und ähnliche Aufwendungen")),
    ("66", ("2300", "Sonstige Aufwendungen")), ("67", ("2200", "Körperschaftsteuer")),
    ("70", ("8400", "Erlöse 19 % USt")), ("7", ("2700", "Sonstige Erträge")),
]

PLANS = {
    "DE": {"code": "SKR03", "nom": _("SKR03 (DATEV Standardkontenrahmen 03)"), "comptes": SKR03, "defaut": SKR03_DEFAUT},
}


def plan_du_pays(pays):
    """Plan national du pays, ou None si l'application utilise le PCMN tel quel (Belgique, autres pays)."""
    return PLANS.get((pays or "").upper())


def compte_national(compte_pcmn, pays):
    """(compte national, intitulé national) ou (compte_pcmn, '') si pas de plan national."""
    plan = plan_du_pays(pays)
    compte_pcmn = str(compte_pcmn or "")
    if not plan:
        return compte_pcmn, ""
    if compte_pcmn in plan["comptes"]:
        return plan["comptes"][compte_pcmn]
    for prefixe, valeur in plan["defaut"]:
        if compte_pcmn.startswith(prefixe):
            return valeur
    return compte_pcmn, ""


def convertir_ecritures(ecritures, pays):
    """Convertit les lignes du journal dans le plan national (sans modifier les montants)."""
    if not plan_du_pays(pays):
        return ecritures
    resultat = []
    for e in ecritures:
        compte, intitule = compte_national(e["compte"], pays)
        resultat.append(dict(e, compte_pcmn=e["compte"], compte=compte, intitule=intitule or e.get("intitule", "")))
    return resultat

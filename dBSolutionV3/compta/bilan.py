"""
Comptes annuels belges (schéma BNB – présentation du schéma complet, rubriques et codes) :
bilan après répartition non effectuée (le résultat de l'exercice est présenté séparément)
et compte de résultats, établis à partir du journal général (classes 1 à 7 du PCMN).
"""
from collections import OrderedDict
from datetime import date
from decimal import Decimal

from django.utils.translation import gettext_lazy as _

from .journal import ecritures_societe

ZERO = Decimal("0.00")

# ----------------------------------------------------------------------
# Rubriques : clé -> (code BNB, libellé)
# ----------------------------------------------------------------------
ACTIF = OrderedDict([
    ("frais_etablissement", ("20", _("I. Frais d'établissement"))),
    ("immo_incorporelles", ("21", _("II. Immobilisations incorporelles"))),
    ("terrains_constructions", ("22", _("A. Terrains et constructions"))),
    ("installations", ("23", _("B. Installations, machines et outillage"))),
    ("mobilier_roulant", ("24", _("C. Mobilier et matériel roulant"))),
    ("location_financement", ("25", _("D. Location-financement et droits similaires"))),
    ("autres_corporelles", ("26", _("E. Autres immobilisations corporelles"))),
    ("en_cours", ("27", _("F. Immobilisations en cours et acomptes versés"))),
    ("immo_financieres", ("28", _("IV. Immobilisations financières"))),
    ("creances_plus_un_an", ("29", _("V. Créances à plus d'un an"))),
    ("stocks", ("3", _("VI. Stocks et commandes en cours d'exécution"))),
    ("creances_commerciales", ("40", _("A. Créances commerciales"))),
    ("autres_creances", ("41", _("B. Autres créances"))),
    ("placements", ("50/53", _("VIII. Placements de trésorerie"))),
    ("disponible", ("54/58", _("IX. Valeurs disponibles"))),
    ("regul_actif", ("490/1", _("X. Comptes de régularisation"))),
])

PASSIF = OrderedDict([
    ("capital", ("10/11", _("I. Apport (capital)"))),
    ("plus_values_reevaluation", ("12", _("II. Plus-values de réévaluation"))),
    ("reserves", ("13", _("III. Réserves"))),
    ("resultat_reporte", ("14", _("IV. Bénéfice (Perte) reporté(e)"))),
    ("resultat_exercice", ("9904", _("Bénéfice (Perte) de l'exercice (à affecter)"))),
    ("subsides", ("15", _("V. Subsides en capital"))),
    ("provisions", ("16", _("VII. Provisions et impôts différés"))),
    ("dettes_plus_un_an", ("17", _("VIII. Dettes à plus d'un an"))),
    ("dettes_echeant", ("42", _("A. Dettes à plus d'un an échéant dans l'année"))),
    ("dettes_financieres", ("43", _("B. Dettes financières"))),
    ("dettes_commerciales", ("44", _("C. Dettes commerciales"))),
    ("acomptes_recus", ("46", _("D. Acomptes reçus sur commandes"))),
    ("dettes_impots", ("450/3", _("E1. Impôts"))),
    ("dettes_remunerations", ("454/9", _("E2. Rémunérations et charges sociales"))),
    ("autres_dettes", ("47/48", _("F. Autres dettes"))),
    ("regul_passif", ("492/3", _("X. Comptes de régularisation"))),
])

RESULTATS = OrderedDict([
    ("chiffre_affaires", ("70", _("A. Chiffre d'affaires"))),
    ("variation_en_cours", ("71", _("B. Variation des en-cours de fabrication, des produits finis et des commandes en cours"))),
    ("production_immobilisee", ("72", _("C. Production immobilisée"))),
    ("autres_produits_exploitation", ("74", _("D. Autres produits d'exploitation"))),
    ("produits_non_recurrents_exploitation", ("76A", _("E. Produits d'exploitation non récurrents"))),
    ("approvisionnements", ("60", _("A. Approvisionnements et marchandises"))),
    ("services", ("61", _("B. Services et biens divers"))),
    ("remunerations", ("62", _("C. Rémunérations, charges sociales et pensions"))),
    ("amortissements", ("630", _("D. Amortissements et réductions de valeur sur frais d'établissement, sur immobilisations incorporelles et corporelles"))),
    ("reductions_valeur", ("631/4", _("E. Réductions de valeur sur stocks, sur commandes en cours et sur créances commerciales"))),
    ("provisions_rc", ("635/8", _("F. Provisions pour risques et charges"))),
    ("autres_charges_exploitation", ("640/8", _("G. Autres charges d'exploitation"))),
    ("charges_non_recurrentes_exploitation", ("66A", _("I. Charges d'exploitation non récurrentes"))),
    ("produits_financiers", ("75/76B", _("IV. Produits financiers"))),
    ("charges_financieres", ("65/66B", _("V. Charges financières"))),
    ("impots", ("67/77", _("IX. Impôts sur le résultat"))),
    ("autres_resultat", ("68/79", _("Prélèvements / transferts (impôts différés, réserves immunisées)"))),
])

PRODUITS = {"chiffre_affaires", "variation_en_cours", "production_immobilisee", "autres_produits_exploitation",
            "produits_non_recurrents_exploitation", "produits_financiers"}


def rubrique_bilan(compte, solde):
    """(côté, rubrique) d'un compte de bilan selon son solde (débit – crédit)."""
    c = compte
    deb = solde >= 0
    if c.startswith("20"): return "A", "frais_etablissement"
    if c.startswith("21"): return "A", "immo_incorporelles"
    if c.startswith("22"): return "A", "terrains_constructions"
    if c.startswith("23"): return "A", "installations"
    if c.startswith("24"): return "A", "mobilier_roulant"
    if c.startswith("25"): return "A", "location_financement"
    if c.startswith("26"): return "A", "autres_corporelles"
    if c.startswith("27"): return "A", "en_cours"
    if c.startswith("28"): return "A", "immo_financieres"
    if c.startswith("29"): return "A", "creances_plus_un_an"
    if c.startswith("3"): return "A", "stocks"
    if c.startswith("40"): return ("A", "creances_commerciales") if deb else ("P", "acomptes_recus")
    if c.startswith("41"): return ("A", "autres_creances") if deb else ("P", "autres_dettes")
    if c.startswith("42"): return "P", "dettes_echeant"
    if c.startswith("43"): return "P", "dettes_financieres"
    if c.startswith("44"): return ("P", "dettes_commerciales") if not deb else ("A", "autres_creances")
    if c[:3] in ("450", "451", "452", "453"): return ("P", "dettes_impots") if not deb else ("A", "autres_creances")
    if c.startswith("45"): return ("P", "dettes_remunerations") if not deb else ("A", "autres_creances")
    if c.startswith("46"): return "P", "acomptes_recus"
    if c.startswith("47") or c.startswith("48"): return ("P", "autres_dettes") if not deb else ("A", "autres_creances")
    if c[:3] in ("490", "491"): return "A", "regul_actif"
    if c[:3] in ("492", "493"): return "P", "regul_passif"
    if c.startswith("49"): return ("A", "autres_creances") if deb else ("P", "autres_dettes")
    if c[:2] in ("50", "51", "52", "53"): return "A", "placements"
    if c.startswith("5"): return ("A", "disponible") if deb else ("P", "dettes_financieres")
    if c.startswith("10") or c.startswith("11"): return "P", "capital"
    if c.startswith("12"): return "P", "plus_values_reevaluation"
    if c.startswith("13"): return "P", "reserves"
    if c.startswith("14"): return "P", "resultat_reporte"
    if c.startswith("15"): return "P", "subsides"
    if c.startswith("16"): return "P", "provisions"
    if c.startswith("17"): return "P", "dettes_plus_un_an"
    if c.startswith("19"): return "P", "capital"
    return ("A", "autres_creances") if deb else ("P", "autres_dettes")


def rubrique_resultat(compte):
    c = compte
    if c.startswith("70"): return "chiffre_affaires"
    if c.startswith("71"): return "variation_en_cours"
    if c.startswith("72"): return "production_immobilisee"
    if c.startswith("73") or c.startswith("74"): return "autres_produits_exploitation"
    if c[:3] in ("760", "761", "762", "763", "764"): return "produits_non_recurrents_exploitation"
    if c.startswith("75") or c.startswith("76"): return "produits_financiers"
    if c.startswith("77"): return "impots"
    if c.startswith("78") or c.startswith("79"): return "autres_resultat"
    if c.startswith("60"): return "approvisionnements"
    if c.startswith("61"): return "services"
    if c.startswith("62"): return "remunerations"
    if c.startswith("630"): return "amortissements"
    if c[:3] in ("631", "632", "633", "634"): return "reductions_valeur"
    if c[:3] in ("635", "636", "637", "638"): return "provisions_rc"
    if c.startswith("63") or c.startswith("64"): return "autres_charges_exploitation"
    if c[:3] in ("660", "661", "662", "663", "664"): return "charges_non_recurrentes_exploitation"
    if c.startswith("65") or c.startswith("66"): return "charges_financieres"
    if c.startswith("67"): return "impots"
    return "autres_resultat"


def _soldes(ecritures):
    s = {}
    for e in ecritures:
        s[e["compte"]] = s.get(e["compte"], ZERO) + e["debit"] - e["credit"]
    return s


def _resultat(soldes):
    """Montants des rubriques du compte de résultats (produits positifs, charges positives)."""
    r = {k: ZERO for k in RESULTATS}
    for compte, solde in soldes.items():
        if compte[:1] not in ("6", "7"):
            continue
        k = rubrique_resultat(compte)
        if k in ("impots", "autres_resultat"):
            r[k] += solde            # montant net en charge
        elif k in PRODUITS:
            r[k] += -solde           # produit : solde créditeur
        else:
            r[k] += solde            # charge : solde débiteur
    ventes = sum((r[k] for k in ("chiffre_affaires", "variation_en_cours", "production_immobilisee",
                                 "autres_produits_exploitation", "produits_non_recurrents_exploitation")), ZERO)
    cout = sum((r[k] for k in ("approvisionnements", "services", "remunerations", "amortissements",
                               "reductions_valeur", "provisions_rc", "autres_charges_exploitation",
                               "charges_non_recurrentes_exploitation")), ZERO)
    exploitation = ventes - cout
    avant_impots = exploitation + r["produits_financiers"] - r["charges_financieres"]
    exercice = avant_impots - r["impots"] - r["autres_resultat"]
    return r, {"ventes": ventes, "cout": cout, "exploitation": exploitation,
               "avant_impots": avant_impots, "exercice": exercice}


def comptes_annuels(societe, annee):
    """Bilan au 31/12/annee et compte de résultats de l'exercice (année civile)."""
    debut, fin = date(annee, 1, 1), date(annee, 12, 31)
    toutes = ecritures_societe(societe, None, fin)
    cumul = _soldes(toutes)
    exercice = _soldes([e for e in toutes if e["date"] >= debut])
    anterieur = _soldes([e for e in toutes if e["date"] < debut])

    actif = {k: ZERO for k in ACTIF}
    passif = {k: ZERO for k in PASSIF}
    detail = {}
    for compte, solde in sorted(cumul.items()):
        if compte[:1] in ("6", "7", "8", "9") or not solde:
            continue
        cote, k = rubrique_bilan(compte, solde)
        montant = solde if cote == "A" else -solde
        (actif if cote == "A" else passif)[k] += montant
        detail.setdefault(k, []).append({"compte": compte, "montant": montant})

    # Résultats des exercices antérieurs non affectés → reporté ; exercice → à affecter
    _r, tot_ant = _resultat(anterieur)
    passif["resultat_reporte"] += tot_ant["exercice"]
    rubriques_resultat, totaux_resultat = _resultat(exercice)
    passif["resultat_exercice"] = totaux_resultat["exercice"]

    t = lambda d, cles: sum((d[k] for k in cles), ZERO)
    immo_corp = t(actif, ["terrains_constructions", "installations", "mobilier_roulant", "location_financement",
                          "autres_corporelles", "en_cours"])
    actifs_immobilises = actif["immo_incorporelles"] + immo_corp + actif["immo_financieres"]
    creances_un_an = actif["creances_commerciales"] + actif["autres_creances"]
    actifs_circulants = (actif["creances_plus_un_an"] + actif["stocks"] + creances_un_an + actif["placements"]
                         + actif["disponible"] + actif["regul_actif"])
    total_actif = actif["frais_etablissement"] + actifs_immobilises + actifs_circulants

    capitaux_propres = t(passif, ["capital", "plus_values_reevaluation", "reserves", "resultat_reporte",
                                  "resultat_exercice", "subsides"])
    dettes_fiscales = passif["dettes_impots"] + passif["dettes_remunerations"]
    dettes_un_an = t(passif, ["dettes_echeant", "dettes_financieres", "dettes_commerciales", "acomptes_recus",
                              "autres_dettes"]) + dettes_fiscales
    dettes = passif["dettes_plus_un_an"] + dettes_un_an + passif["regul_passif"]
    total_passif = capitaux_propres + passif["provisions"] + dettes

    return {
        "annee": annee, "actif": actif, "passif": passif, "detail": detail,
        "resultat": rubriques_resultat, "totaux_resultat": totaux_resultat,
        "totaux": {
            "immo_corporelles": immo_corp, "actifs_immobilises": actifs_immobilises,
            "creances_un_an": creances_un_an, "actifs_circulants": actifs_circulants, "total_actif": total_actif,
            "capitaux_propres": capitaux_propres, "dettes_fiscales": dettes_fiscales, "dettes_un_an": dettes_un_an,
            "dettes": dettes, "total_passif": total_passif, "ecart": total_actif - total_passif,
        },
        "nb_ecritures": len(toutes),
    }


def _ligne(code, libelle, n, n1, niveau=2, gras=False):
    return {"code": code, "libelle": libelle, "n": n, "n1": n1, "niveau": niveau, "gras": gras}


def presentation(ca, cb):
    """Lignes à afficher (exercice N et N-1) du bilan et du compte de résultats."""
    A, P, T, R, TR = ca["actif"], ca["passif"], ca["totaux"], ca["resultat"], ca["totaux_resultat"]
    A1, P1, T1, R1, TR1 = cb["actif"], cb["passif"], cb["totaux"], cb["resultat"], cb["totaux_resultat"]
    act = lambda k, niveau=2: _ligne(ACTIF[k][0], ACTIF[k][1], A[k], A1[k], niveau)
    pas = lambda k, niveau=2: _ligne(PASSIF[k][0], PASSIF[k][1], P[k], P1[k], niveau)
    res = lambda k, niveau=2: _ligne(RESULTATS[k][0], RESULTATS[k][1], R[k], R1[k], niveau)
    tot = lambda code, lib, k, niveau=1: _ligne(code, lib, T[k], T1[k], niveau, True)

    actif = [
        act("frais_etablissement", 1),
        tot("21/28", _("ACTIFS IMMOBILISÉS"), "actifs_immobilises", 0),
        act("immo_incorporelles", 1),
        tot("22/27", _("III. Immobilisations corporelles"), "immo_corporelles", 1),
        act("terrains_constructions"), act("installations"), act("mobilier_roulant"),
        act("location_financement"), act("autres_corporelles"), act("en_cours"),
        act("immo_financieres", 1),
        tot("29/58", _("ACTIFS CIRCULANTS"), "actifs_circulants", 0),
        act("creances_plus_un_an", 1), act("stocks", 1),
        tot("40/41", _("VII. Créances à un an au plus"), "creances_un_an", 1),
        act("creances_commerciales"), act("autres_creances"),
        act("placements", 1), act("disponible", 1), act("regul_actif", 1),
        tot("20/58", _("TOTAL DE L'ACTIF"), "total_actif", 0),
    ]
    passif = [
        tot("10/15", _("CAPITAUX PROPRES"), "capitaux_propres", 0),
        pas("capital", 1), pas("plus_values_reevaluation", 1), pas("reserves", 1),
        pas("resultat_reporte", 1), pas("resultat_exercice", 1), pas("subsides", 1),
        pas("provisions", 0),
        tot("17/49", _("DETTES"), "dettes", 0),
        pas("dettes_plus_un_an", 1),
        tot("42/48", _("IX. Dettes à un an au plus"), "dettes_un_an", 1),
        pas("dettes_echeant"), pas("dettes_financieres"), pas("dettes_commerciales"), pas("acomptes_recus"),
        tot("45", _("E. Dettes fiscales, salariales et sociales"), "dettes_fiscales", 2),
        pas("dettes_impots", 3), pas("dettes_remunerations", 3), pas("autres_dettes"),
        pas("regul_passif", 1),
        tot("10/49", _("TOTAL DU PASSIF"), "total_passif", 0),
    ]
    tr = lambda code, lib, k, niveau=0: _ligne(code, lib, TR[k], TR1[k], niveau, True)
    resultats = [
        tr("70/76A", _("I. Ventes et prestations"), "ventes"),
        res("chiffre_affaires"), res("variation_en_cours"), res("production_immobilisee"),
        res("autres_produits_exploitation"), res("produits_non_recurrents_exploitation"),
        tr("60/66A", _("II. Coût des ventes et des prestations"), "cout"),
        res("approvisionnements"), res("services"), res("remunerations"), res("amortissements"),
        res("reductions_valeur"), res("provisions_rc"), res("autres_charges_exploitation"),
        res("charges_non_recurrentes_exploitation"),
        tr("9901", _("III. Bénéfice (Perte) d'exploitation"), "exploitation"),
        res("produits_financiers", 0), res("charges_financieres", 0),
        tr("9903", _("VI. Bénéfice (Perte) de l'exercice avant impôts"), "avant_impots"),
        res("impots", 0), res("autres_resultat", 0),
        tr("9904", _("Bénéfice (Perte) de l'exercice"), "exercice"),
    ]
    return actif, passif, resultats

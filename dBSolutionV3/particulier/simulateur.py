"""
Simulateur d'achat d'un véhicule (formule Bronze) : prêt auto, taxes de mise en circulation, taxe de roulage
annuelle, immatriculation et plaques, puis rapport financier de l'éventuel achat (coût total, coût net, par mois,
par km) sur la durée de détention.

Pays : Belgique (Wallonie, Bruxelles, Flandre), France (13 régions), Luxembourg, Pays-Bas, Allemagne.
Règles 2026 relevées sur des sources publiques (service-public.gouv.fr pour la France, sites spécialisés pour les
autres) : montants INDICATIFS, à vérifier sur les calculateurs officiels ; chaque montant peut être imposé à la main.
"""
import math
from decimal import ROUND_HALF_UP, Decimal as D

from django.utils.translation import gettext as _

from .calculs import mensualite_pret


def r2(x):
    return D(str(x or 0)).quantize(D("0.01"), rounding=ROUND_HALF_UP)


# ==================================================================
# BELGIQUE
# ==================================================================
# Chevaux fiscaux belges selon la cylindrée (cm³) : (cylindrée maximale, CV)
CV_BE = [(750, 4), (950, 5), (1150, 6), (1350, 7), (1550, 8), (1750, 9), (1950, 10), (2150, 11), (2350, 12),
         (2550, 13), (2750, 14), (3050, 15), (3250, 16), (3450, 17), (3650, 18), (3850, 19), (4050, 20)]
# Taxe de circulation annuelle Wallonie / Bruxelles par CV (2026-2027) ; 13, 14, 16 à 19 CV interpolés
TAXE_CIRC_BE = {4: 107.18, 5: 134.11, 6: 193.91, 7: 253.31, 8: 313.24, 9: 373.16, 10: 432.30, 11: 561.00, 12: 689.70,
                13: 818.31, 14: 946.92, 15: 1075.54, 16: 1408.79, 17: 1742.03, 18: 2075.28, 19: 2408.52, 20: 2741.77}
# Wallonie, TMC depuis le 01/07/2025 : base selon les kW
TMC_WAL_BASE = [(70, 64.01), (85, 128.02), (100, 515.20), (110, 902.37), (120, 1289.55), (155, 2579.10), (None, 5159.25)]
# Bruxelles, TMC : le plus élevé des barèmes CV et kW
TMC_BRU = [(8, 70, 78.88), (10, 85, 157.76), (11, 100, 634.89), (14, 110, 1112.01), (15, 120, 1589.14),
           (17, 155, 3178.28), (None, None, 6357.85)]


def cv_belges(cylindree):
    if not cylindree:
        return 4
    for maxi, cv in CV_BE:
        if cylindree <= maxi:
            return cv
    return 20 + math.ceil((cylindree - 4050) / 200)


def taxe_circulation_be(cv):
    if cv <= 4:
        return D("107.18")
    if cv <= 20:
        return r2(TAXE_CIRC_BE[cv])
    return r2(2741.77 + (cv - 20) * 149.56)


def tmc_wallonie(p):
    if p["energie"] == "electrique" and (p["kw"] or 0) <= 120:
        coef = D("0.01")
    elif p["energie"] == "electrique":
        coef = D("0.10")
    elif p["energie"] in ("hybride", "phev"):
        coef = D("0.8")
    else:
        coef = D("1")
    base = next(m for seuil, m in TMC_WAL_BASE if seuil is None or (p["kw"] or 0) <= seuil)
    co2 = D(p["co2"] or 0) if p["energie"] != "electrique" else D(136)
    masse = D(p["masse"] or 1838) if p["energie"] != "electrique" else D(1838)
    montant = D(str(base)) * (co2 / 136) * (masse / 1838) * coef
    montant = min(max(montant, D(50)), D(9000))
    if p["age"]:
        montant = max(montant * max(D(1) - D("0.1") * D(str(p["age"])), D(0)), D("61.50"))
    return r2(montant)


def tmc_bruxelles(p):
    cv, kw = p["cv_be"], p["kw"] or 0
    if p["energie"] == "electrique":
        montant = D("78.88")
    else:
        # Le plus élevé des deux barèmes (CV fiscaux ou kW)
        par_cv = next(m for cvmax, _k, m in TMC_BRU if cvmax is None or cv <= cvmax)
        par_kw = next(m for _c, kwmax, m in TMC_BRU if kwmax is None or kw <= kwmax)
        montant = D(str(max(par_cv, par_kw)))
    if p["age"]:
        montant = max(montant * max(D(1) - D("0.1") * D(str(p["age"])), D(0)), D("78.88"))
    return r2(montant)


def biv_flandre(p):
    if p["energie"] == "electrique":
        return D("61.50")
    co2 = float(p["co2"] or 0)
    air = 628.29 if p["energie"] == "diesel" else 28.54
    montant = ((co2 * 1.245) / 246) ** 6 * 4500 + air
    if p["energie"] == "gpl":
        montant -= 298                      # réduction LPG (indicative)
    montant *= max(1 - 0.1 * (p["age"] or 0), 0.1)
    return r2(min(max(montant, 58.16), 14539))


def verkeersbelasting_flandre(p):
    if p["energie"] == "electrique":
        return D("60.94")
    base = float(taxe_circulation_be(p["cv_be"]))
    co2 = float(p["co2"] or 149)
    montant = base * (1 + 0.003 * (co2 - 149))
    montant *= 1.15 if p["energie"] == "diesel" else 0.85
    montant *= 1.10                                   # opcentiemen communaux
    return r2(max(montant, 60.94))


# ==================================================================
# FRANCE
# ==================================================================
REGIONS_FR = {
    "ARA": ("Auvergne-Rhône-Alpes", 43.00), "BFC": ("Bourgogne-Franche-Comté", 60.00), "BRE": ("Bretagne", 60.00),
    "CVL": ("Centre-Val de Loire", 60.00), "COR": ("Corse", 53.00), "GES": ("Grand Est", 60.00),
    "HDF": ("Hauts-de-France", 43.00), "IDF": ("Île-de-France", 68.95), "NOR": ("Normandie", 60.00),
    "NAQ": ("Nouvelle-Aquitaine", 58.00), "OCC": ("Occitanie", 59.50), "PDL": ("Pays de la Loire", 51.00),
    "PAC": ("Provence-Alpes-Côte d'Azur", 60.00),
}
# Malus CO2 2026 (WLTP) : 108 g → 50 € … 191 g → 79 911 € ; au-delà 80 000 €
MALUS_CO2_FR = [50, 75, 100, 125, 150, 170, 190, 210, 230, 240, 260, 280, 310, 330, 360, 400, 450, 540, 650, 740, 818,
                898, 983, 1074, 1172, 1276, 1386, 1504, 1629, 1761, 1901, 2049, 2205, 2370, 2544, 2726, 2918, 3119, 3331,
                3552, 3784, 4026, 4279, 4543, 4818, 5105, 5404, 5715, 6126, 6537, 7248, 7959, 8770, 9681, 10692, 11803,
                13014, 14325, 15736, 17247, 18858, 20569, 22380, 24291, 26302, 28413, 30624, 32935, 35346, 37857, 40468,
                43179, 45990, 48901, 51912, 55023, 58134, 61245, 64356, 67467, 70578, 73689, 76800, 79911]
MALUS_POIDS_FR = [(1500, 1700, 10), (1700, 1800, 15), (1800, 1900, 20), (1900, 2000, 25), (2000, None, 30)]


def cv_fiscaux_fr(co2, kw):
    """Puissance administrative française : CO2 / 45 + (kW / 40) ^ 1,6, arrondie."""
    if not kw:
        return None
    return max(1, round((co2 or 0) / 45 + (kw / 40) ** 1.6))


def malus_co2_fr(co2):
    co2 = int(co2 or 0)
    if co2 < 108:
        return D(0)
    if co2 > 191:
        return D(80000)
    return D(MALUS_CO2_FR[co2 - 108])


def malus_poids_fr(masse, energie):
    if energie == "electrique" or not masse:
        return D(0)
    masse -= {"hybride": 100, "phev": min(200, int(masse * 0.15))}.get(energie, 0)
    total = D(0)                     # calcul marginal, tranche par tranche (ex. officiel : 1 950 kg → 6 775 €)
    for debut, fin, prix in MALUS_POIDS_FR:
        if masse >= debut:
            kg = (min(masse, fin - 1) - debut + 1) if fin else (masse - debut + 1)
            total += D(kg) * prix
    return total


def carte_grise_fr(p):
    cv = p["cv_fr"] or 1
    taux = D(str(REGIONS_FR.get(p["region"], REGIONS_FR["IDF"])[1]))
    regionale = D(cv) * taux
    if p["energie"] == "electrique" and p["region"] == "HDF":
        regionale /= 2
    if (p["age"] or 0) >= 10:
        regionale /= 2
    return r2(regionale + D("11") + D("2.76"))


# ==================================================================
# LUXEMBOURG, PAYS-BAS, ALLEMAGNE
# ==================================================================
def taxe_luxembourg(p):
    """Estimation : CO2 × 1 € (essence) / × 1,5 (diesel), minimum 30 € (électrique 30 €)."""
    if p["energie"] == "electrique":
        return D(30)
    facteur = D("1.5") if p["energie"] == "diesel" else D("1")
    return r2(max(D(p["co2"] or 0) * facteur, D(30)))


# BPM 2026 (essence) : (début de tranche g/km, montant au début, € par gramme)
BPM_NL = [(0, 687, 2), (77, 841, 82), (100, 2727, 181), (139, 9786, 297), (155, 14538, 594)]
# Dépréciation forfaitaire des occasions importées : (âge en mois, % au début, % par mois)
BPM_DEPRECIATION = [(0, 0, 12), (1, 12, 4), (3, 20, 3.5), (5, 27, 1.5), (9, 33, 1), (18, 42, 0.75), (30, 51, 0.5),
                    (42, 57, 0.42), (54, 62, 0.42), (66, 67, 0.42), (78, 72, 0.25), (90, 75, 0.25), (102, 78, 0.25),
                    (114, 81, 0.19)]


def bpm_nl(p):
    if p["energie"] == "electrique":
        brut = 687.0
    else:
        co2 = int(p["co2"] or 0)
        debut, montant, prix = [t for t in BPM_NL if co2 >= t[0]][-1]
        brut = montant + (co2 - debut) * prix
        if p["energie"] == "diesel" and co2 > 69:
            brut += (co2 - 69) * 114.83
    if p["age"]:
        mois = int(p["age"] * 12)
        debut, pct, par_mois = [t for t in BPM_DEPRECIATION if mois >= t[0]][-1]
        depreciation = min(pct + (mois - debut) * par_mois, 100) if mois < 234 else 100
        brut *= (1 - depreciation / 100)
    return r2(brut)


def mrb_nl(p):
    """Estimation annuelle : 126 € / trimestre à 1 000 kg (essence, opcenten compris), +22 € par 100 kg ;
    diesel × 1,85 ; électrique 70 % du tarif essence (2026)."""
    masse = (p["masse"] or 1300)
    trimestre = max(126 + (masse - 1000) / 100 * 22, 60)
    if p["energie"] == "diesel":
        trimestre *= 1.85
    elif p["energie"] == "electrique":
        trimestre *= 0.70
    return r2(trimestre * 4)


KFZ_CO2_DE = [(95, 115, 2.00), (115, 135, 2.20), (135, 155, 2.50), (155, 175, 2.90), (175, 195, 3.40), (195, None, 4.00)]


def kfz_steuer_de(p):
    if p["energie"] == "electrique":
        return D(0)                                   # exonérée (jusqu'en 2035)
    cyl = p["cylindree"] or 0
    taux = 9.50 if p["energie"] == "diesel" else 2.00
    montant = math.ceil(cyl / 100) * taux
    co2 = int(p["co2"] or 0)
    for debut, fin, prix in KFZ_CO2_DE:
        if co2 > debut:
            montant += ((min(co2, fin) if fin else co2) - debut) * prix
    return r2(montant)


# Immatriculation et plaques (estimations, hors plaque personnalisée)
FRAIS_IMMAT = {
    "BE": (D("30"), D("0"), D("1000")),     # plaque DIV 30 € (certificat inclus) ; plaque personnalisée 1 000 €
    "FR": (D("0"), D("35"), D("0")),        # carte grise comptée à part ; plaques ~35 €
    "LU": (D("55"), D("40"), D("0")),
    "NL": (D("50"), D("30"), D("0")),
    "DE": (D("30"), D("35"), D("12.80")),   # Wunschkennzeichen ~12,80 €
}


# ==================================================================
# SIMULATION
# ==================================================================
def _nombre(d, cle, defaut=None, entier=False):
    v = d.get(cle)
    if v in (None, ""):
        return defaut
    try:
        return int(float(v)) if entier else float(v)
    except (TypeError, ValueError):
        return defaut


def simuler(d):
    pays = (d.get("pays") or "BE").upper()
    p = {
        "pays": pays,
        "region": d.get("region") or {"BE": "wallonie", "FR": "IDF"}.get(pays, ""),
        "energie": d.get("energie") or "essence",
        "co2": _nombre(d, "co2", 0),
        "kw": _nombre(d, "kw", 0),
        "cylindree": _nombre(d, "cylindree", 0, True),
        "masse": _nombre(d, "masse", None, True),
        "age": _nombre(d, "age", 0),                 # âge du véhicule (années) : 0 = neuf
    }
    p["cv_be"] = cv_belges(p["cylindree"])
    p["cv_fr"] = _nombre(d, "cv_fiscaux", None, True) or cv_fiscaux_fr(p["co2"], p["kw"])
    prix = D(str(_nombre(d, "prix", 0)))

    # ---------------- Taxes à l'achat et taxe annuelle
    lignes_achat, annuel, notes = [], D(0), []
    if pays == "BE":
        region = p["region"]
        if region == "flandre":
            lignes_achat.append({"code": "tmc", "libelle": _("Taxe de mise en circulation (BIV)"), "montant": biv_flandre(p)})
            annuel = verkeersbelasting_flandre(p)
        elif region == "bruxelles":
            lignes_achat.append({"code": "tmc", "libelle": _("Taxe de mise en circulation (TMC)"), "montant": tmc_bruxelles(p)})
            annuel = taxe_circulation_be(p["cv_be"]) if p["energie"] != "electrique" else D("107.18")
        else:
            lignes_achat.append({"code": "tmc", "libelle": _("Taxe de mise en circulation (TMC)"), "montant": tmc_wallonie(p)})
            annuel = taxe_circulation_be(p["cv_be"]) if p["energie"] != "electrique" else D("107.18")
        notes.append(_("Belgique : %(cv)s CV fiscaux (cylindrée).") % {"cv": p["cv_be"]})
    elif pays == "FR":
        lignes_achat.append({"code": "carte_grise", "libelle": _("Certificat d'immatriculation (carte grise)"),
                             "montant": carte_grise_fr(p)})
        if not p["age"] or d.get("premiere_immatriculation_france"):
            malus = min(malus_co2_fr(p["co2"]) if p["energie"] != "electrique" else D(0), D(80000))
            poids = malus_poids_fr(p["masse"], p["energie"])
            total_malus = min(malus + poids, D(80000))
            if malus:
                lignes_achat.append({"code": "malus", "libelle": _("Malus écologique (CO2)"), "montant": r2(malus)})
            if poids and total_malus > malus:
                lignes_achat.append({"code": "malus_poids", "libelle": _("Malus au poids"), "montant": r2(total_malus - malus)})
        notes.append(_("France : %(cv)s CV fiscaux ; pas de taxe annuelle pour un particulier.") % {"cv": p["cv_fr"]})
    elif pays == "LU":
        annuel = taxe_luxembourg(p)
        notes.append(_("Luxembourg : taxe annuelle estimée selon le CO2 (minimum 30 €)."))
    elif pays == "NL":
        bpm = bpm_nl(p)
        if bpm:
            lignes_achat.append({"code": "bpm", "libelle": _("BPM (taxe d'achat)"), "montant": bpm})
        annuel = mrb_nl(p)
        notes.append(_("Pays-Bas : BPM payée à la première immatriculation aux Pays-Bas ; MRB estimée selon la masse (moyenne des provinces)."))
    elif pays == "DE":
        annuel = kfz_steuer_de(p)
        notes.append(_("Allemagne : voiture électrique exonérée de Kfz-Steuer jusqu'en 2035."))

    immat, plaques, perso = FRAIS_IMMAT.get(pays, (D(0), D(0), D(0)))
    if immat:
        lignes_achat.append({"code": "immatriculation", "libelle": _("Immatriculation"), "montant": immat})
    if plaques:
        lignes_achat.append({"code": "plaques", "libelle": _("Plaques"), "montant": plaques})
    if d.get("plaque_personnalisee") and perso:
        lignes_achat.append({"code": "plaque_perso", "libelle": _("Plaque personnalisée"), "montant": perso})
    # Montants imposés à la main
    for l in lignes_achat:
        force = d.get(f"force_{l['code']}")
        if force not in (None, ""):
            l["montant"], l["force"] = r2(force), True
    if d.get("force_annuel") not in (None, ""):
        annuel = r2(d["force_annuel"])
    taxes_achat = r2(sum((l["montant"] for l in lignes_achat), D(0)))

    # ---------------- Prêt
    apport = D(str(_nombre(d, "apport", 0)))
    duree = _nombre(d, "duree_mois", 0, True)
    taux = D(str(_nombre(d, "taux", 0)))
    capital = max(prix - apport, D(0))
    pret = None
    if duree and capital:
        mensualite = mensualite_pret(capital, taux, duree)
        total_rembourse = r2(mensualite * duree)
        restant, r, tableau = capital, taux / 1200, []
        for n in range(1, duree + 1):
            i = restant * r
            restant = max(restant - (mensualite - i), D(0))
            if n % 12 == 0 or n == duree:
                tableau.append({"mois": n, "capital_restant": r2(restant)})
        pret = {"capital": r2(capital), "mensualite": mensualite, "duree_mois": duree, "taux": taux,
                "total_rembourse": total_rembourse, "cout_credit": r2(total_rembourse - capital), "tableau": tableau}

    # ---------------- Rapport financier sur la durée de détention
    annees = D(str(_nombre(d, "annees_detention", 5)))
    km_an = D(str(_nombre(d, "km_an", 15000)))
    conso = D(str(_nombre(d, "conso", 6)))              # L ou kWh / 100 km
    prix_energie = D(str(_nombre(d, "prix_energie", 1.75)))
    assurance = D(str(_nombre(d, "assurance_an", 0)))
    entretien = D(str(_nombre(d, "entretien_an", 0)))
    revente = d.get("valeur_revente")
    if revente in (None, ""):
        # Décote indicative : −20 % la première année puis −15 % par an
        decote = D("0.80") * D("0.85") ** max(int(annees) - 1, 0) if annees >= 1 else D(1)
        revente = r2(prix * decote)
    else:
        revente = r2(revente)
    energie_an = r2(km_an * conso / 100 * prix_energie)
    postes = [
        {"code": "prix", "libelle": _("Prix d'achat"), "montant": r2(prix)},
        {"code": "taxes_achat", "libelle": _("Taxes et immatriculation"), "montant": taxes_achat},
        {"code": "credit", "libelle": _("Coût du crédit"), "montant": pret["cout_credit"] if pret else D(0)},
        {"code": "taxe_annuelle", "libelle": _("Taxe de circulation"), "montant": r2(annuel * annees)},
        {"code": "energie", "libelle": _("Carburant / énergie"), "montant": r2(energie_an * annees)},
        {"code": "assurance", "libelle": _("Assurance"), "montant": r2(assurance * annees)},
        {"code": "entretien", "libelle": _("Entretiens et réparations"), "montant": r2(entretien * annees)},
    ]
    postes = [x for x in postes if x["montant"]]
    cout_total = r2(sum((x["montant"] for x in postes), D(0)))
    cout_net = r2(cout_total - revente)
    mois = annees * 12
    km_total = km_an * annees
    return {
        "parametres": {**p, "cv_fiscaux": p["cv_fr"] if pays == "FR" else p["cv_be"] if pays == "BE" else None},
        "taxes_achat": {"lignes": [{**l, "libelle": str(l["libelle"])} for l in lignes_achat], "total": taxes_achat},
        "taxe_annuelle": annuel,
        "pret": pret,
        "rapport": {
            "annees": annees, "km_total": int(km_total), "energie_an": energie_an,
            "postes": [{**x, "libelle": str(x["libelle"])} for x in postes],
            "cout_total": cout_total, "valeur_revente": revente, "cout_net": cout_net,
            "cout_mois": r2(cout_net / mois) if mois else None,
            "cout_km": (cout_net / km_total).quantize(D("0.001")) if km_total else None,
            "budget_mensuel": r2((pret["mensualite"] if pret else D(0)) + (annuel + energie_an + assurance + entretien) / 12),
            "a_payer_achat": r2((apport if pret else prix) + taxes_achat),
        },
        "notes": [str(n) for n in notes] + [str(_("Montants indicatifs (règles 2026) : vérifiez sur les calculateurs officiels."))],
        "regions_fr": {k: v[0] for k, v in REGIONS_FR.items()},
    }

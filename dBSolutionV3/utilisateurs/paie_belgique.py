"""
Calcul d'une paie mensuelle belge (secteur privé) – paramètres 2026.

Brut (+ heures supplémentaires) -> brut majoré (108 % ouvriers) -> ONSS
travailleur 13,07 % – bonus à l'emploi (proratisé temps partiel)
-> imposable (+ avantages en nature) -> précompte professionnel
(formule-clé annexe III) -> cotisation spéciale de sécurité sociale
-> net.  Double pécule de vacances (employés) et prime de fin d'année
(13e mois) calculés à part ; informations congés payés (droit, solde, simple pécule).
Coût employeur = brut + cotisations patronales – réduction structurelle
– réduction groupe-cible + cotisations / provision vacances
+ cotisation de solidarité CO2.

⚠ Estimation : ne remplace pas le calcul d'un secrétariat social agréé.
Les paramètres sont regroupés ci-dessous pour être mis à jour chaque année.
"""
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

D = Decimal
ZERO = D("0")
CENT = D("0.01")


def r2(x):
    return D(x).quantize(CENT, rounding=ROUND_HALF_UP)


# ==================================================================
# PARAMÈTRES 2026
# ==================================================================
ANNEE_PARAMETRES = 2026
HEURES_MOIS_TEMPS_PLEIN = D("164.67")        # 38 h × 52 / 12

TAUX_ONSS_TRAVAILLEUR = D("13.07")           # %
COEF_BRUT_MAJORE_OUVRIER = D("1.08")
TAUX_PATRONAL_DEFAUT = D("25.00")            # % taux facial secteur marchand

# ---- Bonus à l'emploi social (01/07/2026, montants temps plein)
BONUS_EMPLOI = {  # statut: (max A, pente A, max B, pente B)
    "employe": (D("127.54"), D("0.2739"), D("171.99"), D("0.2699")),
    "ouvrier": (D("137.74"), D("0.2958"), D("185.75"), D("0.2915")),
}
BONUS_A_S1, BONUS_A_S2 = D("2937.93"), D("3403.62")
BONUS_B_S1, BONUS_B_S2 = D("2300.62"), D("2937.93")
BONUS_FISCAL_A, BONUS_FISCAL_B = D("0.3314"), D("0.5254")

# ---- Précompte professionnel – formule-clé
FRAIS_PRO_TAUX = D("0.30")
FRAIS_PRO_MAX = D("6070.00")
BAREME = [  # (seuil, impôt cumulé au seuil, taux)
    (D("0.00"), D("0.00"), D("0.2675")),
    (D("16710.00"), D("4469.93"), D("0.4280")),
    (D("29500.00"), D("9944.05"), D("0.4815")),
    (D("51050.00"), D("20320.38"), D("0.5350")),
]
REDUCTION_QUOTITE_EXEMPTEE = D("2987.98")
REDUCTION_QUOTITE_EXEMPTEE_COUPLE = D("5975.96")
QUOTIENT_CONJUGAL_TAUX = D("0.30")
QUOTIENT_CONJUGAL_MAX = D("13790.00")

REDUCTION_ENFANTS = {0: D("0"), 1: D("52"), 2: D("138"), 3: D("367"), 4: D("635"),
                     5: D("925"), 6: D("1216"), 7: D("1510"), 8: D("1833")}
REDUCTION_ENFANT_SUPPLEMENTAIRE = D("322")
REDUCTION_PARENT_ISOLE = D("52")
REDUCTION_BENEFICIAIRE_HANDICAPE = D("52")
REDUCTION_CONJOINT_HANDICAPE = D("52")

# Heures supplémentaires : réduction de précompte (sur la rémunération
# de base des heures sup), max 180 h / an
REDUCTION_PP_HEURES_SUP = {20: D("0.6681"), 50: D("0.5775"), 100: D("0.5775")}
HEURES_SUP_MAX_AN = 180

# ---- Cotisation spéciale de sécurité sociale (retenue mensuelle)
CSSS_SEUIL_1 = D("1095.09")
CSSS_SEUIL_2 = D("1945.38")
CSSS_SEUIL_3 = D("2190.18")
CSSS_SEUIL_4 = D("6038.82")
CSSS_FORFAIT_DEUX_REVENUS = D("9.30")
CSSS_MAX_ISOLE = D("60.94")
CSSS_MAX_DEUX_REVENUS = D("51.64")

# ---- Pécule de vacances
DOUBLE_PECULE_TAUX = D("0.92")               # employés : 92 % du brut mensuel
DOUBLE_PECULE_PART_ONSS = D("0.85")          # ONSS 13,07 % sur 85 %
PRECOMPTE_PECULE = [  # (rémunération annuelle brute jusqu'à, taux)
    (D("10675.00"), D("0.0000")),
    (D("13660.00"), D("0.1917")),
    (D("17375.00"), D("0.2120")),
    (D("20840.00"), D("0.2625")),
    (D("23580.00"), D("0.3130")),
    (D("26340.00"), D("0.3433")),
    (D("31830.00"), D("0.3634")),
    (D("34640.00"), D("0.3937")),
    (D("45860.00"), D("0.4239")),
    (D("59900.00"), D("0.4744")),
    (None, D("0.5350")),
]
COTISATION_VACANCES_OUVRIER = D("15.84")     # % (5,57 trim. + 10,27 annuelle) sur 108 %

# ---- Congés payés (vacances annuelles)
CONGES_JOURS_TEMPS_PLEIN = D("20")           # régime 5 jours / semaine, année complète
SALAIRE_JOURNALIER_COEF = D("3") / D("65")   # salaire journalier = mensuel × 3 / 65 (5 jours / semaine)
PECULE_OUVRIER_TAUX = D("15.38")             # % du brut à 108 % de l'exercice (payé par la caisse de vacances)

# ---- Prime de fin d'année (13e mois)
#   CP 200 : un salaire mensuel brut, au prorata des mois prestés / assimilés (année civile) ;
#   CP 112 : taux horaire au 1er décembre × horaire hebdomadaire × 52 / 12, période du 01/12 au 30/11,
#            payée au plus tard le 20 décembre (min. 3 mois d'ancienneté).
#   Précompte : barème des allocations exceptionnelles (mêmes taux que le pécule de vacances).

# ---- Réduction structurelle (catégorie 1, à partir du 01/07/2026, par trimestre)
STRUCT_F = D("0")
STRUCT_ALPHA, STRUCT_S0 = D("0.14"), D("11687.74")
STRUCT_DELTA, STRUCT_S2 = D("0.16"), D("9738.14")

# ---- Voiture de société
ATN_CO2_REFERENCE = {"essence": 70, "lpg": 70, "cng": 70, "diesel": 58}
ATN_POURCENTAGE_BASE = D("5.5")
ATN_POURCENTAGE_MIN, ATN_POURCENTAGE_MAX = D("4"), D("18")
ATN_MINIMUM_ANNUEL = D("1690.00")
ATN_COEF_AGE = [(12, D("1.00")), (24, D("0.94")), (36, D("0.88")),
                (48, D("0.82")), (60, D("0.76")), (None, D("0.70"))]
CO2_INDEX = D("185.85") / D("114.08")
CO2_FORFAIT = {"essence": 768, "diesel": 600, "lpg": 990, "cng": 990}
CO2_MINIMUM = D("33.93")
CO2_COEF_APRES_07_2023 = D("4.00")

# ==================================================================
# BARÈMES DES COMMISSIONS PARITAIRES
# ==================================================================
# CP 112 (garages, ouvriers) – minimums horaires au 01/02/2026
CP112_TAUX_HORAIRES = {
    "A1": D("16.46"), "A2": D("17.20"), "A2_1": D("18.06"), "B1": D("18.92"),
    "B2": D("19.95"), "C1": D("20.98"), "C2": D("22.02"), "D1": D("23.05"), "D2": D("24.08"),
}

# CP 200 (employés) – minimums mensuels au 01/01/2026, par classe et expérience (0–26 ans)
_CP200_I = {
    "A": "2242.81 2249.57 2256.28 2263.06 2269.90 2276.51 2283.27 2289.96 2297.16 2315.80 2334.52 2350.42 2366.19 2382.16 2397.80 2413.37 2428.84 2444.35 2459.89",
    "B": "2336.25 2349.64 2363.08 2376.61 2394.83 2413.37 2427.38 2462.42 2497.56 2532.54 2567.80 2597.46 2626.81 2656.48 2685.87 2715.45 2725.03 2734.55 2744.25 2753.78 2763.42 2773.18 2782.63 2792.25 2801.86 2811.39 2820.99",
    "C": "2369.31 2369.31 2422.73 2469.70 2516.65 2563.76 2610.73 2657.89 2705.05 2752.17 2799.16 2846.25 2893.29 2930.44 2967.49 3004.68 3041.73 3078.85 3089.44 3100.07 3110.73 3121.59 3132.28 3143.19 3153.91 3164.86 3175.61",
    "D": "2555.73 2572.63 2589.26 2606.19 2671.93 2730.41 2788.83 2847.10 2905.53 2963.62 3022.34 3080.46 3139.00 3197.28 3255.71 3304.78 3353.79 3402.80 3451.91 3500.99 3518.35 3535.83 3553.29 3570.59 3587.83 3605.11 3622.42",
}
# Barème II : employé depuis au moins 1 an dans l'entreprise (expérience 1–26)
_CP200_II = {
    "A": "2310.30 2317.19 2324.14 2330.81 2337.66 2344.46 2351.35 2358.93 2378.04 2397.33 2413.71 2429.89 2446.31 2462.42 2478.44 2494.33 2510.24 2526.16",
    "B": "2413.09 2426.87 2440.76 2459.32 2478.44 2492.88 2528.90 2565.14 2601.10 2637.36 2667.83 2698.00 2728.54 2758.86 2789.20 2799.07 2808.85 2818.89 2828.76 2838.66 2848.50 2858.33 2868.34 2878.15 2887.96 2897.83",
    "C": "2433.25 2488.16 2536.36 2584.73 2633.22 2681.47 2730.03 2778.60 2827.02 2875.48 2923.83 2972.20 3010.43 3048.53 3086.76 3124.96 3163.20 3174.02 3184.94 3195.97 3207.12 3218.09 3229.43 3240.49 3251.76 3262.72",
    "D": "2642.08 2659.13 2676.55 2744.52 2804.72 2864.69 2924.79 2984.80 3044.74 3105.00 3164.92 3225.06 3285.11 3345.24 3395.69 3446.06 3496.57 3547.01 3597.56 3615.45 3633.38 3651.35 3669.27 3686.98 3704.65 3722.55",
}
CP200_BAREME_I = {k: [D(x) for x in v.split()] for k, v in _CP200_I.items()}
CP200_BAREME_II = {k: [D(x) for x in v.split()] for k, v in _CP200_II.items()}

# Revenu minimum mensuel moyen garanti (CP 100 / minimum national) – 01/07/2026
RMMMG = D("2233.61")


def minimum_cp(commission_paritaire, categorie="", classe="", experience=0, bareme_ii=False):
    """Retourne (taux horaire minimum, salaire mensuel minimum) temps plein."""
    if commission_paritaire == "CP112":
        taux = CP112_TAUX_HORAIRES.get(categorie)
        return (taux, r2(taux * HEURES_MOIS_TEMPS_PLEIN)) if taux else (None, None)

    if commission_paritaire == "CP200" and classe:
        exp = max(0, int(experience or 0))
        if bareme_ii and exp >= 1:
            ligne = CP200_BAREME_II.get(classe, [])
            idx = exp - 1
        else:
            ligne = CP200_BAREME_I.get(classe, [])
            idx = exp
        if not ligne:
            return None, None
        mensuel = ligne[min(idx, len(ligne) - 1)]
        return r2(mensuel / HEURES_MOIS_TEMPS_PLEIN), mensuel

    if commission_paritaire == "RMMMG":
        return r2(RMMMG / HEURES_MOIS_TEMPS_PLEIN), RMMMG

    return None, None


# ==================================================================
# CALCULS
# ==================================================================
def bonus_emploi(salaire_temps_plein, statut, fraction=D("1")):
    """Bonus à l'emploi social mensuel (volet A, volet B), proratisé."""
    max_a, pente_a, max_b, pente_b = BONUS_EMPLOI.get(statut, BONUS_EMPLOI["employe"])
    s = D(salaire_temps_plein)

    if s <= BONUS_A_S1:
        a = max_a
    elif s <= BONUS_A_S2:
        a = max(ZERO, max_a - pente_a * (s - BONUS_A_S1))
    else:
        a = ZERO

    if s <= BONUS_B_S1:
        b = max_b
    elif s <= BONUS_B_S2:
        b = max(ZERO, max_b - pente_b * (s - BONUS_B_S1))
    else:
        b = ZERO

    return r2(a * fraction), r2(b * fraction)


def impot_bareme(revenu_annuel):
    revenu = max(ZERO, D(revenu_annuel))
    impot = ZERO
    for seuil, cumul, taux in BAREME:
        if revenu >= seuil:
            impot = cumul + (revenu - seuil) * taux
    return impot


def reduction_enfants(nombre):
    n = max(0, int(nombre or 0))
    if n <= 8:
        return REDUCTION_ENFANTS[n]
    return REDUCTION_ENFANTS[8] + (n - 8) * REDUCTION_ENFANT_SUPPLEMENTAIRE


def precompte_professionnel(imposable_mensuel, situation_familiale,
                            nombre_enfants=0, nombre_enfants_handicapes=0,
                            parent_isole=False, beneficiaire_handicape=False,
                            conjoint_handicape=False, bonus_a=ZERO, bonus_b=ZERO,
                            reduction_heures_sup=ZERO):
    annuel = D(imposable_mensuel) * 12
    frais = min(annuel * FRAIS_PRO_TAUX, FRAIS_PRO_MAX)
    net_annuel = annuel - frais

    un_revenu = situation_familiale == "marie_un_revenu"
    if un_revenu:
        part_conjoint = min(net_annuel * QUOTIENT_CONJUGAL_TAUX, QUOTIENT_CONJUGAL_MAX)
        impot = impot_bareme(net_annuel - part_conjoint) + impot_bareme(part_conjoint)
        impot -= REDUCTION_QUOTITE_EXEMPTEE_COUPLE
    else:
        impot = impot_bareme(net_annuel) - REDUCTION_QUOTITE_EXEMPTEE

    mensuel = max(ZERO, impot) / 12

    enfants = int(nombre_enfants or 0) + int(nombre_enfants_handicapes or 0)
    reductions = reduction_enfants(enfants)
    if parent_isole and enfants > 0 and not un_revenu:
        reductions += REDUCTION_PARENT_ISOLE
    if beneficiaire_handicape:
        reductions += REDUCTION_BENEFICIAIRE_HANDICAPE
    if conjoint_handicape and un_revenu:
        reductions += REDUCTION_CONJOINT_HANDICAPE

    reductions += D(bonus_a) * BONUS_FISCAL_A + D(bonus_b) * BONUS_FISCAL_B
    reductions += D(reduction_heures_sup)

    return r2(max(ZERO, mensuel - reductions))


def cotisation_speciale_securite_sociale(brut_onss, situation_familiale):
    """Retenue mensuelle CSSS (base : brut soumis ONSS, 108 % ouvriers)."""
    s = D(brut_onss)
    deux_revenus = situation_familiale == "marie_deux_revenus"

    if s <= CSSS_SEUIL_1:
        return ZERO
    if s <= CSSS_SEUIL_2:
        return CSSS_FORFAIT_DEUX_REVENUS if deux_revenus else ZERO
    if s <= CSSS_SEUIL_3:
        montant = (s - CSSS_SEUIL_2) * D("0.076")
        if deux_revenus:
            montant = max(montant, CSSS_FORFAIT_DEUX_REVENUS)
        return r2(montant)
    if s <= CSSS_SEUIL_4:
        montant = D("18.60") + (s - CSSS_SEUIL_3) * D("0.011")
        return r2(min(montant, CSSS_MAX_DEUX_REVENUS if deux_revenus else CSSS_MAX_ISOLE))
    return CSSS_MAX_DEUX_REVENUS if deux_revenus else CSSS_MAX_ISOLE


def double_pecule_employe(brut_mensuel_temps_plein, fraction=D("1")):
    """Double pécule de vacances d'un employé (92 % du brut mensuel)."""
    brut_mensuel = D(brut_mensuel_temps_plein) * fraction
    brut = r2(brut_mensuel * DOUBLE_PECULE_TAUX)
    onss = r2(brut_mensuel * DOUBLE_PECULE_PART_ONSS * TAUX_ONSS_TRAVAILLEUR / 100)
    annuel = brut_mensuel * 12
    taux = PRECOMPTE_PECULE[-1][1]
    for plafond, t in PRECOMPTE_PECULE:
        if plafond is None or annuel <= plafond:
            taux = t
            break
    precompte = r2((brut - onss) * taux)
    return {"brut": brut, "onss": onss, "precompte": precompte, "net": r2(brut - onss - precompte)}


def taux_precompte_exceptionnel(brut_mensuel_normal):
    """Taux du précompte des allocations exceptionnelles (pécule, 13e mois) selon le brut annuel normal."""
    annuel = D(brut_mensuel_normal or 0) * 12
    for plafond, t in PRECOMPTE_PECULE:
        if plafond is None or annuel <= plafond:
            return t
    return PRECOMPTE_PECULE[-1][1]


def prime_fin_annee(montant_reference, mois_prestes=12, statut="employe", brut_mensuel_normal=None):
    """
    Prime de fin d'année (13e mois) : référence × mois prestés / 12.
    ONSS 13,07 % (sur 108 % pour un ouvrier, sans bonus à l'emploi), précompte des allocations exceptionnelles.
    """
    mois = max(0, min(12, int(mois_prestes or 0)))
    brut = r2(D(montant_reference or 0) * mois / 12)
    if brut <= 0:
        return None
    base_onss = r2(brut * COEF_BRUT_MAJORE_OUVRIER) if statut == "ouvrier" else brut
    onss = r2(base_onss * TAUX_ONSS_TRAVAILLEUR / 100)
    taux = taux_precompte_exceptionnel(brut_mensuel_normal if brut_mensuel_normal is not None else montant_reference)
    precompte = r2((brut - onss) * taux)
    return {
        "reference": r2(montant_reference or 0),
        "mois": mois,
        "brut": brut,
        "base_onss": base_onss,
        "onss": onss,
        "taux_precompte": r2(taux * 100),
        "precompte": precompte,
        "net": r2(brut - onss - precompte),
    }


def conges_payes(statut, brut_mensuel, jours_pris=0, jours_droit=None, fraction=D("1"), brut_majore=None):
    """
    Informations congés payés du mois :
      - employé : simple pécule = salaire maintenu des jours pris (compris dans le salaire du mois) ;
      - ouvrier : jours payés par la caisse de vacances (pécule simple + double ≈ 15,38 % du brut à 108 %
        de l'année précédente) — estimation annuelle sur la base du mois.
    """
    jours = D(jours_pris or 0)
    journalier = r2(D(brut_mensuel or 0) * SALAIRE_JOURNALIER_COEF)
    droit = D(jours_droit) if jours_droit not in (None, "") else r2(CONGES_JOURS_TEMPS_PLEIN * D(fraction or 1))
    info = {"droit": droit, "jours_pris": jours, "salaire_journalier": journalier,
            "simple_pecule": ZERO, "pecule_ouvrier_annuel": ZERO}
    if statut == "ouvrier":
        base = D(brut_majore if brut_majore is not None else D(brut_mensuel or 0) * COEF_BRUT_MAJORE_OUVRIER)
        info["pecule_ouvrier_annuel"] = r2(base * 12 * PECULE_OUVRIER_TAUX / 100)
    else:
        info["simple_pecule"] = r2(journalier * jours)
    return info


def reduction_structurelle(brut_onss_mensuel, fraction=D("1")):
    """Réduction structurelle mensuelle (catégorie 1)."""
    if fraction <= 0:
        return ZERO
    s = D(brut_onss_mensuel) * 3 / fraction           # salaire trimestriel temps plein
    r = STRUCT_F
    if s < STRUCT_S0:
        r += STRUCT_ALPHA * (STRUCT_S0 - s)
    if s < STRUCT_S2:
        r += STRUCT_DELTA * (STRUCT_S2 - s)
    return r2(max(ZERO, r) * fraction / 3)


def mois_entre(debut, fin):
    return (fin.year - debut.year) * 12 + (fin.month - debut.month)


def atn_voiture(valeur_catalogue, co2, carburant, date_immatriculation, date_paie):
    """Avantage de toute nature mensuel pour une voiture de société."""
    if not valeur_catalogue:
        return ZERO
    if carburant == "electrique":
        pourcentage = ATN_POURCENTAGE_MIN
    else:
        ref = ATN_CO2_REFERENCE.get(carburant, 70)
        pourcentage = ATN_POURCENTAGE_BASE + D("0.1") * (int(co2 or 0) - ref)
        pourcentage = min(max(pourcentage, ATN_POURCENTAGE_MIN), ATN_POURCENTAGE_MAX)

    coef = D("1.00")
    if date_immatriculation:
        age = mois_entre(date_immatriculation, date_paie) + 1
        for limite, c in ATN_COEF_AGE:
            if limite is None or age <= limite:
                coef = c
                break

    annuel = D(valeur_catalogue) * coef * D(6) / D(7) * pourcentage / 100
    return r2(max(annuel, ATN_MINIMUM_ANNUEL) / 12)


def cotisation_co2(co2, carburant, commandee_apres_07_2023=False):
    """Cotisation de solidarité CO2 mensuelle (à charge de l'employeur)."""
    if carburant == "electrique":
        montant = CO2_MINIMUM
    else:
        forfait = CO2_FORFAIT.get(carburant, 768)
        montant = (D(int(co2 or 0)) * 9 - forfait) / 12 * CO2_INDEX
        if commandee_apres_07_2023:
            montant *= CO2_COEF_APRES_07_2023
    return r2(max(montant, CO2_MINIMUM))


def calculer_paie(brut, statut="employe", taux_patronal=None, situation_familiale="isole",
                  nombre_enfants=0, nombre_enfants_handicapes=0, parent_isole=False,
                  beneficiaire_handicape=False, conjoint_handicape=False,
                  regime_travail=D("100"), taux_horaire=ZERO,
                  heures_sup=ZERO, majoration_heures_sup=50,
                  atn_autres=ZERO, voiture=None, date_paie=None,
                  double_pecule=False, reduction_groupe_cible=ZERO,
                  treizieme_mois=None, conges_jours_pris=ZERO, conges_jours_droit=None):
    fraction = (D(regime_travail or 100) / 100) if regime_travail else D("1")
    date_paie = date_paie or date.today()

    # ---- Brut
    brut_base = r2(brut or 0)
    taux_horaire = D(taux_horaire or 0)
    heures_sup = D(heures_sup or 0)
    maj = int(majoration_heures_sup or 50)
    base_heures_sup = r2(heures_sup * taux_horaire)
    montant_heures_sup = r2(base_heures_sup * (1 + D(maj) / 100))
    brut_total = r2(brut_base + montant_heures_sup)
    brut_majore = r2(brut_total * COEF_BRUT_MAJORE_OUVRIER) if statut == "ouvrier" else brut_total

    # ---- ONSS travailleur et bonus à l'emploi (proratisé)
    onss_brut = r2(brut_majore * TAUX_ONSS_TRAVAILLEUR / 100)
    bonus_a, bonus_b = (bonus_emploi(brut_total / fraction, statut, fraction)
                        if brut_total > 0 else (ZERO, ZERO))
    bonus = min(onss_brut, bonus_a + bonus_b)
    onss = r2(onss_brut - bonus)

    # ---- Avantages en nature
    atn_auto = ZERO
    co2 = ZERO
    if voiture:
        atn_auto = atn_voiture(voiture.get("valeur_catalogue"), voiture.get("co2"),
                               voiture.get("carburant"), voiture.get("date_immatriculation"), date_paie)
        atn_auto = max(ZERO, atn_auto - D(voiture.get("contribution_personnelle") or 0))
        co2 = cotisation_co2(voiture.get("co2"), voiture.get("carburant"),
                             voiture.get("commandee_apres_07_2023"))
    atn_total = r2(atn_auto + D(atn_autres or 0))

    # ---- Précompte
    imposable = r2(brut_total - onss + atn_total)
    reduction_hs = ZERO
    if base_heures_sup > 0:
        reduction_hs = r2(base_heures_sup * REDUCTION_PP_HEURES_SUP.get(maj, D("0.5775")))
    precompte = precompte_professionnel(
        imposable, situation_familiale, nombre_enfants, nombre_enfants_handicapes,
        parent_isole, beneficiaire_handicape, conjoint_handicape, bonus_a, bonus_b, reduction_hs,
    )

    # ---- Cotisation spéciale de sécurité sociale
    csss = cotisation_speciale_securite_sociale(brut_majore, situation_familiale)

    # ---- Net (les avantages en nature ne sont pas payés en argent)
    net = r2(brut_total - onss - precompte - csss)

    # ---- Double pécule de vacances (employés)
    pecule = None
    if double_pecule and statut == "employe" and brut_base > 0:
        pecule = double_pecule_employe(brut_base / fraction, fraction)
        net = r2(net + pecule["net"])

    # ---- Prime de fin d'année (13e mois) : treizieme_mois = {"reference": montant, "mois": n} ou None
    prime = None
    if treizieme_mois:
        prime = prime_fin_annee(treizieme_mois.get("reference"), treizieme_mois.get("mois", 12),
                                statut, brut_mensuel_normal=brut_base / fraction if fraction else brut_base)
        if prime:
            net = r2(net + prime["net"])

    # ---- Congés payés (informations)
    conges = conges_payes(statut, brut_base, conges_jours_pris, conges_jours_droit, fraction, brut_majore)

    # ---- Employeur
    taux_patronal = D(taux_patronal) if taux_patronal not in (None, "") else TAUX_PATRONAL_DEFAUT
    cotisations_patronales = r2(brut_majore * taux_patronal / 100)
    red_struct = min(cotisations_patronales, reduction_structurelle(brut_majore, fraction))
    red_gc = min(cotisations_patronales - red_struct, D(reduction_groupe_cible or 0))
    cotisations_nettes = r2(cotisations_patronales - red_struct - red_gc)

    if statut == "ouvrier":
        vacances = r2(brut_majore * COTISATION_VACANCES_OUVRIER / 100)
    else:
        # provision mensuelle du double pécule
        vacances = r2(brut_base * DOUBLE_PECULE_TAUX / 12)

    # Prime de fin d'année : cotisations patronales (+ cotisations vacances ouvriers) sur la prime
    prime_patronal = prime_vacances = ZERO
    if prime:
        prime_patronal = r2(prime["base_onss"] * taux_patronal / 100)
        if statut == "ouvrier":
            prime_vacances = r2(prime["base_onss"] * COTISATION_VACANCES_OUVRIER / 100)
        prime["cotisations_patronales"] = prime_patronal
        prime["cotisations_vacances"] = prime_vacances
        cotisations_nettes = r2(cotisations_nettes + prime_patronal)
        vacances = r2(vacances + prime_vacances)
        brut_total_employeur = r2(brut_total + prime["brut"])
    else:
        brut_total_employeur = brut_total

    brut_employeur = r2(brut_total_employeur + cotisations_nettes + vacances + co2)

    return {
        "fraction": fraction,
        "brut_base": brut_base,
        "montant_heures_sup": montant_heures_sup,
        "brut": brut_total,
        "brut_majore": brut_majore,
        "onss_brut": onss_brut,
        "bonus_emploi": r2(bonus),
        "onss": onss,
        "atn_voiture": atn_auto,
        "atn_total": atn_total,
        "imposable": imposable,
        "reduction_heures_sup": reduction_hs,
        "precompte": precompte,
        "taux_precompte": r2(precompte / imposable * 100) if imposable else ZERO,
        "csss": csss,
        "double_pecule": pecule,
        "treizieme_mois": prime,
        "conges": conges,
        "net": net,
        "taux_patronal": taux_patronal,
        "cotisations_patronales": cotisations_patronales,
        "reduction_structurelle": red_struct,
        "reduction_groupe_cible": r2(red_gc),
        "cotisations_patronales_nettes": cotisations_nettes,
        "vacances_employeur": vacances,
        "cotisation_co2": co2,
        "brut_employeur": brut_employeur,
    }


# ==================================================================
# COMPTABILISATION (PCMN – plan comptable minimum normalisé belge)
# ==================================================================
from django.utils.translation import gettext as _, gettext_noop

COMPTES = {
    "620200": gettext_noop("Rémunérations et avantages sociaux directs – employés"),
    "620300": gettext_noop("Rémunérations et avantages sociaux directs – ouvriers"),
    "621000": gettext_noop("Cotisations patronales d'assurances sociales"),
    "625000": gettext_noop("Provisions pour pécules de vacances (dotations)"),
    "453000": gettext_noop("Précomptes retenus"),
    "454000": gettext_noop("Office National de Sécurité Sociale"),
    "455000": gettext_noop("Rémunérations"),
    "456000": gettext_noop("Pécules de vacances"),
    "550000": gettext_noop("Banque – compte courant"),
}


def ecritures_paie(statut, brut, cotisations_patronales=ZERO, cotisation_co2=ZERO,
                   cotisations_vacances=ZERO, onss=ZERO, csss=ZERO, precompte=ZERO,
                   net_salaire=ZERO, double_pecule=None, date_paiement=None, treizieme_mois=None):
    """
    Écriture de salaire (journal des opérations diverses) + paiement.
    Retourne une liste de lignes {compte, libelle, debit, credit, type}.
    """
    L = []

    def ligne(compte, libelle, debit=ZERO, credit=ZERO, type_="salaire"):
        debit, credit = r2(debit or 0), r2(credit or 0)
        if debit or credit:
            L.append({"compte": compte, "intitule": _(COMPTES[compte]) if compte in COMPTES else "",
                      "libelle": libelle, "debit": debit, "credit": credit, "type": type_})

    compte_brut = "620300" if statut == "ouvrier" else "620200"

    # ---- Charges
    ligne(compte_brut, _("Salaire brut"), debit=brut)
    ligne("621000", _("Cotisations patronales ONSS (après réductions)"), debit=cotisations_patronales)
    ligne("621000", _("Cotisation de solidarité CO2 (voiture de société)"), debit=cotisation_co2)
    if statut == "ouvrier":
        ligne("621000", _("Cotisations vacances annuelles ouvriers"), debit=cotisations_vacances)
    else:
        ligne("625000", _("Provision double pécule de vacances"), debit=cotisations_vacances)

    # ---- Dettes
    ligne("454000", _("ONSS travailleur (13,07 % – bonus à l'emploi)"), credit=onss)
    ligne("454000", _("Cotisation spéciale de sécurité sociale"), credit=csss)
    ligne("454000", _("Cotisations patronales ONSS"), credit=cotisations_patronales)
    ligne("454000", _("Cotisation de solidarité CO2"), credit=cotisation_co2)
    if statut == "ouvrier":
        ligne("454000", _("Cotisations vacances annuelles ouvriers"), credit=cotisations_vacances)
    else:
        ligne("456000", _("Provision double pécule de vacances"), credit=cotisations_vacances)
    ligne("453000", _("Précompte professionnel"), credit=precompte)
    ligne("455000", _("Salaire net à payer"), credit=net_salaire)

    # ---- Double pécule payé ce mois (employés) : utilisation de la provision
    if double_pecule and double_pecule.get("brut"):
        ligne("456000", _("Double pécule de vacances brut"), debit=double_pecule["brut"], type_="pecule")
        ligne("454000", _("Retenue ONSS double pécule"), credit=double_pecule.get("onss"), type_="pecule")
        ligne("453000", _("Précompte double pécule"), credit=double_pecule.get("precompte"), type_="pecule")
        ligne("455000", _("Double pécule net à payer"), credit=double_pecule.get("net"), type_="pecule")

    # ---- Prime de fin d'année (13e mois) : charge de rémunération, retenues et net à payer
    if treizieme_mois and treizieme_mois.get("brut"):
        ligne(compte_brut, _("Prime de fin d'année (13e mois) brute"), debit=treizieme_mois["brut"], type_="prime")
        ligne("454000", _("Retenue ONSS prime de fin d'année"), credit=treizieme_mois.get("onss"), type_="prime")
        ligne("453000", _("Précompte prime de fin d'année"), credit=treizieme_mois.get("precompte"), type_="prime")
        ligne("455000", _("Prime de fin d'année nette à payer"), credit=treizieme_mois.get("net"), type_="prime")

    # ---- Paiement du net
    if date_paiement:
        total_net = (D(net_salaire or 0) + D((double_pecule or {}).get("net") or 0)
                     + D((treizieme_mois or {}).get("net") or 0))
        ligne("455000", _("Paiement du salaire net"), debit=total_net, type_="paiement")
        ligne("550000", _("Paiement du salaire net"), credit=total_net, type_="paiement")

    return L

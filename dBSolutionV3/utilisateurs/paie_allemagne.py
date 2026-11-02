"""
Calcul d'une paie mensuelle allemande (Lohnabrechnung) – paramètres 2026.

Brut (+ heures supplémentaires, + avantage voiture « 1 %-Regelung »)
-> cotisations sociales salarié (KV + Zusatzbeitrag, PV, RV, AV) plafonnées aux BBG
-> Lohnsteuer (tarif § 32a EStG 2026, Programmablaufplan 2026 : Vorsorgepauschale,
   Arbeitnehmer-Pauschbetrag, Steuerklassen I à VI)
-> Solidaritätszuschlag (Freigrenze 20 350 €) et Kirchensteuer (8 % BY/BW, 9 % ailleurs),
   calculés avec les Kinderfreibeträge
-> net.
Minijob (≤ 603 €) : RV salarié 3,6 %, forfaits employeur (Minijob-Zentrale), pas de Lohnsteuer (2 % forfaitaire).
Midijob / Übergangsbereich (603,01 – 2 000 €) : base salarié réduite (facteur F = 0,6619).
Gérant (Geschäftsführer) : considéré comme gérant associé majoritaire, non soumis aux assurances sociales.

Coût employeur = brut + parts patronales KV/PV/RV/AV + Umlagen U1/U2 + Insolvenzgeldumlage
+ assurance accidents (Berufsgenossenschaft, taux saisi).

⚠ Estimation : ne remplace pas un logiciel de paie certifié (ITSG / DATEV) ni le Steuerberater.
Sources des paramètres 2026 : § 32a EStG, PAP 2026 (BMF 12.11.2025), Rechengrößen SV 2026.
"""
from datetime import date
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP

from django.utils.translation import gettext as _, gettext_noop

D = Decimal
ZERO = D("0")
CENT = D("0.01")


def r2(x):
    return D(x).quantize(CENT, rounding=ROUND_HALF_UP)


def euro_bas(x):
    return D(x).quantize(D("1"), rounding=ROUND_DOWN)


# ==================================================================
# PARAMÈTRES 2026
# ==================================================================
ANNEE_PARAMETRES = 2026
HEURES_MOIS_TEMPS_PLEIN = D("173.33")        # 40 h × 52 / 12
MINDESTLOHN = D("13.90")                      # €/h au 01/01/2026

# ---- Sozialversicherung (BBG mensuelles)
BBG_KV_PV = D("5812.50")
BBG_RV_AV = D("8450.00")
KV_TAUX = D("14.6")                           # % (moitié / moitié)
KV_ZUSATZ_MOYEN = D("2.9")                    # % (moitié / moitié)
RV_TAUX = D("18.6")
AV_TAUX = D("2.6")
PV_TAUX = D("3.6")
PV_AN_SACHSEN, PV_AG_SACHSEN = D("2.3"), D("1.3")
PV_ZUSCHLAG_KINDERLOS = D("0.6")              # à charge du salarié (à partir de 23 ans)
PV_ABSCHLAG_PAR_ENFANT = D("0.25")            # du 2e au 5e enfant de moins de 25 ans
INSOLVENZGELD_TAUX = D("0.15")                # employeur
UMLAGEN_DEFAUT = D("2.00")                    # U1 + U2 + Berufsgenossenschaft (estimation, varie selon la caisse)

# ---- Minijob / Übergangsbereich
MINIJOB_GRENZE = D("603.00")
MIDIJOB_OBERGRENZE = D("2000.00")
MIDIJOB_FAKTOR_F = D("0.6619")
MINIJOB_RV_AN = D("3.6")                      # 18,6 % – 15 % employeur
MINIJOB_AG = {"kv": D("13"), "rv": D("15"), "pauschsteuer": D("2"),
              "u1": D("0.8"), "u2": D("0.22"), "insolvenz": D("0.15")}

# ---- Lohnsteuer (PAP 2026)
GFB = 12348
W1STKL5, W2STKL5, W3STKL5 = 14071, 34939, 222260
ARBEITNEHMER_PAUSCHBETRAG = D("1230")
SONDERAUSGABEN_PAUSCHBETRAG = D("36")
ENTLASTUNGSBETRAG_ALLEINERZIEHENDE = D("4260")
KINDERFREIBETRAG_VOLL = D("9756")             # par enfant, les deux parents (Steuerklassen II, III)
KINDERFREIBETRAG_HALB = D("4878")             # Steuerklassen I, IV
VSP_HOECHSTBETRAG_AV_KVPV = D("1900")
BBG_KV_PV_AN, BBG_RV_AV_AN = D("69750"), D("101400")
SOLZFREI = D("20350")
SOLI_TAUX, SOLI_MILDERUNG = D("5.5"), D("11.9")
KIRCHENSTEUER_TAUX = {"BY": D("8"), "BW": D("8")}
KIRCHENSTEUER_DEFAUT = D("9")

# ---- Voiture de société (1 %-Regelung, prix catalogue brut)
ATN_TAUX_VOITURE = D("1.0")
ATN_TAUX_ELECTRIQUE = D("0.25")               # véhicule 100 % électrique (prix catalogue ≤ 100 000 €)
ATN_PLAFOND_ELECTRIQUE = D("100000")
ATN_TAUX_ELECTRIQUE_AU_DELA = D("0.5")

BUNDESLAENDER = [
    ("BW", "Baden-Württemberg"), ("BY", "Bayern"), ("BE", "Berlin"), ("BB", "Brandenburg"),
    ("HB", "Bremen"), ("HH", "Hamburg"), ("HE", "Hessen"), ("MV", "Mecklenburg-Vorpommern"),
    ("NI", "Niedersachsen"), ("NW", "Nordrhein-Westfalen"), ("RP", "Rheinland-Pfalz"),
    ("SL", "Saarland"), ("SN", "Sachsen"), ("ST", "Sachsen-Anhalt"), ("SH", "Schleswig-Holstein"),
    ("TH", "Thüringen"),
]


# ==================================================================
# IMPÔT
# ==================================================================
def tarif_32a(zve):
    """Einkommensteuer annuelle § 32a EStG 2026 (euros entiers, arrondi vers le bas)."""
    x = int(euro_bas(max(zve, ZERO)))
    if x <= GFB:
        return ZERO
    if x <= 17799:
        y = D(x - GFB) / 10000
        return euro_bas((D("914.51") * y + 1400) * y)
    if x <= 69878:
        z = D(x - 17799) / 10000
        return euro_bas((D("173.10") * z + 2397) * z + D("1034.87"))
    if x <= 277825:
        return euro_bas(D("0.42") * x - D("11135.63"))
    return euro_bas(D("0.45") * x - D("19470.38"))


def _st_klasse_5_6(x):
    """§ 39b al. 2 phrase 7 EStG (Steuerklassen V et VI)."""
    def mst(v):
        v = D(v)
        st = 2 * (tarif_32a(v * D("1.25")) - tarif_32a(v * D("0.75")))
        return max(st, euro_bas(v * D("0.14")))

    x = D(int(euro_bas(x)))
    if x <= W1STKL5:
        return euro_bas(mst(x))
    st1 = mst(W1STKL5)
    if x <= W2STKL5:
        return euro_bas(min(mst(x), st1 + (x - W1STKL5) * D("0.42")))
    st2 = min(mst(W2STKL5), st1 + (W2STKL5 - W1STKL5) * D("0.42"))
    if x <= W3STKL5:
        return euro_bas(st2 + (x - W2STKL5) * D("0.42"))
    st3 = st2 + (W3STKL5 - W2STKL5) * D("0.42")
    return euro_bas(st3 + (x - W3STKL5) * D("0.45"))


def impot_classe(zve, steuerklasse):
    if steuerklasse == 3:
        return euro_bas(2 * tarif_32a(D(zve) / 2))
    if steuerklasse in (5, 6):
        return _st_klasse_5_6(zve)
    return tarif_32a(zve)


def taux_pv_salarie(nombre_enfants, kinderlos_zuschlag, sachsen):
    taux = PV_AN_SACHSEN if sachsen else PV_TAUX / 2
    enfants = int(nombre_enfants or 0)
    if enfants == 0 and kinderlos_zuschlag:
        taux += PV_ZUSCHLAG_KINDERLOS
    elif enfants >= 2:
        taux -= PV_ABSCHLAG_PAR_ENFANT * (min(enfants, 5) - 1)
    return taux


def vorsorgepauschale(brut_annuel, zusatzbeitrag, taux_pv_an, soumis_sv=True):
    """Vorsorgepauschale annuelle (PAP 2026 : RV + max(KV/PV, min(AV + KV/PV, 1 900 €)))."""
    if not soumis_sv:
        return ZERO
    base_rv = min(brut_annuel, BBG_RV_AV_AN)
    base_kv = min(brut_annuel, BBG_KV_PV_AN)
    vsp_rv = base_rv * RV_TAUX / 2 / 100
    vsp_av = base_rv * AV_TAUX / 2 / 100
    vsp_kvpv = base_kv * (D("7.0") + D(zusatzbeitrag) / 2 + taux_pv_an) / 100
    return vsp_rv + max(vsp_kvpv, min(vsp_av + vsp_kvpv, VSP_HOECHSTBETRAG_AV_KVPV))


def lohnsteuer_annuelle(brut_annuel, steuerklasse, kinderfreibetraege, zusatzbeitrag, taux_pv_an,
                        soumis_sv=True, nombre_enfants=0):
    """Retourne (Lohnsteuer annuelle, base Soli/KiSt annuelle avec Kinderfreibeträge)."""
    sk = int(steuerklasse or 1)
    deductions = SONDERAUSGABEN_PAUSCHBETRAG
    if sk != 6:
        deductions += ARBEITNEHMER_PAUSCHBETRAG
    if sk == 2:
        deductions += ENTLASTUNGSBETRAG_ALLEINERZIEHENDE + D("240") * max(int(nombre_enfants or 1) - 1, 0)
    zve = max(D(brut_annuel) - deductions - vorsorgepauschale(D(brut_annuel), zusatzbeitrag, taux_pv_an, soumis_sv), ZERO)
    lst = impot_classe(zve, sk)

    zkf = D(kinderfreibetraege or 0)
    if zkf > 0 and sk in (1, 2, 3, 4):
        kfb = zkf * (KINDERFREIBETRAG_VOLL if sk in (2, 3) else KINDERFREIBETRAG_HALB)
        jbmg = impot_classe(max(zve - kfb, ZERO), sk)
    else:
        jbmg = lst
    return lst, jbmg


def soli_annuel(jbmg, steuerklasse):
    freigrenze = SOLZFREI * (2 if int(steuerklasse or 1) == 3 else 1)
    if jbmg <= freigrenze:
        return ZERO
    return min(jbmg * SOLI_TAUX / 100, (jbmg - freigrenze) * SOLI_MILDERUNG / 100)


def atn_voiture(voiture):
    """Avantage voiture mensuel selon la 1 %-Regelung (sans le supplément trajet domicile-travail)."""
    if not voiture or not voiture.get("valeur_catalogue"):
        return ZERO
    prix = D(voiture["valeur_catalogue"])
    prix_arrondi = (prix / 100).quantize(D("1"), rounding=ROUND_DOWN) * 100   # arrondi à la centaine inférieure
    if voiture.get("carburant") == "electrique":
        taux = ATN_TAUX_ELECTRIQUE if prix <= ATN_PLAFOND_ELECTRIQUE else ATN_TAUX_ELECTRIQUE_AU_DELA
    else:
        taux = ATN_TAUX_VOITURE
    atn = r2(prix_arrondi * taux / 100)
    return max(ZERO, atn - D(voiture.get("contribution_personnelle") or 0))


# ==================================================================
# CALCUL DE LA PAIE
# ==================================================================
def calculer_paie(brut, statut="employe", steuerklasse=1, kirchensteuer=False, bundesland="",
                  kinderfreibetraege=0, nombre_enfants=0, kinderlos_zuschlag=True,
                  zusatzbeitrag=None, taux_umlagen=None, regime_travail=D("100"), taux_horaire=ZERO,
                  heures_sup=ZERO, majoration_heures_sup=25, atn_autres=ZERO, voiture=None,
                  date_paie=None, conges_jours_pris=ZERO, conges_jours_droit=None):
    fraction = (D(regime_travail or 100) / 100) if regime_travail else D("1")
    zusatz = D(KV_ZUSATZ_MOYEN if zusatzbeitrag in (None, "") else zusatzbeitrag)
    umlagen = D(UMLAGEN_DEFAUT if taux_umlagen in (None, "") else taux_umlagen)
    sachsen = bundesland == "SN"
    sk = int(steuerklasse or 1)

    # ---- Brut
    brut_base = r2(brut or 0)
    taux_horaire = D(taux_horaire or 0)
    heures_sup = D(heures_sup or 0)
    maj = int(majoration_heures_sup or 0)
    montant_hs = r2(heures_sup * taux_horaire * (1 + D(maj) / 100))
    brut_total = r2(brut_base + montant_hs)

    atn_auto = atn_voiture(voiture)
    atn_total = r2(atn_auto + D(atn_autres or 0))
    base = r2(brut_total + atn_total)            # salaire soumis (cotisations et impôt)

    dirigeant = statut == "dirigeant"
    minijob = not dirigeant and ZERO < base <= MINIJOB_GRENZE
    midijob = not dirigeant and MINIJOB_GRENZE < base <= MIDIJOB_OBERGRENZE

    taux_pv_an = taux_pv_salarie(nombre_enfants, kinderlos_zuschlag, sachsen)
    pv_ag = PV_AG_SACHSEN if sachsen else PV_TAUX / 2
    taux_an = {"kv": KV_TAUX / 2 + zusatz / 2, "pv": taux_pv_an, "rv": RV_TAUX / 2, "av": AV_TAUX / 2}
    taux_ag = {"kv": KV_TAUX / 2 + zusatz / 2, "pv": pv_ag, "rv": RV_TAUX / 2, "av": AV_TAUX / 2}
    plafonds = {"kv": BBG_KV_PV, "pv": BBG_KV_PV, "rv": BBG_RV_AV, "av": BBG_RV_AV}
    noms = {"kv": _("Assurance maladie (KV, y c. Zusatzbeitrag)"), "pv": _("Assurance dépendance (PV)"),
            "rv": _("Assurance pension (RV)"), "av": _("Assurance chômage (AV)")}

    sv = []          # [{branche, libelle, base, taux_an, an, taux_ag, ag}]
    autres_ag = []   # [{libelle, base, taux, montant}]
    lohnsteuer = soli = kist = pauschsteuer = ZERO

    if dirigeant:
        pass  # Geschäftsführer associé majoritaire : pas d'assurances sociales
    elif minijob:
        an = r2(base * MINIJOB_RV_AN / 100)
        sv.append({"branche": "rv", "libelle": _("Minijob – assurance pension (RV)"), "base": base,
                   "taux_an": MINIJOB_RV_AN, "an": an, "taux_ag": MINIJOB_AG["rv"], "ag": r2(base * MINIJOB_AG["rv"] / 100)})
        sv.append({"branche": "kv", "libelle": _("Minijob – assurance maladie forfaitaire (KV)"), "base": base,
                   "taux_an": ZERO, "an": ZERO, "taux_ag": MINIJOB_AG["kv"], "ag": r2(base * MINIJOB_AG["kv"] / 100)})
        pauschsteuer = r2(base * MINIJOB_AG["pauschsteuer"] / 100)
        for cle, libelle in (("u1", _("Umlage U1 (maladie)")), ("u2", _("Umlage U2 (maternité)")),
                             ("insolvenz", _("Insolvenzgeldumlage"))):
            autres_ag.append({"libelle": libelle, "base": base, "taux": MINIJOB_AG[cle],
                              "montant": r2(base * MINIJOB_AG[cle] / 100)})
        autres_ag.append({"libelle": _("Impôt forfaitaire 2 % (Pauschsteuer)"), "base": base,
                          "taux": MINIJOB_AG["pauschsteuer"], "montant": pauschsteuer})
    else:
        if midijob:
            g, o, f = MINIJOB_GRENZE, MIDIJOB_OBERGRENZE, MIDIJOB_FAKTOR_F
            base_totale = r2(f * g + (o / (o - g) - g / (o - g) * f) * (base - g))
            base_an = r2(o / (o - g) * (base - g))
        pv_an_general = PV_AN_SACHSEN if sachsen else PV_TAUX / 2
        for b in ("kv", "pv", "rv", "av"):
            if midijob:
                # Gesamtbeitrag sur la base totale réduite ; part salarié sur sa base propre ;
                # supplément / abattement PV enfants : uniquement à charge du salarié
                general_an = pv_an_general if b == "pv" else taux_an[b]
                total = r2(base_totale * (general_an + taux_ag[b]) / 100)
                an_general = r2(base_an * general_an / 100)
                ag = max(total - an_general, ZERO)
                an = an_general + r2(base_an * (taux_an[b] - general_an) / 100)
                assiette = base_an
            else:
                assiette = min(base, plafonds[b])
                an = r2(assiette * taux_an[b] / 100)
                ag = r2(assiette * taux_ag[b] / 100)
            sv.append({"branche": b, "libelle": noms[b], "base": assiette, "taux_an": taux_an[b], "an": an,
                       "taux_ag": taux_ag[b], "ag": ag})
        assiette_insolvenz = min(base, BBG_RV_AV)
        autres_ag.append({"libelle": _("Insolvenzgeldumlage"), "base": assiette_insolvenz,
                          "taux": INSOLVENZGELD_TAUX, "montant": r2(assiette_insolvenz * INSOLVENZGELD_TAUX / 100)})

    if not minijob and base > 0:
        # U1 / U2 (caisse maladie) et Berufsgenossenschaft : taux global saisi (aussi pour le gérant : BG)
        autres_ag.append({"libelle": _("Umlagen U1 / U2 et assurance accidents (Berufsgenossenschaft)"),
                          "base": base, "taux": umlagen, "montant": r2(base * umlagen / 100)})

    sv_an = r2(sum((l["an"] for l in sv), ZERO))
    sv_ag = r2(sum((l["ag"] for l in sv), ZERO))
    autres = r2(sum((l["montant"] for l in autres_ag), ZERO))

    # ---- Lohnsteuer / Soli / Kirchensteuer (pas pour le Minijob : impôt forfaitaire employeur)
    if not minijob and base > 0:
        annuel = base * 12
        lst_an, jbmg = lohnsteuer_annuelle(annuel, sk, kinderfreibetraege, zusatz, taux_pv_an,
                                           soumis_sv=not dirigeant, nombre_enfants=nombre_enfants)
        lohnsteuer = r2(lst_an / 12)
        soli = r2(soli_annuel(jbmg, sk) / 12)
        if kirchensteuer:
            kist = r2(jbmg * KIRCHENSTEUER_TAUX.get(bundesland, KIRCHENSTEUER_DEFAUT) / 100 / 12)
    impots = r2(lohnsteuer + soli + kist)

    # ---- Net (les avantages en nature ne sont pas payés en argent)
    net = r2(brut_total - sv_an - impots)

    # ---- Congés (Bundesurlaubsgesetz : 20 jours minimum en semaine de 5 jours, souvent 30 par contrat)
    droit = D(conges_jours_droit) if conges_jours_droit not in (None, "") else (D("20") * fraction).quantize(D("0.1"))
    conges = {"droit": droit, "jours_pris": D(conges_jours_pris or 0), "simple_pecule": ZERO,
              "pecule_ouvrier_annuel": ZERO, "salaire_journalier": ZERO}

    cotisations_patronales = r2(sv_ag + autres)
    brut_employeur = r2(brut_total + cotisations_patronales)
    taux_patronal = r2(cotisations_patronales / base * 100) if base else ZERO

    return {
        "pays": "DE",
        "fraction": fraction,
        "brut_base": brut_base,
        "montant_heures_sup": montant_hs,
        "brut": brut_total,
        "brut_majore": base,
        "onss_brut": sv_an,
        "bonus_emploi": ZERO,
        "onss": sv_an,
        "atn_voiture": atn_auto,
        "atn_total": atn_total,
        "imposable": base,
        "reduction_heures_sup": ZERO,
        "precompte": lohnsteuer,
        "taux_precompte": r2(lohnsteuer / base * 100) if base else ZERO,
        "soli": soli,
        "kirchensteuer": kist,
        "impots_total": impots,
        "csss": ZERO,
        "double_pecule": None,
        "treizieme_mois": None,
        "conges": conges,
        "net": net,
        "taux_patronal": taux_patronal,
        "cotisations_patronales": cotisations_patronales,
        "reduction_structurelle": ZERO,
        "reduction_groupe_cible": ZERO,
        "cotisations_patronales_nettes": cotisations_patronales,
        "vacances_employeur": ZERO,
        "cotisation_co2": ZERO,
        "brut_employeur": brut_employeur,
        "steuerklasse": sk,
        "minijob": minijob,
        "midijob": midijob,
        "dirigeant": dirigeant,
        "sv": sv,
        "autres_patronales": autres_ag,
        "sv_an": sv_an,
        "sv_ag": sv_ag,
        "pauschsteuer": pauschsteuer,
    }


# ==================================================================
# FICHE DE PAIE
# ==================================================================
def lignes_fiche(r, ligne, salaire_brut_heure=None, heures=None, heures_sup=None, majoration=0):
    lignes = [ligne(_("Salaire de base (Grundgehalt)"), base=heures or None, taux=salaire_brut_heure,
                    unite_taux="€/h", montant=r["brut_base"], signe="+")]
    if r["montant_heures_sup"]:
        lignes.append(ligne(_("Heures supplémentaires (majoration %(m)s %%)") % {"m": majoration},
                            base=heures_sup, montant=r["montant_heures_sup"], signe="+"))
    lignes.append(ligne(_("Rémunération brute (Bruttolohn)"), montant=r["brut"], style="total"))
    if r["atn_voiture"]:
        lignes.append(ligne(_("Avantage voiture de société (1 %%-Regelung)"), montant=r["atn_voiture"], signe="+"))
    if r["atn_total"] - r["atn_voiture"]:
        lignes.append(ligne(_("Autres avantages en nature (Sachbezüge)"), montant=r["atn_total"] - r["atn_voiture"], signe="+"))
    if r["atn_total"]:
        lignes.append(ligne(_("Salaire soumis (Steuer- / SV-Brutto)"), montant=r["brut_majore"], style="info"))
    if r["minijob"]:
        lignes.append(ligne(_("Minijob (≤ %(g)s €) : impôt forfaitaire payé par l'employeur") % {"g": MINIJOB_GRENZE},
                            style="info"))
    if r["midijob"]:
        lignes.append(ligne(_("Übergangsbereich (Midijob) : cotisations salarié réduites"), style="info"))
    for l in r["sv"]:
        if l["an"]:
            lignes.append(ligne(l["libelle"], base=l["base"], taux=l["taux_an"], montant=l["an"], signe="-"))
    if r["sv_an"]:
        lignes.append(ligne(_("Total cotisations sociales salarié"), montant=r["sv_an"], signe="-", style="sous-total"))
    if not r["minijob"]:
        lignes.append(ligne(_("Lohnsteuer (classe d'impôt %(k)s)") % {"k": r["steuerklasse"]}, base=r["imposable"],
                            taux=r["taux_precompte"], montant=r["precompte"], signe="-"))
        if r["soli"]:
            lignes.append(ligne(_("Solidaritätszuschlag"), montant=r["soli"], signe="-"))
        if r["kirchensteuer"]:
            lignes.append(ligne(_("Kirchensteuer"), montant=r["kirchensteuer"], signe="-"))
    if r["atn_total"]:
        lignes.append(ligne(_("Avantages en nature (non payés en argent)"), montant=r["atn_total"], signe="-"))
    lignes.append(ligne(_("Net à payer (Auszahlungsbetrag)"), montant=r["net"], style="total"))
    conges = r["conges"]
    if conges["jours_pris"] or conges["droit"]:
        lignes.append(ligne(_("Congés : droit annuel"), montant=conges["droit"], style="info", unite="j"))
        lignes.append(ligne(_("Congés : jours pris ce mois"), montant=conges["jours_pris"], style="info", unite="j"))
    return lignes


# ==================================================================
# COMPTABILISATION (comptes internes PCMN, convertis en SKR03 à l'affichage)
# ==================================================================
COMPTES = {
    "620200": gettext_noop("Salaires (Gehälter)"),
    "620300": gettext_noop("Salaires (Löhne)"),
    "618000": gettext_noop("Rémunération du gérant (Geschäftsführergehälter)"),
    "621000": gettext_noop("Charges sociales légales (gesetzliche soziale Aufwendungen)"),
    "453000": gettext_noop("Dettes Lohnsteuer / Soli / Kirchensteuer (Finanzamt)"),
    "454000": gettext_noop("Dettes de sécurité sociale (Krankenkassen)"),
    "455000": gettext_noop("Salaires nets à payer"),
    "550000": gettext_noop("Banque – compte courant"),
}


def ecritures_paie(statut, brut, cotisations_patronales=ZERO, sv_an=ZERO, impots=ZERO, pauschsteuer=ZERO,
                   net_salaire=ZERO, date_paiement=None):
    L = []

    def ligne(compte, libelle, debit=ZERO, credit=ZERO, type_="salaire"):
        debit, credit = r2(debit or 0), r2(credit or 0)
        if debit or credit:
            L.append({"compte": compte, "intitule": _(COMPTES[compte]) if compte in COMPTES else "",
                      "libelle": libelle, "debit": debit, "credit": credit, "type": type_})

    compte_brut = {"ouvrier": "620300", "dirigeant": "618000"}.get(statut, "620200")
    ligne(compte_brut, _("Salaire brut"), debit=brut)
    ligne("621000", _("Parts patronales SV, Umlagen et assurance accidents"), debit=cotisations_patronales - pauschsteuer)
    ligne("621000", _("Impôt forfaitaire Minijob (2 %)"), debit=pauschsteuer)
    ligne("454000", _("Cotisations sociales salarié"), credit=sv_an)
    ligne("454000", _("Cotisations patronales (Krankenkasse / Minijob-Zentrale)"), credit=cotisations_patronales - pauschsteuer)
    ligne("453000", _("Lohnsteuer, Solidaritätszuschlag et Kirchensteuer"), credit=impots)
    ligne("453000", _("Impôt forfaitaire Minijob (2 %)"), credit=pauschsteuer)
    ligne("455000", _("Salaire net à payer"), credit=net_salaire)
    if date_paiement and net_salaire:
        ligne("455000", _("Paiement du salaire net"), debit=net_salaire, type_="paiement")
        ligne("550000", _("Paiement du salaire net"), credit=net_salaire, type_="paiement")
    return L

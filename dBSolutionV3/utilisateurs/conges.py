"""
Congés payés, pécules de vacances et prime de fin d'année (13e mois) d'un travailleur pour une année,
calculés à partir de ses paies mensuelles (PaieUtilisateur).

Règles belges (rappel) :
- droit : 20 jours pour un temps plein (5 j / semaine) ayant travaillé toute l'année précédente (exercice),
  au prorata du régime de travail ; à prendre avant le 31 décembre ;
- employé : simple pécule = salaire maintenu pendant les jours pris ; double pécule = 92 % du brut mensuel
  (ONSS 13,07 % sur 85 %), payé en général en mai / juin ;
- ouvrier : pécule payé par la caisse de vacances = 15,38 % du brut à 108 % de l'exercice précédent
  (8 % simple + 7,38 % double) ; l'employeur cotise 15,84 % du brut à 108 % ;
- 13e mois : CP 200 = 1 salaire mensuel brut au prorata des mois prestés (année civile), payé en décembre ;
  CP 112 = taux horaire × 38 h × 52 / 12, période du 1er décembre au 30 novembre, payé au plus tard le 20 décembre.
"""
from decimal import Decimal as D

from .paie_belgique import (
    COEF_BRUT_MAJORE_OUVRIER, CONGES_JOURS_TEMPS_PLEIN, HEURES_MOIS_TEMPS_PLEIN, PECULE_OUVRIER_TAUX, SALAIRE_JOURNALIER_COEF,
    TAUX_ONSS_TRAVAILLEUR, double_pecule_employe, prime_fin_annee, r2, taux_precompte_exceptionnel,
)

ZERO = D("0")


def _d(v):
    return D(v or 0)


def _droit_par_defaut(paie):
    regime = _d(getattr(paie, "regime_travail", None) or 100)
    return r2(CONGES_JOURS_TEMPS_PLEIN * regime / 100)


def _brut_majore(p):
    if p.salaire_brut_majore:
        return _d(p.salaire_brut_majore)
    brut = _d(p.salaire_brut_mensuel)
    return r2(brut * COEF_BRUT_MAJORE_OUVRIER) if p.statut_travailleur == "ouvrier" else brut


def _reference_treizieme(p):
    """Montant de référence du 13e mois (même règle que PaieUtilisateur.parametres_treizieme_mois)."""
    if p.treizieme_mois_reference:
        return _d(p.treizieme_mois_reference)
    fraction = _d(p.regime_travail or 100) / 100
    if p.statut_travailleur == "ouvrier" and p.salaire_brut_heure:
        return r2(_d(p.salaire_brut_heure) * HEURES_MOIS_TEMPS_PLEIN * fraction)
    return _d(p.salaire_brut_mensuel)


def situation_conges(paies_travailleur, annee, aujourdhui, paiements=None):
    """
    paies_travailleur : QuerySet des paies du travailleur (toutes années).
    paiements : paiements de congés hors paie (compta.PaiementConges) de l'année, ou None.
    Retourne un dict avec les lignes mensuelles, les totaux, les pécules et le 13e mois.
    """
    paies_annee = {p.mois: p for p in paies_travailleur.filter(annee=annee)}
    paies_prec = list(paies_travailleur.filter(annee=annee - 1))
    derniere = (paies_travailleur.filter(annee__lte=annee).order_by("-annee", "-mois").first()
                or paies_travailleur.order_by("annee", "mois").first())

    statut = getattr(derniere, "statut_travailleur", "employe") if derniere else "employe"
    regime = _d(getattr(derniere, "regime_travail", None) or 100) if derniere else D("100")
    fraction = regime / 100 if regime else D("1")

    # ---- Droit annuel : dernière valeur encodée dans l'année, sinon 20 j × régime
    droit = None
    for m in sorted(paies_annee, reverse=True):
        if paies_annee[m].conges_jours_droit is not None:
            droit = _d(paies_annee[m].conges_jours_droit)
            break
    droit_source = "encode"
    if droit is None:
        droit = _droit_par_defaut(derniere) if derniere else CONGES_JOURS_TEMPS_PLEIN
        droit_source = "defaut"

    # ---- Lignes mensuelles
    lignes, cumul = [], ZERO
    total_simple = ZERO
    for mois in range(1, 13):
        p = paies_annee.get(mois)
        pris = _d(p.conges_jours_pris) if p else ZERO
        cumul += pris
        simple = _d(p.conges_simple_pecule) if p else ZERO
        total_simple += simple
        lignes.append({
            "mois": mois,
            "paie": p,
            "pris": pris,
            "cumul": cumul,
            "solde": droit - cumul,
            "simple_pecule": simple,
            "double_pecule": p.double_pecule_brut if p and p.double_pecule_ce_mois else None,
            "treizieme": p.treizieme_mois_brut if p and p.treizieme_mois_ce_mois else None,
            "passe": (annee, mois) < (aujourdhui.year, aujourdhui.month),
            "courant": (annee, mois) == (aujourdhui.year, aujourdhui.month),
        })
    paiements = list(paiements or [])
    jours_hors_paie = sum((_d(pc.jours) for pc in paiements if pc.type == "SIMPLE_PECULE"), ZERO)
    jours_sortie = sum((_d(pc.jours) for pc in paiements if pc.type == "PECULE_SORTIE"), ZERO)
    pris = cumul + jours_hors_paie
    restant = droit - pris - jours_sortie

    # Mois restants dans l'année (mois courant compris) pour planifier les jours à prendre
    if annee < aujourdhui.year:
        mois_restants = 0
    elif annee > aujourdhui.year:
        mois_restants = 12
    else:
        mois_restants = 12 - aujourdhui.month + 1

    # ---- Salaire de référence (dernière paie)
    brut_mensuel = _d(derniere.salaire_brut_mensuel) if derniere else ZERO
    journalier = r2(brut_mensuel * SALAIRE_JOURNALIER_COEF)

    # ---- Pécules de vacances
    pecule = {"statut": statut}
    if statut == "ouvrier":
        base_prec = sum((_brut_majore(p) for p in paies_prec), ZERO)
        if base_prec:
            pecule["base"] = base_prec
            pecule["base_source"] = "annee_precedente"
            pecule["nb_paies_base"] = len(paies_prec)
        else:
            pecule["base"] = r2(brut_mensuel * COEF_BRUT_MAJORE_OUVRIER * 12)
            pecule["base_source"] = "estimation"
        total = r2(pecule["base"] * PECULE_OUVRIER_TAUX / 100)
        pecule["total"] = total
        pecule["simple"] = r2(pecule["base"] * D("8") / 100)
        pecule["double"] = r2(total - pecule["simple"])
        pecule["valeur_jour"] = r2(pecule["simple"] / droit) if droit else ZERO
    else:
        payes = [p for p in paies_annee.values() if p.double_pecule_ce_mois and p.double_pecule_brut]
        hors_paie = [pc for pc in paiements if pc.type == "DOUBLE_PECULE"]
        if hors_paie and not payes:
            pecule["double_paye"] = True
            pecule["double_mois"] = [pc.date.month for pc in hors_paie]
            pecule["double_hors_paie"] = True
            pecule["double_brut"] = sum((_d(pc.brut) for pc in hors_paie), ZERO)
            pecule["double_onss"] = sum((_d(pc.onss) for pc in hors_paie), ZERO)
            pecule["double_precompte"] = sum((_d(pc.precompte) for pc in hors_paie), ZERO)
            pecule["double_net"] = sum((_d(pc.net) for pc in hors_paie), ZERO)
        elif payes:
            pecule["double_paye"] = True
            pecule["double_mois"] = [p.mois for p in payes]
            pecule["double_brut"] = sum((_d(p.double_pecule_brut) for p in payes), ZERO)
            pecule["double_onss"] = sum((_d(p.double_pecule_onss) for p in payes), ZERO)
            pecule["double_precompte"] = sum((_d(p.double_pecule_precompte) for p in payes), ZERO)
            pecule["double_net"] = sum((_d(p.double_pecule_net) for p in payes), ZERO)
        elif brut_mensuel:
            est = double_pecule_employe(brut_mensuel / fraction, fraction)
            pecule["double_paye"] = False
            pecule["double_brut"], pecule["double_onss"] = est["brut"], est["onss"]
            pecule["double_precompte"], pecule["double_net"] = est["precompte"], est["net"]
        pecule["simple_cumule"] = total_simple + sum(
            (_d(pc.brut) for pc in paiements if pc.type == "SIMPLE_PECULE"), ZERO)
        pecule["valeur_jour"] = journalier
        pecule["simple_restant"] = r2(journalier * max(restant, ZERO))

    # ---- Prime de fin d'année (13e mois)
    treizieme = {"cp": getattr(derniere, "commission_paritaire", "") if derniere else ""}
    payes = [p for p in paies_annee.values() if p.treizieme_mois_ce_mois and p.treizieme_mois_brut]
    if payes:
        p = payes[-1]
        treizieme.update({
            "paye": True, "mois": p.mois, "mois_prestes": p.treizieme_mois_mois_prestes,
            "brut": _d(p.treizieme_mois_brut), "onss": _d(p.treizieme_mois_onss),
            "precompte": _d(p.treizieme_mois_precompte), "net": _d(p.treizieme_mois_net),
        })
    elif derniere:
        # Période de référence : 01/12 (N-1) → 30/11 (N) en CP 112 ; année civile sinon
        if treizieme["cp"] == "CP112":
            periode = [(annee - 1, 12)] + [(annee, m) for m in range(1, 12)]
        else:
            periode = [(annee, m) for m in range(1, 13)]
        avec_paie = set(paies_travailleur.filter(annee__in={a for a, _m in periode})
                        .values_list("annee", "mois"))
        prestes = sum(1 for c in periode if c in avec_paie)
        a_venir = sum(1 for c in periode if c > (aujourdhui.year, aujourdhui.month) and c not in avec_paie)
        mois_prevus = min(12, prestes + a_venir)
        reference = _reference_treizieme(derniere)
        est = prime_fin_annee(reference, mois_prevus, statut, brut_mensuel) if reference else None
        treizieme.update({
            "paye": False, "mois_prestes": prestes, "mois_prevus": mois_prevus,
            "reference": reference, "estimation": est,
        })

    return {
        "annee": annee,
        "statut": statut,
        "regime": regime,
        "droit": droit,
        "droit_source": droit_source,
        "pris": pris,
        "restant": restant,
        "depasse": restant < 0,
        "pourcentage": int(min(pris * 100 / droit, 100)) if droit else 0,
        "mois_restants": mois_restants,
        "a_planifier_par_mois": r2(max(restant, ZERO) / mois_restants) if mois_restants else ZERO,
        "lignes": lignes,
        "paiements": paiements,
        "jours_hors_paie": jours_hors_paie,
        "jours_sortie": jours_sortie,
        "nb_paies": len(paies_annee),
        "derniere": derniere,
        "brut_mensuel": brut_mensuel,
        "salaire_journalier": journalier,
        "pecule": pecule,
        "treizieme": treizieme,
    }


# ======================================================================
# PROPOSITION DE MONTANTS POUR UN PAIEMENT DE CONGÉS HORS PAIE
# ======================================================================
POURCENT_SORTIE_EMPLOYE = D("15.34")    # 7,67 % simple + 7,67 % double du brut de l'année
PART_SIMPLE_SORTIE = D("7.67")


def _taux_effectif_precompte(p):
    """Taux de précompte réellement appliqué sur la dernière paie (précompte / imposable)."""
    imposable = _d(p.salaire_imposable)
    if imposable > 0 and p.montant_precompte:
        return _d(p.montant_precompte) / imposable
    return taux_precompte_exceptionnel(p.salaire_brut_mensuel)


def _taux_patronal(p):
    if p.taux_charges_patronales:
        return _d(p.taux_charges_patronales) / 100
    base = _d(p.salaire_brut_majore or p.salaire_brut_mensuel)
    return (_d(p.cotisations_patronales) / base) if base and p.cotisations_patronales else D("0.25")


def proposer_paiement(type_paiement, paies_travailleur, annee, aujourdhui, jours=None, paiements=None):
    """
    Montants proposés (modifiables) : {"brut", "onss", "precompte", "cotisations_patronales", "jours",
    "statut", "explication", "avertissement"}.
    """
    s = situation_conges(paies_travailleur, annee, aujourdhui, paiements)
    p = s["derniere"]
    res = {"brut": ZERO, "onss": ZERO, "precompte": ZERO, "cotisations_patronales": ZERO,
           "jours": ZERO, "statut": s["statut"], "explication": "", "avertissement": ""}
    if p is None:
        res["avertissement"] = "aucune_paie"
        return res
    brut_mensuel = _d(p.salaire_brut_mensuel)
    fraction = s["regime"] / 100 if s["regime"] else D("1")
    ouvrier = s["statut"] == "ouvrier"

    if type_paiement == "DOUBLE_PECULE":
        if ouvrier:
            res["avertissement"] = "ouvrier_caisse"
            return res
        e = double_pecule_employe(brut_mensuel / fraction, fraction)
        res.update(brut=e["brut"], onss=e["onss"], precompte=e["precompte"], explication="double")

    elif type_paiement == "SIMPLE_PECULE":
        if ouvrier:
            res["avertissement"] = "ouvrier_caisse"
        nb = _d(jours) if jours not in (None, "") else max(s["restant"], ZERO)
        brut = r2(s["salaire_journalier"] * nb)
        onss = r2(brut * TAUX_ONSS_TRAVAILLEUR / 100)
        res.update(jours=nb, brut=brut, onss=onss,
                   precompte=r2((brut - onss) * _taux_effectif_precompte(p)),
                   cotisations_patronales=r2(brut * _taux_patronal(p)), explication="simple")

    elif type_paiement == "PECULE_SORTIE":
        if ouvrier:
            res["avertissement"] = "ouvrier_caisse"
            return res
        base = sum((_d(x.salaire_brut_mensuel) for x in paies_travailleur.filter(annee=annee)), ZERO)
        brut = r2(base * POURCENT_SORTIE_EMPLOYE / 100)
        simple = r2(base * PART_SIMPLE_SORTIE / 100)
        double = brut - simple
        onss = r2((simple + double * D("85") / D("92")) * TAUX_ONSS_TRAVAILLEUR / 100)
        res.update(jours=max(s["restant"], ZERO), brut=brut, onss=onss,
                   precompte=r2((brut - onss) * taux_precompte_exceptionnel(brut_mensuel)),
                   cotisations_patronales=r2(simple * _taux_patronal(p)), explication="sortie", base=base)
    return res

"""
Coût de revient de la main-d'œuvre, calculé à partir des paies (rapport de calcul du salaire).

    taux de revient horaire = salaire total employeur / heures prestées

- salaire total employeur : PaieUtilisateur.salaire_total
  (brut + cotisations patronales nettes + provision vacances + CO2 + congés payés) ;
- heures prestées : heures du mois + heures supplémentaires. À défaut (salaire mensuel sans
  heures encodées) : horaire de référence 38 h/sem. (164,67 h/mois) × régime de travail.

Rôles concernés : chef mécanicien, mécaniciens, apprentis, magasinier.
"""
from collections import OrderedDict
from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Q, Sum
from django.utils.translation import gettext_lazy as _

ZERO = Decimal("0.00")
HEURES_REFERENCE_MOIS = Decimal("164.67")  # 38 h/sem × 52 / 12

ROLES_ATELIER = OrderedDict([
    ("chef_mecanicien", _("Chef mécanicien")),
    ("mecanicien", _("Mécaniciens")),
    ("apprentis", _("Apprentis")),
    ("magasinier", _("Magasinier")),
])


def r2(x):
    return Decimal(x or 0).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def cout_paie(paie):
    """Coût total employeur d'une paie."""
    return Decimal(paie.salaire_total or paie.salaire_brut_mensuel_employeur or 0)


def heures_paie(paie):
    """(heures, estimé?) d'une paie."""
    heures = Decimal(paie.nombre_heures_preste or 0) + Decimal(paie.heures_supplementaires or 0)
    if heures > 0:
        return heures, False
    regime = Decimal(paie.regime_travail or 100) / Decimal("100")
    return r2(HEURES_REFERENCE_MOIS * regime), True


def cout_horaire_paie(paie):
    heures, _estime = heures_paie(paie)
    return r2(cout_paie(paie) / heures) if heures else ZERO


def cout_horaire_utilisateur(utilisateur, annee=None, mois=None):
    """
    Taux de revient horaire d'un utilisateur : paie du mois demandé,
    sinon dernière paie antérieure, sinon dernière paie connue. None si aucune paie.
    """
    from .models import PaieUtilisateur

    if not utilisateur:
        return None
    paies = PaieUtilisateur.objects.filter(utilisateur=utilisateur).order_by("-annee", "-mois")
    paie = None
    if annee and mois:
        paie = (paies.filter(annee=annee, mois=mois).first()
                or paies.filter(Q(annee__lt=annee) | Q(annee=annee, mois__lt=mois)).first())
    paie = paie or paies.first()
    return cout_horaire_paie(paie) if paie else None


def _periode_mois(annee, mois=None, trimestre=None):
    if mois:
        return [mois]
    if trimestre:
        return [3 * (trimestre - 1) + i for i in (1, 2, 3)]
    return list(range(1, 13))


def rapport_cout_main_oeuvre(societe, annee, mois=None, trimestre=None):
    """
    Rapport par utilisateur et par rôle sur la période :
    coût employeur, heures prestées, taux de revient, heures imputées (main-d'œuvre),
    taux d'occupation, main-d'œuvre facturable et marge.
    """
    from maindoeuvre.models import MainDoeuvre
    from .models import PaieUtilisateur

    liste_mois = _periode_mois(annee, mois, trimestre)
    paies = (
        PaieUtilisateur.objects
        .filter(utilisateur__societe=societe, utilisateur__role__in=list(ROLES_ATELIER),
                annee=annee, mois__in=liste_mois)
        .select_related("utilisateur")
    )

    lignes = OrderedDict()
    for paie in paies:
        u = paie.utilisateur
        l = lignes.setdefault(u.pk, {
            "utilisateur": u, "role": u.role, "nb_paies": 0,
            "cout": ZERO, "heures": ZERO, "heures_estimees": False,
            "heures_imputees": ZERO, "facturable": ZERO,
        })
        heures, estime = heures_paie(paie)
        l["nb_paies"] += 1
        l["cout"] += cout_paie(paie)
        l["heures"] += heures
        l["heures_estimees"] = l["heures_estimees"] or estime

    # Heures imputées sur les interventions (fiches main-d'œuvre) de la période
    mo = (
        MainDoeuvre.objects
        .filter(utilisateur_id__in=list(lignes), date__year=annee, date__month__in=liste_mois)
        .values("utilisateur_id", "temps_minutes", "taux_horaire")
    )
    for m in mo:
        l = lignes.get(m["utilisateur_id"])
        if not l:
            continue
        h = Decimal(m["temps_minutes"] or 0) / Decimal("60")
        l["heures_imputees"] += h
        l["facturable"] += h * Decimal(m["taux_horaire"] or 0)

    def finaliser(l):
        l["cout"] = r2(l["cout"])
        l["heures"] = r2(l["heures"])
        l["heures_imputees"] = r2(l["heures_imputees"])
        l["facturable"] = r2(l["facturable"])
        l["taux_revient"] = r2(l["cout"] / l["heures"]) if l["heures"] else ZERO
        l["occupation"] = r2(l["heures_imputees"] / l["heures"] * 100) if l["heures"] else ZERO
        # Coût réel des heures imputées et coût des heures non imputées (improductives)
        l["cout_impute"] = r2(l["heures_imputees"] * l["taux_revient"])
        l["cout_non_impute"] = r2(l["cout"] - l["cout_impute"])
        # Taux de revient « productif » : tout le coût réparti sur les seules heures imputées
        l["taux_revient_productif"] = r2(l["cout"] / l["heures_imputees"]) if l["heures_imputees"] else ZERO
        l["marge"] = r2(l["facturable"] - l["cout_impute"])
        return l

    roles = []
    total = {"cout": ZERO, "heures": ZERO, "heures_imputees": ZERO, "facturable": ZERO, "heures_estimees": False}
    for code, libelle in ROLES_ATELIER.items():
        du_role = sorted(
            (finaliser(l) for l in lignes.values() if l["role"] == code),
            key=lambda l: (l["utilisateur"].nom or "", l["utilisateur"].prenom or ""),
        )
        sous = {"cout": ZERO, "heures": ZERO, "heures_imputees": ZERO, "facturable": ZERO, "heures_estimees": False}
        for l in du_role:
            for k in ("cout", "heures", "heures_imputees", "facturable"):
                sous[k] += l[k]
            sous["heures_estimees"] = sous["heures_estimees"] or l["heures_estimees"]
        sous = finaliser(sous)
        for k in ("cout", "heures", "heures_imputees", "facturable"):
            total[k] += sous[k]
        total["heures_estimees"] = total["heures_estimees"] or sous["heures_estimees"]
        roles.append({"code": code, "libelle": libelle, "lignes": du_role, "total": sous})

    return {"roles": roles, "total": finaliser(total), "mois": liste_mois}

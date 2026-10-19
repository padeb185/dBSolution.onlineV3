"""
Rentabilité d'un véhicule (Données financières).

    coût d'acquisition  = prix d'achat + taxe de mise en circulation + autres frais d'achat
  + coûts d'utilisation = carburant + recharges + AdBlue (HTVA)
                        + maintenances (entretien interne au coût de revient + garages externes HTVA)
                        + coûts annuels (assurance, taxe de circulation, vignettes, contrôle technique…)
  = coût total
  − valeur de revente (0 par défaut)
  = coût net
  − revenus des locations (HTVA)
  = résultat net du véhicule

Coût au kilomètre : coûts ÷ kilomètres parcourus depuis l'achat (km châssis − km de départ).
Les montants énergie sont HTVA : la TVA est récupérée par la société.
"""
from collections import OrderedDict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

ZERO = Decimal("0.00")


def r2(x):
    return Decimal(x or 0).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def date_depart(ex):
    """Début de la détention : date d'achat, sinon mise en circulation, sinon création de la fiche."""
    if ex.date_achat:
        return ex.date_achat
    if ex.date_mise_en_circulation:
        return ex.date_mise_en_circulation
    if ex.created_at:
        return timezone.localtime(ex.created_at).date() if timezone.is_aware(ex.created_at) else ex.created_at.date()
    return timezone.localdate()


def _jour(d):
    from datetime import datetime
    if isinstance(d, datetime):
        return timezone.localtime(d).date() if timezone.is_aware(d) else d.date()
    return d


# ------------------------------------------------------------------
# Énergie
# ------------------------------------------------------------------
def energie(ex):
    from adblue.models import AdBlue
    from fuel.models import Fuel
    from fuel.totaux_energie import PAYS_SOCIETE, _ventiler
    from recharge.models import Electricite, RechargeCarburant

    res = OrderedDict([
        ("carburant", {"label": _("Carburant"), "quantite": ZERO, "unite": "L", "ht": ZERO, "ttc": ZERO, "nb": 0}),
        ("electricite", {"label": _("Recharges électriques"), "quantite": ZERO, "unite": "kWh", "ht": ZERO, "ttc": ZERO, "nb": 0}),
        ("adblue", {"label": _("AdBlue"), "quantite": ZERO, "unite": "L", "ht": ZERO, "ttc": ZERO, "nb": 0}),
    ])

    def ajouter(cle, obj, quantite, ttc, taux):
        ht, _tva = _ventiler(ttc, getattr(obj, "montant_ht", None), getattr(obj, "montant_tva", None), taux)
        l = res[cle]
        l["nb"] += 1
        l["quantite"] += Decimal(str(quantite or 0))
        l["ht"] += ht
        l["ttc"] += r2(ttc)

    for f in Fuel.objects.filter(voiture_exemplaire=ex):
        ajouter("carburant", f, f.litres, f.prix_refuelling, Fuel.TVA_CARBURANT.get(f.pays, 0))
    for e in Electricite.objects.filter(voiture_exemplaire=ex):
        ajouter("electricite", e, e.kW, e.prix_recharge, RechargeCarburant.TVA_ELECTRICITE.get(e.pays or PAYS_SOCIETE, 0))
    for a in AdBlue.objects.filter(voiture_exemplaire=ex):
        ajouter("adblue", a, a.litres, a.prix_adblue, AdBlue.TVA_CARBURANT.get(a.pays, 0))

    for l in res.values():
        l["ht"], l["ttc"] = r2(l["ht"]), r2(l["ttc"])
    return res


# ------------------------------------------------------------------
# Maintenances
# ------------------------------------------------------------------
def maintenances(ex):
    from facture.models import Facture

    internes, total_internes = [], ZERO
    for f in (Facture.objects.filter(voiture_exemplaire=ex, client_est_societe=True, statut=Facture.Statut.EMISE)
              .prefetch_related("lines").order_by("-issue_date")):
        c = f.couts_internes()
        internes.append({"facture": f, **c})
        total_internes += c["total"]

    externes, total_externes = [], ZERO
    try:
        from maintenance.maintenance_externe.models import MaintenanceExterne
        for m in MaintenanceExterne.objects.filter(voiture_exemplaire=ex).select_related("garage").order_by("-date_facture"):
            externes.append(m)
            total_externes += Decimal(m.total_htva or 0)
    except Exception:
        pass

    return {
        "internes": internes, "total_internes": r2(total_internes),
        "externes": externes, "total_externes": r2(total_externes),
        "total": r2(total_internes + total_externes),
    }


# ------------------------------------------------------------------
# Coûts annuels (assurance, taxe de circulation, vignettes…)
# ------------------------------------------------------------------
def couts_annuels(ex, aujourdhui=None):
    from .models import CoutAnnuelVehicule as C

    aujourdhui = aujourdhui or timezone.localdate()
    debut = date_depart(ex)
    lignes_saisies = list(ex.couts_annuels.all())
    annees = sorted({a for a in range(debut.year, aujourdhui.year + 1)} | {l.annee for l in lignes_saisies}, reverse=True)

    par_annee = []
    total = ZERO
    for annee in annees:
        lignes = [{"objet": l, "type": l.type_cout, "libelle": l.get_type_cout_display(),
                   "detail": " – ".join(x for x in (l.get_pays_display() if l.pays else "", l.libelle) if x),
                   "montant": r2(l.montant), "defaut": False}
                  for l in lignes_saisies if l.annee == annee]
        types_saisis = {l["type"] for l in lignes}

        # Mois de détention dans l'année (prorata des montants par défaut)
        m_debut = debut.month if annee == debut.year else 1
        m_fin = aujourdhui.month if annee == aujourdhui.year else 12
        mois = max(m_fin - m_debut + 1, 0) if debut.year <= annee <= aujourdhui.year else 0

        for type_cout, defaut in ((C.Type.ASSURANCE, ex.assurance), (C.Type.TAXE_CIRCULATION, ex.taxe_roulage)):
            if type_cout not in types_saisis and defaut and mois:
                montant = r2(Decimal(defaut) * mois / 12)
                lignes.append({"objet": None, "type": type_cout, "libelle": C.Type(type_cout).label,
                               "detail": _("montant annuel par défaut (%(mois)s/12 mois)") % {"mois": mois},
                               "montant": montant, "defaut": True, "annuel": r2(defaut)})
        sous_total = r2(sum((l["montant"] for l in lignes), ZERO))
        total += sous_total
        par_annee.append({"annee": annee, "lignes": lignes, "total": sous_total, "mois": mois})
    return {"annees": par_annee, "total": r2(total), "debut": debut}


# ------------------------------------------------------------------
# Locations
# ------------------------------------------------------------------
def locations(ex):
    from voiture.voiture_location.models import Location

    liste = list(Location.objects.filter(voiture_exemplaire=ex).order_by("-date_debut"))
    return {
        "liste": liste,
        "nb": len(liste),
        "htva": r2(sum((l.prix_htva for l in liste), ZERO)),
        "tvac": r2(sum((l.prix_tvac for l in liste), ZERO)),
        "km": sum((l.kilometrage or 0 for l in liste)),
    }


# ------------------------------------------------------------------
# Synthèse
# ------------------------------------------------------------------
def rentabilite(ex):
    acquisition = {
        "prix_achat": r2(ex.prix_achat),
        "taxe_mise_en_circulation": r2(ex.taxe_mise_en_circulation),
        "frais_achat": r2(ex.frais_achat),
    }
    acquisition["total"] = r2(sum(acquisition.values(), ZERO))

    en = energie(ex)
    total_energie = r2(sum((l["ht"] for l in en.values()), ZERO))
    mt = maintenances(ex)
    an = couts_annuels(ex)
    loc = locations(ex)

    utilisation = r2(total_energie + mt["total"] + an["total"])
    cout_total = r2(acquisition["total"] + utilisation)
    valeur_revente = r2(ex.valeur_revente)
    cout_net = r2(cout_total - valeur_revente)
    resultat = r2(loc["htva"] - cout_net)

    km = max(int(ex.kilometres_chassis or 0) - int(ex.kilometrage_achat or 0), 0)
    par_km = lambda x: (Decimal(x) / km).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP) if km else None

    return {
        "acquisition": acquisition,
        "energie": en,
        "total_energie": total_energie,
        "maintenances": mt,
        "couts_annuels": an,
        "locations": loc,
        "utilisation": utilisation,
        "cout_total": cout_total,
        "valeur_revente": valeur_revente,
        "cout_net": cout_net,
        "resultat": resultat,
        "km": km,
        "km_depart": int(ex.kilometrage_achat or 0),
        "par_km": {
            "energie": par_km(total_energie),
            "maintenances": par_km(mt["total"]),
            "annuels": par_km(an["total"]),
            "utilisation": par_km(utilisation),
            "total": par_km(cout_total),
            "revente": par_km(valeur_revente),
            "cout_net": par_km(cout_net),
            "revenus": par_km(loc["htva"]),
            "net": par_km(resultat),
        },
    }

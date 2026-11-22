"""
Rapport des voitures (Direction) : statistiques et graphiques de coûts.

- Véhicules de la société : coûts depuis l'achat, repris des Données financières (rentabilite.py) :
  acquisition, énergie, maintenances (pièces / main-d'œuvre), coûts annuels, coût au km, locations.
- Véhicules clients : chiffre d'affaires HTVA des factures émises aux clients (notes de crédit déduites),
  ventilé en pièces, main-d'œuvre et autres lignes, avec coût de revient, marge et heures facturées.
"""
from collections import OrderedDict
from decimal import Decimal

from django.utils.translation import gettext as _

from .rentabilite import r2, rentabilite

ZERO = Decimal("0.00")
TOP_VEHICULES = 7          # au-delà : regroupés dans « Autres véhicules »


def _nom(ex):
    marque = getattr(ex.voiture_marque, "nom_marque", "") or ""
    modele = getattr(ex.voiture_modele, "nom_modele", "") or ""
    return f"{marque} {modele}".strip()


def _top(items, cle_valeur, cle_label):
    """Les TOP_VEHICULES plus grands + « Autres véhicules » (pour un camembert lisible)."""
    tries = sorted((i for i in items if i[cle_valeur] > 0), key=lambda i: i[cle_valeur], reverse=True)
    parts = [{"label": i[cle_label], "valeur": float(i[cle_valeur])} for i in tries[:TOP_VEHICULES]]
    reste = sum((i[cle_valeur] for i in tries[TOP_VEHICULES:]), ZERO)
    if reste > 0:
        parts.append({"label": _("Autres véhicules"), "valeur": float(reste)})
    return parts


def _parts(paires):
    return [{"label": str(l), "valeur": float(v)} for l, v in paires if v and v > 0]


# ------------------------------------------------------------------ véhicules de la société
def rapport_societe(qs):
    lignes = []
    for ex in qs:
        r = rentabilite(ex)
        mt = r["maintenances"]
        lignes.append({
            "ex": ex, "nom": _nom(ex), "immat": ex.immatriculation or "—",
            "label": f"{ex.immatriculation or _nom(ex)}",
            "km": r["km"],
            "acquisition": r["acquisition"]["total"],
            "energie": r["total_energie"],
            "pieces": mt["total_pieces"], "main_oeuvre": mt["total_main_oeuvre"],
            "maintenances": mt["total"],
            "annuels": r["couts_annuels"]["total"],
            "utilisation": r["utilisation"],
            "cout_total": r["cout_total"],
            "par_km": r["par_km"]["total"],
            "locations": r["locations"]["htva"],
            "resultat": r["resultat"],
            "carburant": r["energie"]["carburant"]["ht"] + (r["energie"].get("carburant_estime") or {}).get("ht", ZERO),
            "electricite": r["energie"]["electricite"]["ht"],
            "adblue": r["energie"]["adblue"]["ht"],
        })
    lignes.sort(key=lambda l: l["cout_total"], reverse=True)

    def somme(cle):
        return r2(sum((l[cle] for l in lignes), ZERO))

    cles = ("km", "acquisition", "energie", "pieces", "main_oeuvre", "maintenances", "annuels", "utilisation",
            "cout_total", "locations", "resultat", "carburant", "electricite", "adblue")
    totaux = {c: (sum(l[c] for l in lignes) if c == "km" else somme(c)) for c in cles}
    totaux["par_km"] = (totaux["utilisation"] / totaux["km"]).quantize(Decimal("0.001")) if totaux["km"] else None

    graphiques = OrderedDict([
        ("repartition", {"titre": _("Répartition des coûts de la flotte"), "parts": _parts([
            (_("Acquisition"), totaux["acquisition"]), (_("Énergie"), totaux["energie"]),
            (_("Maintenances"), totaux["maintenances"]), (_("Coûts annuels"), totaux["annuels"])])}),
        ("utilisation", {"titre": _("Coûts d'utilisation"), "parts": _parts([
            (_("Carburant"), totaux["carburant"]), (_("Recharges électriques"), totaux["electricite"]),
            (_("AdBlue"), totaux["adblue"]), (_("Pièces"), totaux["pieces"]),
            (_("Main-d'œuvre"), totaux["main_oeuvre"]), (_("Coûts annuels"), totaux["annuels"])])}),
        ("vehicules", {"titre": _("Coût total par véhicule"), "parts": _top(lignes, "cout_total", "label")}),
    ])
    return {"lignes": lignes, "totaux": totaux, "nb": len(lignes), "graphiques": graphiques}


# ------------------------------------------------------------------ véhicules clients
def _annees_factures(societe):
    from facture.models import Facture
    return sorted({d.year for d in Facture.objects.filter(
        societe=societe, statut=Facture.Statut.EMISE, client_est_societe=False,
        voiture_exemplaire__isnull=False).values_list("issue_date", flat=True) if d}, reverse=True)


def rapport_clients(societe, annee=None):
    from facture.models import Facture, FactureLine
    T = FactureLine.TypeLigne

    qs = (Facture.objects.filter(societe=societe, statut=Facture.Statut.EMISE, client_est_societe=False,
                                 voiture_exemplaire__isnull=False)
          .select_related("voiture_exemplaire__voiture_marque", "voiture_exemplaire__voiture_modele",
                          "client_particulier", "client_atelier", "societe_cliente", "proprietaire")
          .prefetch_related("lines"))
    if annee:
        qs = qs.filter(issue_date__year=annee)

    vide = lambda: {"pieces": ZERO, "pieces_cout": ZERO, "main_oeuvre": ZERO, "main_oeuvre_cout": ZERO,
                    "heures": ZERO, "autres": ZERO, "total": ZERO, "cout": ZERO, "nb": 0}
    par_vehicule, mois = OrderedDict(), OrderedDict((m, {"pieces": ZERO, "main_oeuvre": ZERO, "autres": ZERO})
                                                    for m in range(1, 13))
    for f in qs:
        signe = Decimal("-1") if f.type_document == Facture.TypeDocument.NOTE_CREDIT else Decimal("1")
        ex = f.voiture_exemplaire
        v = par_vehicule.get(ex.pk)
        if v is None:
            v = par_vehicule[ex.pk] = {"ex": ex, "nom": _nom(ex), "immat": ex.immatriculation or "—",
                                       "label": ex.immatriculation or _nom(ex), "clients": set(), **vide()}
        nom_client = f.client_nom or f.nom_client_courant()
        if nom_client:
            v["clients"].add(nom_client)
        v["nb"] += 1
        for l in f.lines.all():
            if l.type_ligne == T.LOCATION:
                continue                       # les locations ne sont pas de l'atelier
            ht = l.total_ht * signe
            cout = l.cout_total * signe
            if l.type_ligne == T.PIECE:
                v["pieces"] += ht; v["pieces_cout"] += cout; cle = "pieces"
            elif l.type_ligne == T.MAIN_OEUVRE:
                v["main_oeuvre"] += ht; v["main_oeuvre_cout"] += cout
                v["heures"] += Decimal(l.quantity or 0) * signe; cle = "main_oeuvre"
            else:
                v["autres"] += ht; cle = "autres"
            v["total"] += ht
            v["cout"] += cout
            if annee:
                mois[f.issue_date.month][cle] += ht

    lignes = []
    for v in par_vehicule.values():
        if not v["total"]:
            continue
        v["clients"] = ", ".join(sorted(v["clients"]))
        v["marge"] = r2(v["total"] - v["cout"])
        v["marge_pct"] = (v["marge"] * 100 / v["total"]).quantize(Decimal("0.1")) if v["total"] else None
        for c in ("pieces", "pieces_cout", "main_oeuvre", "main_oeuvre_cout", "autres", "total", "cout"):
            v[c] = r2(v[c])
        v["heures"] = v["heures"].quantize(Decimal("0.01"))
        lignes.append(v)
    lignes.sort(key=lambda l: l["total"], reverse=True)

    def somme(cle):
        return r2(sum((l[cle] for l in lignes), ZERO))

    totaux = {c: somme(c) for c in ("pieces", "pieces_cout", "main_oeuvre", "main_oeuvre_cout", "autres",
                                     "total", "cout", "marge")}
    totaux["heures"] = sum((l["heures"] for l in lignes), Decimal("0")).quantize(Decimal("0.01"))
    totaux["nb_factures"] = sum(l["nb"] for l in lignes)
    totaux["marge_pct"] = (totaux["marge"] * 100 / totaux["total"]).quantize(Decimal("0.1")) if totaux["total"] else None
    totaux["marge_pieces"] = r2(totaux["pieces"] - totaux["pieces_cout"])
    totaux["marge_main_oeuvre"] = r2(totaux["main_oeuvre"] - totaux["main_oeuvre_cout"])
    totaux["taux_horaire_moyen"] = r2(totaux["main_oeuvre"] / totaux["heures"]) if totaux["heures"] else None

    graphiques = OrderedDict([
        ("repartition", {"titre": _("Chiffre d'affaires atelier : pièces et main-d'œuvre"), "parts": _parts([
            (_("Pièces"), totaux["pieces"]), (_("Main-d'œuvre"), totaux["main_oeuvre"]), (_("Autres"), totaux["autres"])])}),
        ("marge", {"titre": _("Marge : pièces et main-d'œuvre"), "parts": _parts([
            (_("Marge pièces"), totaux["marge_pieces"]), (_("Marge main-d'œuvre"), totaux["marge_main_oeuvre"])])}),
        ("vehicules", {"titre": _("Chiffre d'affaires par véhicule"), "parts": _top(lignes, "total", "label")}),
    ])
    evolution = None
    if annee:
        evolution = {"mois": list(mois.keys()),
                     "pieces": [float(m["pieces"]) for m in mois.values()],
                     "main_oeuvre": [float(m["main_oeuvre"]) for m in mois.values()],
                     "autres": [float(m["autres"]) for m in mois.values()]}
    return {"lignes": lignes, "totaux": totaux, "nb": len(lignes), "graphiques": graphiques, "evolution": evolution}

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


# ------------------------------------------------------------------ locations
def _annees_locations(societe):
    from voiture.voiture_location.models import Location
    return sorted({d.year for d in Location.objects.filter(societe=societe).values_list("date_debut", flat=True) if d},
                  reverse=True)


def rapport_locations(societe, annee=None):
    """
    Locations de véhicules : chiffre d'affaires HTVA (prix de la location, toutes options comprises),
    ventilé par composante, par véhicule et par lieu (circuit ou route), avec jours loués, km et reste à payer.
    """
    from voiture.voiture_location.models import Location, prix_htva_depuis_tvac

    qs = (Location.objects.filter(societe=societe)
          .select_related("voiture_exemplaire__voiture_marque", "voiture_exemplaire__voiture_modele",
                          "client", "societe_cliente", "client_pilotage__client_particulier", "instructeur",
                          "societe")
          .prefetch_related("boxes", "factures__lines"))
    if annee:
        qs = qs.filter(date_debut__year=annee)

    composantes = OrderedDict([
        ("vehicule", [_("Location du véhicule"), ZERO]), ("boxes", [_("Box en pit lane"), ZERO]),
        ("instructeur", [_("Instructeur"), ZERO]), ("deuxieme_pilote", [_("Deuxième pilote"), ZERO]),
        ("carburant", [_("Carburant inclus"), ZERO]), ("km_supp", [_("Kilomètres supplémentaires"), ZERO]),
    ])
    par_vehicule, par_lieu = OrderedDict(), OrderedDict()
    mois = OrderedDict((m, ZERO) for m in range(1, 13))
    nb = jours_total = km_total = 0
    ca_total = reste_total = ZERO

    for loc in qs:
        taux = loc.taux_tva
        htva = lambda tvac: prix_htva_depuis_tvac(tvac, taux)
        parts = {
            "vehicule": htva(loc.prix_vehicule_tvac), "boxes": htva(loc.total_boxes_tvac),
            "instructeur": htva(loc.total_instructeur_tvac), "deuxieme_pilote": htva(loc.total_deuxieme_pilote_tvac),
            "carburant": htva(loc.total_carburant_tvac), "km_supp": htva(loc.total_km_supplementaires_tvac),
        }
        ca = r2(loc.prix_htva)
        jours = ((loc.date_fin - loc.date_debut).days + 1) if loc.date_fin and loc.date_fin >= loc.date_debut else 1
        km = int(loc.kilometrage or 0)
        reste = r2(loc.reste_a_payer)
        nb += 1; jours_total += jours; km_total += km; ca_total += ca; reste_total += reste
        for c, v in parts.items():
            composantes[c][1] += v
        if annee:
            mois[loc.date_debut.month] += ca

        ex = loc.voiture_exemplaire
        v = par_vehicule.get(ex.pk) if ex else None
        if ex and v is None:
            v = par_vehicule[ex.pk] = {"ex": ex, "nom": _nom(ex), "immat": ex.immatriculation or "—",
                                       "label": ex.immatriculation or _nom(ex), "nb": 0, "jours": 0, "km": 0,
                                       "vehicule": ZERO, "options": ZERO, "total": ZERO, "reste": ZERO,
                                       "circuit": 0, "route": 0, "a_payer": OrderedDict()}
        if v is not None:
            v["nb"] += 1; v["jours"] += jours; v["km"] += km
            v["vehicule"] += parts["vehicule"]; v["options"] += ca - parts["vehicule"]
            v["total"] += ca; v["reste"] += reste
            v["circuit" if loc.type_location == "circuit" else "route"] += 1
            if reste > 0:
                _cibles_a_payer(v["a_payer"], loc, reste)

        lieu = loc.lieu or loc.get_type_location_display()
        par_lieu[lieu] = par_lieu.get(lieu, ZERO) + ca

    lignes = []
    for v in par_vehicule.values():
        v["a_payer"] = list(v["a_payer"].values())
        for c in ("vehicule", "options", "total", "reste"):
            v[c] = r2(v[c])
        v["par_jour"] = r2(v["total"] / v["jours"]) if v["jours"] else None
        v["par_km"] = (v["total"] / v["km"]).quantize(Decimal("0.001")) if v["km"] else None
        lignes.append(v)
    lignes.sort(key=lambda l: l["total"], reverse=True)

    ca_total = r2(ca_total)
    totaux = {
        "nb": nb, "jours": jours_total, "km": km_total, "total": ca_total, "reste": r2(reste_total),
        "vehicule": r2(sum((l["vehicule"] for l in lignes), ZERO)),
        "options": r2(sum((l["options"] for l in lignes), ZERO)),
        "moyenne": r2(ca_total / nb) if nb else None,
        "par_jour": r2(ca_total / jours_total) if jours_total else None,
        "par_km": (ca_total / km_total).quantize(Decimal("0.001")) if km_total else None,
    }
    lieux = [{"label": l, "total": t} for l, t in par_lieu.items()]
    graphiques = OrderedDict([
        ("composantes", {"titre": _("Chiffre d'affaires des locations par composante"),
                         "parts": _parts([(l, r2(v)) for l, v in composantes.values()])}),
        ("vehicules", {"titre": _("Chiffre d'affaires des locations par véhicule"), "parts": _top(lignes, "total", "label")}),
        ("lieux", {"titre": _("Chiffre d'affaires par circuit ou route"), "parts": _top(lieux, "total", "label")}),
    ])
    evolution = {"mois": list(mois.keys()), "locations": [float(x) for x in mois.values()]} if annee else None
    return {"lignes": lignes, "totaux": totaux, "nb": len(lignes), "graphiques": graphiques, "evolution": evolution}


def _cibles_a_payer(cibles, loc, reste):
    """
    Liens « reste à payer » d'une location : ses factures pas encore payées (principale et complémentaires
    de kilomètres supplémentaires), sinon la location elle-même quand elle n'est pas encore facturée.
    Une facture commune à plusieurs locations n'apparaît qu'une fois.
    """
    from django.urls import reverse

    factures = [f for f in loc.factures.all() if f.statut_paiement != "PAYE" and f.type_document != "NOTE_CREDIT"]
    for f in factures:
        cle = f"f{f.pk}"
        if cle not in cibles:
            cibles[cle] = {"url": reverse("facture:detail", args=[f.pk]),
                           "libelle": f.numero or _("Facture brouillon"),
                           "detail": f.get_statut_paiement_display() if f.est_emise else _("Brouillon"),
                           "montant": r2(f.reste_a_payer) if f.est_emise else r2(f.total)}
    if not factures:
        cibles[f"l{loc.pk}"] = {"url": reverse("voiture_location:location_detail", args=[loc.pk]),
                                "libelle": _("Location du %(date)s") % {"date": loc.date_debut.strftime("%d/%m/%Y")},
                                "detail": _("non facturée") if loc.facture is None else loc.statut_paiement_display,
                                "montant": reste}


# ------------------------------------------------------------------ coûts et gains (bilan)
def _postes_vehicule(ex, r=None):
    """
    Tous les coûts (HTVA) et gains d'un véhicule depuis l'achat, poste par poste,
    à partir des Données financières (rentabilite.py) :
    coûts = acquisition + énergie + maintenances + coûts annuels ; gains = locations + valeur de revente.
    """
    from .models import CoutAnnuelVehicule as C

    r = r or rentabilite(ex)
    a, en, mt = r["acquisition"], r["energie"], r["maintenances"]
    annuels = OrderedDict((t.value, ZERO) for t in C.Type)
    for an in r["couts_annuels"]["annees"]:
        for l in an["lignes"]:
            annuels[l["type"]] = annuels.get(l["type"], ZERO) + l["montant"]

    couts = OrderedDict([
        ("acquisition", (_("Acquisition"), OrderedDict([
            ("prix_achat", (_("Prix d'achat"), a.get("prix_achat", ZERO))),
            ("loyers", (_("Loyers de leasing / renting"), a.get("loyers", ZERO))),
            ("interets", (_("Intérêts du crédit"), a.get("interets", ZERO))),
            ("taxe_mise_en_circulation", (_("Taxe de mise en circulation"), a.get("taxe_mise_en_circulation", ZERO))),
            ("frais_achat", (_("Autres frais d'achat"), a.get("frais_achat", ZERO))),
        ]))),
        ("energie", (_("Énergie"), OrderedDict([
            ("carburant", (_("Carburant"), en["carburant"]["ht"])),
            ("carburant_estime", (_("Carburant non encodé (estimation)"), (en.get("carburant_estime") or {}).get("ht", ZERO))),
            ("electricite", (_("Recharges électriques"), en["electricite"]["ht"])),
            ("adblue", (_("AdBlue"), en["adblue"]["ht"])),
        ]))),
        ("maintenances", (_("Maintenances"), OrderedDict([
            ("internes", (_("Atelier interne (pièces et main-d'œuvre)"), mt["total_internes"])),
            ("externes", (_("Garages externes"), r2(mt["total_externes"] - mt["total_carrosseries"]))),
            ("carrosseries", (_("Carrosserie (reste à charge après assurance)"), mt["total_carrosseries"])),
        ]))),
        ("annuels", (_("Coûts annuels"), OrderedDict(
            (t, (C.Type(t).label, annuels.get(t, ZERO))) for t in annuels))),
    ])
    gains = OrderedDict([
        ("locations", (_("Locations (HTVA)"), r["locations"]["htva"])),
        ("revente", (_("Valeur de revente"), r["valeur_revente"])),
    ])
    return {"couts": couts, "gains": gains, "km": r["km"], "nb_locations": r["locations"]["nb"]}


def rapport_bilan(qs, exemplaire_id=None):
    """Bilan coûts / gains de toute la flotte ou d'un seul véhicule, et comparaison par véhicule."""
    vehicules = list(qs)
    selection = [v for v in vehicules if str(v.pk) == str(exemplaire_id)] if exemplaire_id else vehicules

    couts, gains = OrderedDict(), OrderedDict()
    par_vehicule, km = [], 0
    for ex in selection:
        p = _postes_vehicule(ex)
        km += p["km"]
        c_ex = g_ex = ZERO
        for cle, (libelle, postes) in p["couts"].items():
            bloc = couts.setdefault(cle, {"libelle": libelle, "postes": OrderedDict(), "total": ZERO})
            for k, (lib, montant) in postes.items():
                ligne = bloc["postes"].setdefault(k, {"libelle": lib, "montant": ZERO})
                ligne["montant"] += montant
                bloc["total"] += montant
                c_ex += montant
        for k, (lib, montant) in p["gains"].items():
            ligne = gains.setdefault(k, {"libelle": lib, "montant": ZERO})
            ligne["montant"] += montant
            g_ex += montant
        par_vehicule.append({"ex": ex, "label": ex.immatriculation or _nom(ex), "couts": r2(c_ex), "gains": r2(g_ex),
                             "resultat": r2(g_ex - c_ex)})

    # Postes à zéro masqués ; arrondis
    for bloc in couts.values():
        bloc["postes"] = [dict(l, montant=r2(l["montant"])) for l in bloc["postes"].values() if l["montant"]]
        bloc["total"] = r2(bloc["total"])
    blocs = [b for b in couts.values() if b["postes"]]
    gains_l = [dict(l, montant=r2(l["montant"])) for l in gains.values() if l["montant"]]
    total_couts = r2(sum((b["total"] for b in blocs), ZERO))
    total_gains = r2(sum((l["montant"] for l in gains_l), ZERO))
    resultat = r2(total_gains - total_couts)

    detail = [(l["libelle"], l["montant"]) for b in blocs for l in b["postes"] if l["montant"] > 0]
    graphiques = OrderedDict([
        ("couts", {"titre": _("Tous les coûts, poste par poste"), "parts": _parts(detail)}),
        ("blocs", {"titre": _("Coûts par catégorie"), "parts": _parts([(b["libelle"], b["total"]) for b in blocs])}),
        ("gains", {"titre": _("Coûts et gains"), "parts": _parts([(_("Coûts"), total_couts)] +
                                                                [(l["libelle"], l["montant"]) for l in gains_l])}),
    ])
    par_vehicule.sort(key=lambda v: v["resultat"])
    return {
        "vehicules": vehicules, "exemplaire_id": str(exemplaire_id or ""), "nb": len(selection),
        "blocs": blocs, "gains": gains_l, "total_couts": total_couts, "total_gains": total_gains,
        "resultat": resultat, "km": km,
        "cout_km": (total_couts / km).quantize(Decimal("0.001")) if km else None,
        "resultat_km": (resultat / km).quantize(Decimal("0.001")) if km else None,
        "par_vehicule": par_vehicule, "graphiques": graphiques, "lignes": par_vehicule,
        "comparaison": {"labels": [v["label"] for v in par_vehicule],
                        "couts": [float(v["couts"]) for v in par_vehicule],
                        "gains": [float(v["gains"]) for v in par_vehicule]} if len(selection) > 1 else None,
    }


def graphiques_vehicule(ex, r):
    """Camemberts 3D des Données financières d'un véhicule, à partir de son calcul de rentabilité."""
    p = _postes_vehicule(ex, r)
    blocs = [(libelle, sum((m for _l, m in postes.values()), ZERO)) for libelle, postes in p["couts"].values()]
    detail = [(lib, m) for _b, postes in p["couts"].values() for lib, m in postes.values()]
    total_couts = r2(sum((m for _l, m in blocs), ZERO))
    gains = [(lib, m) for lib, m in p["gains"].values()]
    mt = r["maintenances"]
    return [
        {"titre": _("Coûts par catégorie"), "parts": _parts(blocs)},
        {"titre": _("Tous les coûts, poste par poste"), "parts": _parts(detail)},
        {"titre": _("Coûts et gains"), "parts": _parts([(_("Coûts"), total_couts)] + gains)},
        {"titre": _("Maintenances : pièces et main-d'œuvre"), "parts": _parts([
            (_("Pièces"), mt["total_pieces"]), (_("Main-d'œuvre"), mt["total_main_oeuvre"])])},
    ]

"""Calculs de l'espace particuliers : consommation, coûts, rappels (échéances)."""
import calendar
from collections import OrderedDict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

D = Decimal
ZERO = D("0.00")
SEUIL_JOURS = 30        # rappel « proche » : échéance dans 30 jours…
SEUIL_KM = 1000         # … ou dans 1 000 km


def r2(x):
    return D(x or 0).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def ajouter_mois(d, n):
    m = d.month - 1 + n
    a = d.year + m // 12
    m = m % 12 + 1
    return date(a, m, min(d.day, calendar.monthrange(a, m)[1]))


def mois_entre(debut, fin):
    if not debut or not fin or fin < debut:
        return 0
    n = (fin.year - debut.year) * 12 + fin.month - debut.month
    return n - 1 if fin.day < debut.day else n


# ------------------------------------------------------------------
# Consommation (méthode du plein à plein)
# ------------------------------------------------------------------
def famille_carburant(carburant):
    """Les consommations ne se mélangent pas : carburants liquides (L), électricité (kWh), GNC (kg)."""
    from .models import unite_carburant
    return unite_carburant(carburant)


def famille_principale(vehicule):
    from .models import CARBURANT_PAR_ENERGIE, Carburant
    return famille_carburant(CARBURANT_PAR_ENERGIE.get(vehicule.energie, Carburant.SP95))


def consommation(vehicule, unite=None):
    """
    Consommation entre deux pleins complets : quantités ajoutées depuis le plein complet précédent
    (pleins partiels compris) ÷ kilomètres parcourus × 100, pour une seule famille de carburant
    (par défaut celle de l'énergie du véhicule) : L/100 km, kWh/100 km ou kg/100 km.
    Hybride rechargeable : carburant et recharges sont calculés séparément.
    """
    unite = unite or famille_principale(vehicule)
    pleins = sorted((p for p in vehicule.pleins.all() if famille_carburant(p.carburant) == unite),
                    key=lambda p: (p.kilometrage, p.date))
    mesures, precedent, cumul = [], None, ZERO
    for p in pleins:
        if precedent is not None:
            cumul += D(p.quantite)
        if p.plein_complet:
            if precedent is not None and p.kilometrage > precedent.kilometrage:
                km = p.kilometrage - precedent.kilometrage
                mesures.append({"date": p.date, "km": km, "quantite": r2(cumul),
                                "conso": (cumul / km * 100).quantize(D("0.01"))})
            precedent, cumul = p, ZERO
    total_q = sum((m["quantite"] for m in mesures), ZERO)
    total_km = sum(m["km"] for m in mesures)
    return {
        "mesures": mesures,
        "moyenne": (total_q / total_km * 100).quantize(D("0.01")) if total_km else None,
        "derniere": mesures[-1]["conso"] if mesures else None,
        "unite": unite,
    }


# ------------------------------------------------------------------
# Rappels
# ------------------------------------------------------------------
def statut_rappel(rappel, km_actuel, aujourdhui=None):
    aujourdhui = aujourdhui or date.today()
    jours = (rappel.echeance_date - aujourdhui).days if rappel.echeance_date else None
    km = (rappel.echeance_km - km_actuel) if rappel.echeance_km is not None else None
    if not rappel.actif:
        statut = "inactif"
    elif (jours is not None and jours < 0) or (km is not None and km <= 0):
        statut = "en_retard"
    elif (jours is not None and jours <= SEUIL_JOURS) or (km is not None and km <= SEUIL_KM):
        statut = "proche"
    else:
        statut = "a_venir"
    return {"statut": statut, "jours_restants": jours, "km_restants": km}


def marquer_fait(rappel, jour=None, km=None):
    """Rappel réalisé : nouvelle échéance selon les intervalles, sinon désactivé."""
    jour = jour or date.today()
    if not (rappel.intervalle_mois or rappel.intervalle_km):
        rappel.actif = False
    else:
        rappel.echeance_date = ajouter_mois(jour, rappel.intervalle_mois) if rappel.intervalle_mois else None
        rappel.echeance_km = (km + rappel.intervalle_km) if (rappel.intervalle_km and km is not None) else None
        rappel.actif = True
    rappel.save()
    return rappel


def synchroniser_rappel_document(document):
    """Document avec date d'expiration (assurance, contrôle technique…) : rappel à l'échéance."""
    from .models import Rappel
    rappel = getattr(document, "rappel", None) if document.pk else None
    if not document.date_expiration:
        if rappel:
            rappel.delete()
        return None
    libelle = f"{document.get_type_display()} – {document.titre}".strip(" –") if document.titre else str(document.get_type_display())
    if rappel is None:
        rappel = Rappel(vehicule=document.vehicule, document=document)
    rappel.libelle = str(_("Échéance : %(doc)s") % {"doc": libelle})[:120]
    rappel.echeance_date = document.date_expiration
    rappel.echeance_km = None
    rappel.actif = document.date_expiration >= date.today() or rappel.actif
    rappel.save()
    return rappel


def avancer_rappels_entretien(entretien):
    """Entretien encodé : les rappels actifs du même type repartent de cette date / ce kilométrage."""
    if not entretien.type:
        return []
    faits = []
    for rappel in entretien.vehicule.rappels.filter(actif=True, type_entretien=entretien.type, document__isnull=True,
                                                    code=""):   # rappels automatiques : rappels_auto.apres_entretien
        faits.append(marquer_fait(rappel, entretien.date, entretien.kilometrage))
    from .rappels_auto import apres_entretien
    apres_entretien(entretien.vehicule, entretien.date, entretien.kilometrage, type_entretien=entretien.type)
    return faits


# ------------------------------------------------------------------
# Coûts et rentabilité
# ------------------------------------------------------------------
def _somme(qs, champ="montant"):
    return r2(qs.aggregate(s=Sum(champ))["s"])


def paiements_document(document, aujourdhui=None):
    """Paiements d'un document [(date, montant)] : prime mensuelle chaque mois (annuelle chaque année) de la date
    de début jusqu'à l'expiration, au plus aujourd'hui ; sans mode : le montant une fois, à la date de début."""
    aujourdhui = aujourdhui or date.today()
    if document.montant is None:
        return []
    montant = D(document.montant)
    if document.mode_paiement in ("mensuel", "annuel") and document.date_debut:
        pas = 1 if document.mode_paiement == "mensuel" else 12
        fin = min(document.date_expiration, aujourdhui) if document.date_expiration else aujourdhui
        paiements, n = [], 0
        while True:
            jour = ajouter_mois(document.date_debut, n * pas)
            if jour > fin or (document.date_expiration and jour >= document.date_expiration):
                break
            paiements.append((jour, montant))
            n += 1
        return paiements
    return [(document.date_debut, montant)]


def paiements_documents(vehicule, aujourdhui=None):
    return [p for d in vehicule.documents.all() for p in paiements_document(d, aujourdhui)]


def mois_detention(debut, aujourdhui):
    """Durée de détention en mois, mois partiels compris (jours ÷ 30,44), au moins 1 mois :
    le coût mensuel s'affiche dès le premier mois. None sans date d'achat."""
    if not debut:
        return None
    jours = (aujourdhui - debut).days
    if jours < 0:
        return None
    return max(D(jours) / D("30.4375"), D(1)).quantize(D("0.1"))


# ------------------------------------------------------------------
# Type d'achat : prêt, leasing, renting
# ------------------------------------------------------------------
def mensualite_pret(capital, taux_annuel, duree_mois):
    """Mensualité constante d'un prêt amortissable (taux annuel en %)."""
    if not capital or not duree_mois:
        return None
    capital, r = D(capital), D(taux_annuel or 0) / D(1200)
    if r == 0:
        return r2(capital / duree_mois)
    return r2(capital * r / (1 - (1 + r) ** -duree_mois))


def financement(vehicule, aujourdhui=None):
    """Mensualités, intérêts, capital restant, loyers payés et kilomètres du contrat, à la date du jour.
    None si le véhicule n'a pas de type d'achat (comptant implicite)."""
    from .models import Financement
    aujourdhui = aujourdhui or date.today()
    try:
        f = vehicule.financement
    except Financement.DoesNotExist:
        return None
    debut = f.date_debut or vehicule.date_achat
    duree = f.duree_mois or 0
    ecoules = mois_entre(debut, aujourdhui) if debut else 0
    payes = min(ecoules, duree) if duree else ecoules
    res = {"type_achat": f.type_achat, "date_debut": debut, "duree_mois": duree or None,
           "mois_payes": payes, "mois_restants": max(duree - payes, 0) if duree else None,
           "date_fin": ajouter_mois(debut, duree) if debut and duree else None,
           "mensualite": None, "paye_a_ce_jour": ZERO, "reste_a_payer": None}

    if f.type_achat == "pret":
        capital = D(f.montant_emprunte) if f.montant_emprunte is not None else (
            D(vehicule.prix_achat) - D(f.apport or 0) if vehicule.prix_achat is not None else None)
        mensualite = r2(f.mensualite) if f.mensualite is not None else mensualite_pret(capital, f.taux_annuel, duree)
        r = D(f.taux_annuel or 0) / D(1200)
        restant, interets = D(capital or 0), ZERO
        for _i in range(payes if mensualite else 0):
            i = restant * r
            interets += i
            restant = max(restant - (D(mensualite) - i), ZERO)
        res.update(
            capital=r2(capital) if capital is not None else None, mensualite=mensualite,
            interets_a_ce_jour=r2(interets), capital_restant=r2(restant),
            interets_totaux=r2(D(mensualite) * duree - D(capital)) if mensualite and capital and duree else None,
            paye_a_ce_jour=r2(D(f.apport or 0) + D(mensualite or 0) * payes),
            reste_a_payer=r2(D(mensualite or 0) * (duree - payes)) if duree else None,
        )
    elif f.type_achat in ("leasing", "renting"):
        mensualite = r2(f.mensualite) if f.mensualite is not None else None
        loyers = r2(D(f.premier_loyer or 0) + D(mensualite or 0) * payes)
        res.update(
            mensualite=mensualite, loyers_a_ce_jour=loyers, paye_a_ce_jour=loyers,
            reste_a_payer=r2(D(mensualite or 0) * (duree - payes)) if duree else None,
            valeur_residuelle=r2(f.valeur_residuelle) if f.valeur_residuelle is not None else None,
            option_levee=f.type_achat == "leasing" and f.option_levee,
            cout_total_contrat=r2(D(f.premier_loyer or 0) + D(mensualite or 0) * duree) if duree else None,
        )
        # Kilomètres autorisés par le contrat (à ce jour et projection en fin de contrat)
        if f.km_annuels:
            km_parcourus = max(vehicule.kilometrage_actuel - (vehicule.kilometrage_achat or 0), 0)
            autorises = int(f.km_annuels * ecoules / 12)
            depassement = max(km_parcourus - autorises, 0)
            prix_km = D(f.prix_km_supplementaire or 0)
            projection = int(km_parcourus / ecoules * duree) if ecoules and duree else None
            depassement_fin = max(projection - int(f.km_annuels * duree / 12), 0) if projection is not None else None
            res.update(
                km_autorises_a_ce_jour=autorises, km_parcourus=km_parcourus, depassement_km=depassement,
                cout_depassement=r2(prix_km * depassement) if prix_km else None,
                km_projetes_fin=projection, depassement_km_fin=depassement_fin,
                cout_depassement_fin=r2(prix_km * depassement_fin) if prix_km and depassement_fin is not None else None,
            )
    return res


def synthese(vehicule, aujourdhui=None):
    from .models import CategorieDepense, VenteParticulier
    aujourdhui = aujourdhui or date.today()
    # Véhicule vendu : les calculs s'arrêtent à la date de la vente (frais de vente compris)
    vente = VenteParticulier.objects.filter(vehicule=vehicule, statut="vendue").first()
    if vente:
        aujourdhui = min(aujourdhui, vente.date_vente)
    pleins, entretiens, documents, depenses = (vehicule.pleins.all(), vehicule.entretiens.all(),
                                                vehicule.documents.all(), vehicule.depenses.all())

    fin = financement(vehicule, aujourdhui)
    type_achat = fin["type_achat"] if fin else "comptant"
    proprietaire = type_achat in ("comptant", "pret") or bool(fin and fin.get("option_levee"))

    postes = OrderedDict()
    if type_achat in ("comptant", "pret") and vehicule.prix_achat is not None:
        postes["achat"] = {"libelle": str(_("Prix d'achat")), "montant": r2(D(vehicule.prix_achat))}
    if type_achat == "pret" and fin.get("interets_a_ce_jour"):
        postes["interets"] = {"libelle": str(_("Intérêts du prêt (à ce jour)")), "montant": fin["interets_a_ce_jour"]}
    if type_achat in ("leasing", "renting"):
        postes["loyers"] = {"libelle": str(_("Loyers payés (à ce jour)")), "montant": fin["loyers_a_ce_jour"]}
        if fin.get("option_levee") and fin.get("valeur_residuelle") is not None:
            postes["achat"] = {"libelle": str(_("Option d'achat levée")), "montant": fin["valeur_residuelle"]}
    postes["energie"] = {"libelle": str(_("Carburant / énergie")), "montant": _somme(pleins)}
    postes["entretiens"] = {"libelle": str(_("Entretiens et réparations")), "montant": _somme(entretiens)}
    pneus = vehicule.trains_pneus.filter(prix__isnull=False)
    if pneus.exists():
        postes["pneus"] = {"libelle": str(_("Pneus")), "montant": _somme(pneus, "prix")}
    maintenances = vehicule.maintenances.all()
    if maintenances.exists():
        postes["maintenances"] = {"libelle": str(_("Maintenances (garage)")),
                                  "montant": _somme(maintenances, "total_tvac")}
    postes["documents"] = {"libelle": str(_("Assurance, contrôle technique, documents")),
                           "montant": r2(sum((m for _j, m in paiements_documents(vehicule, aujourdhui)), ZERO))}
    if vente and vente.frais_vente:
        postes["frais_vente"] = {"libelle": str(_("Frais de vente")), "montant": r2(vente.frais_vente)}
    for code, libelle in CategorieDepense.choices:
        m = _somme(depenses.filter(categorie=code))
        if m:
            postes[f"depense_{code}"] = {"libelle": str(libelle), "montant": m}
    # Coût d'usage : tout sauf l'achat ; coût total : achat + usage ;
    # coût net : coût total − valeur de revente estimée (ce que le véhicule a réellement coûté)
    usage = r2(sum((p["montant"] for c, p in postes.items() if c not in ("achat", "interets", "loyers")), ZERO))
    total = r2(sum((p["montant"] for p in postes.values()), ZERO))
    # Leasing / renting sans option levée : le véhicule n'est pas à vous, pas de valeur de revente
    revente = (r2(D(vehicule.valeur_estimee))
               if vehicule.valeur_estimee is not None and proprietaire else None)
    net = r2(total - (revente or ZERO))

    km_actuel = vehicule.kilometrage_actuel
    # Kilomètres parcourus depuis l'achat (sans kilométrage d'achat : depuis le premier kilométrage saisi)
    depart = vehicule.kilometrage_depart
    km = max(km_actuel - depart, 0) if depart is not None else 0
    depreciation = (r2(D(vehicule.prix_achat) - D(vehicule.valeur_estimee or 0))
                    if vehicule.prix_achat is not None and vehicule.valeur_estimee is not None else None)
    debut = vehicule.date_achat or (fin["date_debut"] if fin else None)
    mois = mois_detention(debut, aujourdhui)

    # Par année (graphique)
    annees = {}
    lignes_annees = [(cle, jour, montant)
                     for qs, cle, champ in ((pleins, "energie", "montant"), (entretiens, "entretiens", "montant"),
                                            (vehicule.maintenances.all(), "entretiens", "total_tvac"),
                                            (depenses, "autres", "montant"))
                     for jour, montant in qs.values_list("date", champ)]
    lignes_annees += [("entretiens", jour, prix) for jour, prix in vehicule.trains_pneus.values_list("date_achat", "prix")]
    lignes_annees += [("documents", jour, montant) for jour, montant in paiements_documents(vehicule, aujourdhui)]
    for cle, jour, montant in lignes_annees:
        if jour and montant:
            a = annees.setdefault(jour.year, {"annee": jour.year, "energie": ZERO, "entretiens": ZERO,
                                              "documents": ZERO, "autres": ZERO})
            a[cle] = r2(a[cle] + D(montant))
    conso = consommation(vehicule)
    return {
        "postes": [dict(code=c, **p) for c, p in postes.items()],
        "cout_usage": usage,
        "depreciation": depreciation,
        "cout_total": total,
        "valeur_revente": revente,
        "cout_net": net,
        "kilometrage_actuel": km_actuel,
        "km_parcourus": km,
        "cout_km": (usage / km).quantize(D("0.001")) if km else None,
        # Coût au km et par mois : sur le coût net (achat + usage − revente)
        "cout_total_km": (net / km).quantize(D("0.001")) if km else None,
        "mois_detention": mois,
        "cout_mois": r2(net / mois) if mois else None,
        "consommation_moyenne": conso["moyenne"],
        "consommation_derniere": conso["derniere"],
        "consommation_unite": conso["unite"],
        # Hybride rechargeable : consommation électrique à part
        "consommation_electrique": (consommation(vehicule, "kWh")["moyenne"]
                                    if vehicule.energie == "phev" else None),
        "par_annee": [annees[a] for a in sorted(annees)],
        "type_achat": type_achat,
        "financement": fin,
    }


# ------------------------------------------------------------------
# Rapport : carburant, électricité, financement, coûts et kilomètres par mois
# ------------------------------------------------------------------
def periode_rapport(code, aujourdhui=None):
    """« 12m » (12 derniers mois, défaut), « annee » (année en cours), « tout », ou une année « 2025 »."""
    aujourdhui = aujourdhui or date.today()
    if code == "tout":
        return None, aujourdhui
    if code == "annee":
        return date(aujourdhui.year, 1, 1), aujourdhui
    if code and code.isdigit() and len(code) == 4:
        annee = int(code)
        return date(annee, 1, 1), min(date(annee, 12, 31), aujourdhui)
    return ajouter_mois(aujourdhui.replace(day=1), -11), aujourdhui


def _mois(d):
    return f"{d.year}-{d.month:02d}"


def _liste_mois(debut, fin):
    """Mois de debut à fin inclus : ['2025-12', '2026-01', …]"""
    mois, d = [], debut.replace(day=1)
    while d <= fin:
        mois.append(_mois(d))
        d = ajouter_mois(d, 1)
    return mois


def _bloc_maintenances(maintenances, mois):
    """Maintenances par un garage : pièces / main-d'œuvre (TVAC), par mois et par type."""
    par_mois = {m: {"mois": m, "pieces": ZERO, "main_oeuvre": ZERO} for m in mois}
    types = {}
    pieces = main_oeuvre = htva = tva = ZERO
    for m in maintenances:
        p, mo = D(m.total_pieces_tvac), D(m.total_main_oeuvre_tvac)
        pieces += p
        main_oeuvre += mo
        htva += D(m.total_htva)
        tva += D(m.total_tva)
        if _mois(m.date) in par_mois:
            par_mois[_mois(m.date)]["pieces"] += p
            par_mois[_mois(m.date)]["main_oeuvre"] += mo
        t = types.setdefault(m.type_maintenance, {"code": m.type_maintenance, "libelle": str(m.get_type_maintenance_display()),
                                                  "nombre": 0, "pieces": ZERO, "main_oeuvre": ZERO})
        t["nombre"] += 1
        t["pieces"] += p
        t["main_oeuvre"] += mo
    total = pieces + main_oeuvre
    return {
        "nombre": len(maintenances),
        "pieces": r2(pieces), "main_oeuvre": r2(main_oeuvre), "total": r2(total),
        "moyenne": r2(total / len(maintenances)) if maintenances else None,
        "total_htva": r2(htva), "total_tva": r2(tva),
        "part_pieces": (pieces / total * 100).quantize(D("0.1")) if total else None,
        "par_mois": [{"mois": v["mois"], "pieces": r2(v["pieces"]), "main_oeuvre": r2(v["main_oeuvre"])}
                     for v in par_mois.values()],
        "par_type": [{**t, "pieces": r2(t["pieces"]), "main_oeuvre": r2(t["main_oeuvre"]),
                      "total": r2(t["pieces"] + t["main_oeuvre"])}
                     for t in sorted(types.values(), key=lambda t: -(t["pieces"] + t["main_oeuvre"]))],
    }


def _bloc_entretiens(entretiens, mois):
    """Entretiens : nombre, total, pièces / main-d'œuvre (si détaillés), par mois et par type."""
    from .models import TypeEntretien
    libelles = dict(TypeEntretien.choices)
    par_mois = {m: {"mois": m, "pieces": ZERO, "main_oeuvre": ZERO, "non_detaille": ZERO} for m in mois}
    types = {}
    pieces = main_oeuvre = non_detaille = ZERO
    for e in entretiens:
        total = D(e.montant or 0)
        if e.pieces is not None or e.main_oeuvre is not None:
            p, mo, nd = D(e.pieces or 0), D(e.main_oeuvre or 0), ZERO
        else:
            p, mo, nd = ZERO, ZERO, total
        pieces, main_oeuvre, non_detaille = pieces + p, main_oeuvre + mo, non_detaille + nd
        pm = par_mois.get(_mois(e.date))
        if pm:
            pm["pieces"] += p
            pm["main_oeuvre"] += mo
            pm["non_detaille"] += nd
        t = types.setdefault(e.type, {"code": e.type, "libelle": str(libelles.get(e.type, e.type)), "nombre": 0,
                                      "pieces": ZERO, "main_oeuvre": ZERO, "total": ZERO})
        t["nombre"] += 1
        t["pieces"] += p
        t["main_oeuvre"] += mo
        t["total"] += total
    total = pieces + main_oeuvre + non_detaille
    n = len(entretiens)
    return {
        "nombre": n, "pieces": r2(pieces), "main_oeuvre": r2(main_oeuvre), "non_detaille": r2(non_detaille),
        "total": r2(total), "moyenne": r2(total / n) if n else None,
        "par_mois": [{k: (r2(v) if k != "mois" else v) for k, v in x.items()} for x in par_mois.values()],
        "par_type": [{**t, "pieces": r2(t["pieces"]), "main_oeuvre": r2(t["main_oeuvre"]), "total": r2(t["total"])}
                     for t in sorted(types.values(), key=lambda t: -t["total"])],
    }


def rapport(vehicule, code_periode=None, aujourdhui=None):
    from .models import CategorieDepense  # noqa: F401  (catégories des autres dépenses)
    aujourdhui = aujourdhui or date.today()
    debut, fin_periode = periode_rapport(code_periode, aujourdhui)

    pleins_tous = list(vehicule.pleins.all().order_by("date", "kilometrage"))
    if debut is None:
        dates = [p.date for p in pleins_tous] + [vehicule.date_achat]
        autres = [d for qs in (vehicule.entretiens.all(), vehicule.depenses.all(), vehicule.releves.all(),
                               vehicule.maintenances.all())
                  for d in qs.values_list("date", flat=True)]
        dates = [d for d in dates + autres if d]
        debut = min(dates).replace(day=1) if dates else aujourdhui.replace(day=1)
    dans = lambda d: d is not None and debut <= d <= fin_periode  # noqa: E731
    mois = _liste_mois(debut, fin_periode)
    vide = lambda: {m: ZERO for m in mois}  # noqa: E731

    # ---------------- Carburant (pleins) et électricité (recharges)
    def bloc(pleins):
        par_mois = {m: {"mois": m, "quantite": ZERO, "montant": ZERO} for m in mois}
        total_q = total_m = tva = ZERO
        groupes = {}
        pays = {}
        for p in pleins:
            q, m = D(p.quantite), D(p.montant)
            total_q += q
            total_m += m
            tva += D(p.montant_tva or 0)
            pm = par_mois[_mois(p.date)]
            pm["quantite"] += q
            pm["montant"] += m
            g = groupes.setdefault(p.lieu_recharge if p.carburant == "electricite" else p.carburant,
                                   {"quantite": ZERO, "montant": ZERO, "nombre": 0})
            g["quantite"] += q
            g["montant"] += m
            g["nombre"] += 1
            if p.pays:
                pa = pays.setdefault(p.pays, {"pays": p.pays, "montant": ZERO, "tva": ZERO, "quantite": ZERO})
                pa["montant"] += m
                pa["quantite"] += q
                pa["tva"] += D(p.montant_tva or 0)
        for pm in par_mois.values():
            pm["prix_moyen"] = (pm["montant"] / pm["quantite"]).quantize(D("0.001")) if pm["quantite"] else None
            pm["quantite"], pm["montant"] = r2(pm["quantite"]), r2(pm["montant"])
        return {
            "nombre": len(pleins),
            "total_quantite": r2(total_q),
            "total_montant": r2(total_m),
            "total_tva": r2(tva),
            "prix_moyen": (total_m / total_q).quantize(D("0.001")) if total_q else None,
            "par_type": [{"code": c or "", "quantite": r2(g["quantite"]), "montant": r2(g["montant"]),
                          "nombre": g["nombre"]} for c, g in sorted(groupes.items(), key=lambda kv: -kv[1]["montant"])],
            "par_pays": [{**pa, "montant": r2(pa["montant"]), "tva": r2(pa["tva"]), "quantite": r2(pa["quantite"])}
                         for pa in sorted(pays.values(), key=lambda x: -x["montant"])],
            "par_mois": list(par_mois.values()),
        }

    periode_pleins = [p for p in pleins_tous if dans(p.date)]
    carburant = bloc([p for p in periode_pleins if p.carburant != "electricite"])
    electricite = bloc([p for p in periode_pleins if p.carburant == "electricite"])
    # Consommation (plein à plein) des mesures de la période
    unite_carburant = famille_principale(vehicule) if famille_principale(vehicule) != "kWh" else "L"
    for cle_bloc, unite in ((carburant, unite_carburant), (electricite, "kWh")):
        c = consommation(vehicule, unite)
        mesures = [m for m in c["mesures"] if dans(m["date"])]
        q = sum((m["quantite"] for m in mesures), ZERO)
        k = sum(m["km"] for m in mesures)
        cle_bloc["consommation_moyenne"] = (q / k * 100).quantize(D("0.01")) if k else None
        cle_bloc["consommation_unite"] = c["unite"]
        cle_bloc["consommation_mesures"] = [{"date": m["date"], "conso": m["conso"]} for m in mesures]

    # ---------------- Financement : payé, reste à payer, échéancier
    fin = financement(vehicule, aujourdhui)
    echeancier = []
    if fin and fin.get("date_debut") and fin.get("duree_mois") and fin.get("mensualite"):
        mensualite = D(fin["mensualite"])
        initial = D(fin.get("paye_a_ce_jour") or 0) - mensualite * fin["mois_payes"]   # apport / premier loyer
        total = initial + mensualite * fin["duree_mois"]
        for n in range(0, fin["duree_mois"] + 1, max(1, fin["duree_mois"] // 24)):
            paye = initial + mensualite * n
            echeancier.append({"date": ajouter_mois(fin["date_debut"], n), "paye": r2(paye), "reste": r2(total - paye)})

    # ---------------- Coûts par mois (énergie, entretiens, documents, autres, financement)
    couts = {cle: vide() for cle in ("energie", "electricite", "entretiens", "documents", "autres", "financement")}
    for p in periode_pleins:
        couts["electricite" if p.carburant == "electricite" else "energie"][_mois(p.date)] += D(p.montant)
    for cle, qs, champ, champ_montant in (
            ("entretiens", vehicule.entretiens.all(), "date", "montant"),
            ("entretiens", vehicule.maintenances.all(), "date", "total_tvac"),
            ("entretiens", vehicule.trains_pneus.all(), "date_achat", "prix"),
            ("autres", vehicule.depenses.all(), "date", "montant")):
        for jour, montant in qs.values_list(champ, champ_montant):
            if dans(jour) and montant:
                couts[cle][_mois(jour)] += D(montant)
    # Documents (assurance) : prime mensuelle chaque mois, sinon le montant à la date de début
    for jour, montant in paiements_documents(vehicule, aujourdhui):
        if dans(jour) and montant:
            couts["documents"][_mois(jour)] += D(montant)
    if fin and fin.get("date_debut") and fin.get("mensualite"):
        for n in range(fin["duree_mois"] or 0):
            jour = ajouter_mois(fin["date_debut"], n + 1)
            if dans(jour) and jour <= aujourdhui:
                couts["financement"][_mois(jour)] += D(fin["mensualite"])
    couts_par_mois = [{"mois": m, **{cle: r2(couts[cle][m]) for cle in couts}} for m in mois]
    for c in couts_par_mois:
        c["total"] = r2(sum((c[cle] for cle in couts), ZERO))
    totaux = {cle: r2(sum(couts[cle].values(), ZERO)) for cle in couts}
    total_periode = r2(sum(totaux.values(), ZERO))

    # ---------------- Kilomètres par mois (plus haut kilométrage connu à la fin de chaque mois)
    releves = sorted([(d, k) for qs in (vehicule.releves.all(), vehicule.pleins.all(), vehicule.entretiens.all(),
                                        vehicule.maintenances.all())
                      for d, k in qs.values_list("date", "kilometrage") if d and k])
    km_par_mois, precedent = [], None
    depart = vehicule.kilometrage_depart
    for m in mois:
        connus = [k for d, k in releves if _mois(d) <= m]
        km_fin = max(connus) if connus else depart
        if precedent is None:
            avant = [k for d, k in releves if _mois(d) < mois[0]]
            precedent = max(avant) if avant else (depart if depart is not None else km_fin)
        km_par_mois.append({"mois": m, "km": max((km_fin or 0) - (precedent or 0), 0)})
        precedent = km_fin if km_fin is not None else precedent
    km_periode = sum(x["km"] for x in km_par_mois)

    return {
        "periode": {"code": code_periode or "12m", "debut": debut, "fin": fin_periode, "mois": len(mois)},
        "carburant": carburant,
        "electricite": electricite,
        "financement": fin,
        "echeancier": echeancier,
        "couts": {"par_mois": couts_par_mois, "totaux": totaux, "total": total_periode,
                  "moyenne_mois": r2(total_periode / len(mois)) if mois else None,
                  "cout_km": (total_periode / km_periode).quantize(D("0.001")) if km_periode else None},
        "maintenances": _bloc_maintenances([m for m in vehicule.maintenances.all() if dans(m.date)], mois),
        "entretiens": _bloc_entretiens([e for e in vehicule.entretiens.all() if dans(e.date)], mois),
        "kilometres": {"par_mois": km_par_mois, "total": km_periode,
                       "moyenne_mois": round(km_periode / len(mois)) if mois else None},
    }


# ==================================================================
# PNEUS : nombre de trains par type (été, hiver, slick…) et statistiques
# ==================================================================
def statistiques_pneus(trains, aujourd_hui=None):
    """Statistiques des trains de pneus (un train = les pneus d'un essieu).

    Par type (été, hiver, 4 saisons, pluie, semi-slick, slick) et au total : nombre de trains (en service,
    montés, remplacés), kilomètres parcourus, coût, coût aux 1 000 km, kilométrage et durée moyens avant
    remplacement ; par essieu et par marque.
    """
    from .models import TrainPneus
    aujourd_hui = aujourd_hui or date.today()

    def vide():
        return {"trains": 0, "en_service": 0, "montes": 0, "remplaces": 0, "km": 0, "cout": D(0),
                "km_trains_prix": 0, "_km_remplaces": [], "_jours_remplaces": []}

    def ajouter(acc, t, km):
        acc["trains"] += 1
        acc["en_service"] += 1 if t.actif else 0
        acc["montes"] += 1 if (t.actif and t.est_monte) else 0
        acc["remplaces"] += 0 if t.actif else 1
        acc["km"] += km
        if t.prix is not None:
            acc["cout"] += D(t.prix)
            acc["km_trains_prix"] += km
        if not t.actif:
            acc["_km_remplaces"].append(km)
            debut = t.date_achat or t.date_montage
            if debut and t.date_remplacement:
                acc["_jours_remplaces"].append((t.date_remplacement - debut).days)

    def finaliser(acc):
        kms, jours = acc.pop("_km_remplaces"), acc.pop("_jours_remplaces")
        km_prix = acc.pop("km_trains_prix")
        acc["cout"] = r2(acc["cout"])
        # Coût aux 1 000 km : seulement les trains dont le prix est connu
        acc["cout_1000_km"] = r2(acc["cout"] * 1000 / km_prix) if km_prix and acc["cout"] else None
        acc["km_moyen_remplacement"] = round(sum(kms) / len(kms)) if kms else None
        acc["duree_moyenne_mois"] = round(sum(jours) / len(jours) / 30.44, 1) if jours else None
        return acc

    par_type, par_position, par_marque, total = {}, {}, {}, vide()
    for t in trains:
        km = t.km_effectues()
        ajouter(total, t, km)
        ajouter(par_type.setdefault(t.type_pneus, vide()), t, km)
        ajouter(par_position.setdefault(t.position, vide()), t, km)
        marque = (t.marque or "").strip().title() or "—"
        ajouter(par_marque.setdefault(marque, vide()), t, km)

    libelles = dict(TrainPneus.TypePneus.choices)
    return {
        "total": finaliser(total),
        # Tous les types, même à zéro, dans l'ordre du modèle (été, hiver, 4 saisons, pluie, semi-slick, slick)
        "par_type": [{"type": code, "libelle": str(libelles[code]), **finaliser(par_type.get(code, vide()))}
                     for code in libelles],
        "par_position": [{"position": code, "libelle": str(lib), **finaliser(par_position.get(code, vide()))}
                         for code, lib in TrainPneus.Position.choices],
        "par_marque": sorted(({"marque": m, **finaliser(a)} for m, a in par_marque.items()),
                             key=lambda x: (-x["trains"], x["marque"])),
    }

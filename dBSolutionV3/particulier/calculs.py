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
def consommation(vehicule):
    """
    Consommation entre deux pleins complets : quantités ajoutées depuis le plein complet précédent
    (pleins partiels compris) ÷ kilomètres parcourus × 100. Unité : L/100 km ou kWh/100 km.
    """
    pleins = sorted(vehicule.pleins.all(), key=lambda p: (p.kilometrage, p.date))
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
    for rappel in entretien.vehicule.rappels.filter(actif=True, type_entretien=entretien.type, document__isnull=True):
        faits.append(marquer_fait(rappel, entretien.date, entretien.kilometrage))
    return faits


# ------------------------------------------------------------------
# Coûts et rentabilité
# ------------------------------------------------------------------
def _somme(qs, champ="montant"):
    return r2(qs.aggregate(s=Sum(champ))["s"])


def synthese(vehicule, aujourdhui=None):
    from .models import CategorieDepense
    aujourdhui = aujourdhui or date.today()
    pleins, entretiens, documents, depenses = (vehicule.pleins.all(), vehicule.entretiens.all(),
                                                vehicule.documents.all(), vehicule.depenses.all())

    postes = OrderedDict()
    if vehicule.prix_achat is not None:
        postes["achat"] = {"libelle": str(_("Prix d'achat")), "montant": r2(D(vehicule.prix_achat))}
    postes["energie"] = {"libelle": str(_("Carburant / énergie")), "montant": _somme(pleins)}
    postes["entretiens"] = {"libelle": str(_("Entretiens et réparations")), "montant": _somme(entretiens)}
    postes["documents"] = {"libelle": str(_("Assurance, contrôle technique, documents")), "montant": _somme(documents)}
    for code, libelle in CategorieDepense.choices:
        m = _somme(depenses.filter(categorie=code))
        if m:
            postes[f"depense_{code}"] = {"libelle": str(libelle), "montant": m}
    # Coût d'usage : tout sauf l'achat ; coût total : achat + usage ;
    # coût net : coût total − valeur de revente estimée (ce que le véhicule a réellement coûté)
    usage = r2(sum((p["montant"] for c, p in postes.items() if c != "achat"), ZERO))
    total = r2(sum((p["montant"] for p in postes.values()), ZERO))
    revente = r2(D(vehicule.valeur_estimee)) if vehicule.valeur_estimee is not None else None
    net = r2(total - (revente or ZERO))

    km_actuel = vehicule.kilometrage_actuel
    km = max(km_actuel - (vehicule.kilometrage_achat or 0), 0)
    depreciation = (r2(D(vehicule.prix_achat) - D(vehicule.valeur_estimee or 0))
                    if vehicule.prix_achat is not None and vehicule.valeur_estimee is not None else None)
    mois = mois_entre(vehicule.date_achat, aujourdhui) if vehicule.date_achat else None

    # Par année (graphique)
    annees = {}
    for qs, cle in ((pleins, "energie"), (entretiens, "entretiens"), (documents, "documents"), (depenses, "autres")):
        champ_date = "date_debut" if cle == "documents" else "date"
        for jour, montant in qs.values_list(champ_date, "montant"):
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
        "par_annee": [annees[a] for a in sorted(annees)],
    }

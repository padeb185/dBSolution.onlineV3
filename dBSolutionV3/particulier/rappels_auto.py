"""
Plan d'entretien d'un véhicule : rappels automatiques d'entretien, de contrôle technique et d'assurance.

Entretien (« le premier des deux ») :
  - service normal : tous les ans ; Long Life : tous les 2 ans ;
  - kilométrage : moteur thermique / hybride 15 000, 20 000, 25 000 ou 30 000 km ;
    électrique 20 000, 30 000 ou 40 000 km (ou sans kilométrage : la date seule).
  Point de départ : le dernier entretien encodé (révision / vidange, ou maintenance « Entretien » / « Check-up »),
  sinon l'achat, sinon aujourd'hui et le kilométrage actuel.
Contrôle technique : règle du pays d'immatriculation (premier contrôle après N ans, puis tous les M ans,
  puis tous les ans à partir d'un âge) ; point de départ : le dernier contrôle encodé, sinon la mise en circulation.
Assurance : l'échéance du document « Assurance » (son rappel est créé avec le document).
Règles indicatives (2026) : les échéances restent modifiables dans l'onglet Rappels.
"""
from datetime import date

from django.utils.translation import gettext_lazy as _

from .calculs import ajouter_mois, statut_rappel

KM_THERMIQUE = [15000, 20000, 25000, 30000]
KM_ELECTRIQUE = [20000, 30000, 40000]
TYPES_ENTRETIEN_PERIODIQUE = ("revision", "vidange")
TYPES_MAINTENANCE_PERIODIQUE = ("entretien", "checkup")

# pays : (premier contrôle après N ans, puis tous les M ans, annuel à partir de X ans ou None)
CONTROLE_TECHNIQUE = {
    "BE": (4, 1, None), "FR": (4, 2, None), "LU": (4, 2, 6), "NL": (4, 2, 8), "DE": (3, 2, None),
    "AT": (3, 2, 5), "IT": (4, 2, None), "ES": (4, 2, 10), "PT": (4, 2, 8), "IE": (4, 2, 10),
    "PL": (3, 2, 5), "CH": (5, 3, None), "GB": (3, 1, None), "DK": (4, 2, None), "SE": (3, 2, 5),
    "FI": (3, 2, 5), "NO": (4, 2, None), "CZ": (4, 2, None), "SK": (4, 2, None), "HU": (4, 2, None),
    "SI": (4, 2, 7), "HR": (2, 1, None), "RO": (3, 2, 12), "BG": (3, 2, 5), "GR": (4, 2, None),
    "CY": (4, 2, None), "MT": (4, 2, None), "EE": (4, 2, 10), "LV": (3, 2, None), "LT": (3, 2, None),
}


def est_electrique(vehicule):
    return vehicule.energie == "electrique"


def options_km(vehicule):
    return KM_ELECTRIQUE if est_electrique(vehicule) else KM_THERMIQUE


def km_par_defaut(vehicule, long_life):
    if est_electrique(vehicule):
        return 30000
    return 30000 if long_life else (20000 if vehicule.energie == "diesel" else 15000)


# ------------------------------------------------------------------ Entretien
def dernier_entretien(vehicule):
    """(date, km, libellé) du dernier entretien périodique encodé, sinon de l'achat, sinon d'aujourd'hui."""
    candidats = [(e.date, e.kilometrage, str(e.get_type_display()))
                 for e in vehicule.entretiens.filter(type__in=TYPES_ENTRETIEN_PERIODIQUE)]
    candidats += [(m.date, m.kilometrage, str(m.get_type_maintenance_display()))
                  for m in vehicule.maintenances.filter(type_maintenance__in=TYPES_MAINTENANCE_PERIODIQUE)]
    if candidats:
        jour, km, libelle = max(candidats, key=lambda c: (c[0], c[1] or 0))
        return {"date": jour, "km": km, "source": "entretien", "libelle": libelle}
    if vehicule.date_achat:
        return {"date": vehicule.date_achat, "km": vehicule.kilometrage_achat, "source": "achat", "libelle": ""}
    return {"date": date.today(), "km": vehicule.kilometrage_actuel, "source": "aujourdhui", "libelle": ""}


def echeances_entretien(vehicule, intervalle_mois, intervalle_km):
    base = dernier_entretien(vehicule)
    return base, {
        "echeance_date": ajouter_mois(base["date"], intervalle_mois) if intervalle_mois else None,
        "echeance_km": (base["km"] + intervalle_km) if intervalle_km and base["km"] is not None else None,
    }


# ------------------------------------------------------------------ Contrôle technique
def regle_ct(vehicule):
    return CONTROLE_TECHNIQUE.get((vehicule.pays_immatriculation or "").upper())


def periode_ct(regle, age_ans):
    """Mois avant le contrôle suivant, selon l'âge du véhicule au dernier contrôle."""
    _premier, periode, annuel = regle
    return 12 if annuel is not None and age_ans >= annuel else periode * 12


def dernier_ct(vehicule):
    dates = [d for d in vehicule.documents.filter(type="controle_technique").values_list("date_debut", flat=True) if d]
    dates += list(vehicule.entretiens.filter(type="controle_technique").values_list("date", flat=True))
    return max(dates) if dates else None


def prochain_ct(vehicule):
    """(échéance, source) du prochain contrôle technique, ou (None, raison)."""
    regle = regle_ct(vehicule)
    if regle is None:
        return None, "pays"
    mise_en_circulation = vehicule.date_mise_en_circulation or (
        date(vehicule.annee, 1, 1) if vehicule.annee else None)
    dernier = dernier_ct(vehicule)
    if dernier:
        age = (dernier - mise_en_circulation).days // 365 if mise_en_circulation else regle[0]
        return ajouter_mois(dernier, periode_ct(regle, age)), "dernier_controle"
    if mise_en_circulation:
        echeance = ajouter_mois(mise_en_circulation, regle[0] * 12)
        while echeance < date.today():       # contrôles passés non encodés : prochaine échéance théorique
            age = (echeance - mise_en_circulation).days // 365
            echeance = ajouter_mois(echeance, periode_ct(regle, age))
        return echeance, "mise_en_circulation"
    return None, "mise_en_circulation_inconnue"


def _ct_par_document(vehicule):
    return vehicule.documents.filter(type="controle_technique", date_expiration__gte=date.today()).exists()


# ------------------------------------------------------------------ Plan complet
def _rappel(vehicule, code):
    return vehicule.rappels.filter(code=code).first()


def _statut(rappel, vehicule):
    if rappel is None:
        return None
    return {"id": rappel.pk, "libelle": rappel.libelle, "echeance_date": rappel.echeance_date,
            "echeance_km": rappel.echeance_km, "intervalle_mois": rappel.intervalle_mois,
            "intervalle_km": rappel.intervalle_km, "actif": rappel.actif,
            "statut": statut_rappel(rappel, vehicule.kilometrage_actuel)}


def assurance(vehicule):
    doc = vehicule.documents.filter(type="assurance", date_expiration__isnull=False).order_by("-date_expiration").first()
    if doc is None:
        return None
    jours = (doc.date_expiration - date.today()).days
    return {"document": doc.pk, "titre": doc.titre or doc.organisme, "organisme": doc.organisme,
            "date_expiration": doc.date_expiration, "jours_restants": jours,
            "mode_paiement": doc.mode_paiement, "montant": doc.montant}


def plan(vehicule):
    rappel_e = _rappel(vehicule, "entretien")
    long_life = bool(rappel_e and (rappel_e.intervalle_mois or 12) >= 24)
    intervalle_km = rappel_e.intervalle_km if rappel_e else km_par_defaut(vehicule, long_life)
    base, proposition = echeances_entretien(vehicule, 24 if long_life else 12, intervalle_km)
    ct, source_ct = prochain_ct(vehicule)
    regle = regle_ct(vehicule)
    doc_ct = vehicule.documents.filter(type="controle_technique", date_expiration__gte=date.today()).first()
    return {
        "electrique": est_electrique(vehicule),
        "entretien": {
            "rappel": _statut(rappel_e, vehicule),
            "long_life": long_life,
            "intervalle_km": intervalle_km,
            "options_km": options_km(vehicule),
            "base": base,
            "proposition": proposition,
        },
        "controle_technique": {
            "rappel": _statut(_rappel(vehicule, "controle_technique"), vehicule),
            "regle": {"premier": regle[0], "periode": regle[1], "annuel_a_partir_de": regle[2]} if regle else None,
            "echeance": ct,
            "source": source_ct,
            "document_echeance": doc_ct.date_expiration if doc_ct else None,
        },
        "assurance": assurance(vehicule),
    }


def appliquer(vehicule, entretien=None, controle_technique=None):
    """entretien : {"actif", "long_life", "intervalle_km"} ; controle_technique : {"actif"}."""
    from .models import Rappel
    if entretien is not None:
        rappel = _rappel(vehicule, "entretien")
        if not entretien.get("actif", True):
            if rappel:
                rappel.delete()
        else:
            mois = 24 if entretien.get("long_life") else 12
            km = entretien.get("intervalle_km")
            km = int(km) if km not in (None, "", 0, "0") else None
            _base, ech = echeances_entretien(vehicule, mois, km)
            rappel = rappel or Rappel(vehicule=vehicule, code="entretien")
            rappel.libelle = str(_("Entretien périodique (Long Life)") if mois == 24 else _("Entretien périodique"))
            rappel.type_entretien = "revision"
            rappel.intervalle_mois, rappel.intervalle_km = mois, km
            rappel.echeance_date, rappel.echeance_km = ech["echeance_date"], ech["echeance_km"]
            rappel.actif = True
            rappel.save()
    if controle_technique is not None:
        rappel = _rappel(vehicule, "controle_technique")
        echeance, _source = prochain_ct(vehicule)
        # Certificat de contrôle avec date d'expiration : son propre rappel suffit (pas de doublon)
        if not controle_technique.get("actif", True) or echeance is None or _ct_par_document(vehicule):
            if rappel:
                rappel.delete()
        else:
            regle = regle_ct(vehicule)
            rappel = rappel or Rappel(vehicule=vehicule, code="controle_technique")
            rappel.libelle = str(_("Contrôle technique"))
            rappel.type_entretien = "controle_technique"
            rappel.echeance_date, rappel.echeance_km = echeance, None
            rappel.intervalle_mois = regle[1] * 12 if regle else None
            rappel.intervalle_km = None
            rappel.actif = True
            rappel.save()
    return plan(vehicule)


def apres_entretien(vehicule, jour, km, type_entretien=None, type_maintenance=None):
    """Entretien ou contrôle encodé : les rappels automatiques repartent de cette date / ce kilométrage."""
    from .calculs import marquer_fait
    if type_entretien in TYPES_ENTRETIEN_PERIODIQUE or type_maintenance in TYPES_MAINTENANCE_PERIODIQUE:
        rappel = _rappel(vehicule, "entretien")
        if rappel:
            marquer_fait(rappel, jour, km)
    if type_entretien == "controle_technique":
        rappel = _rappel(vehicule, "controle_technique")
        if rappel:
            echeance, _s = prochain_ct(vehicule)
            if echeance is None or _ct_par_document(vehicule):
                rappel.delete()
            else:
                rappel.echeance_date, rappel.actif = echeance, True
                rappel.save()

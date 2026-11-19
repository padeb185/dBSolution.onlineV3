"""
Charges des véhicules dans le journal général (PCMN belge, comptes « frais de véhicules » 6127xx) :
- énergie : carburants 612700, recharges électriques 612710, AdBlue 612720 (fuel.totaux_energie) ;
- maintenances confiées à un garage externe (garage officiel) 612730 ;
- carrosserie externe 612740 (part prise en charge par l'assurance : créance 416000 / produit 740000) ;
- primes d'assurance des véhicules 612750 (pas de TVA), à chaque échéance mensuelle ou annuelle.

Chaque fonction renvoie des lignes {journal, date, piece, compte, intitule, libelle, debit, credit}.
"""
import calendar
from datetime import date
from decimal import Decimal

from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop

ZERO = Decimal("0.00")
R2 = Decimal("0.01")

COMPTE_MAINTENANCE_EXTERNE = "612730"
COMPTE_CARROSSERIE = "612740"
COMPTE_ASSURANCE = "612750"
COMPTE_TVA_DEDUCTIBLE = "411000"
COMPTE_CREANCE_ASSURANCE = "416000"
COMPTE_FOURNISSEURS = "440000"
COMPTE_BANQUE = "550000"
COMPTE_INDEMNITES_ASSURANCE = "740000"

INTITULES = {
    "612700": gettext_noop("Carburants véhicules"),
    "612710": gettext_noop("Recharges électriques véhicules"),
    "612720": gettext_noop("AdBlue"),
    COMPTE_MAINTENANCE_EXTERNE: gettext_noop("Entretien et réparations véhicules – garages externes"),
    COMPTE_CARROSSERIE: gettext_noop("Carrosserie véhicules – carrossiers externes"),
    COMPTE_ASSURANCE: gettext_noop("Assurances véhicules"),
    COMPTE_CREANCE_ASSURANCE: gettext_noop("Créances diverses – indemnités d'assurance à recevoir"),
    COMPTE_INDEMNITES_ASSURANCE: gettext_noop("Indemnités d'assurance (sinistres)"),
}


def _r(x):
    return Decimal(x or 0).quantize(R2)


def _ligne(L, journal, jour, piece, compte, libelle, debit=ZERO, credit=ZERO, intitule=None):
    debit, credit = _r(debit), _r(credit)
    if debit or credit:
        L.append({"journal": journal, "date": jour, "piece": piece, "compte": compte,
                  "intitule": intitule if intitule is not None else _(INTITULES.get(compte, "")),
                  "libelle": libelle, "debit": debit, "credit": credit})


def _immat(obj):
    return getattr(getattr(obj, "voiture_exemplaire", None), "immatriculation", "") or ""


# ------------------------------------------------------------------ énergie
def ecritures_energie(societe, debut=None, fin=None):
    from fuel import totaux_energie as te
    L = []
    for o in te.operations_entre(societe, debut, fin):
        for l in te.ecritures(o):
            L.append(dict(l, journal="ACH", date=o["date"], piece=o["piece"]))
    return L


# ------------------------------------------------------------------ garages externes
def _facture_fournisseur(L, obj, jour, piece, compte, libelle, nom_fournisseur):
    lib = f"{libelle} – {nom_fournisseur}".strip(" –")
    _ligne(L, "ACH", jour, piece, compte, lib, debit=obj.total_htva)
    _ligne(L, "ACH", jour, piece, COMPTE_TVA_DEDUCTIBLE, lib, debit=obj.total_tva, intitule=_("TVA à récupérer"))
    _ligne(L, "ACH", jour, piece, COMPTE_FOURNISSEURS, lib, credit=obj.total_tvac, intitule=_("Fournisseurs"))
    return lib


def ecritures_maintenances_externes(societe, debut=None, fin=None):
    from maintenance.maintenance_externe.models import MaintenanceExterne
    L = []
    for m in MaintenanceExterne.objects.filter(societe=societe).select_related("garage", "voiture_exemplaire"):
        piece = m.numero_facture or f"MEXT-{str(m.pk)[:8]}"
        lib = _facture_fournisseur(L, m, m.date_facture, piece, COMPTE_MAINTENANCE_EXTERNE, m.libelle_facture,
                                   getattr(m.garage, "nom", ""))
        if m.date_paiement:
            _ligne(L, "BQ", m.date_paiement, piece, COMPTE_FOURNISSEURS, lib, debit=m.total_tvac, intitule=_("Fournisseurs"))
            _ligne(L, "BQ", m.date_paiement, piece, COMPTE_BANQUE, lib, credit=m.total_tvac,
                   intitule=_("Banque – compte courant"))
    return [l for l in L if _dans(l["date"], debut, fin)]


def ecritures_carrosseries(societe, debut=None, fin=None):
    """
    Facture du carrossier : charge HTVA, TVA déductible, dette fournisseur TVAC.
    Prise en charge par l'assurance : créance sur l'assureur (416000) et produit (740000) ;
    si l'assureur paie directement le carrossier, la créance est compensée avec la dette (440000).
    Paiement : montant réellement payé au carrossier.
    """
    from maintenance.maintenance_externe.models import CarrosserieExterne
    L = []
    for c in CarrosserieExterne.objects.filter(societe=societe, facture_date__isnull=False).select_related(
            "carrossier", "voiture_exemplaire"):
        piece = c.facture_numero or f"CARR-{str(c.pk)[:8]}"
        jour = c.facture_date
        lib = _facture_fournisseur(L, c, jour, piece, COMPTE_CARROSSERIE, c.libelle_facture,
                                   str(c.carrossier or ""))
        indemnite = min(_r(c.montant_assurance), _r(c.total_tvac)) if c.prise_en_charge_assurance else ZERO
        if indemnite:
            lib_ass = f"{_('Prise en charge assurance')} – {lib}"
            _ligne(L, "OD", jour, piece, COMPTE_CREANCE_ASSURANCE, lib_ass, debit=indemnite)
            _ligne(L, "OD", jour, piece, COMPTE_INDEMNITES_ASSURANCE, lib_ass, credit=indemnite)
            if c.assurance_paie_carrossier:
                _ligne(L, "OD", jour, piece, COMPTE_FOURNISSEURS, lib_ass, debit=indemnite, intitule=_("Fournisseurs"))
                _ligne(L, "OD", jour, piece, COMPTE_CREANCE_ASSURANCE, lib_ass, credit=indemnite)
        if c.date_paiement and c.montant_a_payer:
            _ligne(L, "BQ", c.date_paiement, piece, COMPTE_FOURNISSEURS, lib, debit=c.montant_a_payer,
                   intitule=_("Fournisseurs"))
            _ligne(L, "BQ", c.date_paiement, piece, COMPTE_BANQUE, lib, credit=c.montant_a_payer,
                   intitule=_("Banque – compte courant"))
    return [l for l in L if _dans(l["date"], debut, fin)]


# ------------------------------------------------------------------ assurances
def _ajouter_mois(d, n):
    m = d.month - 1 + n
    a, m = d.year + m // 12, m % 12 + 1
    return date(a, m, min(d.day, calendar.monthrange(a, m)[1]))


def echeances_police(p, jusqu_au):
    """(date, montant) des primes échues de la police jusqu'à la date donnée (incluse)."""
    if not p.date_debut:
        return []
    mensuel = p.frequence_paiement == "mensuel"
    if mensuel:
        montant = p.prime_mensuelle if p.prime_mensuelle else (p.prime_annuelle / 12 if p.prime_annuelle else None)
    else:
        montant = p.prime_annuelle if p.prime_annuelle else (p.prime_mensuelle * 12 if p.prime_mensuelle else None)
    if not montant:
        return []
    fin = min(d for d in (jusqu_au, p.date_fin) if d is not None)
    if not p.actif and p.updated_at:
        fin = min(fin, timezone.localtime(p.updated_at).date())     # police clôturée sans date de fin
    pas = 1 if mensuel else 12
    echeances, i = [], 0
    while True:
        jour = _ajouter_mois(p.date_debut, i * pas)
        if jour > fin:
            break
        echeances.append((jour, _r(montant)))
        i += 1
    return echeances


def ecritures_assurances(societe, debut=None, fin=None):
    """Primes échues (jamais au-delà d'aujourd'hui) : charge 612750 / banque 550000 (domiciliation, virement…)."""
    from assurance_police.models import AssurancePolice
    jusqu_au = min(d for d in (fin, timezone.localdate()) if d is not None)
    L = []
    for p in AssurancePolice.objects.filter(societe=societe).select_related("assurance", "voiture_exemplaire"):
        compagnie = getattr(p.assurance, "nom_compagnie", "") or ""
        lib = f"{_('Prime')} {p.get_type_couverture_display()} – {_immat(p)} – {compagnie} {p.numero_contrat}".strip()
        for jour, montant in echeances_police(p, jusqu_au):
            if not _dans(jour, debut, fin):
                continue
            piece = f"ASS-{p.numero_contrat}-{jour:%Y%m}"
            journal = "CAI" if p.mode_paiement == "cash" else "BQ"
            compte_tresorerie = "570000" if p.mode_paiement == "cash" else COMPTE_BANQUE
            _ligne(L, journal, jour, piece, COMPTE_ASSURANCE, lib, debit=montant)
            _ligne(L, journal, jour, piece, compte_tresorerie, lib, credit=montant,
                   intitule=_("Caisse") if p.mode_paiement == "cash" else _("Banque – compte courant"))
    return L


def _dans(jour, debut, fin):
    return jour is not None and (debut is None or jour >= debut) and (fin is None or jour <= fin)

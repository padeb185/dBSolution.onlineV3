"""
Locations réalisées mais pas encore facturées : produits à recevoir (factures à établir).

Principe (comptabilité d'engagement) :
  - à la fin de la location (fait générateur), si aucune facture n'est encore émise :
        404000 Produits à recevoir (factures à établir)   débit   (HTVA)
        700300 Chiffre d'affaires – locations                crédit
  - à l'émission de la facture : écriture inverse (extourne), datée de la facture.
    La facture passe ensuite normalement en 400000 Clients / 700300 / 451000.

Sur une période qui contient les deux dates, les écritures s'annulent ; à une date de bilan située entre la fin
de la location et sa facture, le montant reste en 404000 et apparaît dans les créances commerciales.
Pas de TVA à ce stade : elle n'est due qu'à la facturation.
"""
from decimal import Decimal

from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop

ZERO = Decimal("0.00")
COMPTE_PRODUITS_A_RECEVOIR = "404000"
COMPTE_CA_LOCATIONS = "700300"
INTITULES = {
    COMPTE_PRODUITS_A_RECEVOIR: gettext_noop("Produits à recevoir – factures à établir"),
    COMPTE_CA_LOCATIONS: gettext_noop("Chiffre d'affaires – locations"),
}


def _locations(societe):
    from voiture.voiture_location.models import Location
    return (Location.objects.filter(societe=societe)
            .select_related("voiture_exemplaire", "client", "societe_cliente", "client_pilotage__client_particulier",
                            "societe")
            .prefetch_related("boxes", "factures__lines"))


def a_facturer(societe, au=None):
    """
    Locations terminées au plus tard à la date « au » (aujourd'hui par défaut) et sans facture émise à cette date :
    [{"location", "date", "montant_htva", "montant_tvac", "jours"}], la plus ancienne d'abord.
    """
    au = au or timezone.localdate()
    resultat = []
    for loc in _locations(societe):
        jour = loc.date_fait_generateur
        if jour is None or jour > au:
            continue
        f = loc.facture_emise
        if f is not None and (f.client_est_societe or f.issue_date <= au):
            continue
        montant = Decimal(loc.prix_htva or 0)
        if montant <= 0:
            continue
        resultat.append({"location": loc, "date": jour, "montant_htva": montant,
                         "montant_tvac": Decimal(loc.prix_tvac or 0), "jours": (au - jour).days})
    resultat.sort(key=lambda r: r["date"])
    return resultat


def ecritures(societe, debut=None, fin=None):
    """Écritures OD « factures à établir » et leurs extournes, filtrées sur la période."""
    aujourdhui = timezone.localdate()
    L = []

    def ligne(jour, piece, compte, libelle, debit=ZERO, credit=ZERO):
        if (debut is None or jour >= debut) and (fin is None or jour <= fin):
            L.append({"journal": "OD", "date": jour, "piece": piece, "compte": compte,
                      "intitule": _(INTITULES[compte]), "libelle": libelle, "debit": debit, "credit": credit})

    for loc in _locations(societe):
        jour = loc.date_fait_generateur
        if jour is None or jour > aujourdhui:
            continue                                   # location pas encore réalisée
        f = loc.facture_emise
        if f is not None and (f.client_est_societe or f.issue_date <= jour):
            continue                                   # facturée au plus tard à la fin de la location : rien à constater
        montant = Decimal(loc.prix_htva or 0).quantize(Decimal("0.01"))
        if montant <= 0:
            continue
        piece = f"FAE-{str(loc.pk)[:8]}"
        immat = getattr(loc.voiture_exemplaire, "immatriculation", "") or ""
        lib = f"{_('Location à facturer')} – {immat} – {loc.nom_locataire} ({jour:%d/%m/%Y})".replace(" –  (", " (")
        ligne(jour, piece, COMPTE_PRODUITS_A_RECEVOIR, lib, debit=montant)
        ligne(jour, piece, COMPTE_CA_LOCATIONS, lib, credit=montant)
        if f is not None:
            lib_ext = f"{_('Extourne – facture émise')} {f.numero} – {lib}"
            ligne(f.issue_date, piece, COMPTE_CA_LOCATIONS, lib_ext, debit=montant)
            ligne(f.issue_date, piece, COMPTE_PRODUITS_A_RECEVOIR, lib_ext, credit=montant)
    return L

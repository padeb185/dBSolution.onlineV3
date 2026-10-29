"""
Paiements des factures : plafond des paiements en espèces par pays
et écritures comptables de caisse / banque (PCMN belge).
"""
from datetime import date
from decimal import Decimal

from django.utils.translation import gettext_lazy as _

# ------------------------------------------------------------------
# Plafond des paiements en espèces à un professionnel, par pays du vendeur
#   (montant, strict, plafond_non_resident)
#   strict=True : le montant doit être INFÉRIEUR au plafond (« X € ou plus interdit »)
#   strict=False : le montant peut ATTEINDRE le plafond (« plus de X € interdit »)
#   None : pas de plafond national
# Sources : Centres européens des consommateurs / autorités nationales (2026).
# À vérifier régulièrement : ces règles changent.
# ------------------------------------------------------------------
PLAFONDS_ESPECES = {
    "BE": (Decimal("3000"), False, None),
    "FR": (Decimal("1000"), False, Decimal("15000")),
    "ES": (Decimal("1000"), True, Decimal("10000")),
    "PT": (Decimal("3000"), True, Decimal("10000")),
    "IT": (Decimal("5000"), True, None),
    "GR": (Decimal("500"), True, None),
    "NL": (Decimal("3000"), True, None),
    "SK": (Decimal("5000"), False, None),
    "SI": (Decimal("5000"), False, None),
    "LT": (Decimal("5000"), False, None),
    "LV": (Decimal("7200"), False, None),
    "HR": (Decimal("15000"), False, None),
    "DE": None,
    "LU": None,
    "AT": None,
    "IE": None,
}

# Règlement (UE) 2024/1624 : plafond européen de 10 000 € à partir du 10 juillet 2027
PLAFOND_UE = Decimal("10000")
DATE_PLAFOND_UE = date(2027, 7, 10)


def plafond_especes(code_pays, jour=None, non_resident=False):
    """
    Retourne {"montant", "strict", "source"} ou None s'il n'y a pas de plafond.
    """
    jour = jour or date.today()
    regle = PLAFONDS_ESPECES.get((code_pays or "BE").upper()[:2])
    montant, strict = None, False
    if regle:
        montant, strict, non_res = regle
        if non_resident and non_res:
            montant, strict = non_res, False
    # Plafond européen (le plus bas des deux s'applique)
    if jour >= DATE_PLAFOND_UE and (montant is None or PLAFOND_UE < montant):
        montant, strict = PLAFOND_UE, True
    if montant is None:
        return None
    return {"montant": montant, "strict": strict}


def depasse_plafond(total_especes, plafond):
    if not plafond:
        return False
    if plafond["strict"]:
        return total_especes >= plafond["montant"]
    return total_especes > plafond["montant"]


# ------------------------------------------------------------------
# Comptabilité (PCMN)
# ------------------------------------------------------------------
COMPTE_CAISSE = "570000"
COMPTE_BANQUE = "550000"
COMPTE_CLIENTS = "400000"

COMPTE_ACOMPTES = "460000"

COMPTES = {
    COMPTE_CAISSE: _("Caisse – espèces"),
    COMPTE_BANQUE: _("Banque – compte courant"),
    COMPTE_CLIENTS: _("Clients"),
    COMPTE_ACOMPTES: _("Acomptes reçus sur commandes"),
}


def compte_tresorerie(mode):
    from .models import PaiementFacture
    return COMPTE_CAISSE if mode == PaiementFacture.Mode.ESPECES else COMPTE_BANQUE


def ecritures_paiement(paiement):
    """
    Écritures d'un encaissement (PaiementFacture ou acompte de location non encore facturé).
    Encaissement : débit caisse ou banque / crédit clients.
    Remboursement au client (note de crédit, montant négatif) : débit clients / crédit caisse ou banque.
    """
    if isinstance(paiement, EncaissementAcompte):
        return paiement.ecritures()
    tresorerie = compte_tresorerie(paiement.mode)
    libelle = f"{paiement.facture.numero or ''} – {paiement.facture.nom_client_courant()}".strip(" –")
    if paiement.location_id:
        libelle = f"{libelle} – {_('Acompte location')}"
    if paiement.montant < 0:
        montant = -paiement.montant
        return [
            {"compte": COMPTE_CLIENTS, "intitule": COMPTES[COMPTE_CLIENTS], "libelle": libelle, "debit": montant, "credit": Decimal("0")},
            {"compte": tresorerie, "intitule": COMPTES[tresorerie], "libelle": libelle, "debit": Decimal("0"), "credit": montant},
        ]
    return [
        {"compte": tresorerie, "intitule": COMPTES[tresorerie], "libelle": libelle, "debit": paiement.montant, "credit": Decimal("0")},
        {"compte": COMPTE_CLIENTS, "intitule": COMPTES[COMPTE_CLIENTS], "libelle": libelle, "debit": Decimal("0"), "credit": paiement.montant},
    ]



# ------------------------------------------------------------------
# Acomptes de location encaissés, pas encore repris comme paiement d'une facture
# ------------------------------------------------------------------
class EncaissementAcompte:
    """
    Acompte de location reçu (caisse si espèces, sinon banque).
      - location pas encore facturée : débit caisse/banque / crédit 460000 Acomptes reçus ;
      - facture émise avant la reprise des acomptes (montant payé sans mode) : contrepartie 400000 Clients.
    Même interface que PaiementFacture pour la page Caisse et banque et le journal comptable.
    """

    def __init__(self, location, montant, facture=None):
        self.location = location
        self.facture = facture
        self.montant = montant
        self.date = location.date_acompte
        self.mode = location.mode_acompte
        self.reference = str(_("Acompte location"))
        self.cree_par = None
        self.pk = None

    @property
    def est_especes(self):
        return self.mode == "ESPECES"

    def get_mode_display(self):
        return self.location.get_mode_acompte_display()

    @property
    def compte(self):
        return compte_tresorerie(self.mode)

    @property
    def piece(self):
        return (self.facture.numero if self.facture else "") or str(_("Acompte location"))

    def ecritures(self):
        tresorerie = compte_tresorerie(self.mode)
        contrepartie = COMPTE_CLIENTS if self.facture else COMPTE_ACOMPTES
        locataire = self.location.locataire
        libelle = " – ".join(filter(None, [
            self.facture.numero if self.facture else "",
            str(_("Acompte location")),
            str(locataire) if locataire else "",
            str(self.location.voiture_exemplaire or ""),
        ]))
        return [
            {"compte": tresorerie, "intitule": COMPTES[tresorerie], "libelle": libelle, "debit": self.montant, "credit": Decimal("0")},
            {"compte": contrepartie, "intitule": COMPTES[contrepartie], "libelle": libelle, "debit": Decimal("0"), "credit": self.montant},
        ]


def acomptes_locations_encaisses(societe, debut=None, fin=None, annee=None, mois=None):
    """Acomptes de location reçus qui ne sont pas (encore) un paiement détaillé d'une facture."""
    from django.apps import apps
    Location = apps.get_model("voiture_location", "Location")

    qs = (Location.objects.filter(societe=societe, acompte=True, montant_acompte__gt=0,
                                  date_acompte__isnull=False, paiements_acompte__isnull=True)
          .select_related("voiture_exemplaire", "client", "societe_cliente", "client_pilotage")
          .prefetch_related("factures", "factures__paiements")
          .order_by("date_acompte"))
    if debut:
        qs = qs.filter(date_acompte__gte=debut)
    if fin:
        qs = qs.filter(date_acompte__lte=fin)
    if annee:
        qs = qs.filter(date_acompte__year=annee)
    if mois:
        qs = qs.filter(date_acompte__month=mois)

    resultat = []
    non_ventile = {}
    for location in qs:
        montant = Decimal(location.montant_acompte).quantize(Decimal("0.01"))
        facture = location.facture_emise
        if facture is not None:
            if facture.client_est_societe:
                continue
            # Facture émise sans reprise de l'acompte : seul le montant payé « sans mode » vient de l'acompte
            reste = non_ventile.setdefault(facture.pk, facture.montant_non_ventile)
            montant = min(montant, reste)
            if montant <= 0:
                continue
            non_ventile[facture.pk] = reste - montant
        resultat.append(EncaissementAcompte(location, montant, facture))
    return resultat

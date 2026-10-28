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

COMPTES = {
    COMPTE_CAISSE: _("Caisse – espèces"),
    COMPTE_BANQUE: _("Banque – compte courant"),
    COMPTE_CLIENTS: _("Clients"),
}


def compte_tresorerie(mode):
    from .models import PaiementFacture
    return COMPTE_CAISSE if mode == PaiementFacture.Mode.ESPECES else COMPTE_BANQUE


def ecritures_paiement(paiement):
    """
    Encaissement : débit caisse ou banque / crédit clients.
    Remboursement au client (note de crédit, montant négatif) : débit clients / crédit caisse ou banque.
    """
    tresorerie = compte_tresorerie(paiement.mode)
    libelle = f"{paiement.facture.numero or ''} – {paiement.facture.nom_client_courant()}".strip(" –")
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

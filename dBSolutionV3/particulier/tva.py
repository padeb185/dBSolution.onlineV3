"""
Taux de TVA (taux normal, en %) appliqués au carburant et à la recharge électrique, par pays de la station.
Mêmes taux que dBSolution (fuel/models.py TVA_CARBURANT, recharge/models.py TVA_ELECTRICITE),
complétés par la Suisse et la Norvège. Un pays absent : taux à saisir sur le plein.
"""
from decimal import ROUND_HALF_UP, Decimal

TVA_CARBURANT = {
    "AT": 20, "BE": 21, "BG": 20, "HR": 25, "CY": 19, "CZ": 21, "DK": 25, "EE": 24, "FI": 25.5,
    "FR": 20, "DE": 19, "GR": 24, "HU": 27, "IE": 23, "IT": 22, "LV": 21, "LT": 21, "LU": 17,
    "MT": 18, "NL": 21, "PL": 23, "PT": 23, "RO": 21, "SK": 23, "SI": 22, "ES": 21, "SE": 25,
    "GB": 20, "CH": 8.1, "NO": 25,
}


def taux_tva(pays):
    """Taux du pays (Decimal) ou None s'il n'est pas connu."""
    taux = TVA_CARBURANT.get((pays or "").upper())
    return Decimal(str(taux)) if taux is not None else None


def ventiler(montant_ttc, taux):
    """Montant TVAC → (montant HTVA, TVA), arrondis au cent. None si le taux est inconnu."""
    if montant_ttc is None or taux is None:
        return None, None
    ttc = Decimal(montant_ttc)
    htva = (ttc / (Decimal("1") + Decimal(taux) / Decimal("100"))).quantize(Decimal("0.01"), ROUND_HALF_UP)
    return htva, ttc - htva

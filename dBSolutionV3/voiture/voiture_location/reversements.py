"""
Reversement des parts d'une location aux autres propriétaires du véhicule.

    base = location facturée HTVA : lignes de la location sur les factures émises
           (facture principale, facture complémentaire des km, notes de crédit déduites)
    part HTVA = base × part (%) ; commission = part × commission (%) ; à reverser = part − commission

Notre société garde sa propre part et les commissions. Les reversements sont (re)calculés à l'émission
d'une facture de la location (principale ou complémentaire) ; un reversement déjà payé n'est jamais modifié :
une différence crée un reversement complémentaire (négatif si trop reversé).
"""
from decimal import ROUND_HALF_UP, Decimal

from django.db import transaction

DEUX = Decimal("0.01")
ZERO = Decimal("0.00")


def _r(x):
    return Decimal(x or 0).quantize(DEUX, rounding=ROUND_HALF_UP)


def parts_a_reverser(location):
    """Parts des autres propriétaires (hors notre société) du véhicule loué."""
    from proprietaire.models import ProprietaireVoiture
    if not location.voiture_exemplaire_id:
        return []
    return [p for p in ProprietaireVoiture.objects.filter(voiture_exemplaire_id=location.voiture_exemplaire_id)
            .select_related("proprietaire", "societe_cliente", "societe")
            .order_by("-part_proprietaire_pourcent", "id") if not p.est_tenant]


def base_facturee(location):
    """Montant HTVA facturé pour la location (factures émises, notes de crédit déduites)."""
    from facture.models import FactureLine
    total = ZERO
    for l in (FactureLine.objects.filter(location=location, facture__statut="EMISE",
                                         facture__client_est_societe=False).select_related("facture")):
        total += _r(l.total_ht) * Decimal(getattr(l.facture, "signe", 1))
    return _r(total)


def calcul_part(location, part, base=None):
    base = _r(location.prix_htva if base is None else base)
    pct = Decimal(part.part_proprietaire_pourcent or 0)
    com_pct = Decimal(getattr(part, "commission_location", 0) or 0)
    montant_part = _r(base * pct / Decimal("100"))
    commission = _r(montant_part * com_pct / Decimal("100"))
    return {"base_htva": base, "part_pourcent": pct, "montant_part_htva": montant_part,
            "commission_pourcent": com_pct, "commission_htva": commission, "montant_du": montant_part - commission}


def ventilation(location):
    """Aperçu : [{part, nom, calcul, deja (reversements existants), reste}] + notre part."""
    lignes = []
    facturee = base_facturee(location)
    # Pas encore facturée : aperçu sur le prix de la location
    base = facturee if location.facture_emise is not None else _r(location.prix_htva)
    total_autres = ZERO
    for part in parts_a_reverser(location):
        c = calcul_part(location, part, base)
        existants = list(location.reversements.filter(part=part))
        lignes.append({"part": part, "nom": part.nom_proprietaire, "calcul": c, "reversements": existants,
                       "reverse": sum((r.montant_du for r in existants if r.est_paye), ZERO),
                       "a_reverser": sum((r.montant_du for r in existants if not r.est_paye), ZERO)})
        total_autres += c["montant_du"]
    return {"base_htva": base, "lignes": lignes, "notre_part": base - total_autres,
            "previsionnel": location.facture_emise is None}


@transaction.atomic
def generer_reversements(location, jour):
    """Crée / met à jour les reversements de la location. Retourne le nombre de reversements modifiés."""
    from .models import ReversementLocation, StatutReversement

    facture = location.facture_emise
    if facture is None or facture.client_est_societe:
        return 0
    modifies = 0
    base = base_facturee(location)
    champs = ("montant_part_htva", "commission_htva", "montant_du")
    for part in parts_a_reverser(location):
        cible = calcul_part(location, part, base)
        existants = list(location.reversements.select_for_update().filter(part=part))
        deja = {k: sum((getattr(r, k) for r in existants), ZERO) for k in champs}
        delta = {k: cible[k] - deja[k] for k in champs}
        if not any(delta.values()):
            continue
        ouvert = next((r for r in existants if r.statut == StatutReversement.A_PAYER), None)
        if ouvert is not None:
            for k in champs:
                setattr(ouvert, k, getattr(ouvert, k) + delta[k])
            ouvert.base_htva = base
            ouvert.part_pourcent = cible["part_pourcent"]
            ouvert.commission_pourcent = cible["commission_pourcent"]
            ouvert.beneficiaire = part.nom_proprietaire[:150]
            if not ouvert.montant_du and not ouvert.montant_part_htva:
                ouvert.delete()
            else:
                ouvert.save()
        else:
            ReversementLocation.objects.create(
                societe=location.societe, location=location, part=part, beneficiaire=part.nom_proprietaire[:150],
                date=jour, part_pourcent=cible["part_pourcent"], base_htva=base,
                commission_pourcent=cible["commission_pourcent"], **delta,
            )
        modifies += 1
    return modifies

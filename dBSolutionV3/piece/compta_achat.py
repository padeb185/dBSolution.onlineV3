"""
Un seul encodage pour les factures d'achat de pièces / lubrifiants / pneus :
la réception en stock crée (ou rattache) l'achat comptable AchatMds correspondant.
"""
from decimal import Decimal

from django.db import transaction

R2 = Decimal("0.01")


def achat_existant(facture):
    """AchatMds déjà encodé pour la même facture (même fournisseur et même référence), non rattaché."""
    from achat_mds.documents import TypeDocumentAchat
    from achat_mds.models import AchatMds
    if not facture.fournisseur_id or not facture.numero_facture:
        return AchatMds.objects.none()
    return AchatMds.objects.filter(
        societe=facture.societe, fournisseur_id=facture.fournisseur_id,
        reference_facture__iexact=facture.numero_facture.strip(),
        type_document=TypeDocumentAchat.FACTURE, facture_stock__isnull=True,
    )


@transaction.atomic
def comptabiliser(facture, transport_htva=None, date_paiement=None):
    """
    Rattache l'achat déjà encodé s'il existe, sinon crée un AchatMds par taux de TVA
    (le transport est porté par la ligne au taux principal).
    Retourne (achats, rattache: bool, ecart_htva: Decimal).
    """
    from achat_mds.models import AchatMds

    existants = list(achat_existant(facture))
    if existants:
        AchatMds.objects.filter(pk__in=[a.pk for a in existants]).update(facture_stock=facture)
        deja = sum((a.achat_montant_htva or Decimal("0") for a in existants), Decimal("0"))
        return existants, True, (Decimal(facture.total_htva) - deja).quantize(R2)

    transport = Decimal(transport_htva or 0).quantize(R2)
    groupes = facture.totaux_par_taux()  # [(taux, base, tva, tvac)]
    if not groupes:
        return [], False, Decimal("0")
    principal = max(groupes, key=lambda g: g[1])[0]
    libelle = (facture.commentaire or "Réception en stock")[:100]
    achats = []
    for taux, base, _tva, _tvac in groupes:
        achats.append(AchatMds.objects.create(
            societe=facture.societe, fournisseur=facture.fournisseur, facture_stock=facture,
            libelle_facture=libelle, reference_facture=facture.numero_facture[:100],
            achat_montant_htva=base, achat_tva=taux,
            transport_montant_htva=transport if (taux == principal and transport) else None,
            date_facture=facture.date_facture, date_paiement=date_paiement,
        ))
    return achats, False, Decimal("0")


def lier_depuis_achat(achat):
    """Encodage direct d'un AchatMds : le rattache à la réception en stock de la même facture, si elle existe."""
    from .models import FactureAchatStock
    if achat.facture_stock_id or not achat.est_facture or not achat.reference_facture:
        return None
    facture = (FactureAchatStock.objects
               .filter(societe=achat.societe, fournisseur_id=achat.fournisseur_id,
                       numero_facture__iexact=achat.reference_facture.strip(), achats_mds__isnull=True)
               .first())
    if facture:
        type(achat).objects.filter(pk=achat.pk).update(facture_stock=facture)
        achat.facture_stock = facture
    return facture

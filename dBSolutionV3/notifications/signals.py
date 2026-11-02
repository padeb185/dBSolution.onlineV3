"""
Déclencheurs des notifications :
  maintenance créée          → chef d'atelier, direction, chef mécanicien
  facture de vente émise     → direction, comptable
  paiement de facture reçu   → comptable
  facture d'achat encodée    → comptable (marchandises, outillage)
L'auteur de l'action ne reçoit pas sa propre notification.
"""
from django.apps import apps
from django.db.models.signals import post_save, pre_save
from django.utils.formats import number_format
from django.utils.translation import gettext as _

from .services import notifier

import functools
import logging

log = logging.getLogger(__name__)


def securise(fonction):
    """Un déclencheur de notification ne doit jamais faire échouer l'enregistrement métier."""
    @functools.wraps(fonction)
    def enveloppe(*args, **kwargs):
        try:
            return fonction(*args, **kwargs)
        except Exception:
            log.exception("Déclencheur de notification en erreur : %s", fonction.__name__)
    return enveloppe


def _euros(x):
    try:
        return f"{number_format(x, 2, force_grouping=True)} €"
    except Exception:
        return f"{x} €"


# ---------------------------------------------------------------- maintenance
@securise
def maintenance_creee(sender, instance, created, **kwargs):
    if not created or kwargs.get("raw"):
        return
    vehicule = instance.voiture_exemplaire or instance.immatriculation
    titre = _("Nouvelle maintenance : %(type)s – %(vehicule)s") % {
        "type": instance.get_type_maintenance_display() if instance.type_maintenance else _("Maintenance"),
        "vehicule": vehicule,
    }
    message = _("Intervention du %(date)s, %(km)s km.") % {
        "date": instance.date_intervention.strftime("%d/%m/%Y") if hasattr(instance.date_intervention, "strftime") else (instance.date_intervention or "—"),
        "km": instance.kilometres_total or 0,
    }
    notifier(instance.societe, type="maintenance", titre=titre, message=message,
             url_name="maintenance:maintenance_detail", url_kwargs={"maintenance_id": str(instance.pk)})


# ---------------------------------------------------------------- factures de vente
@securise
def facture_avant(sender, instance, **kwargs):
    ancien = None
    if instance.pk:
        ancien = sender.objects.filter(pk=instance.pk).values_list("statut", flat=True).first()
    instance._statut_avant = ancien


@securise
def facture_apres(sender, instance, created, **kwargs):
    if kwargs.get("raw") or instance.statut != sender.Statut.EMISE:
        return
    if getattr(instance, "_statut_avant", None) == sender.Statut.EMISE:
        return
    try:
        client = instance.nom_client_courant()
    except Exception:
        client = ""
    titre = _("%(doc)s émise %(numero)s – %(client)s") % {
        "doc": instance.get_type_document_display(), "numero": instance.numero or "", "client": client}
    message = _("Montant : %(total)s TVAC.") % {"total": _euros(instance.total)}
    notifier(instance.societe, type="vente", titre=titre, message=message,
             url_name="facture:detail", url_kwargs={"pk": str(instance.pk)})


@securise
def paiement_recu(sender, instance, created, **kwargs):
    if not created or kwargs.get("raw"):
        return
    f = instance.facture
    titre = _("Paiement reçu : %(montant)s – facture %(numero)s") % {
        "montant": _euros(instance.montant), "numero": f.numero or ""}
    try:
        message = _("Client : %(client)s.") % {"client": f.nom_client_courant()}
    except Exception:
        message = ""
    notifier(f.societe, type="paiement", titre=titre, message=message,
             url_name="facture:detail", url_kwargs={"pk": str(f.pk)})


# ---------------------------------------------------------------- achats
@securise
def achat_mds_cree(sender, instance, created, **kwargs):
    if not created or kwargs.get("raw"):
        return
    notifier(instance.societe, type="achat", titre=_("Facture d'achat encodée : %(achat)s") % {"achat": instance},
             url_name="achat_mds:achat_detail", url_kwargs={"achat_id": str(instance.pk)})


@securise
def outillage_cree(sender, instance, created, **kwargs):
    if not created or kwargs.get("raw"):
        return
    notifier(instance.societe, type="achat", titre=_("Achat d'outillage encodé : %(achat)s") % {"achat": instance},
             url_name="outillage:outillage_detail", url_kwargs={"outillage_id": instance.pk})


def brancher():
    def modele(label):
        try:
            return apps.get_model(label)
        except LookupError:
            return None

    m = modele("maintenance.Maintenance")
    if m:
        post_save.connect(maintenance_creee, sender=m, dispatch_uid="notif_maintenance")
    f = modele("facture.Facture")
    if f:
        pre_save.connect(facture_avant, sender=f, dispatch_uid="notif_facture_avant")
        post_save.connect(facture_apres, sender=f, dispatch_uid="notif_facture_apres")
    p = modele("facture.PaiementFacture")
    if p:
        post_save.connect(paiement_recu, sender=p, dispatch_uid="notif_paiement")
    a = modele("achat_mds.AchatMds")
    if a:
        post_save.connect(achat_mds_cree, sender=a, dispatch_uid="notif_achat_mds")
    o = modele("outillage.Outillage")
    if o:
        post_save.connect(outillage_cree, sender=o, dispatch_uid="notif_outillage")

"""
Créances clients : factures émises non payées, classées par client et par ancienneté
(à partir de l'échéance, sinon de la date de la facture), et locations réalisées pas encore facturées.
"""
from collections import OrderedDict
from decimal import Decimal

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

ZERO = Decimal("0.00")
TRANCHES = OrderedDict([
    ("non_echu", _("Non échu")),
    ("j30", _("1 à 30 jours")),
    ("j60", _("31 à 60 jours")),
    ("j90", _("61 à 90 jours")),
    ("plus90", _("Plus de 90 jours")),
])


def tranche(jours_retard):
    if jours_retard <= 0:
        return "non_echu"
    if jours_retard <= 30:
        return "j30"
    if jours_retard <= 60:
        return "j60"
    if jours_retard <= 90:
        return "j90"
    return "plus90"


def creances_clients(societe, aujourdhui=None):
    from facture.models import Facture

    aujourdhui = aujourdhui or timezone.localdate()
    qs = (Facture.objects.filter(societe=societe, statut=Facture.Statut.EMISE, client_est_societe=False)
          .exclude(type_document=Facture.TypeDocument.NOTE_CREDIT)
          .exclude(statut_paiement=Facture.StatutPaiement.PAYE)
          .select_related("client_particulier", "client_atelier__client_particulier", "client_atelier__societe_cliente",
                          "societe_cliente", "proprietaire", "voiture_exemplaire")
          .order_by("issue_date"))

    clients = OrderedDict()
    totaux = OrderedDict((t, ZERO) for t in TRANCHES)
    for f in qs:
        reste = Decimal(f.reste_a_payer or 0)
        if reste <= 0:
            continue
        echeance = f.due_date or f.issue_date
        retard = (aujourdhui - echeance).days
        t = tranche(retard)
        nom = f.client_nom or f.nom_client_courant() or "—"
        c = clients.setdefault(nom, {"nom": nom, "factures": [], "total": ZERO, "nb": 0,
                                     "tranches": OrderedDict((k, ZERO) for k in TRANCHES), "retard_max": 0})
        c["factures"].append({"facture": f, "echeance": echeance, "retard": retard, "tranche": t, "reste": reste})
        c["tranches"][t] += reste
        c["total"] += reste
        c["nb"] += 1
        c["retard_max"] = max(c["retard_max"], retard)
        totaux[t] += reste

    lignes = sorted(clients.values(), key=lambda c: c["total"], reverse=True)
    total = sum(totaux.values(), ZERO)
    echu = total - totaux["non_echu"]
    return {"clients": lignes, "tranches": TRANCHES, "totaux": totaux, "total": total, "echu": echu,
            "nb_factures": sum(c["nb"] for c in lignes), "aujourdhui": aujourdhui}

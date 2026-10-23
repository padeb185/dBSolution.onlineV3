"""
Comptabilité – journaux de trésorerie (caisse, banque…) avec solde d'ouverture.

Chaque compte de trésorerie (caisse, banque) est ouvert à une date avec un
solde d'ouverture. Son journal reprend :
  • l'écriture d'ouverture,
  • les mouvements encodés à la main (entrées / sorties, virements internes),
  • automatiquement, les encaissements des factures (espèces → caisse par défaut,
    autres modes → banque par défaut) et les salaires nets payés (banque par défaut).
"""
import uuid
from datetime import date
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, Sum
from django.utils.translation import gettext_lazy as _

ZERO = Decimal("0.00")

# Comptes de contrepartie proposés (PCMN belge)
COMPTES_CONTREPARTIE = [
    ("100000", _("Capital")),
    ("400000", _("Clients")),
    ("411000", _("TVA à récupérer")),
    ("440000", _("Fournisseurs")),
    ("451000", _("TVA à payer")),
    ("453000", _("Précomptes retenus")),
    ("454000", _("Office National de Sécurité Sociale")),
    ("455000", _("Rémunérations")),
    ("499000", _("Compte d'attente")),
    ("580000", _("Virements internes")),
    ("600000", _("Achats de marchandises")),
    ("610000", _("Services et biens divers")),
    ("640000", _("Autres charges d'exploitation")),
    ("650000", _("Charges financières")),
    ("700000", _("Chiffre d'affaires – ventes")),
    ("750000", _("Produits financiers")),
]
INTITULES_CONTREPARTIE = dict(COMPTES_CONTREPARTIE)
COMPTE_VIREMENTS_INTERNES = "580000"


class CompteTresorerie(models.Model):
    class Type(models.TextChoices):
        CAISSE = "CAISSE", _("Caisse")
        BANQUE = "BANQUE", _("Banque")

    COMPTE_PCMN_DEFAUT = {Type.CAISSE: "570000", Type.BANQUE: "550000"}

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey(
        "societe.Societe", on_delete=models.CASCADE, related_name="comptes_tresorerie",
    )
    type = models.CharField(_("Type"), max_length=10, choices=Type.choices, default=Type.BANQUE)
    nom = models.CharField(_("Nom du compte"), max_length=100,
                           help_text=_("Ex. : Caisse atelier, KBC compte courant…"))
    compte_pcmn = models.CharField(
        _("Compte comptable (PCMN)"), max_length=10, blank=True,
        help_text=_("570000 pour la caisse, 550000 pour la banque (ou un sous-compte : 550100…)."),
    )
    banque = models.CharField(_("Banque"), max_length=100, blank=True)
    iban = models.CharField(_("IBAN"), max_length=34, blank=True)
    bic = models.CharField(_("BIC"), max_length=11, blank=True)

    date_ouverture = models.DateField(_("Date d'ouverture"), default=date.today)
    solde_ouverture = models.DecimalField(
        _("Solde d'ouverture"), max_digits=12, decimal_places=2, default=ZERO,
        help_text=_("Montant présent dans la caisse / sur le compte à la date d'ouverture."),
    )
    compte_contrepartie_ouverture = models.CharField(
        _("Contrepartie de l'ouverture (PCMN)"), max_length=10, default="499000",
        help_text=_("Compte crédité par l'écriture d'ouverture (499000 compte d'attente, 100000 capital…)."),
    )
    par_defaut = models.BooleanField(
        _("Compte par défaut"), default=False,
        help_text=_("Reçoit automatiquement les encaissements des factures "
                    "(espèces pour une caisse, autres modes pour une banque) et les salaires payés (banque)."),
    )
    actif = models.BooleanField(_("Actif"), default=True)
    remarques = models.TextField(_("Remarques"), blank=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Compte de trésorerie")
        verbose_name_plural = _("Comptes de trésorerie")
        ordering = ["type", "nom"]

    def __str__(self):
        return f"{self.get_type_display()} – {self.nom}"

    def save(self, *args, **kwargs):
        if not self.compte_pcmn:
            self.compte_pcmn = self.COMPTE_PCMN_DEFAUT.get(self.type, "550000")
        self.iban = (self.iban or "").replace(" ", "").upper()
        super().save(*args, **kwargs)
        # Un seul compte par défaut par type et par société
        if self.par_defaut:
            CompteTresorerie.objects.filter(
                societe=self.societe, type=self.type, par_defaut=True
            ).exclude(pk=self.pk).update(par_defaut=False)

    @property
    def journal_code(self):
        return "CAI" if self.type == self.Type.CAISSE else "BQ"

    # -------------------------------------------------------------
    # Lignes du journal
    # -------------------------------------------------------------
    def lignes(self, debut=None, fin=None):
        """
        Toutes les lignes du compte (ouverture, mouvements, sources automatiques)
        triées par date. Chaque ligne : date, libelle, entree, sortie,
        contrepartie, piece, source, objet.
        """
        L = []

        if (debut is None or self.date_ouverture >= debut) and (fin is None or self.date_ouverture <= fin):
            if self.solde_ouverture:
                L.append({
                    "date": self.date_ouverture, "libelle": _("Solde d'ouverture"),
                    "entree": max(self.solde_ouverture, ZERO), "sortie": max(-self.solde_ouverture, ZERO),
                    "contrepartie": self.compte_contrepartie_ouverture, "piece": "OUV",
                    "source": "ouverture", "objet": None, "ordre": 0,
                })

        mouvements = self.mouvements.all()
        if debut:
            mouvements = mouvements.filter(date__gte=debut)
        if fin:
            mouvements = mouvements.filter(date__lte=fin)
        for m in mouvements:
            L.append({
                "date": m.date, "libelle": m.libelle,
                "entree": m.montant if m.sens == m.Sens.ENTREE else ZERO,
                "sortie": m.montant if m.sens == m.Sens.SORTIE else ZERO,
                "contrepartie": m.compte_contrepartie, "piece": m.piece,
                "source": "virement" if m.virement_lie_id else "manuel", "objet": m, "ordre": 1,
            })

        L += self._lignes_automatiques(debut, fin)
        L.sort(key=lambda l: (l["date"], l["ordre"]))
        return L

    def _lignes_automatiques(self, debut, fin):
        if not self.par_defaut:
            return []
        L = []
        bornes_debut = max(d for d in [debut, self.date_ouverture] if d)

        # Encaissements des factures
        try:
            from facture.models import PaiementFacture
            paiements = PaiementFacture.objects.filter(
                facture__societe=self.societe, date__gte=bornes_debut
            ).select_related("facture")
            if fin:
                paiements = paiements.filter(date__lte=fin)
            if self.type == self.Type.CAISSE:
                paiements = paiements.filter(mode=PaiementFacture.Mode.ESPECES)
            else:
                paiements = paiements.exclude(mode=PaiementFacture.Mode.ESPECES)
            for p in paiements:
                client = getattr(p.facture, "nom_client_courant", "") or ""
                L.append({
                    "date": p.date,
                    "libelle": f"{_('Encaissement facture')} {p.facture.numero or ''} {client}".strip(),
                    "entree": p.montant if p.montant > 0 else ZERO,
                    "sortie": -p.montant if p.montant < 0 else ZERO,
                    "contrepartie": "400000", "piece": p.facture.numero or "",
                    "source": "facture", "objet": p, "ordre": 2,
                })
        except Exception:
            pass

        # Salaires nets payés (banque)
        if self.type == self.Type.BANQUE:
            try:
                from utilisateurs.models import PaieUtilisateur
                paies = PaieUtilisateur.objects.filter(
                    utilisateur__societe=self.societe, date_paiement__isnull=False,
                    date_paiement__gte=bornes_debut,
                ).select_related("utilisateur")
                if fin:
                    paies = paies.filter(date_paiement__lte=fin)
                for paie in paies:
                    L.append({
                        "date": paie.date_paiement,
                        "libelle": f"{_('Salaire net')} {paie.mois:02d}/{paie.annee} – "
                                   f"{paie.utilisateur.prenom} {paie.utilisateur.nom}",
                        "entree": ZERO, "sortie": paie.net_a_payer,
                        "contrepartie": "455000", "piece": f"PAIE-{paie.annee}{paie.mois:02d}-{paie.pk}",
                        "source": "paie", "objet": paie, "ordre": 3,
                    })
            except Exception:
                pass
        return L

    def solde(self, au=None):
        """Solde du compte à une date (incluse) – toutes sources confondues."""
        total = ZERO
        for l in self.lignes(fin=au):
            total += l["entree"] - l["sortie"]
        return total


class MouvementTresorerie(models.Model):
    class Sens(models.TextChoices):
        ENTREE = "ENTREE", _("Entrée (recette)")
        SORTIE = "SORTIE", _("Sortie (dépense)")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    compte = models.ForeignKey(CompteTresorerie, on_delete=models.CASCADE, related_name="mouvements",
                               verbose_name=_("Compte"))
    date = models.DateField(_("Date"), default=date.today)
    sens = models.CharField(_("Sens"), max_length=10, choices=Sens.choices, default=Sens.SORTIE)
    montant = models.DecimalField(_("Montant"), max_digits=12, decimal_places=2,
                                  validators=[MinValueValidator(Decimal("0.01"))])
    libelle = models.CharField(_("Libellé"), max_length=255)
    compte_contrepartie = models.CharField(
        _("Compte de contrepartie (PCMN)"), max_length=10, default="499000",
        help_text=_("Ex. : 440000 fournisseurs, 610000 services et biens divers, 700000 ventes…"),
    )
    piece = models.CharField(_("Pièce / référence"), max_length=50, blank=True)
    remarques = models.TextField(_("Remarques"), blank=True)

    # Virement interne : le mouvement jumeau sur l'autre compte
    virement_lie = models.OneToOneField("self", on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name="+", editable=False)

    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="mouvements_tresorerie", editable=False)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Mouvement de trésorerie")
        verbose_name_plural = _("Mouvements de trésorerie")
        ordering = ["date", "created_at"]

    def __str__(self):
        return f"{self.compte} – {self.date} – {self.libelle} – {self.montant} €"

    @property
    def intitule_contrepartie(self):
        return INTITULES_CONTREPARTIE.get(self.compte_contrepartie, "")

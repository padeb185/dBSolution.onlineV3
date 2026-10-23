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
    ("613000", _("Rétributions de tiers – honoraires")),
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

        # Factures d'instructeurs payées depuis ce compte
        try:
            factures = self.factures_instructeurs.filter(date_paiement__isnull=False).select_related("instructeur")
            if debut:
                factures = factures.filter(date_paiement__gte=debut)
            if fin:
                factures = factures.filter(date_paiement__lte=fin)
            L += [f.ligne_tresorerie() for f in factures]
        except Exception:
            pass

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

            # Factures d'instructeurs payées sans compte précisé → banque par défaut
            try:
                factures = FactureInstructeur.objects.filter(
                    societe=self.societe, date_paiement__isnull=False, compte_paiement__isnull=True,
                    date_paiement__gte=bornes_debut,
                ).select_related("instructeur")
                if fin:
                    factures = factures.filter(date_paiement__lte=fin)
                L += [f.ligne_tresorerie() for f in factures]
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


# ======================================================================
# INSTRUCTEURS INDÉPENDANTS – factures d'achat et autofacturation
# ======================================================================
COMPTE_HONORAIRES = "613000"     # Rétributions de tiers / honoraires (PCMN 613)
COMPTE_TVA_DEDUCTIBLE = "411000"
COMPTE_FOURNISSEURS = "440000"
COMPTE_BANQUE_DEFAUT = "550000"
R2 = Decimal("0.01")


class RegimeTVAInstructeur(models.TextChoices):
    ASSUJETTI = "ASSUJETTI", _("Assujetti à la TVA")
    FRANCHISE = "FRANCHISE", _("Franchise des petites entreprises (art. 56bis CTVA)")
    EXONERE = "EXONERE", _("Exonéré de TVA (art. 44 CTVA)")


MENTIONS_TVA_INSTRUCTEUR = {
    RegimeTVAInstructeur.FRANCHISE: _("Régime particulier de franchise des petites entreprises"),
    RegimeTVAInstructeur.EXONERE: _("Exemption de TVA – article 44 du Code de la TVA"),
}


class ProfilInstructeur(models.Model):
    """Données d'entreprise d'un instructeur indépendant (nécessaires à l'autofacturation)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="profils_instructeurs")
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name="profil_instructeur", verbose_name=_("Instructeur"))
    nom_commercial = models.CharField(_("Nom commercial / dénomination"), max_length=200, blank=True)
    numero_entreprise = models.CharField(
        _("Numéro d'entreprise (BCE) / TVA"), max_length=20,
        help_text=_("Ex. : BE0123456789"),
    )
    regime_tva = models.CharField(_("Régime TVA"), max_length=10, choices=RegimeTVAInstructeur.choices,
                                  default=RegimeTVAInstructeur.ASSUJETTI)
    taux_tva = models.DecimalField(_("Taux de TVA (%)"), max_digits=5, decimal_places=2, default=Decimal("21.00"))
    tarif_horaire_htva = models.DecimalField(
        _("Tarif horaire de l'instructeur HTVA (€)"), max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal("0"))],
        help_text=_("Ce que l'entreprise paie à l'instructeur. Vide : prix facturé au client (HTVA)."),
    )
    iban = models.CharField(_("IBAN"), max_length=34, blank=True,
                            help_text=_("Vide : compte bancaire de la fiche utilisateur."))
    delai_paiement_jours = models.PositiveSmallIntegerField(_("Délai de paiement (jours)"), default=30)

    accord_autofacturation = models.BooleanField(
        _("Accord d'autofacturation signé"), default=False,
        help_text=_("L'autofacturation n'est permise qu'avec un accord préalable écrit de l'instructeur."),
    )
    date_accord_autofacturation = models.DateField(_("Date de l'accord d'autofacturation"), null=True, blank=True)
    remarques = models.TextField(_("Remarques"), blank=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Profil d'instructeur indépendant")
        verbose_name_plural = _("Profils d'instructeurs indépendants")

    def __str__(self):
        return self.nom_affiche

    @property
    def nom_affiche(self):
        u = self.utilisateur
        nom = f"{u.prenom} {u.nom}".strip()
        return f"{self.nom_commercial} ({nom})" if self.nom_commercial else nom

    @property
    def iban_paiement(self):
        return self.iban or getattr(self.utilisateur, "numero_compte_bancaire", "") or ""

    @property
    def autofacturation_possible(self):
        return bool(self.accord_autofacturation and self.date_accord_autofacturation and self.numero_entreprise)

    def save(self, *args, **kwargs):
        self.numero_entreprise = (self.numero_entreprise or "").replace(" ", "").replace(".", "").upper()
        self.iban = (self.iban or "").replace(" ", "").upper()
        if self.regime_tva != RegimeTVAInstructeur.ASSUJETTI:
            self.taux_tva = Decimal("0")
        super().save(*args, **kwargs)


class FactureInstructeur(models.Model):
    """Facture d'un instructeur indépendant à l'entreprise (reçue ou autofacture)."""

    class Statut(models.TextChoices):
        BROUILLON = "BROUILLON", _("Brouillon")
        EMISE = "EMISE", _("Émise – à payer")
        PAYEE = "PAYEE", _("Payée")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="factures_instructeurs")
    instructeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                    related_name="factures_instructeur", verbose_name=_("Instructeur"))
    autofacturation = models.BooleanField(
        _("Autofacturation"), default=True,
        help_text=_("Coché : l'entreprise établit la facture au nom et pour le compte de l'instructeur. "
                    "Décoché : facture reçue de l'instructeur."),
    )
    numero = models.CharField(_("Numéro"), max_length=40, blank=True, editable=False)
    reference_instructeur = models.CharField(_("Numéro de la facture de l'instructeur"), max_length=50, blank=True)
    date_facture = models.DateField(_("Date de facture"), default=date.today)
    periode_debut = models.DateField(_("Période du"))
    periode_fin = models.DateField(_("au"))
    date_echeance = models.DateField(_("Échéance"), null=True, blank=True)

    regime_tva = models.CharField(_("Régime TVA"), max_length=10, choices=RegimeTVAInstructeur.choices,
                                  default=RegimeTVAInstructeur.ASSUJETTI)
    taux_tva = models.DecimalField(_("Taux de TVA (%)"), max_digits=5, decimal_places=2, default=Decimal("21.00"))
    montant_htva = models.DecimalField(_("Total HTVA"), max_digits=12, decimal_places=2, default=ZERO)
    montant_tva = models.DecimalField(_("TVA"), max_digits=12, decimal_places=2, default=ZERO)
    montant_tvac = models.DecimalField(_("Total TVAC"), max_digits=12, decimal_places=2, default=ZERO)

    statut = models.CharField(_("Statut"), max_length=10, choices=Statut.choices, default=Statut.BROUILLON)
    date_emission = models.DateField(_("Émise le"), null=True, blank=True, editable=False)
    date_paiement = models.DateField(_("Payée le"), null=True, blank=True)
    compte_paiement = models.ForeignKey(
        CompteTresorerie, on_delete=models.SET_NULL, null=True, blank=True, related_name="factures_instructeurs",
        verbose_name=_("Payée depuis le compte"),
        help_text=_("Vide : compte bancaire par défaut."),
    )
    remarques = models.TextField(_("Remarques"), blank=True)

    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="factures_instructeur_creees", editable=False)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Facture d'instructeur")
        verbose_name_plural = _("Factures d'instructeurs")
        ordering = ["-date_facture", "-created_at"]

    def __str__(self):
        return f"{self.numero or self.reference_instructeur or _('Brouillon')} – {self.instructeur}"

    # ------------------------------------------------------------------
    @property
    def profil(self):
        return getattr(self.instructeur, "profil_instructeur", None)

    @property
    def mention_tva(self):
        return MENTIONS_TVA_INSTRUCTEUR.get(self.regime_tva, "")

    @property
    def piece(self):
        return self.numero or self.reference_instructeur or f"INS-{str(self.pk)[:8]}"

    @property
    def modifiable(self):
        return self.statut == self.Statut.BROUILLON

    def recalculer(self, sauver=True):
        total = sum((l.montant_htva for l in self.lignes.all()), ZERO)
        self.montant_htva = Decimal(total).quantize(R2)
        taux = self.taux_tva if self.regime_tva == RegimeTVAInstructeur.ASSUJETTI else Decimal("0")
        self.montant_tva = (self.montant_htva * Decimal(taux) / 100).quantize(R2)
        self.montant_tvac = (self.montant_htva + self.montant_tva).quantize(R2)
        if sauver:
            self.save(update_fields=["montant_htva", "montant_tva", "montant_tvac", "updated_at"])

    def prochain_numero(self):
        """Série distincte d'autofactures par instructeur et par année : AF-<initiales>-<année>-<n°>."""
        u = self.instructeur
        initiales = ((u.prenom or "?")[:1] + (u.nom or "?")[:2]).upper()
        annee = (self.date_facture or date.today()).year
        prefixe = f"AF-{initiales}{str(u.pk)[:4].upper()}-{annee}-"
        existants = FactureInstructeur.objects.filter(societe=self.societe, numero__startswith=prefixe)
        n = 0
        for num in existants.values_list("numero", flat=True):
            try:
                n = max(n, int(num.rsplit("-", 1)[1]))
            except (ValueError, IndexError):
                pass
        return f"{prefixe}{n + 1:03d}"

    # ------------------------------------------------------------------
    def ecritures(self):
        """Écritures PCMN : journal d'achats (+ paiement)."""
        lib = f"{_('Instructeur')} {self.instructeur.prenom} {self.instructeur.nom} – {self.piece}"
        L = [
            {"journal": "ACH", "date": self.date_facture, "compte": COMPTE_HONORAIRES,
             "intitule": _("Rétributions de tiers – honoraires (instructeurs)"),
             "libelle": lib, "debit": self.montant_htva, "credit": ZERO},
        ]
        if self.montant_tva:
            L.append({"journal": "ACH", "date": self.date_facture, "compte": COMPTE_TVA_DEDUCTIBLE,
                      "intitule": _("TVA à récupérer"), "libelle": lib, "debit": self.montant_tva, "credit": ZERO})
        L.append({"journal": "ACH", "date": self.date_facture, "compte": COMPTE_FOURNISSEURS,
                  "intitule": _("Fournisseurs"), "libelle": lib, "debit": ZERO, "credit": self.montant_tvac})
        if self.date_paiement:
            banque = self.compte_paiement.compte_pcmn if self.compte_paiement else COMPTE_BANQUE_DEFAUT
            L.append({"journal": "BQ", "date": self.date_paiement, "compte": COMPTE_FOURNISSEURS,
                      "intitule": _("Fournisseurs"), "libelle": lib, "debit": self.montant_tvac, "credit": ZERO})
            L.append({"journal": "BQ", "date": self.date_paiement, "compte": banque,
                      "intitule": _("Banque"), "libelle": lib, "debit": ZERO, "credit": self.montant_tvac})
        return L

    def ligne_tresorerie(self):
        return {
            "date": self.date_paiement,
            "libelle": f"{_('Facture instructeur')} {self.piece} – {self.instructeur.prenom} {self.instructeur.nom}",
            "entree": ZERO, "sortie": self.montant_tvac,
            "contrepartie": COMPTE_FOURNISSEURS, "piece": self.piece,
            "source": "instructeur", "objet": self, "ordre": 4,
        }


class LigneFactureInstructeur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facture = models.ForeignKey(FactureInstructeur, on_delete=models.CASCADE, related_name="lignes")
    location = models.ForeignKey("voiture_location.Location", on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="lignes_facture_instructeur", verbose_name=_("Location"))
    date = models.DateField(_("Date"), null=True, blank=True)
    description = models.CharField(_("Description"), max_length=255)
    heures = models.DecimalField(_("Heures"), max_digits=6, decimal_places=2, default=Decimal("1"),
                                 validators=[MinValueValidator(Decimal("0"))])
    prix_heure_htva = models.DecimalField(_("Prix / heure HTVA"), max_digits=10, decimal_places=2, default=ZERO,
                                          validators=[MinValueValidator(Decimal("0"))])
    montant_htva = models.DecimalField(_("Montant HTVA"), max_digits=12, decimal_places=2, default=ZERO)

    class Meta:
        verbose_name = _("Ligne de facture d'instructeur")
        verbose_name_plural = _("Lignes de facture d'instructeur")
        ordering = ["date", "description"]

    def save(self, *args, **kwargs):
        self.montant_htva = (Decimal(self.heures or 0) * Decimal(self.prix_heure_htva or 0)).quantize(R2)
        super().save(*args, **kwargs)

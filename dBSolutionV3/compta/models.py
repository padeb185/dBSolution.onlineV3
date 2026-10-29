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
    ("130000", _("Réserves")),
    ("140000", _("Bénéfice (perte) reporté(e)")),
    ("170000", _("Dettes à plus d'un an")),
    ("173000", _("Emprunts auprès d'établissements de crédit")),
    ("210000", _("Immobilisations incorporelles")),
    ("280000", _("Immobilisations financières")),
    ("220000", _("Terrains")),
    ("221000", _("Constructions")),
    ("230000", _("Installations, machines et outillage")),
    ("240000", _("Mobilier et matériel de bureau")),
    ("241000", _("Matériel roulant")),
    ("340000", _("Marchandises (stock)")),
    ("400000", _("Clients")),
    ("411000", _("TVA à récupérer")),
    ("440000", _("Fournisseurs")),
    ("451000", _("TVA à payer")),
    ("453000", _("Précomptes retenus")),
    ("454000", _("Office National de Sécurité Sociale")),
    ("455000", _("Rémunérations")),
    ("430000", _("Dettes financières à court terme")),
    ("480000", _("Dettes diverses")),
    ("460000", _("Acomptes reçus sur commandes")),
    ("489000", _("Dettes envers les propriétaires (reversements de locations)")),
    ("490000", _("Charges à reporter")),
    ("492000", _("Charges à imputer")),
    ("499000", _("Compte d'attente")),
    ("580000", _("Virements internes")),
    ("600000", _("Achats de marchandises")),
    ("610000", _("Services et biens divers")),
    ("613000", _("Rétributions de tiers – honoraires")),
    ("640000", _("Autres charges d'exploitation")),
    ("650000", _("Charges financières")),
    ("700000", _("Chiffre d'affaires – ventes")),
    ("670000", _("Impôts sur le résultat")),
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

        # Investissements et versements ONSS / précompte payés depuis ce compte
        for rel, champ in (("immobilisations", "date_paiement"), ("versements_sociaux", "date")):
            try:
                qs = getattr(self, rel).filter(**{f"{champ}__isnull": False})
                if debut:
                    qs = qs.filter(**{f"{champ}__gte": debut})
                if fin:
                    qs = qs.filter(**{f"{champ}__lte": fin})
                L += [o.ligne_tresorerie() for o in qs]
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
                client = p.facture.nom_client_courant() or ""
                L.append({
                    "date": p.date,
                    "libelle": (f"{_('Remboursement note de crédit')} {p.facture.numero or ''} {client}".strip() if p.montant < 0
                                else f"{_('Encaissement facture')} {p.facture.numero or ''} {client}".strip()),
                    "entree": p.montant if p.montant > 0 else ZERO,
                    "sortie": -p.montant if p.montant < 0 else ZERO,
                    "contrepartie": "400000", "piece": p.facture.numero or "",
                    "source": "facture", "objet": p, "ordre": 2,
                })
        except Exception:
            pass

        # Reversements aux propriétaires (locations) : sortie de caisse (espèces) ou de banque
        try:
            from voiture.voiture_location.models import ReversementLocation, StatutReversement
            reversements = ReversementLocation.objects.filter(
                location__societe=self.societe, statut=StatutReversement.PAYE, date_paiement__gte=bornes_debut)
            if fin:
                reversements = reversements.filter(date_paiement__lte=fin)
            if self.type == self.Type.CAISSE:
                reversements = reversements.filter(mode_paiement="ESPECES")
            else:
                reversements = reversements.exclude(mode_paiement="ESPECES")
            L += [r.ligne_tresorerie() for r in reversements]
        except Exception:
            pass

        # Acomptes de location reçus, pas encore repris sur une facture émise
        try:
            from facture.paiements import acomptes_locations_encaisses
            for a in acomptes_locations_encaisses(self.societe, debut=bornes_debut, fin=fin):
                if a.est_especes != (self.type == self.Type.CAISSE):
                    continue
                L.append({
                    "date": a.date, "libelle": f"{_('Acompte location')} – {a.location.nom_locataire}".strip(" –"),
                    "entree": a.montant, "sortie": ZERO,
                    "contrepartie": "400000" if a.facture else "460000", "piece": a.piece,
                    "source": "acompte", "objet": a, "ordre": 2,
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

            # Investissements et versements sociaux sans compte précisé → banque par défaut
            for modele, champ in ((Immobilisation, "date_paiement"), (VersementSocial, "date")):
                try:
                    qs = modele.objects.filter(**{"societe": self.societe, f"{champ}__isnull": False,
                                                  "compte_paiement__isnull": True, f"{champ}__gte": bornes_debut})
                    if fin:
                        qs = qs.filter(**{f"{champ}__lte": fin})
                    L += [o.ligne_tresorerie() for o in qs]
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


# ======================================================================
# IMMOBILISATIONS ET AMORTISSEMENTS (PCMN classe 2 – dotations 6302)
# ======================================================================
COMPTE_DOTATIONS = "630200"
COMPTE_PLUS_VALUE = "763000"
COMPTE_MOINS_VALUE = "663000"
COMPTE_CREANCES_DIVERSES = "416000"


class CategorieImmobilisation(models.TextChoices):
    TERRAIN = "TERRAIN", _("Terrains")
    IMMEUBLE = "IMMEUBLE", _("Constructions / immeubles")
    INSTALLATIONS = "INSTALLATIONS", _("Installations, machines et outillage")
    MOBILIER_BUREAU = "MOBILIER_BUREAU", _("Mobilier et matériel de bureau")
    MATERIEL_ROULANT = "MATERIEL_ROULANT", _("Matériel roulant")
    AUTRES = "AUTRES", _("Autres immobilisations corporelles")


# catégorie : (compte d'actif, compte des amortissements actés, durée par défaut en années)
COMPTES_IMMOBILISATIONS = {
    CategorieImmobilisation.TERRAIN: ("220000", None, 0),
    CategorieImmobilisation.IMMEUBLE: ("221000", "221900", 33),
    CategorieImmobilisation.INSTALLATIONS: ("230000", "230900", 10),
    CategorieImmobilisation.MOBILIER_BUREAU: ("240000", "240900", 5),
    CategorieImmobilisation.MATERIEL_ROULANT: ("241000", "241900", 5),
    CategorieImmobilisation.AUTRES: ("260000", "260900", 5),
}

INTITULES_COMPTES_IMMO = {
    "220000": _("Terrains"),
    "221000": _("Constructions"),
    "221900": _("Constructions – amortissements actés"),
    "230000": _("Installations, machines et outillage"),
    "230900": _("Installations, machines et outillage – amortissements actés"),
    "240000": _("Mobilier et matériel de bureau"),
    "240900": _("Mobilier et matériel de bureau – amortissements actés"),
    "241000": _("Matériel roulant"),
    "241900": _("Matériel roulant – amortissements actés"),
    "260000": _("Autres immobilisations corporelles"),
    "260900": _("Autres immobilisations corporelles – amortissements actés"),
    COMPTE_DOTATIONS: _("Dotations aux amortissements sur immobilisations corporelles"),
    COMPTE_PLUS_VALUE: _("Plus-values sur réalisation d'immobilisations corporelles"),
    COMPTE_MOINS_VALUE: _("Moins-values sur réalisation d'immobilisations corporelles"),
    COMPTE_CREANCES_DIVERSES: _("Créances diverses"),
}


class Immobilisation(models.Model):
    class Methode(models.TextChoices):
        LINEAIRE = "LINEAIRE", _("Linéaire")
        DEGRESSIF = "DEGRESSIF", _("Dégressif")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="immobilisations")
    categorie = models.CharField(_("Catégorie"), max_length=20, choices=CategorieImmobilisation.choices,
                                 default=CategorieImmobilisation.INSTALLATIONS)
    libelle = models.CharField(_("Libellé"), max_length=200, help_text=_("Ex. : pont élévateur, camionnette, bâtiment atelier…"))
    fournisseur = models.ForeignKey("fournisseur.Fournisseur", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="immobilisations", verbose_name=_("Fournisseur"))
    reference_facture = models.CharField(_("Référence de la facture"), max_length=100, blank=True)
    immatriculation = models.CharField(_("Immatriculation / n° de série"), max_length=50, blank=True)

    date_acquisition = models.DateField(_("Date d'acquisition"), default=date.today)
    date_mise_en_service = models.DateField(_("Date de mise en service"), null=True, blank=True,
                                            help_text=_("Vide : date d'acquisition."))
    valeur_acquisition = models.DecimalField(_("Valeur d'acquisition HTVA"), max_digits=12, decimal_places=2,
                                             validators=[MinValueValidator(Decimal("0"))])
    frais_accessoires = models.DecimalField(
        _("Frais accessoires et TVA non déductible"), max_digits=12, decimal_places=2, default=ZERO,
        validators=[MinValueValidator(Decimal("0"))],
        help_text=_("Transport, installation, frais d'acte… et part de TVA non déductible (ex. 50 % sur une voiture)."),
    )
    taux_tva = models.DecimalField(_("Taux de TVA (%)"), max_digits=5, decimal_places=2, default=Decimal("21.00"))
    tva_deductible = models.DecimalField(_("TVA déductible (%)"), max_digits=5, decimal_places=2, default=Decimal("100.00"))
    valeur_residuelle = models.DecimalField(_("Valeur résiduelle"), max_digits=12, decimal_places=2, default=ZERO,
                                            validators=[MinValueValidator(Decimal("0"))])

    methode = models.CharField(_("Méthode d'amortissement"), max_length=10, choices=Methode.choices,
                               default=Methode.LINEAIRE,
                               help_text=_("Le dégressif n'est plus admis fiscalement pour les sociétés (acquisitions depuis 2020) ni pour les voitures."))
    duree_annees = models.PositiveSmallIntegerField(_("Durée d'amortissement (années)"), default=5)
    prorata_temporis = models.BooleanField(_("Prorata temporis la première année"), default=True)
    compte_paiement = models.ForeignKey(CompteTresorerie, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name="immobilisations", verbose_name=_("Payée depuis le compte"))
    date_paiement = models.DateField(_("Date de paiement"), null=True, blank=True)

    date_cession = models.DateField(_("Date de cession / mise hors service"), null=True, blank=True)
    prix_cession = models.DecimalField(_("Prix de cession HTVA"), max_digits=12, decimal_places=2, null=True, blank=True)
    remarques = models.TextField(_("Remarques"), blank=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Immobilisation")
        verbose_name_plural = _("Immobilisations")
        ordering = ["categorie", "-date_acquisition"]

    def __str__(self):
        return f"{self.libelle} ({self.get_categorie_display()})"

    # ------------------------------------------------------------------
    @property
    def compte_actif(self):
        return COMPTES_IMMOBILISATIONS[self.categorie][0]

    @property
    def compte_amortissements(self):
        return COMPTES_IMMOBILISATIONS[self.categorie][1]

    @property
    def amortissable(self):
        return self.categorie != CategorieImmobilisation.TERRAIN and (self.duree_annees or 0) > 0

    @property
    def valeur_comptable_brute(self):
        return (Decimal(self.valeur_acquisition or 0) + Decimal(self.frais_accessoires or 0)).quantize(R2)

    @property
    def base_amortissable(self):
        return max(ZERO, self.valeur_comptable_brute - Decimal(self.valeur_residuelle or 0)).quantize(R2)

    @property
    def montant_tva(self):
        return (Decimal(self.valeur_acquisition or 0) * Decimal(self.taux_tva or 0) / 100).quantize(R2)

    @property
    def tva_recuperable(self):
        return (self.montant_tva * Decimal(self.tva_deductible or 0) / 100).quantize(R2)

    @property
    def total_tvac(self):
        return (Decimal(self.valeur_acquisition or 0) + self.montant_tva).quantize(R2)

    @property
    def taux_lineaire(self):
        return (Decimal("100") / self.duree_annees).quantize(Decimal("0.01")) if self.amortissable else ZERO

    @property
    def taux_degressif(self):
        return min(self.taux_lineaire * 2, Decimal("40")) if self.amortissable else ZERO

    @property
    def debut(self):
        return self.date_mise_en_service or self.date_acquisition

    def plan_amortissement(self):
        """[{annee, base, taux, dotation, cumul, vnc}] – exercices = années civiles."""
        if not self.amortissable or not self.base_amortissable:
            return []
        base = self.base_amortissable
        annee = self.debut.year
        fraction = Decimal(13 - self.debut.month) / 12 if self.prorata_temporis else Decimal("1")
        lineaire = base / self.duree_annees
        cumul = ZERO
        plan = []
        derniere_annee = self.date_cession.year - 1 if self.date_cession else None
        i = 0
        while cumul < base and i < self.duree_annees + 2:
            if derniere_annee is not None and annee > derniere_annee:
                break
            reste = base - cumul
            if self.methode == self.Methode.DEGRESSIF:
                deg = reste * self.taux_degressif / 100
                annees_restantes = max(Decimal(self.duree_annees) - Decimal(i) - (1 - fraction if i else 0), Decimal("1"))
                lin_reste = reste / annees_restantes
                dotation = max(deg, lin_reste)
                taux = self.taux_degressif if deg >= lin_reste else self.taux_lineaire
            else:
                dotation = lineaire
                taux = self.taux_lineaire
            if i == 0:
                dotation = dotation * fraction
            dotation = min(dotation, reste).quantize(R2)
            if dotation <= 0:
                break
            cumul += dotation
            plan.append({"annee": annee, "taux": taux, "dotation": dotation, "cumul": cumul,
                         "vnc": (self.valeur_comptable_brute - cumul).quantize(R2)})
            annee += 1
            i += 1
        return plan

    def dotation(self, annee):
        return next((p["dotation"] for p in self.plan_amortissement() if p["annee"] == annee), ZERO)

    def cumul_fin(self, annee):
        cumul = ZERO
        for p in self.plan_amortissement():
            if p["annee"] <= annee:
                cumul = p["cumul"]
        return cumul

    def vnc_fin(self, annee):
        if self.date_cession and self.date_cession.year <= annee:
            return ZERO
        if self.debut.year > annee:
            return ZERO
        return (self.valeur_comptable_brute - self.cumul_fin(annee)).quantize(R2)

    @property
    def vnc_actuelle(self):
        return self.vnc_fin(date.today().year - 1) if self.debut.year < date.today().year else self.valeur_comptable_brute

    @property
    def resultat_cession(self):
        if not self.date_cession:
            return None
        vnc = (self.valeur_comptable_brute - self.cumul_fin(self.date_cession.year - 1)).quantize(R2)
        return (Decimal(self.prix_cession or 0) - vnc).quantize(R2)

    # ------------------------------------------------------------------
    def ecritures(self, debut=None, fin=None):
        lib = f"{self.libelle}" + (f" – {self.reference_facture}" if self.reference_facture else "")
        L = []

        def ligne(journal, jour, compte, debit=ZERO, credit=ZERO, libelle=lib, intitule=None):
            if (debit or credit) and (debut is None or jour >= debut) and (fin is None or jour <= fin):
                L.append({"journal": journal, "date": jour, "compte": compte,
                          "intitule": intitule or INTITULES_COMPTES_IMMO.get(compte) or INTITULES_CONTREPARTIE.get(compte, ""),
                          "libelle": libelle, "debit": Decimal(debit).quantize(R2), "credit": Decimal(credit).quantize(R2),
                          "source": "immobilisation", "objet": self})

        # Acquisition (journal d'achats) – la TVA non déductible est comprise dans les frais accessoires
        ligne("ACH", self.date_acquisition, self.compte_actif, debit=self.valeur_comptable_brute)
        ligne("ACH", self.date_acquisition, COMPTE_TVA_DEDUCTIBLE, debit=self.tva_recuperable, intitule=_("TVA à récupérer"))
        ligne("ACH", self.date_acquisition, COMPTE_FOURNISSEURS,
              credit=self.valeur_comptable_brute + self.tva_recuperable, intitule=_("Fournisseurs"))
        if self.date_paiement:
            banque = self.compte_paiement.compte_pcmn if self.compte_paiement else COMPTE_BANQUE_DEFAUT
            ligne("BQ", self.date_paiement, COMPTE_FOURNISSEURS, debit=self.valeur_comptable_brute + self.tva_recuperable,
                  intitule=_("Fournisseurs"))
            ligne("BQ", self.date_paiement, banque, credit=self.valeur_comptable_brute + self.tva_recuperable,
                  intitule=_("Banque"))
        # Dotations annuelles (31/12)
        for p in self.plan_amortissement():
            jour = date(p["annee"], 12, 31)
            libd = f"{_('Amortissement')} {p['annee']} – {self.libelle}"
            ligne("OD", jour, COMPTE_DOTATIONS, debit=p["dotation"], libelle=libd)
            ligne("OD", jour, self.compte_amortissements, credit=p["dotation"], libelle=libd)
        # Cession
        if self.date_cession:
            cumul = self.cumul_fin(self.date_cession.year - 1)
            prix = Decimal(self.prix_cession or 0)
            libc = f"{_('Cession')} – {self.libelle}"
            if cumul and self.compte_amortissements:
                ligne("OD", self.date_cession, self.compte_amortissements, debit=cumul, libelle=libc)
            ligne("OD", self.date_cession, COMPTE_CREANCES_DIVERSES, debit=prix, libelle=libc)
            res = self.resultat_cession
            if res and res < 0:
                ligne("OD", self.date_cession, COMPTE_MOINS_VALUE, debit=-res, libelle=libc)
            ligne("OD", self.date_cession, self.compte_actif, credit=self.valeur_comptable_brute, libelle=libc)
            if res and res > 0:
                ligne("OD", self.date_cession, COMPTE_PLUS_VALUE, credit=res, libelle=libc)
        return L

    def ligne_tresorerie(self):
        montant = self.valeur_comptable_brute + self.tva_recuperable
        return {"date": self.date_paiement, "libelle": f"{_('Investissement')} – {self.libelle}",
                "entree": ZERO, "sortie": montant, "contrepartie": COMPTE_FOURNISSEURS,
                "piece": self.reference_facture or f"IMMO-{str(self.pk)[:8]}",
                "source": "immobilisation", "objet": self, "ordre": 5}


# ======================================================================
# STOCK – valorisation à l'inventaire et variation de stock (classe 3 / 609)
# ======================================================================
COMPTE_STOCK = "340000"
COMPTE_VARIATION_STOCK = "609400"


class ValorisationStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="valorisations_stock")
    date = models.DateField(_("Date de l'inventaire"), default=date.today)
    valeur_pieces = models.DecimalField(_("Pièces (quantité × prix d'achat)"), max_digits=14, decimal_places=2, default=ZERO)
    valeur_autres = models.DecimalField(_("Autres stocks (fluides, pneus…)"), max_digits=14, decimal_places=2, default=ZERO)
    remarques = models.TextField(_("Remarques"), blank=True)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)

    class Meta:
        verbose_name = _("Valorisation du stock")
        verbose_name_plural = _("Valorisations du stock")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date:%d/%m/%Y} – {self.total} €"

    @property
    def total(self):
        return (Decimal(self.valeur_pieces or 0) + Decimal(self.valeur_autres or 0)).quantize(R2)

    @property
    def precedente(self):
        return (ValorisationStock.objects.filter(societe=self.societe, date__lt=self.date).order_by("-date").first())

    @property
    def variation(self):
        prec = self.precedente
        return (self.total - (prec.total if prec else ZERO)).quantize(R2)

    def ecritures(self):
        v = self.variation
        lib = f"{_('Variation de stock')} – {_('inventaire du')} {self.date:%d/%m/%Y}"
        base = {"journal": "OD", "date": self.date, "libelle": lib, "source": "stock", "objet": self}
        if v > 0:
            return [dict(base, compte=COMPTE_STOCK, intitule=_("Marchandises (stock)"), debit=v, credit=ZERO),
                    dict(base, compte=COMPTE_VARIATION_STOCK, intitule=_("Variation de stock de marchandises"), debit=ZERO, credit=v)]
        if v < 0:
            return [dict(base, compte=COMPTE_VARIATION_STOCK, intitule=_("Variation de stock de marchandises"), debit=-v, credit=ZERO),
                    dict(base, compte=COMPTE_STOCK, intitule=_("Marchandises (stock)"), debit=ZERO, credit=-v)]
        return []


# ======================================================================
# SALAIRES – versements ONSS et précompte professionnel
# ======================================================================
class VersementSocial(models.Model):
    class Type(models.TextChoices):
        ONSS = "ONSS", _("ONSS (cotisations sociales)")
        PRECOMPTE = "PRECOMPTE", _("Précompte professionnel (SPF Finances)")

    COMPTES = {Type.ONSS: "454000", Type.PRECOMPTE: "453000"}

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="versements_sociaux")
    type = models.CharField(_("Type"), max_length=10, choices=Type.choices)
    periode = models.CharField(_("Période"), max_length=20, help_text=_("Ex. : 10/2026 ou T3/2026"))
    date = models.DateField(_("Date du paiement"), default=date.today)
    montant = models.DecimalField(_("Montant"), max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    compte_paiement = models.ForeignKey(CompteTresorerie, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name="versements_sociaux", verbose_name=_("Payé depuis le compte"),
                                        help_text=_("Vide : compte bancaire par défaut."))
    reference = models.CharField(_("Référence / communication"), max_length=100, blank=True)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)

    class Meta:
        verbose_name = _("Versement ONSS / précompte")
        verbose_name_plural = _("Versements ONSS / précompte")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.get_type_display()} {self.periode} – {self.montant} €"

    @property
    def compte_dette(self):
        return self.COMPTES[self.type]

    def ecritures(self):
        banque = self.compte_paiement.compte_pcmn if self.compte_paiement else COMPTE_BANQUE_DEFAUT
        lib = f"{self.get_type_display()} {self.periode}"
        base = {"journal": "BQ", "date": self.date, "libelle": lib, "source": "versement_social", "objet": self}
        return [dict(base, compte=self.compte_dette, intitule=INTITULES_CONTREPARTIE.get(self.compte_dette, ""), debit=self.montant, credit=ZERO),
                dict(base, compte=banque, intitule=_("Banque"), debit=ZERO, credit=self.montant)]

    def ligne_tresorerie(self):
        return {"date": self.date, "libelle": f"{self.get_type_display()} {self.periode}",
                "entree": ZERO, "sortie": self.montant, "contrepartie": self.compte_dette,
                "piece": self.reference or f"{self.type}-{self.periode}", "source": "versement_social",
                "objet": self, "ordre": 6}


# ======================================================================
# OPÉRATIONS DIVERSES (OD) – bilan d'ouverture, capital, emprunts, régularisations…
# ======================================================================
class OperationDiverse(models.Model):
    class Journal(models.TextChoices):
        OUVERTURE = "OUV", _("Écriture d'ouverture (bilan d'ouverture)")
        OD = "OD", _("Opération diverse")
        CLOTURE = "CLO", _("Écriture de clôture / affectation du résultat")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="operations_diverses")
    journal = models.CharField(_("Journal"), max_length=3, choices=Journal.choices, default=Journal.OD)
    date = models.DateField(_("Date"), default=date.today)
    piece = models.CharField(_("Pièce"), max_length=50, blank=True)
    libelle = models.CharField(_("Libellé"), max_length=255)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="operations_diverses", editable=False)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)

    class Meta:
        verbose_name = _("Opération diverse")
        verbose_name_plural = _("Opérations diverses")
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.date:%d/%m/%Y} – {self.libelle}"

    @property
    def total_debit(self):
        return sum((l.debit for l in self.lignes.all()), ZERO)

    @property
    def total_credit(self):
        return sum((l.credit for l in self.lignes.all()), ZERO)

    @property
    def equilibree(self):
        return self.total_debit == self.total_credit

    def ecritures(self):
        return [{"journal": self.journal, "date": self.date, "piece": self.piece or f"OD-{str(self.pk)[:8]}",
                 "compte": l.compte, "intitule": INTITULES_CONTREPARTIE.get(l.compte, ""),
                 "libelle": l.libelle or self.libelle, "debit": l.debit, "credit": l.credit}
                for l in self.lignes.all()]


class LigneOperationDiverse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operation = models.ForeignKey(OperationDiverse, on_delete=models.CASCADE, related_name="lignes")
    compte = models.CharField(_("Compte (PCMN)"), max_length=10)
    libelle = models.CharField(_("Libellé"), max_length=255, blank=True)
    debit = models.DecimalField(_("Débit"), max_digits=14, decimal_places=2, default=ZERO,
                                validators=[MinValueValidator(Decimal("0"))])
    credit = models.DecimalField(_("Crédit"), max_digits=14, decimal_places=2, default=ZERO,
                                 validators=[MinValueValidator(Decimal("0"))])

    class Meta:
        verbose_name = _("Ligne d'opération diverse")
        verbose_name_plural = _("Lignes d'opérations diverses")
        ordering = ["-debit", "compte"]


# =====================================================================
# DERNIER BILAN (établi par le comptable) : base des bilans générés ensuite
# =====================================================================
class BilanReference(models.Model):
    """
    Bilan (et compte de résultats) d'un exercice clôturé, encodé par rubriques BNB
    à partir des comptes annuels établis par le comptable.
    Il sert de colonne N-1 et de soldes d'ouverture pour les bilans générés par l'application.
    """

    class Schema(models.TextChoices):
        ABREGE = "ABREGE", _("Schéma abrégé")
        COMPLET = "COMPLET", _("Schéma complet")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="bilans_reference")
    annee = models.PositiveSmallIntegerField(_("Exercice clôturé au 31/12 de"))
    schema = models.CharField(_("Schéma"), max_length=10, choices=Schema.choices, default=Schema.ABREGE)
    etabli_par = models.CharField(_("Établi par (comptable / fiduciaire)"), max_length=150, blank=True)
    date_depot = models.DateField(_("Date de dépôt à la BNB"), null=True, blank=True)
    montants = models.JSONField(_("Montants par rubrique"), default=dict, blank=True)
    remarques = models.TextField(_("Remarques"), blank=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="bilans_reference", editable=False)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Bilan de référence")
        verbose_name_plural = _("Bilans de référence")
        ordering = ["-annee"]
        constraints = [
            models.UniqueConstraint(fields=["societe", "annee"], name="bilan_reference_unique_annee"),
        ]

    def __str__(self):
        return f"{_('Bilan')} {self.annee} ({self.get_schema_display()})"

    def montant(self, cle):
        try:
            return Decimal(str(self.montants.get(cle) or "0")).quantize(Decimal("0.01"))
        except Exception:
            return Decimal("0.00")

import uuid
from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from maintenance.choices import TVAConfig
from maintenance.models import Maintenance

DEUX = Decimal("0.01")


def arrondi(valeur):
    return Decimal(valeur or 0).quantize(DEUX, rounding=ROUND_HALF_UP)


class MaintenanceExterne(models.Model):
    """
    Maintenance réalisée par un garage officiel (atelier de la marque) :
    pièces et main-d'œuvre HTVA, taux de TVA du pays, montants TVA et totaux calculés.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="maintenances_externes",
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.PROTECT,
        related_name="maintenances_externes",
        verbose_name=_("Véhicule"),
    )

    garage = models.ForeignKey(
        "garage_officiel.GarageOfficiel",
        on_delete=models.PROTECT,
        related_name="maintenances_externes",
        verbose_name=_("Garage officiel"),
    )

    type_maintenance = models.CharField(
        _("Type de maintenance"),
        max_length=50,
        choices=Maintenance.TypeMaintenance.choices,
    )

    date_facture = models.DateField(_("Date de la facture"), default=timezone.localdate)
    numero_facture = models.CharField(_("Numéro de facture du garage"), max_length=50, blank=True)
    kilometrage = models.PositiveIntegerField(_("Kilométrage"), null=True, blank=True)

    pays = models.CharField(
        _("Pays de la TVA"),
        max_length=2,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
    )
    taux_tva = models.DecimalField(
        _("Taux de TVA (%)"),
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        help_text=_("Repris automatiquement du pays, modifiable."),
    )

    pieces_htva = models.DecimalField(
        _("Pièces HTVA (€)"), max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0)],
    )
    main_oeuvre_htva = models.DecimalField(
        _("Main-d'œuvre HTVA (€)"), max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0)],
    )

    # Montants calculés (enregistrés pour les listes, statistiques et la TVA)
    tva_pieces = models.DecimalField(_("TVA pièces (€)"), max_digits=10, decimal_places=2, default=0, editable=False)
    tva_main_oeuvre = models.DecimalField(_("TVA main-d'œuvre (€)"), max_digits=10, decimal_places=2, default=0, editable=False)
    total_pieces_tvac = models.DecimalField(_("Total pièces TVAC (€)"), max_digits=10, decimal_places=2, default=0, editable=False)
    total_main_oeuvre_tvac = models.DecimalField(_("Total main-d'œuvre TVAC (€)"), max_digits=10, decimal_places=2, default=0, editable=False)
    total_htva = models.DecimalField(_("Total HTVA (€)"), max_digits=10, decimal_places=2, default=0, editable=False)
    total_tva = models.DecimalField(_("Total TVA (€)"), max_digits=10, decimal_places=2, default=0, editable=False)
    total_tvac = models.DecimalField(_("Total TVAC (€)"), max_digits=10, decimal_places=2, default=0, editable=False)

    description = models.TextField(_("Description des travaux"), blank=True)

    # Paiement de la facture du garage (page « Factures à payer »)
    date_paiement = models.DateField(_("Date de paiement"), null=True, blank=True)

    # -------------------------------------------------------------
    # Compteurs du véhicule AVANT l'intervention (pour l'annulation)
    # -------------------------------------------------------------
    compteurs_appliques = models.BooleanField(default=False, editable=False)
    km_chassis_avant = models.PositiveIntegerField(null=True, blank=True, editable=False)
    km_moteur_avant = models.PositiveIntegerField(null=True, blank=True, editable=False)
    km_boite_avant = models.PositiveIntegerField(null=True, blank=True, editable=False)
    km_embrayage_avant = models.PositiveIntegerField(null=True, blank=True, editable=False)
    km_dernier_entretien_avant = models.PositiveIntegerField(null=True, blank=True, editable=False)
    km_remplacement_moteur_avant = models.PositiveIntegerField(null=True, blank=True, editable=False)
    km_remplacement_boite_avant = models.PositiveIntegerField(null=True, blank=True, editable=False)
    km_remplacement_embrayage_avant = models.PositiveIntegerField(null=True, blank=True, editable=False)
    variation_kilometres = models.PositiveIntegerField(_("Variation du kilométrage"), default=0, editable=False)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Maintenance externe")
        verbose_name_plural = _("Maintenances externes")
        ordering = ["-date_facture", "-created_at"]
        indexes = [models.Index(fields=["date_facture"])]

    def __str__(self):
        return f"{self.voiture_exemplaire} – {self.get_type_maintenance_display()} – {self.garage}"

    # -------------------------------------------------------------
    # Interface commune avec les factures d'achat (Factures à payer)
    # -------------------------------------------------------------
    @property
    def fournisseur(self):
        return self.garage

    @property
    def fournisseur_id(self):
        return self.garage_id

    @property
    def reference_facture(self):
        return self.numero_facture

    @property
    def montant_htva_total(self):
        return self.total_htva

    @property
    def montant_tva(self):
        return self.total_tva

    @property
    def est_paye(self):
        return self.date_paiement is not None

    @property
    def libelle_facture(self):
        immat = getattr(self.voiture_exemplaire, "immatriculation", "") or ""
        return f"{self.get_type_maintenance_display()} – {immat}".strip(" –")

    def calculer(self):
        if self.taux_tva is None:
            self.taux_tva = Decimal(str(TVAConfig.get_tva(self.pays)))
        taux = Decimal(self.taux_tva) / Decimal("100")
        self.pieces_htva = arrondi(self.pieces_htva)
        self.main_oeuvre_htva = arrondi(self.main_oeuvre_htva)
        self.tva_pieces = arrondi(self.pieces_htva * taux)
        self.tva_main_oeuvre = arrondi(self.main_oeuvre_htva * taux)
        self.total_pieces_tvac = arrondi(self.pieces_htva + self.tva_pieces)
        self.total_main_oeuvre_tvac = arrondi(self.main_oeuvre_htva + self.tva_main_oeuvre)
        self.total_htva = arrondi(self.pieces_htva + self.main_oeuvre_htva)
        self.total_tva = arrondi(self.tva_pieces + self.tva_main_oeuvre)
        self.total_tvac = arrondi(self.total_htva + self.total_tva)

    def save(self, *args, **kwargs):
        self.calculer()
        super().save(*args, **kwargs)

    # =============================================================
    # COMPTEURS DU VÉHICULE (même logique que les maintenances internes)
    # =============================================================
    TYPES_MOTEUR = {"REMPLACEMENT_MOTEUR"}
    TYPES_BOITE = {"remplacement_boite", "remplacement_bte_auto"}
    TYPES_EMBRAYAGE = {"EMBRAYAGE"}
    TYPES_ENTRETIEN = {"entretien", "checkup", "checkup_track"}

    CHAMPS_VEHICULE = [
        "kilometres_chassis", "kilometres_rollback", "date_derniere_intervention",
        "kilometres_moteur", "kilometres_boite", "kilometres_embrayage",
        "kilometres_moteur_rollback", "kilometres_boite_rollback", "kilometres_embrayage_rollback",
        "kilometres_remplacement_moteur", "kilometres_remplacement_boite",
        "kilometres_remplacement_embrayage", "kilometres_dernier_entretien",
        "kilometres_entretien_rollback", "variation_kilometres",
        "nombre_remplacements_moteurs", "nombre_remplacements_boites",
    ]

    @classmethod
    def effet_type(cls, type_maintenance):
        """Compteur remis à zéro par ce type de maintenance (moteur, boite, embrayage, entretien) ou None."""
        if type_maintenance in cls.TYPES_MOTEUR:
            return "moteur"
        if type_maintenance in cls.TYPES_BOITE:
            return "boite"
        if type_maintenance in cls.TYPES_EMBRAYAGE:
            return "embrayage"
        if type_maintenance in cls.TYPES_ENTRETIEN:
            return "entretien"
        return None

    def appliquer_compteurs(self):
        """
        Met à jour le véhicule après l'intervention :
        kilométrage châssis, date de dernière intervention, compteur
        moteur / boîte / embrayage remis à zéro, dernier entretien,
        nombre de moteurs / boîtes. Les valeurs AVANT sont mémorisées.
        """
        from voiture.voiture_exemplaire.models import VoitureExemplaire

        v = VoitureExemplaire.objects.select_for_update().get(pk=self.voiture_exemplaire_id)
        km = self.kilometrage if self.kilometrage is not None else (v.kilometres_chassis or 0)

        # Sauvegarde AVANT intervention
        self.km_chassis_avant = v.kilometres_chassis or 0
        self.km_moteur_avant = v.kilometres_moteur or 0
        self.km_boite_avant = v.kilometres_boite or 0
        self.km_embrayage_avant = v.kilometres_embrayage or 0
        self.km_dernier_entretien_avant = v.kilometres_dernier_entretien or 0
        self.km_remplacement_moteur_avant = v.kilometres_remplacement_moteur or 0
        self.km_remplacement_boite_avant = v.kilometres_remplacement_boite or 0
        self.km_remplacement_embrayage_avant = v.kilometres_remplacement_embrayage or 0
        self.variation_kilometres = max(0, km - self.km_chassis_avant)

        # Le kilométrage ne recule jamais
        v.kilometres_rollback = self.km_chassis_avant
        v.kilometres_moteur_rollback = self.km_moteur_avant
        v.kilometres_boite_rollback = self.km_boite_avant
        v.kilometres_embrayage_rollback = self.km_embrayage_avant
        v.kilometres_chassis = max(km, self.km_chassis_avant)
        if not v.date_derniere_intervention or self.date_facture >= v.date_derniere_intervention:
            v.date_derniere_intervention = self.date_facture

        effet = self.effet_type(self.type_maintenance)
        if effet == "moteur":
            v.kilometres_remplacement_moteur = km          # moteur neuf → 0 km
            v.nombre_remplacements_moteurs = (v.nombre_remplacements_moteurs or 0) + 1
        elif effet == "boite":
            v.kilometres_remplacement_boite = km           # boîte neuve → 0 km
            v.nombre_remplacements_boites = (v.nombre_remplacements_boites or 0) + 1
        elif effet == "embrayage":
            v.kilometres_remplacement_embrayage = km       # embrayage neuf → 0 km
        elif effet == "entretien":
            v.kilometres_entretien_rollback = self.km_dernier_entretien_avant
            v.kilometres_dernier_entretien = km

        v.update_kilometres()
        v.save(update_fields=self.CHAMPS_VEHICULE)
        self.compteurs_appliques = True

    def annuler_compteurs(self):
        """
        Annule l'effet de cette maintenance sur le véhicule (suppression / modification).
        Le kilométrage châssis n'est restauré que si aucune intervention
        plus récente ne l'a fait avancer depuis.
        """
        if not self.compteurs_appliques:
            return
        from voiture.voiture_exemplaire.models import VoitureExemplaire

        v = VoitureExemplaire.objects.select_for_update().get(pk=self.voiture_exemplaire_id)
        km = self.kilometrage or 0
        dernier = (v.kilometres_chassis or 0) == km

        if dernier and self.km_chassis_avant is not None:
            v.kilometres_chassis = self.km_chassis_avant

        effet = self.effet_type(self.type_maintenance)
        if effet == "moteur":
            if (v.kilometres_remplacement_moteur or 0) == km:
                v.kilometres_remplacement_moteur = self.km_remplacement_moteur_avant or 0
            v.nombre_remplacements_moteurs = max(0, (v.nombre_remplacements_moteurs or 0) - 1)
        elif effet == "boite":
            if (v.kilometres_remplacement_boite or 0) == km:
                v.kilometres_remplacement_boite = self.km_remplacement_boite_avant or 0
            v.nombre_remplacements_boites = max(0, (v.nombre_remplacements_boites or 0) - 1)
        elif effet == "embrayage":
            if (v.kilometres_remplacement_embrayage or 0) == km:
                v.kilometres_remplacement_embrayage = self.km_remplacement_embrayage_avant or 0
        elif effet == "entretien":
            if (v.kilometres_dernier_entretien or 0) == km:
                v.kilometres_dernier_entretien = self.km_dernier_entretien_avant or 0

        v.update_kilometres()
        v.save(update_fields=self.CHAMPS_VEHICULE)
        self.compteurs_appliques = False



# =====================================================================
# CARROSSERIE EXTERNE : devis puis facture d'un carrossier (application Carrosserie)
# =====================================================================
def chemin_document_carrosserie(instance, filename):
    """
    Nom de fichier imprévisible, rangé par société : le PDF n'est jamais servi directement,
    il passe par la vue protégée « maintenance_externe:carrosserie_document ».
    """
    from django.db import connection
    schema = getattr(connection, "schema_name", "") or "public"
    return f"prive/carrosserie/{schema}/{uuid.uuid4().hex}.pdf"


class CarrosserieExterne(models.Model):
    """Travaux de carrosserie confiés à un carrossier externe : devis, facture, prise en charge assurance."""

    class Statut(models.TextChoices):
        DEVIS_DEMANDE = "DEVIS_DEMANDE", _("Devis demandé")
        DEVIS_RECU = "DEVIS_RECU", _("Devis reçu")
        DEVIS_ACCEPTE = "DEVIS_ACCEPTE", _("Devis accepté")
        DEVIS_REFUSE = "DEVIS_REFUSE", _("Devis refusé")
        EN_COURS = "EN_COURS", _("Travaux en cours")
        FACTURE = "FACTURE", _("Facturé")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="carrosseries_externes")
    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire", on_delete=models.PROTECT,
        related_name="carrosseries_externes", verbose_name=_("Véhicule"),
    )
    carrossier = models.ForeignKey(
        "carrosserie.Carrosserie", on_delete=models.PROTECT, null=True,
        related_name="carrosseries_externes", verbose_name=_("Carrossier"),
    )
    statut = models.CharField(_("Statut"), max_length=15, choices=Statut.choices, default=Statut.DEVIS_DEMANDE)
    description = models.TextField(_("Dommages / travaux"), blank=True)
    kilometrage = models.PositiveIntegerField(_("Kilométrage"), null=True, blank=True)

    pays = models.CharField(_("Pays de la TVA"), max_length=2, choices=TVAConfig.PAYS_CHOICES,
                            default=TVAConfig.DEFAULT_PAYS)
    taux_tva = models.DecimalField(_("Taux de TVA (%)"), max_digits=5, decimal_places=2, blank=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   help_text=_("Repris automatiquement du pays, modifiable."))

    # --- Devis
    devis_numero = models.CharField(_("Numéro du devis"), max_length=50, blank=True)
    devis_date = models.DateField(_("Date du devis"), null=True, blank=True)
    devis_htva = models.DecimalField(_("Montant du devis HTVA (€)"), max_digits=10, decimal_places=2, default=0,
                                     validators=[MinValueValidator(0)])
    devis_pdf = models.FileField(_("Devis (PDF)"), upload_to=chemin_document_carrosserie, null=True, blank=True)

    # --- Facture
    facture_numero = models.CharField(_("Numéro de facture"), max_length=50, blank=True)
    facture_date = models.DateField(_("Date de la facture"), null=True, blank=True)
    pieces_htva = models.DecimalField(_("Pièces HTVA (€)"), max_digits=10, decimal_places=2, default=0,
                                      validators=[MinValueValidator(0)])
    peinture_htva = models.DecimalField(_("Peinture / ingrédients HTVA (€)"), max_digits=10, decimal_places=2,
                                        default=0, validators=[MinValueValidator(0)])
    main_oeuvre_htva = models.DecimalField(_("Main-d'œuvre HTVA (€)"), max_digits=10, decimal_places=2, default=0,
                                           validators=[MinValueValidator(0)])
    facture_pdf = models.FileField(_("Facture (PDF)"), upload_to=chemin_document_carrosserie, null=True, blank=True)

    # --- Montants calculés
    total_htva = models.DecimalField(_("Total HTVA (€)"), max_digits=10, decimal_places=2, default=0, editable=False)
    total_tva = models.DecimalField(_("Total TVA (€)"), max_digits=10, decimal_places=2, default=0, editable=False)
    total_tvac = models.DecimalField(_("Total TVAC (€)"), max_digits=10, decimal_places=2, default=0, editable=False)

    # --- Assurance
    prise_en_charge_assurance = models.BooleanField(_("Prise en charge par l'assurance"), default=False)
    sinistre = models.ForeignKey(
        "assurance_police.Sinistre", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="carrosseries_externes", verbose_name=_("Sinistre"),
    )
    numero_sinistre = models.CharField(_("Numéro de sinistre (assureur)"), max_length=60, blank=True)
    franchise = models.DecimalField(_("Franchise (€)"), max_digits=10, decimal_places=2, default=0,
                                    validators=[MinValueValidator(0)])
    montant_assurance = models.DecimalField(_("Montant pris en charge TVAC (€)"), max_digits=10, decimal_places=2,
                                            default=0, validators=[MinValueValidator(0)])
    assurance_paie_carrossier = models.BooleanField(
        _("L'assurance paie directement le carrossier"), default=True,
        help_text=_("Coché : seul le reste à charge est à payer au carrossier."),
    )

    # --- Paiement (page « Factures à payer »)
    date_paiement = models.DateField(_("Date de paiement"), null=True, blank=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Carrosserie externe")
        verbose_name_plural = _("Carrosseries externes")
        ordering = ["-facture_date", "-devis_date", "-created_at"]

    def __str__(self):
        return f"{self.voiture_exemplaire} – {_('Carrosserie')} – {self.carrossier}"

    # ------------------------------------------------------------------ calculs
    def calculer(self):
        if self.taux_tva is None:
            self.taux_tva = Decimal(str(TVAConfig.get_tva(self.pays)))
        self.total_htva = arrondi(Decimal(self.pieces_htva or 0) + Decimal(self.peinture_htva or 0)
                                  + Decimal(self.main_oeuvre_htva or 0))
        self.total_tva = arrondi(self.total_htva * Decimal(self.taux_tva) / Decimal("100"))
        self.total_tvac = arrondi(self.total_htva + self.total_tva)

    def save(self, *args, **kwargs):
        self.calculer()
        if self.facture_numero or self.facture_date:
            if self.statut not in (self.Statut.FACTURE,):
                self.statut = self.Statut.FACTURE
        super().save(*args, **kwargs)

    @property
    def est_facturee(self):
        return bool(self.facture_numero or self.facture_date)

    @property
    def devis_tvac(self):
        taux = Decimal(self.taux_tva if self.taux_tva is not None else TVAConfig.get_tva(self.pays))
        return arrondi(Decimal(self.devis_htva or 0) * (1 + taux / Decimal("100")))

    @property
    def ecart_devis_htva(self):
        """Facture − devis (HTVA) ; None tant qu'il manque l'un des deux."""
        if not self.est_facturee or not self.devis_htva:
            return None
        return arrondi(self.total_htva - Decimal(self.devis_htva))

    @property
    def reste_a_charge_tvac(self):
        """Coût TVAC pour la société après intervention de l'assurance (jamais négatif)."""
        if not self.prise_en_charge_assurance:
            return self.total_tvac
        return max(Decimal("0.00"), arrondi(self.total_tvac - Decimal(self.montant_assurance or 0)))

    @property
    def reste_a_charge_htva(self):
        taux = Decimal(self.taux_tva or 0)
        return arrondi(self.reste_a_charge_tvac / (1 + taux / Decimal("100"))) if taux else self.reste_a_charge_tvac

    # ------------------------------------------------------------------ interface « Factures à payer »
    @property
    def fournisseur(self):
        """Le carrossier tient lieu de fournisseur (même interface que les factures d'achat)."""
        return self.carrossier

    @property
    def fournisseur_id(self):
        return self.carrossier_id

    @property
    def reference_facture(self):
        return self.facture_numero

    @property
    def date_facture(self):
        return self.facture_date

    @property
    def montant_htva_total(self):
        return self.total_htva

    @property
    def montant_tva(self):
        return self.total_tva

    @property
    def montant_a_payer(self):
        """Montant dû au carrossier : reste à charge si l'assurance le paie directement, sinon la facture."""
        if self.prise_en_charge_assurance and self.assurance_paie_carrossier:
            return self.reste_a_charge_tvac
        return self.total_tvac

    @property
    def est_paye(self):
        return self.date_paiement is not None

    @property
    def libelle_facture(self):
        immat = getattr(self.voiture_exemplaire, "immatriculation", "") or ""
        return f"{_('Carrosserie')} – {immat}".strip(" –")

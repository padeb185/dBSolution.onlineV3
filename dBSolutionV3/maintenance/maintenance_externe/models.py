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

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Maintenance externe")
        verbose_name_plural = _("Maintenances externes")
        ordering = ["-date_facture", "-created_at"]
        indexes = [models.Index(fields=["date_facture"])]

    def __str__(self):
        return f"{self.voiture_exemplaire} – {self.get_type_maintenance_display()} – {self.garage}"

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

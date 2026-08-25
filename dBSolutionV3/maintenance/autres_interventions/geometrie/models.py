from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import TVAConfig
from maintenance.models import Maintenance


class GeometrieVoiture(models.Model):


    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="geometrie",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="geometrie",
        verbose_name=_("Kilomètres checkup"),
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_geometrie = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment de la géometrie"),

    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    # Angles de suspension
    carrossage_avant_droit = models.DecimalField(
        verbose_name="Carrossage avant droit (°)",
        max_digits=3,
        decimal_places=2,
        default=0.00,
    )

    carrossage_avant_gauche = models.DecimalField(
        verbose_name="Carrossage avant gauche (°)",
        max_digits=3,
        decimal_places=2,
        default=0.00,
    )

    carrossage_arriere_droit = models.DecimalField(
        verbose_name="Carrossage arrière droit (°)",
        max_digits=3,
        decimal_places=2,
        default=0.00,
    )

    carrossage_arriere_gauche = models.DecimalField(
        verbose_name="Carrossage arrière gauche (°)",
        max_digits=3,
        decimal_places=2,
        default=0.00,

    )

    chasse_droite = models.DecimalField(
        verbose_name="Chasse à droite (°)",
        max_digits=3,
        decimal_places=2,
        default=0.00,
    )

    chasse_gauche = models.DecimalField(
        verbose_name="Chasse à gauche (°)",
        max_digits=3,
        decimal_places=2,
        default=0.00,
    )

    pincement_avant_droit = models.DecimalField(
        verbose_name="Pincement avant droit (°)",
        max_digits=3,
        decimal_places=2,
        default=0.00,
    )

    pincement_avant_gauche = models.DecimalField(
        verbose_name="Pincement avant gauche (°)",
        max_digits=3,
        decimal_places=2,
        default=0.00,
    )

    pincement_arriere_droit = models.DecimalField(
        verbose_name="Pincement arrière droit (°)",
        max_digits=3,
        decimal_places=2,
        default=0.00,
    )

    pincement_arriere_gauche = models.DecimalField(
        verbose_name="Pincement arrière gauche (°)",
        max_digits=3,
        decimal_places=2,
        default=0.00,
    )

    poussee_arriere = models.DecimalField(
        verbose_name="Poussée du train arrière (°)",
        max_digits=4,
        decimal_places=2,
        default=0.00,
    )

    angle_pivot = models.DecimalField(
        verbose_name="Angle pivot (°)",
        max_digits=4,
        decimal_places=2,
        default=0.00,
    )

    # Suspension
    hauteur_caisse = models.FloatField(null=True, blank=True, verbose_name=_("Hauteur de caisse (mm)"))

    debattement_suspension_avant = models.FloatField(null=True, blank=True, verbose_name=_("Débattement avant (mm)"))
    debattement_suspension_arriere = models.FloatField(null=True, blank=True, verbose_name=_("Débattement arrière (mm)"))

    raideur_ressort_avant = models.FloatField(null=True, blank=True, verbose_name=_("Raideur ressort avant"))
    raideur_ressort_arriere = models.FloatField(null=True, blank=True, verbose_name=_("Raideur ressort arrière"))

    amortisseur_marque = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Marque des amortisseurs"))

    amortissement_avant_rebond = models.IntegerField(
        verbose_name=_("Amortissement avant rebond"),
        null=True, blank=True
    )

    amortissement_avant_compression = models.IntegerField(
        verbose_name=_("Amortissement avant compression"),
        null=True, blank=True
    )

    amortissement_arriere_rebond = models.IntegerField(
        verbose_name=_("Amortissement arrière rebond"),
        null=True, blank=True
    )

    amortissement_arriere_compression = models.IntegerField(
        verbose_name=_("Amortissement arrière compression"),
        null=True, blank=True
    )

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]
    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="JAUNE",
        verbose_name=_("État visuel / Tag"),
    )

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geometrie",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="geometrie"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="geometrie"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    date = models.DateTimeField(auto_now_add=True,blank=True, null=True, verbose_name=_("Date"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_geometrie is not None:
            if self.kilometrage_geometrie < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_geometrie': _(
                        f"Le kilométrage de la geometrie ({self.kilometrage_geometrie}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):

        # =========================
        # TECHNICIEN
        # =========================
        if not self.tech_technicien_id and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # =========================
        # RÉCUPÉRATION DU VÉHICULE
        # =========================
        voiture = None
        ancien_kilometrage = 0

        if self.voiture_exemplaire_id:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            ancien_kilometrage = (
                    voiture.kilometres_chassis or 0
            )

            # Snapshot AVANT intervention
            self.kilometres_chassis = ancien_kilometrage

        # =========================
        # CALCUL VARIATION
        # =========================
        if self.kilometrage_geometrie is not None:

            self.kilometrage_variation = (
                    self.kilometrage_geometrie
                    - ancien_kilometrage
            )

        else:
            self.kilometrage_variation = 0

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = (
                    _("Géométrie")
                    + " "
                    + str(self.voiture_exemplaire)
            )

            self.main_oeuvre.descriptif = task_name

            self.main_oeuvre.save(
                update_fields=["descriptif"]
            )

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = (
                Maintenance.TypeMaintenance.GEOMETRIE
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            self.maintenance.kilometres_chassis = (
                self.kilometrage_geometrie
                if self.kilometrage_geometrie is not None
                else ancien_kilometrage
            )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAUVEGARDE ÉCHAPPEMENT
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if (
                voiture is not None
                and self.kilometrage_geometrie is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_geometrie
            )

            ancien_km_voiture = int(
                voiture.kilometres_chassis or 0
            )

            if nouveau_kilometrage >= ancien_km_voiture:
                voiture.kilometres_chassis = (
                    nouveau_kilometrage
                )

                voiture.save(
                    update_fields=[
                        "kilometres_chassis"
                    ]
                )

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle Géometrie - {self.voiture_exemplaire.id}"
        return "Contrôle géometrie - non défini"

    class Meta:
        verbose_name = _("Contrôle Géometrie")
        verbose_name_plural = _("Contrôles Géometrie")

        # ======================================================
        # MAIN-D'ŒUVRE
        # ======================================================

    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        heures, minutes = divmod(temps_minutes, 60)

        return f"{heures}h{minutes:02d}"

    @property
    def taux_horaire_main_oeuvre(self):
        if (
                self.main_oeuvre
                and self.main_oeuvre.taux_horaire is not None
        ):
            return self.main_oeuvre.taux_horaire

        return Decimal("0.00")

    @property
    def cout_main_oeuvre(self):
        if not self.main_oeuvre:
            return Decimal("0.00")

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        taux_horaire = (
                self.main_oeuvre.taux_horaire or Decimal("0.00")
        )

        cout = (
                Decimal(str(temps_minutes))
                / Decimal("60")
                * Decimal(str(taux_horaire))
        )

        return cout.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()

        return (
                rapport["total_general"]
                + self.cout_main_oeuvre
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    def generer_rapport_remplacement(self):


        total_pieces = Decimal("0.00")
        cout_main_oeuvre = Decimal(str(self.cout_main_oeuvre or 0))

        return {
            "lignes": [],
            "total_pieces": total_pieces,
            "cout_main_oeuvre": cout_main_oeuvre,
            "total_general": total_pieces + cout_main_oeuvre,
        }
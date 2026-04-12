from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.models import Maintenance


class GeometrieVoiture(models.Model):
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

    kilometres_chassis = models.PositiveIntegerField(default=0)

    kilometrage_geometrie = models.PositiveIntegerField(
        _("Kilométrage au moment de la géometrie"),
        null=True,
        blank=True
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
        ("WHITE", _("Blanc")),
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]
    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="WHITE",
        verbose_name=_("État visuel / Tag"),
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
        # Mise à jour du kilométrage de la voiture si nécessaire
        if self.voiture_exemplaire and self.kilometrage_geometrie:
            if self.kilometrage_geometrie > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_geometrie
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        super().save(*args, **kwargs)

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle Géometrie - {self.voiture_exemplaire.id}"
        return "Contrôle géometrie - non défini"

    class Meta:
        verbose_name = _("Contrôle Géometrie")
        verbose_name_plural = _("Contrôles Géometrie")
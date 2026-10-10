from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from maintenance.models import Maintenance


class AgendaTache(models.Model):
    """Une maintenance planifiée pour un jour donné."""

    class Statut(models.TextChoices):
        A_FAIRE = "A_FAIRE", _("À faire")
        EN_COURS = "EN_COURS", _("En cours")
        FAIT = "FAIT", _("Fait")

    date = models.DateField(_("Date"), db_index=True)

    type_maintenance = models.CharField(
        _("Maintenance"),
        max_length=50,
        choices=Maintenance.TypeMaintenance.choices,
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="agenda_taches",
        verbose_name=_("Véhicule"),
    )

    technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agenda_taches",
        verbose_name=_("Technicien"),
    )

    tag = models.CharField(
        _("Tag"),
        max_length=10,
        choices=Maintenance.Tag.choices,
        default=Maintenance.Tag.JAUNE,
    )

    # Pour toutes les maintenances sauf le checkup piste
    statut = models.CharField(
        _("Statut"),
        max_length=10,
        choices=Statut.choices,
        default=Statut.A_FAIRE,
    )

    # Uniquement pour le checkup piste
    prete_pour = models.CharField(
        _("Prête pour"),
        max_length=255,
        blank=True,
        help_text=_("Ex. : roulage Spa-Francorchamps du 18/10"),
    )

    remarques = models.TextField(_("Remarques"), blank=True)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="agenda_taches",
        verbose_name=_("Société"),
    )

    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agenda_taches_creees",
        verbose_name=_("Créé par"),
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Tâche d'agenda")
        verbose_name_plural = _("Agenda")
        ordering = ["date", "technicien__nom", "id"]

    def __str__(self):
        return f"{self.date:%d/%m/%Y} - {self.get_type_maintenance_display()} - {self.voiture_exemplaire}"

    @property
    def est_checkup_track(self):
        return self.type_maintenance == Maintenance.TypeMaintenance.CHECKUP_TRACK

    @property
    def immatriculation(self):
        return getattr(self.voiture_exemplaire, "immatriculation", "") or ""

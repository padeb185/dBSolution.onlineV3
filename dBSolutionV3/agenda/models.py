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

    # Tâche créée automatiquement depuis une location (checkup piste)
    location = models.OneToOneField(
        "voiture_location.Location",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="agenda_tache",
        verbose_name=_("Location"),
    )

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
    def est_terminee(self):
        """Checkup piste : terminé quand le tag est vert. Autres : statut « Fait »."""
        if self.est_checkup_track:
            return self.tag == Maintenance.Tag.VERT
        return self.statut == self.Statut.FAIT

    @property
    def immatriculation(self):
        return getattr(self.voiture_exemplaire, "immatriculation", "") or ""


class AgendaLocation(models.Model):
    """
    Suivi d'une location dans l'agenda :
    sortie (si le checkup piste est vert) puis contrôle au retour.
    """

    class Controle(models.TextChoices):
        OK = "OK", _("OK")
        PROBLEME = "PROBLEME", _("Problème")

    class NiveauEssence(models.TextChoices):
        RESERVE = "RESERVE", _("Réserve")
        QUART = "1_4", _("1/4")
        DEMI = "1_2", _("1/2")
        TROIS_QUARTS = "3_4", _("3/4")
        PLEIN = "PLEIN", _("Plein")

    location = models.OneToOneField(
        "voiture_location.Location",
        on_delete=models.CASCADE,
        related_name="agenda_location",
        verbose_name=_("Location"),
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="agenda_locations",
        verbose_name=_("Société"),
    )

    # ---- Sortie
    kilometrage_avant = models.PositiveIntegerField(_("Kilométrage avant location"), null=True, blank=True)
    niveau_essence_depart = models.CharField(
        _("Niveau d'essence au départ"), max_length=10, choices=NiveauEssence.choices, blank=True,
    )
    sortie_effectuee = models.BooleanField(_("Sortie effectuée"), default=False)
    sortie_le = models.DateTimeField(_("Sortie le"), null=True, blank=True)
    sortie_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="agenda_locations_sorties", verbose_name=_("Sortie validée par"),
    )

    # ---- Retour
    kilometrage_apres = models.PositiveIntegerField(_("Kilométrage après location"), null=True, blank=True)
    controle_carrosserie = models.CharField(
        _("Contrôle visuel carrosserie"), max_length=10, choices=Controle.choices, blank=True,
    )
    bruit_moteur = models.CharField(_("Bruit moteur"), max_length=10, choices=Controle.choices, blank=True)
    niveau_essence_retour = models.CharField(
        _("Niveau d'essence au retour"), max_length=10, choices=NiveauEssence.choices, blank=True,
    )
    tag_retour = models.CharField(
        _("Tag retour"), max_length=10, choices=Maintenance.Tag.choices, blank=True,
    )
    retour_effectue = models.BooleanField(_("Retour effectué"), default=False)
    retour_le = models.DateTimeField(_("Retour le"), null=True, blank=True)
    retour_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="agenda_locations_retours", verbose_name=_("Retour contrôlé par"),
    )

    remarques = models.TextField(_("Remarques"), blank=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Location (agenda)")
        verbose_name_plural = _("Agenda des locations")

    def __str__(self):
        return str(self.location)

    # ---------------------------------------------------------
    @property
    def checkup(self):
        """Checkup piste lié à la location (agenda maintenances)."""
        return getattr(self.location, "agenda_tache", None)

    @property
    def checkup_vert(self):
        c = self.checkup
        return bool(c and c.tag == Maintenance.Tag.VERT)

    @property
    def ok_pour_sortie(self):
        return self.checkup_vert and not self.sortie_effectuee

    @property
    def probleme_retour(self):
        return _controle_probleme(self.controle_carrosserie, self.bruit_moteur)

    @property
    def km_parcourus(self):
        if self.kilometrage_avant is not None and self.kilometrage_apres is not None:
            return max(0, self.kilometrage_apres - self.kilometrage_avant)
        return None

    @property
    def etat(self):
        """PREPARATION → OK_SORTIE → EN_LOCATION → RETOUR (tag jaune) / PROBLEME (tag rouge)."""
        if self.retour_effectue:
            return "PROBLEME" if self.tag_retour == Maintenance.Tag.ROUGE else "RETOUR"
        if self.sortie_effectuee:
            return "EN_LOCATION"
        return "OK_SORTIE" if self.checkup_vert else "PREPARATION"

    ETATS = {
        "PREPARATION": _("En préparation (checkup non vert)"),
        "OK_SORTIE": _("OK pour sortie"),
        "EN_LOCATION": _("En location"),
        "RETOUR": _("Rentrée – tag jaune"),
        "PROBLEME": _("Rentrée – problème (tag rouge)"),
    }

    @property
    def etat_display(self):
        return self.ETATS[self.etat]


def _controle_probleme(*valeurs):
    return any(v == AgendaLocation.Controle.PROBLEME for v in valeurs)

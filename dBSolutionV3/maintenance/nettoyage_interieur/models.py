from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.models import Maintenance
from utilisateurs.models import Utilisateur

from django.conf import settings


class NettoyageEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("A faire")
    FAIT = "FAIT", _("Fait")
    REPORTER = "REPORTER", _("Reporter")
    PROPRE = "PROPRE", _("Propre")




class NettoyageInterieur(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="nettoyages_interieur",
        verbose_name=_("Nettoyage Interieur"),
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="nettoyages_interieur",
        verbose_name=_("Véhicule")
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
    )

    kilometrage_net_int = models.PositiveIntegerField(
        _("Kilométrage au moment du Nettoyage intérieur"),
        null=True,
        blank=True
    )

    nettoyage_interieur_vitres =  models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Vitres")

    )
    nettoyage_interieur_pare_brise =  models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Pare-brise")
    )
    nettoyage_interieur_aspirateur =  models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Aspirateur")
    )
    nettoyage_interieur_interieur_portes = models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Ouvrants de portes")
    )
    nettoyage_interieur_tableau_de_bord =models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Tableau de bord")
    )
    nettoyage_interieur_plastiques = models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Plastiques")
    )

    nettoyage_interieur_console = models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Console centrale")
    )

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]

    tag_nettoyage_int = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="JAUNE",
        verbose_name=_("État visuel / Tag"),
    )

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    # Champ pour l’utilisateur affecté (technicien)
    tech_utilisateurs = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Utilisateur"),
        related_name="nettoyage_interieur"
    )

    tech_nom_technicien = models.CharField(
        _("Nom du technicien"),
        max_length=255,
        blank=True
    )

    tech_role_technicien = models.CharField(
        _("Rôle du technicien"),
        max_length=255,
        blank=True
    )

    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="nettoyages_interieur_societe"  # unique
    )

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Nettoyage intérieur")
        verbose_name_plural = _("Nettoyages intérieurs")

    def __str__(self):
        return f"Nettoyage intérieur – {self.voiture_exemplaire} ({self.date:%Y-%m-%d})"

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_net_int is not None:
            if self.kilometrage_net_int < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_net_int': _(
                        f"Le kilométrage du check-up ({self.kilometrage_net_int}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Mettre à jour le kilométrage de la voiture si nécessaire
        if self.voiture_exemplaire and self.kilometrage_net_int:
            if self.kilometrage_net_int > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_net_int
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie du kilométrage de la voiture
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        super().save(*args, **kwargs)




from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from utilisateurs.models import Utilisateur
from maintenance.models import Maintenance



class NettoyageEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("A faire")
    FAIT = "FAIT", _("Fait")
    REPORTER = "REPORTER", _("Reporter")
    PROPRE = "PROPRE", _("Propre")



class NettoyageExterieur(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="nettoyages_exterieur",
        verbose_name=_("Check up")
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="nettoyages_exterieur",
        verbose_name=_("Véhicule")
    )


    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    kilometrage_net_ext = models.PositiveIntegerField(
        _("Kilométrage au moment du Nettoyage extérieur"),
        null=True,
        blank=True
    )

    # --- Nettoyage extérieur ---
    nettoyage_exterieur_traces_gomme = models.CharField(max_length=25, choices=NettoyageEtat.choices,default=NettoyageEtat.A_FAIRE,verbose_name=_("Traces de gomme"))
    nettoyage_exterieur_carrosserie = models.CharField(max_length=25, choices=NettoyageEtat.choices,default=NettoyageEtat.A_FAIRE, verbose_name=_("Carrosserie"))
    nettoyage_exterieur_jantes = models.CharField(max_length=25, choices=NettoyageEtat.choices,default=NettoyageEtat.A_FAIRE, verbose_name=_("Jantes"))
    nettoyage_exterieur_sechage = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Séchage"))

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

    # Champ pour l’utilisateur affecté (utilisateur courant)
    tech_utilisateurs = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Utilisateur"),
        related_name="nettoyage_exterieur"
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
        related_name="nettoyage_exterieur"
    )


    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Nettoyage extérieur")
        verbose_name_plural = _("Nettoyages extérieurs")

    def __str__(self):
        return f"Nettoyage extérieur – {self.voiture_exemplaire} ({self.date:%Y-%m-%d})"


    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_net_ext is not None:
            if self.kilometrage_net_ext < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_checkup': _(
                        f"Le kilométrage du check-up ({self.kilometrage_net_ext}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_net_ext:
            if self.kilometrage_net_ext > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_net_ext
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        super().save(*args, **kwargs)


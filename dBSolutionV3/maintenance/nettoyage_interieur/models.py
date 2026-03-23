from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.models import Maintenance
from utilisateurs.models import Utilisateur


class NettoyageInterieur(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="nettoyages_interieur",
        verbose_name=_("Check up")
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="nettoyages_interieur",
        verbose_name=_("Véhicule")
    )



    vitres = models.BooleanField(default=False, verbose_name=_("Vitres"))
    pare_brise = models.BooleanField(default=False, verbose_name=_("Pare-brise"))
    aspirateur = models.BooleanField(default=False, verbose_name=_("Aspirateur"))
    interieur_portes = models.BooleanField(default=False, verbose_name=_("Intérieurs de porte"))
    tableau_de_bord = models.BooleanField(default=False, verbose_name=_("Tableau de bord"))
    plastiques = models.BooleanField(default=False, verbose_name=_("Plastiques"))

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

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    # Champ pour l’utilisateur affecté (technicien)
    tech_utilisateurs = models.ForeignKey(
        Utilisateur,
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




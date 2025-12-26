from django.db import models
from django.utils.translation import gettext_lazy as _

class EmplacementSilentBloc(models.TextChoices):
    AV = "AV", _("Avant")
    AR = "AR", _("Arrière")
    AVG = "AVG", _("Avant gauche")
    AVD = "AVD", _("Avant droit")
    ARG = "ARG", _("Arrière gauche")
    ARD = "ARD", _("Arrière droit")

class TypeSilentBloc(models.TextChoices):
    TRIANGLE = "TRIANGLE", _("Triangle")
    TRIANGLE_SUP = "TRIANGLE_SUP", _("Triangle supérieur")
    MULTI_BRAS = "MULTI_BRAS", _("Suspension multi bras")
    BARRE_STAB_AV = "BARRE_STAB_AV", _("Barre stabilisatrice AV")
    BARRE_STAB_AR = "BARRE_STAB_AR", _("Barre stabilisatrice AR")
    MOTEUR = "MOTEUR", _("Moteur")
    BOITE_VITESSE = "BOITE_VITESSE", _("Boite vitesse")
    PENDULAIRE = "PENDULAIRE", _("Pendulaire")

class SilentBloc(models.Model):
    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="silentblocs",
        verbose_name=_("Maintenance")
    )

    emplacement = models.CharField(
        max_length=10,
        choices=EmplacementSilentBloc.choices,
        verbose_name=_("Emplacement")
    )

    type_bloc = models.CharField(
        max_length=20,
        choices=TypeSilentBloc.choices,
        verbose_name=_("Type de silentbloc")
    )

    etat = models.CharField(
        max_length=10,
        choices=[("BON", "Bon"), ("USE", "Usé"), ("HS", "Hors service")],
        verbose_name=_("État")
    )

    commentaire = models.TextField(
        blank=True,
        verbose_name=_("Observation")
    )

    TAG_CHOICES = [
        ("VERT", "Vert"),
        ("JAUNE", "Jaune"),
        ("ROUGE", "Rouge"),
    ]

    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="VERT",
        verbose_name=_("État visuel / Tag")
    )

    date = models.DateTimeField(auto_now_add=True)

    def is_critique(self):
        return self.etat == "HS"  # ou autre logique critique

    def save(self, *args, **kwargs):
        if self.is_critique():
            self.tag = "ROUGE"
        super().save(*args, **kwargs)

    def __str__(self):
        return _("%(type)s - %(empl)s (%(etat)s)") % {
            "type": self.get_type_bloc_display(),
            "empl": self.get_emplacement_display(),
            "etat": self.etat,
        }

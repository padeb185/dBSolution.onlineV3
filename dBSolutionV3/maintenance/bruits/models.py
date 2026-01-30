from django.db import models
from django.utils.translation import gettext_lazy as _

class EmplacementBruit(models.TextChoices):
    AV = "AV", _("Avant")
    AR = "AR", _("Arrière")
    AVG = "AVG", _("Avant gauche")
    AVD = "AVD", _("Avant droit")
    ARG = "ARG", _("Arrière gauche")
    ARD = "ARD", _("Arrière droit")

class TypeBruit(models.TextChoices):
    ROULEMENT_ROUE = "ROULEMENT_ROUE", _("Roulement de roue")
    ROULEMENT_SUSPENSION = "ROULEMENT_SUSPENSION", _("Roulement de suspension")
    MOTEUR = "MOTEUR", _("Moteur")
    BOITE_VITESSE = "BOITE_VITESSE", _("Boîte de vitesse")
    PONT = "PONT", _("Pont")

class ControleBruit(models.Model):
    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="bruits",
        verbose_name=_("Maintenance")
    )

    emplacement = models.CharField(
        max_length=10,
        choices=EmplacementBruit.choices,
        verbose_name=_("Emplacement")
    )

    type_bruit = models.CharField(
        max_length=30,
        choices=TypeBruit.choices,
        verbose_name=_("Type de bruit")
    )

    niveau_bruit = models.CharField(
        max_length=10,
        choices=[("NORMAL", _("Normal")), ("ANORMAL", _("Anormal"))],
        default="NORMAL",
        verbose_name=_("Niveau de bruit")
    )

    commentaire = models.TextField(
        blank=True,
        verbose_name=_("Observation")
    )

    TAG_CHOICES = [
        ("VERT", "Vert"),
        ("JAUNE", "Jaune"),
        ("ROUGE", "Rouge"),  # critique
    ]
    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="VERT",
        verbose_name=_("Tag")
    )

    date = models.DateTimeField(auto_now_add=True)

    def is_critique(self):
        return self.niveau_bruit == "ANORMAL"

    def save(self, *args, **kwargs):
        if self.is_critique():
            self.tag = "ROUGE"
        super().save(*args, **kwargs)

    def __str__(self):
        return _("%(type)s - %(empl)s (%(niveau)s)") % {
            "type": self.get_type_bruit_display(),
            "empl": self.get_emplacement_display(),
            "niveau": self.niveau_bruit,
        }

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from piece.models import Piece


class TypeFluide(models.TextChoices):
    HUILE_MOTEUR = "HUILE_MOTEUR", _("Huile moteur")
    HUILE_BOITE = "HUILE_BOITE", _("Huile de boîte")
    HUILE_PONT = "HUILE_PONT", _("Huile de pont")
    LIQUIDE_REFROIDISSEMENT = "LDR", _("Liquide de refroidissement")
    LAVE_GLACE = "LAVE_GLACE", _("Lave-glace")
    LIQUIDE_FREIN = "LIQ_FREIN", _("Liquide de frein")
    HUILE_DIRECTION = "HUILE_DIR", _("Huile de direction")


class Fluide(Piece):
    type_fluide = models.CharField(
        max_length=30,
        choices=TypeFluide.choices,
        verbose_name=_("Type de fluide")
    )
    nom_fluide = models.CharField(
        max_length=100,
        verbose_name=_("Nom du fluide")
    )
    qualite_fluide = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Qualité du fluide")
    )

    class Meta:
        verbose_name = _("Fluide")
        verbose_name_plural = _("Fluides")

    def __str__(self):
        return _("%(nom)s (%(type)s)") % {
            "nom": self.nom_fluide,
            "type": self.get_type_fluide_display()
        }


class InventaireFluide(models.Model):
    fluide = models.ForeignKey(
        Fluide,
        on_delete=models.CASCADE,
        related_name="inventaires_fluide",
        verbose_name=_("Fluide")
    )
    variation = models.FloatField(
        help_text=_("+ entrée / - sortie (litres)"),
        verbose_name=_("Variation")
    )
    stock_apres = models.FloatField(
        default=0.0,
        verbose_name=_("Stock après")
    )
    commentaire = models.TextField(
        blank=True,
        verbose_name=_("Commentaire")
    )
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Date")
    )

    def save(self, *args, **kwargs):
        # Met à jour le stock du fluide
        self.fluide.quantite_stock += self.variation
        if self.variation < 0:
            self.fluide.quantite_utilisee += abs(self.variation)
        self.stock_apres = self.fluide.quantite_stock
        self.fluide.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return _("%(fluide)s : %(variation)s L") % {
            "fluide": self.fluide,
            "variation": self.variation
        }

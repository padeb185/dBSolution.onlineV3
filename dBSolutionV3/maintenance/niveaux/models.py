from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from piece.piece_fluides.models import InventaireFluide


class Niveau(models.Model):
    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="niveaux",
        verbose_name=_("Maintenance")
    )

    piece_fluides = models.ForeignKey(
        "piece_fluides.Fluide",
        on_delete=models.PROTECT,
        verbose_name=_("Fluide")
    )

    quantite_utilisee = models.FloatField(
        verbose_name=_("Quantité utilisée (L)"),
        help_text=_("Quantité ajoutée ou retirée")
    )

    commentaire = models.TextField(
        blank=True,
        verbose_name=_("Commentaire")
    )

    date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.quantite_utilisee == 0:
            raise ValidationError(_("La quantité ne peut pas être nulle."))

    def save(self, *args, **kwargs):


        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            InventaireFluide.objects.create(
                fluide=self.fluide,
                variation=-self.quantite_utilisee,
                commentaire=_(
                    "Maintenance %(id)s"
                ) % {"id": self.maintenance.id}
            )

    def __str__(self):
        return _(
            "%(maintenance)s – %(fluide)s (%(qte)s L)"
        ) % {
            "maintenance": self.maintenance,
            "fluide": self.fluide,
            "qte": self.quantite_utilisee
        }

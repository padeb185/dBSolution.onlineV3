from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from piece_fluides.models import Fluide, InventaireFluide, TypeFluide


class Niveau(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="niveaux",
        verbose_name=_("Maintenance")
    )

    piece_fluides = models.ForeignKey(
        "piece_fluides.Fluide",
        on_delete=models.CASCADE,
        verbose_name=_("Fluide")
    )

    quantite_utilisee = models.FloatField(
        verbose_name=_("Quantité utilisée (L)"),
        help_text=_("Quantité prélevée sur le stock"),
    )

    commentaire = models.TextField(
        blank=True,
        verbose_name=_("Commentaire")
    )

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Niveau de fluide")
        verbose_name_plural = _("Niveaux de fluide")

    def save(self, *args, **kwargs):
        is_creation = self._state.adding

        if is_creation:
            # 🔒 Sécurité : stock suffisant
            if self.fluide.quantite_stock < self.quantite_utilisee:
                raise ValueError(
                    _("Stock insuffisant pour %(fluide)s") % {"fluide": self.fluide}
                )

            # 🔁 Création du mouvement d’inventaire
            InventaireFluide.objects.create(
                fluide=self.fluide,
                variation=-self.quantite_utilisee,
                commentaire=_(
                    "Utilisation lors de la maintenance %(maintenance)s"
                ) % {"maintenance": self.maintenance},
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return _(
            "%(fluide)s - %(quantite)s L"
        ) % {
            "fluide": self.fluide,
            "quantite": self.quantite_utilisee,
        }

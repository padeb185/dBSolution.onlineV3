import uuid

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Diagnostic(models.Model):
    """
    Catalogue des codes défaut : pour une marque et un modèle,
    le code défaut (ex. P0301) et la pièce en défaut correspondante.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="diagnostics",
    )

    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.PROTECT,
        related_name="diagnostics",
        verbose_name=_("Marque"),
    )

    voiture_modele = models.ForeignKey(
        "voiture_modele.VoitureModele",
        on_delete=models.PROTECT,
        related_name="diagnostics",
        verbose_name=_("Modèle"),
    )

    code_defaut = models.CharField(
        max_length=20,
        verbose_name=_("Code défaut"),
        validators=[
            RegexValidator(
                regex=r"^[A-Z0-9\-]{2,20}$",
                message=_("Code défaut invalide (lettres majuscules, chiffres et tirets)."),
            )
        ],
        help_text=_("Ex. : P0301, U0100, 2C4F"),
    )

    piece_defaut = models.CharField(
        max_length=255,
        verbose_name=_("Pièce en défaut"),
        help_text=_("Ex. : bobine d'allumage cylindre 1"),
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description / solution"),
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Diagnostic")
        verbose_name_plural = _("Diagnostics")
        ordering = ["voiture_marque__nom_marque", "voiture_modele__nom_modele", "code_defaut"]
        constraints = [
            models.UniqueConstraint(
                fields=["societe", "voiture_modele", "code_defaut", "piece_defaut"],
                name="diagnostic_unique_modele_code_piece",
            )
        ]
        indexes = [
            models.Index(fields=["code_defaut"]),
        ]

    def __str__(self):
        return f"{self.voiture_marque.nom_marque} {self.voiture_modele} – {self.code_defaut} : {self.piece_defaut}"

    def clean(self):
        super().clean()
        if self.code_defaut:
            self.code_defaut = self.code_defaut.strip().upper()
        if self.piece_defaut:
            self.piece_defaut = self.piece_defaut.strip()
        # Le modèle doit appartenir à la marque choisie
        if self.voiture_modele_id and self.voiture_marque_id:
            if self.voiture_modele.voiture_marque_id != self.voiture_marque_id:
                raise ValidationError(
                    {"voiture_modele": _("Ce modèle n'appartient pas à la marque choisie.")}
                )

    def save(self, *args, **kwargs):
        if self.code_defaut:
            self.code_defaut = self.code_defaut.strip().upper()
        # Marque déduite du modèle si absente
        if self.voiture_modele_id and not self.voiture_marque_id:
            self.voiture_marque_id = self.voiture_modele.voiture_marque_id
        super().save(*args, **kwargs)

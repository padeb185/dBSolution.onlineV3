import uuid

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .pieces_defaut import PIECE_AUTRE, PIECES_DEFAUT_CHOICES


class Diagnostic(models.Model):
    """
    Code défaut relevé sur un exemplaire, avec la pièce en défaut
    choisie dans une liste par système (sonde lambda aval, vanne EGR...).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="diagnostics",
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.PROTECT,
        related_name="diagnostics",
        null=True,
        verbose_name=_("Véhicule"),
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
        max_length=80,
        choices=PIECES_DEFAUT_CHOICES,
        verbose_name=_("Pièce en défaut"),
    )

    piece_defaut_autre = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Autre pièce (préciser)"),
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
        ordering = [
            "voiture_exemplaire__voiture_marque__nom_marque",
            "voiture_exemplaire__voiture_modele__nom_modele",
            "voiture_exemplaire__immatriculation",
            "code_defaut",
        ]
        indexes = [
            models.Index(fields=["code_defaut"]),
            models.Index(fields=["piece_defaut"]),
        ]

    def __str__(self):
        return f"{self.voiture_exemplaire} – {self.code_defaut} : {self.piece_libelle}"

    @property
    def piece_libelle(self):
        if self.piece_defaut == PIECE_AUTRE and self.piece_defaut_autre:
            return self.piece_defaut_autre
        return self.get_piece_defaut_display()

    def clean(self):
        super().clean()
        if self.code_defaut:
            self.code_defaut = self.code_defaut.strip().upper()
        if self.piece_defaut == PIECE_AUTRE:
            if not (self.piece_defaut_autre or "").strip():
                raise ValidationError({"piece_defaut_autre": _("Précisez la pièce en défaut.")})
        else:
            self.piece_defaut_autre = None

    def save(self, *args, **kwargs):
        if self.code_defaut:
            self.code_defaut = self.code_defaut.strip().upper()
        super().save(*args, **kwargs)

import uuid
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .pieces_defaut import PIECE_AUTRE, PIECES_DEFAUT_CHOICES


class Diagnostic(models.Model):
    """Une séance de diagnostic sur un exemplaire (plusieurs codes défaut possibles)."""

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

    date_diagnostic = models.DateField(
        default=timezone.localdate,
        verbose_name=_("Date du diagnostic"),
    )

    kilometrage = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Kilométrage"),
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description / solution"),
    )

    # Facturation du diagnostic (main-d'œuvre)
    temps_minutes = models.PositiveIntegerField(
        _("Temps du diagnostic (minutes)"),
        default=0,
    )
    taux_horaire = models.DecimalField(
        _("Taux horaire HTVA (€)"),
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Diagnostic")
        verbose_name_plural = _("Diagnostics")
        ordering = ["-date_diagnostic", "-created_at"]

    def __str__(self):
        return f"{self.voiture_exemplaire} – {self.date_diagnostic:%d/%m/%Y}"

    @property
    def liste_codes(self):
        return ", ".join(c.code_defaut for c in self.codes.all())

    @property
    def temps_display(self):
        minutes = self.temps_minutes or 0
        return f"{minutes // 60}h{minutes % 60:02d}"

    @property
    def cout_htva(self):
        """Coût HTVA du diagnostic (temps × taux horaire, ou taux seul comme forfait si aucun temps)."""
        taux = Decimal(self.taux_horaire or 0)
        if self.temps_minutes:
            montant = Decimal(self.temps_minutes) / Decimal("60") * taux
        else:
            montant = taux
        return montant.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def factures_liees(self):
        return self.factures.all()


class DiagnosticCode(models.Model):
    """Un code défaut relevé lors d'un diagnostic, avec la pièce en défaut."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    diagnostic = models.ForeignKey(
        Diagnostic,
        on_delete=models.CASCADE,
        related_name="codes",
        verbose_name=_("Diagnostic"),
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

    ordre = models.PositiveSmallIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = _("Code défaut")
        verbose_name_plural = _("Codes défaut")
        ordering = ["ordre", "code_defaut"]
        indexes = [
            models.Index(fields=["code_defaut"]),
            models.Index(fields=["piece_defaut"]),
        ]

    def __str__(self):
        return f"{self.code_defaut} : {self.piece_libelle}"

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

from django.db import models
from django.utils.translation import gettext_lazy as _


class TypePieceControle(models.TextChoices):
    ROTULE_DIRECTION = "ROTULE_DIRECTION", _("Rotule de direction")
    ROTULE_SUSPENSION = "ROTULE_SUSPENSION", _("Rotule de suspension")
    BIELLETTE_BARRE_STAB = "BIELLETTE_BARRE_STAB", _("Biellette de barre stabilisatrice")
    BARRE_STABILISATRICE = "BARRE_STABILISATRICE", _("Barre stabilisatrice")
    AMORTISSEUR = "AMORTISSEUR", _("Amortisseur")
    ROULEMENT_ROUE = "ROULEMENT_ROUE", _("Roulement de roue")
    TRIANGLE = "TRIANGLE", _("Triangle")
    MULTI_BRAS = "MULTI_BRAS", _("Multi-bras")


class Emplacement(models.TextChoices):
    AVG = "AVG", _("Avant gauche")
    AVD = "AVD", _("Avant droit")
    ARG = "ARG", _("Arrière gauche")
    ARD = "ARD", _("Arrière droit")
    AV = "AV", _("Avant")
    AR = "AR", _("Arrière")
    SUP = "SUP", _("Supérieur")
    INF = "INF", _("Inférieur")


class EtatPiece(models.TextChoices):
    BON = "BON", _("Bon")
    USE = "USE", _("Usé")
    HS = "HS", _("Hors service")


class JeuPiece(models.Model):
    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="jeux_pieces",
        verbose_name=_("Maintenance"),
        default=1

    )

    vehicle = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Véhicule")
    )

    type_piece = models.CharField(
        max_length=50,
        choices=TypePieceControle.choices,
        verbose_name=_("Pièce contrôlée")
    )

    emplacement = models.CharField(
        max_length=10,
        choices=Emplacement.choices,
        verbose_name=_("Emplacement")
    )

    etat = models.CharField(
        max_length=10,
        choices=EtatPiece.choices,
        null=True,
        blank=True,
        verbose_name=_("État")
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
        verbose_name=_("État visuel / Tag")
    )

    commentaire = models.TextField(
        blank=True,
        verbose_name=_("Observation")
    )

    date = models.DateTimeField(auto_now_add=True)

    def is_critique(self):
        """Renvoie True si la pièce est critique (tag rouge)."""
        return self.tag == "ROUGE"

    def __str__(self):
        return _(
            "%(piece)s – %(empl)s (%(etat)s / %(tag)s)"
        ) % {
            "piece": self.get_type_piece_display(),
            "empl": self.get_emplacement_display(),
            "etat": self.get_etat_display() if self.etat else _("Non précisé"),
            "tag": self.tag
        }


class NoteMaintenance(models.Model):
    ROLE_CHOICES = [
        ("APPRENTI", _("Apprenti")),
        ("MECANICIEN", _("Mécanicien")),
        ("CHEF", _("Chef mécanicien")),
    ]

    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="notes",
        null=True,
    )

    auteur = models.ForeignKey(
        "utilisateurs.Utilisateur",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    note = models.TextField()

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note de {self.role} – {self.date.strftime('%Y-%m-%d %H:%M')}"

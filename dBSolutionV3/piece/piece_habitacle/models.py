from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece  # On suppose que ton modèle de base s'appelle Piece

class PieceHabitacle(Piece):
    """
    Modèle principal pour les pièces de l'habitacle
    """
    class Meta:
        verbose_name = _("Pièce habitacle")
        verbose_name_plural = _("Pièces habitacle")


# Sous-modèles spécifiques
class Siege(PieceHabitacle):
    TYPE_CHOICES = [
        ("conducteur", _("Siège conducteur")),
        ("passager", _("Siège passager")),
        ("ar_droit", _("Siège arrière droit")),
        ("ar_gauche", _("Siège arrière gauche")),
    ]
    type_siege = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name=_("Type de siège")
    )

    class Meta:
        verbose_name = _("Siège")
        verbose_name_plural = _("Sièges")

    def __str__(self):
        return f"{self.get_type_siege_display()} – {super().__str__()}"


class Volant(PieceHabitacle):
    class Meta:
        verbose_name = _("Volant")
        verbose_name_plural = _("Volants")


class GPS(PieceHabitacle):
    class Meta:
        verbose_name = _("GPS")
        verbose_name_plural = _("GPS")


class Radio(PieceHabitacle):
    class Meta:
        verbose_name = _("Radio")
        verbose_name_plural = _("Radios")


class Tapis(PieceHabitacle):
    class Meta:
        verbose_name = _("Tapis")
        verbose_name_plural = _("Tapis")


class CeintureSecurite(PieceHabitacle):
    class Meta:
        verbose_name = _("Ceinture de sécurité")
        verbose_name_plural = _("Ceintures de sécurité")


class Harnais(PieceHabitacle):
    class Meta:
        verbose_name = _("Harnais")
        verbose_name_plural = _("Harnais")


class CompteursCommodo(PieceHabitacle):
    class Meta:
        verbose_name = _("Compteurs / Commodo")
        verbose_name_plural = _("Compteurs / Commodo")


class Airbag(PieceHabitacle):
    POSITION_CHOICES = [
        ("conducteur", _("Conducteur")),
        ("passager", _("Passager")),
        ("lat_gauche", _("Latéral gauche")),
        ("lat_droit", _("Latéral droit")),
        ("siege_conducteur", _("Siège conducteur")),
        ("siege_passager", _("Siège passager")),
        ("sieges_ar_droit", _("Sièges arrière droit")),
        ("sieges_ar_gauche", _("Sièges arrière gauche")),
    ]
    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        verbose_name=_("Position de l'airbag")
    )

    class Meta:
        verbose_name = _("Airbag")
        verbose_name_plural = _("Airbags")

    def __str__(self):
        return f"{self.get_position_display()} – {super().__str__()}"

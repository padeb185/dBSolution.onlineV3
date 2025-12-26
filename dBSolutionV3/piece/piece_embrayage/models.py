from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class TypeEmbrayage(models.TextChoices):
    SIMPLE_DISQUE = "SIMPLE_DISQUE", _("Embrayage simple disque")
    DOUBLE_DISQUE = "DOUBLE_DISQUE", _("Embrayage double disque")
    HYDRAULIQUE = "HYDRAULIQUE", _("Embrayage hydraulique")


class ComposantEmbrayage(models.TextChoices):
    DISQUE = "DISQUE", _("Disque d'embrayage")
    PLATEAU_PRESSION = "PLATEAU_PRESSION", _("Plateau de pression")
    BUTEE = "BUTEE", _("Butée d'embrayage")
    MAITRE_CYLINDRE = "MAITRE_CYLINDRE", _("Maître-cylindre")
    ESCLAVE = "ESCLAVE", _("Cylindre esclave")
    LEVIER = "LEVIER", _("Levier / fourchette")
    RESSORT = "RESSORT", _("Ressort")


class Embrayage(Piece):
    type_embrayage = models.CharField(
        max_length=20,
        choices=TypeEmbrayage.choices,
        verbose_name=_("Type d'embrayage")
    )

    # Relation avec les boîtes mécaniques compatibles
    boites_mecaniques = models.ManyToManyField(
        "piece_boite.BoiteMecanique",
        related_name="embrayages",
        blank=True,
        verbose_name=_("Boîtes mécaniques compatibles")
    )

    # Composants principaux
    disque = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Disque d'embrayage")
    )

    plateau = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Plateau d'embrayage")
    )

    butee = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Butée d'embrayage")
    )

    composants = models.JSONField(
        default=list,
        help_text=_("Liste des composants présents dans cet embrayage"),
        verbose_name=_("Composants")
    )

    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="embrayages",
        blank=True
    )

    class Meta:
        verbose_name = _("Embrayage")
        verbose_name_plural = _("Embrayages")

    def __str__(self):
        return f"{self.get_type_embrayage_display()} – {super().__str__()}"

    def add_composant(self, composant):
        """Ajouter un composant à l'embrayage"""
        if composant not in self.composants:
            self.composants.append(composant)
            self.save()

    def remove_composant(self, composant):
        """Supprimer un composant de l'embrayage"""
        if composant in self.composants:
            self.composants.remove(composant)
            self.save()

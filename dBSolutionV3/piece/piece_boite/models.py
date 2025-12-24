from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


# ⚙️ Boîte mécanique
class BoiteMecanique(Piece):

    NB_VITESSES_CHOICES = [
        (5, _("5 vitesses")),
        (6, _("6 vitesses")),
        (7, _("7 vitesses")),
    ]

    nb_vitesses = models.IntegerField(
        choices=NB_VITESSES_CHOICES,
        verbose_name=_("Nombre de vitesses")
    )

    embrayage = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Embrayage")
    )

    disque_embrayage = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Disque d’embrayage")
    )

    plateau_embrayage = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Plateau d’embrayage")
    )

    butee_embrayage = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Butée d’embrayage")
    )

    pignon = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Pignon")
    )

    synchro = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Synchroniseur")
    )

    arbre_principal = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Arbre principal")
    )

    arbre_secondaire = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Arbre secondaire")
    )

    fourchette_vitesse = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Fourchette de vitesse")
    )

    tringlerie = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Tringlerie")
    )

    huile = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Huile de boîte")
    )

    class Meta:
        verbose_name = _("Boîte mécanique")
        verbose_name_plural = _("Boîtes mécaniques")

    def __str__(self):
        return _("Boîte mécanique %(vitesses)s vitesses") % {
            "vitesses": self.nb_vitesses
        }


# 🔁 Boîte automatique
class BoiteAutomatique(Piece):

    NB_VITESSES_CHOICES = [
        (4, _("4 vitesses")),
        (5, _("5 vitesses")),
        (6, _("6 vitesses")),
        (8, _("8 vitesses")),
    ]

    nb_vitesses = models.IntegerField(
        choices=NB_VITESSES_CHOICES,
        verbose_name=_("Nombre de vitesses")
    )

    convertisseur_torque = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Convertisseur de couple")
    )

    embrayage_hydraulique = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Embrayage hydraulique")
    )

    train_planetaire = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Train planétaire")
    )

    frein_planetaire = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Frein planétaire")
    )

    piston = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Piston")
    )

    valve_body = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Bloc hydraulique")
    )

    solenoides = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Solénoïdes")
    )

    huile_transmission = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Huile de transmission")
    )

    class Meta:
        verbose_name = _("Boîte automatique")
        verbose_name_plural = _("Boîtes automatiques")

    def __str__(self):
        return _("Boîte automatique %(vitesses)s vitesses") % {
            "vitesses": self.nb_vitesses
        }

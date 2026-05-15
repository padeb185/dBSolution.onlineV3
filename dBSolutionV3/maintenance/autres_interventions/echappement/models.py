from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal, ROUND_HALF_UP
from utilisateurs.models import Utilisateur
from societe.models import Societe




class Echappement(models.Model):
    id = models.AutoField(primary_key=True)

    societe = models.ForeignKey(
        Societe,
        on_delete=models.CASCADE,
        related_name="echappement",
        verbose_name=_("Societe"),
        null=True,
        blank=True,
    )

    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="echappement",
        verbose_name=_("Utilisateur"),
        null=True,
        blank=True,
    )


    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="echappement",
        verbose_name=_("Véhicule")
    )


    immatriculation = models.CharField(
        max_length=20,
        verbose_name=_("Immatriculation"),
        blank=True,
    )


    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    kilometrage_echappement = models.IntegerField(
        _("Kilométrage échappement"),
        null=True,
        blank=True
    )


    date = models.DateField(default=timezone.now, verbose_name=_("Date du plein"))


    remarques = models.TextField(null=True, blank=True, verbose_name=_("Remarques"))


    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)


    class Meta:
        verbose_name = _("Echappement")
        verbose_name_plural = _("Échappements")
        ordering = ['-date']

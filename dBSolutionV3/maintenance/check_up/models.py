from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.models import Maintenance


class Location(models.TextChoices):
    AV = "AV", _("Avant")
    AR = "AR", _("Arrière")
    AVG = "AVG", _("Avant gauche")
    AVD = "AVD", _("Avant droit")
    ARG = "ARG", _("Arrière gauche")
    ARD = "ARD", _("Arrière droit")
    SUP = "SUP", _("Supérieur")
    INF = "INF", _("Inférieur")


class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")


class BatterieEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")


class ControleGeneral(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_general",
        verbose_name=_("Maintenance")
    )

    location = models.CharField(
        max_length=10,
        choices=Location.choices,
        verbose_name=_("Emplacement / partie du véhicule"),
        null=True,
        blank=True
    )

    # Essuie-glace
    essuie_glace_av = models.BooleanField(default=True, verbose_name=_("Essuie-glace AV fonctionnel"))
    essuie_glace_ar = models.BooleanField(default=True, verbose_name=_("Essuie-glace AR fonctionnel"))
    pare_brise = models.BooleanField(default=True, verbose_name=_("Pare_Brise sans coups"))

    # Moteur
    moteur_fuite = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Fuite moteur")
    )

    # Boîte de vitesse
    boite_fuite = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Fuite boîte de vitesse")
    )

    # Liquide de frein
    liquide_frein_etat = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("État liquide de frein")
    )
    remplacement_liquide_frein = models.BooleanField(default=False, verbose_name=_("Remplacement liquide de frein"))
    specif_liquide_frein = models.CharField(max_length=100, blank=True, verbose_name=_("Spécification liquide de frein"))
    quantite_liquide_frein = models.FloatField(default=0.0, verbose_name=_("Quantité liquide de frein (L)"))

    # Direction assistée / crémaillère
    direction_fuite = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Fuite direction assistée / crémaillère")
    )
    niveau_direction = models.FloatField(default=0.0, verbose_name=_("Niveau liquide direction"))

    bruit_roulement = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("État roulement de roue")
    )

    # Batterie
    batterie_etat = models.CharField(
        max_length=25,
        choices=BatterieEtat.choices,
        default=BatterieEtat.OK,
        verbose_name=_("État batterie")
    )

    # Réglage phares
    reglage_phares = models.BooleanField(default=True, verbose_name=_("Phares réglés correctement"))

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Contrôle général")
        verbose_name_plural = _("Contrôles généraux")

    def __str__(self):
        return _("Contrôle général – Maintenance %(id)s") % {"id": self.maintenance.id}


class AmortisseurControle(models.Model):
    controle_general = models.ForeignKey(
        "ControleGeneral",
        on_delete=models.CASCADE,
        related_name="amortisseurs",
        verbose_name=_("Contrôle général")
    )
    emplacement = models.CharField(
        max_length=25,
        choices=Location.choices,
        verbose_name=_("Emplacement")
    )
    fuite = models.BooleanField(default=False, verbose_name=_("Fuite"))

    class Meta:
        verbose_name = _("Amortisseur")
        verbose_name_plural = _("Amortisseurs")

    def __str__(self):
        return f"{self.get_emplacement_display()} – {'Fuite' if self.fuite else 'OK'}"


class RessortControle(models.Model):
    controle_general = models.ForeignKey(
        "ControleGeneral",
        on_delete=models.CASCADE,
        related_name="ressorts",
        verbose_name=_("Contrôle général")
    )
    emplacement = models.CharField(
        max_length=25,
        choices=Location.choices,
        verbose_name=_("Emplacement")
    )
    etat = models.CharField(
        max_length=25,
        choices=[("OK", _("OK")), ("CASSE", _("Cassé"))],
        default="OK",
        verbose_name=_("État")
    )

    class Meta:
        verbose_name = _("Ressort")
        verbose_name_plural = _("Ressorts")

    def __str__(self):
        return f"{self.get_emplacement_display()} – {self.etat}"

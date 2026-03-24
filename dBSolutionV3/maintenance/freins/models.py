from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece

class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("Non")
    NOT_OK = "NOT_OK", _("Oui")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class ControleFreins(models.Model):
    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="controle_freins",
        verbose_name=_("Maintenance")
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="controle_freins_checkup_exemplaire_km",
        verbose_name="Kilomètres_freins",
        null=True, blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    kilometrage_controle = models.PositiveIntegerField(
        _("Kilométrage au moment du controle des freins"),
        null=True,
        blank=True
    )


    # --- Freins ---

    freins_usure_plaquettes_av = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes avants (%)"))
    freins_plaquettes_remplacer_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK,verbose_name=_("Plaquettes avant à remplacer"))
    freins_epaisseur_disques_av = models.FloatField(default=0.0, verbose_name=_("Épaisseur des disques avants (mm)"))
    freins_fentes_disques_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fentes sur les disques avants"))
    freins_disques_remplacer_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Disques avants à remplacer"))

    freins_usure_plaquettes_ar = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes arrières (%)"))
    freins_plaquettes_remplacer_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK,verbose_name=_("Plaquettes arrière à remplacer"))
    freins_epaisseur_disques_ar = models.FloatField(default=0, verbose_name=_("Épaisseur des disques arrières (mm)"))
    freins_fentes_disques_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fentes sur les disques arrières"))
    freins_disques_remplacer_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Disques arrières à remplacer"))

    freins_fuites = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fuite"))

    # --- Liquide ---
    frein_liquide_frein_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État liquide de frein"))
    freins_remplacement_liquide_frein = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK,verbose_name=_("Remplacement liquide de frein"))
    freins_specif_liquide_frein = models.CharField(max_length=100, blank=True,verbose_name=_("Spécification liquide de frein"))
    freins_quantite_liquide_frein = models.FloatField(default=0, null=True, blank=True,verbose_name=_("Quantité liquide de frein (L)"))

    frein_machoire_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État de la machoire avant gauche"))
    frein_machoire_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État de la machoire avant droite"))
    frein_machoire_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État de la machoire arrière gauche"))
    frein_machoire_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État de la machoire arrière droite"))



    remarques = models.TextField(
        verbose_name=_("Remarques"), blank=True, null=True)

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]

    tag_freins = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="JAUNE",
        verbose_name=_("État visuel / Tag"),
    )

    # Champ pour l’utilisateur affecté (utilisateur courant)
    utilisateurs = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Utilisateur"),
        related_name="controle_freins"
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="controle_frein"
    )

    tech_nom_technicien = models.CharField(
        _("Nom du technicien"),
        max_length=255,
        blank=True
    )

    tech_role_technicien = models.CharField(
        _("Rôle du technicien"),
        max_length=255,
        blank=True
    )

    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="controle_tech_societe_freins"
    )



    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return _(
            "Contrôle freins – %(partie)s (%(date)s)"
        ) % {
            "partie": self.get_partie_display(),
            "date": self.date.strftime("%Y-%m-%d %H:%M")
        }

    def plaque_critique(self, seuil_usure=30):
        """Retourne True si les plaquettes sont trop usées (critique)."""
        return self.usure_plaquettes >= seuil_usure

    def disque_critique(self, epaisseur_min=20):
        """Retourne True si les disques sont trop fins ou fendus."""
        return self.epaisseur_disques <= epaisseur_min or self.fentes_disques

    def fuite_critique(self):
        """Retourne True si une fuite est détectée."""
        return self.fuites

    def is_critique(self):
        """Retourne True si l'une des conditions critiques est remplie."""
        return self.plaque_critique() or self.disque_critique() or self.fuite_critique()




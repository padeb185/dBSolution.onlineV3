from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin


class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("Non")
    NOT_OK = "NOT_OK", _("Oui")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class ControleFreins(TechnicienMixin, models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_freins",
        verbose_name=_("Maintenance"),
        null=True,  # autorisé vide à la création
        blank=True
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

    kilometrage_controle_brake = models.PositiveIntegerField(
        _("Kilométrage du controle des freins"),
        null=True,
        blank=True
    )


    # --- Freins ---

    avant_freins_pl_usure_plaquettes = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes avant (%)"))
    avant_freins_pl_plaquettes_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK,verbose_name=_("Plaquettes avant à remplacer"))

    avant_freins_d_epaisseur_disques = models.FloatField(default=0.0, verbose_name=_("Épaisseur des disques avant (mm)"))
    avant_freins_d_fentes_disques = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fentes sur les disques avant"))
    avant_freins_d_disques_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Disques avant à remplacer"))

    arriere_freins_pl_usure_plaquettes = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes arrière (%)"))
    arriere_freins_pl_plaquettes_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK,verbose_name=_("Plaquettes arrière à remplacer"))

    arriere_freins_d_epaisseur_disques = models.FloatField(default=0, verbose_name=_("Épaisseur des disques arrière (mm)"))
    arriere_freins_d_fentes_disques = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fentes sur les disques arrière"))
    arriere_freins_d_disques_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Disques arrière à remplacer"))

    fuites_freins_fuites = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fuite"))
    fuites_freins_machoire = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fuite machoire"))
    fuites_freins_flexibles = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fuite flexibles"))
    fuites_freins_tuyaux = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fuite tuyaux rigides"))

    # --- Liquide ---
    liquide_frein_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État liquide de frein"))
    liquide_remplacement_liquide_frein = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK,verbose_name=_("Remplacement liquide de frein"))
    liquide_specif_liquide_frein = models.CharField(max_length=100, blank=True,verbose_name=_("Spécification liquide de frein"))
    liquide_quantite_liquide_frein = models.FloatField(default=0, null=True, blank=True,verbose_name=_("Quantité liquide de frein (L)"))

    machoire_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État de la machoire avant gauche"))
    machoire_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État de la machoire avant droite"))
    machoire_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État de la machoire arrière gauche"))
    machoire_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État de la machoire arrière droite"))



    remarques = models.TextField(
        verbose_name=_("Remarques"), blank=True, null=True)

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]

    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="JAUNE",
        verbose_name=_("État visuel / Tag"),
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

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Contrôle freins")
        verbose_name_plural = _("Contrôles freins")

    def __str__(self):
        return _("Contrôle freins – Maintenance %(id)s") % {"id": self.maintenance.id}

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_controle_brake is not None:
            if self.kilometrage_controle_brake < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_checkup': _(
                        f"Le kilométrage du check-up ({self.kilometrage_controle_brake}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_controle_brake:
            if self.kilometrage_controle_brake > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_controle_brake
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        super().save(*args, **kwargs)
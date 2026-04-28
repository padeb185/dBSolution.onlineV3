from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.models import Maintenance
from utilisateurs.models import Utilisateur
from django.conf import settings
from utils.mixin import TechnicienMixin


# ---------------------------
# TextChoices
# ---------------------------

class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("Non")
    NOT_OK = "NOT_OK", _("Oui")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")

class PneuEtat(models.TextChoices):
    OK = "OK", _("OK")
    NON = "NON", _("Non")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")

# ---------------------------
# Modèle fusionné
# ---------------------------
class ControlePneus(TechnicienMixin, models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_pneus",
        verbose_name=_("Maintenance"),
        null=True,  # autorisé vide à la création
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="controle_pneus",
        verbose_name="Kilomètres_checkup",
        null=True, blank=True
    )

    voiture_pneus = models.ForeignKey(
        "voiture_pneus.VoiturePneus",
        on_delete=models.CASCADE,
        related_name="controle_Pneus",
        verbose_name="Pneus",
        null=True, blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )



    kilometrage_pneus = models.PositiveIntegerField(
        _("Kilométrage au moment du contrôle des pneus"),
        null=True,
        blank=True
    )


    # --- Pneus et Pression
    pneu_bande_avd = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("Bande de roulement du pneu avant droit"))
    pneu_bande_avg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("Bande de roulement du pneu avant gauche"))
    pneu_bande_ard = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("Bande de roulement du pneu arrière droit"))
    pneu_bande_arg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("Bande de roulement du pneu arrière gauche"))

    pneu_epaisseur_avd = models.FloatField(default=0.0, verbose_name=_("Épaisseur du pneu avant droit (mm)"))
    pneu_epaisseur_avg = models.FloatField(default=0.0, verbose_name=_("Épaisseur du pneu avant gauche (mm)"))
    pneu_epaisseur_ard = models.FloatField(default=0.0, verbose_name=_("Épaisseur du pneu arrière droit (mm)"))
    pneu_epaisseur_arg = models.FloatField(default=0.0, verbose_name=_("Épaisseur du pneu arrière gauche (mm)"))

    pneu_sidewall_avd = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("flancs du pneu avant droit"))
    pneu_sidewall_avg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("flancs du pneu avant gauche"))
    pneu_sidewall_ard = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("flancs du pneu arrière droit"))
    pneu_sidewall_arg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("flancs du pneu arrière gauche"))

    pneu_pression_bar_avd = models.FloatField(default=2.4, verbose_name=_("Pression du pneu avant droit en bar"))
    pneu_pression_bar_avg = models.FloatField(default=2.4, verbose_name=_("Pression du pneu avant gauche en bar"))
    pneu_pression_bar_ard = models.FloatField(default=2.4, verbose_name=_("Pression du pneu arrière droit en bar"))
    pneu_pression_bar_arg = models.FloatField(default=2.4, verbose_name=_("Pression du pneu arrière gauche en bar"))



    pneu_train_av =  models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.NON, verbose_name=_("Train avant à remplacer"))
    pneu_train_av_nombre = models.PositiveIntegerField(default=1, null=True, blank=True, verbose_name=_("Nombre de trains avant montés"))
    pneu_train_ar =  models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.NON, verbose_name=_("Train arrière à remplacer"))
    pneu_train_ar_nombre = models.PositiveIntegerField(default=1, null=True, blank=True, verbose_name=_("Nombre de trains arrières montés"))


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

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pneus",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="controle_pneus_techs"
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
        related_name="controle_pneus_societe"
    )

    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    class Meta:
        verbose_name = _("Contrôle pneus")
        verbose_name_plural = _("Contrôles pneus")

    def __str__(self):
        return _("Contrôle pneus – Maintenance %(id)s") % {"id": self.maintenance.id}

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_pneus is not None:
            if self.kilometrage_pneus < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_pneus': _(
                        f"Le kilométrage du controle des pneus ({self.kilometrage_pneus}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_pneus:
            if self.kilometrage_pneus > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_pneus
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        super().save(*args, **kwargs)

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")


# ---------------------------
# Modèle fusionné
# ---------------------------
class Admission(TechnicienMixin, models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="admission",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="admission",
        verbose_name="Kilomètres_checkup",
        null=True, blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    kilometrage_admission = models.PositiveIntegerField(
        _("Kilométrage au moment du controle"),
        null=True,
        blank=True
    )

    # -------------------------
    # FILTRATION
    filtre_air_pc = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                  verbose_name=_("Filtre à air"))
    filtre_air_pc_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix"))
    filtre_air_pc_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    boitier_filtre_air = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                          verbose_name=_("Boîtier filtre à air"))
    boitier_filtre_air_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    boitier_filtre_air_quantite = models.IntegerField(default=0)

    # -------------------------
    # MESURE AIR
    debitmetre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                  verbose_name=_("Débitmètre d'air"))
    debitmetre_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    debitmetre_quantite = models.IntegerField(default=0)

    capteur_map = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                   verbose_name=_("Capteur MAP"))
    capteur_map_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    capteur_map_quantite = models.IntegerField(default=0)

    capteur_temperature_air = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                               verbose_name=_("Capteur température air"))
    capteur_temperature_air_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    capteur_temperature_air_quantite = models.IntegerField(default=0)

    # -------------------------
    # ADMISSION PRINCIPALE
    corps_papillon = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                      verbose_name=_("Corps de papillon"))
    corps_papillon_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    corps_papillon_quantite = models.IntegerField(default=0)

    collecteur_admission = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                            verbose_name=_("Collecteur d'admission"))
    collecteur_admission_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    collecteur_admission_quantite = models.IntegerField(default=0)

    # -------------------------
    # SURALIMENTATION
    turbo = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                             verbose_name=_("Turbo"))
    turbo_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    turbo_quantite = models.IntegerField(default=0)

    intercooler = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                   verbose_name=_("Intercooler"))
    intercooler_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    intercooler_quantite = models.IntegerField(default=0)

    # -------------------------
    # EGR
    vanne_egr = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                 verbose_name=_("Vanne EGR"))
    vanne_egr_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vanne_egr_quantite = models.IntegerField(default=0)

    # -------------------------
    # DIVERS
    durites_admission = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                         verbose_name=_("Durites d'admission"))
    durites_admission_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    durites_admission_quantite = models.IntegerField(default=0)

    joints_admission = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                        verbose_name=_("Joints admission"))
    joints_admission_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    joints_admission_quantite = models.IntegerField(default=0)



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
        related_name="admission"
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
        related_name="admission"
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
        verbose_name = _("Admission")
        verbose_name_plural = _("Admissions")

    def __str__(self):
        return f"Admission moteur - {self.voiture_exemplaire}"


    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_admission is not None:
            if self.kilometrage_admission < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_admission': _(
                        f"Le kilométrage du check-up ({self.kilometrage_conytrole_boite}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_admission:
            if self.kilometrage_admission > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_admission
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        super().save(*args, **kwargs)







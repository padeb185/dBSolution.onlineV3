from decimal import Decimal

from django.core.validators import StepValueValidator

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class HuileBoiteAutoEtat(models.TextChoices):
    ATF3 = "ATF_III", _("ATF III")
    ATF_DSG = "ATF_DSG", _("ATF DSG")
    ATF_DCT = "ATF_DCT", _("ATF DCT")
    ATF_CVT = "ATF_CVT", _("ATF CVT")
    ATF_DEXRON_II = "ATF_DEXRON_II", _("ATF Dexron II")
    ATF_DEXRON_III = "ATF_DEXRON_III", _("ATF Dexron III")
    ATF_DEXRON_VI = "ATF_DEXRON_VI", _("ATF Dexron VI")
    ATF_MERCON = "ATF_MERCON", _("ATF Mercon")
    ATF_MERCON_V = "ATF_MERCON_V", _("ATF Mercon V")
    ATF_MERCON_LV = "ATF_MERCON_LV", _("ATF Mercon LV")
    ATF_MULTI = "ATF_MULTI", _("ATF Multi Vehicle")
    ATF_WS = "ATF_WS", _("ATF Toyota WS")
    ATF_ZF_LIFEGUARD = "ATF_ZF_LIFEGUARD", _("ZF Lifeguard")
    ATF_MOPAR = "ATF_MOPAR", _("Mopar ATF+4")
    ATF_AISIN = "ATF_AISIN", _("Aisin ATF")
    ATF_MBV236 = "ATF_MBV236", _("Mercedes MB 236.x")
    ATF_VOLVO = "ATF_VOLVO", _("Volvo ATF")
    ATF_HONDA = "ATF_HONDA", _("Honda ATF DW-1")
    ATF_NISSAN = "ATF_NISSAN", _("Nissan Matic")


class BoiteVitesseEtat(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class ControleBteVitesseAuto(TechnicienMixin, models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_bte_vitesse_auto",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="controle_bte_vitesse_auto",
        verbose_name=_("Kilomètres checkup"),
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_controle_boite_auto = models.PositiveIntegerField(
        _("Kilométrage au moment du contrôle"),
        null=True,
        blank=True
    )

    # --- Boîte automatique ---
    auto_emb_convertisseur_couple = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Convertisseur de couple")
    )
    auto_emb_embrayages_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Embrayages automatiques")
    )

    pompes_huile = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Pompes à huile")
    )
    pompes_valves = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Valves de contrôle")
    )

    arbre_bte_torque = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Arbre de couple")
    )
    arbre_bte_secondaire_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Arbre secondaire")
    )

    roulement_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Roulements internes")
    )

    huile_auto_niveau_quantite = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=Decimal("0.0"),
        verbose_name=_("Quantité d'huile ajoutée en litres"),
        validators=[StepValueValidator(0.1)]
    )

    huile_auto_niveau_qualite = models.CharField(
        max_length=25,
        choices=HuileBoiteAutoEtat.choices,
        default=HuileBoiteAutoEtat.ATF3,
        verbose_name=_("Qualité de l'huile")
    )

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]
    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="WHITE",
        verbose_name=_("État visuel / Tag"),
    )

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="controle_bte_vitesse_auto",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="controle_bte_auto"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="controle_bte_auto"
    )

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)


    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_controle_boite_auto is not None:
            if self.kilometrage_controle_boite_auto < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_controle_boite_auto': _(
                        f"Le kilométrage du contrôle ({self.kilometrage_controle_boite_auto}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })



    def save(self, *args, **kwargs):
        # Mise à jour du kilométrage de la voiture si nécessaire
        if self.voiture_exemplaire and self.kilometrage_controle_boite_auto:
            if self.kilometrage_controle_boite_auto > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_controle_boite_auto
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

            # ----------------------------
            # MAIN D'OEUVRE AUTO DESCRIPTIF
            # ----------------------------
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Controle boite auto") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        super().save(*args, **kwargs)

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle boîte automatique - {self.voiture_exemplaire.id}"
        return "Contrôle boîte automatique - non défini"

    class Meta:
        verbose_name = _("Contrôle boîte automatique")
        verbose_name_plural = _("Contrôles boîtes automatiques")

    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"
        return self.main_oeuvre.temps_display

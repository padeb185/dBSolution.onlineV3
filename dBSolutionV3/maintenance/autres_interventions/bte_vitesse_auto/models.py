from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class HuileBoiteEtat(models.TextChoices):
    ATF3 = "ATF_III", _("ATF III")
    ATF_DSG = "ATF DSG", _("ATF DSG")


class BoiteVitesseEtat(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À vérifier / remplacer")


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

    kilometres_chassis = models.PositiveIntegerField(default=0)

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

    huile_auto_quantite = models.FloatField(
        default=0,
        verbose_name=_("Quantité d'huile ajoutée en litres")
    )
    huile_auto_qualite = models.CharField(
        max_length=25,
        choices=HuileBoiteEtat.choices,
        default=HuileBoiteEtat.ATF3,
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
        default="JAUNE",
        verbose_name=_("État visuel / Tag"),
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

        super().save(*args, **kwargs)

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle boîte automatique - {self.voiture_exemplaire.id}"
        return "Contrôle boîte automatique - non défini"

    class Meta:
        verbose_name = _("Contrôle boîte automatique")
        verbose_name_plural = _("Contrôles boîtes automatiques")
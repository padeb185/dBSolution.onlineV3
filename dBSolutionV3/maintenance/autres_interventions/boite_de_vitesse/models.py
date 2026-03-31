from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance



class HuileBoiteEtat(models.TextChoices):
    SEPTANTE_CINQ = "75W", _("75W")
    SEPTANTE_5_80 = "75W80", _("75W80")
    SEPTANTE_CINQ90  = "75W90", _("75W90")
    QUATRE_20 = "80W", "80W"
    QUATRE_20_90 = "80W90", _("80W90")
    QUATRE_25_90 = "85W90", _("85W90")
    ATF3 = "ATF_III", _("ATF III")
    ATF_DSG = "ATF DSG", _("ATF DSG")




class BoiteVitesseEtat(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À vérifier / remplacer")

# ---------------------------
# Modèle fusionné
# ---------------------------
class ControleBoite(TechnicienMixin, models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_boite",
        verbose_name=_("Maintenance"),
        null=True,  # autorisé vide à la création
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="controle_boite",
        verbose_name="Kilomètres_checkup",
        null=True, blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    kilometrage_controle_boite = models.PositiveIntegerField(
        _("Kilométrage au moment du controle"),
        null=True,
        blank=True
    )


    # --- Boîte Manuelle ---
    # Embrayage
    bte_embrayage_disque = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Disque d'embrayage"))
    bte_embrayage_plateau = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Plateau d'embrayage"))

    # Arbres
    bte_a_primaire = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Arbre primaire"))
    bte_a_secondaire = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Arbre secondaire"))

    # Roulements
    roulement_bte_primaire = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Roulement arbre primaire"))
    roulement_bte_secondaire = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Roulement arbre secondaire"))
    roulement_bte_differentiel = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Roulement différentiel"))

    # Vitesses / pignons
    vitesse_1 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Pignon 1ère vitesse"))
    vitesse_2 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Pignon 2ème vitesse"))
    vitesse_3 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Pignon 3ème vitesse"))
    vitesse_4 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Pignon 4ème vitesse"))
    vitesse_5 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Pignon 5ème vitesse"))
    vitesse_6 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Pignon 6ème vitesse (si existante)"))
    vitesse_7 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices, default=BoiteVitesseEtat.OK,verbose_name=_("Pignon 7ème vitesse (si existante)"))
    vitesse_8 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices, default=BoiteVitesseEtat.OK,verbose_name=_("Pignon 8ème vitesse (si existante)"))

    # Synchros / fourchettes
    synchros = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Synchros"))
    fourchettes = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Fourchettes"))

    # Huile
    man_huile_manuelle_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"))
    man_huile_manuelle_qualite = models.CharField(max_length=25, choices=HuileBoiteEtat.choices,default=HuileBoiteEtat.SEPTANTE_CINQ, verbose_name=_("Qualité de l'huile"))

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
        related_name="controle_boite"
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
        related_name="controle_boite"
    )

    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    class Meta:
        verbose_name = _("Contrôle boite")
        verbose_name_plural = _("Contrôles boites")


    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle Boîte - {self.voiture_exemplaire.id}"
        return "Contrôle Boîte - non défini"


    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_controle_boite is not None:
            if self.kilometrage_controle_boite < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_controle_boite': _(
                        f"Le kilométrage du check-up ({self.kilometrage_conytrole_boite}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_controle_boite:
            if self.kilometrage_controle_boite > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_controle_boite
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        super().save(*args, **kwargs)







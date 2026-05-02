import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from client_particulier.models import ClientParticulier
from django.conf import settings
from societe.models import Societe
from voiture.voiture_exemplaire.utils_vin import get_vin_year
from voiture.voiture_exemplaire.models import VoitureExemplaire
from maintenance.niveaux.models import Niveau, NiveauxEtat, validate_step_0_1, HuileEtat, RefroidissementQualiteEtat
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin


class TypeUtilisation(models.TextChoices):
    SOCIETE = "societe", _("Société")
    CLIENT = "client", _("Client")
    PRIVE = "prive", _("Privé")
    LOCATION = "location", _("Location")
    INTERNE = "interne", _("Interne")

class NomPays(models.TextChoices):
    BE = "Belgique", _("Belgique")
    LU = "Luxembourg", _("Luxembourg")
    DE = "Allemagne", _("Allemagne")



class RemplacementMoteur(TechnicienMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)



    # -------------------------
    # CONFIG TVA
    # -------------------------
    PAYS_CHOICES = [
        ('BE', _("Belgique")),
        ('LU', _("Luxembourg")),
        ('DE', _("Allemagne")),
    ]

    TVA_PIECES = {
        'BE': 21,
        'LU': 16,
        'DE': 19,
    }

    # -------------------------
    # RELATIONS
    # -------------------------
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="remplacement_moteur",
        null=True,
        blank=True
    )



    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="remplacement_moteur",
        null=True,
        blank=True
    )

    proprietaire = models.ForeignKey(
        "proprietaire.ProprietaireVoiture",
        on_delete=models.PROTECT,
        related_name="remplacement_moteur",
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometres_moteur = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilometres du moteur à remplacer")
    )



    type_utilisation = models.CharField(
        max_length=10,
        choices=TypeUtilisation.choices,
        default=TypeUtilisation.CLIENT
    )

    kilometres_remplacement_moteur = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres au remplacement moteur")
    )

    variation_kilometres = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation de kilomètres depuis le dernier entretien"),
        help_text=_("Calculé automatiquement : total - dernièr entretien")
    )


    remplacement_numero_moteur = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Numéro de série du moteur")
    )

    remplacement_nombre_moteur = models.PositiveIntegerField(
        default=1,
        null=True,
        blank=True,
        verbose_name=_("Nombre de moteur")
    )


    prix_moteur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Prix moteur"),
    )


    client = models.ForeignKey(
        ClientParticulier,
        on_delete=models.CASCADE,
        related_name="remplacement_moteur",
        null=True,
        blank=True,
        verbose_name=_("Client"),
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


    moteur_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile"))
    moteur_niveau_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"),validators=[validate_step_0_1])
    moteur_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30,verbose_name=_("Qualité d'huile"))


    refroidissement_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de refroidissement"))
    refroidissement_quantite = models.FloatField(default=0, verbose_name=_("Quantité de liquide de refroidissement ajoutée en litres"), validators=[validate_step_0_1])
    refroidissement_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices,default=RefroidissementQualiteEtat.G13,verbose_name=_("Qualité de liquide de refroidissement"))


    nombre_remplacements = models.PositiveIntegerField(default=0, editable=False)

    remplacement_effectue = models.BooleanField(
        default=False,
        verbose_name=_("Remplacement effectué"),
    )

    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES
    )

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    tech_last_maintained_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="remplacement_moteur_maintained",
        verbose_name=_("Dernière maintenance effectuée par")
    )

    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="remplacement_moteur"
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
        related_name="remplacement_moteur"
    )

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="remplacement_moteur",
        verbose_name=_("Main d'oeuvre")
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




    def __str__(self):
        return f"{self.voiture_marque.nom_marque} {self.voiture_modele.nom_modele} {self.voiture_modele.nom_variante} - {self.immatriculation}"




    def clean(self):
        if self.voiture_exemplaire and self.voiture_exemplaire.kilometres_moteur is not None:
            if self.voiture_exemplaire.kilometres_moteur > self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometres_moteur": _(
                        "Le kilométrage du moteur ne peut pas être supérieur au kilométrage du véhicule."
                    )
                })



    def save(self, *args, **kwargs):
        km = self.kilometres_chassis or 0

        # -------------------------
        # REMISE À ZÉRO MOTEUR
        # -------------------------
        if self.remplacement_effectue:
            # on stocke le km de référence
            if not self.kilometres_remplacement_moteur:
                self.kilometres_remplacement_moteur = km

            # moteur remis à 0
            self.voiture_exemplaire.kilometres_moteur = km - (self.kilometres_remplacement_moteur or km)

            # sécurité
            if self.voiture_exemplaire.kilometres_moteur < 0:
                self.voiture_exemplaire.kilometres_moteur = 0

        # -------------------------
        # CAS NORMAL (pas de remplacement)
        # -------------------------
        else:
            self.voiture_exemplaire.kilometres_moteur = km

        super().save(*args, **kwargs)


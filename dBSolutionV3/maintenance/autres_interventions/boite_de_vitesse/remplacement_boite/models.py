import uuid
from decimal import Decimal

from django.core.validators import StepValueValidator

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from client_particulier.models import ClientParticulier
from django.conf import settings
from maintenance.autres_interventions.boite_de_vitesse.models import HuileBoiteEtat
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



class RemplacementBoite(TechnicienMixin, models.Model):
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
        related_name="remplacement_boite",
        null=True,
        blank=True
    )



    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="remplacement_boite",
        null=True,
        blank=True
    )

    proprietaires = models.ManyToManyField(
        "proprietaire.ProprietaireVoiture",
        related_name="remplacements_boite",
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometres_boite = models.PositiveIntegerField(
        verbose_name=_("Kilometres de la boite à remplacer")
    )


    kilometres_remplacement_boite = models.PositiveIntegerField(
        verbose_name=_("Kilomètres au remplacement de la boite")
    )

    variation_kilometres = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation de kilomètres depuis le dernier entretien"),
        help_text=_("Calculé automatiquement : total - dernièr entretien")
    )


    remplacement_boite_serie = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Numéro de série de la boite")
    )

    remplacement_boite_nombre = models.PositiveIntegerField(
        default=1,
        null=True,
        blank=True,
        verbose_name=_("Nombre de boite")
    )


    remplacement_boite_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Prix de la boite"),
    )


    client = models.ForeignKey(
        ClientParticulier,
        on_delete=models.CASCADE,
        related_name="remplacement_boite",
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


    boite_niveau_huile_etat =  models.CharField(max_length=25, choices=HuileBoiteEtat.choices,default=HuileBoiteEtat.SEPTANTE_CINQ, verbose_name=_("Qualité de l'huile"))
    boite_niveau_huile_quantite = (models.DecimalField(
                                   max_digits=4,
                                   decimal_places=1,
                                   default=Decimal("0.0"),
                                   verbose_name = _("Quantité d'huile ajoutée en litres"),
                                   validators=[StepValueValidator(0.1)]))



    nombre_remplacements = models.PositiveIntegerField(default=1, editable=False)

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
        related_name="remplacement_boite_maintained",
        verbose_name=_("Dernière maintenance effectuée par")
    )

    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="remplacement_boite"
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
        related_name="remplacement_boite"
    )

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="remplacement_boite",
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
        if self.voiture_exemplaire and self.voiture_exemplaire.kilometres_boite is not None:
            if self.voiture_exemplaire.kilometres_boite > self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometres_boite": _(
                        "Le kilométrage de la boite ne peut pas être supérieur au kilométrage du véhicule."
                    )
                })



    def save(self, *args, **kwargs):

        is_new = not RemplacementBoite.objects.filter(pk=self.pk).exists()

        if is_new and self.voiture_exemplaire_id:
            self.nombre_remplacements = (
                    RemplacementBoite.objects.filter(
                        voiture_exemplaire_id=self.voiture_exemplaire_id,
                        remplacement_effectue=True
                    ).count() + 1
            )

        km = self.kilometres_chassis or 0

        # -------------------------
        # REMISE À ZÉRO MOTEUR
        # -------------------------
        if self.remplacement_effectue:
            # on stocke le km de référence
            if not self.kilometres_remplacement_boite:
                self.kilometres_remplacement_boite = km

            # moteur remis à 0
            self.voiture_exemplaire.kilometres_boite = km - (self.kilometres_remplacement_boite or km)

            # sécurité
            if self.voiture_exemplaire.kilometres_boite < 0:
                self.voiture_exemplaire.kilometres_boite = 0

        # -------------------------
        # CAS NORMAL (pas de remplacement)
        # -------------------------
        else:
            self.voiture_exemplaire.kilometres_boite = km


        super().save(*args, **kwargs)

        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = f"{_('Remplacement boite')} {self.voiture_exemplaire} "

            if self.main_oeuvre.descriptif != task_name:
                self.main_oeuvre.descriptif = task_name
                self.main_oeuvre.save(update_fields=["descriptif"])


@property
def temps_main_oeuvre_display(self):
    if not self.main_oeuvre:
        return "0h00"
    return self.main_oeuvre.temps_display
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import RouesSerrageEtat, FabricantPiece, FabricantLubrifiant
from utils.mixin import TechnicienMixin
from maintenance.services import sync_maintenance
from maintenance.models import Maintenance





class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class Essuyage(TechnicienMixin, models.Model):
    # -------------------------
    # CONFIG TVA
    # -------------------------
    PAYS_CHOICES = [
        ('AT', _("Autriche")),
        ('BE', _("Belgique")),
        ('BG', _("Bulgarie")),
        ('CY', _("Chypre")),
        ('CZ', _("Tchéquie")),
        ('DE', _("Allemagne")),
        ('DK', _("Danemark")),
        ('EE', _("Estonie")),
        ('ES', _("Espagne")),
        ('FI', _("Finlande")),
        ('FR', _("France")),
        ('GR', _("Grèce")),
        ('HR', _("Croatie")),
        ('HU', _("Hongrie")),
        ('IE', _("Irlande")),
        ('IT', _("Italie")),
        ('LT', _("Lituanie")),
        ('LU', _("Luxembourg")),
        ('LV', _("Lettonie")),
        ('MT', _("Malte")),
        ('NL', _("Pays-Bas")),
        ('PL', _("Pologne")),
        ('PT', _("Portugal")),
        ('RO', _("Roumanie")),
        ('SE', _("Suède")),
        ('SI', _("Slovénie")),
        ('SK', _("Slovaquie")),
    ]

    TVA_PIECES = {
        'AT': 20,
        'BE': 21,
        'BG': 20,
        'CY': 19,
        'CZ': 21,
        'DE': 19,
        'DK': 25,
        'EE': 24,
        'ES': 21,
        'FI': 25.5,
        'FR': 20,
        'GR': 24,
        'HR': 25,
        'HU': 27,
        'IE': 23,
        'IT': 22,
        'LT': 21,
        'LU': 17,
        'LV': 21,
        'MT': 18,
        'NL': 21,
        'PL': 23,
        'PT': 23,
        'RO': 21,
        'SE': 25,
        'SI': 22,
        'SK': 23,
    }

    # -------------------------
    # RELATIONS
    # -------------------------
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="essuyage",
        null=True,
        blank=True
    )


    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="essuyage",
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name= _("Kilomètres chassis")
    )

    # -------------------------
    # INFOS
    # -------------------------
    kilometrage_essuyage = models.PositiveIntegerField(
        verbose_name= _("Kilométrage au moment du controle ABS ")
    )

    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES,
        default="BE",
        verbose_name=_("Pays"),
    )

    # -------------------------
    # PIECES
    # -------------------------
    def piece_fields(prefix):
        return {
            f"{prefix}": models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK),
            f"{prefix}_prix": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_quantite": models.IntegerField(default=0),
        }

    # =========================================================
    # BALAIS D'ESSUIE-GLACE
    # =========================================================

    balai_av_gauche = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Balai d'essuie-glace avant gauche"),
    )

    balai_av_gauche_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    balai_av_gauche_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    balai_av_gauche_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    balai_av_droit = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Balai d'essuie-glace avant droit"),
    )

    balai_av_droit_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    balai_av_droit_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    balai_av_droit_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    balai_arriere = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Balai d'essuie-glace arrière"),
    )

    balai_arriere_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    balai_arriere_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    balai_arriere_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # =========================================================
    # BRAS D'ESSUIE-GLACE
    # =========================================================

    bras_av_gauche = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Bras d'essuie-glace avant gauche"),
    )

    bras_av_gauche_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    bras_av_gauche_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    bras_av_gauche_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    bras_av_droit = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Bras d'essuie-glace avant droit"),
    )

    bras_av_droit_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    bras_av_droit_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    bras_av_droit_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    bras_arriere = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Bras d'essuie-glace arrière"),
    )

    bras_arriere_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    bras_arriere_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    bras_arriere_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # =========================================================
    # MOTEURS D'ESSUIE-GLACE
    # =========================================================

    moteur_essuie_glace_av = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Moteur d'essuie-glace avant"),
    )

    moteur_essuie_glace_av_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    moteur_essuie_glace_av_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    moteur_essuie_glace_av_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    moteur_essuie_glace_ar = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Moteur d'essuie-glace arrière"),
    )

    moteur_essuie_glace_ar_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    moteur_essuie_glace_ar_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    moteur_essuie_glace_ar_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # =========================================================
    # MÉCANISME / TRINGLERIE
    # =========================================================

    tringlerie_essuie_glace = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Tringlerie d'essuie-glace"),
    )

    tringlerie_essuie_glace_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    tringlerie_essuie_glace_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    tringlerie_essuie_glace_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # =========================================================
    # POMPES LAVE-GLACE
    # =========================================================

    pompe_lave_glace_av = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Pompe de lave-glace avant"),
    )

    pompe_lave_glace_av_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    pompe_lave_glace_av_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    pompe_lave_glace_av_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    pompe_lave_glace_ar = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Pompe de lave-glace arrière"),
    )

    pompe_lave_glace_ar_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    pompe_lave_glace_ar_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    pompe_lave_glace_ar_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # =========================================================
    # RÉSERVOIR LAVE-GLACE
    # =========================================================

    reservoir_lave_glace = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Réservoir de liquide lave-glace"),
    )

    reservoir_lave_glace_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    reservoir_lave_glace_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    reservoir_lave_glace_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # =========================================================
    # GICLEURS
    # =========================================================

    gicleur_av_gauche = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Gicleur de lave-glace avant gauche"),
    )

    gicleur_av_gauche_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    gicleur_av_gauche_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    gicleur_av_gauche_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    gicleur_av_droit = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Gicleur de lave-glace avant droit"),
    )

    gicleur_av_droit_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    gicleur_av_droit_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    gicleur_av_droit_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    gicleur_arriere = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Gicleur de lave-glace arrière"),
    )

    gicleur_arriere_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    gicleur_arriere_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    gicleur_arriere_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # =========================================================
    # TUYAUX / FLEXIBLES
    # =========================================================

    tuyau_lave_glace_av = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Tuyau flexible de lave-glace avant"),
    )

    tuyau_lave_glace_av_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    tuyau_lave_glace_av_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    tuyau_lave_glace_av_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    tuyau_lave_glace_ar = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Tuyau flexible de lave-glace arrière"),
    )

    tuyau_lave_glace_ar_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    tuyau_lave_glace_ar_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    tuyau_lave_glace_ar_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # =========================================================
    # RACCORDS
    # =========================================================

    raccord_simple = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Raccord simple de lave-glace"),
    )

    raccord_simple_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    raccord_simple_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    raccord_simple_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    raccord_t = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Raccord en T de lave-glace"),
    )

    raccord_t_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    raccord_t_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    raccord_t_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # =========================================================
    # JOINTS
    # =========================================================

    joints_lave_glace = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Joints du circuit de lave-glace"),
    )

    joints_lave_glace_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    joints_lave_glace_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    joints_lave_glace_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # =========================================================
    # LIQUIDE LAVE-GLACE
    # =========================================================

    liquide_lave_glace = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Liquide lave-glace"),
    )

    liquide_lave_glace_fabricant = models.CharField(
        max_length=50,
        choices=FabricantLubrifiant.choices,
        default=FabricantLubrifiant.CHOISIR,
        verbose_name=_("Fabricant"),
        blank=True,
    )

    liquide_lave_glace_quantite = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.0,
        verbose_name=_("Quantité"),
        help_text=_("Quantité ajoutée en litres"),
    )

    liquide_lave_glace_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
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

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="essuyage",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="essuyage"
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
        related_name="essuyage"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
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
        verbose_name = _("Système d'essuyage")
        verbose_name_plural = _("Systèmes d'essuyages")

        # =========================================================
        # STRING
        # =========================================================

    def __str__(self):
        if self.voiture_exemplaire:
            return _(
                "Contrôle essuyage - %(vehicule)s"
            ) % {
                "vehicule": self.voiture_exemplaire
            }

        return _("Contrôle essuyage")

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_essuyage is not None:
            if self.kilometrage_essuyage < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_système_abs': _(
                        f"Le kilométrage du système d'essuyage ({self.kilometrage_essuyage}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    # -------------------------
    # CALCUL GENERIQUE
    # -------------------------
    def calcul_piece(self, prefix):

        prix = getattr(self, f"{prefix}_prix", Decimal("0"))
        quantite = getattr(self, f"{prefix}_quantite", 0)

        total = prix * quantite

        return {
            "prix": prix,
            "quantite": quantite,
            "total": total,
        }

    # -------------------------
    # SAVE
    # -------------------------
    def save(self, *args, **kwargs):

        # ----------------------------
        # CALCUL DES PIÈCES
        # ----------------------------
        self.calcul_piece("balai_av_gauche")
        self.calcul_piece("balai_av_droit")
        self.calcul_piece("balai_arriere")

        self.calcul_piece("bras_av_gauche")
        self.calcul_piece("bras_av_droit")
        self.calcul_piece("bras_arriere")

        self.calcul_piece("moteur_essuie_glace_av")
        self.calcul_piece("moteur_essuie_glace_ar")

        self.calcul_piece("tringlerie_essuie_glace")

        self.calcul_piece("pompe_lave_glace_av")
        self.calcul_piece("pompe_lave_glace_ar")

        self.calcul_piece("reservoir_lave_glace")

        self.calcul_piece("gicleur_av_gauche")
        self.calcul_piece("gicleur_av_droit")
        self.calcul_piece("gicleur_arriere")

        self.calcul_piece("tuyau_lave_glace_av")
        self.calcul_piece("tuyau_lave_glace_ar")

        self.calcul_piece("raccord_simple")
        self.calcul_piece("raccord_t")

        self.calcul_piece("joints_lave_glace")

        self.calcul_piece("liquide_lave_glace")
        # ----------------------------
        # TECHNICIEN AUTO
        # ----------------------------
        if not self.tech_technicien and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # ----------------------------
        # MAIN D'OEUVRE AUTO DESCRIPTIF
        # ----------------------------

        # ----------------------------
        # MAJ KILOMÉTRAGE
        # ----------------------------
        if self.voiture_exemplaire and self.kilometrage_essuyage:
            if self.kilometrage_essuyage > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_essuyage
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # copie locale
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        # ----------------------------
        # SAVE ESSUYAGE
        # ----------------------------
        super().save(*args, **kwargs)


        if self.main_oeuvre_id and self.voiture_exemplaire_id:

            task_name = f"{_('Essuyage')} {self.voiture_exemplaire} "

            if self.main_oeuvre.descriptif != task_name:
                self.main_oeuvre.descriptif = task_name
                self.main_oeuvre.save(update_fields=["descriptif"])

        # ----------------------------
        # SYNC MAINTENANCE
        # ----------------------------
        sync_maintenance(
            self,
            Maintenance.TypeMaintenance.ESSUYAGE
        )
    # -------------------------
    # RAPPORT
    # -------------------------
    # =========================================================
    # RAPPORT DES PIÈCES
    # =========================================================

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        pieces = [
            ("balai_av_gauche", _("Balai d'essuie-glace avant gauche")),
            ("balai_av_droit", _("Balai d'essuie-glace avant droit")),
            ("balai_arriere", _("Balai d'essuie-glace arrière")),

            ("bras_av_gauche", _("Bras d'essuie-glace avant gauche")),
            ("bras_av_droit", _("Bras d'essuie-glace avant droit")),
            ("bras_arriere", _("Bras d'essuie-glace arrière")),

            ("moteur_essuie_glace_av", _("Moteur d'essuie-glace avant")),
            ("moteur_essuie_glace_ar", _("Moteur d'essuie-glace arrière")),

            ("tringlerie_essuie_glace", _("Tringlerie d'essuie-glace")),

            ("pompe_lave_glace_av", _("Pompe de lave-glace avant")),
            ("pompe_lave_glace_ar", _("Pompe de lave-glace arrière")),

            ("reservoir_lave_glace", _("Réservoir de liquide lave-glace")),

            ("gicleur_av_gauche", _("Gicleur de lave-glace avant gauche")),
            ("gicleur_av_droit", _("Gicleur de lave-glace avant droit")),
            ("gicleur_arriere", _("Gicleur de lave-glace arrière")),

            ("tuyau_lave_glace_av", _("Tuyau flexible de lave-glace avant")),
            ("tuyau_lave_glace_ar", _("Tuyau flexible de lave-glace arrière")),

            ("raccord_simple", _("Raccord simple de lave-glace")),
            ("raccord_t", _("Raccord en T de lave-glace")),

            ("joints_lave_glace", _("Joints du circuit de lave-glace")),

            ("liquide_lave_glace", _("Liquide lave-glace")),
        ]

        for prefix, libelle in pieces:
            # L'état est directement le champ de la pièce
            # ex. self.balai_av_gauche
            etat = getattr(self, prefix, None)

            if etat not in [
                EtatOKNotOK.NOT_OK,
                EtatOKNotOK.REMPLACE,
            ]:
                continue

            # -----------------------------
            # QUANTITÉ
            # -----------------------------
            quantite = getattr(
                self,
                f"{prefix}_quantite",
                0,
            )

            if quantite is None:
                quantite = 0

            quantite = Decimal(str(quantite))

            if quantite <= 0:
                continue

            # -----------------------------
            # PRIX
            # -----------------------------
            prix = getattr(
                self,
                f"{prefix}_prix",
                Decimal("0.00"),
            )

            if prix is None:
                prix = Decimal("0.00")

            prix = Decimal(str(prix))

            # -----------------------------
            # FABRICANT
            # -----------------------------
            fabricant = getattr(
                self,
                f"{prefix}_fabricant",
                "",
            )

            # Si c'est un champ choices, on récupère
            # le libellé affiché du fabricant
            try:
                fabricant_label = getattr(
                    self,
                    f"get_{prefix}_fabricant_display",
                )()
            except (AttributeError, TypeError):
                fabricant_label = fabricant

            # -----------------------------
            # LIBELLÉ DE L'ÉTAT
            # -----------------------------
            try:
                etat_label = getattr(
                    self,
                    f"get_{prefix}_display",
                )()
            except (AttributeError, TypeError):
                etat_label = etat

            # -----------------------------
            # TOTAL
            # -----------------------------
            total = prix * quantite
            total_general += total

            rapport.append({
                "champ": libelle,
                "code": prefix,
                "etat": etat,
                "etat_label": etat_label,
                "fabricant": fabricant_label,
                "quantite": quantite,
                "prix": prix,
                "total": total,
            })

        return {
            "lignes": rapport,
            "total_general": total_general,
        }

        # =========================================================
        # TVA
        # =========================================================

    @property
    def taux_tva_pieces(self):
        return Decimal(
            str(self.TVA_PIECES.get(self.pays, 0))
        )



    # ======================================================
        # MAIN-D'ŒUVRE
        # ======================================================

    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        heures, minutes = divmod(temps_minutes, 60)

        return f"{heures}h{minutes:02d}"

    @property
    def taux_horaire_main_oeuvre(self):
        if (
                self.main_oeuvre
                and self.main_oeuvre.taux_horaire is not None
        ):
            return self.main_oeuvre.taux_horaire

        return Decimal("0.00")

    @property
    def cout_main_oeuvre(self):
        if not self.main_oeuvre:
            return Decimal("0.00")

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        taux_horaire = (
                self.main_oeuvre.taux_horaire or Decimal("0.00")
        )

        cout = (
                Decimal(str(temps_minutes))
                / Decimal("60")
                * Decimal(str(taux_horaire))
        )

        return cout.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()

        return (
                rapport["total_general"]
                + self.cout_main_oeuvre
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import FabricantCardan, TVAConfig, RouesSerrageEtat
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class CardanEtat(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    REPARE = "REPARE", _("Réparé")
    NON_PRESENT = "NON_PRESENT", _("Non présent")


class CardanCote(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    AVG = "AVG", _("AVG")
    AVD = "AVD", _("AVD")
    ARG = "ARG", _("ARG")
    ARD = "ARD", _("ARD")


class Cardan(TechnicienMixin, models.Model):
    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="cardan",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="cardan",
        verbose_name=_("Véhicule"),
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_cardan = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du contrôle"),
    )

    kilometres_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Kilomètres rollback")
    )

    kilometres_boite = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_boite_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback boite")
    )

    kilometres_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_moteur_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback moteur")
    )

    kilometres_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_embrayage_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback embrayage")
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    # ======================================================
    # PIÈCES DU CARDAN
    # (chaque pièce : état / fabricant / côté / quantité / prix)
    # ======================================================

    # --- Cardan complet ---
    cardan_complet = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Cardan complet"),
    )
    cardan_complet_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    cardan_complet_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    cardan_complet_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    cardan_complet_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Arbre de transmission ---
    arbre_transmission = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Arbre de transmission"),
    )
    arbre_transmission_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    arbre_transmission_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    arbre_transmission_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    arbre_transmission_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Noix de cardan ---
    noix_cardan = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Noix de cardan"),
    )
    noix_cardan_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    noix_cardan_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    noix_cardan_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    noix_cardan_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Joint homocinétique côté roue ---
    joint_homocinetique_roue = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Joint homocinétique côté roue"),
    )
    joint_homocinetique_roue_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    joint_homocinetique_roue_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    joint_homocinetique_roue_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    joint_homocinetique_roue_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Joint homocinétique côté boîte ---
    joint_homocinetique_boite = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Joint homocinétique côté boîte"),
    )
    joint_homocinetique_boite_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    joint_homocinetique_boite_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    joint_homocinetique_boite_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    joint_homocinetique_boite_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Tripode ---
    tripode = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Tripode"),
    )
    tripode_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    tripode_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    tripode_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    tripode_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Tulipe / bol de transmission ---
    tulipe = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Tulipe / bol de transmission"),
    )
    tulipe_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    tulipe_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    tulipe_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    tulipe_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Soufflet côté roue ---
    soufflet_roue = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Soufflet côté roue"),
    )
    soufflet_roue_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    soufflet_roue_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    soufflet_roue_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    soufflet_roue_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Soufflet côté boîte ---
    soufflet_boite = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Soufflet côté boîte"),
    )
    soufflet_boite_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    soufflet_boite_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    soufflet_boite_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    soufflet_boite_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Colliers de soufflet ---
    colliers_soufflet = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Colliers de soufflet"),
    )
    colliers_soufflet_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    colliers_soufflet_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    colliers_soufflet_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    colliers_soufflet_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Graisse de cardan ---
    graisse_cardan = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Graisse de cardan"),
    )
    graisse_cardan_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    graisse_cardan_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    graisse_cardan_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    graisse_cardan_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Circlip / jonc d'arrêt ---
    circlip_cardan = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Circlip / jonc d'arrêt"),
    )
    circlip_cardan_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    circlip_cardan_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    circlip_cardan_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    circlip_cardan_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Bague cible ABS ---
    bague_abs = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Bague cible ABS"),
    )
    bague_abs_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    bague_abs_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    bague_abs_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    bague_abs_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Palier intermédiaire ---
    palier_intermediaire = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Palier intermédiaire"),
    )
    palier_intermediaire_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    palier_intermediaire_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    palier_intermediaire_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    palier_intermediaire_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Roulement de palier intermédiaire ---
    roulement_palier = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Roulement de palier intermédiaire"),
    )
    roulement_palier_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    roulement_palier_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    roulement_palier_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    roulement_palier_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Croisillon ---
    croisillon = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Croisillon"),
    )
    croisillon_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    croisillon_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    croisillon_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    croisillon_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Flector / disque flexible ---
    flector = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Flector / disque flexible"),
    )
    flector_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    flector_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    flector_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    flector_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Joint spi de sortie de boîte ---
    joint_spi_sortie_boite = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Joint spi de sortie de boîte"),
    )
    joint_spi_sortie_boite_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    joint_spi_sortie_boite_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    joint_spi_sortie_boite_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    joint_spi_sortie_boite_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Écrou de transmission ---
    ecrou_transmission = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Écrou de transmission"),
    )
    ecrou_transmission_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    ecrou_transmission_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    ecrou_transmission_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    ecrou_transmission_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Vis de fixation de cardan ---
    vis_fixation_cardan = models.CharField(
        max_length=25,
        choices=CardanEtat.choices,
        default=CardanEtat.OK,
        verbose_name=_("Vis de fixation de cardan"),
    )
    vis_fixation_cardan_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    vis_fixation_cardan_cote = models.CharField(
        max_length=25,
        choices=CardanCote.choices,
        default=CardanCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    vis_fixation_cardan_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    vis_fixation_cardan_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]
    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="VERT",
        verbose_name=_("État visuel / Tag"),
    )

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cardan",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="cardan"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="cardan"
    )
    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    # ======================================================
    # LISTE DES PIÈCES (source unique pour le rapport)
    # ======================================================
    PIECES_DEF = [
            (_("Cardan complet"), "cardan_complet"),
            (_("Arbre de transmission"), "arbre_transmission"),
            (_("Noix de cardan"), "noix_cardan"),
            (_("Joint homocinétique côté roue"), "joint_homocinetique_roue"),
            (_("Joint homocinétique côté boîte"), "joint_homocinetique_boite"),
            (_("Tripode"), "tripode"),
            (_("Tulipe / bol de transmission"), "tulipe"),
            (_("Soufflet côté roue"), "soufflet_roue"),
            (_("Soufflet côté boîte"), "soufflet_boite"),
            (_("Colliers de soufflet"), "colliers_soufflet"),
            (_("Graisse de cardan"), "graisse_cardan"),
            (_("Circlip / jonc d'arrêt"), "circlip_cardan"),
            (_("Bague cible ABS"), "bague_abs"),
            (_("Palier intermédiaire"), "palier_intermediaire"),
            (_("Roulement de palier intermédiaire"), "roulement_palier"),
            (_("Croisillon"), "croisillon"),
            (_("Flector / disque flexible"), "flector"),
            (_("Joint spi de sortie de boîte"), "joint_spi_sortie_boite"),
            (_("Écrou de transmission"), "ecrou_transmission"),
            (_("Vis de fixation de cardan"), "vis_fixation_cardan"),
    ]

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire_id and self.kilometrage_cardan is not None:
            # Création : on compare au véhicule.
            # Modification : au kilométrage figé avant ce contrôle.
            if self.pk:
                minimum = self.kilometres_chassis or 0
            else:
                minimum = self.voiture_exemplaire.kilometres_chassis or 0

            if self.kilometrage_cardan < minimum:
                raise ValidationError({
                    "kilometrage_cardan": _(
                        "Le kilométrage du contrôle (%(km_controle)s) ne peut pas "
                        "être inférieur au kilométrage avant intervention (%(km_voiture)s)."
                    ) % {
                        "km_controle": self.kilometrage_cardan,
                        "km_voiture": minimum,
                    }
                })

    def save(self, *args, **kwargs):

        # =========================
        # TECHNICIEN
        # =========================
        if not self.tech_technicien_id and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = f"{_('Contrôle cardan')} {self.voiture_exemplaire}"

            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.CARDAN
            self.maintenance.voiture_exemplaire = self.voiture_exemplaire
            self.maintenance.save(
                update_fields=["type_maintenance", "voiture_exemplaire"]
            )

        # =========================
        # KILOMÉTRAGE AVANT INTERVENTION
        # (figé uniquement à la création)
        # =========================
        if self.voiture_exemplaire_id and self._state.adding and not self.kilometres_chassis:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )
            self.kilometres_chassis = voiture.kilometres_chassis or 0

        # =========================
        # CALCUL VARIATION (jamais négative : champ PositiveInteger)
        # =========================
        if self.kilometrage_cardan is not None:
            self.kilometrage_variation = max(
                self.kilometrage_cardan - (self.kilometres_chassis or 0), 0
            )
        else:
            self.kilometrage_variation = 0

        # =========================
        # SAUVEGARDE CONTRÔLE CARDAN
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if self.voiture_exemplaire_id and self.kilometrage_cardan is not None:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )
            if self.kilometrage_cardan > (voiture.kilometres_chassis or 0):
                voiture.kilometres_chassis = self.kilometrage_cardan
                voiture.save(update_fields=["kilometres_chassis"])

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle cardan - {self.voiture_exemplaire.id}"
        return "Contrôle cardan - non défini"

    class Meta:
        verbose_name = _("Contrôle cardan")
        verbose_name_plural = _("Contrôles cardans")

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
        if self.main_oeuvre and self.main_oeuvre.taux_horaire is not None:
            return self.main_oeuvre.taux_horaire

        return Decimal("0.00")

    @property
    def cout_main_oeuvre(self):
        if not self.main_oeuvre:
            return Decimal("0.00")

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        taux_horaire = self.main_oeuvre.taux_horaire or Decimal("0.00")

        cout = (
                Decimal(str(temps_minutes))
                / Decimal("60")
                * Decimal(str(taux_horaire))
        )

        return cout.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # ======================================================
    # RAPPORT
    # ======================================================

    def _choice_display(self, base, suffixe):
        """Libellé d'un champ <base>_<suffixe>, ou '' s'il n'existe pas ou vaut sa valeur par défaut."""
        attr = f"{base}_{suffixe}"
        valeur = getattr(self, attr, None)
        if not valeur:
            return ""
        try:
            defaut = self._meta.get_field(attr).default
        except Exception:
            defaut = None
        if valeur == defaut:
            return ""
        return getattr(self, f"get_{attr}_display")()

    def _fabricant_display(self, base):
        return self._choice_display(base, "fabricant")

    def _cote_display(self, base):
        return self._choice_display(base, "cote")

    def pieces_controle(self):
        """Toutes les pièces contrôlées (hors 'Non présent'), pour le détail / PDF."""
        pieces = []
        for label, base in self.PIECES_DEF:
            etat = getattr(self, base, None)
            if not etat or etat == CardanEtat.NON_PRESENT:
                continue
            pieces.append({
                "base": base,
                "label": label,
                "etat": etat,
                "etat_label": getattr(self, f"get_{base}_display")(),
                "cote": self._cote_display(base),
                "fabricant": self._fabricant_display(base),
            })
        return pieces

    def generer_rapport_remplacement(self):
        lignes = []
        total_pieces = Decimal("0.00")

        etats_labels = {
            CardanEtat.NOT_OK: _("À remplacer"),
            CardanEtat.REMPLACE: _("Remplacé"),
        }

        for label, base in self.PIECES_DEF:
            etat = getattr(self, base, None)

            if etat not in etats_labels:
                continue

            prix = Decimal(str(getattr(self, f"{base}_prix", None) or "0.00"))
            quantite = Decimal(str(getattr(self, f"{base}_quantite", None) or "0"))

            if prix <= 0 or quantite <= 0:
                continue

            total_ligne = (prix * quantite).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            total_pieces += total_ligne

            lignes.append({
                "champ": label,
                "etat": etat,
                "etat_label": etats_labels[etat],
                "fabricant": self._fabricant_display(base),
                "cote": self._cote_display(base),
                "quantite": quantite,
                "prix": prix,
                "total": total_ligne,
            })

        total_pieces = total_pieces.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "lignes": lignes,
            "pieces": lignes,
            "total_pieces": total_pieces,
            "total_general": total_pieces,
        }

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()
        total_pieces = rapport.get("total_pieces", Decimal("0.00"))
        cout_main_oeuvre = self.cout_main_oeuvre or Decimal("0.00")

        return (total_pieces + cout_main_oeuvre).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

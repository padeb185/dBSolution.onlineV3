from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import FabricantCardan, TVAConfig, RouesSerrageEtat
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class ArbreEtat(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    REPARE = "REPARE", _("Réparé")
    NON_PRESENT = "NON_PRESENT", _("Non présent")


class ArbreCote(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    AVANT = "AVANT", _("Avant")
    CENTRAL = "CENTRAL", _("Central")
    ARRIERE = "ARRIERE", _("Arrière")
    ARBRE_AVANT = "ARBRE_AVANT", _("Arbre avant (4x4)")
    ARBRE_ARRIERE = "ARBRE_ARRIERE", _("Arbre arrière (4x4)")


class ArbreTransmission(TechnicienMixin, models.Model):
    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="arbre_transmission",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="arbre_transmission",
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

    kilometrage_arbre = models.PositiveIntegerField(
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
    # PIÈCES DE L'ARBRE DE TRANSMISSION
    # (chaque pièce : état / fabricant / position / quantité / prix)
    # ======================================================

    # --- Arbre de transmission (complet) ---
    arbre_transmission = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Arbre de transmission (complet)"),
    )
    arbre_transmission_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    arbre_transmission_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
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

    # --- Tube d'arbre (voilage / choc) ---
    tube_arbre = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Tube d'arbre (voilage / choc)"),
    )
    tube_arbre_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    tube_arbre_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    tube_arbre_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    tube_arbre_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Équilibrage de l'arbre ---
    equilibrage = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Équilibrage de l'arbre"),
    )
    equilibrage_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    equilibrage_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    equilibrage_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    equilibrage_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Flector avant (disque flexible) ---
    flector_avant = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Flector avant (disque flexible)"),
    )
    flector_avant_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    flector_avant_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    flector_avant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    flector_avant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Flector arrière (disque flexible) ---
    flector_arriere = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Flector arrière (disque flexible)"),
    )
    flector_arriere_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    flector_arriere_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    flector_arriere_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    flector_arriere_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Palier central (support) ---
    palier_central = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Palier central (support)"),
    )
    palier_central_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    palier_central_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    palier_central_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    palier_central_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Roulement de palier central ---
    roulement_palier = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Roulement de palier central"),
    )
    roulement_palier_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    roulement_palier_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
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

    # --- Croisillon avant ---
    croisillon_avant = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Croisillon avant"),
    )
    croisillon_avant_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    croisillon_avant_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    croisillon_avant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    croisillon_avant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Croisillon central ---
    croisillon_central = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Croisillon central"),
    )
    croisillon_central_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    croisillon_central_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    croisillon_central_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    croisillon_central_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Croisillon arrière ---
    croisillon_arriere = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Croisillon arrière"),
    )
    croisillon_arriere_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    croisillon_arriere_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    croisillon_arriere_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    croisillon_arriere_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Joint coulissant / cannelures ---
    joint_coulissant = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Joint coulissant / cannelures"),
    )
    joint_coulissant_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    joint_coulissant_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    joint_coulissant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    joint_coulissant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Soufflet de joint coulissant ---
    soufflet_coulissant = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Soufflet de joint coulissant"),
    )
    soufflet_coulissant_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    soufflet_coulissant_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    soufflet_coulissant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    soufflet_coulissant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Joint homocinétique d'arbre ---
    joint_homocinetique = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Joint homocinétique d'arbre"),
    )
    joint_homocinetique_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    joint_homocinetique_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    joint_homocinetique_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    joint_homocinetique_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Bague de centrage ---
    bague_centrage = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Bague de centrage"),
    )
    bague_centrage_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    bague_centrage_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    bague_centrage_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    bague_centrage_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Amortisseur de vibrations (damper) ---
    amortisseur_vibrations = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Amortisseur de vibrations (damper)"),
    )
    amortisseur_vibrations_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    amortisseur_vibrations_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    amortisseur_vibrations_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    amortisseur_vibrations_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Bride / flasque de sortie de boîte ---
    bride_sortie_boite = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Bride / flasque de sortie de boîte"),
    )
    bride_sortie_boite_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    bride_sortie_boite_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    bride_sortie_boite_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    bride_sortie_boite_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Bride / flasque de pont ---
    bride_pont = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Bride / flasque de pont"),
    )
    bride_pont_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    bride_pont_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    bride_pont_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    bride_pont_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Joint spi de sortie de boîte ---
    joint_spi_sortie_boite = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
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
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
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

    # --- Joint spi d'entrée de pont ---
    joint_spi_pont = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Joint spi d'entrée de pont"),
    )
    joint_spi_pont_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    joint_spi_pont_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    joint_spi_pont_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    joint_spi_pont_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Fixations (vis / écrous / rondelles) ---
    fixations = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Fixations (vis / écrous / rondelles)"),
    )
    fixations_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    fixations_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    fixations_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    fixations_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Graisse ---
    graisse = models.CharField(
        max_length=25,
        choices=ArbreEtat.choices,
        default=ArbreEtat.OK,
        verbose_name=_("Graisse"),
    )
    graisse_fabricant = models.CharField(
        max_length=25,
        choices=FabricantCardan.choices,
        default=FabricantCardan.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    graisse_cote = models.CharField(
        max_length=25,
        choices=ArbreCote.choices,
        default=ArbreCote.CHOISIR,
        verbose_name=_("Position"),
    )
    graisse_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    graisse_prix = models.DecimalField(
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
        related_name="arbre_transmission",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="arbre_transmission"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="arbre_transmission"
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
        (_("Arbre de transmission (complet)"), "arbre_transmission"),
        (_("Tube d'arbre (voilage / choc)"), "tube_arbre"),
        (_("Équilibrage de l'arbre"), "equilibrage"),
        (_("Flector avant (disque flexible)"), "flector_avant"),
        (_("Flector arrière (disque flexible)"), "flector_arriere"),
        (_("Palier central (support)"), "palier_central"),
        (_("Roulement de palier central"), "roulement_palier"),
        (_("Croisillon avant"), "croisillon_avant"),
        (_("Croisillon central"), "croisillon_central"),
        (_("Croisillon arrière"), "croisillon_arriere"),
        (_("Joint coulissant / cannelures"), "joint_coulissant"),
        (_("Soufflet de joint coulissant"), "soufflet_coulissant"),
        (_("Joint homocinétique d'arbre"), "joint_homocinetique"),
        (_("Bague de centrage"), "bague_centrage"),
        (_("Amortisseur de vibrations (damper)"), "amortisseur_vibrations"),
        (_("Bride / flasque de sortie de boîte"), "bride_sortie_boite"),
        (_("Bride / flasque de pont"), "bride_pont"),
        (_("Joint spi de sortie de boîte"), "joint_spi_sortie_boite"),
        (_("Joint spi d'entrée de pont"), "joint_spi_pont"),
        (_("Fixations (vis / écrous / rondelles)"), "fixations"),
        (_("Graisse"), "graisse"),
    ]

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire_id and self.kilometrage_arbre is not None:
            # Création : on compare au véhicule.
            # Modification : au kilométrage figé avant ce contrôle.
            if self.pk:
                minimum = self.kilometres_chassis or 0
            else:
                minimum = self.voiture_exemplaire.kilometres_chassis or 0

            if self.kilometrage_arbre < minimum:
                raise ValidationError({
                    "kilometrage_arbre": _(
                        "Le kilométrage du contrôle (%(km_controle)s) ne peut pas "
                        "être inférieur au kilométrage avant intervention (%(km_voiture)s)."
                    ) % {
                        "km_controle": self.kilometrage_arbre,
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
            task_name = f"{_('Contrôle arbre de transmission')} {self.voiture_exemplaire}"

            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.ARBRE_TRANSMISSION
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
        if self.kilometrage_arbre is not None:
            self.kilometrage_variation = max(
                self.kilometrage_arbre - (self.kilometres_chassis or 0), 0
            )
        else:
            self.kilometrage_variation = 0

        # =========================
        # SAUVEGARDE CONTRÔLE ARBRE DE TRANSMISSION
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if self.voiture_exemplaire_id and self.kilometrage_arbre is not None:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )
            if self.kilometrage_arbre > (voiture.kilometres_chassis or 0):
                voiture.kilometres_chassis = self.kilometrage_arbre
                voiture.save(update_fields=["kilometres_chassis"])

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle arbre de transmission - {self.voiture_exemplaire.id}"
        return "Contrôle arbre de transmission - non défini"

    class Meta:
        verbose_name = _("Contrôle arbre de transmission")
        verbose_name_plural = _("Contrôles arbres de transmission")

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
            if not etat or etat == ArbreEtat.NON_PRESENT:
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
            ArbreEtat.NOT_OK: _("À remplacer"),
            ArbreEtat.REMPLACE: _("Remplacé"),
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

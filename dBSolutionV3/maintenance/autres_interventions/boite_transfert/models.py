from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import (
    FabricantTransmissionIntegrale,
    RouesSerrageEtat,
    SystemeTransmissionIntegrale,
    TVAConfig,
    TypeTransmissionIntegrale,
)
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class TransfertEtat(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    REPARE = "REPARE", _("Réparé")
    NON_PRESENT = "NON_PRESENT", _("Non présent")


class TransfertPosition(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    AVANT = "AVANT", _("Avant")
    CENTRAL = "CENTRAL", _("Central")
    ARRIERE = "ARRIERE", _("Arrière")
    ENTREE = "ENTREE", _("Entrée (côté boîte de vitesses)")
    SORTIE_AVANT = "SORTIE_AVANT", _("Sortie avant")
    SORTIE_ARRIERE = "SORTIE_ARRIERE", _("Sortie arrière")
    GAUCHE = "GAUCHE", _("Gauche")
    DROITE = "DROITE", _("Droite")


class BoiteTransfert(TechnicienMixin, models.Model):
    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="boite_transfert",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="boite_transfert",
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

    kilometrage_transfert = models.PositiveIntegerField(
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
    # SYSTÈME DE TRANSMISSION INTÉGRALE
    # ======================================================
    systeme_transmission = models.CharField(
        max_length=30,
        choices=SystemeTransmissionIntegrale.choices,
        default=SystemeTransmissionIntegrale.CHOISIR,
        verbose_name=_("Système de transmission intégrale"),
    )
    type_transmission = models.CharField(
        max_length=20,
        choices=TypeTransmissionIntegrale.choices,
        default=TypeTransmissionIntegrale.CHOISIR,
        verbose_name=_("Type de transmission intégrale"),
    )
    reference_boite_transfert = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Référence / code de la boîte de transfert"),
    )

    # ======================================================
    # PIÈCES DE LA BOÎTE DE TRANSFERT / TRANSMISSION INTÉGRALE
    # (chaque pièce : état / fabricant / position / quantité / prix)
    # ======================================================

    # --- Boîte de transfert (complète) ---
    boite_transfert = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Boîte de transfert (complète)"),
    )
    boite_transfert_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    boite_transfert_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    boite_transfert_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    boite_transfert_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Huile de boîte de transfert ---
    huile_boite_transfert = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Huile de boîte de transfert"),
    )
    huile_boite_transfert_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    huile_boite_transfert_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    huile_boite_transfert_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    huile_boite_transfert_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Joint de carter de boîte de transfert ---
    joint_carter_transfert = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Joint de carter de boîte de transfert"),
    )
    joint_carter_transfert_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    joint_carter_transfert_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    joint_carter_transfert_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    joint_carter_transfert_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Différentiel central (Torsen / planétaire) ---
    differentiel_central = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Différentiel central (Torsen / planétaire)"),
    )
    differentiel_central_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    differentiel_central_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    differentiel_central_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    differentiel_central_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Viscocoupleur ---
    viscocoupleur = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Viscocoupleur"),
    )
    viscocoupleur_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    viscocoupleur_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    viscocoupleur_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    viscocoupleur_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Coupleur Haldex / embrayage multidisque ---
    coupleur_haldex = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Coupleur Haldex / embrayage multidisque"),
    )
    coupleur_haldex_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    coupleur_haldex_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    coupleur_haldex_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    coupleur_haldex_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Pompe du coupleur (Haldex) ---
    pompe_haldex = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Pompe du coupleur (Haldex)"),
    )
    pompe_haldex_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    pompe_haldex_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    pompe_haldex_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    pompe_haldex_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Filtre du coupleur (Haldex) ---
    filtre_haldex = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Filtre du coupleur (Haldex)"),
    )
    filtre_haldex_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    filtre_haldex_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    filtre_haldex_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    filtre_haldex_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Huile du coupleur (Haldex) ---
    huile_haldex = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Huile du coupleur (Haldex)"),
    )
    huile_haldex_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    huile_haldex_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    huile_haldex_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    huile_haldex_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Chaîne de transfert ---
    chaine_transfert = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Chaîne de transfert"),
    )
    chaine_transfert_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    chaine_transfert_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    chaine_transfert_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    chaine_transfert_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Pignons / engrenages de transfert ---
    pignons_transfert = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Pignons / engrenages de transfert"),
    )
    pignons_transfert_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    pignons_transfert_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    pignons_transfert_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    pignons_transfert_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Roulements de boîte de transfert ---
    roulements_transfert = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Roulements de boîte de transfert"),
    )
    roulements_transfert_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    roulements_transfert_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    roulements_transfert_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    roulements_transfert_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Joints spi (entrée / sorties) ---
    joints_spi_transfert = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Joints spi (entrée / sorties)"),
    )
    joints_spi_transfert_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    joints_spi_transfert_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    joints_spi_transfert_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    joints_spi_transfert_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Actionneur / moteur de crabotage ---
    actionneur_transfert = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Actionneur / moteur de crabotage"),
    )
    actionneur_transfert_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    actionneur_transfert_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    actionneur_transfert_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    actionneur_transfert_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Calculateur de transmission intégrale ---
    module_commande = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Calculateur de transmission intégrale"),
    )
    module_commande_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    module_commande_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    module_commande_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    module_commande_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Capteurs (vitesse / position / température) ---
    capteurs_transfert = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Capteurs (vitesse / position / température)"),
    )
    capteurs_transfert_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    capteurs_transfert_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    capteurs_transfert_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    capteurs_transfert_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Renvoi d'angle (PTU) ---
    ptu = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Renvoi d'angle (PTU)"),
    )
    ptu_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    ptu_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    ptu_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    ptu_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Huile du renvoi d'angle (PTU) ---
    huile_ptu = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Huile du renvoi d'angle (PTU)"),
    )
    huile_ptu_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    huile_ptu_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    huile_ptu_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    huile_ptu_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Différentiel avant ---
    differentiel_avant = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Différentiel avant"),
    )
    differentiel_avant_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    differentiel_avant_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    differentiel_avant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    differentiel_avant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Huile du différentiel avant ---
    huile_differentiel_avant = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Huile du différentiel avant"),
    )
    huile_differentiel_avant_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    huile_differentiel_avant_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    huile_differentiel_avant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    huile_differentiel_avant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Différentiel arrière ---
    differentiel_arriere = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Différentiel arrière"),
    )
    differentiel_arriere_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    differentiel_arriere_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    differentiel_arriere_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    differentiel_arriere_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Huile du différentiel arrière ---
    huile_differentiel_arriere = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Huile du différentiel arrière"),
    )
    huile_differentiel_arriere_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    huile_differentiel_arriere_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    huile_differentiel_arriere_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    huile_differentiel_arriere_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Supports / silent-blocs ---
    supports_transfert = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Supports / silent-blocs"),
    )
    supports_transfert_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    supports_transfert_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    supports_transfert_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    supports_transfert_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Reniflard / mise à l'air ---
    reniflard_transfert = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Reniflard / mise à l'air"),
    )
    reniflard_transfert_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    reniflard_transfert_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
        verbose_name=_("Position"),
    )
    reniflard_transfert_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    reniflard_transfert_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Fixations (vis / écrous / rondelles) ---
    fixations = models.CharField(
        max_length=25,
        choices=TransfertEtat.choices,
        default=TransfertEtat.OK,
        verbose_name=_("Fixations (vis / écrous / rondelles)"),
    )
    fixations_fabricant = models.CharField(
        max_length=30,
        choices=FabricantTransmissionIntegrale.choices,
        default=FabricantTransmissionIntegrale.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    fixations_cote = models.CharField(
        max_length=25,
        choices=TransfertPosition.choices,
        default=TransfertPosition.CHOISIR,
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
        related_name="boite_transfert",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="boite_transfert"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="boite_transfert"
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
        (_("Boîte de transfert (complète)"), "boite_transfert"),
        (_("Huile de boîte de transfert"), "huile_boite_transfert"),
        (_("Joint de carter de boîte de transfert"), "joint_carter_transfert"),
        (_("Différentiel central (Torsen / planétaire)"), "differentiel_central"),
        (_("Viscocoupleur"), "viscocoupleur"),
        (_("Coupleur Haldex / embrayage multidisque"), "coupleur_haldex"),
        (_("Pompe du coupleur (Haldex)"), "pompe_haldex"),
        (_("Filtre du coupleur (Haldex)"), "filtre_haldex"),
        (_("Huile du coupleur (Haldex)"), "huile_haldex"),
        (_("Chaîne de transfert"), "chaine_transfert"),
        (_("Pignons / engrenages de transfert"), "pignons_transfert"),
        (_("Roulements de boîte de transfert"), "roulements_transfert"),
        (_("Joints spi (entrée / sorties)"), "joints_spi_transfert"),
        (_("Actionneur / moteur de crabotage"), "actionneur_transfert"),
        (_("Calculateur de transmission intégrale"), "module_commande"),
        (_("Capteurs (vitesse / position / température)"), "capteurs_transfert"),
        (_("Renvoi d'angle (PTU)"), "ptu"),
        (_("Huile du renvoi d'angle (PTU)"), "huile_ptu"),
        (_("Différentiel avant"), "differentiel_avant"),
        (_("Huile du différentiel avant"), "huile_differentiel_avant"),
        (_("Différentiel arrière"), "differentiel_arriere"),
        (_("Huile du différentiel arrière"), "huile_differentiel_arriere"),
        (_("Supports / silent-blocs"), "supports_transfert"),
        (_("Reniflard / mise à l'air"), "reniflard_transfert"),
        (_("Fixations (vis / écrous / rondelles)"), "fixations"),
    ]

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire_id and self.kilometrage_transfert is not None:
            # Création : on compare au véhicule.
            # Modification : au kilométrage figé avant ce contrôle.
            if self.pk:
                minimum = self.kilometres_chassis or 0
            else:
                minimum = self.voiture_exemplaire.kilometres_chassis or 0

            if self.kilometrage_transfert < minimum:
                raise ValidationError({
                    "kilometrage_transfert": _(
                        "Le kilométrage du contrôle (%(km_controle)s) ne peut pas "
                        "être inférieur au kilométrage avant intervention (%(km_voiture)s)."
                    ) % {
                        "km_controle": self.kilometrage_transfert,
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
            task_name = f"{_('Contrôle boîte de transfert')} {self.voiture_exemplaire}"

            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.BOITE_TRANSFERT
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
        if self.kilometrage_transfert is not None:
            self.kilometrage_variation = max(
                self.kilometrage_transfert - (self.kilometres_chassis or 0), 0
            )
        else:
            self.kilometrage_variation = 0

        # =========================
        # SAUVEGARDE CONTRÔLE BOÎTE DE TRANSFERT
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if self.voiture_exemplaire_id and self.kilometrage_transfert is not None:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )
            if self.kilometrage_transfert > (voiture.kilometres_chassis or 0):
                voiture.kilometres_chassis = self.kilometrage_transfert
                voiture.save(update_fields=["kilometres_chassis"])

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle boîte de transfert - {self.voiture_exemplaire.id}"
        return "Contrôle boîte de transfert - non défini"

    class Meta:
        verbose_name = _("Contrôle boîte de transfert")
        verbose_name_plural = _("Contrôles boîtes de transfert")

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
            if not etat or etat == TransfertEtat.NON_PRESENT:
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
            TransfertEtat.NOT_OK: _("À remplacer"),
            TransfertEtat.REMPLACE: _("Remplacé"),
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

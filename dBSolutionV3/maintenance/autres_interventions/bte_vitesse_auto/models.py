from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import FabricantLubrifiant, FabricantEmbrayage, TVAConfig, HuileBoiteAutoEtat, RouesSerrageEtat
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance






class BoiteVitesseEtat(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    NON_PRESENT = "NON_PRESENT", _("Non présent")


class ControleBteVitesseAuto(TechnicienMixin, models.Model):


    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

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
        verbose_name=_("Kilométrage au moment du contrôle"),
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    # --- Boîte automatique ---
    auto_emb_convertisseur_couple = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Convertisseur de couple")
    )

    auto_emb_convertisseur_couple_fabricant = models.CharField(
        max_length=25,
        choices=FabricantEmbrayage.choices,
        default=FabricantEmbrayage.CHOISIR,
        verbose_name=_("Fabricant")
    )

    auto_emb_convertisseur_couple_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    auto_emb_convertisseur_couple_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )



    double_embrayage = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Double embrayage")
    )

    double_embrayage_fabricant = models.CharField(
        max_length=25,
        choices=FabricantEmbrayage.choices,
        default=FabricantEmbrayage.CHOISIR,
        verbose_name=_("Fabricant")
    )

    double_embrayage_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    double_embrayage_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    pompes_h = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Pompes à huile")
    )

    pompes_h_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    pompes_h_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    pompes_valves = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Valves de contrôle")
    )
    pompes_valves_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    pompes_valves_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    arbre_bte_torque = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Arbre de couple")
    )

    arbre_bte_torque_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    arbre_bte_torque_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )



    arbre_bte_secondaire_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Arbre secondaire")
    )

    arbre_bte_secondaire_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    arbre_bte_secondaire_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    roulement_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Roulements internes")
    )



    roulement_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    roulement_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # ============================================================
    # BOÎTE AUTOMATIQUE - PIÈCES COMPLÉMENTAIRES
    # ============================================================

    # -------------------------
    # Bloc hydraulique
    # -------------------------
    bloc_hydraulique = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Bloc hydraulique")
    )

    bloc_hydraulique_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    bloc_hydraulique_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Mécatronique
    # -------------------------
    mecatronique = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Unité mécatronique")
    )

    mecatronique_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    mecatronique_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Solénoïdes
    # -------------------------
    solenoides = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Solénoïdes")
    )

    solenoides_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    solenoides_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Électrovannes
    # -------------------------
    electrovannes = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Électrovannes")
    )

    electrovannes_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    electrovannes_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Filtre de boîte automatique
    # -------------------------
    filtre_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Filtre de boîte automatique")
    )

    filtre_boite_auto_fabricant = models.CharField(
        max_length=25,
        choices=FabricantEmbrayage.choices,
        default=FabricantEmbrayage.CHOISIR,
        verbose_name=_("Fabricant")
    )

    filtre_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    filtre_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Carter d'huile
    # -------------------------
    carter_huile_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Carter d'huile de boîte")
    )

    carter_huile_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    carter_huile_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Joint de carter
    # -------------------------
    joint_carter_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Joint de carter de boîte")
    )

    joint_carter_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    joint_carter_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Crépine
    # -------------------------
    crepine_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Crépine de boîte automatique")
    )

    crepine_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    crepine_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Pompe hydraulique
    # -------------------------
    pompe_hydraulique_boite = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Pompe hydraulique")
    )

    pompe_hydraulique_boite_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    pompe_hydraulique_boite_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Embrayages internes
    # -------------------------
    embrayages_internes_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Embrayages internes")
    )

    embrayages_internes_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    embrayages_internes_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Disques d'embrayage internes
    # -------------------------
    disques_embrayage_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Disques d'embrayage internes")
    )

    disques_embrayage_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    disques_embrayage_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Disques acier
    # -------------------------
    disques_acier_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Disques acier d'embrayage")
    )

    disques_acier_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    disques_acier_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Tambours d'embrayage
    # -------------------------
    tambours_embrayage_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Tambours d'embrayage")
    )

    tambours_embrayage_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    tambours_embrayage_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Pistons d'embrayage
    # -------------------------
    pistons_embrayage_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Pistons d'embrayage")
    )

    pistons_embrayage_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    pistons_embrayage_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Joints de pistons
    # -------------------------
    joints_pistons_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Joints de pistons")
    )

    joints_pistons_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    joints_pistons_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Train épicycloïdal
    # -------------------------
    train_epicycloidal = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Train épicycloïdal")
    )

    train_epicycloidal_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    train_epicycloidal_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Planétaire
    # -------------------------
    pignon_planetaire = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Pignon planétaire")
    )

    pignon_planetaire_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    pignon_planetaire_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Satellites
    # -------------------------
    pignons_satellites = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Pignons satellites")
    )

    pignons_satellites_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    pignons_satellites_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Couronne
    # -------------------------
    couronne_epicycloidale = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Couronne du train épicycloïdal")
    )

    couronne_epicycloidale_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    couronne_epicycloidale_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Porte-satellites
    # -------------------------
    porte_satellites = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Porte-satellites")
    )

    porte_satellites_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    porte_satellites_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Arbre d'entrée
    # -------------------------
    arbre_entree_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Arbre d'entrée")
    )

    arbre_entree_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    arbre_entree_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Arbre de sortie
    # -------------------------
    arbre_sortie_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Arbre de sortie")
    )

    arbre_sortie_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    arbre_sortie_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Pignons internes
    # -------------------------
    pignons_internes_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Pignons internes")
    )

    pignons_internes_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    pignons_internes_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Roue libre
    # -------------------------
    roue_libre_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Roue libre")
    )

    roue_libre_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    roue_libre_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Freins internes
    # -------------------------
    freins_internes_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Freins internes")
    )

    freins_internes_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    freins_internes_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Bandes de frein
    # -------------------------
    bandes_frein_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Bandes de frein")
    )

    bandes_frein_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    bandes_frein_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Capteur vitesse entrée
    # -------------------------
    capteur_vitesse_entree_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Capteur de vitesse d'entrée")
    )

    capteur_vitesse_entree_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    capteur_vitesse_entree_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Capteur vitesse sortie
    # -------------------------
    capteur_vitesse_sortie_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Capteur de vitesse de sortie")
    )

    capteur_vitesse_sortie_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    capteur_vitesse_sortie_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Capteur température huile
    # -------------------------
    capteur_temperature_huile_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Capteur de température d'huile")
    )

    capteur_temperature_huile_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    capteur_temperature_huile_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Capteur pression huile
    # -------------------------
    capteur_pression_huile_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Capteur de pression d'huile")
    )

    capteur_pression_huile_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    capteur_pression_huile_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Calculateur de boîte
    # -------------------------
    calculateur_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Calculateur de boîte automatique")
    )

    calculateur_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    calculateur_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Faisceau électrique
    # -------------------------
    faisceau_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Faisceau électrique de boîte")
    )

    faisceau_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    faisceau_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Connecteur de boîte
    # -------------------------
    connecteur_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Connecteur électrique de boîte")
    )

    connecteur_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    connecteur_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Sélecteur
    # -------------------------
    selecteur_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Sélecteur de boîte")
    )

    selecteur_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    selecteur_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Capteur de position
    # -------------------------
    capteur_position_selecteur_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Capteur de position du sélecteur")
    )

    capteur_position_selecteur_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    capteur_position_selecteur_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Différentiel
    # -------------------------
    differentiel_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Différentiel")
    )

    differentiel_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    differentiel_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Pignons de différentiel
    # -------------------------
    pignons_differentiel_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Pignons de différentiel")
    )

    pignons_differentiel_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    pignons_differentiel_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Joints spi
    # -------------------------
    joints_spi_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Joints spi de boîte")
    )

    joints_spi_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    joints_spi_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Joints toriques
    # -------------------------
    joints_toriques_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Joints toriques de boîte")
    )

    joints_toriques_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    joints_toriques_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Bagues
    # -------------------------
    bagues_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Bagues de boîte automatique")
    )

    bagues_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    bagues_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Radiateur / échangeur huile
    # -------------------------
    echangeur_huile_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Échangeur d'huile de boîte")
    )

    echangeur_huile_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    echangeur_huile_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Durites d'huile
    # -------------------------
    durites_huile_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Durites d'huile de boîte")
    )

    durites_huile_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    durites_huile_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    # -------------------------
    # Supports de boîte
    # -------------------------
    supports_boite_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Supports de boîte automatique")
    )

    supports_boite_auto_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    supports_boite_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    huile_bte_auto_vitesse = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices, default=BoiteVitesseEtat.OK,
                                          verbose_name=_("Huile de boite de vitesse"))

    huile_bte_auto_vitesse_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,
                                              default=FabricantLubrifiant.CASTROL,
                                              verbose_name=_("Fabricant"))

    huile_bte_auto_vitesse_qualite = models.CharField(max_length=25, choices=HuileBoiteAutoEtat.choices,
                                                      default=HuileBoiteAutoEtat.ATF3,
                                                      verbose_name=_("Qualité de l'huile"))

    huile_bte_auto_vitesse_quantite = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=Decimal("0.0"),
        verbose_name=_("Quantité d'huile ajoutée en litres"),
        validators=[StepValueValidator(0.1)],
    )
    huile_bte_auto_vitesse_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
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
        default="WHITE",
        verbose_name=_("État visuel / Tag"),
    )

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

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


        # =========================
        # TECHNICIEN
        # =========================
        if not self.tech_technicien_id and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = (
                    _("Checkup boite de vitesse automatique")
                    + " "
                    + str(self.voiture_exemplaire)
            )

            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(
                update_fields=["descriptif"]
            )

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = (
                Maintenance.TypeMaintenance.BOITE_AUTO
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                ]
            )

        # =========================
        # KILOMÉTRAGE AVANT INTERVENTION
        # =========================
        if self.voiture_exemplaire_id:

            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            ancien_kilometrage = (
                    voiture.kilometres_chassis or 0
            )

            # Snapshot du kilométrage avant intervention
            self.kilometres_chassis = ancien_kilometrage

            # =========================
            # CALCUL VARIATION
            # =========================
            if self.kilometrage_controle_boite_auto is not None:

                self.kilometrage_variation = (
                        self.kilometrage_controle_boite_auto
                        - ancien_kilometrage
                )

            else:
                self.kilometrage_variation = 0

        # =========================
        # SAUVEGARDE NETTOYAGE EXTÉRIEUR
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if (
                self.voiture_exemplaire_id
                and self.kilometrage_controle_boite_auto is not None
        ):

            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            if (
                    self.kilometrage_controle_boite_auto
                    > (voiture.kilometres_chassis or 0)
            ):
                voiture.kilometres_chassis = (
                    self.kilometrage_controle_boite_auto
                )

                voiture.save(
                    update_fields=["kilometres_chassis"]
                )





    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle boîte automatique - {self.voiture_exemplaire.id}"
        return "Contrôle boîte automatique - non défini"

    class Meta:
        verbose_name = _("Contrôle boîte automatique")
        verbose_name_plural = _("Contrôles boîtes automatiques")

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

    def generer_rapport_remplacement(self):
        lignes = []
        total_pieces = Decimal("0.00")

        pieces = [
            {
                "champ": _("Convertisseur de couple"),
                "etat": self.auto_emb_convertisseur_couple,
                "prix": self.auto_emb_convertisseur_couple_prix,
                "quantite": self.auto_emb_convertisseur_couple_quantite,
            },
            {
                "champ": _("Double embrayage"),
                "etat": self.double_embrayage,
                "prix": self.double_embrayage_prix,
                "quantite": self.double_embrayage_quantite,
            },
            {
                "champ": _("Pompe à huile"),
                "etat": self.pompes_h,
                "prix": self.pompes_h_prix,
                "quantite": self.pompes_h_quantite,
            },
            {
                "champ": _("Valves de contrôle"),
                "etat": self.pompes_valves,
                "prix": self.pompes_valves_prix,
                "quantite": self.pompes_valves_quantite,
            },
            {
                "champ": _("Arbre de couple"),
                "etat": self.arbre_bte_torque,
                "prix": self.arbre_bte_torque_prix,
                "quantite": self.arbre_bte_torque_quantite,
            },
            {
                "champ": _("Arbre secondaire"),
                "etat": self.arbre_bte_secondaire_auto,
                "prix": self.arbre_bte_secondaire_auto_prix,
                "quantite": self.arbre_bte_secondaire_auto_quantite,
            },
            {
                "champ": _("Roulements internes"),
                "etat": self.roulement_auto,
                "prix": self.roulement_auto_prix,
                "quantite": self.roulement_auto_quantite,
            },
            {
                "champ": _("Huile de boîte automatique"),
                "etat": self.huile_bte_auto_vitesse,
                "prix": self.huile_bte_auto_vitesse_prix,
                "quantite": self.huile_bte_auto_vitesse_quantite,
            },
        ]

        etats_labels = {
            "NOT_OK": _("À remplacer"),
            "REMPLACE": _("Remplacé"),
        }

        for piece in pieces:
            etat = piece["etat"]

            if etat not in ("NOT_OK", "REMPLACE"):
                continue

            prix = Decimal(str(piece["prix"] or "0.00"))
            quantite = Decimal(str(piece["quantite"] or "0.00"))

            if prix <= 0 or quantite <= 0:
                continue

            total_ligne = (
                    prix * quantite
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total_pieces += total_ligne

            lignes.append({
                "champ": piece["champ"],
                "etat": etat,
                "etat_label": etats_labels.get(etat, etat),
                "quantite": quantite,
                "prix": prix,
                "total": total_ligne,
            })

        total_pieces = total_pieces.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        return {
            "lignes": lignes,
            "pieces": lignes,
            "total_pieces": total_pieces,
            "total_general": total_pieces,
        }

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()

        total_pieces = rapport.get(
            "total_pieces",
            Decimal("0.00"),
        )

        cout_main_oeuvre = self.cout_main_oeuvre or Decimal("0.00")

        return total_pieces + cout_main_oeuvre

from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.models import Maintenance
from utilisateurs.models import Utilisateur
from voiture.voiture_exemplaire.models import VoitureExemplaire

# ---------------------------
# TextChoices
# ---------------------------
class Location(models.TextChoices):
    AV = "AV", _("Avant")
    AR = "AR", _("Arrière")
    AVG = "AVG", _("Avant gauche")
    AVD = "AVD", _("Avant droit")
    ARG = "ARG", _("Arrière gauche")
    ARD = "ARD", _("Arrière droit")
    SUP = "SUP", _("Supérieur")
    INF = "INF", _("Inférieur")


class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")


class BatterieEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")


class TypeBruit(models.TextChoices):
    ROULEMENT_ROUE = "ROULEMENT_ROUE", _("Roulement de roue")
    ROULEMENT_SUSPENSION = "ROULEMENT_SUSPENSION", _("Roulement de suspension")
    MOTEUR = "MOTEUR", _("Moteur")
    BOITE_VITESSE = "BOITE_VITESSE", _("Boîte de vitesse")
    PONT = "PONT", _("Pont")


class TypePieceControle(models.TextChoices):
    ROTULE_DIRECTION = "ROTULE_DIRECTION", _("Rotule de direction")
    ROTULE_SUSPENSION = "ROTULE_SUSPENSION", _("Rotule de suspension")
    BIELLETTE_BARRE_STAB = "BIELLETTE_BARRE_STAB", _("Biellette de barre stabilisatrice")
    BARRE_STABILISATRICE = "BARRE_STABILISATRICE", _("Barre stabilisatrice")
    AMORTISSEUR = "AMORTISSEUR", _("Amortisseur")
    ROULEMENT_ROUE = "ROULEMENT_ROUE", _("Roulement de roue")
    TRIANGLE = "TRIANGLE", _("Triangle")
    MULTI_BRAS = "MULTI_BRAS", _("Multi-bras")


class EtatPiece(models.TextChoices):
    BON = "BON", _("Bon")
    USE = "USE", _("Usé")
    HS = "HS", _("Hors service")


class PartieFrein(models.TextChoices):
    AVANT = "AVANT", _("Avant")
    ARRIERE = "ARRIERE", _("Arrière")
    AVANT_AR = "AV_AR", _("Avant et arrière")


# ---------------------------
# Modèle fusionné
# ---------------------------
class ControleGeneral(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_general_checkup",
        verbose_name=_("Maintenance")
    )

    # --- Essuie-glaces & Pare-brise ---
    essuie_glace_av = models.BooleanField(default=True, verbose_name=_("Essuie-glace AV fonctionnel"))
    essuie_glace_ar = models.BooleanField(default=True, verbose_name=_("Essuie-glace AR fonctionnel"))
    pare_brise = models.BooleanField(default=True, verbose_name=_("Pare-brise sans coups"))

    # --- Moteur & transmission ---
    moteur_fuite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite moteur"))
    boite_fuite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite boîte de vitesse"))

    # --- Freins ---

    freins_usure_plaquettes_av = models.FloatField(default=0.0, verbose_name=_("Usure des plaquettes avants (%)"))
    freins_plaquettes_remplacer_av = models.BooleanField(default=False, verbose_name=_("Plaquettes avant à remplacer"))
    freins_epaisseur_disques_av = models.FloatField(default=0.0, verbose_name=_("Épaisseur des disques avants (mm)"))
    freins_fentes_disques_av = models.BooleanField(default=False, verbose_name=_("Présence de fentes sur les disques avants"))
    freins_disques_remplacer_av = models.BooleanField(default=False, verbose_name=_("Disques avants à remplacer"))

    freins_usure_plaquettes_ar = models.FloatField(default=0.0, verbose_name=_("Usure des plaquettes arrières (%)"))
    freins_plaquettes_remplacer_ar = models.BooleanField(default=False, verbose_name=_("Plaquettes arrière à remplacer"))
    freins_epaisseur_disques_ar = models.FloatField(default=0.0, verbose_name=_("Épaisseur des disques arrières (mm)"))
    freins_fentes_disques_ar = models.BooleanField(default=False, verbose_name=_("Présence de fentes sur les disques arrières"))
    freins_disques_remplacer_ar = models.BooleanField(default=False, verbose_name=_("Disques arrières à remplacer"))

    freins_fuites = models.BooleanField(default=False, verbose_name=_("Présence de fuite"))





    # --- Liquide ---
    liquide_frein_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État liquide de frein"))
    remplacement_liquide_frein = models.BooleanField(default=False, verbose_name=_("Remplacement liquide de frein"))
    specif_liquide_frein = models.CharField(max_length=100, blank=True, verbose_name=_("Spécification liquide de frein"))
    quantite_liquide_frein = models.FloatField(default=0.0, verbose_name=_("Quantité liquide de frein (L)"))

    direction_fuite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite direction assistée / crémaillère"))
    niveau_direction = models.FloatField(default=0.0, verbose_name=_("Niveau liquide direction"))

    # --- Bruits ---
    bruit_roulement = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État roulement de roue"))
    location_roulement = models.CharField(max_length=10, choices=Location.choices, blank=True, null=True, verbose_name=_("Emplacement du roulement"))

    # --- Batterie ---
    batterie_etat =models.CharField(max_length=25, choices=BatterieEtat.choices, default=BatterieEtat.OK, verbose_name=_("État batterie"))

    # --- Jeux ---

    rotule_direction_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de direction avant droite"))
    rotule_direction_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de direction avant gauche"))
    rotule_direction_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de direction arrière droite"))
    rotule_direction_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de direction arrière gauche"))

    rotule_suspension_inferieure_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotule de suspension inférieure avant droite"))
    rotule_suspension_inferieure_avg= models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotule de suspension inférieure avant gauche"))
    rotule_suspension_inferieure_arD = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotule de suspension inférieure arrière droite"))
    rotule_suspension_inferieure_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotule de suspension inférieure arrière droite"))

    rotule_suspension_superieure_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure avant droite"))
    rotule_suspension_superieure_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure avant gauche"))
    rotule_suspension_superieure_arD = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure arrière droite"))
    rotule_suspension_superieure_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure arrière droite"))

    Biellette_barre_stabilisatrice_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux biellette de barre stabilisatrice avant droite"))
    Biellette_barre_stabilisatrice_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux biellette de barre stabilisatrice avant gauche"))
    Biellette_barre_stabilisatrice_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux biellette de barre stabilisatrice avant droite"))
    Biellette_barre_stabilisatrice_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux biellette de barre stabilisatrice avant gauche"))

    barre_stabilisatrice_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux barre stabilisatrice avant"))
    barre_stabilisatrice_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux barre stabilisatrice arrière"))

    amortisseur_avd =  models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux barre amortisseur avant droit"))
    amortisseur_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux barre amortisseur avant gauche"))
    amortisseur_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux barre amortisseur arrière droit"))
    amortisseur_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux barre amortisseur arrière gauche"))



    ROULEMENT_ROUE = "ROULEMENT_ROUE", _("Roulement de roue")
    TRIANGLE = "TRIANGLE", _("Triangle")
    MULTI_BRAS = "MULTI_BRAS", _("Multi-bras")






    # --- Réglage phares ---
    reglage_phares = models.BooleanField(default=True, verbose_name=_("Phares réglés correctement"))

    # --- Nettoyage extérieur ---
    nettoyage_exterieur_traces_gomme = models.BooleanField(default=False, verbose_name=_("Traces de gomme"))
    nettoyage_exterieur_carrosserie = models.BooleanField(default=False, verbose_name=_("Carrosserie"))
    nettoyage_exterieur_jantes = models.BooleanField(default=False, verbose_name=_("Jantes"))
    nettoyage_exterieur_validation = models.BooleanField(default=False, verbose_name=_("Validation finale"))

    # --- Nettoyage intérieur ---
    nettoyage_interieur_vitres = models.BooleanField(default=False, verbose_name=_("Vitres"))
    nettoyage_interieur_pare_brise = models.BooleanField(default=False, verbose_name=_("Pare-brise"))
    nettoyage_interieur_aspirateur = models.BooleanField(default=False, verbose_name=_("Aspirateur"))
    nettoyage_interieur_portes = models.BooleanField(default=False, verbose_name=_("Intérieurs de porte"))
    nettoyage_interieur_tableau_de_bord = models.BooleanField(default=False, verbose_name=_("Tableau de bord"))
    nettoyage_interieur_plastiques = models.BooleanField(default=False, verbose_name=_("Plastiques"))
    nettoyage_interieur_validation = models.BooleanField(default=False, verbose_name=_("Validation finale"))


    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Contrôle général")
        verbose_name_plural = _("Contrôles généraux")

    def __str__(self):
        return _("Contrôle général – Maintenance %(id)s") % {"id": self.maintenance.id}
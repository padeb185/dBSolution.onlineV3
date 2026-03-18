from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.models import Maintenance
from utilisateurs.models import Utilisateur


# ---------------------------
# TextChoices
# ---------------------------

class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("Non")
    NOT_OK = "NOT_OK", _("Oui")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class BatterieEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")

class PhareEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")

class NettoyageEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("A faire")
    FAIT = "FAIT", _("Fait")
    REPORTER = "REPORTER", _("Reporter")


class NiveauxEtat(models.TextChoices):
    BON = "BON", _("Bon")
    AJOUTER = "AJOUTER", _("Ajouter")


class HuileEtat(models.TextChoices):
    ZERO_16 = "0W16", _("0W16")
    ZERO_20 = "0W20", _("0W20")
    ZERO_30 = "0W30", _("0W30")
    ZERO_40 = "0W40", _("0W40")
    CINQ_20 = "5W20", _("5W20")
    CINQ_30 = "5W30", _("5W30")
    CINQ_40 = "5W40", _("5W40")
    DIX_40 = "10W40", _("10W40")
    DIX_50 = "10W50", _("10W50")
    DIX_60 = "10W60", _("10W60")
    QUINZE_40 = "15W40", _("15W40")
    QUINZE_50 = "15W50", _("15W50")
    VINGT_50 = "20W50", _("20W50")


class HuileBoiteEtat(models.TextChoices):
    SEPTANTE_CINQ = "75W", _("75W")
    SEPTANTE_5_80 = "75W80", _("75W80")
    SEPTANTE_CINQ90  = "75W90", _("75W90")
    QUATRE_20 = "80W", "80W"
    QUATRE_20_90 = "80W90", _("80W90")
    QUATRE_25_90 = "85W90", _("85W90")
    ATF3 = "ATF_III", _("ATF III")
    ATF_DSG = "ATF DSG", _("ATF DSG")


class HuilePontEtat(models.TextChoices):
    SEPTANTE_CINQ140 = "75W140", _("75W140")


# ---------------------------
# Modèle fusionné
# ---------------------------
class ControleGeneral(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_general_checkup",
        verbose_name=_("Maintenance"),
        null=True,  # autorisé vide à la création
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="controle_general_checkup_exemplaire_km",
        verbose_name="Kilomètres_checkup",
        null=True, blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    kilometrage_checkup = models.PositiveIntegerField(
        _("Kilométrage au moment du Checkup"),
        null=True,
        blank=True
    )



    # --- Essuie-glaces & Pare-brise ---
    essuie_glace_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK, verbose_name=_("Essuie-glace AV fonctionnel"))
    essuie_glace_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK, verbose_name=_("Essuie-glace AR fonctionnel"))
    balais_essuie_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Balais avants a remplacer"))
    balais_essuie_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Balai arrière à remplacer"))

    pare_brise_coups = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Pare-brise avec coups"))
    pare_brise_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Pare-brise à remplacer"))

    # --- Moteur & transmission ---
    moteur_fuite =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite moteur"))
    moteur_bruit =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bruit moteur"))
    moteur_perte =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Perte de puissance"))
    moteur_casse =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Moteur à remplacer"))
    moteur_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON, verbose_name=_("Niveau d'huile"))
    moteur_niveau_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"))
    moteur_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30, verbose_name=_("Qualité d'huile"))

    boite_fuite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite boîte de vitesse"))
    boite_bruit = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bruits boîte de vitesse"))
    boite_embrayage = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Problème d'embrayage"))
    boite_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile"))
    boite_niveau_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"))
    boite_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileBoiteEtat.choices, default=HuileBoiteEtat.SEPTANTE_CINQ, verbose_name=_("Qualité d'huile"))

    # --- Pont ----

    pont_fuite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite pont arrière"))
    pont_bruit = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bruits pont arrière"))
    pont_jeu = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu pont arrière"))
    pont_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile"))
    pont_niveau_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"))
    pont_niveau_huile_qualite = models.CharField(max_length=25, choices=HuilePontEtat.choices,default=HuilePontEtat.SEPTANTE_CINQ140,verbose_name=_("Qualité d'huile"))

    # --- Freins ---

    freins_usure_plaquettes_av = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes avants (%)"))
    freins_plaquettes_remplacer_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Plaquettes avant à remplacer"))
    freins_epaisseur_disques_av = models.FloatField(default=0.0, verbose_name=_("Épaisseur des disques avants (mm)"))
    freins_fentes_disques_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Présence de fentes sur les disques avants"))
    freins_disques_remplacer_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Disques avants à remplacer"))

    freins_usure_plaquettes_ar = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes arrières (%)"))
    freins_plaquettes_remplacer_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Plaquettes arrière à remplacer"))
    freins_epaisseur_disques_ar = models.FloatField(default=0, verbose_name=_("Épaisseur des disques arrières (mm)"))
    freins_fentes_disques_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Présence de fentes sur les disques arrières"))
    freins_disques_remplacer_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Disques arrières à remplacer"))

    freins_fuites = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Présence de fuite"))


    # --- Liquide ---
    frein_liquide_frein_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État liquide de frein"))
    freins_remplacement_liquide_frein = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Remplacement liquide de frein"))
    freins_specif_liquide_frein = models.CharField(max_length=100, blank=True, verbose_name=_("Spécification liquide de frein"))
    freins_quantite_liquide_frein = models.FloatField(default=0, null=True, blank=True, verbose_name=_("Quantité liquide de frein (L)"))

    direction_fuite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite direction assistée / crémaillère"), null=True, blank=True)
    niveau_direction = models.FloatField(default=0.0, null=True, blank=True, verbose_name=_("Niveau liquide direction"))

    # --- Bruits ---
    bruit_roulement_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État roulement de roue avant droit"), blank=True, null=True)
    bruit_roulement_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État roulement de roue avant gauche"),  blank=True, null=True)
    bruit_roulement_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État roulement de roue arrière droit"), blank=True, null=True)
    bruit_roulement_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État roulement de roue arrière gauche"),  blank=True, null=True)


    # --- Batterie ---
    batterie_etat =models.CharField(max_length=25, choices=BatterieEtat.choices, default=BatterieEtat.OK, verbose_name=_("État batterie"))

    # --- Jeux ---

    jeu_rotule_direction_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu rotule de direction avant droite"))
    jeu_rotule_direction_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu rotule de direction avant gauche"))
    jeu_rotule_direction_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu rotule de direction arrière droite"))
    jeu_rotule_direction_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu rotule de direction arrière gauche"))

    jeu_rotule_suspension_inferieure_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotule de suspension inférieure avant droite"))
    jeu_rotule_suspension_inferieure_avg= models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotule de suspension inférieure avant gauche"))
    jeu_rotule_suspension_inferieure_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotule de suspension inférieure arrière droite"))
    jeu_rotule_suspension_inferieure_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotule de suspension inférieure arrière droite"))

    jeu_rotule_suspension_superieure_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure avant droite"))
    jeu_rotule_suspension_superieure_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure avant gauche"))
    jeu_rotule_suspension_superieure_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure arrière droite"))
    jeu_rotule_suspension_superieure_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure arrière droite"))

    jeu_Biellette_barre_stabilisatrice_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de barre stabilisatrice avant droite"))
    jeu_Biellette_barre_stabilisatrice_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de barre stabilisatrice avant gauche"))
    jeu_Biellette_barre_stabilisatrice_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de barre stabilisatrice arrière droite"))
    jeu_Biellette_barre_stabilisatrice_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de barre stabilisatrice arrière gauche"))

    jeu_barre_stabilisatrice_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu barre stabilisatrice avant"))
    jeu_barre_stabilisatrice_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu barre stabilisatrice arrière"))

    jeu_amortisseur_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu amortisseur avant droit"))
    jeu_amortisseur_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu amortisseur avant gauche"))
    jeu_amortisseur_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu amortisseur arrière droit"))
    jeu_amortisseur_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu amortisseur arrière gauche"))

    jeu_roulement_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu roulement avant droit"))
    jeu_roulement_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu roulement avant gauche"))
    jeu_roulement_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu roulement arrière droit"))
    jeu_roulement_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu roulement arrière gauche"))

    jeu_triangle_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle avant droit"))
    jeu_triangle_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle avant gauche"))
    jeu_triangle_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle arrière droit"))
    jeu_triangle_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle arrière gauche"))

    jeu_multi_bras_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras avant droit"))
    jeu_multi_bras_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras avant gauche"))
    jeu_multi_bras_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras arrière droit"))
    jeu_multi_bras_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras arrière gauche"))


    # --- Réglage phares ---
    phares_reglages = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Réglage phares"))
    phares_avant = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Feux de routes"))
    phares_gros_phares = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Grand phares"))
    phares_clignotants = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Clignotants"))
    phares_recul = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Feux de recul"))
    phares_anti_brouillard_avant = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Phares anti-brouillard avant"))
    phares_anti_brouillard_arriere = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK, verbose_name=_("Phares anti-brouillard arrière"))


    # --- Nettoyage extérieur ---
    nettoyage_exterieur_traces_gomme = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Traces de gomme"))
    nettoyage_exterieur_carrosserie = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Carrosserie"))
    nettoyage_exterieur_jantes = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Jantes"))
    nettoyage_exterieur_sechage = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Séchage"))

    # --- Nettoyage intérieur ---
    nettoyage_interieur_vitres = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Vitres"))
    nettoyage_interieur_pare_brise = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Pare-brise"))
    nettoyage_interieur_aspirateur = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Aspirateur"))
    nettoyage_interieur_portes = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Intérieurs de porte"))
    nettoyage_interieur_sieges = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Sièges"))
    nettoyage_interieur_carpettes = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Carpettes"))
    nettoyage_interieur_tableau_de_bord = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Tableau de bord"))
    nettoyage_interieur_plastiques = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Plastiques"))



   # niveau boite

    #niveau pont
   # pneus bande de roulement sidewall
    #pression pneus

    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Contrôle général")
        verbose_name_plural = _("Contrôles généraux")

    def __str__(self):
        return _("Contrôle général – Maintenance %(id)s") % {"id": self.maintenance.id}

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_checkup is not None:
            if self.kilometrage_checkup < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_checkup': _(
                        f"Le kilométrage du check-up ({self.kilometrage_checkup}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_checkup:
            if self.kilometrage_checkup > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_checkup
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        super().save(*args, **kwargs)
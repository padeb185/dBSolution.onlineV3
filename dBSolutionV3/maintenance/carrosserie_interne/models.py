from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import RouesSerrageEtat, TAUX_HORAIRE_CHOICES
from maintenance.models import Maintenance




class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")




class CarrosserieInterne(models.Model):
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

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="intervention_carrosserie_interne",
        verbose_name=_("Maintenance"),
        null=True,  # autorisé vide à la création
        blank=True
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="carrosserie_interne"
    )
    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.PROTECT,
        related_name="carrosserie_interne"
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_intervention = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment de l'intervention"),
    )


        # Pare-chocs
    pare_choc_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Pare-chocs avant"))
    pare_choc_av_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    pare_choc_av_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix du pare-chocs avant"))
    pare_choc_av_quantite = models.IntegerField(default=0)



    pare_choc_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Pare-chocs arrière"))
    pare_choc_ar_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    pare_choc_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pare_choc_ar_quantite = models.IntegerField(default=0)



        # Boucliers
    bouclier_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bouclier avant"))
    bouclier_av_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    bouclier_av_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bouclier_av_quantite = models.IntegerField(default=0)



    bouclier_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Bouclier arrière"))
    bouclier_ar_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    bouclier_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bouclier_ar_quantite = models.IntegerField(default=0)




    support_pa_choc_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Support de pare-chocs avant"))
    support_pa_choc_av_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    support_pa_choc_av_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    support_pa_choc_av_quantite = models.IntegerField(default=0)

    support_pa_choc_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Support de pare-chocs arrière"))
    support_pa_choc_ar_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    support_pa_choc_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    support_pa_choc_ar_quantite = models.IntegerField(default=0)

    # Calandre
    calandre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Calandre"))
    calandre_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    calandre_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    calandre_quantite = models.IntegerField(default=0)






      # Ailes
    aile_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Aile avant droit"))
    aile_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    aile_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aile_avd_quantite = models.IntegerField(default=0)

    aile_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Aile avant gauche"))
    aile_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    aile_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aile_avg_quantite = models.IntegerField(default=0)

    aile_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Aile arrière droit"))
    aile_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    aile_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aile_ard_quantite = models.IntegerField(default=0)

    aile_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Aile arrière gauche"))
    aile_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    aile_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aile_arg_quantite = models.IntegerField(default=0)





    # Élargisseurs d'aile
    elargisseur_ail_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Élargisseur d'aile avant droit"))
    elargisseur_ail_avd_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    elargisseur_ail_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    elargisseur_ail_avd_quantite = models.IntegerField(default=0)


    elargisseur_ail_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Élargisseur d'aile avant gauche"))
    elargisseur_ail_avg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    elargisseur_ail_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    elargisseur_ail_avg_quantite = models.IntegerField(default=0)



    elargisseur_ail_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Élargisseur d'aile arrière droit"))
    elargisseur_ail_ard_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    elargisseur_ail_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    elargisseur_ail_ard_quantite = models.IntegerField(default=0)



    elargisseur_ail_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Élargisseur d'aile arrière gauche"))
    elargisseur_ail_arg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    elargisseur_ail_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    elargisseur_ail_arg_quantite = models.IntegerField(default=0)





    # Bas de caisse
    bas_de_caisse_d = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bas de caisse droit"))
    bas_de_caisse_d_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    bas_de_caisse_d_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bas_de_caisse_d_quantite = models.IntegerField(default=0)


    bas_de_caisse_g = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bas de caisse gauche"))
    bas_de_caisse_g_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    bas_de_caisse_g_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bas_de_caisse_g_quantite = models.IntegerField(default=0)

    # Portes
    porte_avd_po = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Porte avant droite"))
    porte_avd_po_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    porte_avd_po_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    porte_avd_po_quantite = models.IntegerField(default=0)

    porte_avg_po = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Porte avant gauche"))
    porte_avg_po_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    porte_avg_po_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    porte_avg_po_quantite = models.IntegerField(default=0)

    # Portes
    porte_ard_po = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                    verbose_name=_("Porte arrière droite"))
    porte_ard_po_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    porte_ard_po_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    porte_ard_po_quantite = models.IntegerField(default=0)

    porte_arg_po = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                    verbose_name=_("Porte arrière gauche"))
    porte_arg_po_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    porte_arg_po_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    porte_arg_po_quantite = models.IntegerField(default=0)

    # Poignée de porte
    poignee_porte = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Poignée de porte")
    )
    poignee_porte_oem = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name=_("Numéro OEM")
    )
    poignee_porte_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        blank=True,
        verbose_name=_("Prix")
    )
    poignee_porte_quantite = models.IntegerField(
        default=0,
        blank=True,
        verbose_name=_("Quantité")
    )

    # Coffre / hayon
    coffre_haillon = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                      verbose_name=_("Coffre / Hayon"))
    coffre_haillon_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    coffre_haillon_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coffre_haillon_quantite = models.IntegerField(default=0)

    # Capot
    capot_pi = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                verbose_name=_("Capot"))
    capot_pi_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    capot_pi_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capot_pi_quantite = models.IntegerField(default=0)

    # Joint de coffre et portes
    joint_coffre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                    verbose_name=_("Joint de coffre"))
    joint_coffre_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    joint_coffre_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joint_coffre_quantite = models.IntegerField(default=0)

    joint_porte_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                       verbose_name=_("Joint de porte avant droit"))
    joint_porte_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    joint_porte_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joint_porte_avd_quantite = models.IntegerField(default=0)

    # Joints de porte
    joint_porte_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                       verbose_name=_("Joint de porte avant gauche"))
    joint_porte_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    joint_porte_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joint_porte_avg_quantite = models.IntegerField(default=0)

    joint_porte_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                       verbose_name=_("Joint de porte arrière droit"))
    joint_porte_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    joint_porte_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joint_porte_ard_quantite = models.IntegerField(default=0)

    joint_porte_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                       verbose_name=_("Joint de porte arrière gauche"))
    joint_porte_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    joint_porte_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joint_porte_arg_quantite = models.IntegerField(default=0)

    # Coquilles d'aile
    coquille_ai_avd = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Coquille d'aile avant droit")
    )
    coquille_ai_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    coquille_ai_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coquille_ai_avd_quantite = models.IntegerField(default=0)

    coquille_ai_avg = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Coquille d'aile avant gauche")
    )
    coquille_ai_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    coquille_ai_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coquille_ai_avg_quantite = models.IntegerField(default=0)

    coquille_ai_ard = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Coquille d'aile arrière droit")
    )
    coquille_ai_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    coquille_ai_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coquille_ai_ard_quantite = models.IntegerField(default=0)

    coquille_ai_arg = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Coquille d'aile arrière gauche")
    )
    coquille_ai_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    coquille_ai_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coquille_ai_arg_quantite = models.IntegerField(default=0)

    # Supports
    support_radiateur = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Support de radiateur")
    )
    support_radiateur_oem = models.CharField(max_length=25, null=True, blank=True,
                                             verbose_name=_("Numero OEM"))
    support_radiateur_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    support_radiateur_quantite = models.IntegerField(default=0)

    # Pare-brise
    pa_brise = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Pare-brise")
    )
    pa_brise_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    pa_brise_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pa_brise_quantite = models.IntegerField(default=0)

    # Vitres de portes
    vitre_porte_avd = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Vitre de porte avant droite")
    )
    vitre_porte_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    vitre_porte_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vitre_porte_avd_quantite = models.IntegerField(default=0)

    vitre_porte_avg = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Vitre de porte avant gauche")
    )
    vitre_porte_avg_oem = models.CharField(max_length=25, null=True, blank=True,
                                           verbose_name=_("Vitre de porte avant gauche oem"))
    vitre_porte_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vitre_porte_avg_quantite = models.IntegerField(default=0)

    vitre_porte_ard = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Vitre de porte arrière droite")
    )
    vitre_porte_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    vitre_porte_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vitre_porte_ard_quantite = models.IntegerField(default=0)

    # Vitre de porte arrière gauche
    vitre_porte_arg = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Vitre de porte arrière gauche")
    )
    vitre_porte_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    vitre_porte_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vitre_porte_arg_quantite = models.IntegerField(default=0)

    # Lunette arrière
    lunette = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                               verbose_name=_("Lunette / vitre arrière"))
    lunette_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    lunette_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    lunette_quantite = models.IntegerField(default=0)

    # Rétroviseurs
    retroviseur_d = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                     verbose_name=_("Rétroviseur droit"))
    retroviseur_d_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    retroviseur_d_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    retroviseur_d_quantite = models.IntegerField(default=0)

    retroviseur_g = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                     verbose_name=_("Rétroviseur gauche"))
    retroviseur_g_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    retroviseur_g_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    retroviseur_g_quantite = models.IntegerField(default=0)

    # Phares
    phare_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                 verbose_name=_("Phare avant droit"))
    phare_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    phare_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    phare_avd_quantite = models.IntegerField(default=0)

    phare_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                 verbose_name=_("Phare avant gauche"))
    phare_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    phare_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    phare_avg_quantite = models.IntegerField(default=0)

    phare_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                 verbose_name=_("Feu arrière droit"))
    phare_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    phare_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    phare_ard_quantite = models.IntegerField(default=0)

    phare_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                 verbose_name=_("Feu arrière gauche"))
    phare_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    phare_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    phare_arg_quantite = models.IntegerField(default=0)

    # Clignotants
    clignotant_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                      verbose_name=_("Clignotant avant droit"))
    clignotant_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    clignotant_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clignotant_avd_quantite = models.IntegerField(default=0)

    clignotant_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                      verbose_name=_("Clignotant avant gauche"))
    clignotant_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    clignotant_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clignotant_avg_quantite = models.IntegerField(default=0)

    clignotant_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                      verbose_name=_("Clignotant arrière droit"))
    clignotant_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    clignotant_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clignotant_ard_quantite = models.IntegerField(default=0)

    clignotant_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                      verbose_name=_("Clignotant arrière gauche"))
    clignotant_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    clignotant_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clignotant_arg_quantite = models.IntegerField(default=0)

    # Troisième feu stop
    troisieme_feu_stop = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                          verbose_name=_("Troisième feu stop"))
    troisieme_feu_stop_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    troisieme_feu_stop_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    troisieme_feu_stop_quantite = models.IntegerField(default=0)

    # Capteur de recul
    capteur_recul = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                     verbose_name=_("Capteur de recul"))
    capteur_recul_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    capteur_recul_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capteur_recul_quantite = models.IntegerField(default=0)

    # Anti-brouillards
    anti_brouillard_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                           verbose_name=_("Anti-brouillard avant droit"))
    anti_brouillard_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    anti_brouillard_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    anti_brouillard_avd_quantite = models.IntegerField(default=0)

    anti_brouillard_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                           verbose_name=_("Anti-brouillard avant gauche"))
    anti_brouillard_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    anti_brouillard_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    anti_brouillard_avg_quantite = models.IntegerField(default=0)

    anti_brouillard_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                          verbose_name=_("Anti-brouillard arrière"))
    anti_brouillard_ar_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    anti_brouillard_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    anti_brouillard_ar_quantite = models.IntegerField(default=0)

    # Clips et visserie
    clips = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                             verbose_name=_("Clips"))
    clips_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    clips_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clips_quantite = models.IntegerField(default=0)

    visserie = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                verbose_name=_("Visserie"))
    visserie_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    visserie_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    visserie_quantite = models.IntegerField(default=0)

    # Peinture
    peinture_avant_gauche = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Peinture de l'aile avant gauche")
    )
    peinture_avant_gauche_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_avant_gauche_quantite = models.IntegerField(default=0)

    peinture_avant_droite = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Peinture de l'aile avant droite")
    )
    peinture_avant_droite_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_avant_droite_quantite = models.IntegerField(default=0)

    peinture_arriere_droite = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Peinture de l'aile arrière droite")
    )
    peinture_arriere_droite_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_arriere_droite_quantite = models.IntegerField(default=0)

    peinture_arriere_gauche = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Peinture de l'aile arrière gauche")
    )
    peinture_arriere_gauche_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_arriere_gauche_quantite = models.IntegerField(default=0)

    peinture_face_avant = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Peinture de la face avant")
    )
    peinture_face_avant_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_face_avant_quantite = models.IntegerField(default=0)

    peinture_capot = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Peinture du capot")
    )
    peinture_capot_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_capot_quantite = models.IntegerField(default=0)

    peinture_arriere_complete = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Peinture arrière complète")
    )
    peinture_arriere_complete_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_arriere_complete_quantite = models.IntegerField(default=0)

    peinture_complete = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Peinture complète")
    )
    peinture_complete_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_complete_quantite = models.IntegerField(default=0)



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
        related_name="carrosserie_interne",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="carrosserie_interne"
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
        related_name="carrosserie_interne_societe"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )


    remarques = models.TextField(verbose_name=_("Remarques"), blank=True, null=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)




    total_pieces = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_main_oeuvre = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_peinture = models.DecimalField(max_digits=12, decimal_places=2, default=0)




    total_htva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_tva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_tvac = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True)



    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe


    class Meta:
        verbose_name = _("Carrosserie Interne")
        verbose_name_plural = _("Carrosseries Internes")

    def __str__(self):
        if self.voiture_exemplaire_id:
            return f"{self.voiture_exemplaire} - {self.date.strftime('%Y-%m-%d')}"
        return f"Carrosserie interne - {self.date.strftime('%Y-%m-%d')}"

    def clean(self):
        if self.voiture_exemplaire_id and self.kilometrage_intervention:
            if self.kilometrage_intervention < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError(
                    _("Le kilométrage de l'intervention (%(intervention)s) ne peut pas être inférieur au kilométrage actuel (%(current)s)."),
                    params={
                        "intervention": self.kilometrage_intervention,
                        "current": self.voiture_exemplaire.kilometres_chassis,
                    }
                )

    def save(self, *args, **kwargs):

        if self.voiture_exemplaire_id and self.kilometrage_intervention:
            if self.kilometrage_intervention > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_intervention
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        self.total_pieces = self._calculate_total_pieces()

        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Carrosserie interne") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])
        super().save(*args, **kwargs)



    def _calculate_total_pieces(self):

        total = Decimal(0)
        for field in self._meta.fields:
            if field.name.endswith("_prix"):
                quant_field_name = f"{field.name[:-5]}_quantite"
                quant = getattr(self, quant_field_name, 0)
                prix = getattr(self, field.name, Decimal(0))
                total += (prix or Decimal(0)) * (quant or 0)
        return total





    def recalcul_totaux(self):
        pieces = sum(item.montant_calcule for item in self.items.all())
        main_oeuvre = sum(item.montant_htva for item in getattr(self, "main_oeuvre", []))
        peinture = sum(item.montant_htva for item in getattr(self, "peinture", []))

        htva = pieces + main_oeuvre + peinture
        tva = htva * Decimal("0.21")

        self.total_pieces = pieces
        self.total_main_oeuvre = main_oeuvre
        self.total_peinture = peinture

        self.total_htva = htva
        self.total_tva = tva
        self.total_tvac = htva + tva

        self.save(update_fields=[
            "total_pieces",
            "total_main_oeuvre",
            "total_peinture",
            "total_htva",
            "total_tva",
            "total_tvac",
        ])

    @property
    def total_htva_calculate(self):
        return sum(item.montant_calcule for item in self.items.all())

    @property
    def total_tva_calculate(self):
        return sum(item.tva_a_recuperer for item in self.items.all())

    @property
    def total_tvac_calculate(self):
        return self.total_htva + self.total_tva





    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        etats_a_afficher = {
            EtatOKNotOK.A_REMPLACER,
            EtatOKNotOK.REMPLACE,
        }

        for field in self._meta.fields:
            field_name = field.name

            # Uniquement les champs d'état utilisant EtatOKNotOK
            if not isinstance(field, models.CharField):
                continue

            if not field.choices:
                continue

            choix_du_champ = {
                choix[0]
                for choix in field.choices
            }

            choix_etat_ok_not_ok = {
                choix[0]
                for choix in EtatOKNotOK.choices
            }

            if choix_du_champ != choix_etat_ok_not_ok:
                continue

            etat = getattr(self, field_name, None)

            if etat not in etats_a_afficher:
                continue

            # Champs associés
            nom_champ_prix = f"{field_name}_prix"
            nom_champ_quantite = f"{field_name}_quantite"
            nom_champ_oem = f"{field_name}_oem"

            # Prix
            prix = getattr(
                self,
                nom_champ_prix,
                Decimal("0.00"),
            )

            if prix is None:
                prix = Decimal("0.00")

            prix = Decimal(str(prix))

            # Quantité
            quantite = getattr(
                self,
                nom_champ_quantite,
                0,
            )

            if quantite is None:
                quantite = 0

            quantite = Decimal(str(quantite))

            # Numéro OEM
            numero_oem = getattr(
                self,
                nom_champ_oem,
                "",
            )

            if numero_oem is None:
                numero_oem = ""

            # Total de la ligne
            total = (
                    prix * quantite
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total_general += total

            rapport.append({
                "champ": field.verbose_name,
                "code": field_name,
                "etat": etat,
                "etat_label": dict(
                    EtatOKNotOK.choices
                ).get(etat, etat),
                "oem": numero_oem,
                "prix": prix,
                "quantite": quantite,
                "total": total,
            })

        total_general = total_general.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        return {
            "lignes": rapport,
            "total_general": total_general,
        }




        
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

        temps_minutes = Decimal(
            str(self.main_oeuvre.temps_minutes or 0)
        )

        taux_horaire = Decimal(
            str(self.taux_horaire or Decimal("50.00"))
        )

        cout = (
                temps_minutes
                / Decimal("60")
                * taux_horaire
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


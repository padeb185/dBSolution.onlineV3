from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import RouesSerrageEtat, TAUX_HORAIRE_CHOICES, TVAConfig
from maintenance.models import Maintenance




class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")

class PeintureEtat(models.TextChoices):
    PEINT = "PEINT", _("Peint")
    APEINDRE = "APEINDRE", _("A peindre")



class CarrosserieInterne(models.Model):

    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )


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

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    # Pare-chocs
    pare_choc_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Pare-chocs avant"))
    pare_choc_av_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    pare_choc_av_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    pare_choc_av_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    pare_choc_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Pare-chocs arrière"))
    pare_choc_ar_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    pare_choc_ar_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    pare_choc_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




        # Boucliers
    bouclier_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bouclier avant"))
    bouclier_av_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    bouclier_av_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    bouclier_av_quantite = models.IntegerField(default=0, verbose_name="Quantité")



    bouclier_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Bouclier arrière"))
    bouclier_ar_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    bouclier_ar_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    bouclier_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))





    support_pa_choc_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Support de pare-chocs avant"))
    support_pa_choc_av_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("OEM"))
    support_pa_choc_av_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    support_pa_choc_av_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    support_pa_choc_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Support de pare-chocs arrière"))
    support_pa_choc_ar_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("OEM"))
    support_pa_choc_ar_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    support_pa_choc_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    # Calandre
    calandre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Calandre"))
    calandre_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    calandre_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    calandre_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))







      # Ailes
    aile_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Aile avant droit"))
    aile_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    aile_avd_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    aile_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    aile_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Aile avant gauche"))
    aile_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    aile_avg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    aile_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    aile_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Aile arrière droit"))
    aile_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    aile_ard_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    aile_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    aile_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Aile arrière gauche"))
    aile_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    aile_arg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    aile_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))






    # Élargisseurs d'aile
    elargisseur_ail_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Élargisseur d'aile avant droit"))
    elargisseur_ail_avd_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("OEM"))
    elargisseur_ail_avd_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    elargisseur_ail_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    elargisseur_ail_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Élargisseur d'aile avant gauche"))
    elargisseur_ail_avg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("OEM"))
    elargisseur_ail_avg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    elargisseur_ail_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    elargisseur_ail_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Élargisseur d'aile arrière droit"))
    elargisseur_ail_ard_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("OEM"))
    elargisseur_ail_ard_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    elargisseur_ail_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    elargisseur_ail_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Élargisseur d'aile arrière gauche"))
    elargisseur_ail_arg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("OEM"))
    elargisseur_ail_arg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    elargisseur_ail_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))






    # Bas de caisse
    bas_de_caisse_d = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bas de caisse droit"))
    bas_de_caisse_d_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("OEM"))
    bas_de_caisse_d_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    bas_de_caisse_d_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    bas_de_caisse_g = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bas de caisse gauche"))
    bas_de_caisse_g_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("OEM"))
    bas_de_caisse_g_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    bas_de_caisse_g_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    # Portes
    porte_avd_po = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Porte avant droite"))
    porte_avd_po_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    porte_avd_po_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    porte_avd_po_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    porte_avg_po = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Porte avant gauche"))
    porte_avg_po_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    porte_avg_po_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    porte_avg_po_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    # Portes
    porte_ard_po = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Porte arrière droite"))
    porte_ard_po_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    porte_ard_po_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    porte_ard_po_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    porte_arg_po = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Porte arrière gauche"))
    porte_arg_po_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    porte_arg_po_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    porte_arg_po_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


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
        verbose_name=_("OEM")
    )
    poignee_porte_quantite = models.IntegerField(
        default=0,
        blank=True,
        verbose_name=_("Quantité")
    )

    poignee_porte_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        blank=True, verbose_name=_("Prix d'achat HTVA")
    )



    # Coffre / hayon
    coffre_haillon = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Coffre / Hayon"))
    coffre_haillon_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    coffre_haillon_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    coffre_haillon_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    # Capot
    capot_pi = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capot"))
    capot_pi_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    capot_pi_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    capot_pi_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    # Joint de coffre et portes
    joint_coffre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Joint de coffre"))
    joint_coffre_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    joint_coffre_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    joint_coffre_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    joint_porte_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Joint de porte avant droit"))
    joint_porte_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    joint_porte_avd_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    joint_porte_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    # Joints de porte
    joint_porte_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Joint de porte avant gauche"))
    joint_porte_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    joint_porte_avg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    joint_porte_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    joint_porte_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Joint de porte arrière droit"))
    joint_porte_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    joint_porte_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    joint_porte_ard_quantite = models.IntegerField(default=0, verbose_name="Quantité")


    joint_porte_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Joint de porte arrière gauche"))
    joint_porte_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    joint_porte_arg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    joint_porte_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    # Coquilles d'aile
    coquille_ai_avd = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Coquille d'aile avant droit")
    )
    coquille_ai_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    coquille_ai_avd_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    coquille_ai_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    coquille_ai_avg = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Coquille d'aile avant gauche")
    )
    coquille_ai_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    coquille_ai_avg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    coquille_ai_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    coquille_ai_ard = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Coquille d'aile arrière droit")
    )
    coquille_ai_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    coquille_ai_ard_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    coquille_ai_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    coquille_ai_arg = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Coquille d'aile arrière gauche")
    )
    coquille_ai_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    coquille_ai_arg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    coquille_ai_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    # Supports
    support_radiateur = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Support de radiateur")
    )
    support_radiateur_oem = models.CharField(max_length=25, null=True, blank=True,
                                             verbose_name=_("OEM"))
    support_radiateur_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    support_radiateur_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    # Pare-brise
    pa_brise = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Pare-brise")
    )
    pa_brise_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    pa_brise_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    pa_brise_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    # Vitres de portes
    vitre_porte_avd = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Vitre de porte avant droite")
    )
    vitre_porte_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    vitre_porte_avd_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    vitre_porte_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    vitre_porte_avg = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Vitre de porte avant gauche")
    )
    vitre_porte_avg_oem = models.CharField(max_length=25, null=True, blank=True,
                                           verbose_name=_("OEM"))
    vitre_porte_avg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    vitre_porte_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    vitre_porte_ard = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Vitre de porte arrière droite")
    )
    vitre_porte_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    vitre_porte_ard_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    vitre_porte_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    # Vitre de porte arrière gauche
    vitre_porte_arg = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
        verbose_name=_("Vitre de porte arrière gauche")
    )
    vitre_porte_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    vitre_porte_arg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    vitre_porte_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    # Lunette arrière
    lunette = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                               verbose_name=_("Lunette / vitre arrière"))
    lunette_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    lunette_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    lunette_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    # Rétroviseurs
    retroviseur_d = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                     verbose_name=_("Rétroviseur droit"))
    retroviseur_d_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    retroviseur_d_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    retroviseur_d_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    retroviseur_g = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                     verbose_name=_("Rétroviseur gauche"))
    retroviseur_g_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    retroviseur_g_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    retroviseur_g_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    # Phares
    phare_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                 verbose_name=_("Phare avant droit"))
    phare_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    phare_avd_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    phare_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    phare_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                 verbose_name=_("Phare avant gauche"))
    phare_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    phare_avg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    phare_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    phare_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                 verbose_name=_("Feu arrière droit"))
    phare_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    phare_ard_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    phare_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)



    phare_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                 verbose_name=_("Feu arrière gauche"))
    phare_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    phare_arg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    phare_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    # Clignotants
    clignotant_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                      verbose_name=_("Clignotant avant droit"))
    clignotant_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    clignotant_avd_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    clignotant_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    clignotant_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                      verbose_name=_("Clignotant avant gauche"))
    clignotant_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    clignotant_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clignotant_avg_quantite = models.IntegerField(default=0, verbose_name="Quantité")


    clignotant_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                      verbose_name=_("Clignotant arrière droit"))
    clignotant_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    clignotant_ard_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    clignotant_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    clignotant_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                      verbose_name=_("Clignotant arrière gauche"))
    clignotant_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    clignotant_arg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    clignotant_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    # Troisième feu stop
    troisieme_feu_stop = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                          verbose_name=_("Troisième feu stop"))
    troisieme_feu_stop_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    troisieme_feu_stop_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    troisieme_feu_stop_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    # Capteur de recul
    capteur_recul = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                     verbose_name=_("Capteur de recul"))
    capteur_recul_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    capteur_recul_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    capteur_recul_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)



    # Anti-brouillards
    anti_brouillard_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                           verbose_name=_("Anti-brouillard avant droit"))
    anti_brouillard_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    anti_brouillard_avd_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    anti_brouillard_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    anti_brouillard_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                           verbose_name=_("Anti-brouillard avant gauche"))
    anti_brouillard_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    anti_brouillard_avg_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    anti_brouillard_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    anti_brouillard_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                          verbose_name=_("Anti-brouillard arrière"))
    anti_brouillard_ar_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    anti_brouillard_ar_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    anti_brouillard_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    # Clips et visserie
    clips = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                             verbose_name=_("Clips"))
    clips_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    clips_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    clips_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    visserie = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                verbose_name=_("Visserie"))
    visserie_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("OEM"))
    visserie_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    visserie_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))




    # Peinture
    peinture_avant_gauche = models.CharField(
        max_length=25, choices=PeintureEtat.choices, default=PeintureEtat.PEINT,
        verbose_name=_("Peinture de l'aile avant gauche")
    )
    peinture_avant_gauche_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    peinture_avant_gauche_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)




    peinture_avant_droite = models.CharField(
        max_length=25, choices=PeintureEtat.choices, default=PeintureEtat.PEINT,
        verbose_name=_("Peinture de l'aile avant droite")
    )
    peinture_avant_droite_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    peinture_avant_droite_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)




    peinture_arriere_droite = models.CharField(
        max_length=25, choices=PeintureEtat.choices, default=PeintureEtat.PEINT,
        verbose_name=_("Peinture de l'aile arrière droite")
    )
    peinture_arriere_droite_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    peinture_arriere_droite_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)




    peinture_arriere_gauche = models.CharField(
        max_length=25, choices=PeintureEtat.choices, default=PeintureEtat.PEINT,
        verbose_name=_("Peinture de l'aile arrière gauche")
    )
    peinture_arriere_gauche_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    peinture_arriere_gauche_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)




    peinture_face_avant = models.CharField(
        max_length=25, choices=PeintureEtat.choices, default=PeintureEtat.PEINT, verbose_name=_("Peinture de la face avant")
    )
    peinture_face_avant_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    peinture_face_avant_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)




    peinture_capot = models.CharField(
        max_length=25, choices=PeintureEtat.choices, default=PeintureEtat.PEINT, verbose_name=_("Peinture du capot")
    )
    peinture_capot_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    peinture_capot_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)




    peinture_arriere_complete = models.CharField(
        max_length=25, choices=PeintureEtat.choices, default=PeintureEtat.PEINT, verbose_name=_("Peinture arrière complète")
    )
    peinture_arriere_complete_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    peinture_arriere_complete_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)




    peinture_complete = models.CharField(
        max_length=25, choices=PeintureEtat.choices, default=PeintureEtat.PEINT, verbose_name=_("Peinture complète")
    )
    peinture_complete_quantite = models.IntegerField(default=0, verbose_name="Quantité")
    peinture_complete_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)




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

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

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

        if (
                self.kilometrage_intervention is not None
                and self.kilometres_chassis is not None
        ):
            self.kilometrage_variation = (
                    self.kilometrage_intervention - self.kilometres_chassis
            )


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

        # =========================
        # ÉTATS À AFFICHER
        # =========================
        etats_a_afficher = {
            EtatOKNotOK.A_REMPLACER,
            EtatOKNotOK.REMPLACE,
            PeintureEtat.APEINDRE,
        }

        # =========================
        # CHOIX CONNUS
        # =========================
        choix_etat_ok_not_ok = {
            choix[0]
            for choix in EtatOKNotOK.choices
        }

        choix_peinture = {
            choix[0]
            for choix in PeintureEtat.choices
        }

        # Labels combinés
        labels_etats = {
            **dict(EtatOKNotOK.choices),
            **dict(PeintureEtat.choices),
        }

        # =========================
        # PARCOURS DES CHAMPS
        # =========================
        for field in self._meta.fields:

            field_name = field.name

            # Seulement CharField
            if not isinstance(field, models.CharField):
                continue

            # Seulement champs avec choices
            if not field.choices:
                continue

            choix_du_champ = {
                choix[0]
                for choix in field.choices
            }

            # Accepter EtatOKNotOK OU PeintureEtat
            if (
                    choix_du_champ != choix_etat_ok_not_ok
                    and choix_du_champ != choix_peinture
            ):
                continue

            # =========================
            # ÉTAT
            # =========================
            etat = getattr(
                self,
                field_name,
                None,
            )

            if etat not in etats_a_afficher:
                continue

            # =========================
            # CHAMPS ASSOCIÉS
            # =========================
            nom_champ_prix = f"{field_name}_prix"
            nom_champ_quantite = f"{field_name}_quantite"
            nom_champ_oem = f"{field_name}_oem"

            # =========================
            # PRIX
            # =========================
            prix = getattr(
                self,
                nom_champ_prix,
                Decimal("0.00"),
            )

            if prix is None:
                prix = Decimal("0.00")

            prix = Decimal(str(prix))

            # =========================
            # QUANTITÉ
            # =========================
            quantite = getattr(
                self,
                nom_champ_quantite,
                0,
            )

            if quantite is None:
                quantite = 0

            quantite = Decimal(str(quantite))

            # =========================
            # OEM
            # =========================
            oem = getattr(
                self,
                nom_champ_oem,
                "",
            )

            if oem is None:
                oem = ""

            # =========================
            # TOTAL LIGNE
            # =========================
            total = (
                    prix * quantite
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total_general += total

            # =========================
            # RAPPORT
            # =========================
            rapport.append({
                "champ": field.verbose_name,
                "code": field_name,

                "etat": etat,
                "etat_label": labels_etats.get(
                    etat,
                    etat,
                ),

                "oem": oem,

                "prix": prix,
                "quantite": quantite,
                "total": total,
            })

        # =========================
        # TOTAL GÉNÉRAL
        # =========================
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


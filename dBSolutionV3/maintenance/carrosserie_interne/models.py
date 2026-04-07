from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from maintenance.models import Maintenance




class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")



class CarrosserieInterne(models.Model):
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
        blank=True
    )

    kilometrage_intervention = models.PositiveIntegerField(
        _("Kilométrage au moment de l'intervention"),
        null=True,
        blank=True
    )


        # Pare-chocs
    pare_choc_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Pare-chocs avant"))
    pare_choc_av_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    pare_choc_av_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    pare_choc_av_quantite = models.IntegerField(default=0, verbose_name="Quantite")



    pare_choc_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Pare-chocs arrière"))
    pare_choc_ar_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    pare_choc_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    pare_choc_ar_quantite = models.IntegerField(default=0)



        # Boucliers
    bouclier_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bouclier avant"))
    bouclier_av_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    bouclier_av_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bouclier_av_quantite = models.IntegerField(default=0)



    bouclier_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Bouclier arrière"))
    bouclier_ar_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    bouclier_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    bouclier_ar_quantite = models.IntegerField(default=0)




    support_pa_choc_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Support de pare-chocs avant"))
    support_pa_choc_av_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    support_pa_choc_av_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    support_pa_choc_av_quantite = models.IntegerField(default=0)

    support_pa_choc_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Support de pare-chocs arrière"))
    support_pa_choc_ar_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    support_pa_choc_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    support_pa_choc_ar_quantite = models.IntegerField(default=0)

    # Calandre
    calandre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Calandre"))
    calandre_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    calandre_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    calandre_quantite = models.IntegerField(default=0)






      # Ailes
    aile_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Aile avant droite"))
    aile_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    aile_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    aile_avd_quantite = models.IntegerField(default=0)

    aile_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Aile avant gauche"))
    aile_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    aile_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    aile_avg_quantite = models.IntegerField(default=0)

    aile_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Aile arrière droite"))
    aile_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    aile_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    aile_ard_quantite = models.IntegerField(default=0)

    aile_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Aile arrière gauche"))
    aile_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    aile_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    aile_arg_quantite = models.IntegerField(default=0)





    # Élargisseurs d'aile
    elargisseur_aile_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Élargisseur d'aile avant droite"))
    elargisseur_aile_avd_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    elargisseur_aile_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    elargisseur_aile_avd_quantite = models.IntegerField(default=0)


    elargisseur_aile_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Élargisseur d'aile avant gauche"))
    elargisseur_aile_avg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    elargisseur_aile_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    elargisseur_aile_avg_quantite = models.IntegerField(default=0)



    elargisseur_aile_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Élargisseur d'aile arrière droite"))
    elargisseur_aile_ard_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    elargisseur_aile_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    elargisseur_aile_ard_quantite = models.IntegerField(default=0)



    elargisseur_aile_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Élargisseur d'aile arrière gauche"))
    elargisseur_aile_arg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    elargisseur_aile_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    elargisseur_aile_arg_quantite = models.IntegerField(default=0)





    # Bas de caisse
    bas_de_caisse_d = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bas de caisse droit"))
    bas_de_caisse_d_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    bas_de_caisse_d_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    bas_de_caisse_d_quantite = models.IntegerField(default=0)


    bas_de_caisse_g = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bas de caisse gauche"))
    bas_de_caisse_g_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    bas_de_caisse_g_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    bas_de_caisse_g_quantite = models.IntegerField(default=0)

    # Portes
    porte_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Porte avant droite"))
    porte_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    porte_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    porte_avd_quantite = models.IntegerField(default=0)

    porte_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Porte avant gauche"))
    porte_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    porte_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    porte_avg_quantite = models.IntegerField(default=0)

    porte_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Porte arrière droite"))
    porte_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    porte_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    porte_ard_quantite = models.IntegerField(default=0)

    porte_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Porte arrière gauche"))
    porte_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    porte_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    porte_arg_quantite = models.IntegerField(default=0)

    poignee_porte = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Poignée de porte"))
    poignee_porte_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    poignee_porte_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    poignee_porte_quantite = models.IntegerField(default=0)

    # Coffre / hayon
    coffre_haillon = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Coffre / Hayon"))
    coffre_haillon_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    coffre_haillon_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    coffre_haillon_quantite = models.IntegerField(default=0)



    # Capot
    capot = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capot"))
    capot_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    capot_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    capot_quantite = models.IntegerField(default=0)



    # Joint de coffre et portes
    joint_coffre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Joint de coffre"))
    joint_coffre_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    joint_coffre_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joint_coffre_quantite = models.IntegerField(default=0)

    joint_porte_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Joint de porte avant droite"))
    joint_porte_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    joint_porte_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    joint_porte_avd_quantite = models.IntegerField(default=0)

    # Joints de porte
    joint_porte_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Joint de porte avant gauche"))
    joint_porte_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    joint_porte_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    joint_porte_avg_quantite = models.IntegerField(default=0)

    joint_porte_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                       verbose_name=_("Joint de porte arrière droite"))
    joint_porte_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    joint_porte_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joint_porte_ard_quantite = models.IntegerField(default=0)

    joint_porte_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Joint de porte arrière gauche"))
    joint_porte_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    joint_porte_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    joint_porte_arg_quantite = models.IntegerField(default=0)

    # Coquilles d'aile
    coquille_aile_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Coquille d'aile avant droite"))
    coquille_aile_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    coquille_aile_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coquille_aile_avd_quantite = models.IntegerField(default=0)

    coquille_aile_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                         verbose_name=_("Coquille d'aile avant gauche"))
    coquille_aile_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    coquille_aile_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    coquille_aile_avg_quantite = models.IntegerField(default=0)

    coquille_aile_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                         verbose_name=_("Coquille d'aile arrière droite"))
    coquille_aile_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    coquille_aile_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coquille_aile_ard_quantite = models.IntegerField(default=0)

    coquille_aile_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Coquille d'aile arrière gauche"))
    coquille_aile_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    coquille_aile_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    coquille_aile_arg_quantite = models.IntegerField(default=0)

    # Supports
    support_radiateur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Support de radiateur"))
    support_radiateur_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Support de radiateur oem"))
    support_radiateur_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    support_radiateur_quantite = models.IntegerField(default=0)






        # Pare-brise
    pa_brise = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Pare-brise"))
    pa_brise_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    pa_brise_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    pa_brise_quantite = models.IntegerField(default=0)




        # Vitres de portes
    vitre_porte_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Vitre de porte avant droite"))
    vitre_porte_avd_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    vitre_porte_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    vitre_porte_avd_quantite = models.IntegerField(default=0)


    vitre_porte_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Vitre de porte avant gauche"))
    vitre_porte_avg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Vitre de porte avant gauche oem"))
    vitre_porte_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    vitre_porte_avg_quantite = models.IntegerField(default=0)


    vitre_porte_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Vitre de porte arrière droite"))
    vitre_porte_ard_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    vitre_porte_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    vitre_porte_ard_quantite = models.IntegerField(default=0)



    vitre_porte_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Vitre de porte arrière gauche"))
    vitre_porte_arg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    vitre_porte_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    vitre_porte_arg_quantite = models.IntegerField(default=0)








        # Lunette arrière
    lunette = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Lunette / vitre arrière"))
    lunette_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    lunette_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    lunette_quantite = models.IntegerField(default=0)




       # Rétroviseurs
    retroviseur_d = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Rétroviseur droit"))
    retroviseur_d_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    retroviseur_d_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    retroviseur_d_quantite = models.IntegerField(default=0)



    retroviseur_g = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Rétroviseur gauche"))
    retroviseur_g_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    retroviseur_g_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    retroviseur_g_quantite = models.IntegerField(default=0)

    # Phares
    phare_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Phare avant droit"))
    phare_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    phare_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    phare_avd_quantite = models.IntegerField(default=0)

    phare_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                 verbose_name=_("Phare avant gauche"))
    phare_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    phare_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    phare_avg_quantite = models.IntegerField(default=0)

    phare_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                 verbose_name=_("Feu arrière droit"))
    phare_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    phare_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    phare_ard_quantite = models.IntegerField(default=0)

    phare_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Feu arrière gauche"))
    phare_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    phare_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    phare_arg_quantite = models.IntegerField(default=0)

    # Clignotants
    clignotant_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Clignotant avant droit"))
    clignotant_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    clignotant_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    clignotant_avd_quantite = models.IntegerField(default=0)

    clignotant_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Clignotant avant gauche"))
    clignotant_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    clignotant_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    clignotant_avg_quantite = models.IntegerField(default=0)

    clignotant_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Clignotant arrière droit"))
    clignotant_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    clignotant_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    clignotant_ard_quantite = models.IntegerField(default=0)

    clignotant_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Clignotant arrière gauche"))
    clignotant_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    clignotant_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    clignotant_arg_quantite = models.IntegerField(default=0)

    troisieme_feu_stop = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                          verbose_name=_("Troisième feu stop"))
    troisieme_feu_stop_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    troisieme_feu_stop_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    troisieme_feu_stop_quantite = models.IntegerField(default=0)

    # Capteur de recul
    capteur_recul = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                     verbose_name=_("Capteur de recul"))
    capteur_recul_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    capteur_recul_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    capteur_recul_quantite = models.IntegerField(default=0)

    # Anti-brouillards avant droit
    anti_brouillard_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                           verbose_name=_("Anti-brouillard avant droit"))
    anti_brouillard_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    anti_brouillard_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    anti_brouillard_avd_quantite = models.IntegerField(default=0)

    # Anti-brouillards avant gauche
    anti_brouillard_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Anti-brouillard avant gauche"))
    anti_brouillard_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    anti_brouillard_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    anti_brouillard_avg_quantite = models.IntegerField(default=0)

    # Anti-brouillards arrière
    anti_brouillard_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Anti-brouillard arrière"))
    anti_brouillard_ar_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Numero OEM"))
    anti_brouillard_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    anti_brouillard_ar_quantite = models.IntegerField(default=0)

    # Clips et visserie
    clips = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Clips"))
    clips_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    clips_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    clips_quantite = models.IntegerField(default=0)


    visserie = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Visserie"))
    visserie_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Numero OEM"))
    visserie_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    visserie_quantite = models.IntegerField(default=0)










    # Peinture
    peinture_avant_gauche = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Peinture de l'aile avant gauche"))
    peinture_avant_gauche_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    peinture_avant_gauche_quantite = models.IntegerField(default=0)

    peinture_avant_droite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Peinture de l'aile avant droite"))
    peinture_avant_droite_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    peinture_avant_droite_quantite = models.IntegerField(default=0)

    peinture_arriere_gauche = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK,verbose_name=_("Peinture de l'aile arrière gauche"))
    peinture_arriere_gauche_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    peinture_arriere_gauche_quantite = models.IntegerField(default=0)

    peinture_face_avant = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Peinture de la face avant"))
    peinture_face_avant_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    peinture_face_avant_quantite = models.IntegerField(default=0)

    peinture_capot = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Peinture du capot"))
    peinture_capot_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    peinture_capot_quantite = models.IntegerField(default=0)

    peinture_arriere = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Peinture de l'arrière"))
    peinture_arriere_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
    peinture_arriere_quantite = models.IntegerField(default=0)

    peinture_complete = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Peinture complète"))
    peinture_complete_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix")
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
        verbose_name = _("Contrôle général")
        verbose_name_plural = _("Contrôles généraux")

    def __str__(self):
        # Si l'objet a une maintenance liée, on affiche son id
        if self.maintenance:
            return f"Check-up {self.maintenance.id}"
        # Sinon on affiche un texte par défaut
        return "Check-up (sans maintenance)"

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_intervention is not None:
            if self.kilometrage_intervention < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_checkup': _(
                        f"Le kilométrage du check-up ({self.kilometrage_intervention}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_intervention:
            if self.kilometrage_intervention > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_intervention
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        super().save(*args, **kwargs)





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


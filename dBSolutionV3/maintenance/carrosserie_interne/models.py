from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("Non")
    NOT_OK = "NOT_OK", _("Oui")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")



class CarrosserieInterne(models.Model):
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
    pare_choc_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Pare-chocs avant"))
    pare_choc_av_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Pare-chocs av oem"))
    pare_choc_av_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pare_choc_av_quantite = models.IntegerField(default=0)



    pare_choc_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Pare-chocs arrière"))
    pare_choc_ar_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Pare-chocs ar oem"))
    pare_choc_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pare_choc_ar_quantite = models.IntegerField(default=0)



        # Boucliers
    bouclier_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK, verbose_name=_("Bouclier avant"))
    bouclier_av_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Bouclier avant oem"))
    bouclier_av_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bouclier_av_quantite = models.IntegerField(default=0)



    bouclier_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Bouclier arrière"))
    bouclier_ar_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Bouclier arrière oem"))
    bouclier_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bouclier_ar_quantite = models.IntegerField(default=0)




    support_pare_choc_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Support de pare-chocs avant"))
    support_pare_choc_av_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Support de pare-chocs oem"))
    support_pare_choc_av_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    support_pare_choc_av_quantite = models.IntegerField(default=0)

    support_pare_choc_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Support de pare-chocs arrière"))
    support_pare_choc_ar_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Support de pare-chocs oem"))
    support_pare_choc_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    support_pare_choc_ar_quantite = models.IntegerField(default=0)

    # Calandre
    calandre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Calandre"))
    calandre_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Calandre oem"))
    calandre_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    calandre_quantite = models.IntegerField(default=0)






      # Ailes
    aile_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                    verbose_name=_("Aile avant droite"))
    aile_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Aile avant droite oem"))
    aile_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aile_avd_quantite = models.IntegerField(default=0)

    aile_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                verbose_name=_("Aile avant gauche"))
    aile_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Aile avant gauche oem"))
    aile_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aile_avg_quantite = models.IntegerField(default=0)

    aile_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                verbose_name=_("Aile arrière droite"))
    aile_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Aile arrière droite oem"))
    aile_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aile_ard_quantite = models.IntegerField(default=0)

    aile_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                verbose_name=_("Aile arrière gauche"))
    aile_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Aile arrière gauche oem"))
    aile_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aile_arg_quantite = models.IntegerField(default=0)





    # Élargisseurs d'aile
    elargisseur_aile_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Élargisseur d'aile avant droite"))
    elargisseur_aile_avd_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Élargisseur d'aile avant droite oem"))
    elargisseur_aile_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    elargisseur_aile_avd_quantite = models.IntegerField(default=0)


    elargisseur_aile_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Élargisseur d'aile avant gauche"))
    elargisseur_aile_avg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Élargisseur d'aile avant gauche oem"))
    elargisseur_aile_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    elargisseur_aile_avg_quantite = models.IntegerField(default=0)



    elargisseur_aile_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Élargisseur d'aile arrière droite"))
    elargisseur_aile_ard_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Élargisseur d'aile arrière droite oem"))
    elargisseur_aile_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    elargisseur_aile_ard_quantite = models.IntegerField(default=0)



    elargisseur_aile_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Élargisseur d'aile arrière gauche"))
    elargisseur_aile_arg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Élargisseur d'aile arrière gauche oem"))
    elargisseur_aile_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    elargisseur_aile_arg_quantite = models.IntegerField(default=0)





    # Bas de caisse
    bas_de_caisse_d = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Bas de caisse droit"))
    bas_de_caisse_d_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Bas de caisse droit oem"))
    bas_de_caisse_d_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bas_de_caisse_d_quantite = models.IntegerField(default=0)


    bas_de_caisse_g = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Bas de caisse gauche"))
    bas_de_caisse_g_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Bas de caisse gauche oem"))
    bas_de_caisse_g_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bas_de_caisse_g_quantite = models.IntegerField(default=0)






    # Supports
    support_radiateur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Support de radiateur"))
    support_radiateur_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Support de radiateur oem"))
    support_radiateur_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    support_radiateur_quantite = models.IntegerField(default=0)






        # Pare-brise
    pare_brise = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Pare-brise"))
    pare_brise_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Pare-brise oem"))
    pare_brise_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pare_brise_quantite = models.IntegerField(default=0)




        # Vitres de portes
    vitre_porte_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Vitre de porte avant droite"))
    vitre_porte_avd_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Vitre de porte avant droite oem"))
    vitre_porte_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vitre_porte_avd_quantite = models.IntegerField(default=0)


    vitre_porte_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Vitre de porte avant gauche"))
    vitre_porte_avg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Vitre de porte avant gauche oem"))
    vitre_porte_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vitre_porte_avg_quantite = models.IntegerField(default=0)


    vitre_porte_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Vitre de porte arrière droite"))
    vitre_porte_ard_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Vitre de porte arrière droite oem"))
    vitre_porte_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vitre_porte_ard_quantite = models.IntegerField(default=0)



    vitre_porte_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Vitre de porte arrière gauche"))
    vitre_porte_arg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Vitre de porte arrière gauche oem"))
    vitre_porte_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vitre_porte_arg_quantite = models.IntegerField(default=0)








        # Lunette arrière
    lunette = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Lunette / vitre arrière"))
    lunette_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Lunette vitre arrière oem"))
    lunette_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    lunette_quantite = models.IntegerField(default=0)




       # Rétroviseurs
    retroviseur_d = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Rétroviseur droit"))
    retroviseur_d_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Rétroviseur droit oem"))
    retroviseur_d_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    retroviseur_d_quantite = models.IntegerField(default=0)



    retroviseur_g = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                         verbose_name=_("Rétroviseur gauche"))
    retroviseur_g_oem = models.CharField(max_length=25, null=True, blank=True,
                                             verbose_name=_("Rétroviseur gauche oem"))
    retroviseur_g_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    retroviseur_g_quantite = models.IntegerField(default=0)







    # Portes
    porte_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Porte avant droite"))
    porte_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Porte avant droite oem"))
    porte_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    porte_avd_quantite = models.IntegerField(default=0)

    porte_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Porte avant gauche"))
    porte_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Porte avant gauche oem"))
    porte_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    porte_avg_quantite = models.IntegerField(default=0)

    porte_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Porte arrière droite"))
    porte_ard_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Porte arrière droite oem"))
    porte_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    porte_ard_quantite = models.IntegerField(default=0)

    porte_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Porte arrière gauche"))
    porte_arg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Porte arrière gauche oem"))
    porte_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    porte_arg_quantite = models.IntegerField(default=0)





    poignee_porte = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Poignée de porte"))
    poignee_porte_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Poignée de porte oem"))
    poignee_porte_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    poignee_porte_quantite = models.IntegerField(default=0)





    # Coffre / hayon
    coffre_haillon = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Coffre / Hayon"))
    coffre_haillon_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Coffre / Hayon oem"))
    coffre_haillon_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coffre_haillon_quantite = models.IntegerField(default=0)






        # Joint de coffre et portes
    joint_coffre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                        verbose_name=_("Joint de coffre"))
    joint_coffre_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Joint de coffre oem"))
    joint_coffre_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joint_coffre_quantite = models.IntegerField(default=0)

    joint_porte_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                           verbose_name=_("Joint de porte avant droite"))
    joint_porte_avd_oem = models.CharField(max_length=25, null=True, blank=True,
                                               verbose_name=_("Joint de porte avant droite oem"))
    joint_porte_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joint_porte_avd_quantite = models.IntegerField(default=0)

    # Joints de porte
    joint_porte_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                       verbose_name=_("Joint de porte avant gauche"))
    joint_porte_avg_oem = models.CharField(max_length=25, null=True, blank=True,
                                           verbose_name=_("Joint de porte avant gauche OEM"))
    joint_porte_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joint_porte_avg_quantite = models.IntegerField(default=0)

    joint_porte_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                       verbose_name=_("Joint de porte arrière droite"))
    joint_porte_ard_oem = models.CharField(max_length=25, null=True, blank=True,
                                           verbose_name=_("Joint de porte arrière droite OEM"))
    joint_porte_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joint_porte_ard_quantite = models.IntegerField(default=0)

    joint_porte_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                       verbose_name=_("Joint de porte arrière gauche"))
    joint_porte_arg_oem = models.CharField(max_length=25, null=True, blank=True,
                                           verbose_name=_("Joint de porte arrière gauche OEM"))
    joint_porte_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joint_porte_arg_quantite = models.IntegerField(default=0)






    # Coquilles d'aile
    coquille_aile_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                         verbose_name=_("Coquille d'aile avant droite"))
    coquille_aile_avd_oem = models.CharField(max_length=25, null=True, blank=True,
                                             verbose_name=_("Coquille d'aile avant droite OEM"))
    coquille_aile_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coquille_aile_avd_quantite = models.IntegerField(default=0)

    coquille_aile_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                         verbose_name=_("Coquille d'aile avant gauche"))
    coquille_aile_avg_oem = models.CharField(max_length=25, null=True, blank=True,
                                             verbose_name=_("Coquille d'aile avant gauche OEM"))
    coquille_aile_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coquille_aile_avg_quantite = models.IntegerField(default=0)

    coquille_aile_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                         verbose_name=_("Coquille d'aile arrière droite"))
    coquille_aile_ard_oem = models.CharField(max_length=25, null=True, blank=True,
                                             verbose_name=_("Coquille d'aile arrière droite OEM"))
    coquille_aile_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coquille_aile_ard_quantite = models.IntegerField(default=0)

    coquille_aile_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                         verbose_name=_("Coquille d'aile arrière gauche"))
    coquille_aile_arg_oem = models.CharField(max_length=25, null=True, blank=True,
                                             verbose_name=_("Coquille d'aile arrière gauche OEM"))
    coquille_aile_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coquille_aile_arg_quantite = models.IntegerField(default=0)






    # Clips et visserie
    clips = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                             verbose_name=_("Clips"))
    clips_oem = models.CharField(max_length=25, null=True, blank=True,
                                 verbose_name=_("Clips OEM"))
    clips_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clips_quantite = models.IntegerField(default=0)

    visserie = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                verbose_name=_("Visserie"))
    visserie_oem = models.CharField(max_length=25, null=True, blank=True,
                                    verbose_name=_("Visserie OEM"))
    visserie_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    visserie_quantite = models.IntegerField(default=0)






    # Capot
    capot = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                             verbose_name=_("Capot"))
    capot_oem = models.CharField(max_length=25, null=True, blank=True,
                                 verbose_name=_("Capot OEM"))
    capot_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capot_quantite = models.IntegerField(default=0)





    # Peinture
    peinture_avant_gauche = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                             verbose_name=_("Peinture avant gauche"))
    peinture_avant_gauche_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_avant_gauche_quantite = models.IntegerField(default=0)

    peinture_avant_droite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                             verbose_name=_("Peinture avant droite"))
    peinture_avant_droite_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_avant_droite_quantite = models.IntegerField(default=0)

    peinture_arriere_gauche = models.CharField(max_length=25, choices=EtatOKNotOK.choices,
                                               default=EtatOKNotOK.NOT_OK,
                                               verbose_name=_("Peinture arrière gauche"))
    peinture_arriere_gauche_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_arriere_gauche_quantite = models.IntegerField(default=0)

    peinture_face_avant = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                           verbose_name=_("Peinture face avant"))
    peinture_face_avant_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_face_avant_quantite = models.IntegerField(default=0)

    peinture_capot = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                      verbose_name=_("Peinture capot"))
    peinture_capot_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_capot_quantite = models.IntegerField(default=0)

    peinture_arriere = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                        verbose_name=_("Peinture arrière"))
    peinture_arriere_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_arriere_quantite = models.IntegerField(default=0)

    peinture_complete = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                         verbose_name=_("Peinture complète"))
    peinture_complete_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    peinture_complete_quantite = models.IntegerField(default=0)






    # Phares
    phare_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                 verbose_name=_("Phare avant droit"))
    phare_avd_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Phare avant droit OEM"))
    phare_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    phare_avd_quantite = models.IntegerField(default=0)

    phare_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                 verbose_name=_("Phare avant gauche"))
    phare_avg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Phare avant gauche OEM"))
    phare_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    phare_avg_quantite = models.IntegerField(default=0)

    phare_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                 verbose_name=_("Feu arrière droit"))
    phare_ard_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Feu arrière droit OEM"))
    phare_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    phare_ard_quantite = models.IntegerField(default=0)

    phare_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                 verbose_name=_("Feu arrière gauche"))
    phare_arg_oem = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("Feu arrière gauche OEM"))
    phare_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    phare_arg_quantite = models.IntegerField(default=0)





    # Clignotants
    clignotant_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                      verbose_name=_("Clignotant avant droit"))
    clignotant_avd_oem = models.CharField(max_length=25, null=True, blank=True,
                                          verbose_name=_("Clignotant avant droit OEM"))
    clignotant_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clignotant_avd_quantite = models.IntegerField(default=0)

    clignotant_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                      verbose_name=_("Clignotant avant gauche"))
    clignotant_avg_oem = models.CharField(max_length=25, null=True, blank=True,
                                          verbose_name=_("Clignotant avant gauche OEM"))
    clignotant_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clignotant_avg_quantite = models.IntegerField(default=0)

    clignotant_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                      verbose_name=_("Clignotant arrière droit"))
    clignotant_ard_oem = models.CharField(max_length=25, null=True, blank=True,
                                          verbose_name=_("Clignotant arrière droit OEM"))
    clignotant_ard_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clignotant_ard_quantite = models.IntegerField(default=0)

    clignotant_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
                                      verbose_name=_("Clignotant arrière gauche"))
    clignotant_arg_oem = models.CharField(max_length=25, null=True, blank=True,
                                          verbose_name=_("Clignotant arrière gauche OEM"))
    clignotant_arg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clignotant_arg_quantite = models.IntegerField(default=0)





    troisieme_feu_stop = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
        verbose_name=_("Troisième feu stop")
    )
    troisieme_feu_stop_oem = models.CharField(
        max_length=25, null=True, blank=True,
        verbose_name=_("Troisième feu stop OEM")
    )
    troisieme_feu_stop_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    troisieme_feu_stop_quantite = models.IntegerField(default=0)





    # Capteur de recul
    capteur_recul = models.CharField(
        max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,
        verbose_name=_("Capteur de recul")
    )
    capteur_recul_oem = models.CharField(
        max_length=25, null=True, blank=True,
        verbose_name=_("Capteur de recul OEM")
    )
    capteur_recul_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capteur_recul_quantite = models.IntegerField(default=0)





    # Anti-brouillards avant droit
    anti_brouillard_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Anti-brouillard avant droit"))
    anti_brouillard_avd_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Anti-brouillard avant droit OEM"))
    anti_brouillard_avd_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    anti_brouillard_avd_quantite = models.IntegerField(default=0)

    # Anti-brouillards avant gauche
    anti_brouillard_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Anti-brouillard avant gauche"))
    anti_brouillard_avg_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Anti-brouillard avant gauche OEM"))
    anti_brouillard_avg_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    anti_brouillard_avg_quantite = models.IntegerField(default=0)

    # Anti-brouillards arrière
    anti_brouillard_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK,verbose_name=_("Anti-brouillard arrière"))
    anti_brouillard_ar_oem = models.CharField(max_length=25, null=True, blank=True,verbose_name=_("Anti-brouillard arrière OEM"))
    anti_brouillard_ar_prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    anti_brouillard_ar_quantite = models.IntegerField(default=0)



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


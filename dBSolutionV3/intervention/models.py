from django.db import models
from django.utils.translation import gettext_lazy as _



class Intervention(models.Model):
    id = models.AutoField(primary_key=True)

    carrosserie = models.ForeignKey(
        "carrosserie.Carrosserie",
        verbose_name=_("Carrosserie"),
        on_delete=models.CASCADE,
        related_name="interventions",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.PROTECT,
        verbose_name="Voiture",
        related_name="interventions",
        null=True,
        blank=True
    )

    pare_chocs = models.BooleanField(_("Pare-chocs"), default=False)
    pare_chocs_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    pare_chocs_quantite = models.PositiveIntegerField(null=True, blank=True)

    bouclier_av = models.BooleanField(_("Bouclier avant"), default=False)
    bouclier_av_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    bouclier_av_quantite = models.PositiveIntegerField(null=True, blank=True)

    bouclier_ar = models.BooleanField(_("Bouclier arrière"), default=False)
    bouclier_ar_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    bouclier_ar_quantite = models.PositiveIntegerField(null=True, blank=True)

    pare_brise = models.BooleanField(_("Pare-brise"), default=False)
    pare_brise_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    pare_brise_quantite = models.PositiveIntegerField(null=True, blank=True)

    vitre_porte_avd = models.BooleanField(_("Vitre de porte avant droit"), default=False)
    vitre_porte_avd_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    vitre_porte_avd_quantite = models.PositiveIntegerField(null=True, blank=True)

    vitre_porte_avg = models.BooleanField(_("Vitre de porte avant gauche"), default=False)
    vitre_porte_avg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    vitre_porte_avg_quantite = models.PositiveIntegerField(null=True, blank=True)

    vitre_porte_ard = models.BooleanField(_("Vitre de porte arrière droit"), default=False)
    vitre_porte_ard_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    vitre_porte_ard_quantite = models.PositiveIntegerField(null=True, blank=True)

    vitre_porte_arg = models.BooleanField(_("Vitre de porte arrière gauche"), default=False)
    vitre_porte_arg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    vitre_porte_arg_quantite = models.PositiveIntegerField(null=True, blank=True)

    lunette = models.BooleanField(_("Lunette"), default=False)
    lunette_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    lunette_quantite = models.PositiveIntegerField(null=True, blank=True)

    retroviseur_d = models.BooleanField(_("Rétroviseur droit"), default=False)
    retroviseur_d_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    retroviseur_d_quantite = models.PositiveIntegerField(null=True, blank=True)

    retroviseur_g = models.BooleanField(_("Rétroviseur gauche"), default=False)
    retroviseur_g_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    retroviseur_g_quantite = models.PositiveIntegerField(null=True, blank=True)

    aile_avd = models.BooleanField(_("Aile avant droit"), default=False)
    aile_avd_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    aile_avd_quantite = models.PositiveIntegerField(null=True, blank=True)

    aile_avg = models.BooleanField(_("Aile avant gauche"), default=False)
    aile_avg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    aile_avg_quantite = models.PositiveIntegerField(null=True, blank=True)

    aile_ard = models.BooleanField(_("Aile arrière droit"), default=False)
    aile_ard_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    aile_ard_quantite = models.PositiveIntegerField(null=True, blank=True)

    aile_arg = models.BooleanField(_("Aile arrière gauche"), default=False)
    aile_arg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    aile_arg_quantite = models.PositiveIntegerField(null=True, blank=True)

    elargisseur_aile_avd = models.BooleanField(_("Élargisseur d’aile avant droit"), default=False)
    elargisseur_aile_avd_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    elargisseur_aile_avd_quantite = models.PositiveIntegerField(null=True, blank=True)

    elargisseur_aile_avg = models.BooleanField(_("Élargisseur d’aile avant gauche"), default=False)
    elargisseur_aile_avg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    elargisseur_aile_avg_quantite = models.PositiveIntegerField(null=True, blank=True)

    elargisseur_aile_ard = models.BooleanField(_("Élargisseur d’aile arrière droit"), default=False)
    elargisseur_aile_ard_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    elargisseur_aile_ard_quantite = models.PositiveIntegerField(null=True, blank=True)

    elargisseur_aile_arg = models.BooleanField(_("Élargisseur d’aile arrière gauche"), default=False)
    elargisseur_aile_arg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    elargisseur_aile_arg_quantite = models.PositiveIntegerField(null=True, blank=True)

    bas_de_caisse_d = models.BooleanField(_("Bas de caisse droit"), default=False)
    bas_de_caisse_d_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    bas_de_caisse_d_quantite = models.PositiveIntegerField(null=True, blank=True)

    bas_de_caisse_g = models.BooleanField(_("Bas de caisse gauche"), default=False)
    bas_de_caisse_g_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    bas_de_caisse_g_quantite = models.PositiveIntegerField(null=True, blank=True)

    support_radiateur = models.BooleanField(_("Support de radiateur"), default=False)
    support_radiateur_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    support_radiateur_quantite = models.PositiveIntegerField(null=True, blank=True)

    support_pare_choc = models.BooleanField(_("Support de pare-chocs"), default=False)
    support_pare_choc_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    support_pare_choc_quantite = models.PositiveIntegerField(null=True, blank=True)

    calandre = models.BooleanField(_("Calandre"), default=False)
    calandre_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    calandre_quantite = models.PositiveIntegerField(null=True, blank=True)

    porte_avd = models.BooleanField(_("Porte avant droite"), default=False)
    porte_avd_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    porte_avd_quantite = models.PositiveIntegerField(null=True, blank=True)

    porte_avg = models.BooleanField(_("Porte avant gauche"), default=False)
    porte_avg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    porte_avg_quantite = models.PositiveIntegerField(null=True, blank=True)

    porte_ard = models.BooleanField(_("Porte arrière droite"), default=False)
    porte_ard_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    porte_ard_quantite = models.PositiveIntegerField(null=True, blank=True)

    porte_arg = models.BooleanField(_("Porte arrière gauche"), default=False)
    porte_arg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    porte_arg_quantite = models.PositiveIntegerField(null=True, blank=True)

    poignee_porte = models.BooleanField(_("Poignée de porte"), default=False)
    poignee_porte_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    poignee_porte_quantite = models.PositiveIntegerField(null=True, blank=True)

    coffre_haillon = models.BooleanField(_("Coffre / hayon"), default=False)
    coffre_haillon_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    coffre_haillon_quantite = models.PositiveIntegerField(null=True, blank=True)

    joint_coffre = models.BooleanField(_("Joint de coffre"), default=False)
    joint_coffre_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    joint_coffre_quantite = models.PositiveIntegerField(null=True, blank=True)

    joint_porte_avd = models.BooleanField(_("Joint de porte avant droit"), default=False)
    joint_porte_avd_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    joint_porte_avd_quantite = models.PositiveIntegerField(null=True, blank=True)

    joint_porte_avg = models.BooleanField(_("Joint de porte avant gauche"), default=False)
    joint_porte_avg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    joint_porte_avg_quantite = models.PositiveIntegerField(null=True, blank=True)

    joint_porte_ard = models.BooleanField(_("Joint de porte arrière droit"), default=False)
    joint_porte_ard_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    joint_porte_ard_quantite = models.PositiveIntegerField(null=True, blank=True)

    joint_porte_arg = models.BooleanField(_("Joint de porte arrière gauche"), default=False)
    joint_porte_arg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    joint_porte_arg_quantite = models.PositiveIntegerField(null=True, blank=True)

    coquille_aile_avd = models.BooleanField(_("Coquille d’aile avant droit"), default=False)
    coquille_aile_avd_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    coquille_aile_avd_quantite = models.PositiveIntegerField(null=True, blank=True)

    coquille_aile_avg = models.BooleanField(_("Coquille d’aile avant gauche"), default=False)
    coquille_aile_avg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    coquille_aile_avg_quantite = models.PositiveIntegerField(null=True, blank=True)

    coquille_aile_ard = models.BooleanField(_("Coquille d’aile arrière droit"), default=False)
    coquille_aile_ard_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    coquille_aile_ard_quantite = models.PositiveIntegerField(null=True, blank=True)

    coquille_aile_arg = models.BooleanField(_("Coquille d’aile arrière gauche"), default=False)
    coquille_aile_arg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    coquille_aile_arg_quantite = models.PositiveIntegerField(null=True, blank=True)

    clips = models.BooleanField(_("Clips"), default=False)
    clips_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    clips_quantite = models.PositiveIntegerField(null=True, blank=True)

    visserie = models.BooleanField(_("Visserie"), default=False)
    visserie_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    visserie_quantite = models.PositiveIntegerField(null=True, blank=True)

    capot = models.BooleanField(_("Capot"), default=False)
    capot_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    capot_quantite = models.PositiveIntegerField(null=True, blank=True)

    peinture_avant_gauche = models.BooleanField(_("Peinture avant gauche"), default=False)
    peinture_avant_gauche_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    peinture_avant_gauche_quantite = models.PositiveIntegerField(null=True, blank=True)

    peinture_avant_droite = models.BooleanField(_("Peinture avant droite"), default=False)
    peinture_avant_droite_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    peinture_avant_droite_quantite = models.PositiveIntegerField(null=True, blank=True)

    peinture_arriere_gauche = models.BooleanField(_("Peinture arriere gauche"), default=False)
    peinture_arriere_gauche_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    peinture_arriere_gauche_quantite = models.PositiveIntegerField(null=True, blank=True)

    peinture_face_avant = models.BooleanField(_("Peinture face avant"), default=False)
    peinture_face_avant_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    peinture_face_avant_quantite = models.PositiveIntegerField(null=True, blank=True)

    peinture_capot = models.BooleanField(_("Peinture capot"), default=False)
    peinture_capot_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    peinture_capot_quantite = models.PositiveIntegerField(null=True, blank=True)

    peinture_arriere = models.BooleanField(_("Peinture arriere"), default=False)
    peinture_arriere_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    peinture_arriere_quantite = models.PositiveIntegerField(null=True, blank=True)

    peinture_complete = models.BooleanField(_("Peinture complete"), default=False)
    peinture_complete_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    peinture_complete_quantite = models.PositiveIntegerField(null=True, blank=True)

    phare_avd = models.BooleanField(_("Phare avant droit"), default=False)
    phare_avd_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    phare_avd_quantite = models.PositiveIntegerField(null=True, blank=True)

    phare_avg = models.BooleanField(_("Phare avant gauche"), default=False)
    phare_avg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    phare_avg_quantite = models.PositiveIntegerField(null=True, blank=True)

    phare_ard = models.BooleanField(_("Phare arrière droite"), default=False)
    phare_ard_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    phare_ard_quantite = models.PositiveIntegerField(null=True, blank=True)

    phare_arg = models.BooleanField(_("Phare arrière gauche"), default=False)
    phare_arg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    phare_arg_quantite = models.PositiveIntegerField(null=True, blank=True)

    clignotant_avd = models.BooleanField(_("Clignotant avant droit"), default=False)
    clignotant_avd_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    clignotant_avd_quantite = models.PositiveIntegerField(null=True, blank=True)

    clignotant_avg = models.BooleanField(_("Clignotant avant gauche"), default=False)
    clignotant_avg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    clignotant_avg_quantite = models.PositiveIntegerField(null=True, blank=True)

    clignotant_ard = models.BooleanField(_("Clignotant arrière droit"), default=False)
    clignotant_ard_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    clignotant_ard_quantite = models.PositiveIntegerField(null=True, blank=True)

    anti_brouillard_avd = models.BooleanField(_("Anti Brouillard avant droit"), default=False)
    anti_brouillard_avd_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    anti_brouillard_avd_quantite = models.PositiveIntegerField(null=True, blank=True)

    anti_brouillard_avg = models.BooleanField(_("Anti Brouillard avant gauche"), default=False)
    anti_brouillard_avg_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    anti_brouillard_avg_quantite = models.PositiveIntegerField(null=True, blank=True)

    troisieme_feux_stop = models.BooleanField(_("Troisième feux stop"), default=False)
    troisieme_feux_stop_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    troisieme_feux_stop_quantite = models.PositiveIntegerField(null=True, blank=True)

    capteur_recul = models.BooleanField(_("Capteur recul"), default=False)
    capteur_recul_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    capteur_recul_quantite = models.PositiveIntegerField(null=True, blank=True)





    montant_devis = models.DecimalField(
        _("Montant du devis"),
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    montant_facture = models.DecimalField(
        _("Montant de la facture"),
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    montant_total = models.DecimalField(
        _("Montant total"),
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Intervention")
        verbose_name_plural = _("Interventions")

    def __str__(self):
        if self.carrosserie:
            return _("Intervention %(id)s – %(carrosserie)s") % {
                "id": self.id,
                "carrosserie": self.carrosserie.nom_societe,
            }
        return _("Intervention %(id)s") % {"id": self.id}

    def clean(self):
        for field in self._meta.fields:

            if field.name.endswith("_prix"):
                base = field.name.replace("_prix", "")

                if not getattr(self, base):
                    setattr(self, field.name, None)
                    setattr(self, f"{base}_quantite", None)

    @property
    def total_prix(self):
        total = 0

        for field in self._meta.fields:

            if field.name.endswith("_prix"):
                base = field.name.replace("_prix", "")

                if getattr(self, base):
                    prix = getattr(self, field.name) or 0
                    qty = getattr(self, f"{base}_quantite") or 0

                    total += prix * qty

        return total

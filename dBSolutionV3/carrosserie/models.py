import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Carrosserie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nom_societe = models.CharField(_("Nom de la société"), max_length=100)
    responsable_nom = models.CharField(_("Responsable nom"), null=True, blank=True, max_length=100)
    responsable_prenom = models.CharField(_("Responsable prenom"),null=True,blank=True, max_length=100)
    adresse = models.CharField(_("Adresse"), max_length=255, blank=True, null=True)
    pays = models.CharField(_("Pays"), max_length=50, blank=True, null=True)
    telephone = models.CharField(_("Téléphone"), max_length=20, blank=True, null=True)
    email = models.EmailField(_("Email"), blank=True, null=True)
    numero_tva = models.CharField(_("Numéro de TVA"), max_length=50, blank=True, null=True)
    peppol_id = models.CharField(
        _("Identifiant Peppol"),
        max_length=50,
        help_text=_("Identifiant Peppol, ex : 0208:BE0123456789"),
        null=True,
        blank=True,
    )




    class Meta:
        verbose_name = _("Carrosserie")
        verbose_name_plural = _("Carrosseries")

    def __str__(self):
        return self.nom_societe

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

    pare_chocs = models.BooleanField(_("Pare-chocs"), default=False)
    pare_chocs_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    pare_chocs_quantite = models.PositiveIntegerField(null=True, blank=True)

    bouclier = models.BooleanField(_("Bouclier"), default=False)
    bouclier_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    bouclier_quantite = models.PositiveIntegerField(null=True, blank=True)

    pare_brise = models.BooleanField(_("Pare-brise"), default=False)
    pare_brise_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    pare_brise_quantite = models.PositiveIntegerField(null=True, blank=True)

    vitre_porte = models.BooleanField(_("Vitre de porte"), default=False)
    vitre_porte_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    vitre_porte_quantite = models.PositiveIntegerField(null=True, blank=True)

    lunette = models.BooleanField(_("Lunette"), default=False)
    lunette_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    lunette_quantite = models.PositiveIntegerField(null=True, blank=True)

    retroviseur = models.BooleanField(_("Rétroviseur"), default=False)
    retroviseur_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    retroviseur_quantite = models.PositiveIntegerField(null=True, blank=True)

    aile = models.BooleanField(_("Aile"), default=False)
    aile_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    aile_quantite = models.PositiveIntegerField(null=True, blank=True)

    elargisseur_aile = models.BooleanField(_("Élargisseur d’aile"), default=False)
    elargisseur_aile_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    elargisseur_aile_quantite = models.PositiveIntegerField(null=True, blank=True)

    bas_de_caisse = models.BooleanField(_("Bas de caisse"), default=False)
    bas_de_caisse_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    bas_de_caisse_quantite = models.PositiveIntegerField(null=True, blank=True)

    support_radiateur = models.BooleanField(_("Support de radiateur"), default=False)
    support_radiateur_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    support_radiateur_quantite = models.PositiveIntegerField(null=True, blank=True)

    support_pare_choc = models.BooleanField(_("Support de pare-chocs"), default=False)
    support_pare_choc_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    support_pare_choc_quantite = models.PositiveIntegerField(null=True, blank=True)

    porte = models.BooleanField(_("Porte"), default=False)
    porte_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    porte_quantite = models.PositiveIntegerField(null=True, blank=True)

    poignee_porte = models.BooleanField(_("Poignée de porte"), default=False)
    poignee_porte_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    poignee_porte_quantite = models.PositiveIntegerField(null=True, blank=True)

    coffre_haillon = models.BooleanField(_("Coffre / hayon"), default=False)
    coffre_haillon_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    coffre_haillon_quantite = models.PositiveIntegerField(null=True, blank=True)

    joint_coffre = models.BooleanField(_("Joint de coffre"), default=False)
    joint_coffre_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    joint_coffre_quantite = models.PositiveIntegerField(null=True, blank=True)

    joint_porte = models.BooleanField(_("Joint de porte"), default=False)
    joint_porte_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    joint_porte_quantite = models.PositiveIntegerField(null=True, blank=True)

    coquille_aile = models.BooleanField(_("Coquille d’aile"), default=False)
    coquille_aile_prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    coquille_aile_quantite = models.PositiveIntegerField(null=True, blank=True)

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




    montant_devis = models.DecimalField(
        _("Montant du devis"),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    montant_facture = models.DecimalField(
        _("Montant de la facture"),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    montant_total = models.DecimalField(
        _("Montant total"),
        max_digits=10,
        decimal_places=2,
        default=0
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

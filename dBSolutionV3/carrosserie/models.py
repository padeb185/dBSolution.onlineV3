import uuid

from django.db import models

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
    bouclier = models.BooleanField(_("Bouclier"), default=False)
    pare_brise = models.BooleanField(_("Pare-brise"), default=False)
    vitre_porte = models.BooleanField(_("Vitre de porte"), default=False)
    lunette = models.BooleanField(_("Lunette"), default=False)
    retroviseur = models.BooleanField(_("Rétroviseur"), default=False)
    aile = models.BooleanField(_("Aile"), default=False)
    elargisseur_aile = models.BooleanField(_("Élargisseur d’aile"), default=False)
    bas_de_caisse = models.BooleanField(_("Bas de caisse"), default=False)
    support_radiateur = models.BooleanField(_("Support de radiateur"), default=False)
    support_pare_choc = models.BooleanField(_("Support de pare-chocs"), default=False)
    porte = models.BooleanField(_("Porte"), default=False)
    poignee_porte = models.BooleanField(_("Poignée de porte"), default=False)
    coffre_haillon = models.BooleanField(_("Coffre / hayon"), default=False)
    joint_coffre = models.BooleanField(_("Joint de coffre"), default=False)
    joint_porte = models.BooleanField(_("Joint de porte"), default=False)
    coquille_aile = models.BooleanField(_("Coquille d’aile"), default=False)
    clips = models.BooleanField(_("Clips"), default=False)
    visserie = models.BooleanField(_("Visserie"), default=False)
    capot = models.BooleanField(_("Capot"), default=False)

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

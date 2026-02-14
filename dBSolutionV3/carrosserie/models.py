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

    numero_iban = models.CharField(max_length=36, blank=True, null=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Carrosserie")
        verbose_name_plural = _("Carrosseries")

    def __str__(self):
        return self.nom_societe


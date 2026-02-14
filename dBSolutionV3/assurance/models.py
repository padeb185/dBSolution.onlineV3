import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class Assurance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nom_compagnie= models.CharField(_("Nom de la compagnie"), max_length=100, blank=True, null=True)
    courtier_nom = models.CharField(_("Nom du courtier"), null=True, blank=True, max_length=100)
    courtier_prenom = models.CharField(_("Prénom du courtier"),null=True,blank=True, max_length=100)

    telephone = models.CharField(_("Téléphone"), max_length=20, blank=True, null=True)
    email = models.EmailField(_("Email"), max_length=255 ,blank=True, null=True)
    peppol_id = models.CharField(
        _("Identifiant Peppol"),
        max_length=50,
        help_text=_("Identifiant Peppol, ex : 0208:BE0123456789"),
        null=True,
        blank=True,
    )
    numero_iban = models.CharField(max_length=36, blank=True, null=True)

    adresse = models.ForeignKey(
        "adresse.Adresse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assurances"
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Assurance")
        verbose_name_plural = _("Assurances")

    def __str__(self):
        return self.nom_compagnie


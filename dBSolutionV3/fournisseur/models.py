import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from adresse.models import Adresse


class Fournisseur(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nom = models.CharField(
        _("Nom du fournisseur"),
        max_length=200,
        unique=True
    )

    adresse = models.OneToOneField(
        Adresse,
        verbose_name=_("Adresse"),
        on_delete=models.CASCADE
    )

    numero_tva = models.CharField(
        _("Numéro de TVA"),
        max_length=20,
        unique=True
    )

    taux_tva = models.DecimalField(
        _("Taux de TVA (%)"),
        max_digits=5,
        decimal_places=2,
        default=21.00
    )

    peppol_id = models.CharField(
        _("Identifiant Peppol"),
        max_length=50,
        help_text=_("Identifiant Peppol, ex : 0208:BE0123456789")
    )

    country_code = models.CharField(
        _("Code pays"),
        max_length=2,
        default="BE",
        help_text=_("ISO 3166-1 alpha-2")
    )

    # --- Métadonnées ---
    is_active = models.BooleanField(_("Actif"), default=True)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)

    class Meta:
        verbose_name = _("Fournisseur")
        verbose_name_plural = _("Fournisseurs")
        indexes = [
            models.Index(fields=["numero_tva"]),
            models.Index(fields=["peppol_id"]),
        ]

    def __str__(self):
        return _("%(nom)s (Fournisseur)") % {"nom": self.nom}

    # --- Helpers Peppol ---
    @property
    def peppol_scheme(self):
        return self.peppol_id.split(":")[0]

    @property
    def peppol_value(self):
        return self.peppol_id.split(":")[1]

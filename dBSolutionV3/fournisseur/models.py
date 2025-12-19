import uuid
from django.db import models
from adresse.models import Adresse


class Fournisseur(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nom = models.CharField(max_length=200, unique=True, verbose_name="Nom du fournisseur")
    adresse = models.OneToOneField(Adresse, on_delete=models.CASCADE)

    numero_tva = models.CharField(max_length=20, unique=True, verbose_name="Numéro de TVA")
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=21.00, verbose_name="Taux de TVA (%)")


    peppol_id = models.CharField(
        max_length=50,
        help_text="Identifiant Peppol, ex: 0208:BE0123456789"
    )
    country_code = models.CharField(
        max_length=2,
        default="BE",
        help_text="ISO 3166-1 alpha-2"
    )

    # --- Métadonnées ---
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        indexes = [
            models.Index(fields=["numero_tva"]),
            models.Index(fields=["peppol_id"]),
        ]

    def __str__(self):
        return f"{self.nom} (Fournisseur)"

    # --- Helpers Peppol ---
    @property
    def peppol_scheme(self):
        return self.peppol_id.split(":")[0]

    @property
    def peppol_value(self):
        return self.peppol_id.split(":")[1]



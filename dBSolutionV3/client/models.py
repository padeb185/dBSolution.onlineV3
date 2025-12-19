from django.db import models


class Client(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.ForeignKey(
        'adresse.Adresse',
        on_delete=models.PROTECT,
        related_name='client'
    )
    numero_tva = models.CharField(
        max_length=20,
        help_text="Numéro TVA du client, ex: BE0987654321"
    )
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=21.00, verbose_name="Taux de TVA (%)")

    peppol_id = models.CharField(
        max_length=50,
        help_text="Identifiant Peppol du client, ex: 0208:BE0987654321"
    )
    code_pays = models.CharField(
        max_length=2,
        default="BE"
    )

    # --- Métadonnées ---
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        indexes = [
            models.Index(fields=["numero_tva"]),
            models.Index(fields=["peppol_id"]),
        ]

    def __str__(self):
        return f"{self.nom} (Client)"

    # --- Helpers Peppol ---
    @property
    def peppol_scheme(self):
        return self.peppol_id.split(":")[0]

    @property
    def peppol_value(self):
        return self.peppol_id.split(":")[1]

from django.db import models
import uuid



class SocieteCliente(models.Model):
    id_societe_cliente = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    adresse = models.ForeignKey(
        'adresse.Adresse',
        on_delete=models.CASCADE,
        related_name='societe_cliente',
        verbose_name='Adresse',
        null=True,
        blank=True
    )

    nom_societe_cliente = models.CharField(
        max_length=100,
        verbose_name='Nom Societe',
        null=True,
        blank=True
    )

    directeur_nom_prenom = models.CharField(
        max_length=100,
        verbose_name="Nom Prémon Directeur",
        null=True,
        blank=True
    )
    numero_tva = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Numéro de TVA",
        null=True,
        blank=True
    )
    site_internet = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Site web"
    )

    peppol_id = models.CharField(
        max_length=50,
        help_text="Identifiant Peppol du client, ex: 0208:BE0987654321",
        null=True,
        blank=True

    )
    pays = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    code_pays = models.CharField(
        max_length=2,
        default="BE"
    )
    numero_entreprise = models.CharField(max_length=255, blank=True, null=True)

    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=21.00, verbose_name="Taux de TVA (%)")


    class Meta:
        verbose_name = "Société cliente"
        verbose_name_plural = "Sociétés clientes"
        ordering = ['nom_societe_cliente']



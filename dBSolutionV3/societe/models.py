from django.db import models
import uuid
from django.utils.text import slugify
from django_tenants.models import TenantMixin, DomainMixin
from django.utils.translation import gettext_lazy as _

from maintenance.choices import TVAConfig


class Societe(TenantMixin):
    schema_name = models.CharField(max_length=63, unique=True)

    adresse = models.ForeignKey(
        'adresse.Adresse',
        on_delete=models.CASCADE,
        related_name='société',
        verbose_name='Adresse',
        null=True,
        blank=True
    )

    slug = models.SlugField(unique=True)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    auto_create_schema = True

    id_societe = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    nom = models.CharField(max_length=100, unique=True)
    directeur = models.CharField(max_length=100)

    numero_tel = models.CharField(
        max_length=30,
        verbose_name=_("Numéro de téléphone"),
        null=True,
        blank=True,
    )

    numero_tva = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Numéro de TVA"),
    )

    iban = models.CharField(
        max_length=34,
        blank=True,
        verbose_name=_("IBAN"),
    )

    max_utilisateurs = models.PositiveIntegerField(
        default=3,
        verbose_name=_("Nombre maximum d'utilisateurs")
    )

    site = models.URLField(max_length=200, blank=True, null=True)

    # Pays d'établissement : pilote la TVA (taux, déclaration), les factures / Peppol,
    # les plafonds de paiement en espèces, les ventes et la comptabilité.
    pays = models.CharField(
        _("Pays"),
        max_length=2,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        help_text=_("Pays d'établissement de la société (TVA, factures, comptabilité)."),
    )

    # Modules activés (societe/modules.py) : vide (null) = tous les modules
    modules = models.JSONField(
        _("Modules activés"),
        null=True,
        blank=True,
        help_text=_("Vide : tous les modules. Sinon, liste des modules activés pour ce tenant."),
    )

    class Meta:
        verbose_name = "Société"
        verbose_name_plural = "Sociétés"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)

        if not self.schema_name:
            self.schema_name = slugify(self.nom).replace("-", "_")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    # ------------------------------------------------------------
    # Modules
    # ------------------------------------------------------------
    def module_actif(self, code):
        return self.modules is None or code in self.modules

    @property
    def modules_actifs(self):
        from .modules import ModulesActifs
        return ModulesActifs(self)

    # ------------------------------------------------------------
    # Pays
    # ------------------------------------------------------------
    @property
    def code_pays(self):
        from core.pays import pays_societe
        return pays_societe(self)

    @property
    def profil_pays(self):
        from core.pays import profil_pays
        return profil_pays(self.code_pays)

    @property
    def taux_tva_normal(self):
        from core.pays import taux_tva_normal
        return taux_tva_normal(self.code_pays)


class Domain(DomainMixin):
    pass
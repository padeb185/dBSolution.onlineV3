from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from decimal import Decimal
from carrosserie.models import validate_iban


class Proprietaire(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)


    adresse = models.ForeignKey(
        "adresse.Adresse",
        on_delete=models.CASCADE,
        related_name="proprietaires",
        null=True,
        blank=True,
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="proprietaires"
    )

    numero_telephone = models.CharField(
        _("Numéro de téléphone"),
        max_length=20,
        null=True,
        blank=True
    )

    numero_permis = models.CharField(
        _("Numéro de permis de conduire"),
        max_length=50,
        null=True,
        blank=True
    )

    numero_carte_id = models.CharField(
        _("Numéro de carte d'identité"),
        max_length=20,
        null=True,
        blank=True
    )

    numero_compte = models.CharField(
        _("Numéro de compte bancaire"),
        max_length=34,
        null=True,
        blank=True,
        validators=[validate_iban]
    )
    numero_carte_bancaire = models.CharField(
        _("Numéro de carte bancaire"),
        max_length=20,
        null=True,
        blank=True
    )

    email = models.EmailField(
        _("Email"),
        max_length=100,
        null=True,
        blank=True
    )

    date_naissance = models.DateField(
        _("Date de naissance"),
        null=True,
        blank=True
    )

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"





class TypeProprietaire(models.TextChoices):
    TENANT = "TENANT", _("Notre société")
    PROPRIETAIRE = "PROPRIETAIRE", _("Propriétaire (personne)")
    SOCIETE_CLIENTE = "SOCIETE_CLIENTE", _("Société partenaire")


CENT = Decimal("100")


class ProprietaireVoiture(models.Model):
    """
    Part de propriété d'un véhicule. Le titulaire est :
      - notre société (le tenant) : sa quote-part est facturée en interne, au coût (sans marge, TVA récupérée) ;
      - un propriétaire (personne) ou une société partenaire : facture avec TVA et marges, à hauteur de sa part.
    Le total des parts d'un véhicule ne dépasse jamais 100 % (100 % exigé pour facturer).
    """
    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="proprietaires_voiture"
    )

    type_proprietaire = models.CharField(
        _("Type de propriétaire"),
        max_length=20,
        choices=TypeProprietaire.choices,
        default=TypeProprietaire.PROPRIETAIRE,
    )

    proprietaire = models.ForeignKey(
        "proprietaire.Proprietaire",
        on_delete=models.CASCADE,
        related_name="proprietaire_voitures",
        null=True,
        blank=True,
        verbose_name=_("Propriétaire"),
    )

    societe_cliente = models.ForeignKey(
        "societe_cliente.SocieteCliente",
        on_delete=models.PROTECT,
        related_name="parts_vehicules",
        null=True,
        blank=True,
        verbose_name=_("Société partenaire"),
    )

    part_proprietaire_pourcent = models.DecimalField(
        _("Part (%)"),
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01")), MaxValueValidator(100)]
    )

    # Marges appliquées sur les factures de ce propriétaire (ignorées pour notre société : coût sans marge)
    marge_pieces = models.DecimalField(
        _("Marge pièces (%)"),
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(0)],
    )
    marge_main_oeuvre = models.DecimalField(
        _("Marge main-d'œuvre (%)"),
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(0)],
    )

    # Locations : commission retenue par notre société sur la part de ce propriétaire
    commission_location = models.DecimalField(
        _("Commission location (%)"),
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("Retenue sur la part du propriétaire dans le prix des locations (frais de gestion)."),
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="proprietaires_voiture",
        null=True,
        blank=True,
    )

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Part de propriété")
        verbose_name_plural = _("Parts de propriété")
        ordering = ["voiture_exemplaire_id", "-part_proprietaire_pourcent"]

    def __str__(self):
        return f"{self.nom_proprietaire} ({self.part_proprietaire_pourcent} %)"

    # -------------------------
    # Titulaire
    # -------------------------
    @property
    def est_tenant(self):
        return self.type_proprietaire == TypeProprietaire.TENANT

    @property
    def est_societe_cliente(self):
        return self.type_proprietaire == TypeProprietaire.SOCIETE_CLIENTE

    @property
    def titulaire(self):
        if self.est_tenant:
            return self.societe
        if self.est_societe_cliente:
            return self.societe_cliente
        return self.proprietaire

    @property
    def nom_proprietaire(self):
        if self.est_tenant:
            return getattr(self.societe, "nom", "") or str(_("Notre société"))
        if self.est_societe_cliente:
            return getattr(self.societe_cliente, "nom_societe_cliente", "") or ""
        p = self.proprietaire
        return f"{p.nom} {p.prenom}".strip() if p else ""

    @property
    def adresse(self):
        return getattr(self.titulaire, "adresse", None)

    @property
    def cle_titulaire(self):
        """Identifiant du titulaire, pour détecter un même propriétaire saisi deux fois."""
        if self.est_tenant:
            return ("tenant",)
        if self.est_societe_cliente:
            return ("societe", str(self.societe_cliente_id))
        return ("proprietaire", self.proprietaire_id)

    @classmethod
    def total_parts(cls, voiture_exemplaire_id, exclure_pk=None):
        qs = cls.objects.filter(voiture_exemplaire_id=voiture_exemplaire_id)
        if exclure_pk:
            qs = qs.exclude(pk=exclure_pk)
        return qs.aggregate(total=Sum("part_proprietaire_pourcent"))["total"] or Decimal("0")

    def clean(self):
        erreurs = {}
        if self.est_tenant:
            self.proprietaire = None
            self.societe_cliente = None
        elif self.est_societe_cliente:
            self.proprietaire = None
            if not self.societe_cliente_id:
                erreurs["societe_cliente"] = _("Choisissez la société partenaire.")
        else:
            self.societe_cliente = None
            # (client particulier repris comme propriétaire : la fiche est créée juste avant l'enregistrement)
            if not self.proprietaire_id and not getattr(self, "proprietaire_a_creer", False):
                erreurs["proprietaire"] = _("Choisissez le propriétaire.")
        if erreurs:
            # Erreur générale (pas liée à un champ) : les formulaires choisissent le titulaire
            # via un champ « titulaire », sans champs proprietaire / societe_cliente
            raise ValidationError(list(erreurs.values()))

        # Saisie groupée (toutes les parts du véhicule en une fois) : total et doublons vérifiés par le formset
        if getattr(self, "verifier_parts", True) and self.voiture_exemplaire_id and self.part_proprietaire_pourcent is not None:
            total = self.total_parts(self.voiture_exemplaire_id, exclure_pk=self.pk)
            if total + self.part_proprietaire_pourcent > CENT:
                raise ValidationError(
                    _("Total des parts > 100 %% interdit (déjà attribué : %(total)s %%, disponible : %(reste)s %%).")
                    % {"total": total, "reste": max(CENT - total, Decimal("0"))}
                )

            # Un même titulaire n'a qu'une part par véhicule
            autres = type(self).objects.filter(voiture_exemplaire_id=self.voiture_exemplaire_id).exclude(pk=self.pk)
            if any(a.cle_titulaire == self.cle_titulaire for a in autres):
                raise ValidationError(_("Ce propriétaire a déjà une part sur ce véhicule : modifiez sa part."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

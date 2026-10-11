import uuid
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from adresse.models import Adresse
from societe_cliente.models import SocieteCliente

DEUX_DECIMALES = Decimal("0.01")


def arrondi(valeur):
    """Arrondi commercial à 2 décimales."""
    return Decimal(str(valeur or 0)).quantize(DEUX_DECIMALES, rounding=ROUND_HALF_UP)


class Company(models.Model):
    """
    Société émettrice de la facture (par tenant) : configuration Peppol.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    adresse = models.ForeignKey(
        Adresse,
        verbose_name=_("Adresse"),
        on_delete=models.PROTECT,
        related_name="companies"
    )
    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="facture_clients",
        null=True,
        blank=True,
    )

    peppol_id = models.CharField(
        _("Identifiant Peppol"),
        max_length=50,
        help_text=_("Ex : 0208:BE0123456789")
    )

    code_pays = models.CharField(
        _("Code pays"),
        max_length=2,
        default="BE"
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Société émettrice")
        verbose_name_plural = _("Sociétés émettrices")

    def __str__(self):
        return self.peppol_id


class Facture(models.Model):
    """
    Facture émise par la société (tenant) à un client particulier
    ou à un client professionnel (facturation électronique UBL / Peppol).
    """

    class TypeFacture(models.TextChoices):
        CLIENT = "CLIENT", _("Client particulier")
        PRO = "PRO", _("Professionnel")

    class Statut(models.TextChoices):
        BROUILLON = "BROUILLON", _("Brouillon")
        EMISE = "EMISE", _("Émise")

    id_facture = models.UUIDField(
        _("Identifiant facture"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Attribué uniquement à l'émission (numérotation continue, sans trou)
    numero = models.CharField(
        _("Numéro de facture"),
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )

    type_facture = models.CharField(
        _("Type de facture"),
        max_length=10,
        choices=TypeFacture.choices,
        default=TypeFacture.CLIENT,
    )

    statut = models.CharField(
        _("Statut"),
        max_length=10,
        choices=Statut.choices,
        default=Statut.BROUILLON,
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="factures",
        null=True,
        blank=True,
        verbose_name=_("Société"),
    )

    company = models.ForeignKey(
        Company,
        verbose_name=_("Société émettrice"),
        on_delete=models.PROTECT,
        related_name="invoices",
        null=True,
        blank=True,
    )

    # Maintenances facturées
    maintenances = models.ManyToManyField(
        "maintenance.Maintenance",
        related_name="factures",
        blank=True,
        verbose_name=_("Maintenances"),
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="factures",
        verbose_name=_("Véhicule"),
    )

    # Client particulier
    client_particulier = models.ForeignKey(
        "client_particulier.ClientParticulier",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="factures",
        verbose_name=_("Client particulier"),
    )

    # Client professionnel
    societe_cliente = models.ForeignKey(
        SocieteCliente,
        verbose_name=_("Client professionnel"),
        on_delete=models.PROTECT,
        related_name="purchases",
        null=True,
        blank=True
    )

    # Copie des coordonnées du client au moment de l'émission
    # (la facture ne change plus si la fiche client est modifiée ensuite)
    client_nom = models.CharField(_("Nom du client"), max_length=255, blank=True)
    client_adresse = models.TextField(_("Adresse du client"), blank=True)
    client_tva = models.CharField(_("TVA du client"), max_length=30, blank=True)
    client_email = models.EmailField(_("Email du client"), blank=True)

    issue_date = models.DateField(_("Date d’émission"), default=timezone.localdate)
    due_date = models.DateField(_("Date d'échéance"), null=True, blank=True)
    currency = models.CharField(_("Devise"), max_length=3, default="EUR")

    # Marges par défaut appliquées aux lignes générées depuis les maintenances
    marge_pieces = models.DecimalField(
        _("Marge pièces (%)"),
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    marge_main_oeuvre = models.DecimalField(
        _("Marge main-d'œuvre (%)"),
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    # Autoliquidation (client pro assujetti dans un autre pays de l'UE)
    autoliquidation = models.BooleanField(_("Autoliquidation TVA"), default=False)

    total_ht = models.DecimalField(_("Total HTVA"), max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_tva = models.DecimalField(_("Total TVA"), max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(_("Total TVAC"), max_digits=12, decimal_places=2, default=Decimal("0.00"))

    remarques = models.TextField(_("Remarques"), blank=True)

    # Facture électronique (UBL 2.1 / Peppol BIS Billing 3.0)
    xml_ubl = models.TextField(_("XML UBL"), blank=True)
    peppol_envoyee_le = models.DateTimeField(_("Envoyée via Peppol le"), null=True, blank=True)
    peppol_reponse = models.TextField(_("Réponse Peppol"), blank=True)

    emise_le = models.DateTimeField(_("Émise le"), null=True, blank=True)
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="factures_creees",
        verbose_name=_("Créée par"),
    )
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, null=True)

    class Meta:
        verbose_name = _("Facture")
        verbose_name_plural = _("Factures")
        ordering = ["-issue_date", "-created_at"]

    def __str__(self):
        return _("Facture %(numero)s") % {"numero": self.numero or _("brouillon")}

    # -------------------------
    # ÉTAT
    # -------------------------
    @property
    def est_pro(self):
        return self.type_facture == self.TypeFacture.PRO

    @property
    def est_brouillon(self):
        return self.statut == self.Statut.BROUILLON

    @property
    def est_emise(self):
        return self.statut == self.Statut.EMISE

    # -------------------------
    # CLIENT
    # -------------------------
    @property
    def client(self):
        return self.societe_cliente if self.est_pro else self.client_particulier

    def nom_client_courant(self):
        if self.est_emise and self.client_nom:
            return self.client_nom
        if self.est_pro and self.societe_cliente:
            return self.societe_cliente.nom_societe_cliente or ""
        if self.client_particulier:
            return f"{self.client_particulier.prenom} {self.client_particulier.nom}".strip()
        return ""

    def copier_coordonnees_client(self):
        """Fige les coordonnées du client sur la facture (à l'émission)."""
        client = self.client
        adresse = getattr(client, "adresse", None) if client else None
        self.client_nom = self.nom_client_courant()
        self.client_email = (getattr(client, "email", "") or "") if client else ""
        self.client_tva = (getattr(client, "numero_tva", "") or "") if self.est_pro and client else ""
        if adresse:
            ligne1 = f"{adresse.rue} {adresse.numero}".strip()
            if adresse.boite:
                ligne1 += f" / {adresse.boite}"
            self.client_adresse = "\n".join(filter(None, [
                ligne1,
                f"{adresse.code_postal} {adresse.ville}".strip(),
                adresse.pays or "",
            ]))
        else:
            self.client_adresse = ""

    # -------------------------
    # TOTAUX
    # -------------------------
    def totaux_par_taux(self):
        """{taux_tva: {"base": Decimal, "tva": Decimal}} — TVA calculée par taux (règle EN 16931)."""
        groupes = {}
        for ligne in self.lines.all():
            taux = Decimal("0.00") if self.autoliquidation else arrondi(ligne.vat_rate)
            groupe = groupes.setdefault(taux, {"base": Decimal("0.00"), "tva": Decimal("0.00")})
            groupe["base"] += ligne.total_ht
        for taux, groupe in groupes.items():
            groupe["base"] = arrondi(groupe["base"])
            groupe["tva"] = arrondi(groupe["base"] * taux / Decimal("100"))
        return dict(sorted(groupes.items()))

    def recalculer_totaux(self, save=True):
        groupes = self.totaux_par_taux()
        self.total_ht = arrondi(sum((g["base"] for g in groupes.values()), Decimal("0.00")))
        self.total_tva = arrondi(sum((g["tva"] for g in groupes.values()), Decimal("0.00")))
        self.total = arrondi(self.total_ht + self.total_tva)
        if save:
            self.save(update_fields=["total_ht", "total_tva", "total", "updated_at"])

    # -------------------------
    # NUMÉROTATION
    # -------------------------
    @classmethod
    def prochain_numero(cls, annee):
        """F2026-0001, F2026-0002… (une séquence par année et par tenant)."""
        prefixe = f"F{annee}-"
        derniers = (
            cls.objects.select_for_update()
            .filter(numero__startswith=prefixe)
            .values_list("numero", flat=True)
        )
        maximum = 0
        for numero in derniers:
            try:
                maximum = max(maximum, int(numero[len(prefixe):]))
            except ValueError:
                continue
        return f"{prefixe}{maximum + 1:04d}"


class FactureLine(models.Model):

    class TypeLigne(models.TextChoices):
        PIECE = "PIECE", _("Pièce / produit")
        MAIN_OEUVRE = "MAIN_OEUVRE", _("Main-d'œuvre")
        AUTRE = "AUTRE", _("Autre")

    facture = models.ForeignKey(
        Facture,
        verbose_name=_("Facture"),
        related_name="lines",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lignes_facture",
        verbose_name=_("Maintenance"),
    )

    type_ligne = models.CharField(
        _("Type de ligne"),
        max_length=15,
        choices=TypeLigne.choices,
        default=TypeLigne.AUTRE,
    )

    ordre = models.PositiveIntegerField(_("Ordre"), default=0)

    description = models.CharField(_("Description"), max_length=255)
    reference = models.CharField(_("Référence"), max_length=100, blank=True)

    quantity = models.DecimalField(
        _("Quantité"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("1.00"),
    )

    # Prix d'achat HTVA (pièces) ou taux horaire (main-d'œuvre) avant marge
    unit_cost = models.DecimalField(
        _("Coût unitaire HTVA"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    marge = models.DecimalField(
        _("Marge (%)"),
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    # Prix de vente unitaire HTVA (= coût × (1 + marge))
    unit_price = models.DecimalField(
        _("Prix unitaire HTVA"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    vat_rate = models.DecimalField(
        _("Taux de TVA"),
        max_digits=4,
        decimal_places=2,
        default=Decimal("21.00"),
        help_text=_("Taux de TVA : 6, 12, 21")
    )

    class Meta:
        verbose_name = _("Ligne de facture")
        verbose_name_plural = _("Lignes de facture")
        ordering = ["ordre", "id"]

    def __str__(self):
        return _("%(desc)s (%(facture)s)") % {
            "desc": self.description,
            "facture": self.facture.numero if self.facture else "-",
        }

    @property
    def unite(self):
        """Code d'unité UN/ECE rec. 20 utilisé dans le XML."""
        return "HUR" if self.type_ligne == self.TypeLigne.MAIN_OEUVRE else "C62"

    @property
    def total_ht(self):
        return arrondi(Decimal(self.quantity or 0) * Decimal(self.unit_price or 0))

    @property
    def marge_montant(self):
        if self.unit_cost is None:
            return Decimal("0.00")
        return arrondi((Decimal(self.unit_price or 0) - Decimal(self.unit_cost)) * Decimal(self.quantity or 0))

    def calculer_prix(self):
        if self.unit_cost is not None:
            self.unit_price = arrondi(
                Decimal(self.unit_cost) * (Decimal("1") + Decimal(self.marge or 0) / Decimal("100"))
            )

    def save(self, *args, **kwargs):
        self.calculer_prix()
        super().save(*args, **kwargs)


class ParametresPeppol(models.Model):
    """
    Paramètres de facturation électronique Peppol d'une société (tenant) :
    point d'accès (Access Point) de test et de production, clés API, identifiant émetteur.
    """

    class Environnement(models.TextChoices):
        TEST = "TEST", _("Test (sandbox)")
        PRODUCTION = "PRODUCTION", _("Production")

    class TypeAuth(models.TextChoices):
        BEARER = "BEARER", _("Bearer token (Authorization: Bearer …)")
        ENTETE = "ENTETE", _("Clé API dans un en-tête personnalisé")

    societe = models.OneToOneField(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="parametres_peppol",
        verbose_name=_("Société"),
    )

    actif = models.BooleanField(_("Envoi Peppol activé"), default=False)
    environnement = models.CharField(
        _("Environnement utilisé"),
        max_length=10,
        choices=Environnement.choices,
        default=Environnement.TEST,
    )

    # Identifiant Peppol de la société émettrice (ex. 0208:0123456789)
    peppol_id = models.CharField(
        _("Identifiant Peppol émetteur"),
        max_length=50,
        blank=True,
        help_text=_("Ex : 0208:0123456789 (numéro d'entreprise belge). Vide : déduit du numéro de TVA."),
    )

    # Serveur de test
    url_test = models.URLField(_("URL du serveur de test"), max_length=255, blank=True)
    cle_api_test = models.CharField(_("Clé API de test"), max_length=255, blank=True)

    # Serveur de production
    url_production = models.URLField(_("URL du serveur de production"), max_length=255, blank=True)
    cle_api_production = models.CharField(_("Clé API de production"), max_length=255, blank=True)

    type_auth = models.CharField(
        _("Authentification"),
        max_length=10,
        choices=TypeAuth.choices,
        default=TypeAuth.BEARER,
    )
    nom_entete = models.CharField(
        _("Nom de l'en-tête de la clé API"),
        max_length=100,
        default="X-API-Key",
        blank=True,
    )
    timeout = models.PositiveIntegerField(_("Délai maximum (secondes)"), default=30)

    envoi_automatique = models.BooleanField(
        _("Envoyer automatiquement à l'émission"),
        default=False,
        help_text=_("Les factures professionnelles sont envoyées via Peppol dès leur émission."),
    )

    derniere_verification = models.DateTimeField(_("Dernier test de connexion"), null=True, blank=True)
    dernier_resultat = models.TextField(_("Résultat du dernier test"), blank=True)
    dernier_test_ok = models.BooleanField(_("Dernier test réussi"), default=False)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Paramètres Peppol")
        verbose_name_plural = _("Paramètres Peppol")

    def __str__(self):
        return _("Paramètres Peppol – %(societe)s") % {"societe": self.societe}

    @property
    def est_test(self):
        return self.environnement == self.Environnement.TEST

    @property
    def url_active(self):
        return self.url_test if self.est_test else self.url_production

    @property
    def cle_active(self):
        return self.cle_api_test if self.est_test else self.cle_api_production

    @property
    def est_configure(self):
        return bool(self.actif and self.url_active and self.cle_active)

    def entetes_auth(self):
        if self.type_auth == self.TypeAuth.ENTETE:
            return {(self.nom_entete or "X-API-Key"): self.cle_active}
        return {"Authorization": f"Bearer {self.cle_active}"}

    @classmethod
    def pour_societe(cls, societe):
        if societe is None:
            return None
        return cls.objects.filter(societe=societe).first()

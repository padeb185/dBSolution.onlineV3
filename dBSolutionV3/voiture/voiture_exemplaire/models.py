import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from client_particulier.models import ClientParticulier
from django.conf import settings
from maintenance.choices import CoteConduite
from societe.models import Societe
from voiture.voiture_exemplaire.utils_vin import VinDecoderService


class TypeUtilisation(models.TextChoices):
    SOCIETE = "societe", _("Société")
    CLIENT = "client", _("Client")
    PRIVE = "prive", _("Privé")
    LOCATION = "location", _("Location")
    INTERNE = "interne", _("Interne")

class NomPays(models.TextChoices):
    # Les valeurs doivent correspondre exactement à celles testées dans
    # maintenance/templates/maintenance/partials/plaque.html
    # --- Benelux ---
    BE = "Belgique", _("Belgique")
    LU = "Luxembourg", _("Luxembourg")
    NL = "Pays-Bas", _("Pays-Bas")
    # --- Europe de l'Ouest ---
    DE = "Allemagne", _("Allemagne")
    FR = "France", _("France")
    AT = "Autriche", _("Autriche")
    IE = "Irlande", _("Irlande")
    # --- Europe du Sud ---
    IT = "Italie", _("Italie")
    ES = "Espagne", _("Espagne")
    PT = "Portugal", _("Portugal")
    GR = "Grèce", _("Grèce")
    CY = "Chypre", _("Chypre")
    MT = "Malte", _("Malte")
    # --- Europe du Nord ---
    DK = "Danemark", _("Danemark")
    SE = "Suède", _("Suède")
    FI = "Finlande", _("Finlande")
    EE = "Estonie", _("Estonie")
    LV = "Lettonie", _("Lettonie")
    LT = "Lituanie", _("Lituanie")
    # --- Europe centrale et de l'Est ---
    PL = "Pologne", _("Pologne")
    CZ = "Tchéquie", _("Tchéquie")
    SK = "Slovaquie", _("Slovaquie")
    HU = "Hongrie", _("Hongrie")
    SI = "Slovénie", _("Slovénie")
    HR = "Croatie", _("Croatie")
    RO = "Roumanie", _("Roumanie")
    BG = "Bulgarie", _("Bulgarie")
    # --- Hors UE ---
    GB = "Royaume-Uni", _("Royaume-Uni")
    NO = "Norvège", _("Norvège")
    CH = "Suisse", _("Suisse")


class KilometresRodage(models.IntegerChoices):
    KM_1000 = 1000, _("1000 km")
    KM_2000 = 2000, _("2000 km")
    KM_3000 = 3000, _("3000 km")
    KM_4000 = 4000, _("4000 km")
    KM_5000 = 5000, _("5000 km")

class KilometresEntretien(models.IntegerChoices):
    KM_5000 = 5000, _("5000 km")
    KM_7500 = 7500, _("7500 km")
    KM_10000 = 10000, _("10000 km")
    KM_12500 = 12500, _("12500 km")
    KM_15000 = 15000, _("15000 km")
    KM_20000 = 20000, _("20000 km")
    KM_25000 = 25000, _("25000 km")


class VoitureExemplaire(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.PROTECT,
        related_name="voitures"
    )

    voiture_modele = models.ForeignKey(
        "voiture_modele.VoitureModele",
        on_delete=models.PROTECT,
        related_name="voitures"
    )

    voiture_embrayage = models.ForeignKey(
        "voiture_embrayage.VoitureEmbrayage",
        on_delete=models.PROTECT,
        related_name="voitures",
        null=True,
        blank=True
    )

    voiture_boite = models.OneToOneField(
        "voiture_boite.VoitureBoite",
        on_delete=models.PROTECT,
        related_name="voitures",
        null=True,
        blank=True
    )

    voiture_moteur = models.OneToOneField(
        "voiture_moteur.MoteurVoiture",
        on_delete=models.PROTECT,
        related_name="voitures",
        null=True,
        blank=True
    )

    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)

    # 🚗 Identification
    immatriculation = models.CharField(
        max_length=12,
        unique=True,
    )

    pays = models.CharField(
        max_length=20,
        choices=NomPays.choices,
        null=True,
        blank=True
    )

    vin_validator = RegexValidator(
        regex=r'^[A-HJ-NPR-Z0-9]{17}$',
        message=_("Le numéro VIN doit contenir exactement 17 caractères alphanumériques (lettres A-H, J-N, P, R-Z et chiffres).")
    )

    numero_vin = models.CharField(
        max_length=17,
        unique=True,
        verbose_name="Numéro VIN",
        validators=[vin_validator],
    )

    vin_simplifie = models.CharField(
        max_length=10,
        verbose_name="VIN simplifié",
        editable=False,
    )

    est_apres_2010 = models.BooleanField(
        default=True,
        editable=False,
        verbose_name="Véhicule de 2010 ou après",
    )

    annee_production = models.PositiveIntegerField(
        verbose_name="Année de production",
        editable=False,
        blank=True,
        null=True,
    )
    mois_production = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ],
        blank=True,
        null=True,
        verbose_name="Mois de production",
    )

    type_utilisation = models.CharField(
        max_length=10,
        choices=TypeUtilisation.choices,
        default=TypeUtilisation.CLIENT
    )

    cote_conduite = models.CharField(
        max_length=25,
        choices=CoteConduite.choices,
        default=CoteConduite.GAUCHE,
        verbose_name=_("Coté conducteur"),
        null=True,
        blank=True,
    )

    # 📏 Kilométrage châssis
    kilometres_chassis = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="Kilomètres châssis")

    kilometres_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback")
    )

    kilometres_rodage = models.PositiveIntegerField(
        choices=KilometresRodage.choices,
        default=KilometresRodage.KM_1000,
        verbose_name=_("Kilométrage de rodage"),
    )

    kilometres_entretien = models.PositiveIntegerField(
        choices=KilometresEntretien.choices,
        default=KilometresEntretien.KM_15000,
        verbose_name=_("Intervalle d'entretien"),
    )

    kilometres_dernier_entretien = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_entretien_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback entretien")
    )

    kilometres_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_remplacement_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_embrayage_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback embrayage")
    )


    kilometres_boite = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_remplacement_boite = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_boite_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback boite")
    )

    kilometres_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_remplacement_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_moteur_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback boite")
    )


    variation_kilometres = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text="Calculé automatiquement : total - dernièr entretien"
    )

    date_derniere_intervention = models.DateField(blank=True, null=True)

    # 🏭 Production

    nombre_remplacements_moteurs = models.PositiveIntegerField(default=0)
    nombre_remplacements_boites = models.PositiveIntegerField(default=0)
    # ⚙️ Moteur / transmission
    numero_moteur = models.CharField(max_length=50, null=True, blank=True)

    date_mise_en_circulation = models.DateField(null=True, blank=True)


    couleur = models.CharField(max_length=50, blank=True, null=True)
    code_couleur = models.CharField(max_length=50, blank=True, null=True)

    # 💰 Données financières
    ETAT_ACHAT_CHOICES = [
        ("NEUF", _("Neuf")),
        ("OCCASION", _("Occasion")),
    ]

    etat_achat = models.CharField(
        max_length=10,
        choices=ETAT_ACHAT_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Véhicule acheté"),
    )

    # Kilométrage au moment de l'achat : 0 pour un véhicule neuf, à compléter pour une occasion
    kilometrage_achat = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Kilométrage de départ"),
    )

    prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    assurance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    taxe_mise_en_circulation = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    taxe_roulage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    # Date d'achat : point de départ des coûts annuels (assurance, taxe, vignettes)
    date_achat = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date d'achat"),
    )

    # Autres frais d'achat : immatriculation, plaques, transport, préparation, carte grise…
    frais_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Autres frais d'achat"),
    )

    # Valeur de revente estimée (ou prix de vente réel) : déduite du coût total du véhicule
    valeur_revente = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Valeur de revente"),
    )

    # Estimation du carburant non encodé (pleins manquants depuis l'achat)
    consommation_estimee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Consommation moyenne (L/100 km)"),
    )
    prix_carburant_estime = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name=_("Prix approximatif du carburant (€/L TVAC)"),
    )

    # 👥 Propriétaires
    nombre_proprietaires = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True
    )

    part_proprietaires_pourcent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )

    client = models.ForeignKey(
        ClientParticulier,
        on_delete=models.CASCADE,
        related_name="exemplaires",
        null=True,
        blank=True
    )


    last_maintained_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="entretien_voitures"
    )

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]

    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="JAUNE",
        verbose_name=_("État visuel / Tag"),
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    @property
    def pneu_avant(self):
        return (
            self.pneus.filter(emplacement="avant").first()
            or self.pneus.filter(emplacement="avant_arriere").first()
        )

    @property
    def pneu_arriere(self):
        return (
            self.pneus.filter(emplacement="arriere").first()
            or self.pneus.filter(emplacement="avant_arriere").first()
        )

    def __str__(self):
        return f"{self.voiture_marque.nom_marque} {self.voiture_modele.nom_modele} {self.voiture_modele.nom_variante} - {self.immatriculation}"

    def save(self, *args, **kwargs):

        if self.numero_vin:
            # -----------------------------------------------------
            # Normalisation VIN
            # -----------------------------------------------------
            self.numero_vin = self.numero_vin.strip().upper()
            self.vin_simplifie = self.numero_vin[-10:]

            # -----------------------------------------------------
            # Marque
            # -----------------------------------------------------
            brand = None

            if self.voiture_marque_id:
                brand = self.voiture_marque.nom_marque

            # -----------------------------------------------------
            # Année de première mise en circulation
            # -----------------------------------------------------
            registration_year = None

            if self.date_mise_en_circulation:
                registration_year = self.date_mise_en_circulation.year

            # -----------------------------------------------------
            # Décodage VIN
            # -----------------------------------------------------
            decoder = VinDecoderService(
                vin=self.numero_vin,
                brand=brand,
                registration_year=registration_year,
            )

            data = decoder.decode()

            production_year = data.get("production_year")

            # -----------------------------------------------------
            # Année de production
            # -----------------------------------------------------
            if production_year is not None:
                self.annee_production = production_year

                self.est_apres_2010 = (
                        production_year >= 2010
                )

            else:
                self.annee_production = None

        else:
            self.vin_simplifie = None
            self.annee_production = None

        # ---------------------------------------------------------
        # Kilométrages
        # ---------------------------------------------------------
        self.update_kilometres()

        super().save(*args, **kwargs)



    # ---------------------------------------------------------
    # Alertes rodage / entretien
    # ---------------------------------------------------------
    INTERVALLE_ENTRETIEN_DEFAUT = 15000

    @property
    def intervalle_entretien(self):
        """Intervalle d'entretien choisi sur le véhicule (kilometres_entretien), 15 000 km par défaut."""
        return self.kilometres_entretien or self.INTERVALLE_ENTRETIEN_DEFAUT

    @property
    def km_debut_moteur(self):
        """Kilométrage châssis au montage du moteur actuel (0 = moteur d'origine)."""
        return self.kilometres_remplacement_moteur or 0

    @property
    def moteur_neuf(self):
        """
        Moteur à roder : moteur remplacé, ou véhicule créé avec un moteur
        n'ayant pas encore parcouru la distance de rodage.
        """
        if self.kilometres_remplacement_moteur:
            return True
        km_creation = self.kilometrage_achat
        return km_creation is not None and km_creation < (self.kilometres_rodage or 0)

    @property
    def km_rodage_effectue(self):
        """
        Kilométrage châssis du dernier rodage au tag vert pour le moteur actuel
        (None si le rodage n'a pas encore été validé).
        """
        if not self.pk:
            return None
        if not hasattr(self, "_km_rodage_effectue"):
            from django.db.models import Max
            from maintenance.autres_interventions.moteur.rodage.models import Rodage
            self._km_rodage_effectue = Rodage.objects.filter(
                voiture_exemplaire_id=self.pk, tag="VERT",
                kilometres_rodage__gte=self.km_debut_moteur,
            ).aggregate(m=Max("kilometres_rodage"))["m"]
        return self._km_rodage_effectue

    @property
    def rodage_valide(self):
        """Un rodage au tag vert a été enregistré pour le moteur actuel."""
        return self.km_rodage_effectue is not None

    @property
    def premier_entretien_fait(self):
        """Un entretien a été fait depuis le montage du moteur actuel."""
        dernier = self.kilometres_dernier_entretien or 0
        return dernier > 0 and dernier >= self.km_debut_moteur

    @property
    def alerte_rodage(self):
        """
        None, ou {"niveau": "info"|"alerte", "restant": km} :
        - pendant le rodage (km moteur < distance de rodage) : info ;
        - distance de rodage atteinte sans rodage au tag vert : alerte.
        S'arrête dès qu'un rodage au tag vert est enregistré pour le moteur actuel ;
        se réactive après un remplacement moteur.
        """
        if not self.moteur_neuf or self.rodage_valide:
            return None
        km_moteur = self.kilometres_moteur or 0
        distance = self.kilometres_rodage or 0
        if km_moteur < distance:
            return {"niveau": "info", "restant": distance - km_moteur}
        return {"niveau": "alerte", "restant": 0}

    @property
    def km_reference_entretien(self):
        """
        Kilométrage châssis à partir duquel court l'intervalle d'entretien :
        le plus récent entre le dernier entretien (du moteur actuel) et le rodage effectué.
        None si ni entretien ni rodage depuis le montage du moteur.
        """
        refs = []
        if self.premier_entretien_fait:
            refs.append(self.kilometres_dernier_entretien or 0)
        if self.km_rodage_effectue is not None:
            refs.append(self.km_rodage_effectue)
        return max(refs) if refs else None

    @property
    def prochain_entretien_km(self):
        """Kilométrage châssis du prochain entretien (None si rien ne sert de référence)."""
        ref = self.km_reference_entretien
        return None if ref is None else ref + self.intervalle_entretien

    @property
    def alerte_entretien(self):
        """
        None, ou {"depasse": km, "seuil": km, "premier": bool} :
        - rodage effectué : alerte quand km châssis > km du rodage effectué + intervalle ;
        - ensuite : km châssis > km du dernier entretien + intervalle ;
        - sans rodage ni entretien depuis le montage du moteur :
          km moteur > distance de rodage + intervalle (moteur neuf) ou > intervalle.
        """
        intervalle = self.intervalle_entretien
        ref = self.km_reference_entretien
        if ref is not None:
            depuis = (self.kilometres_chassis or 0) - ref
            if depuis > intervalle:
                premier = not self.premier_entretien_fait or ref == self.km_rodage_effectue
                return {"depasse": depuis - intervalle, "seuil": ref + intervalle, "premier": premier}
            return None
        km_moteur = self.kilometres_moteur or 0
        seuil = intervalle + ((self.kilometres_rodage or 0) if self.moteur_neuf else 0)
        if km_moteur > seuil:
            return {"depasse": km_moteur - seuil, "seuil": seuil, "premier": True}
        return None

    def update_kilometres(self):
        km_chassis = self.kilometres_chassis or 0

        self.variation_kilometres = max(
            0,
            km_chassis - (self.kilometres_dernier_entretien or 0)
        )

        # -------------------------
        # MOTEUR
        # -------------------------
        if self.kilometres_remplacement_moteur:
            # Jamais négatif (remplacement saisi au-delà du compteur châssis actuel)
            self.kilometres_moteur = max(0, km_chassis - self.kilometres_remplacement_moteur)
        else:
            self.kilometres_moteur = km_chassis

        # -------------------------
        # BOÎTE
        # -------------------------
        if self.kilometres_remplacement_boite:
            self.kilometres_boite = max(0, km_chassis - self.kilometres_remplacement_boite)
        else:
            self.kilometres_boite = km_chassis

        # -------------------------
        # EMBRAYAGE
        # -------------------------
        if self.kilometres_remplacement_embrayage:
            self.kilometres_embrayage = max(0, km_chassis - self.kilometres_remplacement_embrayage)
        else:
            self.kilometres_embrayage = km_chassis


def precharger_alertes(exemplaires):
    """
    Listes de véhicules : lit en UNE requête les rodages au tag vert
    (kilométrage du rodage effectué pour le moteur actuel), au lieu d'une requête par véhicule.
    """
    from maintenance.autres_interventions.moteur.rodage.models import Rodage
    exemplaires = list(exemplaires)
    par_id = {ex.pk: ex for ex in exemplaires}
    for ex in exemplaires:
        ex._km_rodage_effectue = None
    for vid, km in Rodage.objects.filter(voiture_exemplaire_id__in=par_id, tag="VERT").values_list(
            "voiture_exemplaire_id", "kilometres_rodage"):
        ex = par_id.get(vid)
        if ex is None or km is None or km < ex.km_debut_moteur:
            continue
        if ex._km_rodage_effectue is None or km > ex._km_rodage_effectue:
            ex._km_rodage_effectue = km
    return exemplaires


class CoutAnnuelVehicule(models.Model):
    """
    Coût annuel d'un véhicule, modifiable année par année :
    assurance, taxe de circulation, vignettes (Allemagne, Autriche, Suisse…), contrôle technique…
    Sans ligne pour une année, l'assurance et la taxe de circulation reprennent
    les montants annuels par défaut des données financières du véhicule.
    """

    class Type(models.TextChoices):
        ASSURANCE = "ASSURANCE", _("Assurance")
        TAXE_CIRCULATION = "TAXE_CIRCULATION", _("Taxe de circulation")
        VIGNETTE = "VIGNETTE", _("Vignette / péage")
        CONTROLE_TECHNIQUE = "CONTROLE_TECHNIQUE", _("Contrôle technique")
        AUTRE = "AUTRE", _("Autre")

    class PaysVignette(models.TextChoices):
        AUCUN = "", _("—")
        DE = "DE", _("Allemagne (Umweltplakette)")
        AT = "AT", _("Autriche")
        CH = "CH", _("Suisse")
        FR = "FR", _("France (Crit'Air)")
        BE = "BE", _("Belgique (LEZ)")
        NL = "NL", _("Pays-Bas")
        LU = "LU", _("Luxembourg")
        IT = "IT", _("Italie")
        SI = "SI", _("Slovénie")
        CZ = "CZ", _("Tchéquie")
        SK = "SK", _("Slovaquie")
        HU = "HU", _("Hongrie")
        RO = "RO", _("Roumanie")
        BG = "BG", _("Bulgarie")
        AUTRE = "XX", _("Autre pays")

    exemplaire = models.ForeignKey(
        VoitureExemplaire,
        on_delete=models.CASCADE,
        related_name="couts_annuels",
        verbose_name=_("Véhicule"),
    )
    annee = models.PositiveIntegerField(verbose_name=_("Année"))
    type_cout = models.CharField(max_length=20, choices=Type.choices, verbose_name=_("Type"))
    pays = models.CharField(max_length=2, choices=PaysVignette.choices, blank=True, default="", verbose_name=_("Pays"))
    libelle = models.CharField(max_length=100, blank=True, verbose_name=_("Libellé"))
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Montant (€)"))
    date = models.DateField(null=True, blank=True, verbose_name=_("Date de paiement"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Coût annuel du véhicule")
        verbose_name_plural = _("Coûts annuels du véhicule")
        ordering = ["-annee", "type_cout", "pays"]

    def __str__(self):
        return f"{self.exemplaire} – {self.annee} – {self.get_type_cout_display()} : {self.montant} €"


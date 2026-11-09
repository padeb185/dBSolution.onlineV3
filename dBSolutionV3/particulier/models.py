"""
Espace « particuliers » (application Flutter) : données d'un particulier, rangées dans le tenant
partagé settings.PARTICULIERS_SCHEMA (un seul schéma pour tous les particuliers).

Chaque enregistrement appartient à un utilisateur (proprietaire) : l'API filtre TOUJOURS par
propriétaire (voir particulier/api/views.py). Les fichiers (tickets, documents) ne sont jamais servis
par /media/ : ils passent par l'API, qui vérifie le propriétaire.
"""
import os
import uuid
from datetime import date
from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from utilisateurs.models import Utilisateur

ZERO = Decimal("0.00")


def _chemin(instance, nom_fichier, dossier):
    ext = os.path.splitext(nom_fichier)[1].lower()[:10]
    proprietaire = getattr(instance, "proprietaire_id", None) or instance.vehicule.proprietaire_id
    return f"particuliers/{proprietaire}/{dossier}/{uuid.uuid4().hex}{ext}"


def chemin_photo(instance, nom):
    return _chemin(instance, nom, "photos")


def chemin_ticket(instance, nom):
    return _chemin(instance, nom, "tickets")


def chemin_facture(instance, nom):
    return _chemin(instance, nom, "factures")


def chemin_document(instance, nom):
    return _chemin(instance, nom, "documents")


class Energie(models.TextChoices):
    ESSENCE = "essence", _("Essence")
    DIESEL = "diesel", _("Diesel")
    HYBRIDE = "hybride", _("Hybride")
    HYBRIDE_RECHARGEABLE = "phev", _("Hybride rechargeable")
    ELECTRIQUE = "electrique", _("Électrique")
    GPL = "gpl", _("GPL")
    GNC = "gnc", _("GNC")


class Vehicule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name="vehicules_particulier")
    marque = models.CharField(_("Marque"), max_length=60)
    modele = models.CharField(_("Modèle"), max_length=80)
    version = models.CharField(_("Version / finition"), max_length=120, blank=True)
    puissance_ch = models.PositiveSmallIntegerField(_("Puissance (ch)"), null=True, blank=True)
    immatriculation = models.CharField(_("Immatriculation"), max_length=20, blank=True)
    pays_immatriculation = models.CharField(_("Pays d'immatriculation"), max_length=2, default="BE")
    vin = models.CharField(_("VIN"), max_length=17, blank=True)
    energie = models.CharField(_("Énergie"), max_length=12, choices=Energie.choices, default=Energie.ESSENCE)
    annee = models.PositiveSmallIntegerField(_("Année du modèle"), null=True, blank=True)
    date_mise_en_circulation = models.DateField(_("Première mise en circulation"), null=True, blank=True)
    date_achat = models.DateField(_("Date d'achat"), null=True, blank=True)
    prix_achat = models.DecimalField(_("Prix d'achat"), max_digits=12, decimal_places=2, null=True, blank=True,
                                     validators=[MinValueValidator(0)])
    kilometrage_achat = models.PositiveIntegerField(_("Kilométrage à l'achat"), null=True, blank=True)
    valeur_estimee = models.DecimalField(_("Valeur de revente estimée"), max_digits=12, decimal_places=2,
                                         null=True, blank=True, validators=[MinValueValidator(0)])
    couleur = models.CharField(_("Couleur"), max_length=40, blank=True)
    photo = models.ImageField(_("Photo"), upload_to=chemin_photo, null=True, blank=True)
    archive = models.BooleanField(_("Archivé (vendu)"), default=False)
    # Unités propres au véhicule (ex. voiture importée des États-Unis, compteur en miles) ;
    # vide : unités des réglages du compte. Les valeurs restent enregistrées en km et en litres.
    unite_distance = models.CharField(_("Distances"), max_length=2, blank=True, choices=[("km", "km"), ("mi", "mi")])
    unite_volume = models.CharField(_("Volumes de carburant"), max_length=6, blank=True,
                                    choices=[("L", "L"), ("gal_us", "gal US"), ("gal_uk", "gal UK")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Véhicule (particulier)")
        verbose_name_plural = _("Véhicules (particuliers)")
        ordering = ["archive", "marque", "modele"]

    def __str__(self):
        return f"{self.marque} {self.modele} {self.immatriculation}".strip()

    @property
    def kilometrage_actuel(self):
        """Plus haut kilométrage connu (relevés, pleins, entretiens, achat)."""
        valeurs = [self.kilometrage_achat or 0]
        for qs in (self.releves.all(), self.pleins.all(), self.entretiens.all(), self.maintenances.all()):
            km = qs.aggregate(m=models.Max("kilometrage"))["m"]
            if km:
                valeurs.append(km)
        return max(valeurs)

    @property
    def kilometrage_depart(self):
        """Kilométrage de départ des calculs au km : celui de l'achat, sinon le plus bas kilométrage saisi."""
        if self.kilometrage_achat is not None:
            return self.kilometrage_achat
        valeurs = [km for qs in (self.releves.all(), self.pleins.all(), self.entretiens.all(), self.maintenances.all())
                   for km in [qs.aggregate(m=models.Min("kilometrage"))["m"]] if km]
        return min(valeurs) if valeurs else None


class ReleveKilometrique(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="releves")
    date = models.DateField(_("Date"), default=date.today)
    kilometrage = models.PositiveIntegerField(_("Kilométrage"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Relevé kilométrique")
        verbose_name_plural = _("Relevés kilométriques")
        ordering = ["-date", "-kilometrage"]


class Carburant(models.TextChoices):
    SP95 = "sp95", _("Essence SP95 (E5)")
    SP95_E10 = "sp95_e10", _("Essence SP95-E10")
    SP98 = "sp98", _("Essence SP98 (Super Plus)")
    SP102 = "sp102", _("Essence 102 (Ultimate 102)")
    DIESEL = "diesel", _("Diesel (B7)")
    DIESEL_PREMIUM = "diesel_premium", _("Diesel premium (Diesel+)")
    HVO = "hvo", _("HVO (diesel renouvelable, XTL)")
    E85 = "e85", _("Éthanol E85 (superéthanol)")
    GPL = "gpl", _("GPL (LPG)")
    GNC = "gnc", _("GNC (CNG)")
    ELECTRICITE = "electricite", _("Électricité")


# Unité de la quantité selon le carburant (consommation : unité / 100 km)
UNITES_CARBURANT = {Carburant.ELECTRICITE: "kWh", Carburant.GNC: "kg"}

# Carburant proposé par défaut selon l'énergie du véhicule
CARBURANT_PAR_ENERGIE = {
    "essence": Carburant.SP95, "hybride": Carburant.SP95, "phev": Carburant.SP95,
    "diesel": Carburant.DIESEL, "gpl": Carburant.GPL, "gnc": Carburant.GNC, "electrique": Carburant.ELECTRICITE,
}


def unite_carburant(carburant):
    return UNITES_CARBURANT.get(carburant, "L")


class NiveauCarburant(models.TextChoices):
    """Carburant restant dans le réservoir au moment du plein (recharge : batterie restante)."""
    TROIS_QUARTS = "3/4", _("¾")
    MOITIE = "1/2", _("½")
    QUART = "1/4", _("¼")
    RESERVE = "reserve", _("Réserve")
    FIN_RESERVE = "fin_reserve", _("Fin de réserve")
    MINIMUM = "minimum", _("Au minimum")


class LieuRecharge(models.TextChoices):
    DOMICILE = "domicile", _("Domicile")
    TRAVAIL = "travail", _("Travail")
    BORNE_PUBLIQUE = "borne", _("Borne publique (AC)")
    BORNE_RAPIDE = "rapide", _("Borne rapide (DC)")


class Plein(models.Model):
    """Plein de carburant ou recharge électrique (carburant « electricite », API « recharges »)."""
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="pleins")
    date = models.DateField(_("Date"), default=date.today)
    kilometrage = models.PositiveIntegerField(_("Kilométrage"))
    quantite = models.DecimalField(_("Quantité (litres, kWh ou kg)"), max_digits=8, decimal_places=2,
                                   validators=[MinValueValidator(0)])
    montant = models.DecimalField(_("Montant payé TVAC"), max_digits=10, decimal_places=2,
                                  validators=[MinValueValidator(0)])
    niveau_restant = models.CharField(_("Carburant restant"), max_length=12, choices=NiveauCarburant.choices,
                                      blank=True)
    # Recharge électrique
    lieu_recharge = models.CharField(_("Lieu de recharge"), max_length=10, choices=LieuRecharge.choices, blank=True)
    plein_complet = models.BooleanField(_("Plein complet"), default=True,
                                        help_text=_("Nécessaire pour calculer la consommation."))
    carburant = models.CharField(_("Carburant"), max_length=20, choices=Carburant.choices, blank=True)
    # Déduit du carburant (compatibilité) : recharge électrique
    electrique = models.BooleanField(_("Recharge électrique"), default=False, editable=False)
    station = models.CharField(_("Station"), max_length=120, blank=True)
    # Pays de la station et TVA (taux du pays, modifiable) : montant TVAC ventilé en HTVA + TVA
    pays = models.CharField(_("Pays de la station"), max_length=2, blank=True)
    taux_tva = models.DecimalField(_("Taux de TVA (%)"), max_digits=5, decimal_places=2, null=True, blank=True,
                                   validators=[MinValueValidator(0)])
    montant_htva = models.DecimalField(_("Montant HTVA"), max_digits=10, decimal_places=2, null=True, blank=True,
                                       editable=False)
    montant_tva = models.DecimalField(_("TVA"), max_digits=10, decimal_places=2, null=True, blank=True,
                                      editable=False)
    ticket = models.ImageField(_("Photo du ticket"), upload_to=chemin_ticket, null=True, blank=True)
    remarques = models.TextField(_("Remarques"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Plein")
        verbose_name_plural = _("Pleins")
        ordering = ["-date", "-kilometrage"]

    def save(self, *args, **kwargs):
        if not self.carburant:
            self.carburant = CARBURANT_PAR_ENERGIE.get(self.vehicule.energie, Carburant.SP95)
        self.electrique = self.carburant == Carburant.ELECTRICITE
        from .tva import taux_tva, ventiler
        if not self.pays:
            self.pays = self.vehicule.pays_immatriculation or "BE"
        if self.taux_tva is None:
            self.taux_tva = taux_tva(self.pays)
        self.montant_htva, self.montant_tva = ventiler(self.montant, self.taux_tva)
        super().save(*args, **kwargs)

    @property
    def unite(self):
        return unite_carburant(self.carburant)

    @property
    def prix_unitaire(self):
        return (self.montant / self.quantite).quantize(Decimal("0.001")) if self.quantite else None


class TypeEntretien(models.TextChoices):
    REVISION = "revision", _("Révision / entretien périodique")
    VIDANGE = "vidange", _("Vidange")
    PNEUS = "pneus", _("Pneus")
    FREINS = "freins", _("Freins")
    DISTRIBUTION = "distribution", _("Distribution")
    BATTERIE = "batterie", _("Batterie")
    CLIMATISATION = "climatisation", _("Climatisation")
    CONTROLE_TECHNIQUE = "controle_technique", _("Contrôle technique")
    CARROSSERIE = "carrosserie", _("Carrosserie")
    REPARATION = "reparation", _("Réparation")
    AUTRE = "autre", _("Autre")


class Entretien(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="entretiens")
    date = models.DateField(_("Date"), default=date.today)
    kilometrage = models.PositiveIntegerField(_("Kilométrage"), null=True, blank=True)
    type = models.CharField(_("Type"), max_length=20, choices=TypeEntretien.choices, default=TypeEntretien.REVISION)
    description = models.CharField(_("Description"), max_length=255, blank=True)
    garage = models.CharField(_("Garage"), max_length=120, blank=True)
    # Pièces et main-d'œuvre TVAC (facultatifs) : s'ils sont indiqués, le montant est leur total
    pieces = models.DecimalField(_("Pièces TVAC"), max_digits=10, decimal_places=2, null=True, blank=True,
                                 validators=[MinValueValidator(0)])
    main_oeuvre = models.DecimalField(_("Main-d'œuvre TVAC"), max_digits=10, decimal_places=2, null=True, blank=True,
                                      validators=[MinValueValidator(0)])
    montant = models.DecimalField(_("Montant TVAC"), max_digits=10, decimal_places=2, default=ZERO,
                                  validators=[MinValueValidator(0)])
    facture = models.FileField(_("Facture"), upload_to=chemin_facture, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Entretien")
        verbose_name_plural = _("Entretiens")
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        if self.pieces is not None or self.main_oeuvre is not None:
            self.montant = Decimal(self.pieces or 0) + Decimal(self.main_oeuvre or 0)
        super().save(*args, **kwargs)


class TypeDocument(models.TextChoices):
    ASSURANCE = "assurance", _("Assurance")
    CONTROLE_TECHNIQUE = "controle_technique", _("Contrôle technique")
    CARTE_GRISE = "carte_grise", _("Certificat d'immatriculation (carte grise)")
    COC = "coc", _("Certificat de conformité (COC)")
    FACTURE_ACHAT = "facture_achat", _("Facture d'achat")
    AUTRE = "autre", _("Autre")


class Document(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="documents")
    type = models.CharField(_("Type"), max_length=20, choices=TypeDocument.choices)
    titre = models.CharField(_("Titre"), max_length=120, blank=True)
    numero = models.CharField(_("Numéro (police, certificat…)"), max_length=60, blank=True)
    organisme = models.CharField(_("Organisme (assureur, centre…)"), max_length=120, blank=True)
    date_debut = models.DateField(_("Valable du"), null=True, blank=True)
    date_expiration = models.DateField(_("Valable jusqu'au"), null=True, blank=True)
    montant = models.DecimalField(_("Montant (prime, redevance…)"), max_digits=10, decimal_places=2,
                                  null=True, blank=True, validators=[MinValueValidator(0)])
    # Assurance : prime payée par mois ou par an (vide : montant payé une fois, à la date de début)
    mode_paiement = models.CharField(_("Mode de paiement"), max_length=8, blank=True,
                                     choices=[("mensuel", _("Mensuel")), ("annuel", _("Annuel"))])
    fichier = models.FileField(_("Fichier"), upload_to=chemin_document, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        ordering = ["type", "-date_expiration"]

    @property
    def prime_annuelle(self):
        """Mensuel : montant × 12 ; annuel : le montant ; sinon None."""
        if self.montant is None or not self.mode_paiement:
            return None
        return (Decimal(self.montant) * 12).quantize(Decimal("0.01")) if self.mode_paiement == "mensuel" \
            else Decimal(self.montant)

    @property
    def prime_mensuelle(self):
        """Annuel : montant ÷ 12 ; mensuel : le montant ; sinon None."""
        if self.montant is None or not self.mode_paiement:
            return None
        return Decimal(self.montant) if self.mode_paiement == "mensuel" \
            else (Decimal(self.montant) / 12).quantize(Decimal("0.01"))


class Rappel(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="rappels")
    libelle = models.CharField(_("Libellé"), max_length=120)
    type_entretien = models.CharField(_("Type d'entretien"), max_length=20, choices=TypeEntretien.choices, blank=True)
    echeance_date = models.DateField(_("Échéance (date)"), null=True, blank=True)
    echeance_km = models.PositiveIntegerField(_("Échéance (kilométrage)"), null=True, blank=True)
    intervalle_mois = models.PositiveSmallIntegerField(_("Répéter tous les (mois)"), null=True, blank=True)
    intervalle_km = models.PositiveIntegerField(_("Répéter tous les (km)"), null=True, blank=True)
    document = models.OneToOneField(Document, on_delete=models.CASCADE, null=True, blank=True, related_name="rappel")
    actif = models.BooleanField(_("Actif"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Rappel")
        verbose_name_plural = _("Rappels")
        ordering = ["echeance_date", "echeance_km"]


class CategorieDepense(models.TextChoices):
    TAXE = "taxe", _("Taxe de circulation / vignette")
    ASSURANCE = "assurance", _("Assurance")
    PARKING = "parking", _("Parking / péage")
    LAVAGE = "lavage", _("Lavage")
    ACCESSOIRE = "accessoire", _("Accessoires / équipements")
    AMENDE = "amende", _("Amende")
    FINANCEMENT = "financement", _("Crédit / leasing")
    AUTRE = "autre", _("Autre")


class Depense(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="depenses")
    date = models.DateField(_("Date"), default=date.today)
    categorie = models.CharField(_("Catégorie"), max_length=15, choices=CategorieDepense.choices)
    libelle = models.CharField(_("Libellé"), max_length=120, blank=True)
    montant = models.DecimalField(_("Montant TVAC"), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Dépense")
        verbose_name_plural = _("Dépenses")
        ordering = ["-date"]



class CompteParticulier(Utilisateur):
    """Comptes de l'application (rôle « particulier ») pour l'admin Django – modèle proxy, sans table."""

    class Meta:
        proxy = True
        verbose_name = _("Compte particulier")
        verbose_name_plural = _("Comptes particuliers")


# ==================================================================
# ABONNEMENTS (formules de l'application) – voir particulier/abonnements.py
# ==================================================================
class Formule(models.TextChoices):
    GRATUIT = "gratuit", _("Gratuit")
    BRONZE = "bronze", _("Bronze")
    SILVER = "silver", _("Silver")
    GOLD = "gold", _("Gold")


class SourceAbonnement(models.TextChoices):
    AUCUNE = "", _("—")
    ADMIN = "admin", _("Administration")
    APPLE = "apple", _("App Store")
    GOOGLE = "google", _("Google Play")
    TEST = "test", _("Achat de test (développement)")


class AbonnementParticulier(models.Model):
    """Formule d'un compte particulier. Sans ligne, ou échue (date_fin passée) : formule gratuite."""
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name="abonnement_particulier")
    formule = models.CharField(_("Formule"), max_length=10, choices=Formule.choices, default=Formule.GRATUIT)
    date_fin = models.DateTimeField(_("Fin de validité"), null=True, blank=True,
                                    help_text=_("Vide : sans limite de durée (attribution par l'administration)."))
    source = models.CharField(_("Source"), max_length=10, choices=SourceAbonnement.choices, blank=True, default="")
    produit = models.CharField(_("Produit (store)"), max_length=120, blank=True)
    reference_store = models.CharField(_("Référence store"), max_length=255, null=True, blank=True, unique=True,
                                       help_text=_("originalTransactionId (Apple) ou purchaseToken (Google)."))
    environnement = models.CharField(_("Environnement"), max_length=20, blank=True,
                                     help_text=_("Production ou Sandbox (achats de test des stores)."))
    renouvellement_auto = models.BooleanField(_("Renouvellement automatique"), default=False)
    note = models.CharField(_("Note"), max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Abonnement")
        verbose_name_plural = _("Abonnements")

    def __str__(self):
        return f"{self.utilisateur_id} – {self.get_formule_display()}"


class UniteDistance(models.TextChoices):
    KM = "km", _("Kilomètres")
    MI = "mi", _("Miles")


class UniteVolume(models.TextChoices):
    L = "L", _("Litres")
    GAL_US = "gal_us", _("Gallons US")
    GAL_UK = "gal_uk", _("Gallons impériaux (UK)")


# Pays en miles (et gallons US) ; Royaume-Uni : miles, carburant en litres (consommation en mpg impériaux)
PAYS_MILES = {"US", "GB", "LR", "MM", "PR", "GU", "VI", "AS", "MP", "UM"}
PAYS_GALLONS_US = {"US", "LR", "PR", "GU", "VI", "AS", "MP", "UM"}


def unites_par_defaut(pays):
    """(distance, volume) d'après le pays de l'utilisateur."""
    pays = (pays or "").upper()
    return ("mi" if pays in PAYS_MILES else "km", "gal_us" if pays in PAYS_GALLONS_US else "L")


class PreferencesParticulier(models.Model):
    """Réglages de l'application d'un particulier (langue, pays par défaut, unités).
    Les données restent enregistrées en km et en litres : l'application convertit à l'affichage et à la saisie."""
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name="preferences_particulier")
    langue = models.CharField(_("Langue"), max_length=5, choices=settings.LANGUAGES, default="fr")
    pays_defaut = models.CharField(_("Pays d'immatriculation par défaut"), max_length=2, default="BE")
    unite_distance = models.CharField(_("Distances"), max_length=2, choices=UniteDistance.choices, default="km")
    unite_volume = models.CharField(_("Volumes de carburant"), max_length=6, choices=UniteVolume.choices, default="L")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Préférences")
        verbose_name_plural = _("Préférences")

    def __str__(self):
        return f"{self.utilisateur_id} – {self.langue}"


# ==================================================================
# TYPE D'ACHAT (formule Bronze minimum) : comptant, prêt, leasing, renting
# ==================================================================
class TypeAchat(models.TextChoices):
    COMPTANT = "comptant", _("Comptant")
    PRET = "pret", _("Prêt (crédit auto)")
    LEASING = "leasing", _("Leasing avec option d'achat (LOA)")
    RENTING = "renting", _("Renting / location longue durée (LLD)")


class Financement(models.Model):
    """Comment le véhicule est payé ; les mensualités entrent dans les coûts (voir calculs.financement)."""
    vehicule = models.OneToOneField(Vehicule, on_delete=models.CASCADE, related_name="financement")
    type_achat = models.CharField(_("Type d'achat"), max_length=10, choices=TypeAchat.choices,
                                  default=TypeAchat.COMPTANT)
    organisme = models.CharField(_("Organisme (banque, société de leasing)"), max_length=120, blank=True)
    date_debut = models.DateField(_("Début du contrat"), null=True, blank=True)
    duree_mois = models.PositiveSmallIntegerField(_("Durée (mois)"), null=True, blank=True)
    # Prêt
    apport = models.DecimalField(_("Apport"), max_digits=12, decimal_places=2, null=True, blank=True,
                                 validators=[MinValueValidator(0)])
    montant_emprunte = models.DecimalField(_("Montant emprunté"), max_digits=12, decimal_places=2, null=True,
                                           blank=True, validators=[MinValueValidator(0)])
    taux_annuel = models.DecimalField(_("Taux annuel (TAEG, %)"), max_digits=5, decimal_places=2, null=True,
                                      blank=True, validators=[MinValueValidator(0)])
    # Mensualité (prêt : calculée si vide) ; leasing / renting : loyer mensuel
    mensualite = models.DecimalField(_("Mensualité"), max_digits=10, decimal_places=2, null=True, blank=True,
                                     validators=[MinValueValidator(0)])
    # Leasing / renting
    premier_loyer = models.DecimalField(_("Premier loyer majoré / acompte"), max_digits=12, decimal_places=2,
                                        null=True, blank=True, validators=[MinValueValidator(0)])
    valeur_residuelle = models.DecimalField(_("Option d'achat (valeur résiduelle)"), max_digits=12,
                                            decimal_places=2, null=True, blank=True,
                                            validators=[MinValueValidator(0)])
    option_levee = models.BooleanField(_("Option d'achat levée"), default=False)
    km_annuels = models.PositiveIntegerField(_("Kilométrage autorisé par an"), null=True, blank=True)
    prix_km_supplementaire = models.DecimalField(_("Prix du km supplémentaire"), max_digits=6, decimal_places=3,
                                                 null=True, blank=True, validators=[MinValueValidator(0)])
    services_inclus = models.CharField(_("Services inclus (entretien, assurance, pneus…)"), max_length=255,
                                       blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Type d'achat")
        verbose_name_plural = _("Types d'achat")

    def __str__(self):
        return f"{self.vehicule} – {self.get_type_achat_display()}"


class StatutFiscal(models.TextChoices):
    PARTICULIER = "particulier", _("Particulier (usage privé)")
    INDEPENDANT = "independant", _("Indépendant / profession libérale")
    SOCIETE = "societe", _("Société (voiture de société)")


class ProfilFiscal(models.Model):
    """Données de déductibilité d'un véhicule (règles du pays d'immatriculation, voir deductibilite.py)."""
    vehicule = models.OneToOneField(Vehicule, on_delete=models.CASCADE, related_name="profil_fiscal")
    statut = models.CharField(_("Statut"), max_length=12, choices=StatutFiscal.choices,
                              default=StatutFiscal.INDEPENDANT)
    usage_pro = models.PositiveSmallIntegerField(_("Usage professionnel (%)"), default=100,
                                                 validators=[MaxValueValidator(100)])
    co2 = models.PositiveSmallIntegerField(_("Émissions CO2 (g/km, WLTP)"), null=True, blank=True)
    date_commande = models.DateField(_("Date de commande / signature du contrat"), null=True, blank=True)
    duree_amortissement = models.PositiveSmallIntegerField(_("Amortissement (années)"), default=5,
                                                           validators=[MinValueValidator(1), MaxValueValidator(10)])
    taux_tva_manuel = models.DecimalField(_("TVA déductible imposée (%)"), max_digits=5, decimal_places=2,
                                          null=True, blank=True,
                                          validators=[MinValueValidator(0), MaxValueValidator(100)])
    taux_impot_manuel = models.DecimalField(_("Frais déductibles imposés (%)"), max_digits=5, decimal_places=2,
                                            null=True, blank=True,
                                            validators=[MinValueValidator(0), MaxValueValidator(120)])
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Profil fiscal")
        verbose_name_plural = _("Profils fiscaux")


def types_maintenance():
    """Types de maintenance de dBSolution (mêmes codes et libellés, donc mêmes traductions)."""
    from maintenance.models import Maintenance
    return Maintenance.TypeMaintenance.choices


# Familles des types de maintenance (regroupement du choix dans l'application ; libellés traduits par l'app)
FAMILLES_MAINTENANCE = {
    "entretien": ["checkup", "entretien", "niveaux", "LUBRIFICATION", "RODAGE", "checkup_track",
                  "BOUGIES_ALLUMAGE", "BOUGIES_PRECHAUFFAGE"],
    "moteur": ["ADMISSION", "TURBO", "MONTAGE_TURBO", "REMPLACEMENT_MOTEUR", "COURROIE_DISTRI", "CHAINE_DISTRI",
               "ELECTRONIQUE_MOTEUR", "COURROIE_ACCESS", "REFROIDISSEMENT", "ALLUMAGE", "INJECTION", "CULASSE",
               "BAS_MOTEUR", "BANC_PUISSANCE", "PC_MOTEUR", "METROLOGIE_MOTEUR", "CASSE_MOTEUR"],
    "transmission": ["remplacement_boite", "BOITE", "BOITE_AUTO", "EMBRAYAGE", "CARDAN", "ARBRE_TRANSMISSION",
                     "BOITE_TRANSFERT", "remplacement_bte_auto", "CASSE_BOITE"],
    "freinage": ["freins", "ABS", "NETTOYAGE_FREINS", "TAMBOURS", "FREIN_MAIN", "FREIN_MAIN_HYDRAULIQUE",
                 "RENOVATION_MACHOIRES"],
    "roues": ["pneus", "GEOMETRIE", "GEOMETRIE_COURSE", "ROULEMENT", "CREVAISON", "silent_bloc",
              "SUSPENSION_ORIGINE", "SUSPENSION_SPORT", "PC_AIR_JACK"],
    "echappement": ["ECHAPPEMENT", "PC_ECHAPPEMENT"],          # + tous les codes ECH_… et ADBLUE_…
    "electricite": ["BATTERIE", "ALTERNATEUR", "DEMARREUR", "ECLAIRAGE", "FUSIBLES", "BOITIER_ELECTRONIQUE",
                    "AIDE_STATIONNEMENT", "PC_CABLAGE", "PC_BOITIER"],
    "confort": ["CLIMATISATION", "VENTILATION", "ESSUYAGE"],
    "securite": ["ESP", "SECURITE", "PC_ARCEAU", "PC_EXTINCTEUR", "PC_SIEGES"],
    "carrosserie": ["nettoyage_exterieur", "nettoyage_interieur", "CARROSSERIE_INTERNE", "POLISH", "DECONTAMINATION",
                    "CIRE", "CERAMIQUE", "VITRAGE", "ACCIDENT", "PC_DEMONTAGE"],
}
_FAMILLE_PAR_TYPE = {code: f for f, codes in FAMILLES_MAINTENANCE.items() for code in codes}


def famille_maintenance(code):
    if code.startswith(("ECH_", "ADBLUE_")):
        return "echappement"
    return _FAMILLE_PAR_TYPE.get(code, "autres")


class MaintenanceParticulier(models.Model):
    """
    Maintenance faite par un garage (même principe que les maintenances externes de dBSolution) :
    pièces et main-d'œuvre HTVA séparées, TVA du pays, montants calculés pour les statistiques.
    Formule Bronze minimum.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="maintenances")
    type_maintenance = models.CharField(_("Type de maintenance"), max_length=50, choices=types_maintenance,
                                        default="entretien")
    date = models.DateField(_("Date de la facture"), default=date.today)
    garage = models.CharField(_("Garage"), max_length=120, blank=True)
    numero_facture = models.CharField(_("Numéro de facture du garage"), max_length=50, blank=True)
    kilometrage = models.PositiveIntegerField(_("Kilométrage"), null=True, blank=True)
    pays = models.CharField(_("Pays de la TVA"), max_length=2, blank=True)
    taux_tva = models.DecimalField(_("Taux de TVA (%)"), max_digits=5, decimal_places=2, null=True, blank=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)])
    pieces_htva = models.DecimalField(_("Pièces HTVA (€)"), max_digits=10, decimal_places=2, default=ZERO,
                                      validators=[MinValueValidator(0)])
    main_oeuvre_htva = models.DecimalField(_("Main-d'œuvre HTVA (€)"), max_digits=10, decimal_places=2,
                                           default=ZERO, validators=[MinValueValidator(0)])
    # Montants calculés (listes, statistiques, TVA)
    tva_pieces = models.DecimalField(_("TVA pièces (€)"), max_digits=10, decimal_places=2, default=ZERO, editable=False)
    tva_main_oeuvre = models.DecimalField(_("TVA main-d'œuvre (€)"), max_digits=10, decimal_places=2, default=ZERO,
                                          editable=False)
    total_pieces_tvac = models.DecimalField(_("Total pièces TVAC (€)"), max_digits=10, decimal_places=2,
                                            default=ZERO, editable=False)
    total_main_oeuvre_tvac = models.DecimalField(_("Total main-d'œuvre TVAC (€)"), max_digits=10, decimal_places=2,
                                                 default=ZERO, editable=False)
    total_htva = models.DecimalField(_("Total HTVA (€)"), max_digits=10, decimal_places=2, default=ZERO, editable=False)
    total_tva = models.DecimalField(_("Total TVA (€)"), max_digits=10, decimal_places=2, default=ZERO, editable=False)
    total_tvac = models.DecimalField(_("Total TVAC (€)"), max_digits=10, decimal_places=2, default=ZERO, editable=False)
    description = models.TextField(_("Description des travaux"), blank=True)
    facture = models.FileField(_("Facture"), upload_to=chemin_facture, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Maintenance (garage)")
        verbose_name_plural = _("Maintenances (garage)")
        ordering = ["-date", "-created_at"]

    def calculer(self):
        from decimal import ROUND_HALF_UP
        from .tva import taux_tva
        arrondi = lambda v: Decimal(v or 0).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)  # noqa: E731
        if not self.pays:
            self.pays = (self.vehicule.pays_immatriculation or "").upper()
        if self.taux_tva is None:
            self.taux_tva = taux_tva(self.pays) or ZERO
        taux = Decimal(self.taux_tva) / Decimal(100)
        self.pieces_htva = arrondi(self.pieces_htva)
        self.main_oeuvre_htva = arrondi(self.main_oeuvre_htva)
        self.tva_pieces = arrondi(self.pieces_htva * taux)
        self.tva_main_oeuvre = arrondi(self.main_oeuvre_htva * taux)
        self.total_pieces_tvac = arrondi(self.pieces_htva + self.tva_pieces)
        self.total_main_oeuvre_tvac = arrondi(self.main_oeuvre_htva + self.tva_main_oeuvre)
        self.total_htva = arrondi(self.pieces_htva + self.main_oeuvre_htva)
        self.total_tva = arrondi(self.tva_pieces + self.tva_main_oeuvre)
        self.total_tvac = arrondi(self.total_htva + self.total_tva)

    def save(self, *args, **kwargs):
        self.calculer()
        super().save(*args, **kwargs)

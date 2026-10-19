import base64
import re
import uuid
from io import BytesIO
import pyotp
import qrcode
from core.iban import normaliser_iban, validate_iban
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework.exceptions import ValidationError
from adresse.models import Adresse
from societe.models import Societe
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError




class UtilisateurManager(BaseUserManager):
    def validate_password(self, password):
        if not password:
            raise ValidationError("Le mot de passe est obligatoire.")
        if len(password) < 12:
            raise ValidationError("Le mot de passe doit contenir au moins 12 caractères.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Le mot de passe doit contenir au moins une majuscule.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Le mot de passe doit contenir au moins une minuscule.")
        if not re.search(r"\d", password):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")

        if password:
            self.validate_password(password)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Récupère et supprime les FK pour éviter les erreurs d'initialisation
        societe = extra_fields.pop('societe', None)
        adresse = extra_fields.pop('adresse', None)

        if not societe:
            raise ValueError("La société est obligatoire pour un superutilisateur.")
        if not adresse:
            raise ValueError("L'adresse est obligatoire pour un superutilisateur.")
        if not extra_fields.get('date_naissance'):
            raise ValueError("La date de naissance est obligatoire.")

        if password:
            self.validate_password(password)


        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.model(
            email=self.normalize_email(email),
            societe=societe,
            adresse=adresse,
            **extra_fields
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    ROLE_CHOICES = [
        ('apprentis', _('Apprenti')),
        ('mecanicien', _('Mécanicien')),
        ('magasinier', _('Magasinier')),
        ('carrossier', _('Carrossier')),
        ('chef_mecanicien', _('Chef Mécanicien')),
        ('instructeur', _('Instructeur')),
        ('instructeur externe', _('Instructeur Externe')),
        ('vendeur', _('Vendeur')),
        ('comptable', _('Comptable')),
        ('direction', _('Direction')),
    ]

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default='apprentis',
        verbose_name=_("Rôle")
    )

    adresse = models.ForeignKey(
        Adresse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='utilisateurs'
    )

    societe = models.ForeignKey(
        Societe,
        on_delete=models.PROTECT,
        related_name="utilisateurs",
        null=True,
        blank=True,
        to_field="id_societe"
    )

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    numero_registre_national = models.CharField(max_length=100, blank=True, null=True)
    numero_compte_bancaire = models.CharField(max_length=100, blank=True, null=True, validators=[validate_iban],
                                              verbose_name=_("IBAN"))

    email = models.EmailField(unique=True, blank=True, null=True)
    email_entreprise = models.EmailField(unique=True, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)


    schema_name = models.CharField(max_length=100, blank=True, null=True)



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    # TOTP
    totp_secret = models.CharField(max_length=50, blank=True, null=True, editable=False)
    totp_enabled = models.BooleanField(default=False)

    objects = UtilisateurManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilisateurs_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='utilisateurs_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    salaire_brut_heure = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Salaire brut / heure")
    )

    class Meta:
        app_label = 'utilisateurs'



    def generate_totp_secret(self):
        """
        Génère un secret TOTP uniquement s'il n'existe pas encore.

        Retourne le secret afin de pouvoir l'utiliser immédiatement
        dans la vue d'activation.
        """
        if not self.totp_secret:
            self.totp_secret = pyotp.random_base32()

            self.save(
                update_fields=[
                    "totp_secret",
                    "updated_at",
                ]
            )

        return self.totp_secret

    def get_totp_uri(self):
        """
        Génère l'URI utilisée par Google Authenticator,
        Microsoft Authenticator, Authy, etc.
        """
        if not self.totp_secret:
            self.generate_totp_secret()

        issuer = (
            self.societe.nom
            if self.societe
            else "CarsCosts"
        )

        identifiant = (
                self.email
                or self.email_entreprise
                or str(self.pk)
        )

        return pyotp.TOTP(
            self.totp_secret
        ).provisioning_uri(
            name=identifiant,
            issuer_name=issuer,
        )

    def verify_totp(self, token):
        """
        Vérifie un code TOTP à six chiffres.

        valid_window=1 accepte un léger décalage temporel
        entre le serveur et le téléphone.
        """
        if not self.totp_secret or not token:
            return False

        token = str(token).strip().replace(" ", "")

        if not token.isdigit() or len(token) != 6:
            return False

        totp = pyotp.TOTP(self.totp_secret)

        return totp.verify(
            token,
            valid_window=1,
        )

    def generate_qr_code(self):
        """
        Génère le QR code TOTP au format base64.
        """
        totp_uri = self.get_totp_uri()

        qr = qrcode.make(totp_uri)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        return base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")



    def enable_totp(self, token):
        """
        Vérifie le premier code saisi et active le TOTP.

        Retourne True si l'activation réussit.
        """
        if not self.verify_totp(token):
            return False

        if not self.totp_enabled:
            self.totp_enabled = True

            self.save(
                update_fields=[
                    "totp_enabled",
                    "updated_at",
                ]
            )

        return True

    def disable_totp(self):
        """
        Désactive complètement le TOTP et supprime l'ancien secret.
        """
        self.totp_enabled = False
        self.totp_secret = None

        self.save(
            update_fields=[
                "totp_enabled",
                "totp_secret",
                "updated_at",
            ]
        )

    def verify_totp(self, token):
        if not self.totp_secret:
            return False
        totp = pyotp.TOTP(self.totp_secret)
        return totp.verify(token, valid_window=1)

    def generate_qr_code(self):
        totp_uri = pyotp.TOTP(self.totp_secret).provisioning_uri(
            name=self.email,
            issuer_name=self.societe.name
        )
        qr = qrcode.make(totp_uri)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        return qr_base64

    def clean(self):
        super().clean()

        if not self.societe:
            return

        max_users = self.societe.max_utilisateurs

        if max_users is None:
            return

        utilisateurs_existants = Utilisateur.objects.filter(
            societe=self.societe
        )

        if self.pk:
            utilisateurs_existants = utilisateurs_existants.exclude(pk=self.pk)

        if utilisateurs_existants.count() >= max_users:
            raise DjangoValidationError({
                "societe": _(
                    "La limite maximale d'utilisateurs pour cette société est atteinte."
                )
            })

    def save(self, *args, **kwargs):
        # IBAN stocké sans espaces, en majuscules (affiché en groupes de 4 via |format_iban)
        if self.numero_compte_bancaire:
            self.numero_compte_bancaire = normaliser_iban(self.numero_compte_bancaire) or None
        super().save(*args, **kwargs)

    @property
    def iban_formate(self):
        from core.iban import formater_iban
        return formater_iban(self.numero_compte_bancaire) if self.numero_compte_bancaire else ""

    @property
    def iban_valide(self):
        from core.iban import erreur_iban
        return bool(self.numero_compte_bancaire) and erreur_iban(self.numero_compte_bancaire) is None

    def __str__(self):
        return f"{self.prenom} {self.nom}"






class Mecanicien(Utilisateur):
    class Meta:
        proxy = True  # Très important : pas de table supplémentaire, juste une vue "proxy"

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_role_display()}"





class UserLog(models.Model):
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    action = models.CharField(max_length=255)

    date_action = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date_action"]




class StatutTravailleur(models.TextChoices):
    EMPLOYE = "employe", _("Employé")
    OUVRIER = "ouvrier", _("Ouvrier")


class CommissionParitaire(models.TextChoices):
    CP112 = "CP112", _("CP 112 – Entreprises de garage (ouvriers)")
    CP200 = "CP200", _("CP 200 – Employés (CPAE)")
    RMMMG = "RMMMG", _("Salaire minimum national (CP 100 / RMMMG)")
    AUTRE = "AUTRE", _("Autre (taux horaire manuel)")


class ClasseCP200(models.TextChoices):
    A = "A", _("Classe A – fonctions exécutives")
    B = "B", _("Classe B – fonctions de support")
    C = "C", _("Classe C – fonctions de gestion")
    D = "D", _("Classe D – fonctions consultatives")


class MajorationHeuresSup(models.IntegerChoices):
    VINGT = 20, _("20 %")
    CINQUANTE = 50, _("50 %")
    CENT = 100, _("100 % (dimanche / jour férié)")


class Carburant(models.TextChoices):
    ESSENCE = "essence", _("Essence")
    DIESEL = "diesel", _("Diesel")
    LPG = "lpg", _("LPG")
    CNG = "cng", _("CNG")
    ELECTRIQUE = "electrique", _("Électrique")


class CategorieCP112(models.TextChoices):
    A1 = "A1", _("A1 – 16,46 €/h")
    A2 = "A2", _("A1.1 / A2 – 17,20 €/h")
    A2_1 = "A2_1", _("A1.2 / A2.1 – 18,06 €/h")
    B1 = "B1", _("A2.2 / B1 – 18,92 €/h")
    B2 = "B2", _("B2 – 19,95 €/h")
    C1 = "C1", _("C1 – 20,98 €/h")
    C2 = "C2", _("C2 – 22,02 €/h")
    D1 = "D1", _("D1 – 23,05 €/h")
    D2 = "D2", _("D2 – 24,08 €/h")


class SituationFamiliale(models.TextChoices):
    ISOLE = "isole", _("Isolé")
    MARIE_DEUX_REVENUS = "marie_deux_revenus", _("Marié / cohabitant légal – conjoint avec revenus")
    MARIE_UN_REVENU = "marie_un_revenu", _("Marié / cohabitant légal – conjoint sans revenus")


class PaieUtilisateur(models.Model):
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="paies",
        verbose_name=_("Utilisateur")
    )

    mois = models.PositiveSmallIntegerField(
        verbose_name=_("Mois")
    )

    annee = models.PositiveIntegerField(
        verbose_name=_("Année")
    )

    salaire_brut_heure = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Salaire brut / heure")
    )
    salaire_brut_mensuel = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Salaire mensuel")
    )

    salaire_brut_mensuel_employeur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Salaire brut employeur")
    )

    nombre_jours_preste = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Nombre de jours prestés")
    )

    nombre_heures_preste = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name=_("Nombre d'heures prestées")
    )

    taux_charges_patronales = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Taux charges patronales")
    )

    taux_precompte_professionnel = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Taux précompte professionnel")
    )

    taux_onss = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Taux ONSS")
    )

    salaire_net_mois = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Salaire net du mois")
    )

    conges_payes = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Congés payés")
    )

    salaire_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Salaire total")
    )


    # -------------------------
    # STATUT / COMMISSION PARITAIRE
    # -------------------------
    statut_travailleur = models.CharField(
        max_length=10,
        choices=StatutTravailleur.choices,
        default=StatutTravailleur.EMPLOYE,
        verbose_name=_("Statut"),
    )

    commission_paritaire = models.CharField(
        max_length=10,
        choices=CommissionParitaire.choices,
        default=CommissionParitaire.CP112,
        verbose_name=_("Commission paritaire"),
    )

    categorie_cp = models.CharField(
        max_length=10,
        choices=CategorieCP112.choices,
        blank=True,
        default="",
        verbose_name=_("Catégorie (CP 112)"),
        help_text=_("Si une catégorie est choisie, le taux horaire minimum de la CP est appliqué."),
    )

    # -------------------------
    # SITUATION FAMILIALE (précompte)
    # -------------------------
    situation_familiale = models.CharField(
        max_length=25,
        choices=SituationFamiliale.choices,
        default=SituationFamiliale.ISOLE,
        verbose_name=_("Situation familiale"),
    )

    parent_isole = models.BooleanField(
        default=False,
        verbose_name=_("Parent isolé avec enfant(s) à charge"),
    )

    nombre_enfants_charge = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Nombre d'enfants à charge"),
    )

    nombre_enfants_handicapes = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Dont enfants handicapés"),
        help_text=_("Un enfant handicapé compte pour deux."),
    )

    beneficiaire_handicape = models.BooleanField(
        default=False,
        verbose_name=_("Travailleur en situation de handicap"),
    )

    conjoint_handicape = models.BooleanField(
        default=False,
        verbose_name=_("Conjoint en situation de handicap"),
    )

    # -------------------------
    # CP 200 (employés)
    # -------------------------
    classe_cp200 = models.CharField(
        max_length=1, choices=ClasseCP200.choices, blank=True, default="",
        verbose_name=_("Classe de fonction (CP 200)"),
    )
    annees_experience = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("Années d'expérience (CP 200)"),
    )
    anciennete_un_an = models.BooleanField(
        default=False,
        verbose_name=_("Au moins 1 an dans l'entreprise (barème II CP 200)"),
    )

    # -------------------------
    # RÉGIME DE TRAVAIL
    # -------------------------
    regime_travail = models.DecimalField(
        max_digits=5, decimal_places=2, default=100,
        verbose_name=_("Régime de travail (% d'un temps plein)"),
        help_text=_("100 = temps plein, 50 = mi-temps… Proratise le bonus à l'emploi et la réduction structurelle."),
    )

    # -------------------------
    # HEURES SUPPLÉMENTAIRES
    # -------------------------
    heures_supplementaires = models.DecimalField(
        max_digits=6, decimal_places=2, default=0,
        verbose_name=_("Heures supplémentaires"),
        help_text=_("Réduction de précompte limitée à 180 h par an."),
    )
    majoration_heures_sup = models.PositiveSmallIntegerField(
        choices=MajorationHeuresSup.choices, default=MajorationHeuresSup.CINQUANTE,
        verbose_name=_("Sursalaire des heures supplémentaires"),
    )

    # -------------------------
    # PÉCULE DE VACANCES / RÉDUCTIONS
    # -------------------------
    double_pecule_ce_mois = models.BooleanField(
        default=False,
        verbose_name=_("Payer le double pécule de vacances ce mois (employés)"),
    )
    reduction_groupe_cible = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name=_("Réduction groupe-cible (montant mensuel)"),
        help_text=_("Ex. premiers engagements, travailleurs âgés… selon votre région / ONSS."),
    )

    # -------------------------
    # AVANTAGES EN NATURE
    # -------------------------
    atn_autres = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name=_("Autres avantages en nature (montant mensuel)"),
        help_text=_("GSM, PC, internet, logement, chauffage…"),
    )
    voiture_societe = models.BooleanField(default=False, verbose_name=_("Voiture de société"))
    voiture_valeur_catalogue = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Valeur catalogue (TVAC, options comprises)"),
    )
    voiture_co2 = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name=_("Émissions CO2 (g/km)"),
    )
    voiture_carburant = models.CharField(
        max_length=12, choices=Carburant.choices, default=Carburant.DIESEL,
        verbose_name=_("Carburant"),
    )
    voiture_date_immatriculation = models.DateField(
        blank=True, null=True, verbose_name=_("Date de 1re immatriculation"),
    )
    voiture_commandee_apres_07_2023 = models.BooleanField(
        default=False, verbose_name=_("Voiture thermique commandée après le 01/07/2023"),
    )
    voiture_contribution_personnelle = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name=_("Contribution personnelle du travailleur (mensuelle)"),
    )

    # -------------------------
    # RÉSULTATS DU CALCUL
    # -------------------------
    salaire_brut_majore = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Brut majoré (base ONSS)"),
    )

    montant_onss = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("ONSS travailleur"),
    )

    bonus_emploi = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Bonus à l'emploi"),
    )

    salaire_imposable = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Salaire imposable"),
    )

    montant_precompte = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Précompte professionnel"),
    )

    cotisations_patronales = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Cotisations patronales"),
    )
    montant_heures_sup = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Montant heures supplémentaires"),
    )
    atn_voiture = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("ATN voiture de société"),
    )
    atn_total = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Total avantages en nature"),
    )
    csss = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Cotisation spéciale de sécurité sociale"),
    )
    double_pecule_brut = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Double pécule brut"),
    )
    double_pecule_onss = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Double pécule – ONSS"),
    )
    double_pecule_precompte = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Double pécule – précompte"),
    )
    date_paiement = models.DateField(
        blank=True, null=True,
        verbose_name=_("Date de paiement du net"),
    )
    double_pecule_net = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Double pécule net"),
    )
    reduction_structurelle = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Réduction structurelle"),
    )
    cotisations_vacances = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Cotisations / provision vacances (employeur)"),
    )
    cotisation_co2 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("Cotisation de solidarité CO2"),
    )

    # -------------------------
    # CALCUL
    # -------------------------
    def calculer(self):
        """Calcule la paie complète (brut → net, coût employeur)."""
        from datetime import date
        from decimal import Decimal
        from .paie_belgique import calculer_paie, minimum_cp, TAUX_ONSS_TRAVAILLEUR

        fraction = (Decimal(self.regime_travail or 100) / 100) or Decimal("1")

        taux_cp, mensuel_cp = minimum_cp(
            self.commission_paritaire,
            categorie=self.categorie_cp,
            classe=self.classe_cp200,
            experience=self.annees_experience,
            bareme_ii=self.anciennete_un_an,
        )

        # Le taux horaire ne peut pas être inférieur au minimum de la CP
        if taux_cp and (not self.salaire_brut_heure or self.salaire_brut_heure < taux_cp):
            self.salaire_brut_heure = taux_cp

        heures = self.nombre_heures_preste or Decimal("0")
        if heures > 0 and self.salaire_brut_heure:
            self.salaire_brut_mensuel = (heures * self.salaire_brut_heure).quantize(Decimal("0.01"))
        elif mensuel_cp:
            minimum = (mensuel_cp * fraction).quantize(Decimal("0.01"))
            if not self.salaire_brut_mensuel or self.salaire_brut_mensuel < minimum:
                self.salaire_brut_mensuel = minimum

        if not self.salaire_brut_mensuel:
            return None

        if not self.salaire_brut_heure and fraction:
            self.salaire_brut_heure = (
                self.salaire_brut_mensuel / (Decimal("164.67") * fraction)
            ).quantize(Decimal("0.01"))

        voiture = None
        if self.voiture_societe:
            voiture = {
                "valeur_catalogue": self.voiture_valeur_catalogue,
                "co2": self.voiture_co2,
                "carburant": self.voiture_carburant,
                "date_immatriculation": self.voiture_date_immatriculation,
                "commandee_apres_07_2023": self.voiture_commandee_apres_07_2023,
                "contribution_personnelle": self.voiture_contribution_personnelle,
            }

        try:
            date_paie = date(int(self.annee), int(self.mois), 1)
        except (TypeError, ValueError):
            date_paie = date.today()

        r = calculer_paie(
            self.salaire_brut_mensuel,
            statut=self.statut_travailleur,
            taux_patronal=self.taux_charges_patronales,
            situation_familiale=self.situation_familiale,
            nombre_enfants=self.nombre_enfants_charge,
            nombre_enfants_handicapes=self.nombre_enfants_handicapes,
            parent_isole=self.parent_isole,
            beneficiaire_handicape=self.beneficiaire_handicape,
            conjoint_handicape=self.conjoint_handicape,
            regime_travail=self.regime_travail,
            taux_horaire=self.salaire_brut_heure,
            heures_sup=self.heures_supplementaires,
            majoration_heures_sup=self.majoration_heures_sup,
            atn_autres=self.atn_autres,
            voiture=voiture,
            date_paie=date_paie,
            double_pecule=self.double_pecule_ce_mois,
            reduction_groupe_cible=self.reduction_groupe_cible,
        )

        self.montant_heures_sup = r["montant_heures_sup"]
        self.salaire_brut_majore = r["brut_majore"]
        self.taux_onss = TAUX_ONSS_TRAVAILLEUR
        self.montant_onss = r["onss"]
        self.bonus_emploi = r["bonus_emploi"]
        self.atn_voiture = r["atn_voiture"]
        self.atn_total = r["atn_total"]
        self.salaire_imposable = r["imposable"]
        self.montant_precompte = r["precompte"]
        self.taux_precompte_professionnel = r["taux_precompte"]
        self.csss = r["csss"]
        pecule = r["double_pecule"] or {}
        self.double_pecule_brut = pecule.get("brut")
        self.double_pecule_net = pecule.get("net")
        self.double_pecule_onss = pecule.get("onss")
        self.double_pecule_precompte = pecule.get("precompte")
        self.salaire_net_mois = r["net"]
        self.taux_charges_patronales = r["taux_patronal"]
        self.cotisations_patronales = r["cotisations_patronales_nettes"]
        self.reduction_structurelle = r["reduction_structurelle"]
        self.cotisations_vacances = r["vacances_employeur"]
        self.cotisation_co2 = r["cotisation_co2"]
        self.salaire_brut_mensuel_employeur = r["brut_employeur"]
        self.salaire_total = (
            r["brut_employeur"] + (self.conges_payes or Decimal("0"))
        ).quantize(Decimal("0.01"))
        return r

    # -------------------------
    # COMPTABILITÉ
    # -------------------------
    @property
    def net_salaire(self):
        """Net du salaire du mois, hors double pécule."""
        from decimal import Decimal
        return (self.salaire_net_mois or Decimal("0")) - (self.double_pecule_net or Decimal("0"))

    @property
    def net_a_payer(self):
        from decimal import Decimal
        return self.salaire_net_mois or Decimal("0")

    @property
    def est_paye(self):
        return self.date_paiement is not None

    def ecritures_comptables(self, avec_paiement=True):
        from decimal import Decimal
        from .paie_belgique import ecritures_paie

        z = Decimal("0")
        pecule = None
        if self.double_pecule_brut:
            pecule = {
                "brut": self.double_pecule_brut,
                "onss": self.double_pecule_onss or z,
                "precompte": self.double_pecule_precompte or z,
                "net": self.double_pecule_net or z,
            }
        brut = (self.salaire_brut_mensuel or z) + (self.montant_heures_sup or z)
        return ecritures_paie(
            self.statut_travailleur,
            brut,
            cotisations_patronales=self.cotisations_patronales or z,
            cotisation_co2=self.cotisation_co2 or z,
            cotisations_vacances=self.cotisations_vacances or z,
            onss=self.montant_onss or z,
            csss=self.csss or z,
            precompte=self.montant_precompte or z,
            net_salaire=self.net_salaire,
            double_pecule=pecule,
            date_paiement=self.date_paiement if avec_paiement else None,
        )

    def save(self, *args, **kwargs):
        self.calculer()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("utilisateur", "mois", "annee")
        ordering = ["-annee", "-mois"]
        verbose_name = _("Paie utilisateur")
        verbose_name_plural = _("Paies utilisateurs")

    def __str__(self):
        return f"{self.utilisateur} - {self.mois}/{self.annee}"
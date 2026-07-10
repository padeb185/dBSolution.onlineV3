import base64
import re
import uuid
from io import BytesIO
import pyotp
import qrcode
from client_atelier.models import validate_iban
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
    numero_compte_bancaire = models.CharField(max_length=100, blank=True, null=True, validators=[validate_iban])

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
        self.totp_secret = pyotp.random_base32()
        self.save()

    def get_totp_uri(self):
        issuer = self.societe.nom if self.societe else "CarsCosts"
        email = self.email or self.email

        return pyotp.totp.TOTP(self.totp_secret).provisioning_uri(
            name=email,
            issuer_name=issuer
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
        self.full_clean()
        super().save(*args, **kwargs)


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

    salaire_brut_employeur = models.DecimalField(
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

    class Meta:
        unique_together = ("utilisateur", "mois", "annee")
        ordering = ["-annee", "-mois"]
        verbose_name = _("Paie utilisateur")
        verbose_name_plural = _("Paies utilisateurs")

    def __str__(self):
        return f"{self.utilisateur} - {self.mois}/{self.annee}"
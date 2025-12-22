import uuid
import pyotp
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from adresse.models import Adresse
from django_otp.oath import totp
from societe.models import Societe



class UtilisateurManager(BaseUserManager):
    def create_user(self, email_google, password=None, **extra_fields):
        if not email_google:
            raise ValueError("L'email Google doit être défini")
        email_google = self.normalize_email(email_google)
        user = self.model(email_google=email_google, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_google, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email_google, password, **extra_fields)




class Utilisateur(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    adresse = models.ForeignKey(Adresse, on_delete=models.PROTECT, related_name='utilisateurs')
    societe = models.ForeignKey(Societe, on_delete=models.PROTECT, related_name="utilisateurs")

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    email_google = models.EmailField(unique=True)
    email_entreprise = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    salaire_brut_heure = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    nombre_jours_preste = models.PositiveIntegerField(default=0, blank=True, null=True)
    nombre_heures_preste = models.PositiveIntegerField(default=0, blank=True, null=True)
    taux_charges_patronales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # en %
    salaire_majore = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    taux_precompte_professionnel = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # en %
    taux_onss = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # en %
    salaire_net_mois = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salaire_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # TOTP
    totp_secret = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        editable=False,
    )
    totp_enabled = models.BooleanField(default=False)


    objects = UtilisateurManager()

    USERNAME_FIELD = 'email_google'
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

    def get_totp_token(self):
        """Retourne le token TOTP actuel (6 chiffres)"""
        return totp(self.totp_secret, digits=6, step=30, t=int(time.time()))

    def verify_totp(self, token):
        """Vérifie un token fourni par l'utilisateur"""
        return str(self.get_totp_token()) == str(token)

    def generate_totp_secret(self):
        self.totp_secret = pyotp.random_base32()
        self.save(update_fields=["totp_secret"])

    def get_totp_uri(self):
        return pyotp.totp.TOTP(self.totp_secret).provisioning_uri(
            name=self.email,
            issuer_name="dBSolution"
        )

    def __str__(self):
        return f"{self.prenom} {self.nom}"




import qrcode

from urllib.parse import quote as urlquote

def generate_qr_code(user):
    uri = f'otpauth://totp/MyApp:{user.email_google}?secret={user.totp_secret}&issuer=MyApp'
    img = qrcode.make(uri)
    img.show()  # ou img.save('totp.png')

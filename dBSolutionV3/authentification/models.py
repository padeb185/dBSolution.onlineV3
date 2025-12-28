from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import pyotp
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email doit être fournie")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    # 🔐 TOTP
    totp_secret = models.CharField(max_length=32, blank=True, null=True, editable=False)
    totp_enabled = models.BooleanField(default=False)

    # Champs Django obligatoires pour AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # 🔐 Méthode pour générer un secret TOTP
    def generate_totp_secret(self, save=True):
        self.totp_secret = pyotp.random_base32()
        if save:
            self.save(update_fields=['totp_secret'])
        return self.totp_secret

    def get_totp_uri(self):
        if not self.totp_secret:
            self.generate_totp_secret()
        return pyotp.totp.TOTP(self.totp_secret).provisioning_uri(
            name=self.email,
            issuer_name="MaSuperApp"
        )


from django.apps import AppConfig

class AuthentificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentification'
    label = 'authentification'

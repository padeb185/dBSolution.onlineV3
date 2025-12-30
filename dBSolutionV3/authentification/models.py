from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
import pyotp
import uuid


class CustomUserManager(BaseUserManager):
    def create_utilisateur(self, email_google, password=None, **extra_fields):
        if not email_google:
            raise ValueError("L'adresse email doit être fournie")

        email_google = self.normalize_email(email_google)

        extra_fields.setdefault("is_active", True)

        user = self.model(email=email_google, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email_google = models.EmailField(
        unique=True,
        verbose_name="Adresse email Google"
    )

    # 🔐 TOTP
    totp_secret = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        editable=False
    )
    totp_enabled = models.BooleanField(default=False)

    # Champs requis par Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email_google

    # 🔐 Génération du secret TOTP
    def generate_totp_secret(self, save=True):
        self.totp_secret = pyotp.random_base32()
        if save:
            self.save(update_fields=["totp_secret"])
        return self.totp_secret

    def get_totp_uri(self):
        if not self.totp_secret:
            self.generate_totp_secret()
        return pyotp.totp.TOTP(self.totp_secret).provisioning_uri(
            name=self.email_google,
            issuer_name="dBSolution"
        )

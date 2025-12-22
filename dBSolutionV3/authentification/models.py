from django.db import models
import pyotp

class Utilisateur(models.Model):
    email = models.EmailField(unique=True)
    totp_secret = models.CharField(max_length=32, blank=True, null=True, editable=False)
    totp_enabled = models.BooleanField(default=False)

    # 🔐 Méthode pour générer un secret TOTP
    def generate_totp_secret(self):
        import pyotp
        self.totp_secret = pyotp.random_base32()
        self.save(update_fields=['totp_secret'])

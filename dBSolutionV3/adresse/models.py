from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Adresse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    rue = models.CharField(_("Rue"), max_length=255)
    numero = models.CharField(_("Numéro"), max_length=10)
    code_postal = models.CharField(_("Code postal"), max_length=10)
    ville = models.CharField(_("Ville"), max_length=100)

    pays = models.CharField(_("Pays"), max_length=100, default="Belgique")
    code_pays = models.CharField(_("Code pays"), max_length=5, default="BE")

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Adresse")
        verbose_name_plural = _("Adresses")
        ordering = ["ville", "rue"]

    def __str__(self):
        return f"{self.rue} {self.numero}, {self.code_postal} {self.ville}"

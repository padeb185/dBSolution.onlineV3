from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid



class Adresse(models.Model):
    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="adresses",
        null=True,
        blank=True,
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    rue = models.CharField(_("Rue"), max_length=255)
    numero = models.CharField(_("Numéro"), max_length=10)
    boite = models.CharField(_("Boite"), max_length=10, null=True, blank=True)
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
        constraints = [
            models.UniqueConstraint(
                fields=["societe", "rue", "numero", "boite", "code_postal", "ville"],
                name="unique_adresse_par_societe"
            )
        ]

    def clean(self):
        """
        Vérifie qu'il n'y a pas de doublon pour la même société.
        """
        if Adresse.objects.filter(
                societe=self.societe,
                rue__iexact=self.rue,
                numero__iexact=self.numero,
                code_postal__iexact=self.code_postal,
                ville__iexact=self.ville
        ).exclude(id=self.id).exists():
            raise ValidationError(
                _("Cette adresse existe déjà pour cette société.")
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Appelle clean() avant de sauvegarder
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rue} {self.numero}, {self.code_postal} {self.ville} {self.pays} {self.code_pays}"


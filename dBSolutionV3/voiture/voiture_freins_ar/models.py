import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class VoitureFreinsAR(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="freins_ar",
        null=True,
        blank=True,
    )

    # 🔗 Relation principale
    voitures_exemplaires = models.ManyToManyField(
        "voiture_exemplaire.VoitureExemplaire",
        related_name="freins_ar",
        blank=True,
    )


    marque_disques_ar = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    numero_oem_disques_av = models.CharField(
        _("Numéro OEM disque AR (mm)"),
        max_length=25,
        blank=True,
        null=True
    )


    marque_plaquettes_ar = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    numero_oem_plaquettes_ar = models.CharField(
        _("Numéro OEM plaquette AR (mm)"),
        max_length=25,
        blank=True,
        null=True
    )
    # 📏 Dimensions

    taille_disque_ar = models.FloatField("Taille disque AR (mm)", null=True, blank=True)


    epaisseur_disque_ar = models.FloatField("Épaisseur disque AR (mm)", null=True, blank=True)


    epaisseur_min_disque_ar = models.FloatField("Épaisseur minimum disque AR (mm)", null=True, blank=True)


    plaquettes_ar = models.FloatField("Plaquettes AR (mm)", null=True, blank=True)

    remarques = models.TextField(verbose_name=_("Remarques"), blank=True, null=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)


    class Meta:
        verbose_name = "Voiture – Freins Arrière"
        verbose_name_plural = "Voitures – Freins Arrière"

    def __str__(self):
        voitures = ", ".join([str(v) for v in self.voitures_exemplaires.all()])
        return f"{voitures or self.id} – Freins arrière"

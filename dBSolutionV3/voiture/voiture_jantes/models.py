import uuid
from django.db import models



class VoitureJante(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Relations ManyToMany
    voitures_modeles = models.ManyToManyField(
        "voiture_modele.VoitureModele",
        related_name="jantes",
        blank=True
    )

    voitures_exemplaires = models.ManyToManyField(
        "voiture_exemplaire.VoitureExemplaire",
        related_name="jantes",
        blank=True
    )

    # 🔹 Jantes d'origine
    taille_jante_av = models.FloatField(verbose_name="Taille jante AV (pouces)")
    taille_jante_ar = models.FloatField(verbose_name="Taille jante AR (pouces)")
    deport_av = models.CharField(max_length=10, verbose_name="Déport AV (ETXX)")
    deport_ar = models.CharField(max_length=10, verbose_name="Déport AR (ETXX)")
    profil = models.CharField(max_length=10, verbose_name="Profil (XXXX)")

    # 🔹 Nouvelle monte
    nouvelles_montes = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="compatible_jantes",
        verbose_name="Nouvelle monte"
    )

    def __str__(self):
        return f"{self.voiture_exemplaire} – Jantes {self.taille_jante_av}\" AV / {self.taille_jante_ar}\" AR"

    class Meta:
        verbose_name = "Voiture – jante"
        verbose_name_plural = "Voitures – jantes"

import uuid
from django.core.exceptions import ValidationError
from django.db import models
from societe.models import Societe
from django.utils.translation import gettext as _
from django.db import models
from django.db.models import Q, F
from django.utils.timezone import now





class NombrePortes(models.IntegerChoices):
    ZERO = 0, "0 portes"
    DEUX = 2, "2 portes"
    TROIS = 3, "3 portes"
    QUATRE = 4, "4 portes"
    CINQ = 5, "5 portes"





class VoitureModele(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.PROTECT,
        related_name="modeles"
    )
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)

    nom_modele = models.CharField(max_length=100)
    nom_variante = models.CharField(max_length=100, blank=True, null=True)
    nombre_portes = models.IntegerField(choices=NombrePortes.choices)
    nbre_places = models.PositiveSmallIntegerField()
    taille_reservoir = models.DecimalField(max_digits=5, decimal_places=2, help_text="En litres")
    capacite_batterie = models.PositiveIntegerField(null=True, blank=True, help_text="Capacité batterie en kWh")

    annee_debut = models.IntegerField(null=True, blank=True)
    annee_fin = models.IntegerField(null=True, blank=True)
    mois_debut = models.IntegerField(null=True, blank=True)
    mois_fin = models.IntegerField(null=True, blank=True)

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["voiture_marque", "nom_modele", "nom_variante"],
                name="unique_modele_variante_par_marque"
            ),
            models.CheckConstraint(
                check=Q(mois_debut__gte=1, mois_debut__lte=12) | Q(mois_debut__isnull=True),
                name="mois_debut_entre_1_12",
            ),

            # Mois fin entre 1 et 12 (ou NULL)
            models.CheckConstraint(
                check=Q(mois_fin__gte=1, mois_fin__lte=12) | Q(mois_fin__isnull=True),
                name="mois_fin_entre_1_12",
            ),

            # Année début entre 1850 et année actuelle
            models.CheckConstraint(
                check=Q(annee_debut__gte=1940, annee_debut__lte=now().year) | Q(annee_debut__isnull=True),
                name="annee_debut_valide",
            ),

            # Année fin >= année début (si les deux sont remplis)
            models.CheckConstraint(
                check=Q(annee_fin__gte=F("annee_debut")) | Q(annee_fin__isnull=True) | Q(annee_debut__isnull=True),
                name="annee_fin_apres_debut",
            ),

            # Si même année → mois fin >= mois début
            models.CheckConstraint(
                check=(
                        Q(annee_fin__gt=F("annee_debut"))
                        | Q(annee_fin__isnull=True)
                        | Q(annee_debut__isnull=True)
                        | Q(mois_fin__gte=F("mois_debut"))
                ),
                name="mois_fin_apres_debut_si_meme_annee",
            ),
        ]

    def __str__(self):
        return f"{self.nom_modele} {self.nom_variante or ''}".strip()

    def clean(self):
        super().clean()
        if self.voiture_marque and self.nom_modele:
            qs = VoitureModele.objects.filter(
                voiture_marque=self.voiture_marque,
                nom_modele__iexact=self.nom_modele,
            )
            if self.nom_variante:
                qs = qs.filter(nom_variante__iexact=self.nom_variante)
            else:
                qs = qs.filter(nom_variante__isnull=True)

            if self.pk:
                qs = qs.exclude(pk=self.pk)

            if qs.exists():
                raise ValidationError(_("Ce modèle avec cette variante existe déjà pour cette marque."))

    def save(self, *args, **kwargs):
        self.full_clean()  # Valide l’instance avant sauvegarde
        super().save(*args, **kwargs)
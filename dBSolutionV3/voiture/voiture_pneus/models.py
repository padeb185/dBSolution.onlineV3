import uuid
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _



class TypePneus(models.TextChoices):
    ETE = "ete", _("Été")
    PLUIE = "pluie", _("Pluie")
    SEMI_SLICK = "semi_slick", _("Semi-slick")
    SLICK = "slick", _("Slick")
    QUATRE_SAISONS = "4saisons", _("4 saisons")
    HIVER = "hiver", _("Hiver")


class VoiturePneus(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relations ManyToMany
    voitures_modeles = models.ManyToManyField(
        "voiture_modele.VoitureModele",
        related_name="pneus",
        blank=True
    )

    voitures_exemplaires = models.ManyToManyField(
        "voiture_exemplaire.VoitureExemplaire",
        related_name="pneus",
        blank=True
    )

    fournisseur = models.ForeignKey(
        "fournisseur.Fournisseur",
        on_delete=models.PROTECT,
        related_name="pneus"
    )

    type_pneus = models.CharField(
        max_length=20,
        choices=TypePneus.choices
    )

    pneus_avant_largeur = models.CharField(max_length=15, help_text="175 mm")
    pneus_avant_hauteur = models.CharField(max_length=15, help_text="65 %")
    pneus_avant_jante = models.CharField(max_length=15, help_text="15 pouces")

    pneus_arriere_largeur = models.CharField(max_length=15, help_text="175 mm")
    pneus_arriere_hauteur = models.CharField(max_length=15, help_text="65 %")
    pneus_arriere_jante = models.CharField(max_length=15, help_text="15 pouces")


    kilometre_pneus_av= models.PositiveIntegerField(default=0)
    kilometre_pneus_ar = models.PositiveIntegerField(default=0)


    date_remplacement = models.DateField(null=True, blank=True)
    kilometre_remplacement = models.PositiveIntegerField(null=True, blank=True)

    nombre_trains_av = models.PositiveSmallIntegerField(default=1)
    nombre_trains_ar = models.PositiveSmallIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def remplacer_pneus(self, nouveau_type, nouveaux_pneus_avant, nouveaux_pneus_arriere, date=None):
        """
        Archive la monte actuelle et installe de nouveaux pneus.
        L'historique doit être géré dans admin.py ou via signals.
        """
        from django.apps import apps
        VoiturePneusHistorique = apps.get_model('voiture_pneus_historique', 'VoiturePneusHistorique')

        if self.kilometre_pneus_av > 0 or self.kilometre_pneus_ar > 0:
            VoiturePneusHistorique.objects.create(
                voiture_pneus=self,
                type_pneus=self.type_pneus,
                pneus_avant_largeur=self.pneus_avant_largeur,
                pneus_arriere_largeur=self.pneus_arriere_largeur,
                kilometres_effectues=self.kilometre_pneus_av,
                kilometres_effectues_ar=self.kilometre_pneus_ar,
                numero_remplacement=self.historiques.count() + 1 if hasattr(self, 'historiques') else 1,
                date_remplacement=date or timezone.now().date()
            )

        # Mise à jour de la monte
        self.type_pneus = nouveau_type
        self.pneus_avant = nouveaux_pneus_avant
        self.pneus_arriere = nouveaux_pneus_arriere
        self.kilometre_remplacement = self.kilometre_pneus_av
        self.kilometre_remplacement = self.kilometre_pneus_ar
        self.kilometre_pneus = 0
        self.date_remplacement = date or timezone.now().date()
        self.save()

    def __str__(self):
        return f"{self.voitures_exemplaires} - {self.get_type_pneus_display()}"

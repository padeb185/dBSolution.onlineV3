import uuid
from django.db import models
from django.utils import timezone

class VoiturePneus(models.Model):

    class TypePneus(models.TextChoices):
        ETE = "ete", "Été"
        PLUIE = "pluie", "Pluie"
        SEMI_SLICK = "semi_slick", "Semi-slick"
        SLICK = "slick", "Slick"
        QUATRE_SAISONS = "4saisons", "4 saisons"
        HIVER = "hiver", "Hiver"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    voiture_modele = models.ForeignKey(
        'voiture_modele.VoitureModele',
        on_delete=models.PROTECT,
        related_name="configurations_pneus"
    )
    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.PROTECT,
        related_name="pneus",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.PROTECT,
        related_name="pneus",
        null=True, blank=True
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

    pneus_avant = models.CharField(max_length=15, help_text="Format xxx/xx/xx")
    pneus_arriere = models.CharField(max_length=15, help_text="Format xxx/xx/xx")

    kilometre_pneus = models.PositiveIntegerField(default=0)
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

        if self.kilometre_pneus > 0:
            VoiturePneusHistorique.objects.create(
                voiture_pneus=self,
                type_pneus=self.type_pneus,
                pneus_avant=self.pneus_avant,
                pneus_arriere=self.pneus_arriere,
                kilometres_effectues=self.kilometre_pneus,
                numero_remplacement=self.historiques.count() + 1 if hasattr(self, 'historiques') else 1,
                date_remplacement=date or timezone.now().date()
            )

        # Mise à jour de la monte
        self.type_pneus = nouveau_type
        self.pneus_avant = nouveaux_pneus_avant
        self.pneus_arriere = nouveaux_pneus_arriere
        self.kilometre_remplacement = self.kilometre_pneus
        self.kilometre_pneus = 0
        self.date_remplacement = date or timezone.now().date()
        self.save()

    def __str__(self):
        return f"{self.voiture_exemplaire} - {self.get_type_pneus_display()}"

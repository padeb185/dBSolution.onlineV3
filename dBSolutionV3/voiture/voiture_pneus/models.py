import uuid
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _





class VoiturePneus(models.Model):


    class TypePneus(models.TextChoices):
        ETE = "ete", _("Été")
        PLUIE = "pluie", _("Pluie")
        SEMI_SLICK = "semi_slick", _("Semi-slick")
        SLICK = "slick", _("Slick")
        QUATRE_SAISONS = "4saisons", _("4 saisons")
        HIVER = "hiver", _("Hiver")

    class IndiceVitesse(models.TextChoices):
        Q = "Q", _("Q (160 km/h)")
        R = "R", _("R (170 km/h)")
        S = "S", _("S (180 km/h)")
        T = "T", _("T (190 km/h)")
        H = "H", _("H (210 km/h)")
        V = "V", _("V (240 km/h)")
        W = "W", _("W (270 km/h)")
        Y = "Y", _("Y (300 km/h)")
        ZR_W = "ZR W", _("ZR W (>270 km/h)")
        ZR_Y = "ZR Y", _("ZR Y (>300 km/h)")
        ZR = "ZR", _("ZR (historique >240 km/h)")

    class IndiceCharge(models.TextChoices):
        L60 = "60", _("60 (250 kg)")
        M62 = "62", _("62 (265 kg)")
        N64 = "64", _("64 (280 kg)")
        P68 = "68", _("68 (315 kg)")
        Q70 = "70", _("70 (335 kg)")
        R73 = "73", _("73 (365 kg)")
        S75 = "75", _("75 (387 kg)")
        T78 = "78", _("78 (425 kg)")
        U81 = "81", _("81 (450 kg)")
        V84 = "84", _("84 (500 kg)")
        W87 = "87", _("87 (545 kg)")
        Y91 = "91", _("91 (615 kg)")
        Z94 = "94", _("94 (670 kg)")
        X97 = "97", _("97 (730 kg)")
        ZR100 = "100", _("100 (800 kg)")
        ZR103 = "103", _("103 (875 kg)")
        ZR106 = "106", _("106 (950 kg)")
        ZR109 = "109", _("109 (1030 kg)")
        ZR112 = "112", _("112 (1120 kg)")
        ZR115 = "115", _("115 (1215 kg)")
        ZR118 = "118", _("118 (1320 kg)")



    class EmplacementPneus(models.TextChoices):
        AVANT = "avant", _("Avant")
        ARRIERE = "arriere", _("Arrière")
        AVANT_ET_ARRIERE = "avant_arriere", _("Avant et Arrière")

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

    manufacturier = models.CharField(max_length=100)

    emplacement = models.CharField(
        max_length=50,
        choices=EmplacementPneus.choices
    )

    type_pneus = models.CharField(
        max_length=20,
        choices=TypePneus.choices
    )

    nom_type = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    numero_oem = models.CharField(max_length=50, blank=True, null=True)


    pneus_largeur = models.CharField(max_length=15, help_text="175 mm", default="175")
    pneus_hauteur = models.CharField(max_length=15, help_text="65 %", default="65")
    pneus_jante = models.CharField(max_length=15, help_text="15 pouces", default="15")


    kilometre_pneus_av = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Kilomètres pneus avant"),
        null=True,
        blank=True
    )
    kilometre_pneus_ar = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Kilomètres pneus arrière"),
        null=True,
        blank=True

    )

    # Indices
    indice_vitesse = models.CharField(
        max_length=10,
        choices=IndiceVitesse.choices,
        default=IndiceVitesse.T,
        verbose_name=_("Indice de vitesse")
    )
    indice_charge = models.CharField(
        max_length=10,
        choices=IndiceCharge.choices,
        default=IndiceCharge.Y91,
        verbose_name=_("Indice de charge")
    )


    date_remplacement = models.DateField(null=True, blank=True)
    kilometre_remplacement = models.PositiveIntegerField(null=True, blank=True)

    nombre_trains_av = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    nombre_trains_ar = models.PositiveSmallIntegerField(default=1, null=True, blank=True)

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
                pneus_avant_largeur=self.pneus_largeur,
                pneus_arriere_largeur=self.pneus_largeur,
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

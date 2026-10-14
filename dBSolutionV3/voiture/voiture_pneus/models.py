import uuid
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import FabricantPneus


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
        O66 = "66", _("66 (300 kg)")
        P68 = "68", _("68 (315 kg)")
        Q70 = "70", _("70 (335 kg)")
        R73 = "73", _("73 (365 kg)")
        S75 = "75", _("75 (387 kg)")
        T77 = "77", _("77 (412 kg)")
        U78 = "78", _("78 (425 kg)")
        V79 = "79", _("79 (437 kg)")
        W80 = "80", _("80 (450 kg)")
        X81 = "81", _("81 (462 kg)")
        Y82 = "82", _("82 (475 kg)")
        Z83 = "83", _("83 (487 kg)")
        A84 = "84", _("84 (500 kg)")
        B85 = "85", _("85 (515 kg)")
        C86 = "86", _("86 (530 kg)")
        D87 = "87", _("87 (545 kg)")
        E88 = "88", _("88 (560 kg)")
        F89 = "89", _("89 (580 kg)")
        G90 = "90", _("90 (600 kg)")
        H91 = "91", _("91 (615 kg)")
        I92 = "92", _("92 (630 kg)")
        J93 = "93", _("93 (650 kg)")
        K94 = "94", _("94 (670 kg)")
        L95 = "95", _("95 (690 kg)")
        M96 = "96", _("96 (710 kg)")
        N97 = "97", _("97 (730 kg)")
        O98 = "98", _("98 (750 kg)")
        P99 = "99", _("99 (775 kg)")
        Q100 = "100", _("100 (800 kg)")
        R101 = "101", _("101 (825 kg)")
        S102 = "102", _("102 (850 kg)")
        T103 = "103", _("103 (875 kg)")
        U104 = "104", _("104 (900 kg)")
        V105 = "105", _("105 (925 kg)")
        W106 = "106", _("106 (950 kg)")
        X107 = "107", _("107 (975 kg)")
        Y108 = "108", _("108 (1000 kg)")
        Z109 = "109", _("109 (1030 kg)")
        A110 = "110", _("110 (1060 kg)")
        B111 = "111", _("111 (1090 kg)")
        C112 = "112", _("112 (1120 kg)")
        D113 = "113", _("113 (1150 kg)")
        E114 = "114", _("114 (1180 kg)")
        F115 = "115", _("115 (1215 kg)")
        G116 = "116", _("116 (1250 kg)")
        H117 = "117", _("117 (1285 kg)")
        I118 = "118", _("118 (1320 kg)")
        J119 = "119", _("119 (1360 kg)")
        K120 = "120", _("120 (1400 kg)")
        L121 = "121", _("121 (1450 kg)")
        M122 = "122", _("122 (1500 kg)")
        N123 = "123", _("123 (1550 kg)")
        O124 = "124", _("124 (1600 kg)")
        P125 = "125", _("125 (1650 kg)")
        Q126 = "126", _("126 (1700 kg)")
        R127 = "127", _("127 (1750 kg)")
        S128 = "128", _("128 (1800 kg)")
        T129 = "129", _("129 (1850 kg)")
        U130 = "130", _("130 (1900 kg)")



    class EmplacementPneus(models.TextChoices):
        AVANT = "avant", _("Avant")
        ARRIERE = "arriere", _("Arrière")
        AVANT_ET_ARRIERE = "avant_arriere", _("Avant et Arrière")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="pneus",
        null=True,
        blank=True,
    )

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


    manufacturier =  models.CharField(
        max_length=30,
        choices=FabricantPneus.choices,
        default=FabricantPneus.CHOISIR,
        verbose_name=_("Manufacturier")
    )

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


    pneus_largeur = models.CharField(max_length=15, default="175", verbose_name=_("Largeur du pneu"))
    pneus_hauteur = models.CharField(max_length=15, default="65", verbose_name=_("Hauteur du pneu"))
    pneus_jante = models.CharField(max_length=15,  default="15", verbose_name=_("Diamètre de la jante en pouces"))


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
        default=IndiceCharge.H91,
        verbose_name=_("Indice de charge")
    )


    date_remplacement = models.DateField(null=True, blank=True)
    kilometre_remplacement = models.PositiveIntegerField(null=True, blank=True)

    nombre_trains_av = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    nombre_trains_ar = models.PositiveSmallIntegerField(default=1, null=True, blank=True)


    remarques = models.TextField(verbose_name=_("Remarques"), blank=True, null=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)


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

    @property
    def taille(self):
        return f"{self.pneus_largeur}/{self.pneus_hauteur} R{self.pneus_jante}"

    def __str__(self):
        return f"{self.manufacturier} {self.taille} - {self.get_type_pneus_display()}"



class TrainPneus(models.Model):
    """
    Un « train » = un jeu de pneus monté sur un essieu (avant ou arrière)
    d'un véhicule précis.

    - Le compteur de trains commence à 1 (première monte d'origine) et
      s'incrémente à chaque remplacement, séparément pour l'avant et l'arrière.
    - Un véhicule peut avoir deux montes actives par essieu :
      la première monte (ex. été) et une seconde monte (ex. hiver).
      Une seule est montée à la fois ; les km de chaque monte se cumulent
      d'une saison à l'autre.
    - Lors d'un remplacement, l'ancien train est figé (actif=False) avec
      ses km effectués, et le nouveau train repart de zéro.
    """

    class Position(models.TextChoices):
        AVANT = "avant", _("Avant")
        ARRIERE = "arriere", _("Arrière")

    class Monte(models.TextChoices):
        PREMIERE = "premiere", _("Première monte")
        SECONDE = "seconde", _("Seconde monte")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="trains_pneus",
        null=True,
        blank=True,
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="trains_pneus",
        verbose_name=_("Véhicule"),
    )

    voiture_pneus = models.ForeignKey(
        VoiturePneus,
        on_delete=models.SET_NULL,
        related_name="trains",
        null=True,
        blank=True,
        verbose_name=_("Pneus"),
    )

    # Copie du libellé : l'historique reste lisible même si la fiche pneu est supprimée
    libelle_pneus = models.CharField(max_length=200, blank=True, default="")

    position = models.CharField(max_length=10, choices=Position.choices)
    monte = models.CharField(max_length=10, choices=Monte.choices, default=Monte.PREMIERE)
    type_pneus = models.CharField(
        max_length=20,
        choices=VoiturePneus.TypePneus.choices,
        blank=True,
        default="",
    )

    numero = models.PositiveSmallIntegerField(verbose_name=_("N° de train"))

    actif = models.BooleanField(
        default=True,
        help_text=_("Faux une fois le train remplacé (archivé dans l'historique)."),
    )
    est_monte = models.BooleanField(
        default=False,
        help_text=_("Vrai si ce train est actuellement monté sur le véhicule."),
    )

    km_montage = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Km châssis au dernier montage"),
    )
    km_cumules = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Km cumulés lors des montages précédents"),
    )

    date_montage = models.DateField(default=timezone.localdate, verbose_name=_("Date de montage"))
    date_remplacement = models.DateField(null=True, blank=True, verbose_name=_("Date de remplacement"))
    km_remplacement = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("Km châssis au remplacement")
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ["voiture_exemplaire", "position", "numero"]
        verbose_name = _("Train de pneus")
        verbose_name_plural = _("Trains de pneus")
        constraints = [
            models.UniqueConstraint(
                fields=["voiture_exemplaire", "position", "numero"],
                name="unique_numero_train_par_position",
            ),
        ]

    # ------------------------------------------------------------------
    # Kilométrage
    # ------------------------------------------------------------------
    def _km_chassis(self):
        return self.voiture_exemplaire.kilometres_chassis or 0

    @property
    def km_effectues(self):
        """Km parcourus avec ce train (cumul de tous ses montages)."""
        total = self.km_cumules or 0
        if self.est_monte and self.actif:
            total += max(0, self._km_chassis() - (self.km_montage or 0))
        return total

    def demonter(self, km_chassis):
        if self.est_monte:
            self.km_cumules = (self.km_cumules or 0) + max(0, km_chassis - (self.km_montage or 0))
            self.est_monte = False

    def monter(self, km_chassis):
        if not self.est_monte:
            self.est_monte = True
            self.km_montage = km_chassis

    # ------------------------------------------------------------------
    def save(self, *args, **kwargs):
        if self.voiture_pneus_id:
            self.libelle_pneus = str(self.voiture_pneus)[:200]
            self.type_pneus = self.voiture_pneus.type_pneus
        if not self.societe_id and self.voiture_exemplaire_id:
            self.societe_id = self.voiture_exemplaire.societe_id
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.voiture_exemplaire} | {self.get_position_display()} "
            f"train n°{self.numero} ({self.get_monte_display()})"
        )

from decimal import ROUND_HALF_UP, Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import TAUX_HORAIRE_CHOICES, TVAConfig
from maintenance.models import Maintenance


# ============================================================
# ALLUMAGE
# ============================================================

class EtatAllumage(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    NON_PRESENT = "NON_PRESENT", _("Non présent")



class FabricantAllumage(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    OEM = "OEM", _("Origine constructeur (OEM)")

    BOSCH = "BOSCH", _("Bosch")
    NGK = "NGK", _("NGK")
    BERU = "BERU", _("Beru")
    DENSO = "DENSO", _("Denso")
    DELPHI = "DELPHI", _("Delphi")
    HELLA = "HELLA", _("Hella")
    VALEO = "VALEO", _("Valeo")
    BREMBO = "BREMBO", _("Brembo")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    CHAMPION = "CHAMPION", _("Champion")
    BREMI = "BREMI", _("Bremi")
    HITACHI = "HITACHI", _("Hitachi")
    VDO = "VDO", _("VDO")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    FACET = "FACET", _("Facet")
    ERA = "ERA", _("ERA")
    MEYLE = "MEYLE", _("Meyle")
    FEBI = "FEBI", _("Febi Bilstein")

    AUTRE = "AUTRE", _("Autre fabricant")
    INCONNU = "INCONNU", _("Fabricant inconnu")



class Allumage(models.Model):

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="allumage",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    # ========================================================
    # VÉHICULE
    # ========================================================

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="allumages",
        verbose_name=_("Véhicule"),
    )

    immatriculation = models.CharField(
        max_length=20,
        verbose_name=_("Immatriculation"),
        blank=True,
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Kilomètres châssis"),
    )

    kilometrage_allumage = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du controle de l'allumage"),

    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date du contrôle"),
    )

    # ========================================================
    # BOUGIES
    # ========================================================

    bougies_etat = models.CharField(
        max_length=20,
        choices=EtatAllumage.choices,
        default=EtatAllumage.OK,
        verbose_name=_("État des bougies"),
    )

    bougies_fabricant = models.CharField(
        max_length=30,
        choices=FabricantAllumage.choices,
        default=FabricantAllumage.CHOISIR,
        verbose_name=_("Fabricant"),
    )

    bougies_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Référence"),
    )

    bougies_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    bougies_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # ========================================================
    # BOBINES D'ALLUMAGE
    # ========================================================

    bobines_etat = models.CharField(
        max_length=20,
        choices=EtatAllumage.choices,
        default=EtatAllumage.OK,
        verbose_name=_("État des bobines d'allumage"),
    )

    bobines_fabricant = models.CharField(
        max_length=30,
        choices=FabricantAllumage.choices,
        default=FabricantAllumage.CHOISIR,
        verbose_name=_("Fabricant"),
    )

    bobines_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Référence"),
    )

    bobines_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    bobines_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # ========================================================
    # FAISCEAU / CÂBLES HAUTE TENSION
    # ========================================================

    faisceau_allumage_etat = models.CharField(
        max_length=20,
        choices=EtatAllumage.choices,
        default=EtatAllumage.NON_PRESENT,
        verbose_name=_("État du faisceau d'allumage"),
    )

    faisceau_allumage_fabricant = models.CharField(
        max_length=30,
        choices=FabricantAllumage.choices,
        default=FabricantAllumage.CHOISIR,
        verbose_name=_("Fabricant"),
    )

    faisceau_allumage_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    faisceau_allumage_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # ========================================================
    # TÊTE D'ALLUMEUR
    # ========================================================

    tete_allumeur_etat = models.CharField(
        max_length=20,
        choices=EtatAllumage.choices,
        default=EtatAllumage.NON_PRESENT,
        verbose_name=_("État de la tête d'allumeur"),
    )

    tete_allumeur_fabricant = models.CharField(
        max_length=30,
        choices=FabricantAllumage.choices,
        default=FabricantAllumage.CHOISIR,
        verbose_name=_("Fabricant"),
    )

    tete_allumeur_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    tete_allumeur_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # ========================================================
    # DOIGT / ROTOR D'ALLUMEUR
    # ========================================================

    rotor_allumeur_etat = models.CharField(
        max_length=20,
        choices=EtatAllumage.choices,
        default=EtatAllumage.NON_PRESENT,
        verbose_name=_("État du rotor d'allumeur"),
    )

    rotor_allumeur_fabricant = models.CharField(
        max_length=30,
        choices=FabricantAllumage.choices,
        default=FabricantAllumage.CHOISIR,
        verbose_name=_("Fabricant"),
    )

    rotor_allumeur_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    rotor_allumeur_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # ========================================================
    # MODULE D'ALLUMAGE
    # ========================================================

    module_allumage_etat = models.CharField(
        max_length=20,
        choices=EtatAllumage.choices,
        default=EtatAllumage.NON_PRESENT,
        verbose_name=_("État du module d'allumage"),
    )

    module_allumage_fabricant = models.CharField(
        max_length=30,
        choices=FabricantAllumage.choices,
        default=FabricantAllumage.CHOISIR,
        verbose_name=_("Fabricant"),
    )

    module_allumage_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    module_allumage_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # ========================================================
    # CAPTEUR PMH / VILEBREQUIN
    # ========================================================

    capteur_vilebrequin_etat = models.CharField(
        max_length=20,
        choices=EtatAllumage.choices,
        default=EtatAllumage.OK,
        verbose_name=_("État du capteur de vilebrequin"),
    )

    capteur_vilebrequin_fabricant = models.CharField(
        max_length=30,
        choices=FabricantAllumage.choices,
        default=FabricantAllumage.CHOISIR,
        verbose_name=_("Fabricant"),
    )

    capteur_vilebrequin_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    capteur_vilebrequin_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # ========================================================
    # CAPTEUR ARBRE À CAMES
    # ========================================================

    capteur_arbre_cames_etat = models.CharField(
        max_length=20,
        choices=EtatAllumage.choices,
        default=EtatAllumage.OK,
        verbose_name=_("État du capteur d'arbre à cames"),
    )

    capteur_arbre_cames_fabricant = models.CharField(
        max_length=30,
        choices=FabricantAllumage.choices,
        default=FabricantAllumage.CHOISIR,
        verbose_name=_("Fabricant"),
    )

    capteur_arbre_cames_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    capteur_arbre_cames_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # -------------------------
    # CONFIG TVA
    # -------------------------
    PAYS_CHOICES = [
        ('AT', _("Autriche")),
        ('BE', _("Belgique")),
        ('BG', _("Bulgarie")),
        ('CY', _("Chypre")),
        ('CZ', _("Tchéquie")),
        ('DE', _("Allemagne")),
        ('DK', _("Danemark")),
        ('EE', _("Estonie")),
        ('ES', _("Espagne")),
        ('FI', _("Finlande")),
        ('FR', _("France")),
        ('GR', _("Grèce")),
        ('HR', _("Croatie")),
        ('HU', _("Hongrie")),
        ('IE', _("Irlande")),
        ('IT', _("Italie")),
        ('LT', _("Lituanie")),
        ('LU', _("Luxembourg")),
        ('LV', _("Lettonie")),
        ('MT', _("Malte")),
        ('NL', _("Pays-Bas")),
        ('PL', _("Pologne")),
        ('PT', _("Portugal")),
        ('RO', _("Roumanie")),
        ('SE', _("Suède")),
        ('SI', _("Slovénie")),
        ('SK', _("Slovaquie")),
    ]

    TVA_PIECES = {
        'AT': 20,
        'BE': 21,
        'BG': 20,
        'CY': 19,
        'CZ': 21,
        'DE': 19,
        'DK': 25,
        'EE': 24,
        'ES': 21,
        'FI': 25.5,
        'FR': 20,
        'GR': 24,
        'HR': 25,
        'HU': 27,
        'IE': 23,
        'IT': 22,
        'LT': 21,
        'LU': 17,
        'LV': 21,
        'MT': 18,
        'NL': 21,
        'PL': 23,
        'PT': 23,
        'RO': 21,
        'SE': 25,
        'SI': 22,
        'SK': 23,
    }
    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES,
        default="BE",
        verbose_name=_("Pays"),
    )

    # ========================================================
    # COMMENTAIRES
    # ========================================================

    remarques = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Remarques"),
    )

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]

    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="JAUNE",
        verbose_name=_("État visuel / Tag"),
    )

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="allumage",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="allumage"
    )

    tech_nom_technicien = models.CharField(
        _("Nom du technicien"),
        max_length=255,
        blank=True
    )

    tech_role_technicien = models.CharField(
        _("Rôle du technicien"),
        max_length=255,
        blank=True
    )

    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="allumage"
    )
    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )





    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

        class Meta:
            verbose_name = _("Allumage")
            verbose_name_plural = _("Allumages")

    def __str__(self):
        voiture = getattr(self, "voiture_exemplaire", None)
        return f"Allumage moteur - {voiture or 'Sans véhicule'}"




    def clean(self):
        super().clean()

        voiture = getattr(self, "voiture_exemplaire", None)

        if voiture and self.kilometrage_allumage is not None:
            if self.kilometrage_allumage < voiture.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_allumage': _(
                        "Le kilométrage ne peut pas être inférieur au kilométrage actuel."
                    )
                })

    def save(self, *args, **kwargs):

        # =========================
        # TECHNICIEN
        # =========================
        if (
                not self.tech_technicien_id
                and hasattr(self, "_user")
        ):
            self.assign_technicien(
                self._user
            )

        # =========================
        # VEHICULE
        # =========================
        voiture = None

        if self.voiture_exemplaire_id:
            voiture = type(
                self.voiture_exemplaire
            ).objects.get(
                pk=self.voiture_exemplaire_id
            )

        # =========================
        # ANCIEN KM ADMISSION
        # =========================
        ancien_kilometrage = 0

        if self.pk:

            ancien_objet = type(self).objects.filter(
                pk=self.pk
            ).first()

            if ancien_objet:
                ancien_kilometrage = (
                        ancien_objet.kilometrage_allumage
                        or ancien_objet.kilometres_chassis
                        or 0
                )

        elif voiture:

            ancien_kilometrage = (
                    voiture.kilometres_chassis
                    or 0
            )

        # =========================
        # VARIATION
        # =========================
        if self.kilometrage_allumage is not None:

            self.kilometrage_variation = (
                    self.kilometrage_allumage
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km admission
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_allumage
            )

        else:

            self.kilometrage_variation = 0

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if (
                self.main_oeuvre_id
                and self.voiture_exemplaire_id
        ):
            self.main_oeuvre.descriptif = (
                    _("Admission")
                    + " "
                    + str(self.voiture_exemplaire)
            )

            self.main_oeuvre.save(
                update_fields=[
                    "descriptif"
                ]
            )

        # =========================
        # MAINTENANCE
        # =========================
        if (
                self.maintenance_id
                and self.voiture_exemplaire_id
        ):

            self.maintenance.type_maintenance = (
                Maintenance.TypeMaintenance.ALLUMAGE
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_allumage is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_allumage
                )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAVE ADMISSION
        # =========================
        super().save(
            *args,
            **kwargs
        )

        # =========================
        # UPDATE VEHICULE
        # =========================
        if (
                voiture is not None
                and self.kilometrage_allumage is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_allumage
            )

            kilometrage_vehicule = int(
                voiture.kilometres_chassis
                or 0
            )

            # Ne jamais faire redescendre
            # le kilométrage général du véhicule
            if nouveau_kilometrage >= kilometrage_vehicule:
                voiture.kilometres_chassis = (
                    nouveau_kilometrage
                )

                voiture.save(
                    update_fields=[
                        "kilometres_chassis"
                    ]
                )



        # ========================================================
        # SAUVEGARDE
        # ========================================================

        super().save(*args, **kwargs)




    def generer_rapport_remplacement(self):
        lignes = []
        total_general = Decimal("0.00")

        etats_labels = dict(EtatAllumage.choices)

        # ========================================================
        # PARCOURS DES CHAMPS D'ÉTAT
        # ========================================================

        for field in self._meta.fields:
            field_name = field.name

            # On ne traite que les champs utilisant EtatAllumage
            if not (
                    isinstance(field, models.CharField)
                    and field.choices == EtatAllumage.choices
            ):
                continue

            valeur = getattr(self, field_name, None)

            # Uniquement les pièces à remplacer ou remplacées
            if valeur not in (
                    EtatAllumage.A_REMPLACER,
                    EtatAllumage.REMPLACE,
            ):
                continue

            # ====================================================
            # PREFIX
            #
            # bougies_etat -> bougies
            # bobines_etat -> bobines
            # faisceau_allumage_etat -> faisceau_allumage
            # ====================================================

            if field_name.endswith("_etat"):
                prefix = field_name[:-5]
            else:
                prefix = field_name

            # ====================================================
            # PRIX
            # ====================================================

            prix = getattr(
                self,
                f"{prefix}_prix",
                Decimal("0.00"),
            )

            prix = Decimal(
                str(prix or "0.00")
            )

            # ====================================================
            # QUANTITÉ
            # ====================================================

            quantite = getattr(
                self,
                f"{prefix}_quantite",
                0,
            )

            quantite = Decimal(
                str(quantite or 0)
            )

            # ====================================================
            # FABRICANT
            # ====================================================

            fabricant_field_name = (
                f"{prefix}_fabricant"
            )

            fabricant = getattr(
                self,
                fabricant_field_name,
                None,
            )

            fabricant_label = "-"

            if fabricant not in (
                    None,
                    "",
                    "CHOISIR",
            ):
                get_fabricant_display = getattr(
                    self,
                    f"get_{fabricant_field_name}_display",
                    None,
                )

                if callable(get_fabricant_display):
                    fabricant_label = (
                        get_fabricant_display()
                    )
                else:
                    fabricant_label = fabricant

            # ====================================================
            # RÉFÉRENCE
            # ====================================================

            reference = getattr(
                self,
                f"{prefix}_reference",
                None,
            )

            # ====================================================
            # TOTAL
            # ====================================================

            total = (
                    prix * quantite
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total_general += total

            # ====================================================
            # AJOUT AU RAPPORT
            # ====================================================

            lignes.append({
                "champ": field.verbose_name,
                "code": prefix,

                "etat": valeur,
                "etat_label": etats_labels.get(
                    valeur,
                    valeur,
                ),

                "fabricant": fabricant,
                "fabricant_label": fabricant_label,

                "reference": reference,

                "prix": prix.quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                ),

                "quantite": quantite,

                "total": total,
            })

        # ========================================================
        # RETOUR
        # ========================================================

        return {
            "lignes": lignes,

            "total_general": total_general.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            ),
        }
            # ======================================================
            # MAIN-D'ŒUVRE
            # ======================================================

    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        heures, minutes = divmod(temps_minutes, 60)

        return f"{heures}h{minutes:02d}"

    @property
    def taux_horaire_main_oeuvre(self):
        if (
                self.main_oeuvre
                and self.main_oeuvre.taux_horaire is not None
        ):
            return self.main_oeuvre.taux_horaire

        return Decimal("0.00")


    @property
    def cout_main_oeuvre(self):
        if not self.main_oeuvre:
            return Decimal("0.00")

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        taux_horaire = (
                self.main_oeuvre.taux_horaire or Decimal("0.00")
        )

        cout = (
                Decimal(str(temps_minutes))
                / Decimal("60")
                * Decimal(str(taux_horaire))
        )

        return cout.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()

        return (
                rapport["total_general"]
                + self.cout_main_oeuvre
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
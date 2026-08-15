from decimal import ROUND_HALF_UP, Decimal

from django.core.exceptions import ValidationError

from django.db import models
from django.utils.translation import gettext_lazy as _
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
        related_name="admission",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
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

    date_controle = models.DateField(
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
        verbose_name=_("Fabricant des bougies"),
    )

    bougies_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Référence des bougies"),
    )

    bougies_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de bougies"),
    )

    bougies_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix unitaire des bougies HTVA"),
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
        verbose_name=_("Fabricant des bobines d'allumage"),
    )

    bobines_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Référence des bobines d'allumage"),
    )

    bobines_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de bobines d'allumage"),
    )

    bobines_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix unitaire des bobines HTVA"),
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
        verbose_name=_("Fabricant du faisceau d'allumage"),
    )

    faisceau_allumage_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de faisceaux d'allumage"),
    )

    faisceau_allumage_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du faisceau d'allumage HTVA"),
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
        verbose_name=_("Fabricant de la tête d'allumeur"),
    )

    tete_allumeur_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de têtes d'allumeur"),
    )

    tete_allumeur_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la tête d'allumeur HTVA"),
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
        verbose_name=_("Fabricant du rotor d'allumeur"),
    )

    rotor_allumeur_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de rotors d'allumeur"),
    )

    rotor_allumeur_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du rotor d'allumeur HTVA"),
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
        verbose_name=_("Fabricant du module d'allumage"),
    )

    module_allumage_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de modules d'allumage"),
    )

    module_allumage_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du module d'allumage HTVA"),
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
        verbose_name=_("Fabricant du capteur de vilebrequin"),
    )

    capteur_vilebrequin_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de capteurs de vilebrequin"),
    )

    capteur_vilebrequin_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du capteur de vilebrequin HTVA"),
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
        verbose_name=_("Fabricant du capteur d'arbre à cames"),
    )

    capteur_arbre_cames_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de capteurs d'arbre à cames"),
    )

    capteur_arbre_cames_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du capteur d'arbre à cames HTVA"),
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
    # ========================================================
    # TECHNICIEN
    # ========================================================

    if not self.tech_technicien and hasattr(self, "_user"):
        self.assign_technicien(self._user)

    # ========================================================
    # KILOMÉTRAGE
    # ========================================================

    if self.voiture_exemplaire_id:
        voiture = self.voiture_exemplaire

        kilometrage_allumage = self.kilometrage_allumage or 0
        kilometres_chassis = voiture.kilometres_chassis or 0

        # Si le kilométrage Allumage est supérieur au châssis
        if kilometrage_allumage > kilometres_chassis:
            voiture.__class__.objects.filter(
                pk=voiture.pk
            ).update(
                kilometres_chassis=kilometrage_allumage
            )

            # Synchronisation de l'objet en mémoire
            voiture.kilometres_chassis = kilometrage_allumage

        # Copie du kilométrage dans le contrôle Allumage
        self.kilometres_chassis = voiture.kilometres_chassis or 0

    # ========================================================
    # MAIN-D'ŒUVRE
    # ========================================================

    if self.main_oeuvre_id and self.voiture_exemplaire_id:
        task_name = (
            f"{_('Allumage')} "
            f"{self.voiture_exemplaire}"
        )

        self.main_oeuvre.__class__.objects.filter(
            pk=self.main_oeuvre_id
        ).update(
            descriptif=task_name
        )

        self.main_oeuvre.descriptif = task_name

    # ========================================================
    # SAUVEGARDE
    # ========================================================

    super().save(*args, **kwargs)




def generer_rapport_remplacement(self):
    lignes = []
    total_general = Decimal("0.00")
    etats_labels = dict(EtatAllumage.choices)

    for field in self._meta.fields:
        field_name = field.name

        if not (
                isinstance(field, models.CharField)
                and field.choices == EtatAllumage.choices
        ):
            continue

        valeur = getattr(self, field_name, None)

        if valeur not in (
                EtatAllumage.A_REMPLACER,
                EtatAllumage.REMPLACE,
        ):
            continue

        # -------------------------
        # Prix
        # -------------------------

        prix = getattr(
            self,
            f"{field_name}_prix",
            None,
        )

        if prix is None:
            prix = getattr(
                self,
                f"{field_name}_prix_achat",
                Decimal("0.00"),
            )

        prix = Decimal(str(prix or "0.00"))

        # -------------------------
        # Quantité
        # -------------------------

        quantite = getattr(
            self,
            f"{field_name}_quantite",
            1,
        )

        quantite = Decimal(
            str(
                quantite
                if quantite not in (None, 0)
                else 1
            )
        )

        # -------------------------
        # Fabricant
        # -------------------------

        fabricant_field_name = f"{field_name}_fabricant"

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
                fabricant_label = get_fabricant_display()
            else:
                fabricant_label = fabricant

        # -------------------------
        # Total
        # -------------------------

        total = (prix * quantite).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        total_general += total

        lignes.append({
            "champ": field.verbose_name,
            "code": field_name,

            "etat": valeur,
            "etat_label": etats_labels.get(
                valeur,
                valeur,
            ),

            "fabricant": fabricant,
            "fabricant_label": fabricant_label,

            "prix": prix.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            ),

            "quantite": quantite,
            "total": total,
        })

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
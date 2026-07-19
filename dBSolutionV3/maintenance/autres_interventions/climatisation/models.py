from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES

from maintenance.models import Maintenance
from maintenance.services import sync_maintenance
from utils.mixin import TechnicienMixin


# ==========================================================
# CHOIX
# ==========================================================

class EtatClimatisation(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class EtatOperationClimatisation(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("À faire")
    FAIT = "FAIT", _("Fait")
    NON_NECESSAIRE = "NON_NECESSAIRE", _("Non nécessaire")


class QualiteGazClimatisation(models.TextChoices):
    BONNE = "BONNE", _("Bonne")
    CONTAMINE = "CONTAMINE", _("Contaminé")
    HUMIDE = "HUMIDE", _("Présence d'humidité")
    INCONNUE = "INCONNUE", _("Inconnue")


class ResultatFuiteClimatisation(models.TextChoices):
    AUCUNE = "AUCUNE", _("Aucune fuite")
    FAIBLE = "FAIBLE", _("Fuite faible")
    IMPORTANTE = "IMPORTANTE", _("Fuite importante")
    NON_CONTROLEE = "NON_CONTROLEE", _("Non contrôlée")


class TypeGazClimatisation(models.TextChoices):
    R134A = "R134A", _("R134a")
    R1234YF = "R1234YF", _("R1234yf")
    R744 = "R744", _("R744 / CO₂")
    AUTRE = "AUTRE", _("Autre")


# ==========================================================
# MODÈLE
# ==========================================================

class Climatisation(TechnicienMixin, models.Model):

    # ------------------------------------------------------
    # CONFIGURATION TVA
    # ------------------------------------------------------

    PAYS_CHOICES = [
        ("BE", _("Belgique")),
        ("LU", _("Luxembourg")),
        ("DE", _("Allemagne")),
    ]

    TVA_PIECES = {
        "BE": 21,
        "LU": 16,
        "DE": 19,
    }

    # ------------------------------------------------------
    # RELATIONS
    # ------------------------------------------------------

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="climatisation",
        null=True,
        blank=True,
        verbose_name=_("Maintenance"),
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="climatisation",
        verbose_name=_("Véhicule"),
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres châssis"),
    )

    kilometrage_clim = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du contrôle de la climatisation"),
    )

    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES,
        default="BE",
        verbose_name=_("Pays"),
    )

    # ------------------------------------------------------
    # GAZ DE CLIMATISATION
    # ------------------------------------------------------

    type_gaz = models.CharField(
        max_length=20,
        choices=TypeGazClimatisation.choices,
        default=TypeGazClimatisation.R134A,
        verbose_name=_("Type de gaz"),
    )

    autre_type_gaz = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Autre type de gaz"),
    )

    poids_gaz_constructeur = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name=_("Poids de gaz préconisé par le constructeur en grammes"),
    )

    poids_gaz_recupere = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name=_("Poids de gaz récupéré en grammes"),
    )

    poids_gaz_injecte = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name=_("Poids de gaz injecté en grammes"),
    )

    qualite_gaz = models.CharField(
        max_length=25,
        choices=QualiteGazClimatisation.choices,
        default=QualiteGazClimatisation.INCONNUE,
        verbose_name=_("Qualité du gaz"),
    )

    pourcentage_purete_gaz = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        blank=True,
        verbose_name=_("Pureté du gaz en pourcentage"),
    )

    # ------------------------------------------------------
    # HUILE ET TRACEUR
    # ------------------------------------------------------

    ajout_huile = models.CharField(
        max_length=25,
        choices=EtatOperationClimatisation.choices,
        default=EtatOperationClimatisation.A_FAIRE,
        verbose_name=_("Ajout d'huile de climatisation"),
    )

    quantite_huile_recuperee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name=_("Quantité d'huile récupérée en millilitres"),
    )

    quantite_huile_injectee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name=_("Quantité d'huile injectée en millilitres"),
    )

    type_huile = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Type d'huile"),
    )

    ajout_traceur = models.CharField(
        max_length=25,
        choices=EtatOperationClimatisation.choices,
        default=EtatOperationClimatisation.A_FAIRE,
        verbose_name=_("Ajout de traceur"),
    )

    quantite_traceur = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name=_("Quantité de traceur en millilitres"),
    )

    # ------------------------------------------------------
    # MISE SOUS VIDE
    # ------------------------------------------------------

    mise_sous_vide = models.CharField(
        max_length=25,
        choices=EtatOperationClimatisation.choices,
        default=EtatOperationClimatisation.A_FAIRE,
        verbose_name=_("Mise sous vide"),
    )

    duree_mise_sous_vide_minutes = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Durée de mise sous vide en minutes"),
    )

    pression_vide_atteinte = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Pression de vide atteinte"),
    )

    tenue_du_vide = models.CharField(
        max_length=25,
        choices=EtatOperationClimatisation.choices,
        default=EtatOperationClimatisation.A_FAIRE,
        verbose_name=_("Contrôle de tenue du vide"),
    )

    # ------------------------------------------------------
    # CONTRÔLE DES FUITES
    # ------------------------------------------------------

    controle_fuites = models.CharField(
        max_length=25,
        choices=EtatOperationClimatisation.choices,
        default=EtatOperationClimatisation.A_FAIRE,
        verbose_name=_("Contrôle des fuites"),
    )

    resultat_fuites = models.CharField(
        max_length=25,
        choices=ResultatFuiteClimatisation.choices,
        default=ResultatFuiteClimatisation.NON_CONTROLEE,
        verbose_name=_("Résultat du contrôle des fuites"),
    )

    methode_controle_fuites = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Méthode de contrôle des fuites"),
        help_text=_(
            "Exemple : traceur UV, azote hydrogéné, détecteur électronique."
        ),
    )

    emplacement_fuite = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Emplacement de la fuite"),
    )

    # ------------------------------------------------------
    # COMPOSANTS
    # ------------------------------------------------------

    tuyaux = models.CharField(
        max_length=25,
        choices=EtatClimatisation.choices,
        default=EtatClimatisation.OK,
        verbose_name=_("Tuyaux de climatisation"),
    )

    tuyaux_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA des tuyaux"),
    )

    tuyaux_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    valves = models.CharField(
        max_length=25,
        choices=EtatClimatisation.choices,
        default=EtatClimatisation.OK,
        verbose_name=_("Valves de climatisation"),
    )

    valves_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA des valves"),
    )

    valves_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    deshydrateur = models.CharField(
        max_length=25,
        choices=EtatClimatisation.choices,
        default=EtatClimatisation.OK,
        verbose_name=_("Déshydrateur"),
    )

    deshydrateur_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA du déshydrateur"),
    )

    deshydrateur_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    condenseur = models.CharField(
        max_length=25,
        choices=EtatClimatisation.choices,
        default=EtatClimatisation.OK,
        verbose_name=_("Condenseur"),
    )

    condenseur_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA du condenseur"),
    )

    condenseur_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    compresseur = models.CharField(
        max_length=25,
        choices=EtatClimatisation.choices,
        default=EtatClimatisation.OK,
        verbose_name=_("Compresseur de climatisation"),
    )

    compresseur_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA du compresseur"),
    )

    compresseur_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    evaporateur = models.CharField(
        max_length=25,
        choices=EtatClimatisation.choices,
        default=EtatClimatisation.OK,
        verbose_name=_("Évaporateur"),
    )

    evaporateur_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA de l'évaporateur"),
    )

    evaporateur_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    recharge = models.CharField(
        max_length=25,
        choices=EtatClimatisation.choices,
        default=EtatClimatisation.OK,
        verbose_name=_("Recharge de gaz"),
    )

    recharge_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    recharge_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité en grammes"),
    )

    # ------------------------------------------------------
    # MESURES DE FONCTIONNEMENT
    # ------------------------------------------------------

    pression_basse = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name=_("Pression basse"),
    )

    pression_haute = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name=_("Pression haute"),
    )

    temperature_air_entree = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name=_("Température d'air à l'entrée en °C"),
    )

    temperature_air_sortie = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name=_("Température d'air à la sortie en °C"),
    )

    # ------------------------------------------------------
    # INFORMATIONS COMPLÉMENTAIRES
    # ------------------------------------------------------

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
        related_name="climatisation",
        verbose_name=_("Main d'œuvre"),
    )

    # ------------------------------------------------------
    # TECHNICIEN
    # ------------------------------------------------------

    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="climatisation",
    )

    tech_nom_technicien = models.CharField(
        _("Nom du technicien"),
        max_length=255,
        blank=True,
    )

    tech_role_technicien = models.CharField(
        _("Rôle du technicien"),
        max_length=255,
        blank=True,
    )

    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="climatisation",
    )
    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date"),
    )

    created_at = models.DateTimeField(
        _("Créé le"),
        auto_now_add=True,
        blank=True,
        null=True,
    )

    updated_at = models.DateTimeField(
        _("Mis à jour le"),
        auto_now=True,
        blank=True,
        null=True,
    )

    # ------------------------------------------------------
    # META
    # ------------------------------------------------------

    class Meta:
        verbose_name = _("Climatisation")
        verbose_name_plural = _("Climatisations")
        ordering = ["-date"]

    def __str__(self):
        return (
            f"Contrôle climatisation - "
            f"{self.voiture_exemplaire} - {self.date:%d/%m/%Y}"
        )

    # ------------------------------------------------------
    # TECHNICIEN
    # ------------------------------------------------------

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    # ------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------

    def clean(self):

        super().clean()

        erreurs = {}

        if (
                self.voiture_exemplaire_id
                and self.kilometrage_clim is not None
        ):
            kilometres_actuels = (
                    self.voiture_exemplaire.kilometres_chassis or 0
            )
            if self.kilometrage_clim < kilometres_actuels:
                raise ValidationError({
                    "kilometrage_clim": _(
                            "Le kilométrage du contrôle de climatisation "
                            "ne peut pas être inférieur au kilométrage "
                            "actuel du véhicule."
                    )
                })
        if self.type_gaz == TypeGazClimatisation.AUTRE and not self.autre_type_gaz:
            erreurs["autre_type_gaz"] = _(
                "Veuillez préciser le type de gaz utilisé."
            )

        if self.poids_gaz_constructeur < 0:
            erreurs["poids_gaz_constructeur"] = _(
                "Le poids de gaz constructeur ne peut pas être négatif."
            )

        if self.poids_gaz_recupere < 0:
            erreurs["poids_gaz_recupere"] = _(
                "Le poids de gaz récupéré ne peut pas être négatif."
            )

        if self.poids_gaz_injecte < 0:
            erreurs["poids_gaz_injecte"] = _(
                "Le poids de gaz injecté ne peut pas être négatif."
            )

        if erreurs:
            raise ValidationError(erreurs)

    # ------------------------------------------------------
    # CALCUL GÉNÉRIQUE D'UNE PIÈCE
    # ------------------------------------------------------

    def calcul_piece(self, prefix):
        prix = getattr(self, f"{prefix}_prix", Decimal("0")) or Decimal("0")
        quantite = getattr(self, f"{prefix}_quantite", 0) or 0

        return {
            "prix": prix,
            "quantite": quantite,
            "total": prix * quantite,
        }

    # ------------------------------------------------------
    # ENREGISTREMENT
    # ------------------------------------------------------

    def save(self, *args, **kwargs):

        if not self.tech_technicien and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        if (
            self.voiture_exemplaire
            and self.kilometrage_clim is not None
            and self.kilometrage_clim
            > self.voiture_exemplaire.kilometres_chassis
        ):
            self.voiture_exemplaire.kilometres_chassis = (
                self.kilometrage_clim
            )

            self.voiture_exemplaire.save(
                update_fields=["kilometres_chassis"]
            )

        if self.voiture_exemplaire:
            self.kilometres_chassis = (
                self.voiture_exemplaire.kilometres_chassis
            )

        super().save(*args, **kwargs)

        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = (
                f"{_('Climatisation')} {self.voiture_exemplaire}"
            )

            if self.main_oeuvre.descriptif != task_name:
                self.main_oeuvre.descriptif = task_name
                self.main_oeuvre.save(
                    update_fields=["descriptif"]
                )

        sync_maintenance(
            self,
            Maintenance.TypeMaintenance.CLIMATISATION,
        )

    # ------------------------------------------------------
    # RAPPORT DES PIÈCES À REMPLACER
    # ------------------------------------------------------

    from decimal import Decimal

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        prefixes_pieces = [
            "tuyaux",
            "valves",
            "deshydrateur",
            "condenseur",
            "compresseur",
            "evaporateur",
            "recharge",
        ]

        for prefix in prefixes_pieces:
            valeur = getattr(self, prefix)

            # Pièces à remplacer ET déjà remplacées
            if valeur in (
                    EtatClimatisation.NOT_OK,
                    EtatClimatisation.REMPLACE,
            ):
                field = self._meta.get_field(prefix)

                prix = (
                        getattr(self, f"{prefix}_prix", Decimal("0.00"))
                        or Decimal("0.00")
                )
                prix = Decimal(str(prix))

                quantite = (
                        getattr(self, f"{prefix}_quantite", 0)
                        or 0
                )
                quantite = Decimal(str(quantite))

                total = prix * quantite
                total_general += total

                rapport.append({
                    "champ": field.verbose_name,
                    "code": prefix,
                    "etat": valeur,
                    "etat_label": dict(
                        EtatClimatisation.choices
                    ).get(valeur, valeur),
                    "prix": prix,
                    "quantite": quantite,
                    "total": total,
                })

        return {
            "lignes": rapport,
            "total_general": total_general,
        }
    # ------------------------------------------------------
    # PROPRIÉTÉS
    # ------------------------------------------------------

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

    @property
    def difference_poids_gaz(self):
        """
        Différence entre le poids préconisé par le constructeur
        et le poids récupéré avant recharge.
        """
        constructeur = self.poids_gaz_constructeur or Decimal("0")
        recupere = self.poids_gaz_recupere or Decimal("0")

        return constructeur - recupere

    @property
    def ecart_temperature(self):
        """
        Différence entre la température d'entrée et la température
        de sortie de l'air.
        """
        entree = self.temperature_air_entree or Decimal("0")
        sortie = self.temperature_air_sortie or Decimal("0")

        return entree - sortie


    def sync_kilometrage(self):
        if not self.voiture_exemplaire:
            return

        if self.kilometrage_clim is None:
            return

        km = Decimal(str(self.kilometrage_clim))

        voiture = self.voiture_exemplaire
        voiture.refresh_from_db(fields=["kilometres_chassis"])

        if km < voiture.kilometres_chassis:
            raise ValidationError("Kilométrage invalide")

        # 🔥 SOURCE UNIQUE
        voiture.kilometres_chassis = km
        voiture.save(update_fields=["kilometres_chassis"])

        # 🔁 copie locale
        self.kilometres_chassis = km
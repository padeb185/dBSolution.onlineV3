from datetime import timezone
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import RouesSerrageEtat, TAUX_HORAIRE_CHOICES
from maintenance.models import Maintenance
from django.conf import settings
from maintenance.nettoyage_exterieur.models import EtatAjouter
from utils.mixin import TechnicienMixin





class NettoyageEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("A faire")
    FAIT = "FAIT", _("Fait")
    REPORTER = "REPORTER", _("Reporter")
    PROPRE = "PROPRE", _("Propre")




class NettoyageInterieur(TechnicienMixin,models.Model):
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


    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="nettoyages_interieur",
        verbose_name=_("Nettoyage Interieur"),
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="nettoyages_interieur",
        verbose_name=_("Véhicule")
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_net_int = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du Nettoyage intérieur"),
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    nettoyage_interieur_vitres =  models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Vitres")

    )
    nettoyage_interieur_pare_brise =  models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Pare-brise")
    )
    nettoyage_interieur_aspirateur =  models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Aspirateur")
    )
    nettoyage_interieur_interieur_portes = models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Ouvrants de portes")
    )
    nettoyage_interieur_tableau_de_bord =models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Tableau de bord")
    )
    nettoyage_interieur_plastiques = models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Plastiques")
    )

    nettoyage_interieur_console = models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Console centrale")
    )

    nettoyage_interieur_produits = models.CharField(
        max_length=25,
        choices=EtatAjouter.choices,
        default=EtatAjouter.SANS,
        verbose_name=_("Produits")
    )

    nettoyage_interieur_produits_prix = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name=_("Prix d'achat HTVA"))

    nettoyage_interieur_produits_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"))

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

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="nettoyage_interieur",
        verbose_name=_("Main d'oeuvre")
    )

    # Champ pour l’utilisateur affecté (technicien)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Utilisateur"),
        related_name="nettoyage_interieur"
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
        related_name="nettoyages_interieur_societe"  # unique
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe


    class Meta:
        verbose_name = _("Nettoyage intérieur")
        verbose_name_plural = _("Nettoyages intérieurs")

    def __str__(self):
        voiture = getattr(self, "voiture_exemplaire", None)
        date = getattr(self, "date", None)

        if not voiture:
            return "Nettoyage intérieur (incomplet)"

        if not date:
            return f"Nettoyage intérieur – {voiture}"

        return f"Nettoyage intérieur – {voiture} ({date:%Y-%m-%d})"

    def clean(self):
        super().clean()

        if self.voiture_exemplaire_id and self.kilometrage_net_int is not None:
            if self.kilometrage_net_int < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_net_int": _(
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture "
                        f"({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):

        ancien_kilometrage = 0

        # =========================
        # TECHNICIEN
        # =========================
        if not self.tech_technicien_id and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = (
                    _("Nettoyage intérieur")
                    + " "
                    + str(self.voiture_exemplaire)
            )

            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(
                update_fields=["descriptif"]
            )

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = (
                Maintenance.TypeMaintenance.NETTOYAGE_INTERIEUR
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                ]
            )

        # =========================
        # KILOMÉTRAGE AVANT INTERVENTION
        # =========================
        if self.voiture_exemplaire_id:

            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            ancien_kilometrage = (
                    voiture.kilometres_chassis or 0
            )

            # Snapshot du kilométrage avant intervention
            self.kilometres_chassis = ancien_kilometrage

            # =========================
            # CALCUL VARIATION
            # =========================
            if self.kilometrage_net_int is not None:

                self.kilometrage_variation = (
                        self.kilometrage_net_int
                        - ancien_kilometrage
                )

            else:
                self.kilometrage_variation = 0

        # =========================
        # SAUVEGARDE NETTOYAGE EXTÉRIEUR
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if (
                self.voiture_exemplaire_id
                and self.kilometrage_net_int is not None
        ):

            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            if (
                    self.kilometrage_net_int
                    > (voiture.kilometres_chassis or 0)
            ):
                voiture.kilometres_chassis = (
                    self.kilometrage_net_int
                )

                voiture.save(
                    update_fields=["kilometres_chassis"]
                )

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        # Produit ajouté pendant le nettoyage intérieur
        if self.nettoyage_interieur_produits == EtatAjouter.AJOUTER:
            prix = self.nettoyage_interieur_produits_prix or Decimal("0.00")
            quantite = self.nettoyage_interieur_produits_quantite or 0

            prix = Decimal(str(prix))
            quantite = Decimal(str(quantite))

            prix_unitaire = prix.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total = (prix_unitaire * quantite).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total_general += total

            rapport.append({
                "nom": _("Produits de nettoyage intérieur"),

                # Valeur technique utilisée dans le template
                "etat": self.nettoyage_interieur_produits,

                # Libellé affiché
                "etat_label": self.get_nettoyage_interieur_produits_display(),

                "prix": prix_unitaire,
                "prix_unitaire": prix_unitaire,
                "quantite": quantite,
                "total": total,
            })

        total_general = total_general.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        return {
            "lignes": rapport,
            "pieces": rapport,
            "rapport": rapport,
            "total_pieces": total_general,
            "total_general": total_general,
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

        temps_minutes = Decimal(
            str(self.main_oeuvre.temps_minutes or 0)
        )

        taux_horaire = Decimal(
            str(self.taux_horaire or Decimal("50.00"))
        )

        cout = (
                temps_minutes
                / Decimal("60")
                * taux_horaire
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


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

        if self.voiture_exemplaire_id and self.kilometrage_net_int:

            if self.kilometrage_net_int < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError("Le kilométrage ne peut pas diminuer.")

            if self.kilometrage_net_int > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_net_int
                self.voiture_exemplaire.kilometres_dernier_entretien = self.kilometrage_net_int
                self.voiture_exemplaire.date_derniere_intervention = timezone.now().date()

                self.voiture_exemplaire.update_kilometres()
                self.voiture_exemplaire.save()

        if self.voiture_exemplaire_id:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Nettoyage Extérieur") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        super().save(*args, **kwargs)

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        etat_produit = self.nettoyage_interieur_produits

        # Le produit est ajouté uniquement lorsque l'état vaut AJOUTER
        if etat_produit == EtatAjouter.AJOUTER:
            prix = Decimal(
                str(
                    self.nettoyage_interieur_produits_prix
                    or Decimal("0.00")
                )
            )

            quantite = Decimal(
                str(
                    self.nettoyage_interieur_produits_quantite
                    or 0
                )
            )

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
                "nom": _("Produits de nettoyage"),
                "etat": self.get_nettoyage_interieur_produits_display(),
                "prix": prix_unitaire,
                "prix_unitaire": prix_unitaire,
                "quantite": quantite,
                "total": total,
            })

        return {
            "pieces": rapport,
            "rapport": rapport,
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


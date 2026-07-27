from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from maintenance.choices import RouesSerrageEtat, TAUX_HORAIRE_CHOICES
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class NettoyageEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("A faire")
    FAIT = "FAIT", _("Fait")
    REPORTER = "REPORTER", _("Reporter")
    PROPRE = "PROPRE", _("Propre")

class EtatAjouter(models.TextChoices):
    SANS = "SANS", _("Sans")
    AJOUTER = "AJOUTER", _("Ajouter")



class NettoyageExterieur(TechnicienMixin, models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="nettoyages_exterieur",
        verbose_name=_("Nettoyage extérieur")
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="nettoyages_exterieur",
        verbose_name=_("Véhicule")
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_net_ext = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du Nettoyage extérieur"),

    )

    # --- Nettoyage extérieur ---
    nettoyage_exterieur_traces_gomme = models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Traces de gomme")
    )
    nettoyage_exterieur_carrosserie = models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Carrosserie")
    )
    nettoyage_exterieur_jantes = models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Jantes")
    )
    nettoyage_exterieur_sechage = models.CharField(
        max_length=25,
        choices=NettoyageEtat.choices,
        default=NettoyageEtat.A_FAIRE,
        verbose_name=_("Séchage")
    )

    nettoyage_exterieur_produits = models.CharField(
        max_length=25,
        choices=EtatAjouter.choices,
        default=EtatAjouter.SANS,
        verbose_name=_("Produits")
    )

    nettoyage_exterieur_produits_prix = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name=_("Prix d'achat HTVA"))

    nettoyage_exterieur_produits_quantite = models.IntegerField(
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
        related_name="nettoyage_exterieur",
        verbose_name=_("Main d'oeuvre")
    )

    # Champ pour l’utilisateur affecté (technicien)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Utilisateur"),
        related_name="nettoyage_exterieur"
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
        related_name="nettoyages_exterieur_societe"  # unique
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
        verbose_name = _("Nettoyage extérieur")
        verbose_name_plural = _("Nettoyages extérieurs")

    def __str__(self):
        return f"Nettoyage extérieur – {self.voiture_exemplaire} ({self.date:%Y-%m-%d})"


    def clean(self):
        super().clean()

        if self.voiture_exemplaire_id and self.kilometrage_net_ext is not None:
            if self.kilometrage_net_ext < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_net_ext": _(
                        f"Le kilométrage du check-up ({self.kilometrage_net_ext}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture "
                        f"({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):

        if self.voiture_exemplaire_id and self.kilometrage_net_ext:
            if self.kilometrage_net_ext > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_net_ext
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        if self.voiture_exemplaire_id:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien_id and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Nettoyage extérieur") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.NETTOYAGE_EXTERIEUR
            self.maintenance.voiture_exemplaire = self.voiture_exemplaire
            self.maintenance.save(update_fields=["type_maintenance", "voiture_exemplaire"])

        super().save(*args, **kwargs)

    def generer_rapport_remplacement(self):
            rapport = []
            total_general = Decimal("0.00")

            # Produit ajouté pendant le nettoyage
            if self.nettoyage_exterieur_produits == EtatAjouter.AJOUTER:
                prix = self.nettoyage_exterieur_produits_prix or Decimal("0.00")
                quantite = self.nettoyage_exterieur_produits_quantite or 0

                prix = Decimal(str(prix))
                quantite = Decimal(str(quantite))

                total = prix * quantite

                total = total.quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                )

                total_general += total

                rapport.append({
                    "nom": _("Produits de nettoyage"),
                    "etat": self.get_nettoyage_exterieur_produits_display(),
                    "prix": prix.quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP,
                    ),
                    "prix_unitaire": prix.quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP,
                    ),
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


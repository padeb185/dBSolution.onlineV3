from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance
from maintenance.services import sync_maintenance
from maintenance.models import Maintenance


class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")


class Abs(TechnicienMixin, models.Model):

    # -------------------------
    # CONFIG TVA
    # -------------------------
    PAYS_CHOICES = [
        ('BE', _("Belgique")),
        ('LU', _("Luxembourg")),
        ('DE', _("Allemagne")),
    ]

    TVA_PIECES = {
        'BE': 21,
        'LU': 16,
        'DE': 19,
    }

    # -------------------------
    # RELATIONS
    # -------------------------
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="abs",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="abs",
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name= _("Kilomètres chassis")
    )

    # -------------------------
    # INFOS
    # -------------------------
    kilometrage_abs = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name= _("Kilométrage au moment du controle ABS ")
    )

    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES
    )

    # -------------------------
    # PIECES
    # -------------------------
    def piece_fields(prefix):
        return {
            f"{prefix}": models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK),
            f"{prefix}_prix": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_quantite": models.IntegerField(default=0),
        }



    pompe_abs = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Pompe d'ABS"))
    pompe_abs_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva de la pompe ABS"))
    pompe_abs_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    calculateur_abs = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Calculateur d'ABS"))
    calculateur_abs_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva du calculateur d'ABS"))
    calculateur_abs_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))



    capteur_abs_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capteur ABS avant droit"))
    capteur_abs_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capteur ABS avant gauche"))
    capteur_abs_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capteur ABS arrière droit"))
    capteur_abs_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capteur ABS arrière gauche"))

    capteur_abs = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capteur ABS"))
    capteur_abs_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva du capteur"))
    capteur_abs_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))



    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
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
        related_name="abs",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="abs"
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
        related_name="abs"
    )

    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)


    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    class Meta:
        verbose_name = _("système_abs")
        verbose_name_plural = _("Systèmes_abs")

    def __str__(self):
        return f"Controle abs - {self.voiture_exemplaire} {self.date}"

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_abs is not None:
            if self.kilometrage_abs < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_système_abs': _(
                        f"Le kilométrage du système ABS ({self.kilometrage_abs}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    # -------------------------
    # CALCUL GENERIQUE
    # -------------------------
    def calcul_piece(self, prefix):

        prix = getattr(self, f"{prefix}_prix", Decimal("0"))
        quantite = getattr(self, f"{prefix}_quantite", 0)

        total = prix * quantite

        return {
            "prix": prix,
            "quantite": quantite,
            "total": total,
        }

    # -------------------------
    # SAVE
    # -------------------------
    def save(self, *args, **kwargs):

        # ----------------------------
        # CALCUL DES PIÈCES
        # ----------------------------
        self.calcul_piece("pompe_abs")
        self.calcul_piece("calculateur_abs")
        self.calcul_piece("capteur_abs")

        # ----------------------------
        # TECHNICIEN AUTO
        # ----------------------------
        if not self.tech_technicien and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # ----------------------------
        # MAIN D'OEUVRE AUTO DESCRIPTIF
        # ----------------------------
        if self.main_oeuvre:
            task_name = ""

            if self.maintenance:
                task_name = str(self.maintenance)

            elif self.voiture_exemplaire:
                task_name = _("ABS") + " " + str(self.voiture_exemplaire)

            # update descriptif automatiquement
            if hasattr(self.main_oeuvre, "descriptif"):
                self.main_oeuvre.descriptif = task_name
                self.main_oeuvre.save(update_fields=["descriptif"])

        # ----------------------------
        # MAJ KILOMÉTRAGE
        # ----------------------------
        if self.voiture_exemplaire and self.kilometrage_abs:
            if self.kilometrage_abs > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_abs
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # copie locale
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        # ----------------------------
        # SAVE ABS
        # ----------------------------
        super().save(*args, **kwargs)

        # ----------------------------
        # SYNC MAINTENANCE
        # ----------------------------
        sync_maintenance(
            self,
            Maintenance.TypeMaintenance.ABS
        )
    # -------------------------
    # RAPPORT
    # -------------------------
    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0")

        for field in self._meta.fields:
            field_name = field.name

            # On ne garde que les champs état
            if isinstance(field, models.CharField) and field.choices == EtatOKNotOK.choices:
                valeur = getattr(self, field_name)

                if valeur == EtatOKNotOK.NOT_OK:
                    prix = getattr(self, f"{field_name}_prix", Decimal("0"))
                    quantite = getattr(self, f"{field_name}_quantite", 0)

                    total = prix * quantite
                    total_general += total

                    rapport.append({
                        "champ": field.verbose_name,
                        "code": field_name,
                        "prix": prix,
                        "quantite": quantite,
                        "total": total,
                    })

        return {
            "lignes": rapport,
            "total_general": total_general
        }

    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"
        return self.main_oeuvre.temps_display
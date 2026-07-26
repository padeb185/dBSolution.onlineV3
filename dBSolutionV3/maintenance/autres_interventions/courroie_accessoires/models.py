from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import StepValueValidator

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import RouesSerrageEtat
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance

class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class CourroieAccessoires(TechnicienMixin, models.Model):

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
        related_name="courroie_daccess",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="courroie_daccess",
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    # -------------------------
    # INFOS
    # -------------------------
    kilometrage_access = models.PositiveIntegerField(
        verbose_name= _("Kilométrage de la courroie d'accessoires")
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




    # Courroie
    courroie_daccessoires = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Courroie d'accessoires"))
    courroie_daccessoires_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva de la courroie"))
    courroie_daccessoires_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # Courroie
    galet_tendeur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Galet Tendeur"))
    galet_tendeur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva du galet"))
    galet_tendeur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # Courroie
    poulie_damper = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Poulie Damper"))
    poulie_damper_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva de la poulie"))
    poulie_damper_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))


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

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="courroie_daccess"
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
        related_name="courroie_daccess"
    )
    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )
    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courroie_daccess",
        verbose_name=_("Main d'oeuvre")
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

    def clean(self):
        super().clean()

        if self.voiture_exemplaire and self.kilometrage_access is not None:
            if self.kilometrage_access > self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_courroie d' accessoires": _(
                        "Le kilométrage de la courroie d'accessoires ne peut pas être supérieur au kilométrage du véhicule."
                    )
                })

        if self.serrage_roues == RouesSerrageEtat.A_FAIRE:
            raise ValidationError({
                "serrage_roues": _(
                    "Vous devez indiquer si le serrage des roues a été effectué avant d'enregistrer ce contrôle."
                )
            })

    class Meta:
        verbose_name = _("Courroie d'accessoire")
        verbose_name_plural = _("Courroies d'accessoires")

    def __str__(self):
        return f"Courroie d'accessoires moteur - {self.voiture_exemplaire}"



    # -------------------------
    # CALCUL GENERIQUE
    # -------------------------
    def calcul_piece(self, prefix):
        prix = getattr(self, f"{prefix}_prix", 0)
        quantite = getattr(self, f"{prefix}_quantite", 0)

        if not prix or not self.pays:
            return

        tva_rate = Decimal(self.TVA_PIECES.get(self.pays, 0)) / 100

        prix_htva = prix  # pas de marge dans ton modèle

        prix_htva = prix_htva.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        tva = (prix_htva * tva_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        prix_ttc = prix_htva + tva

        setattr(self, f"{prefix}_prix_vente_htva", prix_htva)
        setattr(self, f"{prefix}_tva_vente", tva)
        setattr(self, f"{prefix}_prix_ttc", prix_ttc)


    # -------------------------
    # SAVE
    # -------------------------
    def save(self, *args, **kwargs):

        # 🔥 synchro kilométrage AVANT save
        if hasattr(self, "sync_kilometrage"):
            self.sync_kilometrage()

        # Calculs
        self.calcul_piece("courroie_d'accessoires")


        # ----------------------------
        # MAIN D'OEUVRE AUTO DESCRIPTIF
        # ----------------------------
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Courroie d'accessoires") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])


        super().save(*args, **kwargs)

    from decimal import Decimal

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        for field in self._meta.fields:
            field_name = field.name

            # On ne garde que les champs avec les états
            if (
                    isinstance(field, models.CharField)
                    and field.choices == EtatOKNotOK.choices
            ):
                valeur = getattr(self, field_name)

                # À remplacer OU déjà remplacé
                if valeur in (
                        EtatOKNotOK.NOT_OK,
                        EtatOKNotOK.REMPLACE,
                ):
                    prix = (
                            getattr(self, f"{field_name}_prix", Decimal("0.00"))
                            or Decimal("0.00")
                    )
                    prix = Decimal(str(prix))

                    quantite = (
                            getattr(self, f"{field_name}_quantite", 0)
                            or 0
                    )
                    quantite = Decimal(str(quantite))

                    total = prix * quantite
                    total_general += total

                    rapport.append({
                        "champ": field.verbose_name,
                        "code": field_name,
                        "etat": valeur,
                        "etat_label": dict(
                            EtatOKNotOK.choices
                        ).get(valeur, valeur),
                        "prix": prix,
                        "quantite": quantite,
                        "total": total,
                    })

        return {
            "lignes": rapport,
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



    def sync_kilometrage(self):
        if not self.voiture_exemplaire:
            return

        if self.kilometrage_access is None:
            return

        km = Decimal(str(self.kilometrage_access))

        voiture = self.voiture_exemplaire
        voiture.refresh_from_db(fields=["kilometres_chassis"])

        if km < voiture.kilometres_chassis:
            raise ValidationError("Kilométrage invalide")

        # 🔥 SOURCE UNIQUE
        voiture.kilometres_chassis = km
        voiture.save(update_fields=["kilometres_chassis"])

        # 🔁 copie locale
        self.kilometres_chassis = km



   
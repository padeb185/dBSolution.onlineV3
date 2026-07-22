import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.niveaux.models import  (NiveauxEtat,
                                         HuileEtat, RefroidissementQualiteEtat)
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin




class TypeUtilisation(models.TextChoices):
    SOCIETE = "societe", _("Société")
    CLIENT = "client", _("Client")
    PRIVE = "prive", _("Privé")
    LOCATION = "location", _("Location")
    INTERNE = "interne", _("Interne")



class RemplacementMoteur(TechnicienMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)



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
        related_name="remplacement_moteur",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="remplacement_moteur",
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometres_moteur = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilometres du moteur à remplacer")
    )


    kilometres_remplacement_moteur = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres au remplacement moteur")
    )

    variation_kilometres = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation de kilomètres depuis le dernier entretien"),
        help_text=_("Calculé automatiquement : total - dernièr entretien")
    )

    remplacement_numero_moteurs= models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Numéro de série du moteur")
    )

    nombre_remplacements_moteurs = models.PositiveIntegerField(
        default=1,
        editable=False,
        verbose_name=_("Nombre de remplacements"),
    )

    nombre_moteurs_montes = models.PositiveIntegerField(
        default=1,
        editable=False,
        verbose_name=_("Nombre de moteurs montés"),
    )
    moteur_quantite = models.PositiveIntegerField(
        default=1,
        editable=False,
        verbose_name=_("Quantité")
    )

    moteurs_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Prix d'achat du moteur HTVA"),
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

    niveau_huile_etat = models.CharField(
        max_length=25,
        choices=NiveauxEtat.choices,
        default=NiveauxEtat.BON,
        verbose_name=_("Niveau d'huile")
    )

    niveau_huile_quantite = models.FloatField(
        default=0,
        verbose_name=_("Quantité d'huile ajoutée en litres"),
        validators=[StepValueValidator(0.1)]
    )

    niveau_huile_qualite = models.CharField(
        max_length=25,
        choices=HuileEtat.choices,
        default=HuileEtat.ZERO_30,
        verbose_name=_("Qualité d'huile")
    )
    niveau_huile_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Prix d'achat de l'huile HTVA"),
    )


    refroidissement_etat = models.CharField(
        max_length=25,
        choices=NiveauxEtat.choices,
        default=NiveauxEtat.BON,
        verbose_name=_("Niveau de liquide de refroidissement")
    )

    refroidissement_quantite = models.FloatField(
        default=0,
        verbose_name=_("Quantité de liquide de refroidissement ajoutée en litres"),
        validators=[StepValueValidator(0.1)]
    )

    refroidissement_qualite = models.CharField(
        max_length=25,
        choices=RefroidissementQualiteEtat.choices,
        default=RefroidissementQualiteEtat.G13,
        verbose_name=_("Qualité de liquide de refroidissement")
    )

    refroidissement_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Prix d'achat du liquide de refroidissement HTVA"),
    )


    remplacement_effectue = models.BooleanField(
        default=False,
        verbose_name=_("Remplacement effectué"),
    )

    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES
    )

    tva = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=21.00,
        choices=TVA_PIECES,
        verbose_name=_("TVA")
    )

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    tech_last_maintained_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="remplacement_moteur_maintained",
        verbose_name=_("Dernière maintenance effectuée par")
    )

    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="remplacement_moteur"
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
        related_name="remplacement_moteur"
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
        related_name="remplacement_moteur",
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




    def __str__(self):
        return f"{self.voiture_marque.nom_marque} {self.voiture_modele.nom_modele} {self.voiture_modele.nom_variante} - {self.immatriculation}"




    def clean(self):
        if self.voiture_exemplaire and self.voiture_exemplaire.kilometres_moteur is not None:
            if self.voiture_exemplaire.kilometres_moteur > self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometres_moteur": _(
                        "Le kilométrage du moteur ne peut pas être supérieur au kilométrage du véhicule."
                    )
                })

    def activer_remplacement(self):
        self.kilometres_remplacement_moteur = self.kilometres_chassis
        self.remplacement_effectue = True
        self.save()

    def save(self, *args, **kwargs):
        km = self.kilometres_chassis or 0

        is_new = not RemplacementMoteur.objects.filter(pk=self.pk).exists()

        if is_new and self.voiture_exemplaire_id:
            self.nombre_remplacements_moteurs = (
                    RemplacementMoteur.objects.filter(
                        voiture_exemplaire_id=self.voiture_exemplaire_id,
                        remplacement_effectue=True
                    ).count() + 1
            )

        if is_new and self.voiture_exemplaire_id:
            self.nombre_moteurs_total = (
                    RemplacementMoteur.objects.filter(
                        voiture_exemplaire=self.voiture_exemplaire,
                        remplacement_effectue=True
                    ).count() + 2
            )


        if not self.voiture_exemplaire:
            super().save(*args, **kwargs)
            return

        if self.remplacement_effectue:
            if not self.kilometres_remplacement_moteur:
                self.kilometres_remplacement_moteur = km

            self.voiture_exemplaire.kilometres_moteur = max(
                0,
                km - self.kilometres_remplacement_moteur
            )
        else:
            self.voiture_exemplaire.kilometres_moteur = km

        self.voiture_exemplaire.save(update_fields=["kilometres_moteur"])

        super().save(*args, **kwargs)

        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Remplacement moteur") + " " + str(self.voiture_exemplaire)

            if self.main_oeuvre.descriptif != task_name:
                self.main_oeuvre.descriptif = task_name
                self.main_oeuvre.save(update_fields=["descriptif"])

        if not self.voiture_exemplaire:
            super().save(*args, **kwargs)
            return

        if self.remplacement_effectue and self.kilometres_remplacement_moteur:
            self.voiture_exemplaire.kilometres_moteur = max(
                0,
                km - self.kilometres_remplacement_moteur
            )
        else:
            self.voiture_exemplaire.kilometres_moteur = km

        self.voiture_exemplaire.save(update_fields=["kilometres_moteur"])


        # ----------------------------
        # MAIN D'OEUVRE AUTO DESCRIPTIF
        # ----------------------------
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Remplacement moteur") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])


        super().save(*args, **kwargs)

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        for field in self._meta.fields:
            field_name = field.name

            # Uniquement les champs d'état utilisant EntretienEtat
            if not (
                    isinstance(field, models.CharField)
                    and field.choices == NiveauxEtat.choices
            ):
                continue

            etat = getattr(self, field_name, None)

            if etat not in [
                NiveauxEtat.BON,
                NiveauxEtat.AJOUTER,
            ]:
                continue

            nom_champ_prix = f"{field_name}_prix"
            nom_champ_quantite = f"{field_name}_quantite"
            nom_champ_oem = f"{field_name}_oem"

            # Prix sécurisé
            prix = getattr(
                self,
                nom_champ_prix,
                Decimal("0.00"),
            )

            if prix is None:
                prix = Decimal("0.00")

            prix = Decimal(str(prix))

            # Quantité sécurisée
            quantite = getattr(
                self,
                nom_champ_quantite,
                0,
            )

            if quantite is None:
                quantite = 0

            quantite = Decimal(str(quantite))

            # OEM sécurisé
            numero_oem = getattr(
                self,
                nom_champ_oem,
                "",
            ) or ""

            total = (
                    prix * quantite
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total_general += total

            rapport.append({
                "champ": field.verbose_name,
                "code": field_name,
                "etat": etat,
                "etat_label": dict(
                    NiveauxEtat.choices
                ).get(etat, etat),
                "oem": numero_oem,
                "prix": prix,
                "quantite": quantite,
                "total": total,
            })

        return {
            "lignes": rapport,
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

        total = (
                rapport["total_general"]
                + self.cout_main_oeuvre
        )

        return total.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import StepValueValidator
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import FabricantLubrifiant, TAUX_HORAIRE_CHOICES, TVAConfig, LiquideDirectionQualite, \
    HuileEtat, HuileBoiteNiveauxEtat, HuilePontEtat, RefroidissementQualiteEtat, LiquideFreinsQualite, LaveGlaceQualite, \
    RouesSerrageEtat
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin
from django.core.exceptions import ValidationError




class NiveauxEtat(models.TextChoices):
    BON = "BON", _("OK")
    AJOUTER = "AJOUTER", _("Ajouter")


class Niveau(TechnicienMixin, models.Model):


    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )


    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="Niveaux",
        verbose_name=_("Niveaux"),
        null=True,  # autorisé vide à la création
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="niveau_exemplaire",
        verbose_name="Kilomètres_niveaux",
        null=True, blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_niveaux = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment des niveaux"),

    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    moteur_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile moteur"))
    moteur_niveau_huile_fabricant = models.CharField(max_length=30,choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR,verbose_name=_("Fabricant"))
    moteur_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30, verbose_name=_("Qualité d'huile"))
    moteur_niveau_huile_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    moteur_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    boite_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile de boite"))
    boite_niveau_huile_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    boite_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileBoiteNiveauxEtat.choices,default=HuileBoiteNiveauxEtat.SEPTANTE_CINQ,verbose_name=_("Qualité d'huile"))
    boite_niveau_huile_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    boite_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    pont_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile de pont"))
    pont_niveau_huile_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    pont_niveau_huile_qualite = models.CharField(max_length=25, choices=HuilePontEtat.choices,default=HuilePontEtat.SEPTANTE_CINQ80,verbose_name=_("Qualité d'huile"))
    pont_niveau_huile_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité ajoutée en litres"),validators=[StepValueValidator(0.1)])
    pont_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    refroidissement_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de refroidissement"))
    refroidissement_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices, default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    refroidissement_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices,default=RefroidissementQualiteEtat.G13,verbose_name=_("Qualité de liquide de refroidissement"))
    refroidissement_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité de liquide ajoutée en litres"),validators=[StepValueValidator(0.1)])
    refroidissement_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    frein_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de freins"))
    frein_liquide_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    frein_liquide_qualite = models.CharField(max_length=25, choices=LiquideFreinsQualite.choices,default=LiquideFreinsQualite.DOT4,verbose_name=_("Qualité de liquide de freins"))
    frein_liquide_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=2,  verbose_name=_("Quantité de liquide ajoutée en litres"), validators=[StepValueValidator(0.1)])
    frein_liquide_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    lave_glace_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de lave-glace"))
    lave_glace_liquide_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    lave_glace_liquide_qualite = models.CharField(max_length=25, choices=LaveGlaceQualite.choices,default=LaveGlaceQualite.HIVER,verbose_name=_("Qualité de liquide de lave glace"))
    lave_glace_liquide_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1, verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    lave_glace_liquide_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    direction_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de direction"))
    direction_liquide_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    direction_liquide_qualite = models.CharField(max_length=25, choices=LiquideDirectionQualite.choices,default= LiquideDirectionQualite.CHF_7_1 ,verbose_name=_("Qualité de liquide de direction"))
    direction_liquide_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1, verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    direction_liquide_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))




    remarques = models.TextField(
        blank=True,
        verbose_name=_("Commentaire niveaux")
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

    date = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="niveaux",
        verbose_name=_("Main d'oeuvre")
    )

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="niveaux_techs"
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
        related_name="niveaux_tech_societe"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )


    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe


    class Meta:
        verbose_name = _("Niveau")
        verbose_name_plural = _("Niveaux")


    def __str__(self):
        return f"Niveaux – {self.voiture_exemplaire} ({self.date:%Y-%m-%d})"

    def clean(self):
        super().clean()

        if not self.voiture_exemplaire_id or self.kilometrage_niveaux is None:
            return

        voiture = type(self.voiture_exemplaire).objects.get(
            pk=self.voiture_exemplaire_id
        )

        km_actuel = voiture.kilometres_chassis or 0

        if self.kilometrage_niveaux < km_actuel:
            raise ValidationError({
                "kilometrage_niveaux": _(
                    "Le kilométrage du contrôle niveaux (%(km_controle)s) "
                    "ne peut pas être inférieur au kilométrage actuel de la voiture (%(km_voiture)s)."
                ) % {
                                           "km_controle": self.kilometrage_niveaux,
                                           "km_voiture": km_actuel,
                                       }
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
                    _("Contrôle des niveaux")
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
                Maintenance.TypeMaintenance.NIVEAUX
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
            if self.kilometrage_niveaux is not None:

                self.kilometrage_variation = (
                        self.kilometrage_niveaux
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
                and self.kilometrage_niveaux is not None
        ):

            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            if (
                    self.kilometrage_niveaux
                    > (voiture.kilometres_chassis or 0)
            ):
                voiture.kilometres_chassis = (
                    self.kilometrage_niveaux
                )

                voiture.save(
                    update_fields=["kilometres_chassis"]
                )

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

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        produits = [
            {
                "prefix": "moteur_niveau_huile",
                "label": _("Huile moteur"),
            },
            {
                "prefix": "boite_niveau_huile",
                "label": _("Huile de boîte de vitesses"),
            },
            {
                "prefix": "pont_niveau_huile",
                "label": _("Huile de pont"),
            },
            {
                "prefix": "refroidissement",
                "label": _("Liquide de refroidissement"),
            },
            {
                "prefix": "frein_liquide",
                "label": _("Liquide de freins"),
            },
            {
                "prefix": "lave_glace_liquide",
                "label": _("Liquide de lave-glace"),
            },
            {
                "prefix": "direction_liquide",
                "label": _("Liquide de direction assistée"),
            },
        ]

        for produit in produits:
            prefix = produit["prefix"]

            etat_field = f"{prefix}_etat"
            quantite_field = f"{prefix}_quantite"
            qualite_field = f"{prefix}_qualite"
            fabricant_field = f"{prefix}_fabricant"
            prix_field = f"{prefix}_prix"

            etat = getattr(self, etat_field, None)

            # Ajouter au rapport lorsqu'un produit doit être
            # ajouté ou remplacé
            if etat not in [
                NiveauxEtat.AJOUTER,

            ]:
                continue

            prix = getattr(
                self,
                prix_field,
                Decimal("0.00"),
            )

            if prix is None:
                prix = Decimal("0.00")

            prix = Decimal(str(prix))

            quantite = getattr(
                self,
                quantite_field,
                Decimal("0.00"),
            )

            if quantite is None:
                quantite = Decimal("0.00")

            quantite = Decimal(str(quantite))

            qualite = getattr(
                self,
                qualite_field,
                "",
            )

            fabricant = getattr(
                self,
                fabricant_field,
                "",
            )

            # Libellé traduit de l'état
            try:
                etat_label = getattr(
                    self,
                    f"get_{etat_field}_display",
                )()
            except (AttributeError, TypeError):
                etat_label = etat

            # Libellé traduit de la qualité
            try:
                qualite_label = getattr(
                    self,
                    f"get_{qualite_field}_display",
                )()
            except (AttributeError, TypeError):
                qualite_label = qualite

            # Libellé traduit du fabricant
            try:
                fabricant_label = getattr(
                    self,
                    f"get_{fabricant_field}_display",
                )()
            except (AttributeError, TypeError):
                fabricant_label = fabricant

            total = prix * quantite
            total_general += total

            rapport.append({
                "champ": produit["label"],
                "code": prefix,

                # Valeur technique : AJOUTER, REMPLACE, FAIT...
                "etat": etat,

                # Libellé traduit affiché dans le PDF
                "etat_label": etat_label,

                # Valeur technique de la qualité
                "qualite": qualite,
                "qualite_label": qualite_label,

                # Valeur technique du fabricant
                "fabricant": fabricant,
                "fabricant_label": fabricant_label,

                "prix": prix,
                "prix_unitaire": prix,
                "quantite": quantite,
                "total": total,
            })

        return {
            "lignes": rapport,
            "total_general": total_general,
        }
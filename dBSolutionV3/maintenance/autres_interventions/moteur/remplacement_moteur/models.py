import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import FabricantLubrifiant, RefroidissementFabricant, TVAConfig, RouesSerrageEtat
from maintenance.niveaux.models import  (NiveauxEtat,HuileEtat, RefroidissementQualiteEtat)
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


    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

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

    kilometres_remplacement = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres au moment du remplacement")
    )


    kilometres_moteur = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilometres du moteur à remplacer")
    )

    kilometres_boite = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_boite_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback boite")
    )

    kilometres_moteur_rollback = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Kilomètres rollback moteur")
    )
    kilometres_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_embrayage_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback embrayage")
    )

    kilometres_remplacement_moteur = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres au remplacement moteur")
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
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
    niveau_huile_fabricant = models.CharField(
        max_length=25,
        choices=FabricantLubrifiant.choices,
        default=FabricantLubrifiant.MOBIL,
        verbose_name=_("Fabricant")
    )
    niveau_huile_qualite = models.CharField(
        max_length=25,
        choices=HuileEtat.choices,
        default=HuileEtat.ZERO_30,
        verbose_name=_("Qualité d'huile")
    )

    niveau_huile_quantite = models.FloatField(
        default=0,
        verbose_name=_("Quantité d'huile ajoutée en litres"),
        validators=[StepValueValidator(0.1)]
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

    refroidissement_fabricant = models.CharField(
        max_length=25,
        choices=RefroidissementFabricant.choices,
        default=RefroidissementFabricant.CHOISIR,
        verbose_name=_("Niveau de liquide de refroidissement")
    )

    refroidissement_qualite = models.CharField(
        max_length=25,
        choices=RefroidissementQualiteEtat.choices,
        default=RefroidissementQualiteEtat.G13,
        verbose_name=_("Qualité de liquide de refroidissement")
    )

    refroidissement_quantite = models.FloatField(
        default=0,
        verbose_name=_("Quantité ajoutée en litres"),
        validators=[StepValueValidator(0.1)]
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
        verbose_name=_("Remplacement effectué et remise à zéro"),
    )

   

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )


    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

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
        return (
            f"{self.voiture_exemplaire.voiture_marque.nom_marque} "
            f"{self.voiture_exemplaire.voiture_modele.nom_modele} "
            f"{self.voiture_exemplaire.voiture_modele.nom_variante} - "
            f"{self.voiture_exemplaire.immatriculation}"
        )

    def clean(self):
        super().clean()

        if not self.voiture_exemplaire:
            return

        # ======================================================
        # VALEURS ACTUELLES DE L'EXEMPLAIRE
        # ======================================================
        ancien_km_chassis = (
                self.voiture_exemplaire.kilometres_chassis or 0
        )

        ancien_km_moteur = (
                self.voiture_exemplaire.kilometres_moteur or 0
        )

        # ======================================================
        # NOUVEAU KILOMÉTRAGE SAISI
        # ======================================================
        nouveau_km = (
            self.kilometres_remplacement
        )

        if nouveau_km is None:
            return

        # ======================================================
        # VALIDATION
        # ======================================================
        if nouveau_km < ancien_km_chassis:
            raise ValidationError({
                "kilometres_remplacement": _(
                    "Le nouveau kilométrage ne peut pas être "
                    "inférieur au dernier kilométrage du véhicule."
                )
            })




    def activer_remplacement(self):
        self.kilometres_remplacement_moteur = self.kilometres_remplacement
        self.remplacement_effectue = True
        self.save()

    def save(self, *args, **kwargs):

        # ==========================================================
        # VOITURE
        # ==========================================================
        voiture = self.voiture_exemplaire

        # ==========================================================
        # NOUVEL ENREGISTREMENT ?
        # ==========================================================
        is_new = self._state.adding

        # ==========================================================
        # TECHNICIEN / DERNIÈRE MODIFICATION
        # ==========================================================
        if self.tech_technicien:
            self.tech_last_maintained_by = (
                self.tech_technicien
            )

        # ==========================================================
        # TRAITEMENT DES KILOMÉTRAGES
        # ==========================================================
        if voiture:

            # ------------------------------------------------------
            # VALEURS ACTUELLES DE L'EXEMPLAIRE
            # AVANT LA MODIFICATION
            # ------------------------------------------------------
            ancien_km_chassis = (
                    voiture.kilometres_chassis or 0
            )

            ancien_km_moteur = (
                    voiture.kilometres_moteur or 0
            )

            # ------------------------------------------------------
            # NOUVEAU KILOMÉTRAGE SAISI
            # ------------------------------------------------------
            nouveau_km = (
                self.kilometres_remplacement
            )

            if nouveau_km is not None:

                # ==================================================
                # VALIDATION
                # ==================================================
                if nouveau_km < ancien_km_chassis:
                    raise ValidationError(
                        {
                            "kilometres_remplacement": _(
                                "Le nouveau kilométrage ne peut pas être "
                                "inférieur au dernier kilométrage du véhicule."
                            )
                        }
                    )

                # ==================================================
                # DISTANCE PARCOURUE DEPUIS LE DERNIER CONTRÔLE
                # ==================================================
                difference = (
                        nouveau_km
                        - ancien_km_chassis
                )

                # ==================================================
                # NOUVEAU KILOMÉTRAGE MOTEUR
                #
                # Exemple :
                #
                # chassis = 25 000
                # moteur  = 4 000
                # nouveau = 26 000
                #
                # différence = 1 000
                # moteur = 4 000 + 1 000 = 5 000
                # ==================================================
                nouveau_km_moteur = (
                        ancien_km_moteur
                        + difference
                )

                # ==================================================
                # VALEURS DE L'INTERVENTION
                # ==================================================
                self.kilometres_chassis = (
                    ancien_km_chassis
                )

                self.kilometres_moteur = (
                    nouveau_km_moteur
                )

                # ==================================================
                # SI REMPLACEMENT EFFECTUÉ
                # ==================================================
                if self.remplacement_effectue:
                    self.kilometres_remplacement_moteur = (
                        nouveau_km
                    )

                    voiture.kilometres_remplacement_moteur = (
                        nouveau_km
                    )

                # ==================================================
                # MISE À JOUR DE L'EXEMPLAIRE
                # ==================================================
                voiture.kilometres_chassis = (
                    nouveau_km
                )

                voiture.kilometres_moteur = (
                    nouveau_km_moteur
                )

                update_fields = [
                    "kilometres_chassis",
                    "kilometres_moteur",
                ]

                if self.remplacement_effectue:
                    update_fields.append(
                        "kilometres_remplacement_moteur"
                    )

                voiture.save(
                    update_fields=update_fields
                )

        # ==========================================================
        # NOMBRE DE REMPLACEMENTS
        # ==========================================================
        if is_new and voiture:

            nb_remplacements = (
                RemplacementMoteur.objects.filter(
                    voiture_exemplaire=voiture,
                    remplacement_effectue=True,
                ).count()
            )

            if self.remplacement_effectue:
                nb_remplacements += 1

            self.nombre_remplacements_moteurs = (
                nb_remplacements
            )

            self.nombre_moteurs_montes = (
                    nb_remplacements + 1
            )

        # ==========================================================
        # SAUVEGARDE DU REMPLACEMENT MOTEUR
        # ==========================================================
        super().save(*args, **kwargs)

        # ==========================================================
        # MAIN D'ŒUVRE — DESCRIPTIF AUTOMATIQUE
        # ==========================================================
        if (
                self.main_oeuvre_id
                and self.voiture_exemplaire_id
        ):

            task_name = (
                    _("Remplacement moteur")
                    + " "
                    + str(self.voiture_exemplaire)
            )

            if self.main_oeuvre.descriptif != task_name:
                self.main_oeuvre.descriptif = (
                    task_name
                )

                self.main_oeuvre.save(
                    update_fields=[
                        "descriptif"
                    ]
                )



    def clean_kilometres_remplacement(self):
        nouveau_km = self.cleaned_data.get(
            "kilometres_remplacement"
        )

        if (
                nouveau_km is not None
                and self.exemplaire
                and nouveau_km < self.exemplaire.kilometres_chassis
        ):
            raise ValidationError(
                _("Le kilométrage ne peut pas diminuer.")
            )

        return nouveau_km

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        for field in self._meta.fields:
            field_name = field.name

            # Uniquement les champs utilisant NiveauxEtat
            if not (
                    isinstance(field, models.CharField)
                    and field.choices == NiveauxEtat.choices
            ):
                continue

            etat = getattr(self, field_name, None)

            # On facture uniquement les liquides ajoutés
            if etat != NiveauxEtat.AJOUTER:
                continue

            # Exemples :
            # niveau_huile_etat -> niveau_huile
            # refroidissement_etat -> refroidissement
            champ_base = field_name.removesuffix("_etat")

            nom_champ_prix = f"{champ_base}_prix"
            nom_champ_quantite = f"{champ_base}_quantite"
            nom_champ_oem = f"{champ_base}_oem"
            nom_champ_fabricant = f"{champ_base}_fabricant"

            prix = getattr(
                self,
                nom_champ_prix,
                Decimal("0.00"),
            )

            if prix is None:
                prix = Decimal("0.00")

            prix = Decimal(str(prix))

            quantite = getattr(
                self,
                nom_champ_quantite,
                0,
            )

            if quantite is None:
                quantite = 0

            quantite = Decimal(str(quantite))

            # Ne pas afficher les lignes sans prix ou quantité
            if prix <= 0 or quantite <= 0:
                continue

            numero_oem = getattr(
                self,
                nom_champ_oem,
                "",
            ) or ""

            # Valeur brute du fabricant (code en majuscules)
            fabricant = getattr(
                self,
                nom_champ_fabricant,
                "",
            ) or ""

            # Libellé écrit correspondant, via le get_<champ>_display
            # auto-généré par Django grâce aux choices du champ
            get_fabricant_display = getattr(
                self,
                f"get_{nom_champ_fabricant}_display",
                None,
            )
            fabricant_label = (
                get_fabricant_display()
                if get_fabricant_display is not None
                else fabricant
            )

            total = (
                    prix * quantite
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total_general += total

            rapport.append({
                "champ": field.verbose_name,
                "code": champ_base,
                "etat": etat,
                "etat_label": dict(
                    NiveauxEtat.choices
                ).get(etat, etat),
                "oem": numero_oem,
                "fabricant": fabricant,
                "fabricant_label": fabricant_label,
                "prix": prix,
                "quantite": quantite,
                "total": total,
            })

        # ==================================================
        # MOTEUR DE REMPLACEMENT
        # ==================================================

        moteur_prix = Decimal(str(
            self.moteurs_prix or Decimal("0.00")
        ))

        moteur_quantite = Decimal(str(
            self.moteur_quantite or 0
        ))

        if moteur_prix > 0 and moteur_quantite > 0:
            moteur_total = (
                    moteur_prix * moteur_quantite
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total_general += moteur_total

            rapport.insert(0, {
                "champ": _("Moteur de remplacement"),
                "code": "moteur",
                "etat": (
                    "REMPLACE"
                    if self.remplacement_effectue
                    else "A_REMPLACER"
                ),
                "etat_label": (
                    _("Remplacé")
                    if self.remplacement_effectue
                    else _("À remplacer")
                ),
                "oem": self.remplacement_numero_moteurs or "",
                "fabricant": "",
                "fabricant_label": "",
                "prix": moteur_prix,
                "quantite": moteur_quantite,
                "total": moteur_total,
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
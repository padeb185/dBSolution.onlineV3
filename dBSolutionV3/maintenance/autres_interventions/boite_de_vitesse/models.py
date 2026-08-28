from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import TVAConfig, HuileBoiteEtat, RouesSerrageEtat
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance




class BoiteVitesseEtat(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")

# ---------------------------
# Modèle fusionné
# ---------------------------
class ControleBoite(TechnicienMixin, models.Model):


    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    id = models.BigAutoField(primary_key=True)

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_boite",
        verbose_name=_("Maintenance"),
        null=True,  # autorisé vide à la création
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="controle_boite",
        verbose_name="Kilomètres_checkup",
        null=True, blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_controle_boite = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du controle"),
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )


    # --- Boîte Manuelle ---
    # Embrayage
    bte_embrayage_disque = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Disque d'embrayage"))
    bte_embrayage_disque_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    bte_embrayage_disque_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    bte_embrayage_plateau = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Plateau d'embrayage"))
    bte_embrayage_plateau_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    bte_embrayage_plateau_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    # Arbres
    bte_a_primaire = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Arbre primaire"))
    bte_a_primaire_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    bte_a_primaire_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    bte_a_secondaire = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Arbre secondaire"))
    bte_a_secondaire_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    bte_a_secondaire_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))



    # Roulements
    roulement_bte_primaire = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Roulement arbre primaire"))
    roulement_bte_primaire_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    roulement_bte_primaire_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    roulement_bte_secondaire = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Roulement arbre secondaire"))
    roulement_bte_secondaire_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    roulement_bte_secondaire_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))



    roulement_bte_differentiel = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Roulement différentiel"))
    roulement_bte_differentiel_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    roulement_bte_differentiel_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))



    # Vitesses / pignons
    vitesse_1 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Pignon 1ère vitesse"))
    vitesse_1_quantite = models.PositiveIntegerField(default=1, verbose_name=_("Quantité"))
    vitesse_1_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))



    vitesse_2 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Pignon 2ème vitesse"))
    vitesse_2_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    vitesse_2_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    vitesse_3 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Pignon 3ème vitesse"))
    vitesse_3_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    vitesse_3_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    vitesse_4 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Pignon 4ème vitesse"))
    vitesse_4_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    vitesse_4_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    vitesse_5 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Pignon 5ème vitesse"))
    vitesse_5_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    vitesse_5_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))




    vitesse_6 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Pignon 6ème vitesse (si existante)"))
    vitesse_6_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    vitesse_6_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))



    vitesse_7 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices, default=BoiteVitesseEtat.OK,verbose_name=_("Pignon 7ème vitesse (si existante)"))
    vitesse_7_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    vitesse_7_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))



    vitesse_8 = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices, default=BoiteVitesseEtat.OK,verbose_name=_("Pignon 8ème vitesse (si existante)"))
    vitesse_8_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    vitesse_8_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))



    vitesse_r = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices, default=BoiteVitesseEtat.OK,verbose_name=_("Pignon de marche arrière"))
    vitesse_r_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    vitesse_r_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    # Synchros / fourchettes
    synchros = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Synchros"))
    synchros_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    synchros_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


    fourchettes = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Fourchettes"))
    fourchettes_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    fourchettes_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))





    # Huile
    man_huile_manuelle = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices, default=BoiteVitesseEtat.OK,verbose_name=_("Huile de boite de vitesse"))

    man_huile_manuelle_qualite = models.CharField(max_length=25, choices=HuileBoiteEtat.choices,
                                                  default=HuileBoiteEtat.SEPTANTE_CINQ,
                                                  verbose_name=_("Qualité de l'huile"))
    man_huile_manuelle_quantite = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=Decimal("0.0"),
        verbose_name=_("Quantité d'huile ajoutée en litres"),
        validators=[StepValueValidator(0.1)],
    )
    man_huile_manuelle_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Prix d'achat HTVA"),
    )



    remarques = models.TextField(
        verbose_name=_("Remarques"), blank=True, null=True)

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

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="boite_de_vitesse",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="controle_boite"
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
        related_name="controle_boite"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
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
        verbose_name = _("Contrôle boite")
        verbose_name_plural = _("Contrôles boites")


    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle Boîte - {self.voiture_exemplaire.id}"
        return "Contrôle Boîte - non défini"


    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_controle_boite is not None:
            if self.kilometrage_controle_boite < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_controle_boite': _(
                        f"Le kilométrage du check-up ({self.kilometrage_conytrole_boite}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):

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
                    _("Checkup boite de vitesse")
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
                Maintenance.TypeMaintenance.BOITE
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
            if self.kilometrage_controle_boite is not None:

                self.kilometrage_variation = (
                        self.kilometrage_controle_boite
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
                and self.kilometrage_controle_boite is not None
        ):

            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            if (
                    self.kilometrage_controle_boite
                    > (voiture.kilometres_chassis or 0)
            ):
                voiture.kilometres_chassis = (
                    self.kilometrage_controle_boite
                )

                voiture.save(
                    update_fields=["kilometres_chassis"]
                )






    def calcul_piece(self, prefix):
        prix_achat = getattr(self, f"{prefix}_prix")
        quantite = getattr(self, f"{prefix}_quantite")

        if not prix_achat or not self.pays:
            return

        tva_rate = Decimal(self.TVA_PIECES.get(self.pays, 0)) / 100

        # TVA achat
        setattr(self, f"{prefix}_tva_achat",
                (prix_achat * tva_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

        prix_htva = prix_achat.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        setattr(self, f"{prefix}_prix_vente_htva", prix_htva)

        # TVA vente
        tva = (prix_htva * tva_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        setattr(self, f"{prefix}_tva_vente", tva)

        # TTC
        prix_ttc = prix_htva + tva
        setattr(self, f"{prefix}_prix_ttc", prix_ttc)

    def generer_rapport_remplacement(self):
            rapport = []
            total_general = Decimal("0.00")

            for field in self._meta.fields:
                field_name = field.name

                # Ne garder que les champs utilisant EtatOKNotOK
                if (
                        isinstance(field, models.CharField)
                        and field.choices == BoiteVitesseEtat.choices
                ):
                    valeur = getattr(self, field_name)

                    # Pièces à remplacer ou déjà remplacées
                    if valeur in [
                        BoiteVitesseEtat.NOT_OK,
                        BoiteVitesseEtat.REMPLACE,
                    ]:
                        prix = getattr(
                            self,
                            f"{field_name}_prix",
                            Decimal("0.00"),
                        )

                        if prix is None:
                            prix = Decimal("0.00")

                        prix = Decimal(str(prix))

                        quantite = getattr(
                            self,
                            f"{field_name}_quantite",
                            0,
                        )

                        if quantite is None:
                            quantite = 0

                        quantite = Decimal(str(quantite))

                        total = prix * quantite
                        total_general += total

                        rapport.append({
                            "champ": field.verbose_name,
                            "code": field_name,
                            "etat": valeur,
                            "etat_label": dict(
                                BoiteVitesseEtat.choices
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



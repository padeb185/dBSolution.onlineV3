from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import FabricantLubrifiant, FabricantEmbrayage, TVAConfig, HuileBoiteAutoEtat, RouesSerrageEtat
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance






class BoiteVitesseEtat(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    NON_PRESENT = "NON_PRESENT", _("Non présent")


class ControleBteVitesseAuto(TechnicienMixin, models.Model):


    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_bte_vitesse_auto",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="controle_bte_vitesse_auto",
        verbose_name=_("Kilomètres checkup"),
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_controle_boite_auto = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du contrôle"),
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    # --- Boîte automatique ---
    auto_emb_convertisseur_couple = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Convertisseur de couple")
    )

    auto_emb_convertisseur_couple_fabricant = models.CharField(
        max_length=25,
        choices=FabricantEmbrayage.choices,
        default=FabricantEmbrayage.CHOISIR,
        verbose_name=_("Fabricant")
    )

    auto_emb_convertisseur_couple_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )
    auto_emb_convertisseur_couple_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )



    double_embrayage = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Double embrayage")
    )

    double_embrayage_fabricant = models.CharField(
        max_length=25,
        choices=FabricantEmbrayage.choices,
        default=FabricantEmbrayage.CHOISIR,
        verbose_name=_("Fabricant")
    )

    double_embrayage_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )

    double_embrayage_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    pompes_h = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Pompes à huile")
    )

    pompes_h_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )
    pompes_h_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    pompes_valves = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Valves de contrôle")
    )
    pompes_valves_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )
    pompes_valves_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    arbre_bte_torque = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Arbre de couple")
    )

    arbre_bte_torque_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )
    arbre_bte_torque_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )



    arbre_bte_secondaire_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Arbre secondaire")
    )

    arbre_bte_secondaire_auto_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )

    arbre_bte_secondaire_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    roulement_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Roulements internes")
    )



    roulement_auto_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )

    roulement_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )

    huile_bte_auto_vitesse = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices, default=BoiteVitesseEtat.OK,
                                          verbose_name=_("Huile de boite de vitesse"))

    huile_bte_auto_vitesse_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,
                                              default=FabricantLubrifiant.CASTROL,
                                              verbose_name=_("Fabricant"))

    huile_bte_auto_vitesse_qualite = models.CharField(max_length=25, choices=HuileBoiteAutoEtat.choices,
                                                      default=HuileBoiteAutoEtat.ATF3,
                                                      verbose_name=_("Qualité de l'huile"))

    huile_bte_auto_vitesse_quantite = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=Decimal("0.0"),
        verbose_name=_("Quantité d'huile ajoutée en litres"),
        validators=[StepValueValidator(0.1)],
    )
    huile_bte_auto_vitesse_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Prix d'achat HTVA"),
    )


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
        default="WHITE",
        verbose_name=_("État visuel / Tag"),
    )

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="controle_bte_vitesse_auto",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="controle_bte_auto"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="controle_bte_auto"
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

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_controle_boite_auto is not None:
            if self.kilometrage_controle_boite_auto < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_controle_boite_auto': _(
                        f"Le kilométrage du contrôle ({self.kilometrage_controle_boite_auto}) "
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
                    _("Checkup boite de vitesse automatique")
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
                Maintenance.TypeMaintenance.BOITE_AUTO
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
            if self.kilometrage_controle_boite_auto is not None:

                self.kilometrage_variation = (
                        self.kilometrage_controle_boite_auto
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
                and self.kilometrage_controle_boite_auto is not None
        ):

            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            if (
                    self.kilometrage_controle_boite_auto
                    > (voiture.kilometres_chassis or 0)
            ):
                voiture.kilometres_chassis = (
                    self.kilometrage_controle_boite_auto
                )

                voiture.save(
                    update_fields=["kilometres_chassis"]
                )





    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle boîte automatique - {self.voiture_exemplaire.id}"
        return "Contrôle boîte automatique - non défini"

    class Meta:
        verbose_name = _("Contrôle boîte automatique")
        verbose_name_plural = _("Contrôles boîtes automatiques")

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

    def generer_rapport_remplacement(self):
        lignes = []
        total_pieces = Decimal("0.00")

        pieces = [
            {
                "champ": _("Convertisseur de couple"),
                "etat": self.auto_emb_convertisseur_couple,
                "prix": self.auto_emb_convertisseur_couple_prix,
                "quantite": self.auto_emb_convertisseur_couple_quantite,
            },
            {
                "champ": _("Double embrayage"),
                "etat": self.double_embrayage,
                "prix": self.double_embrayage_prix,
                "quantite": self.double_embrayage_quantite,
            },
            {
                "champ": _("Pompe à huile"),
                "etat": self.pompes_h,
                "prix": self.pompes_h_prix,
                "quantite": self.pompes_h_quantite,
            },
            {
                "champ": _("Valves de contrôle"),
                "etat": self.pompes_valves,
                "prix": self.pompes_valves_prix,
                "quantite": self.pompes_valves_quantite,
            },
            {
                "champ": _("Arbre de couple"),
                "etat": self.arbre_bte_torque,
                "prix": self.arbre_bte_torque_prix,
                "quantite": self.arbre_bte_torque_quantite,
            },
            {
                "champ": _("Arbre secondaire"),
                "etat": self.arbre_bte_secondaire_auto,
                "prix": self.arbre_bte_secondaire_auto_prix,
                "quantite": self.arbre_bte_secondaire_auto_quantite,
            },
            {
                "champ": _("Roulements internes"),
                "etat": self.roulement_auto,
                "prix": self.roulement_auto_prix,
                "quantite": self.roulement_auto_quantite,
            },
            {
                "champ": _("Huile de boîte automatique"),
                "etat": self.huile_bte_auto_vitesse,
                "prix": self.huile_bte_auto_vitesse_prix,
                "quantite": self.huile_bte_auto_vitesse_quantite,
            },
        ]

        etats_labels = {
            "NOT_OK": _("À remplacer"),
            "REMPLACE": _("Remplacé"),
        }

        for piece in pieces:
            etat = piece["etat"]

            if etat not in ("NOT_OK", "REMPLACE"):
                continue

            prix = Decimal(str(piece["prix"] or "0.00"))
            quantite = Decimal(str(piece["quantite"] or "0.00"))

            if prix <= 0 or quantite <= 0:
                continue

            total_ligne = (
                    prix * quantite
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total_pieces += total_ligne

            lignes.append({
                "champ": piece["champ"],
                "etat": etat,
                "etat_label": etats_labels.get(etat, etat),
                "quantite": quantite,
                "prix": prix,
                "total": total_ligne,
            })

        total_pieces = total_pieces.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        return {
            "lignes": lignes,
            "pieces": lignes,
            "total_pieces": total_pieces,
            "total_general": total_pieces,
        }

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()

        total_pieces = rapport.get(
            "total_pieces",
            Decimal("0.00"),
        )

        cout_main_oeuvre = self.cout_main_oeuvre or Decimal("0.00")

        return total_pieces + cout_main_oeuvre

from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import MarqueAmortisseur, TVAConfig, RouesSerrageEtat
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class MoyenMesureHauteur(models.TextChoices):
    LASER = "LASER", _("Laser")
    JAUGE = "JAUGE", _("Jauge de hauteur")
    REGLE = "REGLE", _("Règle / mètre")
    AUTRE = "AUTRE", _("Autre")


class UnitePincement(models.TextChoices):
    DEGRES = "DEGRES", _("Degrés (°)")
    MINUTES = "MINUTES", _("Minutes d'angle (′)")
    MM = "MM", _("Millimètres (mm)")


class ReferenceClics(models.TextChoices):
    FERME = "FERME", _("Position fermée (dur)")
    OUVERT = "OUVERT", _("Position ouverte (souple)")


class TypeRessort(models.TextChoices):
    LINEAIRE = "LINEAIRE", _("Linéaire")
    PROGRESSIF = "PROGRESSIF", _("Progressif")
    DOUBLE = "DOUBLE", _("Double raideur")


class TypeRessortRappel(models.TextChoices):
    AUCUN = "AUCUN", _("Aucun")
    HELPER = "HELPER", _("Helper (rattrapage de jeu)")
    TENDER = "TENDER", _("Tender (double raideur)")


COINS = [("avg", _("AVG")), ("avd", _("AVD")), ("arg", _("ARG")), ("ard", _("ARD"))]
COINS_AV = [("avg", _("AVG")), ("avd", _("AVD"))]


class GeometrieCourse(TechnicienMixin, models.Model):
    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="geometrie_course",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="geometrie_course",
        verbose_name=_("Véhicule"),
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_geometrie = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du contrôle"),
    )

    kilometres_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Kilomètres rollback")
    )

    kilometres_boite = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_boite_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback boite")
    )

    kilometres_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_moteur_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback moteur")
    )

    kilometres_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_embrayage_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback embrayage")
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    # ======================================================
    # FICHE DE RÉGLAGE COURSE (setup)
    # Coins : AVG / AVD / ARG / ARD — « avant » = avant la géométrie,
    # « cible » = réglage demandé par l'ingénieur, « apres » = après la géométrie
    # ======================================================

    # --- Pilote / conditions de pesée ---
    poids_pilote = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True,
                                       verbose_name=_("Poids du pilote équipé (kg)"))
    pesee_avec_pilote = models.BooleanField(default=True, verbose_name=_("Pesée avec pilote (ou lest équivalent)"))
    carburant_litres = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True,
                                           verbose_name=_("Carburant à bord (L)"))
    ingenieur = models.CharField(max_length=120, blank=True, verbose_name=_("Ingénieur / préparateur"))

    # --- Balance : pesée de chaque roue (kg) ---
    poids_avant_avg = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Poids AVG avant géométrie (kg)"))
    poids_avant_avd = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Poids AVD avant géométrie (kg)"))
    poids_avant_arg = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Poids ARG avant géométrie (kg)"))
    poids_avant_ard = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Poids ARD avant géométrie (kg)"))
    poids_apres_avg = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Poids AVG après géométrie (kg)"))
    poids_apres_avd = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Poids AVD après géométrie (kg)"))
    poids_apres_arg = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Poids ARG après géométrie (kg)"))
    poids_apres_ard = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Poids ARD après géométrie (kg)"))

    # --- Hauteur de caisse (mm) ---
    moyen_mesure_hauteur = models.CharField(max_length=10, choices=MoyenMesureHauteur.choices,
                                            default=MoyenMesureHauteur.LASER,
                                            verbose_name=_("Mesure de la hauteur de caisse"))
    point_mesure_hauteur = models.CharField(max_length=100, blank=True, verbose_name=_("Point de mesure"),
                                            help_text=_("Ex. : bas de caisse, plancher, axe de roue…"))
    hauteur_avant_avg = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur AVG avant géométrie (mm)"))
    hauteur_avant_avd = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur AVD avant géométrie (mm)"))
    hauteur_avant_arg = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur ARG avant géométrie (mm)"))
    hauteur_avant_ard = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur ARD avant géométrie (mm)"))
    hauteur_cible_avg = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur AVG cible ingénieur (mm)"))
    hauteur_cible_avd = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur AVD cible ingénieur (mm)"))
    hauteur_cible_arg = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur ARG cible ingénieur (mm)"))
    hauteur_cible_ard = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur ARD cible ingénieur (mm)"))
    hauteur_apres_avg = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur AVG après géométrie (mm)"))
    hauteur_apres_avd = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur AVD après géométrie (mm)"))
    hauteur_apres_arg = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur ARG après géométrie (mm)"))
    hauteur_apres_ard = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur ARD après géométrie (mm)"))

    # --- Carrossage (°) ---
    carrossage_avant_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Carrossage AVG avant géométrie (°)"))
    carrossage_avant_avd = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Carrossage AVD avant géométrie (°)"))
    carrossage_avant_arg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Carrossage ARG avant géométrie (°)"))
    carrossage_avant_ard = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Carrossage ARD avant géométrie (°)"))
    carrossage_cible_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Carrossage AVG cible ingénieur (°)"))
    carrossage_cible_avd = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Carrossage AVD cible ingénieur (°)"))
    carrossage_cible_arg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Carrossage ARG cible ingénieur (°)"))
    carrossage_cible_ard = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Carrossage ARD cible ingénieur (°)"))
    carrossage_apres_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Carrossage AVG après géométrie (°)"))
    carrossage_apres_avd = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Carrossage AVD après géométrie (°)"))
    carrossage_apres_arg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Carrossage ARG après géométrie (°)"))
    carrossage_apres_ard = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Carrossage ARD après géométrie (°)"))

    # --- Chasse (°) — train avant ---
    chasse_avant_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Chasse AVG avant géométrie (°)"))
    chasse_avant_avd = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Chasse AVD avant géométrie (°)"))
    chasse_cible_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Chasse AVG cible ingénieur (°)"))
    chasse_cible_avd = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Chasse AVD cible ingénieur (°)"))
    chasse_apres_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Chasse AVG après géométrie (°)"))
    chasse_apres_avd = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Chasse AVD après géométrie (°)"))

    # --- Pincement (+) / ouverture (−) ---
    unite_pincement = models.CharField(max_length=10, choices=UnitePincement.choices, default=UnitePincement.DEGRES,
                                       verbose_name=_("Unité du pincement"))
    pincement_avant_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Pincement AVG avant géométrie"))
    pincement_avant_avd = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Pincement AVD avant géométrie"))
    pincement_avant_arg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Pincement ARG avant géométrie"))
    pincement_avant_ard = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Pincement ARD avant géométrie"))
    pincement_cible_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Pincement AVG cible ingénieur"))
    pincement_cible_avd = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Pincement AVD cible ingénieur"))
    pincement_cible_arg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Pincement ARG cible ingénieur"))
    pincement_cible_ard = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Pincement ARD cible ingénieur"))
    pincement_apres_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Pincement AVG après géométrie"))
    pincement_apres_avd = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Pincement AVD après géométrie"))
    pincement_apres_arg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Pincement ARG après géométrie"))
    pincement_apres_ard = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Pincement ARD après géométrie"))

    # --- Réglages ingénieur : amortisseurs (nombre de clics) ---
    amortisseur_marque = models.CharField(max_length=255, choices=MarqueAmortisseur.choices,
                                          default=MarqueAmortisseur.CHOISIR, verbose_name=_("Marque des amortisseurs"))
    amortisseur_modele = models.CharField(max_length=120, blank=True, verbose_name=_("Modèle des amortisseurs"))
    reference_clics = models.CharField(max_length=10, choices=ReferenceClics.choices, default=ReferenceClics.FERME,
                                       verbose_name=_("Clics comptés depuis"))
    compression_clics_avg = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Compression AVG (clics)"))
    compression_clics_avd = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Compression AVD (clics)"))
    compression_clics_arg = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Compression ARG (clics)"))
    compression_clics_ard = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Compression ARD (clics)"))
    compression_hv_clics_avg = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Compression haute vitesse AVG (clics)"))
    compression_hv_clics_avd = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Compression haute vitesse AVD (clics)"))
    compression_hv_clics_arg = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Compression haute vitesse ARG (clics)"))
    compression_hv_clics_ard = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Compression haute vitesse ARD (clics)"))
    detente_clics_avg = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Détente AVG (clics)"))
    detente_clics_avd = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Détente AVD (clics)"))
    detente_clics_arg = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Détente ARG (clics)"))
    detente_clics_ard = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Détente ARD (clics)"))

    # --- Ressorts (par essieu) ---
    ressort_type_av = models.CharField(max_length=12, choices=TypeRessort.choices, default=TypeRessort.LINEAIRE,
                                     verbose_name=_("Type de ressort AV"))
    ressort_marque_av = models.CharField(max_length=80, blank=True, verbose_name=_("Marque / référence ressort AV"))
    ressort_raideur_av = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True,
                                              verbose_name=_("Raideur ressort AV (N/mm)"))
    ressort_longueur_av = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True,
                                               verbose_name=_("Longueur ressort AV (mm)"))
    ressort_rappel_type_av = models.CharField(max_length=10, choices=TypeRessortRappel.choices,
                                            default=TypeRessortRappel.AUCUN,
                                            verbose_name=_("Type de ressort de rappel AV"))
    ressort_rappel_raideur_av = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True,
                                                     verbose_name=_("Raideur ressort de rappel AV (N/mm)"))
    ressort_rappel_longueur_av = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True,
                                                      verbose_name=_("Longueur ressort de rappel AV (mm)"))
    barre_antiroulis_av = models.CharField(max_length=80, blank=True, verbose_name=_("Barre anti-roulis AV"),
                                          help_text=_("Diamètre / position de réglage"))
    ressort_type_ar = models.CharField(max_length=12, choices=TypeRessort.choices, default=TypeRessort.LINEAIRE,
                                     verbose_name=_("Type de ressort AR"))
    ressort_marque_ar = models.CharField(max_length=80, blank=True, verbose_name=_("Marque / référence ressort AR"))
    ressort_raideur_ar = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True,
                                              verbose_name=_("Raideur ressort AR (N/mm)"))
    ressort_longueur_ar = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True,
                                               verbose_name=_("Longueur ressort AR (mm)"))
    ressort_rappel_type_ar = models.CharField(max_length=10, choices=TypeRessortRappel.choices,
                                            default=TypeRessortRappel.AUCUN,
                                            verbose_name=_("Type de ressort de rappel AR"))
    ressort_rappel_raideur_ar = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True,
                                                     verbose_name=_("Raideur ressort de rappel AR (N/mm)"))
    ressort_rappel_longueur_ar = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True,
                                                      verbose_name=_("Longueur ressort de rappel AR (mm)"))
    barre_antiroulis_ar = models.CharField(max_length=80, blank=True, verbose_name=_("Barre anti-roulis AR"),
                                          help_text=_("Diamètre / position de réglage"))

    # --- Pressions des pneus à froid (bar) ---
    pression_froid_avg = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_("Pression à froid AVG (bar)"))
    pression_froid_avd = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_("Pression à froid AVD (bar)"))
    pression_froid_arg = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_("Pression à froid ARG (bar)"))
    pression_froid_ard = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_("Pression à froid ARD (bar)"))

    remarques = models.TextField(blank=True, verbose_name=_("Remarques de l'ingénieur"))

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]
    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="VERT",
        verbose_name=_("État visuel / Tag"),
    )

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geometrie_course",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="geometrie_course"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="geometrie_course"
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

    # ======================================================
    # LISTE DES PIÈCES (source unique pour le rapport)
    # ======================================================
    # Pas de pièces : la géométrie course est une prestation (main-d'œuvre)
    PIECES_DEF = []

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire_id and self.kilometrage_geometrie is not None:
            # Création : on compare au véhicule.
            # Modification : au kilométrage figé avant ce contrôle.
            if self.pk:
                minimum = self.kilometres_chassis or 0
            else:
                minimum = self.voiture_exemplaire.kilometres_chassis or 0

            if self.kilometrage_geometrie < minimum:
                raise ValidationError({
                    "kilometrage_geometrie": _(
                        "Le kilométrage du contrôle (%(km_controle)s) ne peut pas "
                        "être inférieur au kilométrage avant intervention (%(km_voiture)s)."
                    ) % {
                        "km_controle": self.kilometrage_geometrie,
                        "km_voiture": minimum,
                    }
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
            task_name = f"{_('Géométrie course')} {self.voiture_exemplaire}"

            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.GEOMETRIE_COURSE
            self.maintenance.voiture_exemplaire = self.voiture_exemplaire
            self.maintenance.save(
                update_fields=["type_maintenance", "voiture_exemplaire"]
            )

        # =========================
        # KILOMÉTRAGE AVANT INTERVENTION
        # (figé uniquement à la création)
        # =========================
        if self.voiture_exemplaire_id and self._state.adding and not self.kilometres_chassis:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )
            self.kilometres_chassis = voiture.kilometres_chassis or 0

        # =========================
        # CALCUL VARIATION (jamais négative : champ PositiveInteger)
        # =========================
        if self.kilometrage_geometrie is not None:
            self.kilometrage_variation = max(
                self.kilometrage_geometrie - (self.kilometres_chassis or 0), 0
            )
        else:
            self.kilometrage_variation = 0

        # =========================
        # SAUVEGARDE CONTRÔLE ARBRE DE TRANSMISSION
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if self.voiture_exemplaire_id and self.kilometrage_geometrie is not None:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )
            if self.kilometrage_geometrie > (voiture.kilometres_chassis or 0):
                voiture.kilometres_chassis = self.kilometrage_geometrie
                voiture.save(update_fields=["kilometres_chassis"])

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Géométrie course - {self.voiture_exemplaire.id}"
        return "Géométrie course - non défini"

    class Meta:
        verbose_name = _("Géométrie course")
        verbose_name_plural = _("Géométries course")

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
        if self.main_oeuvre and self.main_oeuvre.taux_horaire is not None:
            return self.main_oeuvre.taux_horaire

        return Decimal("0.00")

    @property
    def cout_main_oeuvre(self):
        if not self.main_oeuvre:
            return Decimal("0.00")

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        taux_horaire = self.main_oeuvre.taux_horaire or Decimal("0.00")

        cout = (
                Decimal(str(temps_minutes))
                / Decimal("60")
                * Decimal(str(taux_horaire))
        )

        return cout.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # ======================================================
    # RAPPORT
    # ======================================================

    def _choice_display(self, base, suffixe):
        """Libellé d'un champ <base>_<suffixe>, ou '' s'il n'existe pas ou vaut sa valeur par défaut."""
        attr = f"{base}_{suffixe}"
        valeur = getattr(self, attr, None)
        if not valeur:
            return ""
        try:
            defaut = self._meta.get_field(attr).default
        except Exception:
            defaut = None
        if valeur == defaut:
            return ""
        return getattr(self, f"get_{attr}_display")()

    def _fabricant_display(self, base):
        return self._choice_display(base, "fabricant")

    def _cote_display(self, base):
        return self._choice_display(base, "cote")

    def pieces_controle(self):
        """Toutes les pièces contrôlées (hors 'Non présent'), pour le détail / PDF."""
        pieces = []
        for label, base in self.PIECES_DEF:
            etat = getattr(self, base, None)
            if not etat or etat == "NON_PRESENT":
                continue
            pieces.append({
                "base": base,
                "label": label,
                "etat": etat,
                "etat_label": getattr(self, f"get_{base}_display")(),
                "cote": self._cote_display(base),
                "fabricant": self._fabricant_display(base),
            })
        return pieces

    def generer_rapport_remplacement(self):
        lignes = []
        total_pieces = Decimal("0.00")

        etats_labels = {
            "NOT_OK": _("À remplacer"),
            "REMPLACE": _("Remplacé"),
        }

        for label, base in self.PIECES_DEF:
            etat = getattr(self, base, None)

            if etat not in etats_labels:
                continue

            prix = Decimal(str(getattr(self, f"{base}_prix", None) or "0.00"))
            quantite = Decimal(str(getattr(self, f"{base}_quantite", None) or "0"))

            if prix <= 0 or quantite <= 0:
                continue

            total_ligne = (prix * quantite).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            total_pieces += total_ligne

            lignes.append({
                "champ": label,
                "etat": etat,
                "etat_label": etats_labels[etat],
                "fabricant": self._fabricant_display(base),
                "cote": self._cote_display(base),
                "quantite": quantite,
                "prix": prix,
                "total": total_ligne,
            })

        total_pieces = total_pieces.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "lignes": lignes,
            "pieces": lignes,
            "total_pieces": total_pieces,
            "total_general": total_pieces,
        }

    # ======================================================
    # PESÉE : répartitions et cross
    # ======================================================
    def pesee(self, etat):
        """
        Répartition des masses pour etat = "avant" ou "apres" (géométrie) :
        total, % avant, % gauche, cross (AVG + ARD) et poids sans pilote.
        """
        v = {c: getattr(self, f"poids_{etat}_{c}") for c, _l in COINS}
        if any(x is None for x in v.values()):
            return None
        total = sum(v.values(), Decimal("0"))
        if total <= 0:
            return None

        def pct(x):
            return (x * 100 / total).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

        sans_pilote = None
        if self.pesee_avec_pilote and self.poids_pilote:
            sans_pilote = total - self.poids_pilote
        return {
            "coins": v,
            "total": total,
            "avant": v["avg"] + v["avd"], "arriere": v["arg"] + v["ard"],
            "gauche": v["avg"] + v["arg"], "droite": v["avd"] + v["ard"],
            "pct_avant": pct(v["avg"] + v["avd"]), "pct_arriere": pct(v["arg"] + v["ard"]),
            "pct_gauche": pct(v["avg"] + v["arg"]), "pct_droite": pct(v["avd"] + v["ard"]),
            "cross": pct(v["avg"] + v["ard"]), "cross_oppose": pct(v["avd"] + v["arg"]),
            "sans_pilote": sans_pilote,
        }

    @property
    def pesee_avant(self):
        return self.pesee("avant")

    @property
    def pesee_apres(self):
        return self.pesee("apres")

    def grille(self, bases, coins=None):
        """Valeurs par coin pour l'affichage : [{"coin", "code", "valeurs": [...]}, ...]."""
        return [
            {"coin": label, "code": c, "valeurs": [getattr(self, f"{b}_{c}") for b in bases]}
            for c, label in (coins or COINS)
        ]

    @property
    def pesees_affichage(self):
        return [(_("Avant géométrie"), self.pesee_avant), (_("Après géométrie"), self.pesee_apres)]

    @property
    def sections_fiche(self):
        """Sections de la fiche de réglage (détail et PDF), sans les sections vides."""
        etats = [_("Avant géo"), _("Cible ingénieur"), _("Après géo")]
        sections = [
            (_("Balance : pesée de chaque roue"), "balance-pesee.png", [_("Avant géo"), _("Après géo")], "kg",
             ["poids_avant", "poids_apres"], COINS),
            (_("Hauteur de caisse"), "hauteur-caisse.png", etats, "mm",
             ["hauteur_avant", "hauteur_cible", "hauteur_apres"], COINS),
            (_("Carrossage"), "carrossage.png", etats, "°",
             ["carrossage_avant", "carrossage_cible", "carrossage_apres"], COINS),
            (_("Chasse"), "chasse.png", etats, "°",
             ["chasse_avant", "chasse_cible", "chasse_apres"], COINS_AV),
            (_("Pincement / ouverture"), "pincement.png", etats,
             {"DEGRES": "°", "MINUTES": "′", "MM": "mm"}.get(self.unite_pincement, ""),
             ["pincement_avant", "pincement_cible", "pincement_apres"], COINS),
            (_("Amortisseurs (clics)"), "susp_amortisseur.png",
             [_("Compression"), _("Compression HV"), _("Détente")], "",
             ["compression_clics", "compression_hv_clics", "detente_clics"], COINS),
            (_("Pressions des pneus à froid"), "pneus.png", [_("Pression")], "bar", ["pression_froid"], COINS),
        ]
        res = []
        for titre, icone, entetes, unite, bases, coins in sections:
            lignes = self.grille(bases, coins)
            if any(v is not None for l in lignes for v in l["valeurs"]):
                res.append({"titre": titre, "icone": icone, "entetes": entetes, "unite": unite, "lignes": lignes})
        return res

    @property
    def essieux_fiche(self):
        return [
            {
                "titre": titre,
                "type": getattr(self, f"get_ressort_type_{e}_display")(),
                "marque": getattr(self, f"ressort_marque_{e}"),
                "raideur": getattr(self, f"ressort_raideur_{e}"),
                "longueur": getattr(self, f"ressort_longueur_{e}"),
                "rappel_type": getattr(self, f"get_ressort_rappel_type_{e}_display")(),
                "rappel_actif": getattr(self, f"ressort_rappel_type_{e}") != TypeRessortRappel.AUCUN,
                "rappel_raideur": getattr(self, f"ressort_rappel_raideur_{e}"),
                "rappel_longueur": getattr(self, f"ressort_rappel_longueur_{e}"),
                "barre": getattr(self, f"barre_antiroulis_{e}"),
            }
            for e, titre in (("av", _("Essieu avant")), ("ar", _("Essieu arrière")))
        ]

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()
        total_pieces = rapport.get("total_pieces", Decimal("0.00"))
        cout_main_oeuvre = self.cout_main_oeuvre or Decimal("0.00")

        return (total_pieces + cout_main_oeuvre).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

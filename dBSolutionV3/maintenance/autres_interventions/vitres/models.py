from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import FabricantVitrage, TVAConfig, RouesSerrageEtat
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class VitrageEtat(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    REPARE = "REPARE", _("Réparé")
    CALIBRE = "CALIBRE", _("Calibré")
    NON_PRESENT = "NON_PRESENT", _("Non présent")


class VitrageCote(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    AVANT = "AVANT", _("Avant")
    ARRIERE = "ARRIERE", _("Arrière")
    AVG = "AVG", _("AVG")
    AVD = "AVD", _("AVD")
    ARG = "ARG", _("ARG")
    ARD = "ARD", _("ARD")
    GAUCHE = "GAUCHE", _("Gauche")
    DROITE = "DROITE", _("Droite")
    INTERIEUR = "INTERIEUR", _("Intérieur")
    TOIT = "TOIT", _("Toit")


class Vitrage(TechnicienMixin, models.Model):
    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="vitrage",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="vitrage",
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

    kilometrage_vitrage = models.PositiveIntegerField(
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
    # VITRAGE ET RÉTROVISEURS
    # (chaque élément : état / fabricant / position / quantité / prix)
    # ======================================================

    # --- Pare-brise ---
    pare_brise = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Pare-brise"))
    pare_brise_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    pare_brise_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    pare_brise_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    pare_brise_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Impact / fissure (réparation pare-brise) ---
    impact_pare_brise = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Impact / fissure (réparation pare-brise)"))
    impact_pare_brise_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    impact_pare_brise_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    impact_pare_brise_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    impact_pare_brise_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Joint / collage du pare-brise ---
    joint_pare_brise = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Joint / collage du pare-brise"))
    joint_pare_brise_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    joint_pare_brise_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    joint_pare_brise_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    joint_pare_brise_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Capteur de pluie / luminosité ---
    capteur_pluie = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Capteur de pluie / luminosité"))
    capteur_pluie_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    capteur_pluie_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    capteur_pluie_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    capteur_pluie_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Caméra pare-brise (calibrage ADAS) ---
    camera_adas = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Caméra pare-brise (calibrage ADAS)"))
    camera_adas_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    camera_adas_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    camera_adas_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    camera_adas_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Lunette arrière ---
    lunette_arriere = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Lunette arrière"))
    lunette_arriere_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    lunette_arriere_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    lunette_arriere_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    lunette_arriere_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Dégivrage de la lunette arrière ---
    degivrage_lunette = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Dégivrage de la lunette arrière"))
    degivrage_lunette_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    degivrage_lunette_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    degivrage_lunette_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    degivrage_lunette_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Vitre de porte ---
    vitre_porte = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Vitre de porte"))
    vitre_porte_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    vitre_porte_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    vitre_porte_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    vitre_porte_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Mécanisme de lève-vitre ---
    leve_vitre = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Mécanisme de lève-vitre"))
    leve_vitre_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    leve_vitre_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    leve_vitre_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    leve_vitre_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Moteur de lève-vitre ---
    moteur_leve_vitre = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Moteur de lève-vitre"))
    moteur_leve_vitre_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    moteur_leve_vitre_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    moteur_leve_vitre_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    moteur_leve_vitre_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Joint / lèche-vitre ---
    joint_vitre = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Joint / lèche-vitre"))
    joint_vitre_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    joint_vitre_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    joint_vitre_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    joint_vitre_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Vitre de custode ---
    vitre_custode = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Vitre de custode"))
    vitre_custode_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    vitre_custode_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    vitre_custode_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    vitre_custode_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Toit ouvrant / toit vitré ---
    toit_ouvrant = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Toit ouvrant / toit vitré"))
    toit_ouvrant_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    toit_ouvrant_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    toit_ouvrant_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    toit_ouvrant_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Film teinté ---
    film_teinte = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Film teinté"))
    film_teinte_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    film_teinte_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    film_teinte_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    film_teinte_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Rétroviseur extérieur complet ---
    retroviseur_complet = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Rétroviseur extérieur complet"))
    retroviseur_complet_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    retroviseur_complet_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    retroviseur_complet_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    retroviseur_complet_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Glace de rétroviseur ---
    glace_retroviseur = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Glace de rétroviseur"))
    glace_retroviseur_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    glace_retroviseur_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    glace_retroviseur_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    glace_retroviseur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Coque de rétroviseur ---
    coque_retroviseur = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Coque de rétroviseur"))
    coque_retroviseur_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    coque_retroviseur_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    coque_retroviseur_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    coque_retroviseur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Moteur de réglage / rabattement du rétroviseur ---
    moteur_retroviseur = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Moteur de réglage / rabattement du rétroviseur"))
    moteur_retroviseur_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    moteur_retroviseur_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    moteur_retroviseur_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    moteur_retroviseur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Clignotant de rétroviseur ---
    clignotant_retroviseur = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Clignotant de rétroviseur"))
    clignotant_retroviseur_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    clignotant_retroviseur_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    clignotant_retroviseur_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    clignotant_retroviseur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Dégivrage de rétroviseur ---
    degivrage_retroviseur = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Dégivrage de rétroviseur"))
    degivrage_retroviseur_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    degivrage_retroviseur_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    degivrage_retroviseur_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    degivrage_retroviseur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # --- Rétroviseur intérieur ---
    retroviseur_interieur = models.CharField(max_length=25, choices=VitrageEtat.choices, default=VitrageEtat.OK, verbose_name=_("Rétroviseur intérieur"))
    retroviseur_interieur_fabricant = models.CharField(max_length=25, choices=FabricantVitrage.choices, default=FabricantVitrage.CHOISIR,
                                     verbose_name=_("Fabricant"))
    retroviseur_interieur_cote = models.CharField(max_length=25, choices=VitrageCote.choices, default=VitrageCote.CHOISIR,
                                verbose_name=_("Position"))
    retroviseur_interieur_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    retroviseur_interieur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

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
        related_name="vitrage",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="vitrage"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="vitrage"
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
    PIECES_DEF = [
        (_("Pare-brise"), "pare_brise"),
        (_("Impact / fissure (réparation pare-brise)"), "impact_pare_brise"),
        (_("Joint / collage du pare-brise"), "joint_pare_brise"),
        (_("Capteur de pluie / luminosité"), "capteur_pluie"),
        (_("Caméra pare-brise (calibrage ADAS)"), "camera_adas"),
        (_("Lunette arrière"), "lunette_arriere"),
        (_("Dégivrage de la lunette arrière"), "degivrage_lunette"),
        (_("Vitre de porte"), "vitre_porte"),
        (_("Mécanisme de lève-vitre"), "leve_vitre"),
        (_("Moteur de lève-vitre"), "moteur_leve_vitre"),
        (_("Joint / lèche-vitre"), "joint_vitre"),
        (_("Vitre de custode"), "vitre_custode"),
        (_("Toit ouvrant / toit vitré"), "toit_ouvrant"),
        (_("Film teinté"), "film_teinte"),
        (_("Rétroviseur extérieur complet"), "retroviseur_complet"),
        (_("Glace de rétroviseur"), "glace_retroviseur"),
        (_("Coque de rétroviseur"), "coque_retroviseur"),
        (_("Moteur de réglage / rabattement du rétroviseur"), "moteur_retroviseur"),
        (_("Clignotant de rétroviseur"), "clignotant_retroviseur"),
        (_("Dégivrage de rétroviseur"), "degivrage_retroviseur"),
        (_("Rétroviseur intérieur"), "retroviseur_interieur"),
    ]

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire_id and self.kilometrage_vitrage is not None:
            # Création : on compare au véhicule.
            # Modification : au kilométrage figé avant ce contrôle.
            if self.pk:
                minimum = self.kilometres_chassis or 0
            else:
                minimum = self.voiture_exemplaire.kilometres_chassis or 0

            if self.kilometrage_vitrage < minimum:
                raise ValidationError({
                    "kilometrage_vitrage": _(
                        "Le kilométrage du contrôle (%(km_controle)s) ne peut pas "
                        "être inférieur au kilométrage avant intervention (%(km_voiture)s)."
                    ) % {
                        "km_controle": self.kilometrage_vitrage,
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
            task_name = f"{_('Contrôle vitrage')} {self.voiture_exemplaire}"

            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.VITRAGE
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
        if self.kilometrage_vitrage is not None:
            self.kilometrage_variation = max(
                self.kilometrage_vitrage - (self.kilometres_chassis or 0), 0
            )
        else:
            self.kilometrage_variation = 0

        # =========================
        # SAUVEGARDE CONTRÔLE VITRAGE
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if self.voiture_exemplaire_id and self.kilometrage_vitrage is not None:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )
            if self.kilometrage_vitrage > (voiture.kilometres_chassis or 0):
                voiture.kilometres_chassis = self.kilometrage_vitrage
                voiture.save(update_fields=["kilometres_chassis"])

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle vitrage - {self.voiture_exemplaire.id}"
        return "Contrôle vitrage - non défini"

    class Meta:
        verbose_name = _("Contrôle vitrage")
        verbose_name_plural = _("Contrôles vitrage")

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
            if not etat or etat == VitrageEtat.NON_PRESENT:
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
            VitrageEtat.NOT_OK: _("À remplacer"),
            VitrageEtat.REMPLACE: _("Remplacé"),
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

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()
        total_pieces = rapport.get("total_pieces", Decimal("0.00"))
        cout_main_oeuvre = self.cout_main_oeuvre or Decimal("0.00")

        return (total_pieces + cout_main_oeuvre).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

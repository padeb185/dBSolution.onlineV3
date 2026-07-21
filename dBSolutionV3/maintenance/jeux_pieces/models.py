from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import RouesSerrageEtat, TAUX_HORAIRE_CHOICES
from utils.mixin import TechnicienMixin


# -------------------- Choices --------------------

class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")

class TypePieceControle(models.TextChoices):
    ROTULE_DIRECTION = "ROTULE_DIRECTION", _("Rotule de direction")
    ROTULE_SUSPENSION = "ROTULE_SUSPENSION", _("Rotule de suspension")
    BIELLETTE_BARRE_STAB = "BIELLETTE_BARRE_STAB", _("Biellette de barre stabilisatrice")
    BARRE_STABILISATRICE = "BARRE_STABILISATRICE", _("Barre stabilisatrice")
    AMORTISSEUR = "AMORTISSEUR", _("Amortisseur")
    ROULEMENT_ROUE = "ROULEMENT_ROUE", _("Roulement de roue")
    TRIANGLE = "TRIANGLE", _("Triangle")
    MULTI_BRAS = "MULTI_BRAS", _("Multi-bras")

class Emplacement(models.TextChoices):
    AVG = "AVG", _("Avant gauche")
    AVD = "AVD", _("Avant droit")
    ARG = "ARG", _("Arrière gauche")
    ARD = "ARD", _("Arrière droit")
    AV = "AV", _("Avant")
    AR = "AR", _("Arrière")
    SUP = "SUP", _("Supérieur")
    INF = "INF", _("Inférieur")

class EtatPiece(models.TextChoices):
    BON = "BON", _("Bon")
    USE = "USE", _("Usé")
    HS = "HS", _("Hors service")

class RoleUtilisateur(models.TextChoices):
    APPRENTI = "APPRENTI", _("Apprenti")
    MECANICIEN = "MECANICIEN", _("Mécanicien")
    CHEF = "CHEF", _("Chef mécanicien")

# -------------------- Modèle --------------------

class ControleJeuxPieces(TechnicienMixin, models.Model):
    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="jeux_pieces",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="jeux_pieces_checkup",
        verbose_name=_("Kilomètres jeu pièces"),
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_jeu = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du controle des jeux"),
    )

    # --- Jeux ---

    jeu_rotule_direction_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de direction avant droite"),
    )
    jeu_rotule_direction_avd_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la rotule de direction avant droite"),
    )
    jeu_rotule_direction_avd_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_rotule_direction_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de direction avant gauche"),
    )
    jeu_rotule_direction_avg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la rotule de direction avant gauche"),
    )
    jeu_rotule_direction_avg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_rotule_direction_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de direction arrière droite"),
    )
    jeu_rotule_direction_ard_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la rotule de direction arrière droite"),
    )
    jeu_rotule_direction_ard_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_rotule_direction_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de direction arrière gauche"),
    )
    jeu_rotule_direction_arg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la rotule de direction arrière gauche"),
    )
    jeu_rotule_direction_arg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_rotule_suspension_inferieure_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension inférieure avant droite"),
    )
    jeu_rotule_suspension_inferieure_avd_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la rotule de suspension inférieure avant droite"),
    )
    jeu_rotule_suspension_inferieure_avd_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_rotule_suspension_inferieure_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension inférieure avant gauche"),
    )
    jeu_rotule_suspension_inferieure_avg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la rotule de suspension inférieure avant gauche"),
    )
    jeu_rotule_suspension_inferieure_avg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_rotule_suspension_inferieure_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension inférieure arrière droite"),
    )
    jeu_rotule_suspension_inferieure_ard_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la rotule de suspension inférieure arrière droite"),
    )
    jeu_rotule_suspension_inferieure_ard_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_rotule_suspension_inferieure_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension inférieure arrière gauche"),
    )
    jeu_rotule_suspension_inferieure_arg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la rotule de suspension inférieure arrière gauche"),
    )
    jeu_rotule_suspension_inferieure_arg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_rotule_suspension_superieure_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension supérieure avant droite"),
    )
    jeu_rotule_suspension_superieure_avd_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la rotule de suspension supérieure avant droite"),
    )
    jeu_rotule_suspension_superieure_avd_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_rotule_suspension_superieure_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension supérieure avant gauche"),
    )
    jeu_rotule_suspension_superieure_avg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la rotule de suspension supérieure avant gauche"),
    )
    jeu_rotule_suspension_superieure_avg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_rotule_suspension_superieure_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension supérieure arrière droite"),
    )
    jeu_rotule_suspension_superieure_ard_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la rotule de suspension supérieure arrière droite"),
    )
    jeu_rotule_suspension_superieure_ard_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_rotule_suspension_superieure_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension supérieure arrière gauche"),
    )
    jeu_rotule_suspension_superieure_arg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la rotule de suspension supérieure arrière gauche"),
    )
    jeu_rotule_suspension_superieure_arg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_Biellette_barre_stabilisatrice_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu biellette de barre stabilisatrice avant droite"),
    )
    jeu_Biellette_barre_stabilisatrice_avd_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la biellette de barre stabilisatrice avant droite"),
    )
    jeu_Biellette_barre_stabilisatrice_avd_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_Biellette_barre_stabilisatrice_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu biellette de barre stabilisatrice avant gauche"),
    )
    jeu_Biellette_barre_stabilisatrice_avg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la biellette de barre stabilisatrice avant gauche"),
    )
    jeu_Biellette_barre_stabilisatrice_avg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_Biellette_barre_stabilisatrice_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu biellette de barre stabilisatrice arrière droite"),
    )
    jeu_Biellette_barre_stabilisatrice_ard_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la biellette de barre stabilisatrice arrière droite"),
    )
    jeu_Biellette_barre_stabilisatrice_ard_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_Biellette_barre_stabilisatrice_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu biellette de barre stabilisatrice arrière gauche"),
    )
    jeu_Biellette_barre_stabilisatrice_arg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la biellette de barre stabilisatrice arrière gauche"),
    )
    jeu_Biellette_barre_stabilisatrice_arg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_barre_stabilisatrice_av = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu barre stabilisatrice avant"),
    )
    jeu_barre_stabilisatrice_av_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la barre stabilisatrice avant"),
    )
    jeu_barre_stabilisatrice_av_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_barre_stabilisatrice_ar = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu barre stabilisatrice arrière"),
    )
    jeu_barre_stabilisatrice_ar_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la barre stabilisatrice arrière"),
    )
    jeu_barre_stabilisatrice_ar_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_amortisseur_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu amortisseur avant droit"),
    )
    jeu_amortisseur_avd_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de l'amortisseur avant droit"),
    )
    jeu_amortisseur_avd_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_amortisseur_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu amortisseur avant gauche"),
    )
    jeu_amortisseur_avg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de l'amortisseur avant gauche"),
    )
    jeu_amortisseur_avg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_amortisseur_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu amortisseur arrière droit"),
    )
    jeu_amortisseur_ard_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de l'amortisseur arrière droit"),
    )
    jeu_amortisseur_ard_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_amortisseur_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu amortisseur arrière gauche"),
    )
    jeu_amortisseur_arg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de l'amortisseur arrière gauche"),
    )
    jeu_amortisseur_arg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_roulement_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu roulement avant droit"),
    )
    jeu_roulement_avd_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du roulement avant droit"),
    )
    jeu_roulement_avd_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_roulement_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu roulement avant gauche"),
    )
    jeu_roulement_avg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du roulement avant gauche"),
    )
    jeu_roulement_avg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_roulement_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu roulement arrière droit"),
    )
    jeu_roulement_ard_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du roulement arrière droit"),
    )
    jeu_roulement_ard_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_roulement_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu roulement arrière gauche"),
    )
    jeu_roulement_arg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du roulement arrière gauche"),
    )
    jeu_roulement_arg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_triangle_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu triangle avant droit"),
    )
    jeu_triangle_avd_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du triangle avant droit"),
    )
    jeu_triangle_avd_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_triangle_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu triangle avant gauche"),
    )
    jeu_triangle_avg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du triangle avant gauche"),
    )
    jeu_triangle_avg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_triangle_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu triangle arrière droit"),
    )
    jeu_triangle_ard_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du triangle arrière droit"),
    )
    jeu_triangle_ard_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_triangle_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu triangle arrière gauche"),
    )
    jeu_triangle_arg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix du triangle arrière gauche"),
    )
    jeu_triangle_arg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_multi_bras_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu suspension multi-bras avant droit"),
    )
    jeu_multi_bras_avd_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la suspension multi-bras avant droite"),
    )
    jeu_multi_bras_avd_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_multi_bras_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu suspension multi-bras avant gauche"),
    )
    jeu_multi_bras_avg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la suspension multi-bras avant gauche"),
    )
    jeu_multi_bras_avg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_multi_bras_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu suspension multi-bras arrière droit"),
    )
    jeu_multi_bras_ard_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la suspension multi-bras arrière droite"),
    )
    jeu_multi_bras_ard_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    jeu_multi_bras_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu suspension multi-bras arrière gauche"),
    )
    jeu_multi_bras_arg_prix = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix de la suspension multi-bras arrière gauche"),
    )
    jeu_multi_bras_arg_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )


    # Tag visuel
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
        verbose_name=_("Remarques"), blank=True, null=True)

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jeux_pieces",
        verbose_name=_("Main d'oeuvre")
    )

    # Champ pour l’utilisateur affecté (utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Utilisateur"),
        related_name="controle_jeux_utilisateurs"
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
        related_name="controle_jeux_societe"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    # Méthode pour assigner l’utilisateur courant automatiquement
    def assign_technicien(self, user):
        """Assigne l'utilisateur courant et met à jour les champs dérivés"""
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Contrôle Jeu")
        verbose_name_plural = _("Contrôles Jeux")

    def __str__(self):
        return _("Controle des jeux – Maintenance %(id)s") % {"id": self.maintenance.id}

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_jeu is not None:
            if self.kilometrage_jeu < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_checkup': _(
                        f"Le kilométrage du check-up ({self.kilometrage_jeu}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):

        if self.voiture_exemplaire and self.kilometrage_jeu:
            if self.kilometrage_jeu > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_jeu
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        # ----------------------------
        # MAIN D'OEUVRE AUTO DESCRIPTIF
        # ----------------------------
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Controle des jeux") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        super().save(*args, **kwargs)



    def generer_rapport_remplacement(self):
            rapport = []
            total_general = Decimal("0.00")

            for field in self._meta.fields:
                field_name = field.name

                # Garder uniquement les CharField utilisant EtatOKNotOK
                if not (
                        isinstance(field, models.CharField)
                        and field.choices == EtatOKNotOK.choices
                ):
                    continue

                etat = getattr(self, field_name, None)

                if etat not in [
                    EtatOKNotOK.A_REMPLACER,
                    EtatOKNotOK.REMPLACE,
                ]:
                    continue

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
                    "etat": etat,
                    "etat_label": dict(
                        EtatOKNotOK.choices
                    ).get(etat, etat),
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


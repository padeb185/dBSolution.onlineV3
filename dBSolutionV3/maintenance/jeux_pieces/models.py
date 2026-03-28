from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.mixin import TechnicienMixin


# -------------------- Choices --------------------

class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("Non")
    NOT_OK = "NOT_OK", _("Oui")
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
        null=True,  # autorisé vide à la création
        blank=True,
        default=1
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
        blank=True
    )

    kilometrage_jeu = models.PositiveIntegerField(
        _("Kilométrage au moment du controle des jeux"),
        null=True,
        blank=True
    )

    # --- Jeux ---

    jeu_rotule_direction_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu rotule de direction avant droite"))
    jeu_rotule_direction_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu rotule de direction avant gauche"))
    jeu_rotule_direction_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu rotule de direction arrière droite"))
    jeu_rotule_direction_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu rotule de direction arrière gauche"))


    jeu_rotule_suspension_inferieure_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension inférieure avant droite"))
    jeu_rotule_suspension_inferieure_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension inférieure avant gauche"))
    jeu_rotule_suspension_inferieure_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension inférieure arrière droite"))
    jeu_rotule_suspension_inferieure_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension inférieure arrière droite"))

    jeu_rotule_suspension_superieure_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure avant droite"))
    jeu_rotule_suspension_superieure_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure avant gauche"))
    jeu_rotule_suspension_superieure_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure arrière droite"))
    jeu_rotule_suspension_superieure_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure arrière droite"))

    jeu_Biellette_barre_stabilisatrice_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de barre stabilisatrice avant droite"))
    jeu_Biellette_barre_stabilisatrice_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de barre stabilisatrice avant gauche"))
    jeu_Biellette_barre_stabilisatrice_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de barre stabilisatrice arrière droite"))
    jeu_Biellette_barre_stabilisatrice_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de barre stabilisatrice arrière gauche"))

    jeu_barre_stabilisatrice_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu barre stabilisatrice avant"))
    jeu_barre_stabilisatrice_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu barre stabilisatrice arrière"))

    jeu_amortisseur_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu amortisseur avant droit"))
    jeu_amortisseur_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu amortisseur avant gauche"))
    jeu_amortisseur_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu amortisseur arrière droit"))
    jeu_amortisseur_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu amortisseur arrière gauche"))

    jeu_roulement_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu roulement avant droit"))
    jeu_roulement_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu roulement avant gauche"))
    jeu_roulement_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu roulement arrière droit"))
    jeu_roulement_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu roulement arrière gauche"))

    jeu_triangle_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle avant droit"))
    jeu_triangle_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle avant gauche"))
    jeu_triangle_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle arrière droit"))
    jeu_triangle_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle arrière gauche"))

    jeu_multi_bras_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras avant droit"))
    jeu_multi_bras_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras avant gauche"))
    jeu_multi_bras_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras arrière droit"))
    jeu_multi_bras_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras arrière gauche"))

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
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_jeu:
            if self.kilometrage_jeu > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_jeu
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        super().save(*args, **kwargs)


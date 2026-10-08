from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class Electronique(Piece):

    TYPE_PIECE_ELECTRONIQUE = (
        ("debitmetre", _("Débitmètre")),
        ("sonde_temp_eau", _("Sonde de température eau")),
        ("sonde_temp_huile", _("Sonde de température d’huile")),
        ("capteur_cliquetis", _("Capteur de cliquetis")),
        ("sonde_lambda", _("Sonde lambda")),
        ("capteur_aac", _("Capteur d'arbre à came")),
        ("capteur_vilebrequin", _("Capteur vilebrequin")),
        ("sonde_press_filtre_particule", _("Sonde de pression filtre à particules")),
        ("vanne_egr", _("Vanne EGR")),
        ("boitier_papillon", _("Boîtier papillon")),
        ("electrovanne_turbo", _("Électrovanne de turbo")),
        ("sonde_press_turbo", _("Sonde pression turbo")),
        ("capteur_abs", _("Capteur ABS")),
        ("accelerateur", _("Accélérateur")),
        ("contacteur_feux_stop", _("Contacteur feux stop")),
        ("calculateur_abs", _("Calculateur ABS")),
        ("calculateur_moteur", _("Calculateur moteur")),
        ("boitier_servitude_int", _("Boîtier servitude intérieur")),
        ("fusibles", _("Fusibles")),
        ("boitier_additionnel", _("Boîtier additionnel")),
        ("radar_recul", _("Radar de recul")),
        ("capteur_pression_pneus", _("Capteur pression pneus")),
        ("capteur_pression_adm", _("Capteur pression admission")),
        ("regulateur_pression_carb", _("Régulateur pression carburant")),
        ("capteur_niveau_huile", _("Capteur niveau huile")),
        ("capteur_niveau_liquide_freins", _("Capteur niveau liquide freins")),
        ("calculateur_bdv", _("Calculateur de boîte de vitesse")),
        ("relais_prechauffage", _("Relais de préchauffage")),
        ("relais", _("Relais")),
        ("resistance_chauffage", _("Résistance de chauffage")),
        ("capteur_temp_adm", _("Capteur de température d’admission")),
        ("capteur_emb", _("Capteur d’embrayage")),
    )

    type_piece_electronique = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_ELECTRONIQUE
    )

    # 🔗 compatibilité moteur ou véhicule (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="electroniques",
        blank=True
    )

    class Meta:
        verbose_name = "Pièce électronique"
        verbose_name_plural = "Pièces électroniques"

    def __str__(self):
        return f"{self.get_type_piece_electronique_display()} – {super().__str__()}"

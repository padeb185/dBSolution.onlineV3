from django.db import models
from piece.models import Piece

class Electronique(Piece):

    TYPE_PIECE_ELECTRONIQUE = (
        ("débitmètre", "Débitmètre"),
        ("sonde_temp_eau", "Sonde de température eau"),
        ("sonde_temp_huile", "Sonde de température d’huile"),
        ("capteur_cliquetis", "Capteur de cliquetis"),
        ("sonde_lambda", "Sonde lambda"),
        ("capteur_aac", "Capteur d'arbre à came"),
        ("capteur-vilebrequin", "Capteur Vilebrequin"),
        ("sonde_press_filtre_particule", "Sonde de pression filtre à particule"),
        ("vanne_egr", "Vanne EGR"),
        ("boitier_papillon", "Boîtier papillon"),
        ("électrovanne_turbo", "Électrovanne de turbo"),
        ("sonde_press_turbo", "Sonde pression turbo"),
        ("capteur_abs", "Capteur ABS"),
        ("accélérateur", "Accélérateur"),
        ("contacteur_feux_stop", "Contacteur feux stop"),
        ("sonde_lambda", "Sonde lambda"),
        ("calculateur_abs", "Calculateur ABS"),
        ("calculateur_moteur", "Calculateur moteur"),
        ("boitier_servitude_int", "Boîtier servitude intérieur"),
        ("fusibles", "Fusibles"),
        ("boitier_additionnel", "Boîtier additionnel"),
        ("radar_recul", "Radar de recul"),
        ("capteur_pression_pneus", "Capteur pression pneus"),
        ("capteur_pression_adm", "Capteur pression admission"),
        ("régulateur_pression_carb", "Régulateur pression carburant"),
        ("Capteur_niveau_huile", "Capteur niveau huile"),
        ("capteur_niveau_liquide_freins", "Capteur niveau liquide freins"),
        ("calculateur_bdv", "Calculateur Boite De Vitesse"),
        ("relais_préchauffage", "Relais de préchauffage"),
        ("relais", "Relais"),
        ("Résistance_chauffage", "Résistance de chauffage"),
        ("capteur_temp_adm", "Capteur de température d'admission"),
        ("sonde_temp_huile", "Sonde de température d'huile"),
        ("capteur_emb", "Capteur d'embrayage"),

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

from django.db import models
from piece.models import Piece


class PieceMoteur(Piece):

    TYPE_PIECE_MOTEUR = (
        ("arbre_came_ad", "Arbre à cames admission"),
        ("arbre_came_ec", "Arbre à cames échappement"),
        ("vilebrequin", "Vilebrequin"),
        ("bielle", "Bielle"),
        ("durite_eau", "Durite Eau"),
        ("durite_huile","Durite Huile"),
        ("durite_carburant", "Durite Carburant"),
        ("piston", "Piston"),
        ("soupape", "Soupape"),
        ("bloc", "Bloc moteur"),
        ("ressorts_soupape", "Ressorts de Soupapes"),
        ("culbuteurs", "Culbuteurs"),
        ("culasse", "Culasse"),
        ("carter_huile", "Carter Huile"),
        ("pompe_huile", "Pompe Huile"),
        ("échangeur", "Échangeur"),
        ("pressoirs_hydraulique", "Pressoirs Hydraulique"),
        ("joint_culasse", "Joint de Culasse"),
        ("Poulie_AAC_ADM", "Poulie Arbre A Came Admission"),
        ("Poulie_AAC_ECH", "Poulie Arbre A Came Échappement"),
        ("poulie_vilebrequin", "Poulie de Vilebrequin"),
        ("distribution", "Distribution"),
        ("chaine distribution", "Chaine de Distribution"),
        ("Courroie_distribution", "Courroie de Distribution"),
        ("galets", "Galets"),
        ("galet_tendeur", "Galet Tendeur"),
        ("cache_soupapes", "Cache Soupapes"),
        ("Bougies_allumage", "Bougies Allumage"),
        ("bougies_préchauffage", "Bougies Préchauffage"),
        ("vanne_EGR", "Vanne EGR"),
        ("collecteur_admission", "Collecteur d'admission"),
        ("Collecteur_échappement", "Collecteur d'échappement"),
        ("injecteurs", "Injecteurs"),
        ("pompe_carburant", "Pompe à Carburant"),
        ("rampe_injection", "Rampe d'injection"),
        ("turbo", "Turbo"),
        ("joint", "Joint moteur"),
        ("kit_joints", "Kit de joints"),
        ("poussoirs", "Poussoirs"),
        ("pompe_eau", "Pompe à Eau"),
        ("pompe_vide", "Pompe à vide")

    )

    type_piece_moteur = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_MOTEUR
    )

    # 🔗 compatibilité moteur (N↔N)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="pieces_moteur",
        blank=True
    )

    class Meta:
        verbose_name = "Pièce moteur"
        verbose_name_plural = "Pièces moteur"

    def __str__(self):
        return f"{self.get_type_piece_moteur_display()} – {super().__str__()}"

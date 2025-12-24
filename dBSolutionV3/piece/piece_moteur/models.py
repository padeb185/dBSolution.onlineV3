from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece

class PieceMoteur(Piece):

    TYPE_PIECE_MOTEUR = (
        ("arbre_came_ad", _("Arbre à cames admission")),
        ("arbre_came_ec", _("Arbre à cames échappement")),
        ("vilebrequin", _("Vilebrequin")),
        ("bielle", _("Bielle")),
        ("durite_eau", _("Durite Eau")),
        ("durite_huile", _("Durite Huile")),
        ("durite_carburant", _("Durite Carburant")),
        ("piston", _("Piston")),
        ("soupape", _("Soupape")),
        ("bloc", _("Bloc moteur")),
        ("ressorts_soupape", _("Ressorts de Soupapes")),
        ("culbuteurs", _("Culbuteurs")),
        ("culasse", _("Culasse")),
        ("carter_huile", _("Carter Huile")),
        ("pompe_huile", _("Pompe Huile")),
        ("echangeur", _("Échangeur")),
        ("pressoirs_hydraulique", _("Pressoirs Hydraulique")),
        ("joint_culasse", _("Joint de Culasse")),
        ("Poulie_AAC_ADM", _("Poulie Arbre A Came Admission")),
        ("Poulie_AAC_ECH", _("Poulie Arbre A Came Échappement")),
        ("poulie_vilebrequin", _("Poulie de Vilebrequin")),
        ("distribution", _("Distribution")),
        ("chaine_distribution", _("Chaine de Distribution")),
        ("Courroie_distribution", _("Courroie de Distribution")),
        ("galets", _("Galets")),
        ("galet_tendeur", _("Galet Tendeur")),
        ("cache_soupapes", _("Cache Soupapes")),
        ("Bougies_allumage", _("Bougies Allumage")),
        ("bougies_préchauffage", _("Bougies Préchauffage")),
        ("vanne_EGR", _("Vanne EGR")),
        ("collecteur_admission", _("Collecteur d'admission")),
        ("Collecteur_échappement", _("Collecteur d'échappement")),
        ("injecteurs", _("Injecteurs")),
        ("pompe_carburant", _("Pompe à Carburant")),
        ("rampe_injection", _("Rampe d'injection")),
        ("turbo", _("Turbo")),
        ("joint", _("Joint moteur")),
        ("kit_joints", _("Kit de joints")),
        ("poussoirs", _("Poussoirs")),
        ("pompe_eau", _("Pompe à Eau")),
        ("pompe_vide", _("Pompe à vide"))
    )

    type_piece_moteur = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_MOTEUR,
        verbose_name=_("Type de pièce moteur")
    )

    # 🔗 compatibilité moteur (N↔N)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="pieces_moteur",
        blank=True
    )

    class Meta:
        verbose_name = _("Pièce moteur")
        verbose_name_plural = _("Pièces moteur")

    def __str__(self):
        return _("%(type)s – %(nom)s") % {
            "type": self.get_type_piece_moteur_display(),
            "nom": super().__str__()
        }

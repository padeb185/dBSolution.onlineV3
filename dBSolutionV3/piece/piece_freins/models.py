from django.db import models
from piece.models import Piece

class PieceFreins(Piece):

    TYPE_PIECE_FREINAGE = (
        ("machoire_frein_avg", "Mâchoire de frein AVG"),
        ("machoire_frein_avd", "Mâchoire de frein AVD"),
        ("machoire_frein_arg", "Mâchoire de frein ARG"),
        ("machoire_frein_ard", "Mâchoire de frein ARD"),
        ("plaquettes_av", "Plaquettes AV"),
        ("plaquettes_ar", "Plaquettes AR"),
        ("disques_av", "Disques AV"),
        ("disques_ar", "Disques AR"),
        ("epaisseur_av", "Épaisseur AV"),
        ("epaisseur_ar", "Épaisseur AR"),
        ("epaisseur_min_av", "Épaisseur min AV"),
        ("epaisseur_min_ar", "Épaisseur min AR"),
        ("porte_etrier", "Porte étrier"),
        ("pompe_abs", "Pompe ABS"),
        ("liquide_qualite", "Liquide qualité"),
        ("servo_frein", "Servo-frein"),
        ("maitre_cylindre", "Maître-cylindre"),
        ("cylindre_recepteur", "Cylindre récepteur AV/AR G/D"),
        ("petites_fournitures", "Petites fournitures freins"),
        ("graisse", "Graisse"),
        ("kit_reparation_machoire", "Kit réparation mâchoire"),
        ("soufflet", "Soufflet"),
        ("coulisseaux", "Coulisseaux"),
        ("visserie", "Visserie"),
        ("flexibles", "Flexibles"),
        ("tuyau", "Tuyau"),
        ("nippe", "Nippe"),
        ("master_vac", "Master vac"),
    )

    type_piece_frein = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_FREINAGE
    )

    # 🔗 compatibilité moteur (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="freinages",
        blank=True
    )

    class Meta:
        verbose_name = "Pièce de freinage"
        verbose_name_plural = "Pièces de freinage"

    def __str__(self):
        return f"{self.get_type_piece_frein_display()} – {super().__str__()}"

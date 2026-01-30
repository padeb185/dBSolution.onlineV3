from maintenance.models import (
    Maintenance, ControleGeneral, AmortisseurControle, RessortControle,
    ControleBruit, JeuPiece, ControleFreins, NettoyageExterieur, NettoyageInterieur
)
from voiture_exemplaire.models import VoitureExemplaire
from utilisateurs.models import Utilisateur


def creer_maintenance_complete(exemplaire: VoitureExemplaire, mecanicien: Utilisateur):
    # 1. Créer l'objet Maintenance
    maintenance = Maintenance.objects.create(voiture=exemplaire,
                                             status="EN_COURS")  # adapte selon ton modèle Maintenance

    # 2. Contrôle général
    controle_general = ControleGeneral.objects.create(maintenance=maintenance)

    # Ajouter amortisseurs
    for loc in ["AVG", "AVD", "ARG", "ARD"]:
        AmortisseurControle.objects.create(controle_general=controle_general, emplacement=loc)

    # Ajouter ressorts
    for loc in ["AVG", "AVD", "ARG", "ARD"]:
        RessortControle.objects.create(controle_general=controle_general, emplacement=loc)

    # 3. Bruits
    for loc in ["AVG", "AVD", "ARG", "ARD"]:
        for type_bruit in ["ROULEMENT_ROUE", "ROULEMENT_SUSPENSION", "MOTEUR", "BOITE_VITESSE", "PONT"]:
            ControleBruit.objects.create(
                maintenance=maintenance,
                emplacement=loc,
                type_bruit=type_bruit
            )

    # 4. Pièces
    for loc in ["AVG", "AVD", "ARG", "ARD"]:
        for piece in ["ROTULE_DIRECTION", "ROTULE_SUSPENSION", "BIELLETTE_BARRE_STAB",
                      "BARRE_STABILISATRICE", "AMORTISSEUR", "ROULEMENT_ROUE",
                      "TRIANGLE", "MULTI_BRAS"]:
            JeuPiece.objects.create(
                maintenance=maintenance,
                vehicle=exemplaire,
                type_piece=piece,
                emplacement=loc
            )

    # 5. Freins
    for partie in ["AVANT", "ARRIERE", "AV_AR"]:
        ControleFreins.objects.create(
            maintenance=maintenance,
            partie=partie,
            usure_plaquettes=0.0,
            epaisseur_disques=100.0
        )

    # 6. Nettoyage
    NettoyageExterieur.objects.create(maintenance=maintenance, voiture_exemplaire=exemplaire, mecanicien=mecanicien)
    NettoyageInterieur.objects.create(maintenance=maintenance, voiture_exemplaire=exemplaire, mecanicien=mecanicien)

    return maintenance

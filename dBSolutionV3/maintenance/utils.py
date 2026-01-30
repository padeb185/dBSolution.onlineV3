from django.template.loader import render_to_string
from weasyprint import HTML
from maintenance.models import Maintenance
from maintenance.check_up.models import ControleGeneral, AmortisseurControle, RessortControle, ControleBruit, JeuPiece, \
    ControleFreins, NettoyageInterieur, NettoyageExterieur
from utilisateurs.models import Utilisateur
from voiture.voiture_exemplaire.models import VoitureExemplaire


def generate_maintenance_report(maintenance: Maintenance):
    """
    Génère un rapport PDF complet pour une maintenance donnée.
    Inclut :
    - Jeux de pièces
    - Niveaux de fluides
    - Contrôle freins
    - Silentblocs et bruits
    - Contrôle général
    - Nettoyage intérieur / extérieur
    """

    # Jeux de pièces
    jeux = maintenance.jeux_pieces.all()

    # Notes et rapport
    notes = maintenance.notes.all()

    # Niveaux de fluides
    niveaux = maintenance.niveaux.all() if hasattr(maintenance, "niveaux") else []

    # Contrôle freins
    controle_freins = getattr(maintenance, "controle_freins", None)

    # Silentblocs
    silentblocs = getattr(maintenance, "silent_blocs", None)

    # Bruits
    bruits = getattr(maintenance, "bruits", None)

    # Contrôle général
    controle_general = getattr(maintenance, "controle_general", None)

    # Nettoyage
    nettoyage_int = getattr(maintenance, "nettoyageinterieur_set", None)
    nettoyage_ext = getattr(maintenance, "nettoyageexterieur_set", None)

    # Préparer le rendu HTML
    html = render_to_string(
        "maintenance/rapport_pdf.html",
        {
            "maintenance": maintenance,
            "jeux": jeux,
            "notes": notes,
            "niveaux": niveaux,
            "controle_freins": controle_freins,
            "silentblocs": silentblocs,
            "bruits": bruits,
            "controle_general": controle_general,
            "nettoyage_int": nettoyage_int,
            "nettoyage_ext": nettoyage_ext,
            "critique": maintenance.has_critical_issue() if hasattr(maintenance, "has_critical_issue") else False,
        }
    )

    # Générer PDF
    pdf_file = HTML(string=html).write_pdf()
    return pdf_file





def creer_maintenance_complete(exemplaire: VoitureExemplaire, mecanicien: Utilisateur, tenant):

    # 1. Créer l'objet Maintenance lié au tenant
    maintenance = Maintenance.objects.create(
        voiture=exemplaire,
        status="EN_COURS",
        tenant=tenant  # <--- ici on assigne le tenant
    )

    # 2. Contrôle général
    controle_general = ControleGeneral.objects.create(
        maintenance=maintenance
    )

    # Amortisseurs
    for loc in ["AVG", "AVD", "ARG", "ARD"]:
        AmortisseurControle.objects.create(
            controle_general=controle_general
        , emplacement=loc
        )

    # Ressorts
    for loc in ["AVG", "AVD", "ARG", "ARD"]:
        RessortControle.objects.create(
            controle_general=controle_general
        , emplacement=loc
        )

    # Bruits
    for loc in ["AVG", "AVD", "ARG", "ARD"]:
        for type_bruit in ["ROULEMENT_ROUE", "ROULEMENT_SUSPENSION", "MOTEUR", "BOITE_VITESSE", "PONT"]:
            ControleBruit.objects.create(
                maintenance=maintenance,
                emplacement=loc,
                type_bruit=type_bruit
            )

    # Pièces
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

    # Freins
    for partie in ["AVANT", "ARRIERE", "AV_AR"]:
        ControleFreins.objects.create(
            maintenance=maintenance,
            partie=partie,
            usure_plaquettes=0.0,
            epaisseur_disques=100.0
        )

    # Nettoyage
    NettoyageExterieur.objects.create(
        maintenance=maintenance, voiture_exemplaire=exemplaire,
        mecanicien=mecanicien,

    )
    NettoyageInterieur.objects.create(
        maintenance=maintenance, voiture_exemplaire=exemplaire,
        mecanicien=mecanicien
    )

    return maintenance

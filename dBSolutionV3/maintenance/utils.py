from django.template.loader import render_to_string
from weasyprint import HTML

from django.template.loader import render_to_string
from weasyprint import HTML
from maintenance.models import (
    Maintenance,
    ControleGeneral,
    NettoyageInterieur,
    NettoyageExterieur
)

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

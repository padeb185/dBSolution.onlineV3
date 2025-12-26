from django.template.loader import render_to_string
from weasyprint import HTML



def generate_maintenance_report(maintenance):
    jeux = maintenance.jeux_pieces.all()
    niveaux = maintenance.niveaux.all()  # lien avec les fluides
    freins = maintenance.controles_freins.all()
    notes = maintenance.notes.all()

    # Détecte les éléments critiques pour mettre le tag rouge
    for jeu in jeux:
        jeu.tag = "ROUGE" if jeu.etat == "HS" else jeu.tag

    for niveau in niveaux:
        niveau.tag = "ROUGE" if niveau.is_critique() else niveau.tag

    for frein in freins:
        frein.tag = "ROUGE" if frein.is_critique() else "VERT"

    html = render_to_string(
        "maintenance/rapport_pdf.html",
        {
            "maintenance": maintenance,
            "jeux": jeux,
            "niveaux": niveaux,
            "freins": freins,
            "notes": notes,
        }
    )

    return HTML(string=html).write_pdf()

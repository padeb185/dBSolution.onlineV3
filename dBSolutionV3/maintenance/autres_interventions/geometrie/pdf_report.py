# geometrie/pdf_report.py

from io import BytesIO
from django.http import HttpResponse
from django.utils.timezone import localtime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_geometrie_pdf(geometrie):
    """
    Génère un rapport PDF complet pour un objet GeometrieVoiture
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------------------------------------------------
    # TITRE
    # ---------------------------------------------------
    elements.append(
        Paragraph(
            "<b>RAPPORT DE GÉOMÉTRIE VEHICULE</b>",
            styles["Title"]
        )
    )
    elements.append(Spacer(1, 10))

    # ---------------------------------------------------
    # INFOS GENERALES
    # ---------------------------------------------------
    voiture = geometrie.voiture_exemplaire

    data_info = [
        ["Date", localtime(geometrie.date).strftime("%d/%m/%Y %H:%M") if geometrie.date else ""],
        ["Technicien", geometrie.tech_nom_technicien or ""],
        ["Société", str(geometrie.tech_societe) if geometrie.tech_societe else ""],
        ["Véhicule", str(voiture) if voiture else ""],
        ["Kilométrage actuel", f"{geometrie.kilometres_chassis} km"],
        ["Kilométrage géométrie", f"{geometrie.kilometrage_geometrie or 0} km"],
        ["Tag", geometrie.tag],
    ]

    table = Table(data_info, colWidths=[70 * mm, 100 * mm])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # ---------------------------------------------------
    # ANGLES
    # ---------------------------------------------------
    elements.append(Paragraph("<b>Angles de suspension</b>", styles["Heading2"]))
    elements.append(Spacer(1, 5))

    data_angles = [
        ["Mesure", "Valeur"],
        ["Carrossage avant droit", f"{geometrie.carrossage_avant_droit}°"],
        ["Carrossage avant gauche", f"{geometrie.carrossage_avant_gauche}°"],
        ["Carrossage arrière droit", f"{geometrie.carrossage_arriere_droit}°"],
        ["Carrossage arrière gauche", f"{geometrie.carrossage_arriere_gauche}°"],
        ["Chasse droite", f"{geometrie.chasse_droite}°"],
        ["Chasse gauche", f"{geometrie.chasse_gauche}°"],
        ["Pincement avant droit", f"{geometrie.pincement_avant_droit}°"],
        ["Pincement avant gauche", f"{geometrie.pincement_avant_gauche}°"],
        ["Pincement arrière droit", f"{geometrie.pincement_arriere_droit}°"],
        ["Pincement arrière gauche", f"{geometrie.pincement_arriere_gauche}°"],
        ["Poussée arrière", f"{geometrie.poussee_arriere}°"],
        ["Angle pivot", f"{geometrie.angle_pivot}°"],
    ]

    table = Table(data_angles, colWidths=[120 * mm, 50 * mm])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # ---------------------------------------------------
    # SUSPENSION
    # ---------------------------------------------------
    elements.append(Paragraph("<b>Suspension</b>", styles["Heading2"]))
    elements.append(Spacer(1, 5))

    data_suspension = [
        ["Hauteur de caisse", f"{geometrie.hauteur_caisse or ''} mm"],
        ["Débattement avant", f"{geometrie.debattement_suspension_avant or ''} mm"],
        ["Débattement arrière", f"{geometrie.debattement_suspension_arriere or ''} mm"],
        ["Raideur ressort avant", geometrie.raideur_ressort_avant or ""],
        ["Raideur ressort arrière", geometrie.raideur_ressort_arriere or ""],
        ["Marque amortisseurs", geometrie.amortisseur_marque or ""],
        ["Amortissement AV rebond", geometrie.amortissement_avant_rebond or ""],
        ["Amortissement AV compression", geometrie.amortissement_avant_compression or ""],
        ["Amortissement AR rebond", geometrie.amortissement_arriere_rebond or ""],
        ["Amortissement AR compression", geometrie.amortissement_arriere_compression or ""],
    ]

    table = Table(data_suspension, colWidths=[120 * mm, 50 * mm])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # ---------------------------------------------------
    # REMARQUES
    # ---------------------------------------------------
    elements.append(Paragraph("<b>Remarques</b>", styles["Heading2"]))
    elements.append(Spacer(1, 5))
    elements.append(
        Paragraph(
            geometrie.remarques or "Aucune remarque.",
            styles["Normal"]
        )
    )

    # ---------------------------------------------------
    # BUILD
    # ---------------------------------------------------
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="rapport_geometrie.pdf"'
    response.write(pdf)

    return response
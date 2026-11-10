"""
Récapitulatif du véhicule (PDF imprimable) : identité, coûts totaux par poste (camembert), revente et coût net,
consommation, type d'achat, entretiens / maintenances, pneus, documents et rappels, vente.
Formule Bronze minimum (voir VehiculeViewSet.recapitulatif).
"""
import math
from datetime import date
from decimal import Decimal as D

from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from .calculs import consommation, statut_rappel, synthese
from .plaque import plaque_svg

COULEURS = ["#2563EB", "#F59E0B", "#10B981", "#EF4444", "#8B5CF6", "#06B6D4", "#EC4899", "#84CC16", "#64748B",
            "#F97316", "#14B8A6", "#A855F7"]


def camembert_svg(postes, taille=180):
    """Camembert SVG (rendu par WeasyPrint) : [(montant, couleur)]."""
    total = sum(float(m) for m, _c in postes)
    if total <= 0:
        return ""
    r, c = taille / 2 - 2, taille / 2
    if len(postes) == 1:
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{taille}" height="{taille}">'
                f'<circle cx="{c}" cy="{c}" r="{r}" fill="{postes[0][1]}"/>'
                f'<circle cx="{c}" cy="{c}" r="{r * 0.55}" fill="#fff"/></svg>')
    morceaux, angle = [], -math.pi / 2
    for montant, couleur in postes:
        part = float(montant) / total * 2 * math.pi
        if part <= 0:
            continue
        x1, y1 = c + r * math.cos(angle), c + r * math.sin(angle)
        angle += part
        x2, y2 = c + r * math.cos(angle), c + r * math.sin(angle)
        grand = 1 if part > math.pi else 0
        morceaux.append(f'<path d="M{c},{c} L{x1:.2f},{y1:.2f} A{r},{r} 0 {grand},1 {x2:.2f},{y2:.2f} Z" '
                        f'fill="{couleur}" stroke="#fff" stroke-width="1.5"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{taille}" height="{taille}">{"".join(morceaux)}'
            f'<circle cx="{c}" cy="{c}" r="{r * 0.55}" fill="#fff"/></svg>')


def contexte(vehicule):
    from .models import VenteParticulier
    s = synthese(vehicule)
    postes = [p for p in s["postes"] if D(p["montant"] or 0) > 0]
    total = sum((D(p["montant"]) for p in postes), D(0))
    for i, p in enumerate(postes):
        p["couleur"] = COULEURS[i % len(COULEURS)]
        p["pct"] = (D(p["montant"]) * 100 / total).quantize(D("0.1")) if total else None
    km_actuel = vehicule.kilometrage_actuel
    entretiens = sorted(
        [{"date": e.date, "libelle": str(e.get_type_display()), "garage": e.garage, "km": e.kilometrage,
          "pieces": e.pieces, "main_oeuvre": e.main_oeuvre, "montant": e.montant} for e in vehicule.entretiens.all()]
        + [{"date": m.date, "libelle": str(m.get_type_maintenance_display()), "garage": m.garage, "km": m.kilometrage,
            "pieces": m.total_pieces_tvac, "main_oeuvre": m.total_main_oeuvre_tvac, "montant": m.total_tvac}
           for m in vehicule.maintenances.all()],
        key=lambda x: x["date"], reverse=True)
    pneus = [{"t": t, "km": t.km_effectues(km_actuel)} for t in vehicule.trains_pneus.all()]
    rappels = [{"r": r, "statut": statut_rappel(r, km_actuel)} for r in vehicule.rappels.filter(actif=True)]
    conso = consommation(vehicule)
    from .models import TypeAchat
    return {
        "v": vehicule,
        "s": s,
        "type_achat": dict(TypeAchat.choices).get(s["type_achat"], s["type_achat"]),
        "plaque": plaque_svg(vehicule.immatriculation, vehicule.pays_immatriculation, 34),
        "postes": postes,
        "total": total,
        "camembert": camembert_svg([(p["montant"], p["couleur"]) for p in postes]),
        "conso": conso,
        "conso_elec": consommation(vehicule, "kWh") if vehicule.energie == "phev" else None,
        "entretiens": entretiens,
        "pneus": pneus,
        "documents": vehicule.documents.all(),
        "rappels": rappels,
        "vente": VenteParticulier.objects.filter(vehicule=vehicule).first(),
        "aujourdhui": date.today(),
        "km_actuel": km_actuel,
    }


def pdf(vehicule):
    from weasyprint import HTML
    html = render_to_string("particulier/pdf_recapitulatif.html", contexte(vehicule))
    return HTML(string=html).write_pdf()

from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.text import slugify
from weasyprint import HTML
from django.contrib.auth.decorators import login_required
from .forms import StatsFournisseurForm
from . import calculs
from .models import StatsFournisseur


@login_required
def stats_fournisseur_view(request):
    """
    Sans fournisseur : vue d'ensemble (classement des fournisseurs, évolution des achats).
    Avec fournisseur : tableau de bord du fournisseur (KPI, graphiques, factures).
    """
    societe = request.user.societe
    form = StatsFournisseurForm(request.GET or None, societe=societe)
    aujourd_hui = timezone.localdate()

    fournisseur = annee = mois = None
    sources = list(calculs.SOURCES)
    if form.is_valid():
        fournisseur = form.cleaned_data.get("fournisseur")
        annee = form.cleaned_data.get("annee")
        mois = int(form.cleaned_data["mois"]) if form.cleaned_data.get("mois") else None
        sources = form.cleaned_data.get("sources") or sources
    if not request.GET:
        form = StatsFournisseurForm(initial={"sources": sources}, societe=societe)

    # Toutes les années (évolution) puis la période filtrée
    toutes = calculs.lignes_achats(societe, fournisseur=fournisseur, sources=sources)
    periode = [l for l in toutes
               if (not annee or l["date"].year == annee) and (not mois or l["date"].month == mois)]
    annee_graph = annee or (max((l["date"].year for l in toutes), default=aujourd_hui.year))

    kpi = calculs.totaux(periode)
    comparaison = None
    if annee:
        precedente = [l for l in toutes
                      if l["date"].year == annee - 1 and (not mois or l["date"].month == mois)]
        t_prec = calculs.totaux(precedente)
        comparaison = {
            "annee": annee - 1, "htva": t_prec["htva"],
            "evolution": (calculs.q((kpi["htva"] - t_prec["htva"]) * 100 / t_prec["htva"])
                          if t_prec["htva"] else None),
        }

    stats_mois = calculs.par_mois(toutes, annee_graph)
    stats_mois_prec = calculs.par_mois(toutes, annee_graph - 1)
    stats_annees = calculs.par_annee(toutes)
    stats_sources = [s for s in calculs.par_source(periode) if s["source"] in sources]
    classement = calculs.par_fournisseur(periode) if fournisseur is None else []

    def f(v):
        return float(v or 0)

    graphiques = {
        "annee": annee_graph,
        "mois": {
            "labels": [str(m["nom"])[:3] + "." for m in stats_mois],
            "htva": [f(m["htva"]) for m in stats_mois],
            "htva_prec": [f(m["htva"]) for m in stats_mois_prec],
            "nb": [m["nb"] for m in stats_mois],
        },
        "annees": {
            "labels": [str(a["annee"]) for a in stats_annees],
            "htva": [f(a["htva"]) for a in stats_annees],
            "tva": [f(a["tva"]) for a in stats_annees],
        },
        "sources": [{"label": str(s["libelle"]), "htva": f(s["htva"])} for s in stats_sources if s["htva"]],
        "fournisseurs": [{"label": str(c["fournisseur"]), "htva": f(c["htva"])} for c in classement[:10]],
    }

    params = request.GET.copy()
    return render(request, "stats_fournisseurs/statistiques.html", {
        "form": form,
        "fournisseur": fournisseur,
        "annee": annee,
        "annee_graph": annee_graph,
        "mois": mois,
        "mois_nom": calculs.NOMS_MOIS[mois - 1] if mois else None,
        "kpi": kpi,
        "comparaison": comparaison,
        "stats_mois": stats_mois,
        "stats_annees": stats_annees,
        "stats_sources": stats_sources,
        "classement": classement,
        "factures": list(reversed(periode)) if fournisseur else [],
        "graphiques": graphiques,
        "query": params.urlencode(),
    })


@login_required
def stats_fournisseur_pdf_view(request):
    """
    PDF du détail des factures d'un fournisseur
    (mêmes filtres que la page statistiques : fournisseur, année, mois).
    """
    form = StatsFournisseurForm(request.GET or None, societe=request.user.societe)

    if not form.is_valid() or not form.cleaned_data.get("fournisseur"):
        return HttpResponse(status=400)

    societe = request.user.societe
    fournisseur = form.cleaned_data["fournisseur"]
    annee = form.cleaned_data.get("annee")
    mois = form.cleaned_data.get("mois")
    mois = int(mois) if mois else None

    # Sécurité : le fournisseur doit appartenir à la société de l'utilisateur
    if getattr(fournisseur, "societe_id", None) not in (None, societe.pk):
        return HttpResponse(status=404)

    stats, _ = StatsFournisseur.objects.get_or_create(
        societe=societe,
        fournisseur=fournisseur,
    )

    factures = stats.get_lignes(annee=annee, mois=mois)

    total_htva = sum((f["htva"] for f in factures), Decimal("0.00"))
    total_tva = sum((f["tva"] for f in factures), Decimal("0.00"))
    total_tvac = total_htva + total_tva

    mois_label = dict(form.fields["mois"].choices).get(mois) if mois else None

    html_string = render_to_string(
        "stats_fournisseurs/statistiques_pdf.html",
        {
            "societe": societe,
            "fournisseur": fournisseur,
            "annee": annee,
            "mois_label": mois_label,
            "factures": factures,
            "nb_factures": len(factures),
            "total_htva": StatsFournisseur._q(total_htva),
            "total_tva": StatsFournisseur._q(total_tva),
            "total_tvac": StatsFournisseur._q(total_tvac),
            "date_export": timezone.now(),
        },
        request=request,
    )

    nom_fichier = f"factures_{slugify(fournisseur.nom)}"
    if annee:
        nom_fichier += f"_{annee}"
    if mois:
        nom_fichier += f"_{mois:02d}"

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{nom_fichier}.pdf"'

    HTML(
        string=html_string,
        base_url=request.build_absolute_uri(),
    ).write_pdf(response)

    return response

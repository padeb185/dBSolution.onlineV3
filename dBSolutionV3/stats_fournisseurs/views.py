from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.text import slugify
from weasyprint import HTML
from django.contrib.auth.decorators import login_required
from .forms import StatsFournisseurForm
from .models import StatsFournisseur


@login_required
def stats_fournisseur_view(request):

    form = StatsFournisseurForm(request.GET or None)

    stats = None
    stats_mois = []
    stats_annees = []

    total_htva = Decimal("0.00")
    total_tva = Decimal("0.00")
    total_tvac = Decimal("0.00")
    nb_factures = 0

    if form.is_valid():

        fournisseur = form.cleaned_data.get("fournisseur")
        annee = form.cleaned_data.get("annee")
        mois = form.cleaned_data.get("mois")

        if mois:
            mois = int(mois)

        if fournisseur:

            stats, _ = StatsFournisseur.objects.get_or_create(
                societe=request.user.societe,
                fournisseur=fournisseur
            )

            stats_mois = stats.stats_par_mois(annee) or []
            stats_annees = stats.stats_par_annee() or []

            if mois:
                stats_mois = [r for r in stats_mois if r["mois"] == mois]

            total_htva = stats.total_achats_htva
            total_tva = stats.total_tva
            total_tvac = stats.total_tvac
            nb_factures = stats.nb_factures

    return render(request, "stats_fournisseurs/statistiques.html", {
        "form": form,
        "stats": stats,
        "stats_mois": stats_mois,
        "stats_annees": stats_annees,
        "total_htva": total_htva,
        "total_tva": total_tva,
        "total_tvac": total_tvac,
        "nb_factures": nb_factures,
    })


@login_required
def stats_fournisseur_pdf_view(request):
    """
    PDF du détail des factures d'un fournisseur
    (mêmes filtres que la page statistiques : fournisseur, année, mois).
    """
    form = StatsFournisseurForm(request.GET or None)

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

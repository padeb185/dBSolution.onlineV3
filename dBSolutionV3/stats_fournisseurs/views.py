from decimal import Decimal
from django.shortcuts import render
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
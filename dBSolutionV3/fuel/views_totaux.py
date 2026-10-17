"""Totaux énergie (carburants, recharges, AdBlue) : écran, PDF et journal comptable CSV."""
import csv
from datetime import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from adblue.models import AdBlue
from recharge.models import Electricite
from .models import Fuel
from . import totaux_energie as te


def _deduction(request):
    try:
        d = Decimal(request.GET.get("deduction") or "100")
    except Exception:
        d = Decimal("100")
    return min(max(d, Decimal("0")), Decimal("100"))


def _annees(societe):
    annees = set()
    for model in (Fuel, Electricite, AdBlue):
        annees |= {d.year for d in model.objects.filter(societe=societe).dates("date", "year")}
    annees.add(timezone.localdate().year)
    return sorted(annees, reverse=True)


def _contexte(request):
    societe = request.user.societe
    periode = te.Periode.depuis_requete(request)
    deduction = _deduction(request)
    ops = te.operations(societe, periode)
    ctx = {
        "societe": societe,
        "periode": periode,
        "deduction": deduction,
        "operations": ops,
        "familles": [(k, _(v["label"])) for k, v in te.FAMILLES.items()],
        "query": periode.querystring() + (f"&deduction={deduction}" if deduction != 100 else ""),
    }
    ctx.update(te.totaux(ops, periode, deduction))
    ctx["compta"] = te.comptabilite(ops, deduction)
    return ctx


@never_cache
@login_required
def energie_totaux(request):
    ctx = _contexte(request)
    ctx.update({
        "annees": _annees(request.user.societe),
        "mois_choix": [(i, _(te.MOIS_NOMS[i])) for i in range(1, 13)],
        "trimestres": [1, 2, 3, 4],
    })
    return render(request, "fuel/totaux/energie_totaux.html", ctx)


@login_required
def energie_totaux_pdf(request):
    from weasyprint import HTML

    ctx = _contexte(request)
    ctx["detail"] = request.GET.get("detail", "1") == "1"
    ctx["compta_detail"] = request.GET.get("journal") == "1"
    ctx["date_export"] = datetime.now()
    html = render_to_string("fuel/totaux/energie_totaux_pdf.html", ctx, request=request)
    pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="totaux_energie_{ctx["periode"].slug}.pdf"'
    return response


@login_required
def energie_journal_csv(request):
    """Journal des achats énergie (CSV ; séparateur point-virgule, virgule décimale)."""
    ctx = _contexte(request)

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="journal_energie_{ctx["periode"].slug}.csv"'
    response.write("﻿")  # BOM pour Excel

    w = csv.writer(response, delimiter=";")
    w.writerow([_("Date"), _("Journal"), _("Pièce"), _("Compte"), _("Intitulé du compte"), _("Libellé"),
                _("Pays"), _("Taux TVA"), _("Débit"), _("Crédit")])

    def fmt(x):
        return f"{x:.2f}".replace(".", ",") if x else ""

    for e in ctx["compta"]["journal"]:
        o = e["op"]
        for l in e["lignes"]:
            w.writerow([o["date"].strftime("%d/%m/%Y"), "ACH", o["piece"], l["compte"], l["intitule"],
                        l["libelle"], o["pays"], fmt(o["taux"]), fmt(l["debit"]), fmt(l["credit"])])
    return response

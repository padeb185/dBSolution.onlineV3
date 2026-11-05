"""Comptabilité : immobilisations / amortissements, stock, salaires (versements) et journal général."""
import csv
from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from .forms_immo import ImmobilisationForm, ValorisationStockForm, VersementSocialForm
from .journal import SOURCES, balance, ecritures_societe
from .models import (COMPTES_IMMOBILISATIONS, REGLES_AMORTISSEMENT_BE, CategorieImmobilisation, Immobilisation,
                     NatureImmobilisation, ValorisationStock, VersementSocial)
from .views import _autorise, _log, _refus

ZERO = Decimal("0.00")


def _annee(request, defaut=None):
    try:
        return int(request.GET.get("annee") or defaut or timezone.localdate().year)
    except ValueError:
        return timezone.localdate().year


def _immos(request):
    return Immobilisation.objects.filter(societe=request.user.societe).select_related("fournisseur", "compte_paiement")


# ==================================================================
# IMMOBILISATIONS
# ==================================================================
@never_cache
@login_required
def immobilisations_liste(request):
    if not _autorise(request.user):
        return _refus(request)

    annee = _annee(request)
    categorie = request.GET.get("categorie") or ""
    immos = list(_immos(request))
    if categorie:
        immos = [i for i in immos if i.categorie == categorie]

    lignes, par_cat = [], {}
    for i in immos:
        d = {"immo": i, "dotation": i.dotation(annee), "cumul": i.cumul_fin(annee), "vnc": i.vnc_fin(annee),
             "cedee": bool(i.date_cession and i.date_cession.year <= annee),
             "pas_encore": i.debut.year > annee}
        lignes.append(d)
        c = par_cat.setdefault(i.categorie, {"label": i.get_categorie_display(), "compte": i.compte_actif,
                                             "brut": ZERO, "dotation": ZERO, "cumul": ZERO, "vnc": ZERO, "nb": 0})
        if not d["cedee"] and not d["pas_encore"]:
            c["brut"] += i.valeur_comptable_brute
            c["cumul"] += d["cumul"]
            c["vnc"] += d["vnc"]
            c["nb"] += 1
        c["dotation"] += d["dotation"]
    totaux = {k: sum((c[k] for c in par_cat.values()), ZERO) for k in ("brut", "dotation", "cumul", "vnc")}
    return render(request, "compta/immo/immobilisations_liste.html", {
        "lignes": lignes, "par_categorie": sorted(par_cat.values(), key=lambda c: c["compte"]), "totaux": totaux,
        "annee": annee, "annees": range(timezone.localdate().year - 10, timezone.localdate().year + 6),
        "categories": CategorieImmobilisation.choices, "categorie": categorie,
    })


def _form_immo(request, immo=None):
    societe = request.user.societe
    if request.method == "POST":
        form = ImmobilisationForm(request.POST, instance=immo, societe=societe)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.societe = societe
            obj.duree_annees = form.cleaned_data["duree_annees"]
            obj.save()
            _log(request, f"Immobilisation {'modifiée' if immo else 'créée'} – {obj.libelle}")
            messages.success(request, _("L'immobilisation a été enregistrée."))
            return redirect("compta:immobilisation_detail", pk=obj.pk)
        messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        initial = {}
        cat = request.GET.get("categorie")
        nature = request.GET.get("nature")
        if not immo and nature in REGLES_AMORTISSEMENT_BE:
            regle = REGLES_AMORTISSEMENT_BE[nature]
            initial = {"nature": nature, "categorie": regle[0], "duree_annees": regle[1]}
        elif not immo and cat in COMPTES_IMMOBILISATIONS:
            initial = {"categorie": cat, "duree_annees": COMPTES_IMMOBILISATIONS[cat][2]}
        form = ImmobilisationForm(instance=immo, societe=societe, initial=initial)
    return render(request, "compta/immo/immobilisation_form.html", {
        "form": form, "immo": immo,
        "durees": {k: v[2] for k, v in COMPTES_IMMOBILISATIONS.items()},
        "regles": _regles_belges(),
        "regles_js": {str(n): {"categorie": str(r[0]), "duree": r[1], "note": str(r[2])}
                      for n, r in REGLES_AMORTISSEMENT_BE.items()},
    })


def _regles_belges():
    """Tableau des durées usuelles en Belgique, groupé par catégorie PCMN."""
    lignes = []
    for nature, (categorie, duree, note) in REGLES_AMORTISSEMENT_BE.items():
        lignes.append({
            "nature": NatureImmobilisation(nature).label,
            "categorie": CategorieImmobilisation(categorie).label,
            "compte": COMPTES_IMMOBILISATIONS[categorie][0],
            "duree": duree,
            "taux": (Decimal("100") / duree).quantize(Decimal("0.01")) if duree else None,
            "note": note,
        })
    return lignes


@never_cache
@login_required
def immobilisation_ajouter(request):
    if not _autorise(request.user):
        return _refus(request)
    return _form_immo(request)


@never_cache
@login_required
def immobilisation_modifier(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    return _form_immo(request, get_object_or_404(_immos(request), pk=pk))


@never_cache
@login_required
def immobilisation_detail(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    immo = get_object_or_404(_immos(request), pk=pk)
    return render(request, "compta/immo/immobilisation_detail.html", {
        "immo": immo, "plan": immo.plan_amortissement(), "ecritures": immo.ecritures(),
    })


@never_cache
@login_required
def immobilisation_supprimer(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    immo = get_object_or_404(_immos(request), pk=pk)
    if request.method == "POST":
        _log(request, f"Immobilisation supprimée – {immo.libelle}")
        immo.delete()
        messages.success(request, _("L'immobilisation a été supprimée."))
        return redirect("compta:immobilisations_liste")
    return render(request, "compta/immo/supprimer.html", {
        "titre": _("Supprimer l'immobilisation"), "objet": immo,
        "retour": "compta:immobilisation_detail", "retour_pk": immo.pk,
    })


# ==================================================================
# STOCK
# ==================================================================
def _valeur_pieces(societe):
    try:
        from piece.models import Piece
        return sum((p.valeur_stock for p in Piece.objects.filter(societe=societe, quantite_stock__gt=0)), ZERO)
    except Exception:
        return ZERO


@never_cache
@login_required
def stock_compta(request):
    if not _autorise(request.user):
        return _refus(request)
    societe = request.user.societe
    valeur_actuelle = _valeur_pieces(societe)
    if request.method == "POST":
        form = ValorisationStockForm(request.POST)
        if form.is_valid():
            v = form.save(commit=False)
            v.societe = societe
            v.save()
            _log(request, f"Valorisation du stock {v.date:%d/%m/%Y}")
            messages.success(request, _("La valorisation du stock a été enregistrée."))
            return redirect("compta:stock_compta")
    else:
        form = ValorisationStockForm(initial={"date": timezone.localdate(), "valeur_pieces": valeur_actuelle})
    valorisations = list(ValorisationStock.objects.filter(societe=societe))
    return render(request, "compta/immo/stock.html", {
        "form": form, "valeur_actuelle": valeur_actuelle, "valorisations": valorisations,
        "derniere": valorisations[0] if valorisations else None,
    })


@login_required
def stock_supprimer(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    v = get_object_or_404(ValorisationStock, societe=request.user.societe, pk=pk)
    if request.method == "POST":
        v.delete()
        messages.success(request, _("La valorisation du stock a été supprimée."))
        return redirect("compta:stock_compta")
    return render(request, "compta/immo/supprimer.html", {
        "titre": _("Supprimer la valorisation du stock"), "objet": v, "retour": "compta:stock_compta",
    })


# ==================================================================
# SALAIRES : paiement des nets, versements ONSS / précompte
# ==================================================================
@never_cache
@login_required
def salaires_compta(request):
    if not _autorise(request.user):
        return _refus(request)
    from utilisateurs.models import PaieUtilisateur

    societe = request.user.societe
    annee = _annee(request)
    if request.method == "POST":
        form = VersementSocialForm(request.POST, societe=societe)
        if form.is_valid():
            v = form.save(commit=False)
            v.societe = societe
            v.save()
            _log(request, f"Versement {v.get_type_display()} {v.periode}")
            messages.success(request, _("Le versement a été enregistré."))
            return redirect(f"{request.path}?annee={annee}")
    else:
        form = VersementSocialForm(societe=societe, initial={"date": timezone.localdate()})

    paies = list(PaieUtilisateur.objects.filter(utilisateur__societe=societe, annee=annee)
                 .select_related("utilisateur").order_by("mois", "utilisateur__nom"))
    versements = list(VersementSocial.objects.filter(societe=societe, date__year__in=[annee, annee + 1]))

    # Dettes salariales (année) : constituées par les paies / apurées par les paiements et versements
    E = ecritures_societe(societe, date(annee, 1, 1), date(annee, 12, 31),
                          sources=["salaire", "paiement_salaire", "versement_social"])
    comptes = {c["compte"]: c for c in balance(E)}
    from core.pays import pays_societe
    from .plans_comptables import compte_national, convertir_ecritures
    pays = pays_societe(societe)
    if pays == "DE":
        postes = (("455000", _("Salaires nets à payer")),
                  ("454000", _("Cotisations sociales à payer (Krankenkassen / Minijob-Zentrale)")),
                  ("453000", _("Lohnsteuer, Solidaritätszuschlag et Kirchensteuer à payer (Finanzamt)")))
    else:
        postes = (("455000", _("Rémunérations nettes à payer")), ("454000", _("ONSS à payer")),
                  ("454100", _("Cotisation annuelle vacances ouvriers à payer")),
                  ("459000", _("Cotisations sociales du dirigeant à payer")),
                  ("453000", _("Précompte professionnel à payer")), ("456000", _("Pécules de vacances")))
    dettes = []
    for code, intitule in postes:
        c = comptes.get(code, {"debit": ZERO, "credit": ZERO})
        dettes.append({"compte": compte_national(code, pays)[0], "intitule": intitule, "debit": c["debit"],
                       "credit": c["credit"], "solde": c["credit"] - c["debit"]})
    paiements = convertir_ecritures([e for e in E if e["source"] in ("paiement_salaire", "versement_social")], pays)

    return render(request, "compta/immo/salaires.html", {
        "form": form, "annee": annee, "annees": range(timezone.localdate().year - 5, timezone.localdate().year + 2),
        "paies": paies, "versements": versements, "dettes": dettes, "paiements": paiements,
        "total_net": sum((p.net_a_payer for p in paies), ZERO),
        "total_paye": sum((p.net_a_payer for p in paies if p.date_paiement), ZERO),
        "total_debit": sum((e["debit"] for e in paiements), ZERO),
        "total_credit": sum((e["credit"] for e in paiements), ZERO),
    })


@login_required
def versement_supprimer(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    v = get_object_or_404(VersementSocial, societe=request.user.societe, pk=pk)
    if request.method == "POST":
        v.delete()
        messages.success(request, _("Le versement a été supprimé."))
        return redirect("compta:salaires_compta")
    return render(request, "compta/immo/supprimer.html", {
        "titre": _("Supprimer le versement"), "objet": v, "retour": "compta:salaires_compta",
    })


# ==================================================================
# JOURNAL GÉNÉRAL ET BALANCE
# ==================================================================
@never_cache
@login_required
def journal_general(request):
    if not _autorise(request.user):
        return _refus(request)
    import calendar

    annee = _annee(request)
    try:
        mois = int(request.GET.get("mois") or 0)
    except ValueError:
        mois = 0
    debut = date(annee, mois or 1, 1)
    fin = date(annee, mois, calendar.monthrange(annee, mois)[1]) if mois else date(annee, 12, 31)
    choisies = [s for s in request.GET.getlist("source") if s in SOURCES] or list(SOURCES.keys())
    compte = (request.GET.get("compte") or "").strip()

    E = ecritures_societe(request.user.societe, debut, fin, choisies)
    # Comptabilisation par pays : comptes du plan national de la société (DE → SKR03, BE → PCMN)
    from core.pays import pays_societe
    from .plans_comptables import convertir_ecritures, plan_du_pays
    pays = pays_societe(request.user.societe)
    plan = plan_du_pays(pays)
    E = convertir_ecritures(E, pays)
    if compte:
        E = [e for e in E if e["compte"].startswith(compte)]
    bal = balance(E)
    total_debit = sum((e["debit"] for e in E), ZERO)
    total_credit = sum((e["credit"] for e in E), ZERO)

    if request.GET.get("export") == "csv":
        nom = f"journal_general_{annee}{'-%02d' % mois if mois else ''}.csv"
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="{nom}"'
        response.write("﻿")
        w = csv.writer(response, delimiter=";")
        entete = [_("Date"), _("Journal"), _("Pièce"), plan["code"] if plan else _("Compte"), _("Intitulé du compte"),
                  _("Libellé"), _("Débit"), _("Crédit"), _("Source")]
        if plan:
            entete.append(_("Compte interne (PCMN)"))
        w.writerow(entete)
        fmt = lambda x: f"{x:.2f}".replace(".", ",") if x else ""
        for e in E:
            ligne = [e["date"].strftime("%d/%m/%Y"), e["journal"], e["piece"], e["compte"], e["intitule"],
                     e["libelle"], fmt(e["debit"]), fmt(e["credit"]), SOURCES.get(e["source"], "")]
            if plan:
                ligne.append(e.get("compte_pcmn", ""))
            w.writerow(ligne)
        return response

    return render(request, "compta/immo/journal_general.html", {
        "ecritures": E, "balance": bal, "total_debit": total_debit, "total_credit": total_credit,
        "equilibre": abs(total_debit - total_credit) < Decimal("0.01"),
        "annee": annee, "mois": mois, "annees": range(timezone.localdate().year - 5, timezone.localdate().year + 2),
        "mois_choix": range(1, 13), "sources": SOURCES, "choisies": choisies, "compte": compte,
        "query": request.GET.urlencode(), "plan": plan,
    })

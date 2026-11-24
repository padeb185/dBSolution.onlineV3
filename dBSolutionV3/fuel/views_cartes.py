"""
Cartes carburant / recharge électrique : liste, ajout, modification, détail (transactions et relevés).
Accès : direction, comptable et superutilisateurs (informations financières).
"""
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from .cartes import CarteCarburantForm
from .models import CarteCarburant

ROLES_CARTES = {"direction", "comptable"}
ZERO = Decimal("0.00")


def _autorise(user):
    return bool(getattr(user, "is_superuser", False) or getattr(user, "role", None) in ROLES_CARTES)


def _refus(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _cartes(request):
    return (CarteCarburant.objects.filter(societe=request.user.societe)
            .select_related("fournisseur", "voiture_exemplaire", "titulaire", "compte_tresorerie"))


@never_cache
@login_required
def cartes_liste(request):
    if not _autorise(request.user):
        return _refus(request)
    from . import totaux_energie as te

    cartes = list(_cartes(request))
    ops = te.operations_entre(request.user.societe)
    aujourdhui = timezone.localdate()
    debut_mois = aujourdhui.replace(day=1)
    for c in cartes:
        les_ops = [o for o in ops if o.get("carte") and o["carte"].pk == c.pk]
        c.nb_transactions = len(les_ops)
        c.total_mois = sum((o["ttc"] for o in les_ops if o["date"] >= debut_mois), ZERO)
        releves = te.releves_carte(c, les_ops) if c.est_periodique else []
        c.a_payer = sum((r["ttc"] for r in releves if not r["paye"]), ZERO)
        c.prochain_prelevement = min((r["prelevement"] for r in releves if not r["paye"]), default=None)
    sans_carte = sum(1 for o in ops if not o.get("carte"))
    return render(request, "fuel/cartes/liste.html", {
        "cartes": cartes,
        "total_a_payer": sum((c.a_payer for c in cartes), ZERO),
        "total_mois": sum((c.total_mois for c in cartes), ZERO),
        "sans_carte": sans_carte,
    })


def _formulaire(request, carte=None):
    if not _autorise(request.user):
        return _refus(request)
    societe = request.user.societe
    form = CarteCarburantForm(request.POST or None, instance=carte, societe=societe)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.societe = societe
        obj.save()
        messages.success(request, _("Carte enregistrée."))
        return redirect("fuel:carte_detail", pk=obj.pk)
    return render(request, "fuel/cartes/form.html", {"form": form, "carte": carte})


@never_cache
@login_required
def carte_ajouter(request):
    return _formulaire(request)


@never_cache
@login_required
def carte_modifier(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    return _formulaire(request, get_object_or_404(_cartes(request), pk=pk))


@never_cache
@login_required
def carte_detail(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    from . import totaux_energie as te

    carte = get_object_or_404(_cartes(request), pk=pk)
    ops = [o for o in te.operations_entre(request.user.societe) if o.get("carte") and o["carte"].pk == carte.pk]
    ops.sort(key=lambda o: o["date"], reverse=True)
    releves = te.releves_carte(carte, ops) if carte.est_periodique else []
    aujourdhui = timezone.localdate()
    debut_mois = aujourdhui.replace(day=1)
    total_mois = sum((o["ttc"] for o in ops if o["date"] >= debut_mois), ZERO)
    jour = sum((o["ttc"] for o in ops if o["date"] == aujourdhui), ZERO)
    par_famille = {}
    for o in ops:
        f = par_famille.setdefault(o["famille_label"], {"nb": 0, "ttc": ZERO, "quantite": ZERO, "unite": o["unite"]})
        f["nb"] += 1
        f["ttc"] += o["ttc"]
        f["quantite"] += o["quantite"]
    return render(request, "fuel/cartes/detail.html", {
        "carte": carte,
        "ops": ops,
        "releves": releves,
        "par_famille": par_famille,
        "total": sum((o["ttc"] for o in ops), ZERO),
        "total_mois": total_mois,
        "total_jour": jour,
        "a_payer": sum((r["ttc"] for r in releves if not r["paye"]), ZERO),
        "depasse_mois": bool(carte.plafond_mensuel and total_mois > carte.plafond_mensuel),
        "depasse_jour": bool(carte.plafond_journalier and jour > carte.plafond_journalier),
        "ecritures": te.ecritures(ops[0]) if ops else [],
    })

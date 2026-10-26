"""Sinistres : liste, déclaration, modification, suppression (liés à une police d'assurance)."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _, gettext_noop
from django.views.decorators.cache import never_cache

from core.securite import url_sure
from utilisateurs.models import UserLog

from .forms import SinistreForm
from .models import Sinistre


def _sinistres(request):
    return (Sinistre.objects.filter(police__societe=request.user.societe)
            .select_related("police", "police__voiture_exemplaire", "police__voiture_exemplaire__voiture_marque",
                            "police__voiture_exemplaire__voiture_modele", "police__assurance"))


def _suivant(request, defaut):
    return url_sure(request.POST.get("next") or request.GET.get("next"), request) or defaut


@never_cache
@login_required
def sinistre_liste(request):
    sinistres = _sinistres(request)
    etat = request.GET.get("etat") or "ouverts"
    if etat == "ouverts":
        sinistres = sinistres.filter(cloture=False)
    elif etat == "clotures":
        sinistres = sinistres.filter(cloture=True)
    return render(request, "assurance_police/sinistre_list.html", {"sinistres": sinistres, "etat": etat})


@never_cache
@login_required
def sinistre_ajouter(request):
    initial = {}
    if request.GET.get("police"):
        initial["police"] = request.GET["police"]
    vehicule_id = request.GET.get("voiture") or None
    form = SinistreForm(request.POST or None, user=request.user, vehicule_id=vehicule_id, initial=initial)
    if request.method == "POST" and form.is_valid():
        sinistre = form.save()
        UserLog.objects.create(utilisateur=request.user, action=f"{gettext_noop('Déclaration de sinistre')} - "
                               f"{getattr(sinistre.police.voiture_exemplaire, 'immatriculation', '') or ''}")
        messages.success(request, _("Sinistre enregistré."))
        return redirect(_suivant(request, "assurance_police:sinistre_liste"))
    return render(request, "assurance_police/sinistre_form.html", {"form": form, "sinistre": None})


@never_cache
@login_required
def sinistre_modifier(request, sinistre_id):
    sinistre = get_object_or_404(_sinistres(request), id=sinistre_id)
    form = SinistreForm(request.POST or None, instance=sinistre, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Sinistre mis à jour."))
        return redirect(_suivant(request, "assurance_police:sinistre_liste"))
    return render(request, "assurance_police/sinistre_form.html", {"form": form, "sinistre": sinistre})


@never_cache
@login_required
def sinistre_supprimer(request, sinistre_id):
    sinistre = get_object_or_404(_sinistres(request), id=sinistre_id)
    if request.method == "POST":
        sinistre.delete()  # les carrosseries externes liées gardent leurs données (lien remis à vide)
        messages.success(request, _("Sinistre supprimé."))
        return redirect("assurance_police:sinistre_liste")
    return render(request, "assurance_police/sinistre_confirm_delete.html", {"sinistre": sinistre})

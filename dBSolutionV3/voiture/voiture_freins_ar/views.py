from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from .forms import VoitureFreinsARForm
from ..voiture_modele.models import VoitureModele
from ..voiture_freins_ar.models import VoitureFreinsAR
from societe.models import Societe
from django.utils.translation import gettext_lazy as _



@login_required
def ajouter_freins_ar(request, modele_id):
    tenant = request.user.societe

    modele = get_object_or_404(
        VoitureModele,
        id=modele_id,
    )

    if request.method == "POST":
        post_data = request.POST.copy()

        champs_float = [
            "taille_disque_ar",
            "epaisseur_disque_ar",
            "epaisseur_min_disque_ar",
            "plaquettes_ar",
        ]

        for champ in champs_float:
            valeur = post_data.get(champ)

            if valeur:
                post_data[champ] = valeur.replace(",", ".")

        form = VoitureFreinsARForm(
            post_data,
            request.FILES or None,
        )

        if form.is_valid():
            freins_ar = form.save(commit=False)
            freins_ar.societe = tenant
            freins_ar.save()
            form.save_m2m()

            messages.success(
                request,
                _("Freins arrière ajoutés avec succès !"),
            )

            return redirect(
                "voiture_freins_ar:freins_ar_list",
            )

        messages.error(
            request,
            _("Veuillez corriger les erreurs ci-dessous."),
        )

    else:
        form = VoitureFreinsARForm()

    return render(
        request,
        "voiture_freins_ar/ajouter_freins_ar_simple.html",
        {
            "form": form,
            "modele": modele,
        },
    )


@login_required
def ajouter_freins_ar_simple(request):
    tenant = request.user.societe

    if request.method == "POST":
        post_data = request.POST.copy()

        champs_float = [
            "taille_disque_ar",
            "epaisseur_disque_ar",
            "epaisseur_min_disque_ar",
            "plaquettes_ar",
        ]

        for champ in champs_float:
            valeur = post_data.get(champ)

            if valeur:
                post_data[champ] = valeur.replace(",", ".")

        form = VoitureFreinsARForm(
            post_data,
            request.FILES or None,
        )

        if form.is_valid():
            obj = form.save(commit=False)
            obj.societe = tenant
            obj.save()
            form.save_m2m()

            messages.success(
                request,
                _("Freins arrière ajoutés avec succès !"),
            )

            return redirect(
                "voiture_freins_ar:freins_ar_list",
            )

        messages.error(
            request,
            _("Veuillez corriger les erreurs du formulaire."),
        )

    else:
        form = VoitureFreinsARForm()

    return render(
        request,
        "voiture_freins_ar/ajouter_freins_ar_simple.html",
        {
            "form": form,
        },
    )


@never_cache
@login_required
def freins_ar_detail_view(request, frein_ar_id):
    frein = get_object_or_404(
        VoitureFreinsAR,
        id=frein_ar_id,
    )

    return render(
        request,
        "voiture_freins_ar/freins_ar_detail.html",
        {
            "frein": frein,
        },
    )


@never_cache
@login_required
def liste_freins_ar(request, societe_id=None):
    societe = request.user.societe

    if societe_id:
        societe = get_object_or_404(
            Societe,
            id=societe_id,
        )

    freins_ar = VoitureFreinsAR.objects.filter(
        societe=societe,
    )

    return render(
        request,
        "voiture_freins_ar/freins_ar_list.html",
        {
            "freins_ar": freins_ar,
        },
    )
    return render(request, "voiture_freins_ar/freins_ar_list.html", {
        "freins_ar": freins_ar
    })

@login_required
def modifier_freins_ar_view(request, frein_ar_id):
    tenant = request.user.societe


    freins_ar = get_object_or_404(VoitureFreinsAR, id=frein_ar_id)

    if request.method == "POST":
        form_frein = VoitureFreinsARForm(request.POST, instance=freins_ar)
        if form_frein.is_valid():
            form_frein.save()
            messages.success(request, _("Freins arrière mis à jour avec succès."))
            return redirect("voiture_freins_ar:freins_ar_detail", frein_ar_id=freins_ar.id)

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form_frein = VoitureFreinsARForm(instance=freins_ar)

    return render(
        request,
        "voiture_freins_ar/modifier_freins_ar.html",
        {
            "form": form_frein,
            "frein": freins_ar,
        }
    )
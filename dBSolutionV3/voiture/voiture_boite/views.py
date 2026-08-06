from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from voiture.voiture_boite.forms import VoitureBoiteForm
from voiture.voiture_boite.models import VoitureBoite
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render





@login_required
def liste_boite_view(request):
    boites = (
        VoitureBoite.objects
        .all()
        .order_by("fabricant", "nom_du_type")
    )

    return render(
        request,
        "voiture_boite/list.html",
        {
            "boites": boites,
        },
    )


@login_required
def ajouter_boite_view(request):
    tenant = request.user.societe

    if request.method == "POST":
        form = VoitureBoiteForm(
            request.POST,
            request.FILES or None,
        )

        if form.is_valid():
            boite = form.save(commit=False)
            boite.societe = tenant
            boite.save()
            form.save_m2m()

            messages.success(
                request,
                _("Boîte de vitesse ajoutée avec succès."),
            )

            return redirect("voiture_boite:list")

        messages.error(
            request,
            _("Le formulaire contient des erreurs."),
        )

    else:
        form = VoitureBoiteForm()

    return render(
        request,
        "voiture_boite/ajouter_boite.html",
        {
            "form": form,
        },
    )

@login_required
def boite_detail_view(request, boite_id):
    boite = get_object_or_404(
        VoitureBoite,
        id=boite_id,
    )

    return render(
        request,
        "voiture_boite/boite_detail.html",
        {
            "boite": boite,
        },
    )


@login_required
def modifier_boite_view(request, boite_id):
    boite_instance = get_object_or_404(
        VoitureBoite,
        id=boite_id,
    )

    if request.method == "POST":
        form = VoitureBoiteForm(
            request.POST,
            request.FILES or None,
            instance=boite_instance,
        )

        if form.is_valid():
            boite = form.save()

            messages.success(
                request,
                _("Boîte de vitesse mise à jour avec succès."),
            )

            return redirect(
                "voiture_boite:boite_detail",
                boite_id=boite.id,
            )

        messages.error(
            request,
            _("Le formulaire contient des erreurs."),
        )

    else:
        form = VoitureBoiteForm(instance=boite_instance)

    return render(
        request,
        "voiture_boite/modifier_boite.html",
        {
            "form": form,
            "boite": boite_instance,
        },
    )
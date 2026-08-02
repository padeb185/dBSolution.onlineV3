from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from voiture.voiture_embrayage.forms import VoitureEmbrayageForm
from voiture.voiture_embrayage.models import VoitureEmbrayage
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext as _




@never_cache
@login_required
def liste_embrayage(request):
    embrayages = VoitureEmbrayage.objects.all()
    return render(request, "voiture_embrayage/list.html",
                  {
                      "embrayages": embrayages
                  })




@login_required
def ajouter_embrayage_view(request):

    if request.method == "POST":
        form = VoitureEmbrayageForm(
            request.POST,
            request.FILES or None,
        )

        if form.is_valid():
            embrayage = form.save(commit=False)

            embrayage.save()
            form.save_m2m()

            messages.success(request, _("Embrayage ajouté avec succès !"))
            return redirect("voiture_embrayage:list")

        messages.error(request, _("Veuillez corriger les erreurs du formulaire."))

    else:
        form = VoitureEmbrayageForm()

    return render(
        request,
        "voiture_embrayage/ajouter_embrayage.html",
        {
            "form": form,
        },
    )



@login_required
def lier_embrayage(request, embrayage_id):
    embrayage = get_object_or_404(VoitureEmbrayage, id=embrayage_id)
    exemplaires = VoitureExemplaire.objects.all().order_by("id")

    if request.method == "POST":
        cible_id = request.POST.get("cible_id")
        if cible_id:
            embrayage.voiture_exemplaire_id = cible_id
            embrayage.voiture_modele = None  # on supprime tout lien précédent avec un modèle
            embrayage.save()

            messages.success(
                request,
                _("L'embrayage a été lié au véhicule avec succès.")
            )

            return redirect("voiture_embrayage:list")

    return render(
        request,
        "voiture_embrayage/lier_embrayage.html",
        {
            "embrayage": embrayage,
            "exemplaires": exemplaires,
        },
    )




@login_required
def embrayage_detail_view(request, embrayage_id):
    embrayage = get_object_or_404(
        VoitureEmbrayage,
        id=embrayage_id,
    )

    return render(
        request,
        "voiture_embrayage/embrayage_detail.html",
        {
            "embrayage": embrayage,
        },
    )




@login_required
def modifier_embrayage_view(request, embrayage_id):
    embrayage = get_object_or_404(
        VoitureEmbrayage,
        id=embrayage_id,
    )

    if request.method == "POST":
        form = VoitureEmbrayageForm(
            request.POST,
            request.FILES or None,
            instance=embrayage,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                _("Embrayage mis à jour avec succès."),
            )

            return redirect(
                "voiture_embrayage:embrayage_detail",
                embrayage_id=embrayage.id,
            )

        messages.error(
            request,
            _("Le formulaire contient des erreurs."),
        )

    else:
        form = VoitureEmbrayageForm(instance=embrayage)

    return render(
        request,
        "voiture_embrayage/modifier_embrayage.html",
        {
            "form": form,
            "embrayage": embrayage,
        },
    )





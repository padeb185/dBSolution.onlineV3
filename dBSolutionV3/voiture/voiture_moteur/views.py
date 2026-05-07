from django_tenants.utils import tenant_context
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from .forms import MoteurVoitureForm
from .models import MoteurVoiture, TypeCarburant, TypeMoteur, TypeDistribution
from django.contrib import messages
from django.views.decorators.cache import never_cache



@login_required()
def moteur_detail_view(request, moteur_id):
    moteur = get_object_or_404(MoteurVoiture, id=moteur_id)
    return render(request, 'voiture_moteur/moteur_detail.html', {
        'moteur': moteur,
    })




@never_cache
@login_required
def liste_moteur(request):
    tenant = request.user.societe  # récupérer le tenant
    with tenant_context(tenant):
        moteurs = MoteurVoiture.objects.all()  # tous les moteurs du tenant
        context = {"moteurs": moteurs}
        return render(request, "voiture_moteur/list.html", context)




@login_required
def ajouter_moteur_view(request):

    if request.method == "POST":
        form = MoteurVoitureForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Moteur ajouté avec succès !")
            return redirect("voiture_moteur:list")

    else:
        form = MoteurVoitureForm()

    context = {
        "form": form,
        "TypeMoteur": TypeMoteur,
        "TypeCarburant": TypeCarburant,
        "TypeDistribution": TypeDistribution,
    }

    return render(request, "voiture_moteur/ajouter_moteur.html", context)

@login_required
def modifier_moteur_view(request, moteur_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        moteur = get_object_or_404(
            MoteurVoiture.objects.select_related(),
            id=moteur_id
        )

        if request.method == "POST":
            form = MoteurVoitureForm(request.POST, instance=moteur)
            if form.is_valid():
                form.save()
                messages.success(request, _("Moteur mis à jour avec succès."))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
        else:
            form = MoteurVoitureForm(instance=moteur)

    return render(
        request,
        "voiture_moteur/modifier_moteur.html",
        {
            "form": form,
            "moteur": moteur
        }
    )



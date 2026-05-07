from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django_tenants.utils import tenant_context
from voiture.voiture_boite.forms import VoitureBoiteForm
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_boite.models import VoitureBoite
from voiture.voiture_boite.models import TypeBoite
from django.utils.translation import gettext as _


@login_required
def liste_boite_view(request):

    tenant = request.user.societe
    with tenant_context(tenant):

        boites = VoitureBoite.objects.all()
        context = {"boites": boites}

    return render(request, "voiture_boite/list.html", context)




@login_required
def ajouter_boite_view(request):
    tenant = request.user.societe

    with tenant_context(tenant):

        if request.method == "POST":
            form = VoitureBoiteForm(request.POST)

            if form.is_valid():
                boite = form.save(commit=False)
                boite.societe = tenant
                boite.save()
                form.save_m2m()

                messages.success(
                    request,
                    "Boite de vitesse ajoutée avec succès"
                )

                return redirect("voiture_boite:ajouter_boite")

        else:
            form = VoitureBoiteForm()

    return render(request, "voiture_boite/ajouter_boite.html", {
        "form": form,
    })




@login_required
def boite_detail_view(request, boite_id):

    tenant = request.user.societe
    with tenant_context(tenant):

        boite = get_object_or_404(VoitureBoite, id=boite_id)

    return render(request, "voiture_boite/boite_detail.html", {"boite": boite})




@login_required
def modifier_boite_view(request, boite_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        boite_instance = get_object_or_404(
            VoitureBoite.objects.select_related(),
            id=boite_id
        )

        if request.method == "POST":
            form = VoitureBoiteForm(request.POST, instance=boite_instance)
            if form.is_valid():
                form.save()
                messages.success(request, _("Boîte de vitesse mise à jour avec succès."))
                # Redirection vers la page de détail après sauvegarde
                return redirect('voiture_boite:boite_detail', boite_id=boite_instance.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
        else:
            form = VoitureBoiteForm(instance=boite_instance)

    return render(
        request,
        "voiture_boite/modifier_boite.html",
        {
            "form": form,          # on passe le formulaire au template
            "boite": boite_instance # l'objet boîte pour infos complémentaires si nécessaire
        }
    )



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
    """
    Affiche tous les exemplaires de véhicules avec recherche sur marque et immatriculation
    """
    tenant = request.user.societe
    with tenant_context(tenant):
        boites = VoitureBoite.objects.all()
        context = {"boites": boites}
    return render(request, "voiture_boite/list.html", context)




@login_required
def ajouter_boite_view(request):
    if request.method == "POST":
        VoitureBoite.objects.create(
            fabricant=request.POST.get("fabricant"),
            nom_du_type=request.POST.get("nom_du_type"),
            type_de_boite=request.POST.get("type_de_boite"),
            nombre_rapport=request.POST.get("nombre_rapport") or 5,
            qualite_huile=request.POST.get("qualite_huile"),
            quantite_huile_l=request.POST.get("quantite_huile_l"),
        )
        messages.success(request, "Boite de vitesse ajoutée avec succès")

        return redirect("voiture_boite:ajouter_boite")

    # Passer TypeBoite au template pour la liste déroulante
    context = {
        "TypeBoite": TypeBoite,
    }

    return render(request, "voiture_boite/ajouter_boite.html", context)






@login_required
def boite_detail_view(request, boite_id):
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



from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context
from voiture.voiture_embrayage.forms import VoitureEmbrayageForm
from voiture.voiture_embrayage.models import VoitureEmbrayage
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_embrayage.models import TypeEmbrayage
from voiture.voiture_embrayage.models import TypeVolantMoteur
from voiture.voiture_embrayage.models import TypePlateauPression
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext as _
from voiture.voiture_embrayage.models import TypeButeeDEmbrayage



@never_cache
@login_required
def liste_embrayage(request):

    tenant = request.user.societe
    with tenant_context(tenant):
        embrayages = VoitureEmbrayage.objects.all()
    return render(request, "voiture_embrayage/list.html",
                  {
                      "embrayages": embrayages
                  })




@login_required
def ajouter_embrayage_view(request):
    tenant = request.user.societe

    with tenant_context(tenant):

        if request.method == "POST":
            form = VoitureEmbrayageForm(request.POST)

            if form.is_valid():
                embrayage = form.save(commit=False)
                embrayage.societe = tenant
                embrayage.save()

                messages.success(request, _("Embrayage ajouté avec succès !"))
                return redirect("voiture_embrayage:list")

            else:
                messages.error(request, _("Veuillez corriger les erreurs du formulaire."))

        else:
            form = VoitureEmbrayageForm()

        context = {
            "form": form,
        }

    return render(request, "voiture_embrayage/ajouter_embrayage.html", context)



@login_required
def lier_embrayage(request, embrayage_id):
    tenant = request.user.societe  # ton tenant
    with tenant_context(tenant):
        embrayage = get_object_or_404(VoitureEmbrayage, id=embrayage_id)
        exemplaires = VoitureExemplaire.objects.all().order_by("id")

        if request.method == "POST":
            cible_id = request.POST.get("cible_id")
            if cible_id:
                embrayage.voiture_exemplaire_id = cible_id
                embrayage.voiture_modele = None  # on supprime tout lien précédent avec un modèle
                embrayage.save()
                return redirect("voiture_embrayage:list")  # ou vers la page détail

    return render(request, "voiture_embrayage/lier_embrayage.html", {
        "embrayage": embrayage,
        "exemplaires": exemplaires
    })






@login_required()
def embrayage_detail_view(request, embrayage_id):
    tenant = request.user.societe
    with tenant_context(tenant):

        embrayage = get_object_or_404(VoitureEmbrayage, id=embrayage_id)

    return render(request, 'voiture_embrayage/embrayage_detail.html', {
        'embrayage': embrayage,
    })





@login_required
def modifier_embrayage_view(request, embrayage_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        embrayage_instance = get_object_or_404(
            VoitureEmbrayage.objects.select_related(),
            id=embrayage_id
        )

        if request.method == "POST":
            form = VoitureEmbrayageForm(request.POST, instance=embrayage_instance)
            if form.is_valid():
                form.save()
                messages.success(request, _("Embrayage mis à jour avec succès."))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
        else:
            form = VoitureEmbrayageForm(instance=embrayage_instance)

    return render(
        request,
        "voiture_embrayage/modifier_embrayage.html",
        {
            "form": form,
            "embrayage": embrayage_instance
        }
    )






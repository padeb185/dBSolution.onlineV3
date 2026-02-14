# assurance/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from adresse.models import Adresse
from django.utils.translation import gettext as _
from assurance.models import Assurance

from dBSolutionV3.assurance.form import AssuranceForm


@method_decorator([login_required, never_cache], name='dispatch')
class AssuranceListView(ListView):
    model = Assurance
    template_name = "assurance/assurance_list.html"
    context_object_name = "assurances"
    paginate_by = 20
    ordering = ["nom_compagnie"]







@login_required
def assurance_detail(request, assurance_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        assurance = get_object_or_404(Assurance, id=assurance_id)
        adresse = assurance.adresse

    return render(
        request,
        "assurance/assurance_detail.html",
        {
            "assurance": assurance,
            "adresse": adresse,
        },
    )




@login_required
def ajouter_assurance_all(request):
    assurance = Assurance()
    assurance.adresse = Adresse()

    if request.method == "POST":
        nom_societe = request.POST.get("assurance")


        if not nom_societe:
            messages.error(request, _("Le nom de la assurance est obligatoire."))
        else:
            adresse = Adresse.objects.create(
                rue=request.POST.get("rue"),
                numero=request.POST.get("numero"),
                code_postal=request.POST.get("code_postal"),
                ville=request.POST.get("ville"),
                pays=request.POST.get("pays"),
                code_pays=request.POST.get("code_pays")
            )
            assurance = Assurance.objects.create(
                nom_compagnie=request.POST.get("nom_compagnie"),
                nom_courtier=request.POST.get("nom_courtier"),
                prenom_courtier=request.POST.get("prenom_courtier"),
                peppol_id=request.POST.get("peppol_id"),
                email=request.POST.get("email"),
                telephone=request.POST.get("telephone"),

                adresse=adresse
            )
            messages.success(request, _(f"Compagnie d'assurance: '{assurance.nom_societe}' ajouté avec succès !"))
            return redirect("assurance:assurance_list")

    # S'assurer que fournisseur.adresse existe
    if not hasattr(assurance, "adresse") or assurance.adresse is None:
        assurance.adresse = Adresse()

    return render(request, "assurance/assurance_form.html", {"assurance":assurance})




@login_required
def modifier_assurance(request, assurance_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        assurance = get_object_or_404(Assurance, id=assurance_id)

        if request.method == "POST":
            form = AssuranceForm(request.POST, instance=assurance)
            if form.is_valid():
                form.save()
                messages.success(request, "assurance mise à jour avec succès.")
                return redirect(
                    'assurance:modifier_assurance',
                    assurance_id=assurance.id
                )
        else:
            form = AssuranceForm(instance=assurance)

    return render(
        request,
        "assurance/modifier_assurance.html",
        {
            "form": form,
            "assurance": assurance,
        }
    )





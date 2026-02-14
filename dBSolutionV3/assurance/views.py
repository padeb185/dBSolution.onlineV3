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
from assurance.forms import AssuranceForm


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
def ajouter_assurance_all(request, assurance_id=None):
    tenant = request.user.societe

    with tenant_context(tenant):
        if assurance_id:
            # modification
            assurance = get_object_or_404(Assurance, id=assurance_id)
        else:
            # création
            assurance = Assurance()

    if request.method == "POST":
        form = AssuranceForm(request.POST, instance=assurance)
        if form.is_valid():
            form.save()
            messages.success(request, "Compagnie d'assurance enregistrée avec succès.")

        else:
            messages.error(request, "Le formulaire contient des erreurs. Vérifiez les champs obligatoires.")
    else:
        form = AssuranceForm(instance=assurance)

    return render(request, "assurance/assurance_form.html", {"form": form})



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






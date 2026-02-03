from intervention.models import Intervention
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django_tenants.utils import tenant_context



# Create your views here.

@login_required()
class InterventionListView(ListView):
    model = Intervention
    template_name = "intervention/intervention_list.html"
    context_object_name = "interventions"
    paginate_by = 20
    ordering = ["nom_societe"]



@login_required()
def intervention_create(request):
    if request.method == "POST":
        form = InterventionForm(request.POST)
        if form.is_valid():
            intervention = form.save(commit=False)
            # Calcul automatique du total
            intervention.montant_total = intervention.total_prix
            intervention.save()
            return redirect(reverse("intervention_list"))  # à adapter selon ta vue liste
    else:
        form = InterventionForm()

    return render(request, "intervention/intervention_form.html", {"form": form})






@login_required
def ajouter_intervention_all(request):
    if request.method == "POST":
        form = InterventionForm(request.POST)
        if form.is_valid():
            intervention = form.save(commit=False)
            # Calcul automatique du total
            intervention.montant_total = intervention.total_prix
            intervention.save()
            return redirect(reverse("intervention_list"))  # Redirige vers la liste
    else:
        form = InterventionForm()

    return render(request, "intervention/intervention_form.html", {"form": form})


class InterventionForm:
    pass


@login_required
def modifier_intervention(request, intervention_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        intervention = get_object_or_404(Intervention, id=intervention_id)

        if request.method == "POST":
            form =InterventionForm(request.POST, instance=intervention)
            if form.is_valid():
                form.save()
                messages.success(request, "Intervention mise à jour avec succès.")
                return redirect(
                    'intervention:modifier_intervention',
                    intervention_id=intervention.id
                )
        else:
            form = InterventionForm(instance=intervention)

    return render(
        request,
        "intervention/modifier_intervention.html",
        {
            "form": form,
            "intervention": intervention,
        }
    )

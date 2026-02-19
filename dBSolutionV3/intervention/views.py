from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import never_cache
from .forms import InterventionForm
from .models import Intervention
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from carrosserie.models import Carrosserie
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Intervention



class InterventionListView(LoginRequiredMixin, ListView):
    model = Intervention
    template_name = "intervention/intervention_list.html"
    context_object_name = "interventions"
    paginate_by = 20




@login_required
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
    carrosseries = Carrosserie.objects.all()
    voitures = VoitureExemplaire.objects.all().values_list('immatriculation', flat=True)
    pieces = ["pare_chocs", "bouclier_av", "pare_brise"]  # Liste des éléments à réparer

    # Préparer un dictionnaire pour stocker les valeurs des pièces
    pieces_values = {}
    for piece in pieces:
        pieces_values[piece] = {"checked": False, "prix": "", "quantite": ""}

    if request.method == "POST":
        form = InterventionForm(request.POST)
        if form.is_valid():
            intervention = form.save(commit=False)

            # Récupérer la voiture via UUID
            voiture_uuid = request.POST.get("voiture_immatriculation")
            if voiture_uuid:
                try:
                    intervention.voiture_immatriculation = VoitureExemplaire.objects.get(id=UUID(voiture_uuid))
                except VoitureExemplaire.DoesNotExist:
                    form.add_error("voiture_immatriculation", "Voiture non trouvée.")

            # Récupérer les informations des pièces depuis POST
            for piece in pieces:
                checked = request.POST.get(f"{piece}_checked") == "on"
                prix = request.POST.get(f"{piece}_prix", "")
                quantite = request.POST.get(f"{piece}_quantite", "")
                pieces_values[piece] = {
                    "checked": checked,
                    "prix": prix,
                    "quantite": quantite,
                }

            # Calcul automatique du total
            intervention.montant_total = intervention.total_prix  # Assure que total_prix prend en compte les pièces
            intervention.save()
            return redirect(reverse("intervention:intervention_list"))
        else:
            print(form.errors)
            # Si le formulaire est invalide, on conserve les valeurs des pièces pour réaffichage
            for piece in pieces:
                checked = request.POST.get(f"{piece}_checked") == "on"
                prix = request.POST.get(f"{piece}_prix", "")
                quantite = request.POST.get(f"{piece}_quantite", "")
                pieces_values[piece] = {
                    "checked": checked,
                    "prix": prix,
                    "quantite": quantite,
                }
    else:
        form = InterventionForm()

    return render(request, "intervention/intervention_form.html", {
        "form": form,
        "carrosseries": carrosseries,
        "voitures": voitures,
        "pieces": pieces,
        "pieces_values": pieces_values,
    })





@login_required
def modifier_intervention(request, intervention_id):
    tenant = request.user.societe  # ou autre attribut qui identifie le tenant

    with tenant_context(tenant):
        intervention = get_object_or_404(Intervention, id=intervention_id)

        if request.method == "POST":
            form = InterventionForm(request.POST, instance=intervention)
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



@login_required
def intervention_detail(request, intervention_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        intervention = get_object_or_404(Intervention, id=intervention_id)
        adresse = intervention.carrosserie.adresse

    return render(
        request,
        "intervention/intervention_detail.html",
        {
            "intervention": intervention,
            "adresse": adresse,
        },
    )

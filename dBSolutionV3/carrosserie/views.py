# carrosserie/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from .forms import CarrosserieForm
from .models import Carrosserie
from adresse.models import Adresse
from django.utils.translation import gettext as _



@method_decorator([login_required, never_cache], name='dispatch')
class CarrosserieListView(ListView):
    model = Carrosserie
    template_name = "carrosserie/carrosserie_list.html"
    context_object_name = "carrosseries"
    paginate_by = 20
    ordering = ["nom_societe"]







@login_required
def carrosserie_detail(request, carrosserie_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        carrosserie = get_object_or_404(Carrosserie, id=carrosserie_id)
        adresse = carrosserie.adresse

    return render(
        request,
        "carrosserie/carrosserie_detail.html",
        {
            "carrosserie": carrosserie,
            "adresse": adresse,
        },
    )



@login_required
def ajouter_assurance_all(request):
    tenant = request.user.societe  # si tu utilises tenant
    carrosserie = Carrosserie()  # objet vide pour formulaire

    if request.method == "POST":
        form_carrosserie = CarrosserieForm(request.POST)

        # Créer ou récupérer une adresse
        adresse_data = {
            "rue": request.POST.get("rue"),
            "numero": request.POST.get("numero"),
            "code_postal": request.POST.get("code_postal"),
            "ville": request.POST.get("ville"),
            "pays": request.POST.get("pays"),
            "code_pays": request.POST.get("code_pays"),
            "societe": tenant
        }

        # Si l'un des champs obligatoires est vide, on renvoie une erreur
        if not adresse_data["rue"] or not adresse_data["numero"] or not adresse_data["code_postal"] or not adresse_data["ville"]:
            messages.error(request, "Les champs d'adresse sont obligatoires.")
        elif form_carrosserie.is_valid():
            # Créer l'adresse en base
            adresse = Adresse.objects.create(**adresse_data)

            # Créer la carrosserie et l'associer à l'adresse
            carrosserie = form_carrosserie.save(commit=False)
            carrosserie.adresse = adresse
            carrosserie.save()

            messages.success(request, f"carrosserie '{carrosserie.nom_compagnie}' créée avec succès !")

        else:
            messages.error(request, "Le formulaire contient des erreurs.")

    else:
        form_carrosserie = CarrosserieForm()

    return render(request, "carrosserie/carrosserie_form.html", {
        "form": form_carrosserie
    })




@login_required
def modifier_carrosserie(request, carrosserie_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        carrosserie = get_object_or_404(Carrosserie, id=carrosserie_id)

        if request.method == "POST":
            form = CarrosserieForm(request.POST, instance=carrosserie)
            if form.is_valid():
                form.save()
                messages.success(request, "Carrosserie mise à jour avec succès.")
                return redirect(
                    'carrosserie:modifier_carrosserie',
                    carrosserie_id=carrosserie.id
                )
        else:
            form = CarrosserieForm(instance=carrosserie)

    return render(
        request,
        "carrosserie/modifier_carrosserie.html",
        {
            "form": form,
            "carrosserie": carrosserie,
        }
    )





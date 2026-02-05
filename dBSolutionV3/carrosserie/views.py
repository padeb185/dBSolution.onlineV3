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
def ajouter_carrosserie_all(request):
    carrosserie = Carrosserie()
    carrosserie.adresse = Adresse()

    if request.method == "POST":
        nom_societe = request.POST.get("carrosserie")


        if not nom_societe:
            messages.error(request, "Le nom de la carrosserie est obligatoire.")
        else:
            adresse = Adresse.objects.create(
                rue=request.POST.get("rue"),
                numero=request.POST.get("numero"),
                code_postal=request.POST.get("code_postal"),
                ville=request.POST.get("ville"),
                pays=request.POST.get("pays"),
                code_pays=request.POST.get("code_pays")
            )
            carrosserie = Carrosserie.objects.create(
                nom_societe=nom_societe,
                numero_tva=request.POST.get("numero_tva"),
                peppol_id=request.POST.get("peppol_id"),
                email=request.POST.get("email"),
                telephone=request.POST.get("telephone"),
                responsable_prenom=request.POST.get("responsable_prenom"),
                responsable_nom=request.POST.get("responsable_nom"),
                adresse=adresse
            )
            messages.success(request, f"Carrosserie '{carrosserie.nom_societe}' ajouté avec succès !")
            return redirect("carrosserie:carrosserie_list")

    # S'assurer que fournisseur.adresse existe
    if not hasattr(carrosserie, "adresse") or carrosserie.adresse is None:
        carrosserie.adresse = Adresse()

    return render(request, "carrosserie/carrosserie_form.html", {"carrosserie":carrosserie})




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





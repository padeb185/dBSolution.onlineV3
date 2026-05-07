# carrosserie/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context, schema_context
from .forms import CarrosserieForm
from .models import Carrosserie
from adresse.models import Adresse
from django.utils.translation import gettext as _
from adresse.forms import AdresseForm
from assurance.forms import AssuranceForm
from assurance.models import Assurance



@method_decorator([login_required, never_cache], name='dispatch')
class CarrosserieListView(ListView):
    model = Carrosserie
    template_name = "carrosserie/carrosserie_list.html"
    context_object_name = "carrosseries"
    paginate_by = 100
    ordering = ["nom_societe"]

    def get_queryset(self):
        societe = self.request.user.societe
        with tenant_context(societe):
            # On récupère uniquement les carrosseries du tenant courant
            return Carrosserie.objects.all().order_by("nom_societe")


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
    tenant = request.user.societe

    with tenant_context(tenant):

        if request.method == "POST":

            form_carrosserie = CarrosserieForm(request.POST)
            form_adresse = AdresseForm(request.POST)

            if form_carrosserie.is_valid() and form_adresse.is_valid():

                # 1. créer adresse
                adresse = form_adresse.save(commit=False)
                adresse.societe = tenant
                adresse.save()

                # 2. créer carrosserie
                carrosserie = form_carrosserie.save(commit=False)
                carrosserie.societe = tenant
                carrosserie.adresse = adresse
                carrosserie.save()

                messages.success(
                    request,
                    _(f"Carrosserie '{carrosserie.nom_societe}' créée avec succès !")
                )

                return redirect("carrosserie:list")

        else:
            form_carrosserie = CarrosserieForm()
            form_adresse = AdresseForm()

    return render(request, "carrosserie/carrosserie_form.html", {
        "form": form_carrosserie,
        "form_adresse": form_adresse,
    })




@login_required
def modifier_carrosserie(request, carrosserie_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupérer l'assureur et son adresse liée
        carrosserie = get_object_or_404(
            Carrosserie.objects.select_related("adresse"),
            id=carrosserie_id
        )
        adresse = carrosserie.adresse

        if request.method == "POST":
            # Formulaires pour Carrosserie et Adresse
            form_carrosserie = CarrosserieForm(request.POST, instance=carrosserie)
            form_adresse = AdresseForm(request.POST, instance=adresse)

            if form_carrosserie.is_valid() and form_adresse.is_valid():
                # Sauvegarde adresse puis mise à jour de l'carrosserie
                adresse = form_adresse.save()
                carrosserie = form_carrosserie.save(commit=False)
                carrosserie.adresse = adresse
                carrosserie.save()

                messages.success(request, _("Carrosserie et adresse mises à jour avec succès."))
                return redirect(
                    "carrosserie:modifier_carrosserie",
                    carrosserie_id=carrosserie.id
                )
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
        else:
            # Pré-remplissage des formulaires
            form_carrosserie = CarrosserieForm(instance=carrosserie)
            form_adresse = AdresseForm(instance=adresse)

    return render(
        request,
        "carrosserie/modifier_carrosserie.html",
        {
            "form": form_carrosserie,
            "form_adresse": form_adresse,
            "carrosserie": carrosserie,
            "adresse": adresse,
        }
    )



@never_cache
@login_required
def dashboard_carrosserie_view(request):
    user = request.user
    societe = user.societe
    context = {}

    # --- Sécurité : récupère le tenant (la société de l'utilisateur) ---
    societe = request.user.societe
    schema_name = societe.schema_name  # pour django-tenants


    # --- Stats initialisées à zéro ---

    total_carrosserie = 0


    carrosseries = []

    if schema_name:
        with schema_context(schema_name):

            carrosseries = Carrosserie.objects.filter(societe=societe)



            # Totaux

            total_carrosserie = carrosseries.count()




    else:
        modeles = []

    context.update({
        'user': user,
        'societe': societe,

        'total_carrosserie': total_carrosserie,



        'carrosserie': carrosseries,


    })


    return render(request, "carrosserie/dashboard_carrosserie.html", context)


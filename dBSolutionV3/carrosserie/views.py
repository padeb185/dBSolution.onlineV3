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
from intervention.models import Intervention


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
    tenant = request.user.societe  # Société liée à l'utilisateur

    # Pré-remplissage en cas d'erreur
    adresse_data = {}

    if request.method == "POST":
        form_carrosserie = CarrosserieForm(request.POST)

        # Récupération des données adresse
        adresse_data = {
            "rue": request.POST.get("rue", "").strip(),
            "numero": request.POST.get("numero", "").strip(),
            "code_postal": request.POST.get("code_postal", "").strip(),
            "ville": request.POST.get("ville", "").strip(),
            "pays": request.POST.get("pays", "Belgique").strip(),
            "code_pays": request.POST.get("code_pays", "BE").strip(),
            "societe": tenant
        }

        # Vérification des champs obligatoires
        if not adresse_data["rue"] or not adresse_data["numero"] or not adresse_data["code_postal"] or not adresse_data["ville"]:
            messages.error(request, _("Les champs d'adresse (rue, numéro, code postal, ville) sont obligatoires."))
        elif form_carrosserie.is_valid():
            # Crée l'adresse
            adresse = Adresse.objects.create(**adresse_data)

            # Crée la carrosserie et lie l'adresse
            carrosserie = form_carrosserie.save(commit=False)
            carrosserie.adresse = adresse
            carrosserie.save()

            messages.success(request, _(f"Carrosserie '{carrosserie.nom_societe}' créée avec succès !"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form_carrosserie = CarrosserieForm()

    return render(request, "carrosserie/carrosserie_form.html", {
        "form": form_carrosserie,
        "adresse": adresse_data  # permet de pré-remplir le template
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

    total_carrosserie = total_intervention = 0


    carrosseries = interventions = []

    if schema_name:
        with schema_context(schema_name):

            carrosseries = Carrosserie.objects.filter(societe=societe)
            interventions = Intervention.objects.all()


            # Totaux

            total_carrosserie = carrosseries.count()
            total_intervention = interventions.count()



    else:
        modeles = []

    context.update({
        'user': user,
        'societe': societe,

        'total_carrosserie': total_carrosserie,
        'total_intervention': total_intervention,


        'carrosserie': carrosseries,
        'intervention': interventions,

    })


    return render(request, "carrosserie/dashboard_carrosserie.html", context)


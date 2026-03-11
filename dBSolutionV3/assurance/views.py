# assurance/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context, schema_context
from adresse.models import Adresse
from django.utils.translation import gettext as _
from assurance.models import Assurance
from assurance.forms import AssuranceForm
from adresse.forms import AdresseForm
from assurance_police.models import AssurancePolice


@method_decorator([login_required, never_cache], name='dispatch')
class AssuranceListView(ListView):
    model = Assurance
    template_name = "assurance/assurance_list.html"
    context_object_name = "assurances"
    paginate_by = 20
    ordering = ["nom_compagnie"]

    def get_queryset(self):
        societe = self.request.user.societe
        return Assurance.objects.filter(societe=societe)


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
    tenant = request.user.societe

    if request.method == "POST":
        form_assurance = AssuranceForm(request.POST)

        adresse_data = {
            "rue": request.POST.get("rue"),
            "numero": request.POST.get("numero"),
            "code_postal": request.POST.get("code_postal"),
            "ville": request.POST.get("ville"),
            "pays": request.POST.get("pays"),
            "code_pays": request.POST.get("code_pays"),
            "societe": tenant
        }

        # Vérification champs obligatoires
        if not all([
            adresse_data["rue"],
            adresse_data["numero"],
            adresse_data["code_postal"],
            adresse_data["ville"]
        ]):
            messages.error(request, "Les champs d'adresse sont obligatoires.")

        elif form_assurance.is_valid():
            with transaction.atomic():     # évite la création d'adresse orpheline

                adresse = Adresse.objects.create(**adresse_data)

                # Création assurance
                assurance = form_assurance.save(commit=False)
                assurance.adresse = adresse
                assurance.societe = tenant
                assurance.save()

                messages.success(
                    request,
                    f"Assurance '{assurance.nom_compagnie}' créée avec succès !"
                )

        else:
            messages.error(request, "Le formulaire contient des erreurs.")

    else:
        form_assurance = AssuranceForm()

    return render(request, "assurance/assurance_form.html", {
                "form": form_assurance
    })



@login_required
def modifier_assurance(request, assurance_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupérer l'assureur et son adresse liée
        assurance = get_object_or_404(
            Assurance.objects.select_related("adresse"),
            id=assurance_id
        )
        adresse = assurance.adresse

        if request.method == "POST":
            # Formulaires pour Assurance et Adresse
            form_assurance = AssuranceForm(request.POST, instance=assurance)
            form_adresse = AdresseForm(request.POST, instance=adresse)

            if form_assurance.is_valid() and form_adresse.is_valid():
                # Sauvegarde adresse puis mise à jour de l'assurance
                adresse = form_adresse.save()
                assurance = form_assurance.save(commit=False)
                assurance.adresse = adresse
                assurance.save()

                messages.success(request, "Assurance et adresse mises à jour avec succès.")
                return redirect(
                    "assurance:modifier_assurance",
                    assurance_id=assurance.id
                )
            else:
                messages.error(request, "Le formulaire contient des erreurs.")
        else:
            # Pré-remplissage des formulaires
            form_assurance = AssuranceForm(instance=assurance)
            form_adresse = AdresseForm(instance=adresse)

    return render(
        request,
        "assurance/modifier_assurance.html",
        {
            "form": form_assurance,
            "form_adresse": form_adresse,
            "assurance": assurance,
            "adresse": adresse,
        }
    )





@never_cache
@login_required
def dashboard_assurance_view(request):
    user = request.user
    societe = getattr(user, "societe", None)

    # Valeurs par défaut
    total_assurance = 0
    total_assurance_police = 0
    assurance = []
    assurance_police = []

    if societe:
        schema_name = societe.schema_name

        with schema_context(schema_name):

            assurance = Assurance.objects.filter(societe=societe)
            assurance_police = AssurancePolice.objects.filter(societe=societe)

            total_assurance = assurance.count()
            total_assurance_police = assurance_police.count()

    context = {
        "user": user,
        "societe": societe,
        "total_assurance": total_assurance,
        "total_assurance_police": total_assurance_police,
        "assurance": assurance,
        "assurance_police": assurance_police,
    }

    return render(request, "assurance/dashboard_assurance.html", context)
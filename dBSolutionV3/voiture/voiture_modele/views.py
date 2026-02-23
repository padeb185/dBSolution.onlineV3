from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django_tenants.utils import tenant_context
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .forms import VoitureModeleForm
from .models import VoitureModele



@login_required
def modeles_par_marque(request, marque_id):
    marque = get_object_or_404(VoitureMarque, id_marque=marque_id)
    modeles = VoitureModele.objects.filter(marque=marque).order_by('nom_modele')
    context = {
        'marque': marque,
        'modeles': modeles,
    }
    return render(request, 'voiture_modele/modeles_list_all.html', context)


@login_required
class VoitureModeleListView(LoginRequiredMixin, ListView):
    model = VoitureModele
    template_name = "voiture_modele/modele_list_all.html"
    context_object_name = "modeles"
    paginate_by = 10

    def get_queryset(self):
        # 🔒 Filtrer par société de l'utilisateur
        return VoitureModele.objects.filter(
            societe=self.request.user.societe
        ).select_related("voiture_marque").order_by("nom_modele")



@login_required
def voiture_modele_detail(request, voiture_modele_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        voiture_modele = get_object_or_404(VoitureModele, id=voiture_modele_id)


    return render(
        request,
        "voiture_modele/voiture_modele_detail.html",
        {
            "voiture_modele": voiture_modele,

        },
    )


@login_required
def ajouter_voiture_modele_all(request):
    tenant = request.user.societe  # Société liée à l'utilisateur

    # Pré-remplissage en cas d'erreur
    adresse_data = {}

    if request.method == "POST":
        form_voiture_modele = VoitureModeleForm(request.POST)

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



        if form_voiture_modele.is_valid():
            voiture_modele = form_voiture_modele.save(commit=False)
            voiture_modele.save()

            messages.success(request, f"Modèle  '{voiture_modele.nom_modele}' créée avec succès !")

        else:
            messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form_voiture_modele = VoitureModeleForm()

    return render(request, "voiture_modele/voiture_modele_form.html", {
        "form": form_voiture_modele,
        "adresse": adresse_data  # permet de pré-remplir le template
    })



@login_required
def modifier_voiture_modele(request, voiture_modele_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupérer l'assureur et son adresse liée
        voiture_modele = get_object_or_404(
            VoitureModele.objects.select_related("adresse"),
            id=voiture_modele_id
        )
        adresse = voiture_modele.adresse

        if request.method == "POST":
            # Formulaires pour VoitureModele et Adresse
            form_voiture_modele = VoitureModeleForm(request.POST, instance=voiture_modele)


            if form_voiture_modele.is_valid():


                voiture_modele = form_voiture_modele.save(commit=False)
                voiture_modele.adresse = adresse
                voiture_modele.save()

                messages.success(request, "VoitureModele et adresse mises à jour avec succès.")
                return redirect(
                    "voiture_modele:modifier_voiture_modele",
                    voiture_modele_id=voiture_modele.id
                )
            else:
                messages.error(request, "Le formulaire contient des erreurs.")
        else:
            # Pré-remplissage des formulaires
            form_voiture_modele = VoitureModeleForm(instance=voiture_modele)


    return render(
        request,
        "voiture_modele/modifier_voiture_modele.html",
        {
            "form": form_voiture_modele,
            "voiture_modele": voiture_modele,
            "adresse": adresse,
        }
    )

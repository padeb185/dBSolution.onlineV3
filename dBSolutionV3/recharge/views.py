from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from recharge.models import Electricite
from recharge.forms import ElectriciteForm
from django.utils.translation import gettext_lazy as _
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele




@method_decorator([login_required, never_cache], name="dispatch")
class ElectriciteListView(ListView):
    model = Electricite
    template_name = "recharge/recharge_list.html"
    context_object_name = "recharges"   # ⚠️ important : pluriel
    paginate_by = 20
    ordering = ["-date"]

    def get_queryset(self):
        societe = self.request.user.societe
        return (
            Electricite.objects
            .select_related(
                "utilisateur",
                "voiture_exemplaire",
                "voiture_exemplaire__voiture_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque",
            )
            .order_by("-date_recharge")
            .filter(societe=societe)
        )



@login_required
def ajouter_recharge_all(request):
    tenant = request.user.societe  # récupère le tenant de l'utilisateur

    with tenant_context(tenant):
        if request.method == "POST":
            form = ElectriciteForm(request.POST)

            # --- Auto-remplissage de voiture_exemplaire via immatriculation si absent ---
            immatriculation = request.POST.get("immatriculation")
            if not request.POST.get("voiture_exemplaire") and immatriculation:
                try:
                    voiture = VoitureExemplaire.objects.get(immatriculation=immatriculation)
                    form.data = form.data.copy()
                    form.data["voiture_exemplaire"] = str(voiture.id)
                except VoitureExemplaire.DoesNotExist:
                    form.add_error("voiture_exemplaire", _("Voiture introuvable."))

            if form.is_valid():
                recharge = form.save(commit=False)


                recharge.utilisateur = request.user
                recharge.societe = request.user.societe

                recharge.save()
                messages.success(request, _("Recharge ajoutée avec succès."))
            else:
                print(form.errors)  # utile pour debug
                messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
        else:
            form = ElectriciteForm()

        type_carburant_choices = Electricite._meta.get_field("type_carburant").choices

        return render(
            request,
            "recharge/electricite_form.html",
            {
                "form": form,
                "recharge": form.instance,
                "type_carburant_choices": type_carburant_choices,
            },
        )
"""
@login_required
def ajouter_recharge_all(request):
    voiture = None

    # ⚡ Si immatriculation déjà passée en GET ou POST
    immat = request.GET.get("immat") or request.POST.get("immatriculation")
    if immat:
        try:
            voiture = VoitureExemplaire.objects.get(immatriculation=immat)
        except VoitureExemplaire.DoesNotExist:
            voiture = None

    if request.method == "POST":
        form = ElectriciteForm(request.POST, voiture=voiture)
        if form.is_valid():
            electricite = form.save(commit=False)
            electricite.utilisateur = request.user
            electricite.save()
            messages.success(request, "Recharge électrique ajoutée avec succès.")
            return redirect("recharge:recharge_list")
        else:
            print("ERREURS FORMULAIRE:", form.errors)
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ElectriciteForm(voiture=voiture)

    return render(request, "recharge/electricite_form.html", {"form": form})

"""

@login_required
def electricite_detail(request, electricite_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        electricite = get_object_or_404(Electricite, id=electricite_id)

    return render(
        request,
        "electricite/electricite_detail.html",
        {"electricite": electricite},
    )


@login_required
def modifier_electricite(request, electricite_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        electricite = get_object_or_404(
            Electricite,
            pk=electricite_id
        )

        if request.method == "POST":
            form = ElectriciteForm(
                request.POST,
                request.FILES,
                instance=electricite_id
            )

            if form.is_valid():
                electricite = form.save()
                messages.success(request, "le plein de carburant a été mis à jour avec succès.")

            else:
                messages.error(request, "Le formulaire contient des erreurs.")
        else:
            form = ElectriciteForm(instance=electricite)

    return render(
        request,
        "electricite/modifier_electricite.html",
        {
            "form": form,
            "electricite": electricite,
        }
    )







def check_immatriculation(request):
    immat = request.GET.get('immatriculation', '').strip()
    try:
        voiture = VoitureExemplaire.objects.get(immatriculation__iexact=immat)
        data = {
            'id': voiture.id,
            'marque': voiture.voiture_modele.voiture_marque.nom_marque,
            'modele': voiture.voiture_modele.nom_modele,
            'volume': voiture.voiture_modele.taille_reservoir,

        }
        return JsonResponse(data)
    except VoitureExemplaire.DoesNotExist:
        return JsonResponse({'error': 'not found'})






@require_GET
def get_marques(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse([], safe=False)

    marques = (
        VoitureMarque.objects
        .filter(nom_marque__icontains=query)
        .values_list("nom_marque", flat=True)
        .distinct()[:10]
    )

    return JsonResponse(list(marques), safe=False)


@require_GET
def get_modeles(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse([], safe=False)

    modeles = (
        VoitureModele.objects
        .filter(nom_modele__icontains=query)
        .values_list("nom_modele", flat=True)
        .distinct()[:10]
    )

    return JsonResponse(list(modeles), safe=False)


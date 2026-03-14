from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _
from django_tenants.utils import tenant_context

from recharge.models import Electricite
from recharge.forms import ElectriciteForm

from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele


@method_decorator([login_required, never_cache], name="dispatch")
class ElectriciteListView(ListView):
    model = Electricite
    template_name = "recharge/recharge_list.html"
    context_object_name = "recharges"
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
            .filter(societe=societe)
            .order_by("-date_recharge")
        )


@login_required
def ajouter_recharge_all(request):
    tenant = request.user.societe

    with tenant_context(tenant):

        if request.method == "POST":

            form = ElectriciteForm(request.POST)

            # 🔎 Auto-détection du véhicule via immatriculation
            immatriculation = request.POST.get("immatriculation")

            if not request.POST.get("voiture_exemplaire") and immatriculation:

                try:
                    voiture = VoitureExemplaire.objects.get(
                        immatriculation__iexact=immatriculation
                    )

                    form.data = form.data.copy()
                    form.data["voiture_exemplaire"] = str(voiture.id)

                except VoitureExemplaire.DoesNotExist:
                    form.add_error("voiture_exemplaire", _("Voiture introuvable."))

            if form.is_valid():

                recharge = form.save(commit=False)

                recharge.utilisateur = request.user
                recharge.societe = request.user.societe

                # ⚡ récupération automatique capacité batterie
                if recharge.voiture_exemplaire:
                    recharge.volume_max = (
                        recharge.voiture_exemplaire.voiture_modele.capacite_batterie
                    )
                else:
                    form.add_error(
                        "voiture_exemplaire",
                        _("Véhicule obligatoire."),
                    )

                    return render(
                        request,
                        "recharge/electricite_form.html",
                        {"form": form},
                    )

                recharge.save()

                messages.success(
                    request,
                    _("Recharge ajoutée avec succès.")
                )

                return redirect("recharge:recharge_list")

            else:

                print(form.errors)
                messages.error(
                    request,
                    _("Veuillez corriger les erreurs ci-dessous.")
                )

        else:

            form = ElectriciteForm()

        type_carburant_choices = (
            Electricite._meta.get_field("type_carburant").choices
        )

        return render(
            request,
            "recharge/electricite_form.html",
            {
                "form": form,
                "recharge": form.instance,
                "type_carburant_choices": type_carburant_choices,
            },
        )


@login_required
def electricite_detail(request, electricite_id):

    tenant = request.user.societe

    with tenant_context(tenant):

        electricite = get_object_or_404(
            Electricite,
            id=electricite_id
        )

    return render(
        request,
        "electricite/electricite_detail.html",
        {
            "electricite": electricite
        },
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
                instance=electricite
            )

            if form.is_valid():

                electricite = form.save()

                messages.success(
                    request,
                    _("La recharge a été mise à jour avec succès.")
                )

                return redirect("recharge:recharge_list")

            else:

                messages.error(
                    request,
                    _("Le formulaire contient des erreurs.")
                )

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


@login_required
def check_immatriculation(request):

    immat = request.GET.get("immatriculation", "").strip()

    try:

        voiture = VoitureExemplaire.objects.get(
            immatriculation__iexact=immat
        )

        data = {
            "id": voiture.id,
            "marque": voiture.voiture_modele.voiture_marque.nom_marque,
            "modele": voiture.voiture_modele.nom_modele,
            "volume": voiture.capacite_batterie,
        }

        return JsonResponse(data)

    except VoitureExemplaire.DoesNotExist:

        return JsonResponse(
            {"error": "not found"}
        )


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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from recharge.models import Electricite
from recharge.forms import ElectriciteForm
from django.utils.translation import gettext_lazy as _




@method_decorator([login_required, never_cache], name="dispatch")
class ElectriciteListView(ListView):
    model = Electricite
    template_name = "recharge/recharge_list.html"
    context_object_name = "recharges"   # ⚠️ important : pluriel
    paginate_by = 20
    ordering = ["-date"]

    def get_queryset(self):
        return (
            Electricite.objects
            .select_related(
                "utilisateur",
                "voiture_exemplaire",
                "voiture_exemplaire__voiture_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque",
            )
            .order_by("-date_recharge")
        )



@login_required
def ajouter_recharge_all(request):
    tenant = request.user.societe

    with tenant_context(tenant):
        if request.method == "POST":
            form = ElectriciteForm(request.POST)
            if form.is_valid():
                electricite = form.save(commit=False)
                electricite.utilisateur = request.user  # ⚡ Utilisateur courant
                electricite.save()
                messages.success(request, _("Recharge électrique ajoutée avec succès."))
                return redirect("recharge:recharge_list")  # redirection après POST
            else:
                messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
        else:
            form = ElectriciteForm()

        # ⚡ Créer une instance vierge sécurisée pour le template
        electricite_instance = form.instance
        if not electricite_instance.voiture_exemplaire_id:
            # On évite l'erreur RelatedObjectDoesNotExist
            electricite_instance.voiture_exemplaire = None

        # ⚡ Passer les choices de type_carburant au template
        type_carburant_choices = Electricite._meta.get_field("type_carburant").choices

        return render(
            request,
            "recharge/electricite_form.html",
            {
                "form": form,
                "electricite": electricite_instance,
                "type_carburant_choices": type_carburant_choices,
            },
        )




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

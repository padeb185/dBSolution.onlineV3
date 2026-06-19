from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import schema_context, tenant_context
from proprietaire.models import Proprietaire, ProprietaireVoiture
from django.utils.translation import gettext_lazy as _
from adresse.models import Adresse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ProprietaireForm, ProprietaireVoitureForm
from .models import Proprietaire
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from adresse.forms import AdresseForm





@never_cache
@login_required
def proprietaire_dashboard_view(request):
    user = request.user
    societe = getattr(user, "societe", None)

    # Valeurs par défaut
    total_proprietaire = 0
    total_voiture_cop = 0
    proprietaire = []
    proprietaire_voiture = []

    if societe:
        schema_name = societe.schema_name

        with schema_context(schema_name):

            proprietaire = Proprietaire.objects.filter(societe=societe)
            proprietaire_voiture = ProprietaireVoiture.objects.filter(societe=societe)

            total_proprietaire = proprietaire.count()
            total_voiture_cop = proprietaire_voiture.count()

    context = {
        "user": user,
        "societe": societe,
        "total_proprietaire": total_proprietaire,
        "total_voiture_cop": total_voiture_cop,
        "proprietaire": proprietaire,
        "proprietaire_voiture": proprietaire_voiture,

    }

    return render(request, "proprietaire/proprietaire_dashboard.html", context)




@method_decorator([login_required, never_cache], name='dispatch')
class ProprietaireListView(ListView):
    model = Proprietaire
    template_name = "proprietaire/proprietaire_list.html"
    context_object_name = "proprietaires"
    ordering = ["nom", "prenom"]

    def get_queryset(self):
        user = self.request.user

        if not hasattr(user, "societe") or user.societe is None:
            return Proprietaire.objects.none()

        return Proprietaire.objects.filter(societe=user.societe)




@login_required
def proprietaire_form_view(request):
    tenant = request.user.societe

    if request.method == "POST":
        form = ProprietaireForm(request.POST)

        adresse_instance = Adresse(societe=tenant)
        adresse_form = AdresseForm(request.POST, instance=adresse_instance)

        if form.is_valid() and adresse_form.is_valid():
            with tenant_context(tenant):
                adresse = adresse_form.save(commit=False)
                adresse.societe = tenant
                adresse.save()

                proprietaire = form.save(commit=False)
                proprietaire.societe = tenant
                proprietaire.adresse = adresse
                proprietaire.save()

                messages.success(
                    request,
                    _("Propriétaire '%(prenom)s %(nom)s' ajouté avec succès !") % {
                        "prenom": proprietaire.prenom,
                        "nom": proprietaire.nom
                    }
                )

                return redirect("proprietaire:proprietaire_list")
        else:
            print("FORM ERRORS:", form.errors)
            print("ADRESSE FORM ERRORS:", adresse_form.errors)
            messages.error(request, _("Veuillez corriger les erreurs du formulaire."))

    else:
        form = ProprietaireForm()
        adresse_form = AdresseForm()

    return render(
        request,
        "proprietaire/proprietaire_form.html",
        {
            "form": form,
            "adresse_form": adresse_form,
            "tenant": tenant,
        }
    )




@never_cache
@login_required
def proprietaire_detail_view(request, proprietaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        proprietaire = get_object_or_404(Proprietaire, id=proprietaire_id)
        adresse = proprietaire.adresse  # si tu veux l’afficher séparément

    return render(request, "proprietaire/proprietaire_detail.html", {
        "proprietaire": proprietaire,
        "adresse": adresse,
    })



@login_required
def modifier_proprietaire_view(request, proprietaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        proprietaire = get_object_or_404(Proprietaire, id=proprietaire_id)

        if request.method == "POST":
            form = ProprietaireForm(request.POST, instance=proprietaire)
            if form.is_valid():
                form.save()
                messages.success(request, _(f"Client '{proprietaire.prenom} {proprietaire.nom}' modifié avec succès !"))

            else:
                # Ici, si la carte bancaire est invalide, Django affichera automatiquement l'erreur
                messages.error(request, _("Veuillez corriger les erreurs dans le formulaire."))
        else:
            form = ProprietaireForm(instance=proprietaire)

    return render(
        request,
        "proprietaire/modifier_proprietaire.html",
        {
            "form": form,
            "proprietaire": proprietaire,
        }
    )





@method_decorator([login_required, never_cache], name='dispatch')
class ProprietaireVoitureListView(ListView):
    model = Proprietaire
    template_name = "proprietaire/proprietaire_voiture_list.html"
    context_object_name = "proprietaire_voitures"
    ordering = ["proprietaire_voitures"]

    def get_queryset(self):
        user = self.request.user

        if not hasattr(user, "societe") or user.societe is None:
            return ProprietaireVoiture.objects.none()

        return ProprietaireVoiture.objects.filter(societe=user.societe)




@login_required
def proprietaire_voiture_form_view(request):
    tenant = request.user.societe

    voitures = VoitureExemplaire.objects.all()
    proprietaires = Proprietaire.objects.filter(societe=tenant)
    tenant = request.user.societe

    if request.method == "POST":

        form = ProprietaireVoitureForm(request.POST)


        if form.is_valid():

            with tenant_context(tenant):

                # Sauvegarde propriétaire
                proprietaire_voiture = form.save(commit=False)
                proprietaire_voiture.societe = tenant

                proprietaire_voiture.save()

                messages.success(
                    request,
                    _(
                        f"Propriétaire '{proprietaire.prenom} {proprietaire.nom}' ajouté avec succès !"
                    )
                )

        else:
            messages.error(
                request,
                _("Veuillez corriger les erreurs du formulaire.")
            )

    else:
        form = ProprietaireVoitureForm()

    return render(
        request,
        "proprietaire/proprietaire_voiture_form.html",
        {
            "form": form,
            "tenant": tenant,
        }
    )


def total_part_voiture(request, voiture_id):
    total = (
        ProprietaireVoiture.objects
        .filter(voiture_exemplaire_id=voiture_id)
        .aggregate(total=Sum("part_proprietaire_pourcent"))
        ["total"] or 0
    )

    return JsonResponse({"total": total})


@login_required
def proprietaire_voiture_detail_view(request, proprietaire_voiture_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        proprietaire_voiture = get_object_or_404(ProprietaireVoiture, id=proprietaire_voiture_id)
        adresse = proprietaire_voiture.proprietaire.adresse

    return render(
        request,
        "proprietaire/proprietaire_voiture_detail.html",
        {
            "proprietaire_voiture": proprietaire_voiture,
            "adresse": adresse,
        },
    )



@login_required
def modifier_proprietaire_voiture_view(request, proprietaire_voiture_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        proprietaire_voiture = get_object_or_404(
            ProprietaireVoiture,
            id=proprietaire_voiture_id
        )

        if request.method == "POST":
            form_proprietaire_voiture = ProprietaireVoitureForm(
                request.POST,
                instance=proprietaire_voiture
            )

            if form_proprietaire_voiture.is_valid():  # ✅ corrigé
                proprietaire_voiture = form_proprietaire_voiture.save()

                messages.success(
                    request,
                    _("Propriété mise à jour avec succès.")
                )
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))

        else:
            form_proprietaire_voiture = ProprietaireVoitureForm(
                instance=proprietaire_voiture
            )

    return render(
        request,
        "proprietaire/modifier_proprietaire_voiture.html",
        {
            "form": form_proprietaire_voiture,
            "proprietaire_voiture": proprietaire_voiture,
        }
    )
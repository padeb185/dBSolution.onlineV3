from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
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
from .forms import ProprietaireForm
from .models import Proprietaire  # adapte au nom réel
from voiture.voiture_exemplaire.models import VoitureExemplaire


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

    proprietaire = Proprietaire()
    proprietaire.adresse = Adresse()

    if request.method == "POST":
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")

        if not nom or not prenom:
            messages.error(request, _("Le prénom et le nom du propriétaire sont obligatoires."))
        else:
            with tenant_context(tenant):
                adresse = Adresse.objects.create(
                    societe=tenant,
                    rue=request.POST.get("rue"),
                    numero=request.POST.get("numero"),
                    code_postal=request.POST.get("code_postal"),
                    ville=request.POST.get("ville"),
                    pays=request.POST.get("pays"),
                    code_pays=request.POST.get("code_pays")
                )

                proprietaire = Proprietaire.objects.create(
                    societe=tenant,
                    prenom=prenom,
                    nom=nom,
                    date_naissance=request.POST.get("date_naissance"),
                    numero_permis=request.POST.get("numero_permis"),
                    numero_carte_id=request.POST.get("numero_carte_id"),
                    numero_compte=request.POST.get("numero_compte"),
                    email=request.POST.get("email"),
                    numero_telephone=request.POST.get("numero_telephone"),
                    adresse=adresse
                )

                messages.success(
                    request,
                    _(f"Propriétaire '{proprietaire.prenom} {proprietaire.nom}' ajouté avec succès !")
                )

        if not hasattr(proprietaire, "adresse") or proprietaire.adresse is None:
            proprietaire.adresse = Adresse()

        return render(
            request,
            "proprietaire/proprietaire_form.html",
            {"proprietaire": proprietaire, "tenant": tenant}
        )


    return render(
        request,
        "proprietaire/proprietaire_form.html",
        {"proprietaire": proprietaire, "tenant": tenant}
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





@csrf_exempt  # facultatif si CSRF bien géré côté JS
def check_prenom(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prenom = data.get("prenom")

        try:
            proprietaire = Proprietaire.objects.select_related("adresse").get(prenom__iexact=prenom)

            return JsonResponse({
                "exist": True,
                "prenom": proprietaire.prenom,
                "nom": proprietaire.nom,
                "email": proprietaire.email,
                "adresse": {
                    "rue": proprietaire.adresse.rue if proprietaire.adresse else "",
                    "numero": proprietaire.adresse.numero if proprietaire.adresse else "",
                    "code_postal": proprietaire.adresse.code_postal if proprietaire.adresse else "",
                    "ville": proprietaire.adresse.ville if proprietaire.adresse else "",
                    "pays": proprietaire.adresse.pays if proprietaire.adresse else "",
                    "code_pays": proprietaire.adresse.code_pays if proprietaire.adresse else "",
                } if proprietaire.adresse else None
            })

        except Proprietaire.DoesNotExist:
            return JsonResponse({"exist": False})

    return JsonResponse({"error": "Invalid request"}, status=400)








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

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

@login_required
def proprietaire_voiture_form_view(request):
    tenant = request.user.societe

    voitures = VoitureExemplaire.objects.all()
    proprietaires = Proprietaire.objects.filter(societe=tenant)

    if request.method == "POST":

        proprietaire_id = request.POST.get("proprietaire")
        exemplaire_id = request.POST.get("exemplaire")
        part = request.POST.get("part_proprietaire_pourcent")

        # Validation basique
        if not proprietaire_id or not exemplaire_id:
            messages.error(request, _("Veuillez sélectionner un propriétaire et une voiture."))
            return redirect("proprietaire:proprietaire_voiture_form")

        # Conversion safe
        try:
            part = float(part) if part else 100
        except ValueError:
            messages.error(request, _("La part doit être un nombre valide."))
            return redirect("proprietaire:proprietaire_voiture_form")

        with tenant_context(tenant):

            proprietaire = get_object_or_404(
                Proprietaire,
                id=proprietaire_id,
                societe=tenant
            )

            voiture_exemplaire = get_object_or_404(
                VoitureExemplaire,
                id=exemplaire_id
            )

            try:
                obj = ProprietaireVoiture(
                    societe=tenant,
                    proprietaire=proprietaire,
                    voiture_exemplaire=voiture_exemplaire,
                    part_proprietaire_pourcent=part
                )

                # 🔥 IMPORTANT : déclenche la validation 100%
                obj.full_clean()
                obj.save()

                messages.success(request, _("Association créée avec succès !"))
                return redirect("proprietaire:proprietaire_voiture_list")

            except ValidationError as e:
                messages.error(request, e.messages[0])
                return redirect("proprietaire:proprietaire_voiture_form")

    return render(
        request,
        "proprietaire/proprietaire_voiture_form.html",
        {
            "tenant": tenant,
            "voitures": voitures,
            "proprietaires": proprietaires
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

def proprietaire_voiture_detail_view(request):
    return render(request, 'proprietaire/proprietaire_voiture_detail.html')
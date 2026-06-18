from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context, schema_context
from adresse.models import Adresse
from django.utils.translation import gettext as _
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from client_atelier.forms import ClientAtelierForm
from client_atelier.models import ClientAtelier
from societe_cliente.models import SocieteCliente
from client_particulier.models import ClientParticulier
from voiture.voiture_exemplaire.models import VoitureExemplaire
from client_pilotage.models import ClientPilotage


@method_decorator([login_required, never_cache], name='dispatch')
class ClientAtelierListView(ListView):
    model = ClientAtelier
    template_name = "client_atelier/client_atelier_list.html"
    context_object_name = "client_ateliers"
    ordering = ["nom", "prenom"]

    def get_queryset(self):
        societe = self.request.user.societe
        return ClientAtelier.objects.filter(societe=societe)




@never_cache
@login_required
def client_atelier_detail_view(request, client_atelier_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        client_atelier = get_object_or_404(ClientAtelier, id=client_atelier_id)
        adresse = client_atelier.adresse  # si tu veux l’afficher séparément

    return render(request, "client_atelier/client_atelier_detail.html", {
        "client_atelier": client_atelier,
        "adresse": adresse,
    })




@login_required
def client_atelier_form_view(request):
    tenant = request.user.societe

    with tenant_context(tenant):

        if request.method == "POST":

            form = ClientAtelierForm(request.POST)

            if form.is_valid():

                with transaction.atomic():

                    # -----------------------
                    # CLIENT PARTICULIER
                    # -----------------------
                    client_particulier = ClientParticulier.objects.create(
                        societe=tenant,
                        nom=form.cleaned_data.get("nom"),
                        prenom=form.cleaned_data.get("prenom"),
                        email=form.cleaned_data.get("email"),
                        numero_telephone=form.cleaned_data.get("numero_telephone"),
                        numero_carte_id=form.cleaned_data.get("numero_carte_id"),
                        numero_compte=form.cleaned_data.get("numero_compte"),
                        numero_carte_bancaire=form.cleaned_data.get("numero_carte_bancaire"),
                        date_naissance=form.cleaned_data.get("date_naissance"),
                    )

                    # -----------------------
                    # ADRESSE
                    # -----------------------
                    adresse = Adresse.objects.create(
                        societe=tenant,
                        rue=form.cleaned_data.get("rue"),
                        numero=form.cleaned_data.get("numero"),
                        boite=form.cleaned_data.get("boite"),
                        code_postal=form.cleaned_data.get("code_postal"),
                        ville=form.cleaned_data.get("ville"),
                        pays=form.cleaned_data.get("pays"),
                        code_pays=form.cleaned_data.get("code_pays"),
                    )

                    # -----------------------
                    # CLIENT ATELIER
                    # -----------------------
                    client_atelier = form.save(commit=False)
                    client_atelier.client_particulier = client_particulier
                    client_atelier.societe = tenant
                    client_atelier.adresse = adresse
                    client_atelier.save()

                    form.save_m2m()

                messages.success(
                    request,
                    _(
                        "Client '%(prenom)s %(nom)s' créé avec succès !"
                    ) % {
                        "prenom": client_particulier.prenom,
                        "nom": client_particulier.nom,
                    }
                )

            else:
                messages.error(
                    request,
                    _("Veuillez corriger les erreurs du formulaire.")
                )

        else:
            form = ClientAtelierForm()

        return render(
            request,
            "client_atelier/client_atelier_form.html",
            {
                "form": form,
            }
        )

@login_required
def modifier_client_atelier_view(request, client_atelier_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        client_atelier = get_object_or_404(
            ClientAtelier.objects.select_related(
                "client_particulier",
                "adresse",
                "societe_cliente",
            ),
            id=client_atelier_id,
            societe=tenant,
        )

        cp = client_atelier.client_particulier
        adresse = client_atelier.adresse

        societes = SocieteCliente.objects.filter(societe=tenant)

        if request.method == "POST":

            form = ClientAtelierForm(
                request.POST,
                instance=client_atelier
            )

            if form.is_valid():

                with transaction.atomic():

                    obj = form.save(commit=False)
                    obj.societe = tenant

                    # CLIENT PARTICULIER
                    cp.prenom = form.cleaned_data.get("prenom")
                    cp.nom = form.cleaned_data.get("nom")
                    cp.email = form.cleaned_data.get("email")
                    cp.numero_telephone = form.cleaned_data.get("numero_telephone")
                    cp.numero_carte_id = form.cleaned_data.get("numero_carte_id")
                    cp.numero_compte = form.cleaned_data.get("numero_compte")
                    cp.numero_carte_bancaire = form.cleaned_data.get("numero_carte_bancaire")
                    cp.date_naissance = form.cleaned_data.get("date_naissance")
                    cp.save()

                    # ADRESSE
                    if adresse is None:
                        adresse = Adresse.objects.create(societe=tenant)

                    adresse.rue = form.cleaned_data.get("rue")
                    adresse.numero = form.cleaned_data.get("numero")
                    adresse.boite = form.cleaned_data.get("boite")
                    adresse.code_postal = form.cleaned_data.get("code_postal")
                    adresse.ville = form.cleaned_data.get("ville")
                    adresse.pays = form.cleaned_data.get("pays")
                    adresse.code_pays = form.cleaned_data.get("code_pays")
                    adresse.save()

                    # RELATIONS FINAL
                    obj.client_particulier = cp
                    obj.adresse = adresse
                    obj.save()

                    form.save_m2m()

                messages.success(
                    request,
                    _("Client '%(prenom)s %(nom)s' modifié avec succès !") % {
                        "prenom": cp.prenom,
                        "nom": cp.nom,
                    }
                )

            else:
                messages.error(
                    request,
                    _("Veuillez corriger les erreurs dans le formulaire.")
                )

        else:

            initial = {}

            if cp:
                initial.update({
                    "prenom": cp.prenom,
                    "nom": cp.nom,
                    "email": cp.email,
                    "numero_telephone": cp.numero_telephone,
                    "numero_carte_id": cp.numero_carte_id,
                    "numero_compte": cp.numero_compte,
                    "numero_carte_bancaire": cp.numero_carte_bancaire,
                })

                if cp.date_naissance:
                    initial["date_naissance"] = cp.date_naissance.strftime("%Y-%m-%d")

            if adresse:
                initial.update({
                    "rue": adresse.rue,
                    "numero": adresse.numero,
                    "boite": adresse.boite,
                    "code_postal": adresse.code_postal,
                    "ville": adresse.ville,
                    "pays": adresse.pays,
                    "code_pays": adresse.code_pays,
                })

            form = ClientAtelierForm(
                instance=client_atelier,
                initial=initial
            )

        return render(
            request,
            "client_atelier/modifier_client_atelier.html",
            {
                "form": form,
                "client_atelier": client_atelier,
                "societes": societes,
                "adresse": adresse,
            }
        )

def client_atelier_view(request):
    tenant = request.user.societe

    with tenant_context(tenant):

        if request.method == "POST":
            form = ClientAtelierForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, _("Client créé avec succès !"))

            else:
                messages.error(request, _("Veuillez corriger les erreurs dans le formulaire."))
        else:
            form = ClientAtelierForm()

        return render(request, "client_atelier_form.html", {"form": form})





@csrf_exempt  # facultatif si CSRF bien géré côté JS
def check_prenom(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prenom = data.get("prenom")

        try:
            client = ClientAtelier.objects.select_related("adresse").get(prenom__iexact=prenom)

            return JsonResponse({
                "exist": True,
                "prenom": client.prenom,
                "nom": client.nom,
                "email": client.email,
                "adresse": {
                    "rue": client.adresse.rue if client.adresse else "",
                    "numero": client.adresse.numero if client.adresse else "",
                    "code_postal": client.adresse.code_postal if client.adresse else "",
                    "ville": client.adresse.ville if client.adresse else "",
                    "pays": client.adresse.pays if client.adresse else "",
                    "code_pays": client.adresse.code_pays if client.adresse else "",
                } if client.adresse else None
            })

        except ClientAtelier.DoesNotExist:
            return JsonResponse({"exist": False})

    return JsonResponse({"error": "Invalid request"}, status=400)





@never_cache
@login_required
def dashboard_client_view(request):
    user = request.user
    societe = getattr(user, "societe", None)

    # Valeurs par défaut
    total_client = 0
    total_client_atelier = 0
    total_client_pilotage = 0
    client_particulier = []
    client_atelier = []
    client_pilotage = []

    if societe:
        schema_name = societe.schema_name

        with schema_context(schema_name):

            client_particulier = ClientParticulier.objects.filter(societe=societe)
            client_atelier = ClientAtelier.objects.filter(societe=societe)
            client_pilotage = ClientPilotage.objects.filter(societe=societe)

            total_client_particulier = client_particulier.count()
            total_client_atelier = client_atelier.count()
            total_client_pilotage = client_pilotage.count()

    context = {
        "user": user,
        "societe": societe,
        "total_client_particulier": total_client_particulier,
        "total_client_atelier": total_client_atelier,
        "total_client_pilotage": total_client_pilotage,
        "client_particulier": client_particulier,
        "client_atelier": client_atelier,
        "client_pilotage": client_pilotage,
    }

    return render(request, "client_atelier/dashboard_client.html", context)
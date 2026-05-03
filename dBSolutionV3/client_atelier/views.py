from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

from dBSolutionV3.client_particulier.models import ClientParticulier


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
    tenant = request.user.societe  # le tenant courant

    # Crée un objet client vide pour le formulaire
    client_atelier = ClientAtelier()
    client_atelier.adresse = Adresse()
    societes = SocieteCliente.objects.filter(societe=tenant)


    if request.method == "POST":
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        societe_id = request.POST.get("societe_cliente")

        if not nom or not prenom:
            messages.error(request, _("Le prénom et le nom du client sont obligatoires."))
        else:
            # Crée l'adresse en tenant compte du tenant
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

                societe = None
                if societe_id:
                    societe = SocieteCliente.objects.filter(id=societe_id).first()

                # Crée le client en associant le tenant et l'adresse
                client_atelier = ClientAtelier.objects.create(
                    societe=tenant,
                    prenom=prenom,
                    nom=nom,
                    numero_carte_id=request.POST.get("numero_carte_id"),
                    numero_compte=request.POST.get("numero_compte"),
                    email=request.POST.get("email"),
                    numero_telephone=request.POST.get("numero_telephone"),
                    adresse=adresse
                )

                messages.success(
                    request,
                    _(f"Client '{client_atelier.prenom} {client_atelier.nom}' ajouté avec succès !")
                )

    # S'assurer que client.adresse existe pour le formulaire
    if not hasattr(client_atelier, "adresse") or client_atelier.adresse is None:
        client_atelier.adresse = Adresse()

    return render(
        request,
        "client_atelier/client_atelier_form.html",
        {
            "client_atelier": client_atelier,
            "tenant": tenant,
            "societes": societes,
        }
    )







@login_required
def modifier_client_atelier_view(request, client_atelier_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        client_atelier = get_object_or_404(ClientAtelier, id=client_atelier_id)
        societes = SocieteCliente.objects.filter(societe=tenant)

        if request.method == "POST":
            form = ClientAtelierForm(request.POST, instance=client_atelier)
            if form.is_valid():
                form.save()
                messages.success(request, _(f"Client '{client_atelier.prenom} {client_atelier.nom}' modifié avec succès !"))

            else:
                # Ici, si la carte bancaire est invalide, Django affichera automatiquement l'erreur
                messages.error(request, _("Veuillez corriger les erreurs dans le formulaire."))
        else:
            form = ClientAtelierForm(instance=client_atelier)

    return render(
        request,
        "client_atelier/modifier_client_atelier.html",
        {
            "form": form,
            "client_atelier": client_atelier,
            "societes": societes,
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
    client_particulier = []
    client_atelier = []

    if societe:
        schema_name = societe.schema_name

        with schema_context(schema_name):

            client_particulier = ClientParticulier.objects.filter(societe=societe)
            client_atelier = ClientAtelier.objects.filter(societe=societe)

            total_client_particulier = client_particulier.count()
            total_client_atelier = client_atelier.count()

    context = {
        "user": user,
        "societe": societe,
        "total_client_particulier": total_client_particulier,
        "total_client_atelier": total_client_atelier,
        "client_particulier": client_particulier,
        "client_atelier": client_atelier,
    }

    return render(request, "client_atelier/dashboard_client.html", context)
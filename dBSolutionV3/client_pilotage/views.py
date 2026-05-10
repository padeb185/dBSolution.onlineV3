from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from adresse.models import Adresse
from .forms import ClientPilotageForm
from .models import  ClientPilotage
from django.utils.translation import gettext as _
from societe_cliente.models import SocieteCliente
from voiture.voiture_exemplaire.models import VoitureExemplaire





@method_decorator([login_required, never_cache], name='dispatch')
class ClientPilotageListView(ListView):
    model = ClientPilotage
    template_name = "client_pilotage/client_pilotage_list.html"
    context_object_name = "clients pilotages"
    ordering = ["nom", "prenom"]

    def get_queryset(self):
        societe = self.request.user.societe
        return ClientPilotage.objects.filter(societe=societe)




@never_cache
@login_required
def client_pilotage_detail_view(request, client_pilotage_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        client_pilotage = get_object_or_404(ClientPilotage, id=client_pilotage_id)
        adresse = client_pilotage.adresse  # si tu veux l’afficher séparément

    return render(request, "client_pilotage/client_pilotage_detail.html", {
        "client_pilotage": client_pilotage,
        "adresse": adresse,
    })




@login_required
def modifier_client_pilotage_view(request, client_pilotage_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        client_pilotage = get_object_or_404(ClientPilotage, id=client_pilotage_id)

        if request.method == "POST":
            form = ClientPilotageForm(request.POST, instance=client_pilotage)
            if form.is_valid():
                form.save()
                messages.success(request, _(f"Client '{client_pilotage.prenom} {client_pilotage.nom}' modifié avec succès !"))

            else:
                # Ici, si la carte bancaire est invalide, Django affichera automatiquement l'erreur
                messages.error(request, _("Veuillez corriger les erreurs dans le formulaire."))
        else:
            form = ClientPilotageForm(instance=client_pilotage)

    return render(
        request,
        "client_pilotage/modifier_client_pilotage.html",
        {
            "form": form,
            "client_pilotage": client_pilotage,
        }
    )


@login_required
def client_pilotage_form_view(request):
    tenant = request.user.societe

    client_pilotage = ClientPilotage()
    client_pilotage.adresse = Adresse()
    societes = SocieteCliente.objects.filter(societe=tenant)
    voitures = VoitureExemplaire.objects.filter(societe=tenant)

    if request.method == "POST":
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        societe_id = request.POST.get("societe_cliente")

        if not nom or not prenom:
            messages.error(request, _("Le prénom et le nom du client sont obligatoires."))
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

                societes = None
                if societe_id:
                    societes = SocieteCliente.objects.filter(id=societe_id).first()

                client_pilotage = ClientPilotage.objects.create(
                    societe=tenant,
                    prenom=prenom,
                    nom=nom,
                    numero_carte_id=request.POST.get("numero_carte_id"),
                    numero_compte=request.POST.get("numero_compte"),
                    email=request.POST.get("email"),
                    numero_telephone=request.POST.get("numero_telephone"),
                    adresse=adresse
                )

                # ✅ 🔥 AJOUT DES VOITURES
                voiture_ids = request.POST.getlist("voitures")
                if voiture_ids:
                    client_pilotage.voitures.set(voiture_ids)

                messages.success(
                    request,
                    _(f"Client '{client_pilotage.prenom} {client_pilotage.nom}' ajouté avec succès !")
                )

    if not hasattr(client_pilotage, "adresse") or client_pilotage.adresse is None:
        client_pilotage.adresse = Adresse()

    return render(
        request,
        "client_atelier/client_atelier_form.html",
        {
            "client_atelier": client_pilotage,
            "tenant": tenant,
            "societes": societes,
            "voitures": voitures,
        }
    )


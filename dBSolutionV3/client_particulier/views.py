from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from adresse.models import Adresse
from .forms import ClientParticulierForm
from .models import ClientParticulier
from django.utils.translation import gettext as _



@method_decorator([login_required, never_cache], name='dispatch')
class ClientParticulierListView(ListView):
    model = ClientParticulier
    template_name = "client_particulier/client_list.html"
    context_object_name = "clients"
    paginate_by = 20
    ordering = ["nom", "prenom"]




@never_cache
@login_required
def client_detail(request, client_particulier_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        client_particulier = get_object_or_404(ClientParticulier, id=client_particulier_id)
        adresse = client_particulier.adresse  # si tu veux l’afficher séparément

    return render(request, "client_particulier/client_detail.html", {
        "client_particulier": client_particulier,
        "adresse": adresse,
    })






@login_required
def ajouter_client_all(request):
    # Crée un objet client vide pour le formulaire
    client_particulier = ClientParticulier()
    client_particulier.adresse = Adresse()

    if request.method == "POST":
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")

        if not nom or not prenom:
            messages.error(request, _("Le prénom et le nom du client sont obligatoires."))
        else:
            adresse = Adresse.objects.create(
                rue=request.POST.get("rue"),
                numero=request.POST.get("numero"),
                code_postal=request.POST.get("code_postal"),
                ville=request.POST.get("ville"),
                pays=request.POST.get("pays"),
                code_pays=request.POST.get("code_pays")
            )

            client_particulier = ClientParticulier.objects.create(
                prenom=prenom,
                nom=nom,
                date_naissance=request.POST.get("date_naissance"),
                numero_permis=request.POST.get("numero_permis"),
                numero_carte_id=request.POST.get("numero_carte_id"),
                numero_compte=request.POST.get("numero_compte"),
                email=request.POST.get("email"),
                numero_telephone=request.POST.get("numero_telephone"),
                niveau=request.POST.get("niveau") or ClientParticulier.Niveau.DEBUTANT,
                historique=request.POST.get("historique"),
                location=request.POST.get("location"),
                adresse=adresse
            )

            messages.success(request, _(f"Client '{client_particulier.prenom} {client_particulier.nom}' ajouté avec succès !"))



    # S'assurer que client.adresse existe
    if not hasattr(client_particulier, "adresse") or client_particulier.adresse is None:
        client_particulier.adresse = Adresse()

    return render(request, "client_particulier/client_form.html", {"client_particulier": client_particulier})







@login_required
def modifier_client(request, client_particulier_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        client_particulier = get_object_or_404(ClientParticulier, id=client_particulier_id)

        if request.method == "POST":
            form = ClientParticulierForm(request.POST, instance=client_particulier)
            if form.is_valid():
                form.save()
                messages.success(request, _(f"Client '{client_particulier.prenom} {client_particulier.nom}' modifié avec succès !"))

            else:
                # Ici, si la carte bancaire est invalide, Django affichera automatiquement l'erreur
                messages.error(request, _("Veuillez corriger les erreurs dans le formulaire."))
        else:
            form = ClientParticulierForm(instance=client_particulier)

    return render(
        request,
        "client_particulier/modifier_client.html",
        {
            "form": form,
            "client_particulier": client_particulier,
        }
    )



def client_create_view(request):
    tenant = request.user.societe

    with tenant_context(tenant):

        if request.method == "POST":
            form = ClientParticulierForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Client créé avec succès !")
                return redirect("client_list")
            else:
                messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
        else:
            form = ClientParticulierForm()

        return render(request, "client_form.html", {"form": form})
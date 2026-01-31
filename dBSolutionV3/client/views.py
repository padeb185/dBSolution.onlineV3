from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from adresse.models import Adresse
from client.forms import ClientForm
from client.models import Client




class ClientListView(ListView):
    model = Client
    template_name = "client/client_list.html"
    context_object_name = "clients"
    paginate_by = 20
    ordering = ["nom", "prenom"]




@never_cache
@login_required
def client_detail(request, client_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        client = get_object_or_404(Client, id=client_id)
        adresse = client.adresse

    return render(
        request,
        "client/client_detail.html",
        {
            "client": client,
            "adresse": adresse,
        },
    )







@login_required
def ajouter_client_all(request):
    # Crée un objet client vide pour le formulaire
    client = Client()
    client.adresse = Adresse()

    if request.method == "POST":
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")

        if not nom or not prenom:
            messages.error(request, "Le prénom et le nom du client sont obligatoires.")
        else:
            adresse = Adresse.objects.create(
                rue=request.POST.get("rue"),
                numero=request.POST.get("numero"),
                code_postal=request.POST.get("code_postal"),
                ville=request.POST.get("ville"),
                pays=request.POST.get("pays"),
                code_pays=request.POST.get("code_pays")
            )

            client = Client.objects.create(
                prenom=prenom,
                nom=nom,
                date_naissance=request.POST.get("date_naissance"),
                numero_permis=request.POST.get("numero_permis"),
                numero_carte_id=request.POST.get("numero_carte_id"),
                numero_compte=request.POST.get("numero_compte"),
                email=request.POST.get("email"),
                numero_telephone=request.POST.get("numero_telephone"),
                niveau=request.POST.get("niveau") or Client.Niveau.DEBUTANT,
                historique=request.POST.get("historique"),
                location=request.POST.get("location"),
                adresse=adresse
            )

            messages.success(request, f"Client '{client.nom}' ajouté avec succès !")

            # NE PAS faire de redirect, on reste sur le formulaire
            # client = Client()  # si tu veux réinitialiser le formulaire

    # S'assurer que client.adresse existe
    if not hasattr(client, "adresse") or client.adresse is None:
        client.adresse = Adresse()

    return render(request, "client/client_form.html", {"client": client})






@login_required
def modifier_client(request, client_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        client = get_object_or_404(Client, id=client_id)

        if request.method == "POST":
            form = ClientForm(request.POST, instance=client)
            if form.is_valid():
                form.save()
                messages.success(request, "Client mis à jour avec succès.")
                return redirect(
                    'client:modifier_client',
                    client_id=client.id
                )
        else:
            form = ClientForm(instance=client)

    return render(
        request,
        "client/modifier_client.html",
        {
            "form": form,
            "client": client,
        }
    )

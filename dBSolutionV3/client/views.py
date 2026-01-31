from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context

from dBSolutionV3.adresse.models import Adresse
from dBSolutionV3.client.forms import ClientForm
from dBSolutionV3.client.models import Client




class FournisseurListView(ListView):
    model = Client
    template_name = "client/client_list.html"
    context_object_name = "client"
    paginate_by = 20
    ordering = ["nom", "prenom"]


@never_cache
@login_required
def fournisseur_detail(request, client_id):
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
    client = Client()
    client.adresse = Adresse()

    if request.method == "POST":
        nom = request.POST.get("client")


        if not nom:
            messages.error(request, "Le nom du client est obligatoire.")
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
                prenom=request.POST.get("prenom"),
                nom=nom,
                date_naissance=request.POST.get("date_naissance"),
                age=request.POST.get("age") or 0,
                numero_cate_id=request.POST.get("numero_cate_id"),
                numero_permis=request.POST.get("numero_permis"),
                numero_compte=request.POST.get("numero_compte"),

                email=request.POST.get("email"),
                numero_telephone=request.POST.get("numero_telephone"),
                niveau=request.POST.get("niveau"),
                historique=request.POST.get("historique"),
                localisation=request.POST.get("localisation"),
                adresse=adresse
            )
            messages.success(request, f"Client '{client.nom}' ajouté avec succès !")
            return redirect("client:client_forms")

    # S'assurer que fournisseur.adresse existe
    if not hasattr(client, "adresse") or client.adresse is None:
        client.adresse = Adresse()

    return render(request, "client/client_form.html", {"client": client})




@login_required
def modifier_fournisseur(request, client_id):
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

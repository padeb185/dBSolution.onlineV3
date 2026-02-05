from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from adresse.models import Adresse
from societe_cliente.models import SocieteCliente
from societe_cliente.forms import SocieteClienteForm




@method_decorator([login_required, never_cache], name='dispatch')
class SocieteClienteListView(ListView):
    model = SocieteCliente
    template_name = "societe_cliente/societe_cliente_list.html"
    context_object_name = "societe_clientes"
    paginate_by = 20
    ordering = ["nom_societe_cliente" ]






@never_cache
@login_required
def societe_cliente_detail(request, societe_cliente_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        societe_cliente = get_object_or_404(
            SocieteCliente,
            id_societe_cliente=societe_cliente_id
        )

        adresse = societe_cliente.adresse

    return render(
        request,
        "societe_cliente/societe_cliente_detail.html",
        {
            "societe_cliente": societe_cliente,
            "adresse": adresse,
        },
    )







@login_required
def ajouter_societe_cliente_all(request):
    # Crée un objet client vide pour le formulaire
    societe_cliente = SocieteCliente()
    societe_cliente.adresse = Adresse()

    if request.method == "POST":
        nom_societe_cliente = request.POST.get("nom_societe_cliente")


        if not nom_societe_cliente:
            messages.error(request, "Le nom de la société cliente est obligatoire.")
        else:
            adresse = Adresse.objects.create(
                rue=request.POST.get("rue"),
                numero=request.POST.get("numero"),
                code_postal=request.POST.get("code_postal"),
                ville=request.POST.get("ville"),
                pays=request.POST.get("pays"),
                code_pays=request.POST.get("code_pays")
            )

            societe_cliente = SocieteCliente.objects.create(
                nom_societe_cliente=nom_societe_cliente,
                directeur_nom_prenom=request.POST.get("directeur_nom_prenom"),
                numero_telephone=request.POST.get("numero_telephone"),
                numero_compte=request.POST.get("numero_compte"),
                numero_tva=request.POST.get("numero_tva"),
                site_internet=request.POST.get("site_internet"),
                email=request.POST.get("email"),
                historique=request.POST.get("historique"),
                location=request.POST.get("location"),
                adresse=adresse,
                code_pays=request.POST.get("code_pays")
            )

            messages.success(request, f"SocieteCliente '{societe_cliente.nom_societe_cliente}' ajouté avec succès !")

            # NE PAS faire de redirect, on reste sur le formulaire
            # client = Client()  # si tu veux réinitialiser le formulaire

    # S'assurer que client.adresse existe
    if not hasattr(societe_cliente, "adresse") or societe_cliente.adresse is None:
        societe_cliente.adresse = Adresse()

    return render(request, "societe_cliente/societe_cliente_form.html", {"societe_cliente": societe_cliente})






@login_required
def modifier_societe_cliente(request, societe_cliente_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        societe_cliente = get_object_or_404(
            SocieteCliente,
            id_societe_cliente=societe_cliente_id
        )

        if request.method == "POST":
            form = SocieteClienteForm(request.POST, instance=societe_cliente)
            if form.is_valid():
                form.save()
                messages.success(request, "Société cliente mis à jour avec succès.")
                return redirect(
                    'societe_cliente:modifier_societe_cliente',
                    societe_cliente_id=societe_cliente.id_societe_cliente
                )
        else:
            form = SocieteClienteForm(instance=societe_cliente)

    return render(
        request,
        "societe_cliente/modifier_societe_cliente.html",
        {
            "form": form,
            "societe_cliente": societe_cliente,
        }
    )

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
from django.utils.translation import gettext as _






@method_decorator([login_required, never_cache], name="dispatch")
class SocieteClienteListView(ListView):
    model = SocieteCliente
    template_name = "societe_cliente/societe_cliente_list.html"
    context_object_name = "societe_clientes"
    paginate_by = 20
    ordering = ["nom_societe_cliente"]

    def dispatch(self, request, *args, **kwargs):
        self.tenant = getattr(request.user, "societe", None)

        if not self.tenant:
            messages.error(request, "Aucune société sélectionnée.")
            return redirect("dashboard")  # adapte la redirection

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        societe = self.request.user.societe
        with tenant_context(self.tenant):
            return (
                SocieteCliente.objects.all()
                .order_by("nom_societe_cliente")
                .filter(societe=societe)
            )



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

    tenant = request.user.societe

    with tenant_context(tenant):

        if request.method == "POST":

            form = SocieteClienteForm(request.POST)

            if form.is_valid():

                # Création adresse
                adresse = Adresse.objects.create(
                    rue=form.cleaned_data.get("rue"),
                    numero=form.cleaned_data.get("numero"),
                    code_postal=form.cleaned_data.get("code_postal"),
                    ville=form.cleaned_data.get("ville"),
                    pays=form.cleaned_data.get("pays"),
                    code_pays=form.cleaned_data.get("code_pays"),
                )

                # Création société
                societe_cliente = form.save(commit=False)
                societe_cliente.societe = tenant
                societe_cliente.adresse = adresse
                societe_cliente.save()

                messages.success(
                    request,
                    _("Société cliente ajoutée avec succès !")
                )

        else:
            form = SocieteClienteForm()

        return render(
            request,
            "societe_cliente/societe_cliente_form.html",
            {
                "form": form
            }
        )




@login_required
def modifier_societe_cliente(request, societe_cliente_id):

    tenant = request.user.societe

    with tenant_context(tenant):

        societe_cliente = get_object_or_404(
            SocieteCliente,
            id_societe_cliente=societe_cliente_id
        )

        if request.method == "POST":

            form = SocieteClienteForm(
                request.POST,
                instance=societe_cliente
            )

            if form.is_valid():

                # -------------------------
                # MAJ ADRESSE
                # -------------------------
                adresse = societe_cliente.adresse

                adresse.rue = form.cleaned_data.get("rue")
                adresse.numero = form.cleaned_data.get("numero")
                adresse.code_postal = form.cleaned_data.get("code_postal")
                adresse.ville = form.cleaned_data.get("ville")
                adresse.pays = form.cleaned_data.get("pays")
                adresse.code_pays = form.cleaned_data.get("code_pays")

                adresse.save()

                # -------------------------
                # MAJ SOCIETE
                # -------------------------
                form.save()

                messages.success(
                    request,
                    _(
                        f"SocieteCliente '{societe_cliente.nom_societe_cliente}' modifiée avec succès !"
                    )
                )

        else:

            initial = {}

            if societe_cliente.adresse:

                initial = {
                    "rue": societe_cliente.adresse.rue,
                    "numero": societe_cliente.adresse.numero,
                    "code_postal": societe_cliente.adresse.code_postal,
                    "ville": societe_cliente.adresse.ville,
                    "pays": societe_cliente.adresse.pays,
                    "code_pays": societe_cliente.adresse.code_pays,
                }

            form = SocieteClienteForm(
                instance=societe_cliente,
                initial=initial
            )

    return render(
        request,
        "societe_cliente/modifier_societe_cliente.html",
        {
            "form": form,
            "societe_cliente": societe_cliente,
        }
    )
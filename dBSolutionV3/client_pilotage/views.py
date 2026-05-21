from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context, schema_context
from adresse.models import Adresse
from .forms import ClientPilotageForm
from .models import  ClientPilotage
from django.utils.translation import gettext as _
from societe_cliente.models import SocieteCliente
from voiture.voiture_exemplaire.models import VoitureExemplaire
from client_particulier.models import ClientParticulier
from django.db import transaction
from adresse.models import Adresse




@method_decorator([login_required, never_cache], name='dispatch')
class ClientPilotageListView(ListView):
    model = ClientPilotage
    template_name = "client_pilotage/client_pilotage_list.html"
    context_object_name = "clients_pilotages"


    def get_queryset(self):
        societe = self.request.user.societe
        return (
            ClientPilotage.objects
            .select_related("client_particulier")
            .filter(societe=societe)
        )




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

        client_pilotage = get_object_or_404(
            ClientPilotage,
            id=client_pilotage_id,
            societe=tenant
        )

        cp = client_pilotage.client_particulier
        adresse = client_pilotage.adresse

        if request.method == "POST":

            form = ClientPilotageForm(
                request.POST,
                instance=client_pilotage
            )

            if form.is_valid():

                with transaction.atomic():

                    # -----------------------
                    # CLIENT PILOTAGE (base)
                    # -----------------------
                    obj = form.save(commit=False)
                    obj.societe = tenant

                    # -----------------------
                    # CLIENT PARTICULIER
                    # -----------------------
                    cp.prenom = form.cleaned_data.get("prenom")
                    cp.nom = form.cleaned_data.get("nom")
                    cp.email = form.cleaned_data.get("email")
                    cp.numero_telephone = form.cleaned_data.get("numero_telephone")
                    cp.numero_carte_id = form.cleaned_data.get("numero_carte_id")
                    cp.numero_compte = form.cleaned_data.get("numero_compte")
                    cp.numero_carte_bancaire = form.cleaned_data.get("numero_carte_bancaire")
                    cp.date_naissance = form.cleaned_data.get("date_naissance")
                    cp.save()

                    # -----------------------
                    # ADRESSE
                    # -----------------------
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

                    # -----------------------
                    # RELATIONS FINAL
                    # -----------------------
                    obj.client_particulier = cp
                    obj.adresse = adresse
                    obj.save()

                messages.success(
                    request,
                    _(f"Client '{cp.prenom} {cp.nom}' modifié avec succès !")
                )
            else:
                messages.error(
                    request,
                    _("Veuillez corriger les erreurs du formulaire.")
                )

        else:

            initial = {}


            if client_pilotage.client_particulier.date_naissance:
                initial["date_naissance"] = client_pilotage.client_particulier.date_naissance.strftime("%Y-%m-%d")



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

            form = ClientPilotageForm(
                instance=client_pilotage,
                initial=initial
            )

        return render(
            request,
            "client_pilotage/modifier_client_pilotage.html",
            {
                "form": form,
                "client_pilotage": client_pilotage,
                "adresse": adresse,
            }
        )


@login_required
def client_pilotage_form_view(request):

    tenant = request.user.societe

    with tenant_context(tenant):

        if request.method == "POST":

            form = ClientPilotageForm(request.POST)

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
                        date_naissance=form.cleaned_data.get("date_naissance")
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
                    # CLIENT PILOTAGE
                    # -----------------------
                    client_pilotage = form.save(commit=False)
                    client_pilotage.client_particulier = client_particulier
                    client_pilotage.societe = tenant
                    client_pilotage.adresse = adresse
                    client_pilotage.save()

                    form.save_m2m()

                messages.success(
                    request,
                    _(
                        f"Client '{client_particulier.prenom} "
                        f"{client_particulier.nom}' créé avec succès !"
                    )
                )
            else:
                messages.error(
                    request,
                    _("Veuillez corriger les erreurs du formulaire.")
                )

        else:

            form = ClientPilotageForm()

        return render(
            request,
            "client_pilotage/client_pilotage_form.html",
            {
                "form": form,
            }
        )
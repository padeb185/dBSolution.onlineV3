from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from adresse.models import Adresse
from django.utils.translation import gettext as _
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from client_particulier.models import ClientParticulier
from client_particulier.forms import ClientParticulierForm
from adresse.forms import AdresseForm


@method_decorator([login_required, never_cache], name='dispatch')
class ClientParticulierListView(ListView):
    model = ClientParticulier
    template_name = "client_particulier/clientparticulier_list.html"
    context_object_name = "clients"
    paginate_by = 20
    ordering = ["nom", "prenom"]

    def get_queryset(self):
        societe = self.request.user.societe
        return ClientParticulier.objects.filter(societe=societe)


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
def client_particulier_form_view(request):

    tenant = request.user.societe

    with tenant_context(tenant):

        if request.method == "POST":

            form = ClientParticulierForm(request.POST)

            if form.is_valid():

                with transaction.atomic():

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
                    # CLIENT PARTICULIER
                    # -----------------------
                    client_particulier = form.save(commit=False)
                    client_particulier.societe = tenant
                    client_particulier.adresse = adresse
                    client_particulier.save()

                    form.save_m2m()

                messages.success(
                    request,
                    _(
                        f"Client '{client_particulier.prenom} "
                        f"{client_particulier.nom}' créé avec succès !"
                    )
                )

                return redirect("client_particulier_list")

            else:
                messages.error(
                    request,
                    _("Veuillez corriger les erreurs du formulaire.")
                )

        else:
            form = ClientParticulierForm()

        return render(
            request,
            "client_particulier/client_form.html",
            {
                "form": form,
            }
        )





@login_required
def modifier_client_particulier_view(request, client_particulier_id):

    tenant = request.user.societe

    with tenant_context(tenant):

        client_particulier = get_object_or_404(
            ClientParticulier,
            id=client_particulier_id,
            societe=tenant
        )

        cp = client_particulier
        adresse = client_particulier.adresse

        if request.method == "POST":

            form = ClientParticulierForm(
                request.POST,
                instance=client_particulier
            )

            if form.is_valid():

                with transaction.atomic():

                    obj = form.save(commit=False)

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

                        adresse = Adresse.objects.create(
                            societe=tenant
                        )

                    adresse.rue = form.cleaned_data.get("rue")
                    adresse.numero = form.cleaned_data.get("numero")
                    adresse.boite = form.cleaned_data.get("boite")
                    adresse.code_postal = form.cleaned_data.get("code_postal")
                    adresse.ville = form.cleaned_data.get("ville")
                    adresse.pays = form.cleaned_data.get("pays")
                    adresse.code_pays = form.cleaned_data.get("code_pays")

                    adresse.save()

                    # -----------------------
                    # CLIENT PILOTAGE
                    # -----------------------
                    obj.client_particulier = cp
                    obj.adresse = adresse
                    obj.societe = tenant
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

            if adresse:
                initial = {
                    "rue": adresse.rue,
                    "numero": adresse.numero,
                    "boite": adresse.boite,
                    "code_postal": adresse.code_postal,
                    "ville": adresse.ville,
                    "pays": adresse.pays,
                    "code_pays": adresse.code_pays,
                }

            form = ClientParticulierForm(
                instance=client_particulier,
                initial=initial
            )

        return render(
            request,
            "client_particulier/modifier_client_particulier.html",
            {
                "form": form,
                "client_particulier": client_particulier,
                "adresse": adresse,
            }
        )





@csrf_exempt  # facultatif si CSRF bien géré côté JS
def check_prenom(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prenom = data.get("prenom")

        try:
            client = ClientParticulier.objects.select_related("adresse").get(prenom__iexact=prenom)

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

        except ClientParticulier.DoesNotExist:
            return JsonResponse({"exist": False})

    return JsonResponse({"error": "Invalid request"}, status=400)
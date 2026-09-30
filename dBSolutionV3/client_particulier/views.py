import client_particulier
from core.suppression import analyser_suppression
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from adresse.models import Adresse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from client_particulier.forms import ClientParticulierForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import router, transaction
from django.db.models import ProtectedError, RestrictedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _, gettext_noop
from utilisateurs.models import UserLog

from .models import ClientParticulier







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

    client_particulier = None

    if request.method == "POST":
        form = ClientParticulierForm(request.POST)

        if form.is_valid():
            with transaction.atomic():

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

                client_particulier = form.save(commit=False)
                client_particulier.societe = tenant
                client_particulier.adresse = adresse
                client_particulier.save()

                form.save_m2m()

            messages.success(
                request,
                _(
                    f"Client '{client_particulier.prenom} "
                    f"{client_particulier.nom}' créé avec succès ! "
                    f"Âge : {client_particulier.age} ans"
                )
            )
            return redirect(
                f"{reverse('client_particulier:clientparticulier_list')}?saved=1"
            )

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
            "client_particulier": client_particulier,
        }
    )


@login_required
def modifier_client_particulier_view(request, client_particulier_id):

    tenant = request.user.societe

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
                # CLIENT PARTICULIER
                # -----------------------
                obj.client_particulier = cp
                obj.adresse = adresse
                obj.societe = tenant
                obj.save()

            messages.success(
                request,
                _(f"Client '{cp.prenom} {cp.nom}' modifié avec succès !")
            )

            return redirect(
                f"{reverse('client_particulier:client_detail', kwargs={'client_particulier_id': client_particulier.id})}?saved=1"
            )

        else:
            messages.error(
                request,
                _("Veuillez corriger les erreurs du formulaire.")
            )

    else:
        initial = {}

        if client_particulier.date_naissance:
            initial["date_naissance"] = client_particulier.date_naissance.strftime("%Y-%m-%d")

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









def _masquer(valeur, visibles=4):
    """Masque une donnée sensible : ne garde que les derniers caractères."""
    if not valeur:
        return None
    valeur = str(valeur).replace(" ", "")
    if len(valeur) <= visibles:
        return "•" * len(valeur)
    return "•" * (len(valeur) - visibles) + valeur[-visibles:]









ACTION_SUPPRESSION_CLIENT = gettext_noop("Suppression du client particulier")


def _masquer(valeur, visibles=4):
    """Masque une donnée sensible : ne garde que les derniers caractères."""
    if not valeur:
        return None
    valeur = str(valeur).replace(" ", "")
    if len(valeur) <= visibles:
        return "•" * len(valeur)
    return "•" * (len(valeur) - visibles) + valeur[-visibles:]


@login_required
def delete_client_view(request, pk):
    client = get_object_or_404(
        ClientParticulier.objects.select_related("adresse", "societe"),
        pk=pk,
    )

    analyse = analyser_suppression(client)
    objets_bloquants = analyse["bloquants"]
    objets_supprimes = analyse["supprimes"]

    if request.method == "POST":
        nom_complet = f"{client.prenom} {client.nom}"

        # Libellé pour le log (capturé AVANT la suppression)
        nom_log = f"{client.nom} {client.prenom}"
        if client.email:
            nom_log += f" ({client.email})"

        if objets_bloquants:
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : ce client est encore utilisé ailleurs.") % {"nom": nom_complet},
            )
            return redirect("client_particulier:delete_client", pk=pk)

        try:
            with transaction.atomic():
                adresse = client.adresse
                client.delete()
                # OneToOne : l'adresse n'appartient qu'à ce client → on la supprime aussi
                if adresse:
                    adresse.delete()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_CLIENT} : {nom_log}",
                )
        except (ProtectedError, RestrictedError):
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : ce client est encore utilisé ailleurs.") % {"nom": nom_complet},
            )
            return redirect("client_particulier:delete_client", pk=pk)

        messages.success(request, _("Le client « %(nom)s » a bien été supprimé.") % {"nom": nom_complet})

        return redirect(
            f"{reverse('client_particulier:clientparticulier_list')}?deleted=1"
        )

    return render(
        request,
        "client_particulier/delete_client.html",
        {
            "client": client,
            "objets_supprimes": objets_supprimes,
            "objets_bloquants": objets_bloquants,
            # Données sensibles masquées pour l'affichage
            "compte_masque": _masquer(client.numero_compte),
            "carte_bancaire_masquee": _masquer(client.numero_carte_bancaire),
            "carte_id_masquee": _masquer(client.numero_carte_id, 3),
            "registre_national_masque": _masquer(client.numero_registre_national, 3),
        },
    )
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import  ListView
from django_tenants.utils import tenant_context, schema_context
from .models import Fournisseur
from .forms import FournisseurForm
from adresse.models import Adresse
from django.utils.translation import gettext as _
from achat_mds.models import AchatMds
from django.http import JsonResponse
from django.views.decorators.http import require_POST





@method_decorator([login_required, never_cache], name='dispatch')
class FournisseurListView(ListView):
    model = Fournisseur
    template_name = "fournisseur/fournisseur_list.html"
    context_object_name = "fournisseurs"
    ordering = ["nom"]

    def get_queryset(self):
        tenant = self.request.user.societe
        return Fournisseur.objects.filter(societe=tenant)




@never_cache
@login_required
def fournisseur_detail(request, fournisseur_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
        adresse = fournisseur.adresse

    return render(
        request,
        "fournisseur/fournisseur_detail.html",
        {
            "fournisseur": fournisseur,
            "adresse": adresse,
        },
    )





@login_required
def liste_fournisseur_all(request):
    tenant = request.user.societe  # le tenant de l'utilisateur

    with tenant_context(tenant):
        # Récupérer tous les fournisseurs liés à ce tenant
        fournisseurs = Fournisseur.objects.filter(societe=tenant).order_by('id')

    return render(
        request,
        'fournisseur/fournisseur_list.html',
        {'fournisseurs': fournisseurs}
    )


@login_required
def ajouter_fournisseur_all(request):
    tenant = request.user.societe

    if request.method == "POST":
        form_fournisseur = FournisseurForm(request.POST)

        if form_fournisseur.is_valid():
            rue = form_fournisseur.cleaned_data.get("rue")
            numero = form_fournisseur.cleaned_data.get("numero")
            boite = form_fournisseur.cleaned_data.get("boite")
            code_postal = form_fournisseur.cleaned_data.get("code_postal")
            ville = form_fournisseur.cleaned_data.get("ville")
            pays = form_fournisseur.cleaned_data.get("pays") or "Belgique"
            code_pays = form_fournisseur.cleaned_data.get("code_pays") or "BE"

            if not all([rue, numero, code_postal, ville]):
                messages.error(
                    request,
                    _("Les champs d'adresse sont obligatoires.")
                )
            else:
                with transaction.atomic():
                    adresse = Adresse.objects.create(
                        rue=rue,
                        numero=numero,
                        boite=boite,
                        code_postal=code_postal,
                        ville=ville,
                        pays=pays,
                        code_pays=code_pays,
                        societe=tenant,
                    )

                    fournisseur = form_fournisseur.save(commit=False)
                    fournisseur.adresse_id = adresse.id
                    fournisseur.societe = tenant
                    fournisseur.save()

                    messages.success(
                        request,
                        _(f"Fournisseur '{fournisseur.nom}' créé avec succès !"))
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form_fournisseur = FournisseurForm()

    return render(request, "fournisseur/fournisseur_form.html", {
        "form": form_fournisseur,
    })




@login_required
def modifier_fournisseur(request, fournisseur_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)

        if request.method == "POST":
            form = FournisseurForm(request.POST, instance=fournisseur)
            if form.is_valid():
                form.save()
                messages.success(request, _(f"Fournisseur '{fournisseur.nom}' modifié avec succès !"))


        else:
            form = FournisseurForm(instance=fournisseur)

    return render(
        request,
        "fournisseur/modifier_fournisseur.html",
        {
            "form": form,
            "fournisseur": fournisseur,
        }
    )


@never_cache
@login_required
def fournisseur_dashboard_view(request):
    tenant = request.user.societe
    user = request.user
    societe = user.societe

    with tenant_context(tenant):


        fournisseurs = Fournisseur.objects.all()
        achat_mds = AchatMds.objects.all()

        total_fournisseur = fournisseurs.count()
        total_achat = achat_mds.count()

        context = {
            "user": user,
            "societe": societe,
            "total_fournisseur": total_fournisseur,
            "total_achat": total_achat,
            "fournisseurs": fournisseurs,
        }

    return render(request, "fournisseur/fournisseur_dashboard.html", context)






@login_required
@require_POST
def check_nom_fournisseur_view(request):
    try:
        tenant = request.user.societe

        # 👇 valeur envoyée par le JS
        nom = request.POST.get("nom_marque", "").strip()

        if not nom:
            return JsonResponse({"exists": False})

        # 👇 contrôle dans TON modèle Fournisseur
        exists = Fournisseur.objects.filter(
            societe=tenant,
            nom__iexact=nom
        ).exists()

        return JsonResponse({
            "exists": exists
        })

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

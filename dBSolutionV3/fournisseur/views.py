from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, ListView
from django_tenants.utils import tenant_context
from .models import Fournisseur
from .forms import FournisseurForm
from adresse.forms import AdresseForm
from adresse.models import Adresse



class FournisseurListView(ListView):
    model = Fournisseur
    template_name = "fournisseurs/fournisseur_list.html"
    context_object_name = "fournisseurs"
    paginate_by = 20
    ordering = ["nom"]






@never_cache
@login_required
def fournisseur_detail(request, fournisseur_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
        adresse = fournisseur.adresse

    return render(
        request,
        "fournisseurs/fournisseur_detail.html",
        {
            "fournisseur": fournisseur,
            "adresse": adresse,
        },
    )







@login_required
def liste_fournisseur_all(request):
    tenant = request.user.societe

    try:
        with tenant_context(tenant):
            fournisseurs = Fournisseur.objects.select_related(
                'nom', 'numero_tva'
            ).all().order_by('id')
    except Exception as e:
        # En cas d'erreur (rare), on affiche un message
        messages.error(request, f"Erreur lors de la récupération des fournisseurs : {e}")
        fournisseurs = []

    return render(
        request,
        'fournisseur/fournisseur_list.html',
        {'fournisseurs': fournisseurs}  # pluriel plus clair
    )






@login_required
def ajouter_fournisseur_all(request):
    fournisseur = Fournisseur()
    fournisseur.adresse = Adresse()

    if request.method == "POST":
        nom = request.POST.get("fournisseur")


        if not nom:
            messages.error(request, "Le nom du fournisseur est obligatoire.")
        else:
            adresse = Adresse.objects.create(
                rue=request.POST.get("rue"),
                numero=request.POST.get("numero"),
                code_postal=request.POST.get("code_postal"),
                ville=request.POST.get("ville"),
                pays=request.POST.get("pays"),
                code_pays=request.POST.get("code_pays")
            )
            fournisseur = Fournisseur.objects.create(
                nom=nom,
                numero_tva=request.POST.get("numero_tva"),
                taux_tva=request.POST.get("taux_tva") or 0,
                peppol_id=request.POST.get("peppol_id"),
                email=request.POST.get("email"),
                telephone_fixe=request.POST.get("telephone_fixe"),
                gsm=request.POST.get("gsm"),
                adresse=adresse
            )
            messages.success(request, f"Fournisseur '{fournisseur.nom}' ajouté avec succès !")
            return redirect("fournisseur:fournisseur_list")

    # S'assurer que fournisseur.adresse existe
    if not hasattr(fournisseur, "adresse") or fournisseur.adresse is None:
        fournisseur.adresse = Adresse()

    return render(request, "fournisseurs/fournisseur_form.html", {"fournisseur": fournisseur})




@login_required
def modifier_fournisseur(request, fournisseur_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)

        if request.method == "POST":
            form = FournisseurForm(request.POST, instance=fournisseur)
            if form.is_valid():
                form.save()
                messages.success(request, "Fournisseur mis à jour avec succès.")
                return redirect(
                    'fournisseur:modifier_fournisseur',
                    fournisseur_id=fournisseur.id
                )
        else:
            form = FournisseurForm(instance=fournisseur)

    return render(
        request,
        "fournisseurs/modifier_fournisseur.html",
        {
            "form": form,
            "fournisseur": fournisseur,
        }
    )

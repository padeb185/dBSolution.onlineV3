from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import  ListView
from django_tenants.utils import tenant_context, schema_context
from .models import Fournisseur, Achat
from .forms import FournisseurForm, AchatForm
from adresse.forms import AdresseForm
from adresse.models import Adresse
from django.utils.translation import gettext as _
from societe.models import Societe



@method_decorator([login_required, never_cache], name='dispatch')
class FournisseurListView(ListView):
    model = Fournisseur
    template_name = "fournisseur/fournisseur_list.html"
    context_object_name = "fournisseurs"
    paginate_by = 20
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

    with tenant_context(tenant):
        fournisseur = Fournisseur()
        fournisseur.adresse = Adresse()

        if request.method == "POST":
            nom = request.POST.get("fournisseur")

            if not nom:
                messages.error(request, _("Le nom du fournisseur est obligatoire."))
            else:
                # Crée l'adresse avec le tenant
                adresse = Adresse.objects.create(
                    societe=tenant,  # <-- ici
                    rue=request.POST.get("rue"),
                    numero=request.POST.get("numero"),
                    boite=request.POST.get("boite"),
                    code_postal=request.POST.get("code_postal"),
                    ville=request.POST.get("ville"),
                    pays=request.POST.get("pays"),
                    code_pays=request.POST.get("code_pays")
                )

                # Crée le fournisseur avec le tenant
                fournisseur = Fournisseur.objects.create(
                    societe=tenant,  # <-- ici aussi
                    nom=nom,
                    numero_tva=request.POST.get("numero_tva"),
                    taux_tva=request.POST.get("taux_tva") or 0,
                    peppol_id=request.POST.get("peppol_id"),
                    email=request.POST.get("email"),
                    telephone_fixe=request.POST.get("telephone_fixe"),
                    gsm=request.POST.get("gsm"),
                    adresse=adresse
                )

                messages.success(request, _(f"Fournisseur '{fournisseur.nom}' ajouté avec succès !"))

        # S'assurer que fournisseur.adresse existe
        if not hasattr(fournisseur, "adresse") or fournisseur.adresse is None:
            fournisseur.adresse = Adresse()

        return render(
            request,
            "fournisseur/fournisseur_form.html",
            {"fournisseur": fournisseur}
        )



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

        total_fournisseur = fournisseurs.count()

        context = {
            "user": user,
            "societe": societe,
            "total_fournisseur": total_fournisseur,
            "fournisseurs": fournisseurs,
        }

    return render(request, "fournisseur/fournisseur_dashboard.html", context)



@login_required
def fournisseur_achat_view(request):
    tenant = request.user.societe

    with tenant_context(tenant):

        fournisseurs = Fournisseur.objects.all()

        if request.method == "POST":
            form = AchatForm(request.POST)

            if form.is_valid():
                achat = form.save(commit=False)
                achat.save()
                messages.success(request, "Achat enregistré avec succès")


        else:
            form = AchatForm()

        return render(request, "fournisseur/fournisseur_achat.html", {
            "form": form,
            "fournisseurs": fournisseurs,

        })


@method_decorator([login_required, never_cache], name='dispatch')
class AchatMdsListView(ListView):
    model = Achat
    template_name = "fournisseur/achat_list.html"
    context_object_name = "achats"
    paginate_by = 20
    ordering = ["nom"]

    def get_queryset(self):
        tenant = self.request.user.societe
        return Achat.objects.filter(societe=tenant)


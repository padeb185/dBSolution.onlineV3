# adresse/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from .forms import AdresseForm
from .models import adresse
from adresse.models import Adresse
from django.utils.translation import gettext as _



@method_decorator([login_required, never_cache], name='dispatch')
class AdresseListView(ListView):
    model = adresse
    template_name = "adresse/adresse_list.html"
    context_object_name = "adresses"
    paginate_by = 20
    ordering = ["nom_societe"]







@login_required
def adresse_detail(request, adresse_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        adresse = get_object_or_404(Adresse, id=adresse_id)
        adresse = adresse.adresse

    return render(
        request,
        "adresse/adresse_detail.html",
        {
            "adresse": adresse,
        },
    )




@login_required
def ajouter_adresse_all(request):
    adresse = Adresse()
    adresse.adresse = Adresse()

    if request.method == "POST":
        nom_societe = request.POST.get("adresse")


        if not nom_societe:
            messages.error(request, _("Le nom de la adresse est obligatoire."))
        else:
            adresse = Adresse.objects.create(
                rue=request.POST.get("rue"),
                numero=request.POST.get("numero"),
                code_postal=request.POST.get("code_postal"),
                ville=request.POST.get("ville"),
                pays=request.POST.get("pays"),
                code_pays=request.POST.get("code_pays")
            )

            messages.success(request, _(f"Adresse '{adresse.rue}, {adresse.code_postal}' ajoutée avec succès !"))



    # S'assurer que fournisseur.adresse existe
    if not hasattr(adresse, "adresse") or adresse.adresse is None:
        adresse.adresse = Adresse()

    return render(request, "adresse/adresse_form.html", {"adresse":adresse})




@login_required
def modifier_adresse(request, adresse_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        adresse = get_object_or_404(Adresse, id=adresse_id)

        if request.method == "POST":
            form = AdresseForm(request.POST, instance=adresse)
            if form.is_valid():
                form.save()
                messages.success(request, _(f"Adresse '{adresse.rue}, {adresse.code_postal}' modifiée avec succès !"))

        else:
            form = AdresseForm(instance=adresse)

    return render(
        request,
        "adresse/modifier_adresse.html",
        {
            "form": form,
            "adresse": adresse,
        }
    )





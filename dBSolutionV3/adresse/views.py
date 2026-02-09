# adresse/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from .forms import AdresseForm
from adresse.models import Adresse
from django.utils.translation import gettext as _
from .models import Adresse


@method_decorator([login_required, never_cache], name='dispatch')
class AdresseListView(ListView):
    model = Adresse
    template_name = "adresse/adresse_list.html"
    context_object_name = "adresses"
    paginate_by = 20
    ordering = ["rue"]

    def get_queryset(self):
        tenant = self.request.user.societe
        return Adresse.objects.filter(societe=tenant)





@never_cache
@login_required
def adresse_detail(request, adresse_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        adresse = get_object_or_404(
            Adresse,
            id=adresse_id,
            societe=tenant
        )


    return render(
        request,
        "adresse/adresse_detail.html",
        {
            "adresse": adresse,
        },
    )





@login_required
def ajouter_adresse_all(request):
    tenant = request.user.societe

    if request.method == "POST":
        rue = request.POST.get("rue")

        if not rue:
            messages.error(request, _("Le nom de la rue est obligatoire."))
        else:
            try:
                adresse = Adresse.objects.create(
                    societe=tenant,
                    rue=request.POST.get("rue"),
                    numero=request.POST.get("numero"),
                    boite=request.POST.get("boite"),
                    code_postal=request.POST.get("code_postal"),
                    ville=request.POST.get("ville"),
                    pays=request.POST.get("pays"),
                    code_pays=request.POST.get("code_pays")
                )

                messages.success(
                    request,
                    _(f"Adresse '{adresse.rue}, {adresse.code_postal}' ajoutée avec succès !")
                )
            except (IntegrityError, ValidationError):
                messages.error(request, _("Cette adresse existe déjà pour cette société."))

    return render(request, "adresse/adresse_form.html")


@login_required
def modifier_adresse(request, adresse_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        adresse = get_object_or_404(
            Adresse,
            id=adresse_id,
            societe=tenant
        )

        if request.method == "POST":
            form = AdresseForm(request.POST, instance=adresse)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    _("Adresse '%(rue)s, %(cp)s' modifiée avec succès !") % {
                        "rue": adresse.rue,
                        "cp": adresse.code_postal
                    }
                )
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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, ListView
from django_tenants.utils import tenant_context
from .models import Fournisseur
from .forms import FournisseurForm


class FournisseurCreateView(CreateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = "fournisseurs/fournisseur_form.html"
    success_url = reverse_lazy("fournisseur_list")  # adapte si besoin




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

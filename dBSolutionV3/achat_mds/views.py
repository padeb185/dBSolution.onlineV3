from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context
from achat_mds.forms import AchatForm
from achat_mds.models import AchatMds
from fournisseur.models import Fournisseur
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required





@login_required
def achat_mds_view(request):
    tenant = request.user.societe

    with tenant_context(tenant):

        # 🔒 IMPORTANT : filtrer par tenant
        fournisseurs = Fournisseur.objects.filter(societe=tenant)
        achat_mds = AchatMds.objects.filter(societe=tenant)

        if request.method == "POST":
            form = AchatForm(request.POST)

            if form.is_valid():
                achat = form.save(commit=False)
                achat.societe = tenant  # sécurité multi-tenant
                achat.save()

                messages.success(request, "Achat enregistré avec succès")

                return redirect("achat_mds:achat_form")  # PRG pattern

        else:
            form = AchatForm()

        return render(request, "achat_mds/achat_form.html", {
            "form": form,
            "achat_mds": achat_mds,
            "fournisseurs": fournisseurs,
        })




@method_decorator([login_required, never_cache], name='dispatch')
class AchatMdsListView(ListView):
    model = AchatMds
    template_name = "achat_mds/achat_list.html"
    context_object_name = "achats"
    paginate_by = 20
    ordering = ["nom"]

    def get_queryset(self):
        tenant = self.request.user.societe
        return AchatMds.objects.filter(societe=tenant)






@never_cache
@login_required
def achat_detail_view(request, achat_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        achat = get_object_or_404(
            AchatMds,
            id=achat_id,
            societe=tenant   # 🔒 IMPORTANT sécurité multi-tenant
        )

        fournisseurs = Fournisseur.objects.filter(societe=tenant)

        return render(
            request,
            "achat_mds/achat_detail.html",
            {
                "achat": achat,
                "fournisseurs": fournisseurs,
            },
        )



@login_required
def modifier_achat_view(request, achat_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        achat = get_object_or_404(AchatMds, id=achat_id)
        fournisseurs = Fournisseur.objects.filter(societe=tenant)

        if request.method == "POST":
            form = AchatForm(request.POST, instance=achat)
            if form.is_valid():
                form.save()
                messages.success(request, _("Achat modifié avec succès !"))


        else:
            form = AchatForm(instance=achat)

    return render(
        request,
        "achat_mds/modifier_achat_mds.html",
        {
            "form": form,
            "fournisseurs": fournisseurs,
            "achat": achat,
        }
    )





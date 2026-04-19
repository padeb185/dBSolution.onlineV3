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



@login_required
def achat_mds_view(request):
    tenant = request.user.societe

    with tenant_context(tenant):

        if request.method == "POST":
            form = AchatForm(request.POST)

            if form.is_valid():
                achat = form.save(commit=False)
                achat.societe = tenant
                achat.save()
                messages.success(request, "Achat enregistré avec succès")


        else:
            form = AchatForm()

        achat_mds = AchatMds.objects.filter(societe=tenant)

        return render(request, "achat_mds/achat_form.html", {
            "form": form,
            "achat_mds": achat_mds,
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
def achat_detail_view(request, achat_mds_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        achat_mds = get_object_or_404(AchatMds, id=achat_mds_id)


    return render(
        request,
        "achat_mds/achat_detail.html",
        {
            "achat_mds": achat_mds,

        },
    )


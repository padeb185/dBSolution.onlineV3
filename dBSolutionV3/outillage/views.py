from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from outillage.models import Outillage
from outillage.forms import OutillageForm



@method_decorator([login_required, never_cache], name='dispatch')
class OutillageListView(ListView):
    model = Outillage
    template_name = "outillage/outillage_list.html"
    context_object_name = "outillages"
    paginate_by = 20
    ordering = ["nom"]

    def get_queryset(self):
        societe = self.request.user.societe
        return Outillage.objects.filter(societe=societe)




@login_required
def outillage_detail(request, outillage_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        outillage = get_object_or_404(Outillage, id_outillage=outillage_id)


    return render(
        request,
        "outillage/outillage_detail.html",
        {
            "outillage": outillage,
        },
    )




@login_required
def ajouter_outillage_all(request):
    tenant = request.user.societe

    if request.method == "POST":
        form_outillage = OutillageForm(request.POST)

        if form_outillage.is_valid():
                # Création outillage
                outillage = form_outillage.save(commit=False)
                outillage.societe = tenant
                outillage.save()

                messages.success(
                    request,
                    f"Outillage '{outillage.libelle}' créée avec succès !"
                )

        else:
            messages.error(request, "Le formulaire contient des erreurs.")

    else:
        form_outillage = OutillageForm()

    return render(request, "outillage/outillage_form.html", {
                "form": form_outillage
    })



@login_required
def modifier_outillage(request, outillage_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupérer l'outillage par son vrai champ PK : id_outillage
        outillage = get_object_or_404(
            Outillage,
            id_outillage=outillage_id
        )

        if request.method == "POST":
            form_outillage = OutillageForm(request.POST, instance=outillage)

            if form_outillage.is_valid():
                form_outillage.save()
                messages.success(request, "Outillage mis à jour avec succès.")
                # Rediriger vers la page de détail de l'outillage
                return redirect("outillage:outillage_detail", outillage_id=outillage.id_outillage)
            else:
                messages.error(request, "Le formulaire contient des erreurs.")
        else:
            form_outillage = OutillageForm(instance=outillage)

    return render(
        request,
        "outillage/modifier_outillage.html",
        {
            "form": form_outillage,
            "outillage": outillage,
        }
    )
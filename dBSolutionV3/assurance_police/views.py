from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from .forms import AssurancePoliceForm
from .models import AssurancePolice, Sinistre



@login_required
def dashboard_assurances(request):
    today = timezone.now().date()
    in_30_days = today + timedelta(days=30)

    polices_actives = AssurancePolice.objects.filter(actif=True).count()
    polices_expirees = AssurancePolice.objects.filter(date_fin__lt=today).count()
    polices_bientot = AssurancePolice.objects.filter(date_fin__range=(today, in_30_days)).count()

    sinistres_ouverts = Sinistre.objects.filter(cloture=False).count()

    cout_total = AssurancePolice.cout_total_annuel()

    context = {
        'polices_actives': polices_actives,
        'polices_expirees': polices_expirees,
        'polices_bientot': polices_bientot,
        'sinistres_ouverts': sinistres_ouverts,
        'cout_total': cout_total,
    }

    return render(request, 'assurance_police/dashboard.html', context)



@method_decorator([login_required, never_cache], name='dispatch')
class AssurancePoliceListView(ListView):
    model = AssurancePolice
    template_name = "assurance_police/assurance_police_list.html"
    context_object_name = "assurance_polices"



@login_required
def ajouter_assurance_all(request):
    tenant = request.user.societe  # si tu utilises tenant

    if request.method == "POST":
        form_assurance_police = AssurancePoliceForm(request.POST)
        if form_assurance_police.is_valid():
            assurance_police = form_assurance_police.save(commit=False)
            # tu peux ajouter tenant ou autre info ici si nécessaire
            # assurance_police.societe = tenant
            assurance_police.save()
            messages.success(
                request,
                f"Assurance '{assurance_police.assurance.nom_compagnie}' créée avec succès !"
            )
            return redirect('assurance_police:assurance_police_list')  # redirection après succès
        else:
            messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form_assurance_police = AssurancePoliceForm()

    return render(request, "assurance_police/assurance_police_form.html", {
        "form": form_assurance_police
    })



@login_required
def assurance_police_detail(request, assurance_police_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        assurance_police = get_object_or_404(AssurancePolice, id=assurance_police_id)


    return render(
        request,
        "assurance_police/assurance_police_detail.html",
        {
            "assurance_police": assurance_police,

        },
    )





@login_required
def modifier_assurance_police(request, assurance_police_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        assurance_police = get_object_or_404(
            AssurancePolice,
            pk=assurance_police_id
        )

        if request.method == "POST":
            form = AssurancePoliceForm(
                request.POST,
                request.FILES,
                instance=assurance_police
            )

            if form.is_valid():
                assurance_police = form.save()
                messages.success(request, "Police d'assurance mise à jour avec succès.")

            else:
                messages.error(request, "Le formulaire contient des erreurs.")
        else:
            form = AssurancePoliceForm(instance=assurance_police)

    return render(
        request,
        "assurance_police/modifier_assurance_police.html",
        {
            "form": form,
            "assurance_police": assurance_police,
        }
    )

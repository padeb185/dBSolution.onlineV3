from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context, schema_context
from django.shortcuts import render
from ..voiture_freins_av.models import VoitureFreinsAV
from .forms import VoitureFreinsAVForm
from ..voiture_freins_ar.models import VoitureFreinsAR
from ..voiture_modele.models import VoitureModele
from societe.models import Societe
from django.utils.translation import gettext_lazy as _




@never_cache
@login_required
def liste_freins_av(request, societe_id=None):
    # Si societe_id est passé, on l'utilise ; sinon on prend celle de l'utilisateur
    societe = request.user.societe
    if societe_id:
        societe = Societe.objects.get(id=societe_id)

    with tenant_context(societe):
        freins = VoitureFreinsAV.objects.filter(societe=societe)

    return render(request, "voiture_freins_av/freins_av_list.html", {"freins": freins, "societe": societe})





@never_cache
@login_required
def freins_av_detail_view(request, frein_av_id):
    frein = get_object_or_404(VoitureFreinsAV, id=frein_av_id)
    return render(request, 'voiture_freins_av/freins_av_detail.html', {
        'frein': frein,
    })





@login_required
def ajouter_freins_av_simple(request):
    tenant = request.user.societe

    with tenant_context(tenant):

        def to_float(value):
            if not value:
                return None
            return float(value.replace(',', '.'))

        if request.method == "POST":
            form = VoitureFreinsAVForm(request.POST)

            if form.is_valid():
                obj = form.save(commit=False)
                obj.societe = tenant
                obj.save()

                messages.success(request, "Freins avant ajoutés avec succès !")
                return redirect("voiture_freins_av:freins_av_list")

        else:
            form = VoitureFreinsAVForm()

        return render(request, "voiture_freins_av/ajouter_freins_simple.html", {
            "form": form
        })


@login_required
def modifier_freins_av_view(request, frein_av_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        freins = get_object_or_404(VoitureFreinsAV, id=frein_av_id)

        if request.method == "POST":
            form_frein = VoitureFreinsAVForm(request.POST, instance=freins)

            if form_frein.is_valid():
                frein = form_frein.save()  # commit=False inutile ici

                messages.success(request, _("Freins avant mis à jour avec succès."))
                return redirect(
                    "voiture_freins_av:modifier_freins_av",
                    frein_av_id=frein.id   # ✅ match URL
                )
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
        else:
            form_frein = VoitureFreinsAVForm(instance=freins)

    return render(
        request,
        "voiture_freins_av/modifier_freins_av.html",
        {
            "form": form_frein,
            "frein": freins,   # ✅ utilisé dans template
        }
    )


@never_cache
@login_required
def dashboard_frein_view(request):
    user = request.user
    societe = user.societe
    context = {}

    # --- Sécurité : récupère le tenant (la société de l'utilisateur) ---
    societe = request.user.societe
    schema_name = societe.schema_name  # pour django-tenants


    # --- Stats initialisées à zéro ---
    total_freins = 0
    total_freins_ar = 0


    freins = freins_ar = []

    if schema_name:
        with schema_context(schema_name):

            freins = VoitureFreinsAV.objects.filter(societe=societe)
            freins_ar = VoitureFreinsAR.objects.filter(societe=societe)


            # Totaux
            total_freins = freins.count()
            total_freins_ar = freins_ar.count()

    else:
        freins = []

    context.update({
        'user': user,
        'societe': societe,

        'total_freins': total_freins,
        'total_freins_ar': total_freins_ar,



        'freins': freins,
        'freins_ar': freins_ar,

    })

    return render(request, "voiture_freins_av/dashboard_frein.html", context)



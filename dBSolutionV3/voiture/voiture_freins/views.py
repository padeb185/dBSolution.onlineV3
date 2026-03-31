from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context, schema_context
from django.shortcuts import render
from ..voiture_freins.models import VoitureFreins
from .forms import VoitureFreinsForm
from ..voiture_freins_ar.models import VoitureFreinsAR
from ..voiture_modele.models import VoitureModele



@login_required
def ajouter_freins_all(request, modele_id):
    tenant = request.user.societe
    with tenant_context(tenant):
        # Récupère le modèle
        modele = get_object_or_404(VoitureModele, id=modele_id)
        marque = modele.voiture_marque  # objet VoitureMarque

        if request.method == "POST":
            form = VoitureFreinsForm(request.POST)
            if form.is_valid():
                exemplaire = form.save(commit=False)
                exemplaire.voiture_modele = modele
                exemplaire.voiture_marque = marque
                exemplaire.save()
                messages.success(request, "Freins avant ajoutés avec succès !")

            else:
                messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
        else:
            # GET → formulaire pré-rempli avec la marque et le modèle
            form = VoitureFreinsForm(initial={
                "voiture_marque": marque.pk,
                "voiture_modele": modele.id
            })

        return render(request, "voiture_freins/ajouter_freins_simple.html", {
            "form": form,
            "modele": modele
        })



@never_cache
@login_required
def liste_freins(request, societe_id=None):
    # Si societe_id est passé, on l'utilise ; sinon on prend celle de l'utilisateur
    societe = request.user.societe
    if societe_id:
        from societe.models import Societe  # ou ton modèle de sociétés
        societe = Societe.objects.get(id=societe_id)

    with tenant_context(societe):
        freins = VoitureFreins.objects.filter(societe=societe)

    return render(request, "voiture_freins/list.html", {"freins": freins, "societe": societe})






@login_required()
def freins_detail_view(request, frein_id):
    frein = get_object_or_404(VoitureFreins, id=frein_id)
    return render(request, 'voiture_freins/freins_detail.html', {
        'frein': frein,
    })






@login_required
def ajouter_freins_simple(request):
    tenant = request.user.societe
    with tenant_context(tenant):

        if request.method == "POST":

            def to_float(value):
                if not value:  # vide → None
                    return None
                return float(value.replace(',', '.'))  # transforme 20,4 → 20.4

            VoitureFreins.objects.create(
                societe=tenant,
                marque_disques_av=request.POST.get("marque_disques_av"),
                marque_plaquettes_av=request.POST.get("marque_plaquettes_av"),
                taille_disque_av=to_float(request.POST.get("taille_disque_av")),
                epaisseur_disque_av=to_float(request.POST.get("epaisseur_disque_av")),
                epaisseur_min_disque_av=to_float(request.POST.get("epaisseur_min_disque_av")),
            )
            messages.success(request, "Freins avant ajoutés avec succès !")


        return render(request, "voiture_freins/ajouter_freins_simple.html")




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

            freins = VoitureFreins.objects.filter(societe=societe)
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

    return render(request, "voiture_freins/dashboard_frein.html", context)



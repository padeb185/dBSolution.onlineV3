from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django_tenants.utils import tenant_context
from django.shortcuts import render
from voiture.voiture_freins.forms import VoitureFreinsForm
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_freins.models import VoitureFreins
from voiture.voiture_exemplaire.models import VoitureExemplaire




@login_required
def ajouter_freins_simple(request):
    """
    Vue pour ajouter un frein avant simple.
    - GET : affiche le formulaire.
    - POST : crée un frein puis redirige vers la liste.
    """
    try:
        if request.method == "POST":
            VoitureFreins.objects.create(
                marque_disque_av=request.POST.get("marque_disque_av", ""),
                marque_plaquettes_av=request.POST.get("marque_plaquettes_av", ""),
                taille_disque_av=request.POST.get("taille_disque_av", ""),
                epaisseur_disque_av=request.POST.get("epaisseur_disque_av", ""),
                epaisseur_min_disque_av=request.POST.get("epaisseur_min_disque_av", ""),
            )
            messages.success(request, "Freins avant ajoutés avec succès.")
            return redirect("voiture_freins:list")
    except Exception as e:
        # Affiche l'erreur dans les messages pour debug
        messages.error(request, f"Erreur lors de l'ajout : {e}")

    # GET ou en cas d'erreur → retourne toujours un HttpResponse
    return render(request, "voiture_freins/ajouter_freins_simple.html")




@login_required
def liste_freins(request):

    tenant = request.user.societe
    with tenant_context(tenant):
        freins = VoitureFreins.objects.all()
    return render(request, "voiture_freins/list.html", {"freins": freins})







@login_required()
def freins_detail_view(request, frein_id):
    frein = get_object_or_404(VoitureFreins, id=frein_id)
    return render(request, 'voiture_freins/freins_detail.html', {
        'frein': frein,
    })




@login_required
def lier_freins(request, frein_id):
    tenant = request.user.societe  # ton tenant
    with tenant_context(tenant):
        frein = get_object_or_404(VoitureFreins, id=frein_id)
        exemplaires = VoitureExemplaire.objects.all().order_by("id")

        if request.method == "POST":
            cible_id = request.POST.get("cible_id")
            if cible_id:
                frein.voiture_exemplaire_id = cible_id
                frein.voiture_modele = None  # on supprime tout lien précédent avec un modèle
                frein.save()
                return redirect("voiture_freins:list")  # ou vers la page détail

    return render(request, "voiture_freins/lier_freins.html", {
        "frein": frein,
        "exemplaires": exemplaires
    })


@login_required
def lier_freins(request, frein_id):
    tenant = request.user.societe  # ton tenant
    with tenant_context(tenant):
        frein = get_object_or_404(VoitureFreins, id=frein_id)
        exemplaires = VoitureExemplaire.objects.all().order_by("id")

        if request.method == "POST":
            cible_id = request.POST.get("cible_id")
            if cible_id:
                frein.voiture_exemplaire_id = cible_id
                frein.voiture_modele = None  # on supprime tout lien précédent avec un modèle
                frein.save()
                return redirect("voiture_freins:list_ar")  # ou vers la page détail

    return render(request, "voiture_freins/lier_freins_ar.html", {
        "frein": frein,
        "exemplaires": exemplaires
    })




@login_required
def ajouter_freins_simple(request):
    if request.method == "POST":
        VoitureFreins.objects.create(
            marque_disque_av=request.POST.get("marque_disque_av"),
            marque_plaquettes_av=request.POST.get("marque_plaquettes_av"),
            taille_disque_av=request.POST.get("taille_disque_av"),
            epaisseur_disque_av=request.POST.get("epaisseur_disque_av"),
            épaisseur_min_disque_av=request.POST.get("epaisseur_min_disque_av"),

        )
        return redirect("voiture_freins:list")

@login_required
def ajouter_freins_ar_simple(request):
    if request.method == "POST":
        VoitureFreins.objects.create(
            marque_disque_ar=request.POST.get("marque_disque_ar"),
            marque_plaquettes_ar=request.POST.get("marque_plaquettes_ar"),
            taille_disque_ar=request.POST.get("taille_disque_ar"),
            epaisseur_disque_ar=request.POST.get("epaisseur_disque_ar"),
            épaisseur_min_disque_ar=request.POST.get("epaisseur_min_disque_ar"),
        )
        return redirect("voiture_freins:list_ar")

    return render(request, "voiture_freins/ajouter_freins_ar_simple.html")



from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele
from .models import MarqueFavorite



@never_cache
@login_required
def marques_list_view(request):
    marques = (
        VoitureMarque.objects
        .prefetch_related("modeles")
        .all()
        .order_by("nom_marque")
    )

    modeles = (
        VoitureModele.objects
        .select_related("voiture_marque")
        .all()
        .order_by("nom_modele")
    )

    favorites_ids = set(
        MarqueFavorite.objects
        .filter(societe=request.user)
        .values_list("marque_id", flat=True)
    )

    return render(
        request,
        "voiture_marque/marques_list.html",
        {
            "marques": marques,
            "modeles": modeles,
            "favorites_ids": favorites_ids,
        },
    )




@login_required
def modeles_par_marque(request, marque_id):
    tenant = request.user.societe

    marque = get_object_or_404(
        VoitureMarque,
        id_marque=marque_id,
        societe=tenant,
    )

    modeles = (
        VoitureModele.objects.filter(
            voiture_marque=marque,
            societe=tenant,
        )
        .order_by("nom_modele")
    )

    return render(
        request,
        "voiture_modele/modeles_par_marque.html",
        {
            "marque": marque,
            "modeles": modeles,
        },
    )



@login_required
def toggle_marque_favorite(request, marque_id):
    tenant = request.user.societe  # ton tenant

    if request.method != "POST":
        raise Http404

    marque = get_object_or_404(VoitureMarque, id_marque=marque_id)

    favori, created = MarqueFavorite.objects.get_or_create(
        societe=request.user,
        marque=marque
    )

    if not created:
        favori.delete()
        is_favorite = False
    else:
        is_favorite = True

    return JsonResponse({
        "is_favorite": is_favorite
    })



@login_required
def marques_favorites(request):

    marques = VoitureMarque.objects.filter(
        favoris__societe=request.user
    ).distinct()

    return render(request, "voiture_marque/marques_favorites.html", {
        "marques": marques
    })


def ajouter_marque(request):
    tenant = request.user.societe


    if request.method == "POST":
        nom_marque = request.POST.get("marque", "").strip()

        if not nom_marque:
            messages.error(request, _("Veuillez entrer un nom de marque."))
            return redirect("voiture_marque:ajouter_marque")

        if VoitureMarque.objects.filter(
            societe=tenant,
            nom_marque__iexact=nom_marque
        ).exists():
            messages.error(request, _("Cette marque existe déjà !"))
            return redirect("voiture_marque:ajouter_marque")

        VoitureMarque.objects.create(
            societe=tenant,
            nom_marque=nom_marque
        )

        messages.success(request, _("Marque ajoutée avec succès !"))
        return redirect("voiture_marque:ajouter_marque")

    return render(request, "voiture_marque/ajouter_marque.html")



@require_POST
def check_marque(request):
    marque = request.POST.get("marque", "").strip()

    exists = VoitureMarque.objects.filter(
        nom_marque__iexact=marque
    ).exists()

    return JsonResponse({"exists": exists})



@never_cache
@login_required
def dashboard_voiture_view(request):
    user = request.user

    marques = VoitureMarque.objects.all().order_by("nom_marque")
    modeles = VoitureModele.objects.all().order_by("nom_modele")
    exemplaires = VoitureExemplaire.objects.all().order_by("-id")

    return render(
        request,
        "voiture_marque/dashboard_voiture.html",
        {
            "user": user,
            "societe": getattr(user, "societe", None),
            "total_marques": marques.count(),
            "total_modele": modeles.count(),
            "total_exemplaires": exemplaires.count(),
            "marques": marques,
            "modele": modeles,
            "exemplaires": exemplaires,
        },
    )
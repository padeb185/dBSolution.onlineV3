from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import VoitureMarque, MarqueFavorite
from django.db.models import Exists, OuterRef


@login_required
def marque_list(request):
    marques = VoitureMarque.objects.all()
    return render(request, "voiture_marque/marque_list.html", {
        "marques": marques
    })




@login_required
def toggle_favori_marque(request, marque_id):
    marque = get_object_or_404(VoitureMarque, pk=marque_id)

    favori, created = MarqueFavorite.objects.get_or_create(
        utilisateur=request.user,
        marque=marque
    )

    if not created:
        favori.delete()
        return JsonResponse({"status": "removed"})
    else:
        return JsonResponse({"status": "added"})





def liste_marques(request):
    favoris = MarqueFavorite.objects.filter(
        utilisateur=request.user,
        marque=OuterRef("pk")
    )

    marques = VoitureMarque.objects.annotate(
        est_favori=Exists(favoris)
    )

    return render(request, "voiture/liste_marques.html", {
        "marques": marques
    })

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Piece

@method_decorator([login_required, never_cache], name='dispatch')
class PieceListView(ListView):
    model = Piece
    template_name = "piece/piece_list.html"
    context_object_name = "pieces"
    paginate_by = 20
    ordering = ["nom"]

    def get_queryset(self):
        societe = self.request.user.societe
        return Piece.objects.filter(societe=societe)




# Détail d'une pièce
class PieceDetailView(DetailView):
    model = Piece
    template_name = "piece/piece_detail.html"
    context_object_name = "piece"

# Création d'une pièce
class PieceCreateView(CreateView):
    model = Piece
    template_name = "piece/piece_form.html"
    fields = [
        "societe", "modele", "voiture_marque", "vehicule",
        "fabricants", "codes_barres",
        "immatriculation", "annee", "site", "pays", "emplacement_etagere", "qualite",
        "oem", "prix_achat", "majoration_pourcent", "tva", "prix_vente",
        "quantite_stock", "quantite_utilisee", "quantite_min",
        "organe", "marque"
    ]
    success_url = reverse_lazy("piece:list")

# Modification d'une pièce
class PieceUpdateView(UpdateView):
    model = Piece
    template_name = "piece/piece_form.html"
    fields = [
        "societe", "modele", "voiture_marque", "vehicule",
        "fabricants", "codes_barres",
        "immatriculation", "annee", "site", "pays", "emplacement_etagere", "qualite",
        "oem", "prix_achat", "majoration_pourcent", "tva", "prix_vente",
        "quantite_stock", "quantite_utilisee", "quantite_min",
        "organe", "marque"
    ]
    success_url = reverse_lazy("piece:list")

# Suppression d'une pièce
class PieceDeleteView(DeleteView):
    model = Piece
    template_name = "piece/piece_confirm_delete.html"
    success_url = reverse_lazy("piece:list")





import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Piece


@csrf_exempt
def check_fabricants(request):

    if request.method == "POST":
        data = json.loads(request.body)
        piece_id = data.get("piece")

        try:
            piece = Piece.objects.get(id=piece_id)

            fabricants = [f.id for f in piece.fabricants.all()]
            codes_barres = [c.id for c in piece.codes_barres.all()]

            return JsonResponse({
                "exist": True,
                "fabricants": fabricants[0] if fabricants else "",
                "oem": piece.oem,
                "codes_barres": codes_barres[0] if codes_barres else "",
                "emplacement_etagere": piece.emplacement_etagere,
            })

        except Piece.DoesNotExist:
            return JsonResponse({"exist": False})

    return JsonResponse({"exist": False})
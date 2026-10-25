from utils.securite import peut_supprimer, refuser_suppression
from django.contrib.auth.mixins import LoginRequiredMixin
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
class PieceDeleteView(LoginRequiredMixin, DeleteView):
    model = Piece
    template_name = "piece/piece_confirm_delete.html"
    success_url = reverse_lazy("piece:list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not peut_supprimer(request.user):
            return refuser_suppression(request)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Piece.objects.filter(societe=self.request.user.societe)

    def form_valid(self, form):
        from django.contrib import messages
        from django.db.models import ProtectedError
        from django.shortcuts import redirect
        from django.utils.translation import gettext as _
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, _("Pièce utilisée dans des maintenances : désactivez-la plutôt que de la supprimer."))
            return redirect("piece:detail", pk=self.object.pk)





import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Piece


@login_required
@require_POST
def check_fabricants(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body or b"{}")
        except (ValueError, UnicodeDecodeError):
            return JsonResponse({"exist": False}, status=400)
        piece_id = data.get("piece")
        if not str(piece_id or "").isdigit():
            return JsonResponse({"exist": False})

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
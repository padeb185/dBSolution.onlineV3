from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django_tenants.utils import tenant_context
from ..voiture_pneus.admin_forms import RemplacementPneusForm
from ..voiture_pneus.models import VoiturePneus



@login_required()
def remplacer_pneus(self, request, pk):
    pneus = self.get_object(request, pk)

    if request.method == "POST":
        form = RemplacementPneusForm(request.POST)
        if form.is_valid():
            pneus.remplacer_pneus(
                nouveau_type=form.cleaned_data["nouveau_type"],
                nouveaux_pneus_avant=form.cleaned_data["pneus_avant"],
                nouveaux_pneus_arriere=form.cleaned_data["pneus_arriere"],
                date=form.cleaned_data["date_remplacement"],
            )
            self.message_user(request, "Pneus remplacés avec succès.")
            return redirect(
                f"../../{pk}/change/"
            )
    else:
        form = RemplacementPneusForm()

    context = {
        "form": form,
        "pneus": pneus,
        "title": "Remplacer les pneus",
    }

    return render(
        request,
        "admin/voiture/voiturepneus/remplacer_pneus.html",
        context,
    )



@login_required
def liste_freins(request):

    tenant = request.user.societe
    with tenant_context(tenant):
        pneus = VoiturePneus.objects.all()
    return render(request, "voiture_pneus/list.html", {"pneus": pneus})







@login_required()
def freins_detail_view(request, pneus_id):
    pneus = get_object_or_404(VoiturePneus, id=pneus_id)
    return render(request, 'voiture_pneus/pneus_detail.html', {
        'pneus': pneus,
    })






@login_required
def ajouter_pneus_simple(request):
    if request.method == "POST":

        VoiturePneus.objects.create(
            pneus_avant_largeur=request.POST.get("pneus_avant_largeur"),
            pneus_avant_hauteur=request.POST.get("pneus_avant_hauteur"),
            pneus_avant_jante=request.POST.get("pneus_avant_jante"),

            pneus_arriere_largeur=request.POST.get("pneus_arriere_largeur"),
            pneus_arriere_hauteur=request.POST.get("pneus_arriere_hauteur"),
            pneus_arriere_jante=request.POST.get("pneus_arriere_jante"),

            indice_vitesse=request.POST.get("indice_vitesse"),
            indice_charge=request.POST.get("indice_charge"),



        )
        return redirect("voiture_freins:list")

    return render(request, "voiture_freins/ajouter_freins_simple.html")

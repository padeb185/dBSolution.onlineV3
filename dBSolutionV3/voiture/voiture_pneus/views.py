from django_tenants.utils import tenant_context
from ..voiture_pneus.admin_forms import RemplacementPneusForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import VoiturePneus



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
def liste_pneus(request):

    tenant = request.user.societe
    with tenant_context(tenant):
        pneus = VoiturePneus.objects.all()
    return render(request, "voiture_pneus/list.html", {"pneus": pneus})







@login_required
def pneus_detail_view(request, embrayage_id):
    from .models import VoiturePneus
    pneu = VoiturePneus.objects.get(id=embrayage_id)
    context = {'pneus': pneu}
    return render(request, "voiture_pneus/pneus_detail.html", context)




@login_required
def ajouter_pneus_simple(request):
    if request.method == "POST":
        VoiturePneus.objects.create(
            manufacturier=request.POST.get("manufacturier"),
            emplacement=request.POST.get("emplacement"),
            type_pneus=request.POST.get("type_pneus"),
            nom_type=request.POST.get("nom_type"),
            pneus_largeur=request.POST.get("pneus_largeur"),
            pneus_hauteur=request.POST.get("pneus_hauteur"),
            pneus_jante=request.POST.get("pneus_jante"),
            indice_vitesse=request.POST.get("indice_vitesse"),
            indice_charge=request.POST.get("indice_charge"),
            numero_oem=request.POST.get("numero_oem"),
        )
        return redirect("voiture_pneus:list")

    # GET request
    context = {
        'TypePneus': VoiturePneus.TypePneus,
        'IndiceVitesse': VoiturePneus.IndiceVitesse,
        'IndiceCharge': VoiturePneus.IndiceCharge,
        'EmplacementPneus': VoiturePneus.EmplacementPneus,
    }

    return render(request, "voiture_pneus/ajouter_pneus_simple.html", context)
from django.contrib import messages
from django_tenants.utils import tenant_context

from .. import voiture_pneus
from ..voiture_pneus.admin_forms import RemplacementPneusForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import VoiturePneus
from django.utils.translation import gettext as _




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
            self.message_user(request, _("Pneus remplacés avec succès."))

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
        manufacturier = request.POST.get("manufacturier")
        emplacement = request.POST.get("emplacement")
        type_pneus = request.POST.get("type_pneus")
        nom_type = request.POST.get("nom_type")
        pneus_largeur = request.POST.get("pneus_largeur")
        pneus_hauteur = request.POST.get("pneus_hauteur")
        pneus_jante = request.POST.get("pneus_jante")
        indice_vitesse = request.POST.get("indice_vitesse")
        indice_charge = request.POST.get("indice_charge")
        numero_oem = request.POST.get("numero_oem")

        # Vérification simple pour un champ obligatoire, exemple "manufacturier"
        if not manufacturier:
            messages.error(request, _("Le nom du manufacturier est obligatoire."))
        else:
            VoiturePneus.objects.create(
                manufacturier=manufacturier,
                emplacement=emplacement,
                type_pneus=type_pneus,
                nom_type=nom_type,
                pneus_largeur=pneus_largeur,
                pneus_hauteur=pneus_hauteur,
                pneus_jante=pneus_jante,
                indice_vitesse=indice_vitesse,
                indice_charge=indice_charge,
                numero_oem=numero_oem,
            )
            messages.success(request,
                             _(f"Le pneu '{voiture_pneus.manufatcurier}' ajouté avec succès !"))

    context = {
        'TypePneus': VoiturePneus.TypePneus,
        'IndiceVitesse': VoiturePneus.IndiceVitesse,
        'IndiceCharge': VoiturePneus.IndiceCharge,
        'EmplacementPneus': VoiturePneus.EmplacementPneus,
    }

    return render(request, "voiture_pneus/ajouter_pneus_simple.html", context)

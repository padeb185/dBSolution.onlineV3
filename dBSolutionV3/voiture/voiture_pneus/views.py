from django.contrib import messages
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context
from .forms import VoiturePneusForm
from .. import voiture_pneus
from ..voiture_pneus.admin_forms import RemplacementPneusForm
from django.shortcuts import render, redirect, get_object_or_404
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


@never_cache
@login_required
def liste_pneus(request):

    tenant = request.user.societe
    pneus = VoiturePneus.objects.filter(societe=tenant)


    return render(request, "voiture_pneus/list.html",{
        "pneus": pneus

})






@login_required
def pneus_detail_view(request, pneu_id):
    from .models import VoiturePneus

    # 🔒 Sécurisé (évite crash si ID invalide)
    pneu = get_object_or_404(VoiturePneus, id=pneu_id)

    # 💡 Optionnel : message info (exemple)
    if request.GET.get("success"):
        messages.success(request, "Pneu changé avec succès.")

    context = {
        'pneus': pneu
    }

    return render(request, "voiture_pneus/pneus_detail.html", context)



@login_required
def ajouter_pneus_simple(request):
    tenant = request.user.societe

    if request.method == "POST":
        form = VoiturePneusForm(
            request.POST,
            request.FILES or None,
        )

        if form.is_valid():
            pneu = form.save(commit=False)
            pneu.societe = tenant
            pneu.save()
            form.save_m2m()

            messages.success(
                request,
                _(
                    f"Le pneu '{pneu.manufacturier} "
                    f"{pneu.pneus_largeur}/{pneu.pneus_hauteur} "
                    f"R{pneu.pneus_jante}' a été ajouté avec succès !"
                ),
            )

            return redirect("voiture_pneus:ajouter_pneus")

        messages.error(
            request,
            _("Le formulaire contient des erreurs."),
        )

    else:
        form = VoiturePneusForm()

    return render(
        request,
        "voiture_pneus/ajouter_pneus_simple.html",
        {
            "form": form,
        },
    )

@login_required
def modifier_pneus_view(request, pneu_id):
    pneus = get_object_or_404(
        VoiturePneus,
        id=pneu_id,
    )

    if request.method == "POST":
        form = VoiturePneusForm(
            request.POST,
            request.FILES or None,
            instance=pneus,
        )

        if form.is_valid():
            pneu = form.save()

            messages.success(
                request,
                _("Pneu mis à jour avec succès."),
            )

            return redirect(
                "voiture_pneus:modifier_pneus",
                pneu_id=pneu.id,
            )

        messages.error(
            request,
            _("Le formulaire contient des erreurs."),
        )

    else:
        form = VoiturePneusForm(instance=pneus)

    return render(
        request,
        "voiture_pneus/modifier_pneus.html",
        {
            "form": form,
            "pneus": pneus,
        },
    )
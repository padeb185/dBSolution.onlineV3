from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from outillage.forms import OutillageForm
from django.utils.translation import gettext_lazy as _
from utilisateurs.models import UserLog
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import ProtectedError, RestrictedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _, gettext_noop

from core.suppression import analyser_suppression
from .models import Outillage






@method_decorator([login_required, never_cache], name='dispatch')
class OutillageListView(ListView):
    model = Outillage
    template_name = "outillage/outillage_list.html"
    context_object_name = "outillages"
    ordering = ["-id"]

    def get_queryset(self):
        societe = self.request.user.societe
        return Outillage.objects.filter(societe=societe)




@login_required
def outillage_detail(request, outillage_id):
    tenant = request.user.societe


    outillage = get_object_or_404(Outillage, id_outillage=outillage_id)


    return render(
        request,
        "outillage/outillage_detail.html",
        {
            "outillage": outillage,
        },
    )



@login_required
def ajouter_outillage_all(request):

    tenant = request.user.societe

    if request.method == "POST":

        form_outillage = OutillageForm(request.POST)

        if form_outillage.is_valid():

            # -------------------------
            # CRÉATION OUTILLAGE
            # -------------------------
            outillage = form_outillage.save(commit=False)

            outillage.societe = tenant

            outillage.save()

            messages.success(
                request,
                _(
                    f"Outillage '{outillage.libelle}' créé avec succès !"
                )
            )
            return redirect(
                f"{reverse('outillage:outillage_list')}?saved=1"
            )

        else:

            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )

    else:

        form_outillage = OutillageForm()

    return render(
        request,
        "outillage/outillage_form.html",
        {
            "form": form_outillage,
        },
    )

@login_required
def modifier_outillage(request, outillage_id):
    tenant = request.user.societe

    # Récupérer l'outillage par son vrai champ PK : id_outillage
    outillage = get_object_or_404(
        Outillage,
        id_outillage=outillage_id
    )

    if request.method == "POST":
        form_outillage = OutillageForm(request.POST, instance=outillage)

        if form_outillage.is_valid():
            form_outillage.save()
            messages.success(request, "Outillage mis à jour avec succès.")

            return redirect(
                f"{reverse('outillage:outillage_detail', kwargs={'outillage_id': outillage.id})}?saved=1"
            )

        else:
            messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form_outillage = OutillageForm(instance=outillage)

    return render(
        request,
        "outillage/modifier_outillage.html",
        {
            "form": form_outillage,
            "outillage": outillage,
        }
    )




ACTION_SUPPRESSION_OUTILLAGE = gettext_noop("Suppression de l'outillage")


@login_required
def delete_outillage_view(request, pk):
    outillage = get_object_or_404(
        Outillage.objects.select_related("fournisseur", "societe"),
        pk=pk,
    )

    analyse = analyser_suppression(outillage)
    objets_bloquants = analyse["bloquants"]
    objets_supprimes = analyse["supprimes"]

    if request.method == "POST":
        libelle = outillage.libelle

        if objets_bloquants:
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : il est encore utilisé ailleurs.") % {"nom": libelle},
            )
            return redirect("outillage:delete_outillage", pk=pk)

        # Libellé pour le log (capturé AVANT la suppression)
        nom_log = libelle
        if outillage.reference:
            nom_log += f" (réf. {outillage.reference})"
        nom_log += f" – {outillage.quantite} pcs"
        nom_log += f" – {outillage.fournisseur.nom if outillage.fournisseur_id else '—'}"
        if outillage.montant_calcule is not None:
            nom_log += f" – {outillage.montant_calcule:.2f} € TVAC"

        try:
            with transaction.atomic():
                outillage.delete()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_OUTILLAGE} : {nom_log}",
                )
        except (ProtectedError, RestrictedError):
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : il est encore utilisé ailleurs.") % {"nom": libelle},
            )
            return redirect("outillage:delete_outillage", pk=pk)

        messages.success(request, _("L'outillage « %(nom)s » a bien été supprimé.") % {"nom": libelle})

        return redirect(
            f"{reverse('outillage:outillage_list')}?deleted=1"
        )

    return render(
        request,
        "outillage/delete_outillage.html",
        {
            "outillage": outillage,
            "objets_supprimes": objets_supprimes,
            "objets_bloquants": objets_bloquants,
        },
    )
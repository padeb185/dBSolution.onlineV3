from django.urls import reverse
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from achat_mds.forms import AchatForm
from fournisseur.models import Fournisseur
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import ProtectedError, RestrictedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _, gettext_noop
from utilisateurs.models import UserLog

from .models import AchatMds





@never_cache
@login_required
def achat_mds_view(request):
    tenant = request.user.societe

    # Filtrer par société
    fournisseurs = Fournisseur.objects.filter(societe=tenant)
    achat_mds = AchatMds.objects.filter(societe=tenant)

    if request.method == "POST":
        form = AchatForm(request.POST)

        if form.is_valid():
            achat = form.save(commit=False)
            achat.societe = tenant
            achat.save()

            messages.success(
                request,
                _("Achat enregistré avec succès.")
            )

            return redirect(
                f"{reverse('achat_mds:achat_list')}?saved=1"
            )

    else:
        form = AchatForm()

    return render(
        request,
        "achat_mds/achat_form.html",
        {
            "form": form,
            "achat_mds": achat_mds,
            "fournisseurs": fournisseurs,
        },
    )



@method_decorator([login_required, never_cache], name='dispatch')
class AchatMdsListView(ListView):
    model = AchatMds
    template_name = "achat_mds/achat_list.html"
    context_object_name = "achats"
    ordering = ["nom"]

    def get_queryset(self):
        tenant = self.request.user.societe
        return AchatMds.objects.filter(societe=tenant)






@never_cache
@login_required
def achat_detail_view(request, achat_id):
    tenant = request.user.societe

    achat = get_object_or_404(
        AchatMds,
        id=achat_id,
        societe=tenant   # 🔒 IMPORTANT sécurité multi-tenant
    )

    fournisseurs = Fournisseur.objects.filter(societe=tenant)

    return render(
        request,
        "achat_mds/achat_detail.html",
        {
            "achat": achat,
            "fournisseurs": fournisseurs,
        },
    )


@never_cache
@login_required
def modifier_achat_view(request, achat_id):
    tenant = request.user.societe


    achat = get_object_or_404(AchatMds, id=achat_id)
    fournisseurs = Fournisseur.objects.filter(societe=tenant)

    if request.method == "POST":
        form = AchatForm(request.POST, instance=achat)
        if form.is_valid():
            form.save()
            messages.success(request, _("Achat modifié avec succès !"))
            return redirect(
                f"{reverse('achat_mds:achat_detail', kwargs={'achat_id': achat.id})}?saved=1"
            )


    else:
        form = AchatForm(instance=achat)

    return render(
        request,
        "achat_mds/modifier_achat_mds.html",
        {
            "form": form,
            "fournisseurs": fournisseurs,
            "achat": achat,
        }
    )







ACTION_SUPPRESSION_ACHAT = gettext_noop("Suppression de l'achat")

@never_cache
@login_required
def delete_achat_view(request, pk):
    achat = get_object_or_404(
        AchatMds.objects.select_related("fournisseur", "societe"),
        pk=pk,
    )

    if request.method == "POST":
        libelle = achat.reference_facture or achat.libelle_facture or str(achat)

        # Libellé pour le log (capturé AVANT la suppression)
        fournisseur_nom = achat.fournisseur.nom if achat.fournisseur else "—"
        date_facture = achat.date_facture.strftime("%d/%m/%Y") if achat.date_facture else "—"
        nom_log = (
            f"{libelle} – {fournisseur_nom} – {date_facture} – "
            f"{achat.total_tvac:.2f} € TVAC"
        )

        try:
            with transaction.atomic():
                achat.delete()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_ACHAT} : {nom_log}",
                )
        except (ProtectedError, RestrictedError):
            messages.error(
                request,
                _("Impossible de supprimer l'achat « %(ref)s » : il est encore utilisé ailleurs.") % {"ref": libelle},
            )
            return redirect("achat_mds:delete_achat", pk=pk)

        messages.success(request, _("L'achat « %(ref)s » a bien été supprimé.") % {"ref": libelle})
        return redirect(
            f"{reverse('achat_mds:achat_list')}?deleted=1"
        )

    return render(request, "achat_mds/delete_achat.html", {"achat": achat})
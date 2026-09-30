from django.db.models import ProtectedError, RestrictedError
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from utilisateurs.models import UserLog
from .forms import AssurancePoliceForm
from .models import Sinistre
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _, gettext_noop

from .models import AssurancePolice







@login_required
def dashboard_assurances(request):
    today = timezone.now().date()
    in_30_days = today + timedelta(days=30)

    polices_actives = AssurancePolice.objects.filter(actif=True).count()
    polices_expirees = AssurancePolice.objects.filter(date_fin__lt=today).count()
    polices_bientot = AssurancePolice.objects.filter(date_fin__range=(today, in_30_days)).count()

    sinistres_ouverts = Sinistre.objects.filter(cloture=False).count()

    cout_total_annuel = AssurancePolice.cout_total_annuel()
    cout_total_mensuel = AssurancePolice.cout_total_mensuel()

    context = {
        'polices_actives': polices_actives,
        'polices_expirees': polices_expirees,
        'polices_bientot': polices_bientot,
        'sinistres_ouverts': sinistres_ouverts,
        'cout_total_annuel': cout_total_annuel,
        'cout_total_mensuel': cout_total_mensuel,
    }

    return render(request, 'assurance_police/dashboard.html', context)




@method_decorator([login_required, never_cache], name="dispatch")
class AssurancePoliceListView(ListView):
    model = AssurancePolice
    template_name = "assurance_police/assurance_police_list.html"
    context_object_name = "assurance_polices"

    def get_queryset(self):
        tenant = self.request.user.societe  # récupération du tenant via le request

        with tenant_context(tenant):
            # Récupérer toutes les polices du tenant, avec select_related pour les relations
            queryset = (
                AssurancePolice.objects
                .select_related("assurance", "voiture_exemplaire")
                .order_by("-date_debut")
            )
        return queryset




@login_required
def ajouter_assurance_all(request):
    tenant = request.user.societe  # si tu utilises tenant
    if request.method == "POST":
        form_assurance_police = AssurancePoliceForm(request.POST)
        if form_assurance_police.is_valid():
            assurance_police = form_assurance_police.save(commit=False)

            assurance_police.societe = tenant
            assurance_police.save()
            messages.success(
                request,
                _(f"Assurance '{assurance_police.assurance.nom_compagnie}' créée avec succès !"
            ))

            return redirect(
                f"{reverse('assurance_police:assurance_police_list')}?saved=1"
            )
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form_assurance_police = AssurancePoliceForm()

    return render(request, "assurance_police/assurance_police_form.html", {
        "form": form_assurance_police
    })



@login_required
def assurance_police_detail(request, assurance_police_id):
    tenant = request.user.societe

    assurance_police = get_object_or_404(AssurancePolice, id=assurance_police_id)


    return render(
        request,
        "assurance_police/assurance_police_detail.html",
        {
            "assurance_police": assurance_police,

        },
    )





@login_required
def modifier_assurance_police(request, assurance_police_id):
    tenant = request.user.societe

    # Récupère l'objet AssurancePolice du tenant
    assurance_police = get_object_or_404(
        AssurancePolice,
        pk=assurance_police_id
    )

    if request.method == "POST":
        form = AssurancePoliceForm(
            request.POST,
            request.FILES,
            instance=assurance_police
        )

        if form.is_valid():
            assurance_police = form.save()
            messages.success(request, _("Police d'assurance mise à jour avec succès."))

            return redirect(
                f"{reverse('assurance_police:assurance_police_detail', kwargs={'assurance_police_id': assurance_police.id})}?saved=1"
            )


        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    else:
        # Pour GET : initialiser le formulaire avec les valeurs existantes
        # et formater les dates correctement si nécessaire
        initial_data = {
            "date_debut": assurance_police.date_debut,
            "date_fin": assurance_police.date_fin,
            # ajouter d'autres champs si nécessaire
        }
        form = AssurancePoliceForm(instance=assurance_police, initial=initial_data)

    return render(
        request,
        "assurance_police/modifier_assurance_police.html",
        {
            "form": form,
            "assurance_police": assurance_police,
        }
    )







ACTION_SUPPRESSION_POLICE = gettext_noop("Suppression de la police d'assurance")


@login_required
def delete_assurance_police_view(request, pk):
    police = get_object_or_404(
        AssurancePolice.objects.select_related("assurance", "voiture_exemplaire", "societe"),
        pk=pk,
    )
    sinistres_lies = police.sinistres.all()

    if request.method == "POST":
        numero = police.numero_contrat

        # Fichier PDF : on capture nom + stockage AVANT la suppression
        nom_fichier = police.document_pdf.name if police.document_pdf else None
        stockage = police.document_pdf.storage if police.document_pdf else None

        # Libellé pour le log (capturé AVANT la suppression)
        compagnie = police.assurance.nom_compagnie if police.assurance else "—"
        voiture = str(police.voiture_exemplaire) if police.voiture_exemplaire_id else "—"
        nb_sinistres = sinistres_lies.count()
        nom_log = f"{numero} – {compagnie} – {voiture}"
        if nb_sinistres:
            nom_log += f" – {nb_sinistres} sinistre(s) supprimé(s)"

        try:
            with transaction.atomic():
                police.delete()  # supprime aussi les sinistres (CASCADE)

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_POLICE} : {nom_log}",
                )

                # Le fichier PDF n'est pas supprimé automatiquement par Django :
                # on l'efface seulement si la transaction est validée
                if nom_fichier:
                    transaction.on_commit(lambda: stockage.delete(nom_fichier))
        except (ProtectedError, RestrictedError):
            messages.error(
                request,
                _("Impossible de supprimer la police « %(numero)s » : elle est encore liée à d'autres éléments.") % {"numero": numero},
            )
            return redirect("assurance_police:delete_assurance_police", pk=pk)

        messages.success(
            request,
            _("La police « %(numero)s » a bien été supprimée.") % {"numero": numero},
        )

        return redirect(
            f"{reverse('assurance_police:assurance_police_list')}?deleted=1"
        )

    return render(
        request,
        "assurance_police/delete_assurance_police.html",
        {
            "police": police,
            "sinistres_lies": sinistres_lies,
        },
    )
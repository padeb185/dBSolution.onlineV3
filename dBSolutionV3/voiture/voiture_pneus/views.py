from django.apps import apps
from django.db import transaction
from django.db.models import Q, ProtectedError
from django.urls import reverse
from django.utils.translation import  gettext_noop
from utilisateurs.models import UserLog  # adapte le chemin si besoin
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .forms import VoiturePneusForm
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





@never_cache
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
            return redirect(
                f"{reverse('voiture_pneus:list')}?saved=1"
            )

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
                f"{reverse('voiture_pneus:pneus_detail', kwargs={'pneu_id': pneu.id})}?saved=1"
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



@never_cache
@login_required
def delete_pneus_view(request, pneus_id):
    tenant = request.user.societe
    role = request.user.role

    # ==================================================
    # AUTORISATIONS
    # ==================================================
    roles_autorises = [
        "direction",
        "chef_mecanicien",
    ]

    if role not in roles_autorises and not request.user.is_superuser:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # ==================================================
    # RÉCUPÉRATION PNEUS (filtré par tenant)
    # ==================================================
    pneus = get_object_or_404(
        VoiturePneus.objects.filter(
            Q(societe=tenant)
            | Q(voitures_exemplaires__client__societe=tenant)
            | Q(
                voitures_exemplaires__client__isnull=True,
                voitures_exemplaires__societe=tenant,
            )
        ).distinct(),
        id=pneus_id,
    )

    # ==================================================
    # EXEMPLAIRE DE RETOUR
    # ==================================================
    exemplaire_id = (
        request.POST.get("exemplaire_id")
        or request.GET.get("exemplaire_id")
    )

    exemplaires_lies = pneus.voitures_exemplaires.all()
    modeles_lies = pneus.voitures_modeles.all()

    exemplaire = None
    if exemplaire_id:
        exemplaire = exemplaires_lies.filter(id=exemplaire_id).first()
    if exemplaire is None:
        exemplaire = exemplaires_lies.first()

    # ==================================================
    # HISTORIQUE LIÉ (info pour l'utilisateur)
    # ==================================================
    nb_historiques = 0
    try:
        VoiturePneusHistorique = apps.get_model(
            "voiture_pneus_historique", "VoiturePneusHistorique"
        )
        nb_historiques = VoiturePneusHistorique.objects.filter(
            voiture_pneus=pneus
        ).count()
    except LookupError:
        pass

    # ==================================================
    # DELETE
    # ==================================================
    if request.method == "POST":

        # Infos à conserver AVANT suppression
        pneus_pk = pneus.pk
        pneus_str = (
            f"{pneus.manufacturier} {pneus.nom_type or ''} "
            f"{pneus.pneus_largeur}/{pneus.pneus_hauteur} R{pneus.pneus_jante}"
        ).strip()
        exemplaires_str = ", ".join(str(e) for e in exemplaires_lies)
        exemplaire_retour_id = exemplaire.id if exemplaire else None

        try:
            with transaction.atomic():

                pneus.delete()

                ACTION_SUPPRESSION_PNEUS = gettext_noop(
                    "Suppression des pneus"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_PNEUS} "
                        f"{pneus_str} (ID {pneus_pk})"
                        + (f" – {exemplaires_str}" if exemplaires_str else "")
                    ),
                )

        except ProtectedError:
            pneus.pk = pneus_pk
            messages.error(
                request,
                _("Impossible de supprimer ces pneus : ils sont encore référencés par d'autres données."),
            )

        except Exception as e:
            pneus.pk = pneus_pk
            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s") % {"erreur": str(e)},
            )

        else:
            messages.success(request, _("Pneus supprimés avec succès."))


            return redirect(
                f"{reverse('voiture_pneus:pneus_list')}?deleted=1"
            )


    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "voiture_pneus/delete_pneus.html",
        {
            "pneus": pneus,
            "exemplaire": exemplaire,
            "exemplaires_lies": exemplaires_lies,
            "modeles_lies": modeles_lies,
            "nb_historiques": nb_historiques,
        },
    )
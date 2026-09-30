from voiture.voiture_embrayage.forms import VoitureEmbrayageForm
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext as _, gettext_noop
from django.views.decorators.cache import never_cache

from voiture.voiture_embrayage.models import VoitureEmbrayage
from utilisateurs.models import UserLog  # adapte le chemin si besoin






@never_cache
@login_required
def liste_embrayage(request):
    embrayages = VoitureEmbrayage.objects.all()
    return render(request, "voiture_embrayage/list.html",
                  {
                      "embrayages": embrayages
                  })




@login_required
def ajouter_embrayage_view(request):

    if request.method == "POST":
        form = VoitureEmbrayageForm(
            request.POST,
            request.FILES or None,
        )

        if form.is_valid():
            embrayage = form.save(commit=False)

            embrayage.save()
            form.save_m2m()

            messages.success(request, _("Embrayage ajouté avec succès !"))

            return redirect(
                f"{reverse('voiture_embrayage:list')}?saved=1"
            )

        messages.error(request, _("Veuillez corriger les erreurs du formulaire."))

    else:
        form = VoitureEmbrayageForm()

    return render(
        request,
        "voiture_embrayage/ajouter_embrayage.html",
        {
            "form": form,
        },
    )



@login_required
def lier_embrayage(request, embrayage_id):
    embrayage = get_object_or_404(VoitureEmbrayage, id=embrayage_id)
    exemplaires = VoitureExemplaire.objects.all().order_by("id")

    if request.method == "POST":
        cible_id = request.POST.get("cible_id")
        if cible_id:
            embrayage.voiture_exemplaire_id = cible_id
            embrayage.voiture_modele = None  # on supprime tout lien précédent avec un modèle
            embrayage.save()

            messages.success(
                request,
                _("L'embrayage a été lié au véhicule avec succès.")
            )

            return redirect("voiture_embrayage:list")

    return render(
        request,
        "voiture_embrayage/lier_embrayage.html",
        {
            "embrayage": embrayage,
            "exemplaires": exemplaires,
        },
    )




@login_required
def embrayage_detail_view(request, embrayage_id):
    embrayage = get_object_or_404(
        VoitureEmbrayage,
        id=embrayage_id,
    )

    return render(
        request,
        "voiture_embrayage/embrayage_detail.html",
        {
            "embrayage": embrayage,
        },
    )




@login_required
def modifier_embrayage_view(request, embrayage_id):
    embrayage = get_object_or_404(
        VoitureEmbrayage,
        id=embrayage_id,
    )

    if request.method == "POST":
        form = VoitureEmbrayageForm(
            request.POST,
            request.FILES or None,
            instance=embrayage,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                _("Embrayage mis à jour avec succès."),
            )

            return redirect(
                "voiture_embrayage:embrayage_detail",
                embrayage_id=embrayage.id,
            )

        messages.error(
            request,
            _("Le formulaire contient des erreurs."),
        )

    else:
        form = VoitureEmbrayageForm(instance=embrayage)

    return render(
        request,
        "voiture_embrayage/modifier_embrayage.html",
        {
            "form": form,
            "embrayage": embrayage,
        },
    )





@never_cache
@login_required
def delete_embrayage_view(request, embrayage_id):
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
    # RÉCUPÉRATION EMBRAYAGE (filtré par tenant)
    # ==================================================
    embrayage = get_object_or_404(
        VoitureEmbrayage.objects.filter(
            Q(societe=tenant)
            | Q(voitures_exemplaires__client__societe=tenant)
            | Q(
                voitures_exemplaires__client__isnull=True,
                voitures_exemplaires__societe=tenant,
            )
        ).distinct(),
        id=embrayage_id,
    )

    exemplaires_lies = embrayage.voitures_exemplaires.all()
    modeles_lies = embrayage.voitures_modeles.all()

    # ==================================================
    # DELETE
    # ==================================================
    if request.method == "POST":

        # Infos à conserver AVANT suppression
        embrayage_pk = embrayage.pk
        embrayage_str = " ".join(
            filter(None, [
                f"#{embrayage.numero_embrayage}" if embrayage.numero_embrayage else None,
                embrayage.fabricant,
                embrayage.oem,
            ])
        )
        exemplaires_str = ", ".join(str(e) for e in exemplaires_lies)

        try:
            with transaction.atomic():

                embrayage.delete()

                ACTION_SUPPRESSION_EMBRAYAGE = gettext_noop(
                    "Suppression de l'embrayage"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_EMBRAYAGE} "
                        f"{embrayage_str} (ID {embrayage_pk})"
                        + (f" – {exemplaires_str}" if exemplaires_str else "")
                    ),
                )

        except ProtectedError:
            embrayage.pk = embrayage_pk
            messages.error(
                request,
                _("Impossible de supprimer cet embrayage : il est encore référencé par d'autres données."),
            )

        except Exception as e:
            embrayage.pk = embrayage_pk
            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s") % {"erreur": str(e)},
            )

        else:
            messages.success(request, _("Embrayage supprimé avec succès."))

            # ⚠️ nom d'URL à vérifier — repli sur le dashboard s'il n'existe pas
            try:
                return redirect(f"{reverse('voiture_embrayage:list')}?deleted=1")
            except NoReverseMatch:
                return redirect("utilisateurs:dashboard")

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "voiture_embrayage/delete_embrayage.html",
        {
            "embrayage": embrayage,
            "exemplaires_lies": exemplaires_lies,
            "modeles_lies": modeles_lies,
        },
    )

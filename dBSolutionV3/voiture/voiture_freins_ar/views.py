from .forms import VoitureFreinsARForm
from ..voiture_modele.models import VoitureModele
from societe.models import Societe
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _, gettext_noop
from django.views.decorators.cache import never_cache
from voiture.voiture_freins_ar.models import VoitureFreinsAR
from utilisateurs.models import UserLog






@login_required
def ajouter_freins_ar(request, modele_id):
    tenant = request.user.societe

    modele = get_object_or_404(
        VoitureModele,
        id=modele_id,
    )

    if request.method == "POST":
        post_data = request.POST.copy()

        champs_float = [
            "taille_disque_ar",
            "epaisseur_disque_ar",
            "epaisseur_min_disque_ar",
            "plaquettes_ar",
        ]

        for champ in champs_float:
            valeur = post_data.get(champ)

            if valeur:
                post_data[champ] = valeur.replace(",", ".")

        form = VoitureFreinsARForm(
            post_data,
            request.FILES or None,
        )

        if form.is_valid():
            freins_ar = form.save(commit=False)
            freins_ar.societe = tenant
            freins_ar.save()
            form.save_m2m()

            messages.success(
                request,
                _("Freins arrière ajoutés avec succès !"),
            )

            return redirect(
                "voiture_freins_ar:freins_ar_list",
            )

        messages.error(
            request,
            _("Veuillez corriger les erreurs ci-dessous."),
        )

    else:
        form = VoitureFreinsARForm()

    return render(
        request,
        "voiture_freins_ar/ajouter_freins_ar_simple.html",
        {
            "form": form,
            "modele": modele,
        },
    )


@login_required
def ajouter_freins_ar_simple(request):
    tenant = request.user.societe

    if request.method == "POST":
        post_data = request.POST.copy()

        champs_float = [
            "taille_disque_ar",
            "epaisseur_disque_ar",
            "epaisseur_min_disque_ar",
            "plaquettes_ar",
        ]

        for champ in champs_float:
            valeur = post_data.get(champ)

            if valeur:
                post_data[champ] = valeur.replace(",", ".")

        form = VoitureFreinsARForm(
            post_data,
            request.FILES or None,
        )

        if form.is_valid():
            obj = form.save(commit=False)
            obj.societe = tenant
            obj.save()
            form.save_m2m()

            messages.success(
                request,
                _("Freins arrière ajoutés avec succès !"),
            )

            return redirect(
                "voiture_freins_ar:freins_ar_list",
            )

        messages.error(
            request,
            _("Veuillez corriger les erreurs du formulaire."),
        )

    else:
        form = VoitureFreinsARForm()

    return render(
        request,
        "voiture_freins_ar/ajouter_freins_ar_simple.html",
        {
            "form": form,
        },
    )


@never_cache
@login_required
def freins_ar_detail_view(request, frein_ar_id):
    frein = get_object_or_404(
        VoitureFreinsAR,
        id=frein_ar_id,
    )

    return render(
        request,
        "voiture_freins_ar/freins_ar_detail.html",
        {
            "frein": frein,
        },
    )


@never_cache
@login_required
def liste_freins_ar(request, societe_id=None):
    societe = request.user.societe

    if societe_id:
        societe = get_object_or_404(
            Societe,
            id=societe_id,
        )

    freins_ar = VoitureFreinsAR.objects.filter(
        societe=societe,
    )

    return render(
        request,
        "voiture_freins_ar/freins_ar_list.html",
        {
            "freins_ar": freins_ar,
        },
    )
    return render(request, "voiture_freins_ar/freins_ar_list.html", {
        "freins_ar": freins_ar
    })

@login_required
def modifier_freins_ar_view(request, frein_ar_id):
    tenant = request.user.societe


    freins_ar = get_object_or_404(VoitureFreinsAR, id=frein_ar_id)

    if request.method == "POST":
        form_frein = VoitureFreinsARForm(request.POST, instance=freins_ar)
        if form_frein.is_valid():
            form_frein.save()
            messages.success(request, _("Freins arrière mis à jour avec succès."))
            return redirect("voiture_freins_ar:freins_ar_detail", frein_ar_id=freins_ar.id)

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form_frein = VoitureFreinsARForm(instance=freins_ar)

    return render(
        request,
        "voiture_freins_ar/modifier_freins_ar.html",
        {
            "form": form_frein,
            "frein": freins_ar,
        }
    )


@never_cache
@login_required
def delete_frein_ar_view(request, frein_ar_id):
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
    # RÉCUPÉRATION FREIN AR (filtré par tenant)
    # ==================================================
    # Accessible si :
    #  - le frein AR appartient directement à la société
    #  - OU il est lié à un exemplaire dont le client appartient à la société
    #  - OU il est lié à un exemplaire sans client appartenant à la société
    frein_ar = get_object_or_404(
        VoitureFreinsAR.objects.filter(
            Q(societe=tenant)
            | Q(voitures_exemplaires__client__societe=tenant)
            | Q(
                voitures_exemplaires__client__isnull=True,
                voitures_exemplaires__societe=tenant,
            )
        ).distinct(),
        id=frein_ar_id,
    )

    # ==================================================
    # EXEMPLAIRE DE RETOUR (pour la redirection)
    # ==================================================
    # Priorité : ?exemplaire_id=... (GET ou POST), sinon le premier exemplaire lié
    exemplaire_id = (
        request.POST.get("exemplaire_id")
        or request.GET.get("exemplaire_id")
    )

    exemplaires_lies = frein_ar.voitures_exemplaires.all()

    exemplaire = None
    if exemplaire_id:
        exemplaire = exemplaires_lies.filter(id=exemplaire_id).first()
    if exemplaire is None:
        exemplaire = exemplaires_lies.first()

    # ==================================================
    # DELETE
    # ==================================================
    if request.method == "POST":
        try:
            with transaction.atomic():

                # Infos pour le log AVANT suppression
                # (les liens M2M sont supprimés avec l'objet)
                exemplaires_str = ", ".join(str(e) for e in exemplaires_lies)
                frein_ar_pk = frein_ar.pk

                # ==================================================
                # SUPPRESSION FREIN AR
                # ==================================================
                frein_ar.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_FREIN_AR = gettext_noop(
                    "Suppression du système de freinage arrière"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_FREIN_AR} "
                        + (f" – {exemplaires_str}" if exemplaires_str else "")
                    ),
                )

            messages.success(
                request,
                _("Système de freinage arrière supprimé avec succès."),
            )

            if exemplaire:
                return redirect(
                    f"{reverse('voiture_freins_ar:frein_ar_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
                )
            return redirect("utilisateurs:dashboard")

        except Exception as e:
            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s") % {"erreur": str(e)},
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "voiture_freins_ar/delete_frein_ar.html",
        {
            "frein_ar": frein_ar,
            "exemplaire": exemplaire,
            "exemplaires_lies": exemplaires_lies,
        },
    )

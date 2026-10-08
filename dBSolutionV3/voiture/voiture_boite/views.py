from django.urls import reverse
from django.views.decorators.cache import never_cache
from utilisateurs.models import UserLog
from voiture.voiture_boite.forms import VoitureBoiteForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import ProtectedError, RestrictedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _, gettext_noop

from core.suppression import analyser_suppression
from .models import VoitureBoite





@login_required
def liste_boite_view(request):
    boites = (
        VoitureBoite.objects
        .all()
        .order_by("fabricant", "nom_du_type")
    )

    return render(
        request,
        "voiture_boite/list.html",
        {
            "boites": boites,
        },
    )




@login_required
def ajouter_boite_view(request):
    tenant = request.user.societe

    if request.method == "POST":
        form = VoitureBoiteForm(
            request.POST,
            request.FILES or None,
        )

        if form.is_valid():
            boite = form.save(commit=False)
            boite.societe = tenant
            boite.save()
            form.save_m2m()

            messages.success(
                request,
                _("Boîte de vitesse ajoutée avec succès."),
            )
            return redirect(
                f"{reverse('voiture_boite:list')}?saved=1"
            )

        messages.error(
            request,
            _("Le formulaire contient des erreurs."),
        )

    else:
        form = VoitureBoiteForm()

    return render(
        request,
        "voiture_boite/ajouter_boite.html",
        {
            "form": form,
        },
    )



@never_cache
@login_required
def boite_detail_view(request, boite_id):
    boite = get_object_or_404(
        VoitureBoite,
        id=boite_id,
    )

    return render(
        request,
        "voiture_boite/boite_detail.html",
        {
            "boite": boite,
        },
    )




@login_required
def modifier_boite_view(request, boite_id):
    boite_instance = get_object_or_404(
        VoitureBoite,
        id=boite_id,
    )

    if request.method == "POST":
        form = VoitureBoiteForm(
            request.POST,
            request.FILES or None,
            instance=boite_instance,
        )

        if form.is_valid():
            boite = form.save()

            messages.success(
                request,
                _("Boîte de vitesse mise à jour avec succès."),
            )

            return redirect(
                f"{reverse('voiture_boite:boite_detail', kwargs={'boite_id': boite.id})}?saved=1"
            )

        messages.error(
            request,
            _("Le formulaire contient des erreurs."),
        )

    else:
        form = VoitureBoiteForm(instance=boite_instance)

    return render(
        request,
        "voiture_boite/modifier_boite.html",
        {
            "form": form,
            "boite": boite_instance,
        },
    )







ACTION_SUPPRESSION_BOITE = gettext_noop("Suppression de la boîte de vitesse")


@login_required
def delete_boite_view(request, pk):
    boite = get_object_or_404(
        VoitureBoite.objects.prefetch_related("voitures_exemplaires", "voitures_modeles"),
        pk=pk,
    )

    exemplaires_lies = list(boite.voitures_exemplaires.all())
    modeles_lies = list(boite.voitures_modeles.all())

    analyse = analyser_suppression(boite)
    objets_bloquants = analyse["bloquants"]
    objets_supprimes = analyse["supprimes"]

    if request.method == "POST":
        libelle = str(boite)

        if objets_bloquants:
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : elle est encore utilisée ailleurs.") % {"nom": libelle},
            )
            return redirect("voiture_boite:delete_boite", pk=pk)

        # Libellé pour le log (capturé AVANT la suppression)
        nom_log = " ".join(filter(None, [
            boite.fabricant,
            boite.nom_du_type,
            boite.get_type_de_boite_display() if boite.type_de_boite else None,
            f"{boite.nombre_rapport} rapports" if boite.nombre_rapport else None,
        ])) or f"#{boite.pk}"
        if boite.oem:
            nom_log += f" (OEM {boite.oem})"
        if exemplaires_lies:
            nom_log += " – véhicule(s) : " + ", ".join(str(v) for v in exemplaires_lies)

        try:
            with transaction.atomic():
                boite.delete()  # retire aussi les liens M2M (véhicules / modèles conservés)

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_BOITE} : {nom_log}",
                )
        except (ProtectedError, RestrictedError):
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : elle est encore utilisée ailleurs.") % {"nom": libelle},
            )
            return redirect("voiture_boite:delete_boite", pk=pk)

        messages.success(request, _("La boîte « %(nom)s » a bien été supprimée.") % {"nom": libelle})

        return redirect(
            f"{reverse('voiture_boite:list')}?deleted=1"
        )

    return render(
        request,
        "voiture_boite/delete_boite.html",
        {
            "boite": boite,
            "exemplaires_lies": exemplaires_lies,
            "modeles_lies": modeles_lies,
            "objets_supprimes": objets_supprimes,
            "objets_bloquants": objets_bloquants,
        },
    )
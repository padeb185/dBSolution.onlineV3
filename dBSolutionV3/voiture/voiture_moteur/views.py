from utilisateurs.models import UserLog
from .forms import MoteurVoitureForm
from .models import TypeCarburant, TypeMoteur, TypeDistribution
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import ProtectedError, RestrictedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _, gettext_noop

from core.suppression import analyser_suppression
from .models import MoteurVoiture








@login_required()
def moteur_detail_view(request, moteur_id):
    moteur = get_object_or_404(MoteurVoiture, id=moteur_id)
    return render(request, 'voiture_moteur/moteur_detail.html', {
        'moteur': moteur,
    })




@never_cache
@login_required
def liste_moteur(request):
    moteurs = MoteurVoiture.objects.all().order_by(
        "motoriste",
        "code_moteur",
    )

    return render(
        request,
        "voiture_moteur/list.html",
        {
            "moteurs": moteurs,
        },
    )



@login_required
def ajouter_moteur_view(request):

    if request.method == "POST":
        form = MoteurVoitureForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Moteur ajouté avec succès !")
            return redirect("voiture_moteur:list")

    else:
        form = MoteurVoitureForm()

    context = {
        "form": form,
        "TypeMoteur": TypeMoteur,
        "TypeCarburant": TypeCarburant,
        "TypeDistribution": TypeDistribution,
    }

    return render(request, "voiture_moteur/ajouter_moteur.html", context)

@login_required
def modifier_moteur_view(request, moteur_id):
    tenant = request.user.societe

    moteur = get_object_or_404(
        MoteurVoiture.objects.select_related(),
        id=moteur_id
    )

    if request.method == "POST":
        form = MoteurVoitureForm(request.POST, instance=moteur)
        if form.is_valid():
            form.save()
            messages.success(request, _("Moteur mis à jour avec succès."))
            return redirect("voiture_moteur:moteur_detail", moteur_id=moteur_id)

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = MoteurVoitureForm(instance=moteur)

    return render(
        request,
        "voiture_moteur/modifier_moteur.html",
        {
            "form": form,
            "moteur": moteur
        }
    )




ACTION_SUPPRESSION_MOTEUR = gettext_noop("Suppression du moteur")


@login_required
def delete_moteur_view(request, pk):
    moteur = get_object_or_404(
        MoteurVoiture.objects
        .select_related("boite")
        .prefetch_related("voitures_exemplaires", "voitures_modeles"),
        pk=pk,
    )

    exemplaires_lies = list(moteur.voitures_exemplaires.all())
    modeles_lies = list(moteur.voitures_modeles.all())

    analyse = analyser_suppression(moteur)
    objets_bloquants = analyse["bloquants"]
    objets_supprimes = analyse["supprimes"]

    if request.method == "POST":
        libelle = f"{moteur.motoriste} {moteur.code_moteur}"

        if objets_bloquants:
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : il est encore utilisé ailleurs.") % {"nom": libelle},
            )
            return redirect("voiture_moteur:delete_moteur", pk=pk)

        # Libellé pour le log (capturé AVANT la suppression)
        details = [
            f"{moteur.cylindree_l} L" if moteur.cylindree_l else None,
            moteur.get_type_moteur_display() if moteur.type_moteur else None,
            moteur.get_carburant_display() if moteur.carburant else None,
            f"{moteur.puissance_ch} ch" if moteur.puissance_ch else None,
        ]
        nom_log = libelle
        details = [d for d in details if d]
        if details:
            nom_log += " (" + ", ".join(details) + ")"
        if exemplaires_lies:
            nom_log += " – véhicule(s) : " + ", ".join(str(v) for v in exemplaires_lies)

        try:
            with transaction.atomic():
                moteur.delete()  # retire aussi les liens M2M (véhicules / modèles conservés)

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_MOTEUR} : {nom_log}",
                )
        except (ProtectedError, RestrictedError):
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : il est encore utilisé ailleurs.") % {"nom": libelle},
            )
            return redirect("voiture_moteur:delete_moteur", pk=pk)

        messages.success(request, _("Le moteur « %(nom)s » a bien été supprimé.") % {"nom": libelle})
        return redirect("voiture_moteur:list")

    return render(
        request,
        "voiture_moteur/delete_moteur.html",
        {
            "moteur": moteur,
            "exemplaires_lies": exemplaires_lies,
            "modeles_lies": modeles_lies,
            "objets_supprimes": objets_supprimes,
            "objets_bloquants": objets_bloquants,
        },
    )
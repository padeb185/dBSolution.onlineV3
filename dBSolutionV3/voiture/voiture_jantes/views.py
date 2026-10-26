import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _, gettext_noop
from django.views.decorators.cache import never_cache

from core.securite import url_sure
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire

from .forms import VoitureJanteForm
from .models import VoitureJante

ROLES_SUPPRESSION = ["direction", "chef_mecanicien"]


def _jantes_du_tenant(request):
    tenant = getattr(request.user, "societe", None)
    return VoitureJante.objects.filter(Q(societe=tenant) | Q(societe__isnull=True))


def _exemplaire_du_tenant(request, exemplaire_id):
    tenant = request.user.societe
    return get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
        ).select_related("voiture_marque", "voiture_modele"),
        id=exemplaire_id,
    )


def _log(request, action, jante):
    UserLog.objects.create(utilisateur=request.user, action=f"{action} - {jante}")


# ---------------------------------------------------------------- liste
@never_cache
@login_required
def liste_jantes(request):
    jantes = _jantes_du_tenant(request).annotate(nb_vehicules=Count("voitures_exemplaires", distinct=True))
    return render(request, "voiture_jantes/list.html", {"jantes": jantes})


# ---------------------------------------------------------------- ajout
@never_cache
@login_required
def ajouter_jante(request):
    exemplaire = None
    exemplaire_id = request.GET.get("exemplaire") or request.POST.get("exemplaire")
    if exemplaire_id:
        exemplaire = _exemplaire_du_tenant(request, exemplaire_id)

    if request.method == "POST":
        form = VoitureJanteForm(request.POST)
        if form.is_valid():
            jante = form.save(commit=False)
            jante.societe = request.user.societe
            jante.save()
            form.save_m2m()
            _log(request, gettext_noop("Ajout de jantes"), jante)

            if exemplaire:
                jante.voitures_exemplaires.add(exemplaire)
                messages.success(request, _("Les jantes « %(jante)s » ont été ajoutées et liées au véhicule.") % {"jante": jante})
                return redirect("voiture_jantes:lier_jantes", exemplaire_id=exemplaire.id)

            messages.success(request, _("Les jantes « %(jante)s » ont été ajoutées.") % {"jante": jante})
            return redirect("voiture_jantes:jante_detail", jante_id=jante.id)
        messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = VoitureJanteForm()

    return render(request, "voiture_jantes/form.html", {
        "form": form,
        "titre": _("Ajouter des jantes"),
        "exemplaire": exemplaire,
        "url_annuler": (
            reverse("voiture_jantes:lier_jantes", kwargs={"exemplaire_id": exemplaire.id})
            if exemplaire else reverse("voiture_jantes:list")
        ),
    })


# ---------------------------------------------------------------- détail
@never_cache
@login_required
def jante_detail(request, jante_id):
    jante = get_object_or_404(_jantes_du_tenant(request), id=jante_id)
    vehicules = jante.voitures_exemplaires.select_related("voiture_marque", "voiture_modele")
    return render(request, "voiture_jantes/detail.html", {
        "jante": jante,
        "vehicules": vehicules,
        "peut_supprimer": request.user.role in ROLES_SUPPRESSION or request.user.is_superuser,
    })


# ---------------------------------------------------------------- modification
@never_cache
@login_required
def modifier_jante(request, jante_id):
    jante = get_object_or_404(_jantes_du_tenant(request), id=jante_id)
    if request.method == "POST":
        form = VoitureJanteForm(request.POST, instance=jante)
        if form.is_valid():
            jante = form.save()
            _log(request, gettext_noop("Modification de jantes"), jante)
            messages.success(request, _("Les jantes ont été modifiées."))
            return redirect(
                url_sure(request.POST.get("next"), request)
                or reverse("voiture_jantes:jante_detail", kwargs={"jante_id": jante.id})
            )
        messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = VoitureJanteForm(instance=jante)

    return render(request, "voiture_jantes/form.html", {
        "form": form,
        "jante": jante,
        "titre": _("Modifier les jantes"),
        "url_annuler": reverse("voiture_jantes:jante_detail", kwargs={"jante_id": jante.id}),
        "next": request.GET.get("next", ""),
    })


# ---------------------------------------------------------------- suppression
@never_cache
@login_required
def supprimer_jante(request, jante_id):
    if request.user.role not in ROLES_SUPPRESSION and not request.user.is_superuser:
        messages.error(request, _("Accès refusé"))
        return redirect("voiture_jantes:jante_detail", jante_id=jante_id)

    jante = get_object_or_404(_jantes_du_tenant(request), id=jante_id)
    if request.method == "POST":
        libelle = str(jante)
        jante.delete()
        UserLog.objects.create(utilisateur=request.user, action=f"{gettext_noop('Suppression de jantes')} - {libelle}")
        messages.success(request, _("Les jantes ont été supprimées."))
        return redirect("voiture_jantes:list")

    return render(request, "voiture_jantes/delete.html", {
        "jante": jante,
        "nb_vehicules": jante.voitures_exemplaires.count(),
    })


# ---------------------------------------------------------------- lier à un véhicule
@never_cache
@login_required
def lier_jantes(request, exemplaire_id):
    exemplaire = _exemplaire_du_tenant(request, exemplaire_id)
    catalogue = _jantes_du_tenant(request)

    if request.method == "POST":
        action = request.POST.get("action")
        jante_id = request.POST.get("jante_id")
        try:
            jante = catalogue.get(id=uuid.UUID(str(jante_id))) if jante_id else None
        except (ValueError, VoitureJante.DoesNotExist):
            jante = None

        if not jante:
            messages.error(request, _("Veuillez sélectionner des jantes."))
        elif action == "retirer":
            jante.voitures_exemplaires.remove(exemplaire)
            messages.success(request, _("Les jantes « %(jante)s » ont été retirées du véhicule.") % {"jante": jante})
        else:
            jante.voitures_exemplaires.add(exemplaire)
            messages.success(request, _("Les jantes « %(jante)s » ont été liées au véhicule « %(vehicule)s ».") % {
                "jante": jante,
                "vehicule": f"{exemplaire.voiture_marque} {exemplaire.immatriculation}",
            })
        return redirect("voiture_jantes:lier_jantes", exemplaire_id=exemplaire.id)

    liees = exemplaire.jantes.all()
    disponibles = catalogue.exclude(id__in=liees.values("id"))
    return render(request, "voiture_jantes/lier.html", {
        "exemplaire": exemplaire,
        "liees": liees,
        "disponibles": disponibles,
    })

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from voiture.voiture_modele.models import VoitureModele
from .forms import DiagnosticForm
from .models import Diagnostic

# Mêmes autorisations que les maintenances (ex. checkup piste)
ROLES_LECTURE_ECRITURE = ["mecanicien", "apprenti", "magasinier", "chef_mecanicien", "direction"]
ROLES_SUPPRESSION = ["direction", "chef_mecanicien"]


def _autorise(user, roles):
    return user.is_superuser or getattr(user, "role", None) in roles


def _refus(request, message=None):
    messages.error(request, message or _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _queryset(request):
    return (
        Diagnostic.objects
        .filter(societe=request.user.societe)
        .select_related("voiture_marque", "voiture_modele")
    )


def _modeles_json(request):
    """Modèles par marque pour filtrer la liste des modèles dans le formulaire."""
    return [
        {"id": str(m.pk), "marque": str(m.voiture_marque_id)}
        for m in VoitureModele.objects.filter(societe=request.user.societe).only("pk", "voiture_marque_id")
    ]


@never_cache
@login_required
def diagnostic_liste(request):
    if not _autorise(request.user, ROLES_LECTURE_ECRITURE):
        return _refus(request, _(
            "Seuls les mécaniciens, apprentis, magasiniers "
            "et chefs mécaniciens peuvent accéder à cette page."
        ))

    return render(request, "voiture_diagnostic/diagnostic_list.html", {
        "diagnostics": _queryset(request),
        "peut_supprimer": _autorise(request.user, ROLES_SUPPRESSION),
    })


@never_cache
@login_required
def diagnostic_ajouter(request):
    if not _autorise(request.user, ROLES_LECTURE_ECRITURE):
        return _refus(request)

    initial = {}
    for champ in ("voiture_marque", "voiture_modele", "code_defaut"):
        if request.GET.get(champ):
            initial[champ] = request.GET[champ]

    form = DiagnosticForm(request.POST or None, user=request.user, initial=initial)
    if request.method == "POST" and form.is_valid():
        diagnostic = form.save()
        messages.success(request, _("Diagnostic '%(code)s' créé avec succès.") % {"code": diagnostic.code_defaut})
        return redirect("voiture_diagnostic:diagnostic_liste")

    return render(request, "voiture_diagnostic/diagnostic_form.html", {
        "form": form,
        "diagnostic": None,
        "modeles_json": _modeles_json(request),
    })


@never_cache
@login_required
def diagnostic_modifier(request, diagnostic_id):
    if not _autorise(request.user, ROLES_LECTURE_ECRITURE):
        return _refus(request)

    diagnostic = get_object_or_404(_queryset(request), id=diagnostic_id)
    form = DiagnosticForm(request.POST or None, instance=diagnostic, user=request.user)
    if request.method == "POST" and form.is_valid():
        diagnostic = form.save()
        messages.success(request, _("Diagnostic '%(code)s' mis à jour.") % {"code": diagnostic.code_defaut})
        return redirect("voiture_diagnostic:diagnostic_liste")

    return render(request, "voiture_diagnostic/diagnostic_form.html", {
        "form": form,
        "diagnostic": diagnostic,
        "modeles_json": _modeles_json(request),
    })


@never_cache
@login_required
def diagnostic_supprimer(request, diagnostic_id):
    if not _autorise(request.user, ROLES_SUPPRESSION):
        return _refus(request)

    diagnostic = get_object_or_404(_queryset(request), id=diagnostic_id)
    if request.method == "POST":
        try:
            diagnostic.delete()
            messages.success(request, _("Diagnostic supprimé."))
        except ProtectedError:
            messages.error(request, _("Impossible de supprimer ce diagnostic."))
        return redirect("voiture_diagnostic:diagnostic_liste")

    return render(request, "voiture_diagnostic/diagnostic_confirm_delete.html", {"diagnostic": diagnostic})

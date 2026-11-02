from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from utils.securite import peut_supprimer, refuser_suppression, roles_requis
from .forms import RemorqueForm
from .models import Remorque, TypeRemorque

ROLES_REMORQUES = ("chef_mecanicien", "chef_atelier", "direction", "mecanicien", "magasinier")
ROLES_GESTION = ("chef_mecanicien", "direction")


def _log(request, action):
    try:
        from utilisateurs.models import UserLog
        UserLog.objects.create(utilisateur=request.user, action=action)
    except Exception:
        pass


def _remorques(request):
    return Remorque.objects.filter(societe=request.user.societe)


@never_cache
@login_required
@roles_requis(*ROLES_REMORQUES)
def remorque_list(request):
    remorques = list(_remorques(request))
    return render(request, "voiture_remorque/remorque_list.html", {
        "remorques": remorques,
        "types": TypeRemorque.choices,
        "peut_gerer": request.user.is_superuser or request.user.role in ROLES_GESTION,
        "nb_actives": sum(1 for r in remorques if r.actif),
        "nb_ct": sum(1 for r in remorques if r.actif and (r.ct_depasse or r.ct_bientot)),
    })


@never_cache
@login_required
@roles_requis(*ROLES_REMORQUES)
def remorque_detail(request, pk):
    remorque = get_object_or_404(_remorques(request), pk=pk)
    return render(request, "voiture_remorque/remorque_detail.html", {
        "remorque": remorque,
        "peut_gerer": request.user.is_superuser or request.user.role in ROLES_GESTION,
    })


@never_cache
@login_required
@roles_requis(*ROLES_GESTION)
def remorque_form(request, pk=None):
    remorque = get_object_or_404(_remorques(request), pk=pk) if pk else None
    societe = request.user.societe
    if request.method == "POST":
        form = RemorqueForm(request.POST, instance=remorque, societe=societe)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.societe = societe
            obj.save()
            _log(request, f"{'Modification' if remorque else 'Ajout'} remorque {obj.immatriculation}")
            messages.success(request, _("La remorque a été enregistrée."))
            return redirect("voiture_remorque:remorque_detail", pk=obj.pk)
        messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = RemorqueForm(instance=remorque, societe=societe)
    return render(request, "voiture_remorque/remorque_form.html", {"form": form, "remorque": remorque})


@login_required
def remorque_supprimer(request, pk):
    if not peut_supprimer(request.user):
        return refuser_suppression(request)
    remorque = get_object_or_404(_remorques(request), pk=pk)
    if request.method == "POST":
        immat = remorque.immatriculation
        remorque.delete()
        _log(request, f"Suppression remorque {immat}")
        messages.success(request, _("La remorque %(immat)s a été supprimée.") % {"immat": immat})
        return redirect("voiture_remorque:remorque_list")
    return redirect("voiture_remorque:remorque_detail", pk=remorque.pk)

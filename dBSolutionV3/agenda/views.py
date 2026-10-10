from datetime import date as date_cls, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from maintenance.models import Maintenance

from .forms import AgendaTacheForm, AgendaTacheRapideForm, cle_alphabetique
from .models import AgendaTache

# Qui peut consulter l'agenda et mettre à jour tag / statut / prête pour
ROLES_AGENDA = ["mecanicien", "apprenti", "magasinier", "chef_mecanicien", "direction"]
# Qui peut planifier (ajouter, modifier, supprimer)
ROLES_PLANIFICATION = ["chef_mecanicien", "direction", "magasinier"]


def _peut(user, roles):
    return user.is_superuser or getattr(user, "role", None) in roles


def _taches_societe(request):
    return AgendaTache.objects.filter(societe=request.user.societe)


def _url_jour(jour):
    return reverse(
        "agenda:agenda_jour_date",
        kwargs={"annee": jour.year, "mois": jour.month, "jour": jour.day},
    )


def _jour_depuis_requete(request, annee=None, mois=None, jour=None):
    if annee and mois and jour:
        try:
            return date_cls(annee, mois, jour)
        except ValueError:
            pass
    valeur = request.GET.get("date")
    if valeur:
        try:
            return date_cls.fromisoformat(valeur)
        except ValueError:
            pass
    return timezone.localdate()


# -----------------------------
# Page d'un jour
# -----------------------------
@never_cache
@login_required
def agenda_jour_view(request, annee=None, mois=None, jour=None):
    if not _peut(request.user, ROLES_AGENDA):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    jour_affiche = _jour_depuis_requete(request, annee, mois, jour)

    taches = (
        _taches_societe(request)
        .filter(date=jour_affiche)
        .select_related("voiture_exemplaire", "voiture_exemplaire__voiture_modele", "technicien")
    )

    # Filtre « mes tâches »
    mes_taches = request.GET.get("moi") == "1"
    if mes_taches:
        taches = taches.filter(technicien=request.user)

    # Maintenances du jour par ordre alphabétique, puis par immatriculation
    taches_triees = sorted(
        taches,
        key=lambda t: (cle_alphabetique(t.get_type_maintenance_display()), cle_alphabetique(t.immatriculation)),
    )
    lignes = [
        {"tache": t, "form": AgendaTacheRapideForm(instance=t, prefix=f"t{t.pk}")}
        for t in taches_triees
    ]

    return render(request, "agenda/agenda_list.html", {
        "jour": jour_affiche,
        "aujourdhui": timezone.localdate(),
        "url_veille": _url_jour(jour_affiche - timedelta(days=1)),
        "url_lendemain": _url_jour(jour_affiche + timedelta(days=1)),
        "url_aujourdhui": _url_jour(timezone.localdate()),
        "lignes": lignes,
        "mes_taches": mes_taches,
        "peut_planifier": _peut(request.user, ROLES_PLANIFICATION),
        "nb_faites": sum(
            1 for t in taches
            if (t.est_checkup_track and t.prete_pour) or (not t.est_checkup_track and t.statut == AgendaTache.Statut.FAIT)
        ),
    })


# -----------------------------
# Ajout
# -----------------------------
@never_cache
@login_required
def ajouter_tache_view(request):
    if not _peut(request.user, ROLES_PLANIFICATION):
        messages.error(request, _("Accès refusé"))
        return redirect("agenda:agenda_jour")

    jour = _jour_depuis_requete(request)

    if request.method == "POST":
        form = AgendaTacheForm(request.POST, user=request.user)
        if form.is_valid():
            tache = form.save(commit=False)
            tache.societe = request.user.societe
            tache.cree_par = request.user
            tache.save()
            messages.success(request, _("Maintenance ajoutée à l'agenda."))
            return redirect(_url_jour(tache.date))
        messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = AgendaTacheForm(
            user=request.user,
            initial={"date": jour, "tag": Maintenance.Tag.JAUNE},
        )

    return render(request, "agenda/agenda_form.html", {
        "form": form,
        "titre": _("Planifier une maintenance"),
        "url_retour": _url_jour(jour),
        "code_checkup_track": Maintenance.TypeMaintenance.CHECKUP_TRACK,
    })


# -----------------------------
# Modification complète
# -----------------------------
@never_cache
@login_required
def modifier_tache_view(request, tache_id):
    if not _peut(request.user, ROLES_PLANIFICATION):
        messages.error(request, _("Accès refusé"))
        return redirect("agenda:agenda_jour")

    tache = get_object_or_404(_taches_societe(request), pk=tache_id)

    if request.method == "POST":
        form = AgendaTacheForm(request.POST, instance=tache, user=request.user)
        if form.is_valid():
            tache = form.save()
            messages.success(request, _("Maintenance modifiée."))
            return redirect(_url_jour(tache.date))
        messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = AgendaTacheForm(instance=tache, user=request.user)

    return render(request, "agenda/agenda_form.html", {
        "form": form,
        "tache": tache,
        "titre": _("Modifier la maintenance planifiée"),
        "url_retour": _url_jour(tache.date),
        "code_checkup_track": Maintenance.TypeMaintenance.CHECKUP_TRACK,
    })


# -----------------------------
# Mise à jour rapide depuis la page du jour (tag, statut, prête pour)
# -----------------------------
@login_required
@require_POST
def maj_rapide_tache_view(request, tache_id):
    tache = get_object_or_404(_taches_societe(request), pk=tache_id)

    if not _peut(request.user, ROLES_AGENDA):
        messages.error(request, _("Accès refusé"))
        return redirect(_url_jour(tache.date))

    form = AgendaTacheRapideForm(request.POST, instance=tache, prefix=f"t{tache.pk}")
    if form.is_valid():
        tache = form.save(commit=False)
        if not tache.est_checkup_track:
            tache.prete_pour = ""
        tache.save(update_fields=["tag", "statut", "prete_pour", "updated_at"])
        messages.success(request, _("Maintenance mise à jour."))
    else:
        messages.error(request, _("Mise à jour impossible."))

    url = _url_jour(tache.date)
    if request.POST.get("moi") == "1":
        url += "?moi=1"
    return redirect(url)


# -----------------------------
# Suppression
# -----------------------------
@login_required
@require_POST
def supprimer_tache_view(request, tache_id):
    tache = get_object_or_404(_taches_societe(request), pk=tache_id)
    jour = tache.date

    if not _peut(request.user, ROLES_PLANIFICATION):
        messages.error(request, _("Accès refusé"))
        return redirect(_url_jour(jour))

    tache.delete()
    messages.success(request, _("Maintenance retirée de l'agenda."))
    return redirect(_url_jour(jour))

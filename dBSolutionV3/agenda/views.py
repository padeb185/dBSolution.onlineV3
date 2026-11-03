from datetime import date as date_cls, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import ProtectedError, RestrictedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, gettext_noop
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from core.suppression import analyser_suppression
from maintenance.models import Maintenance
from utilisateurs.models import UserLog

from .forms import AgendaTacheForm, AgendaTacheRapideForm, cle_alphabetique
from .models import AgendaTache

# Qui peut consulter l'agenda et mettre à jour tag / statut / prête pour
ROLES_AGENDA = ["mecanicien", "apprenti", "apprentis", "magasinier", "chef_mecanicien", "chef_atelier", "direction"]
# Qui peut planifier (ajouter, modifier, supprimer)
ROLES_PLANIFICATION = ["chef_mecanicien", "chef_atelier", "direction", "magasinier"]
# Qui peut supprimer (+ super admin via _peut)
ROLES_SUPPRESSION = ["chef_mecanicien", "direction"]


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
        .select_related("voiture_exemplaire", "voiture_exemplaire__voiture_modele",
                        "voiture_exemplaire__voiture_modele__voiture_marque", "technicien")
    )
    nb_total = taches.count()

    f = _filtres_agenda(request)
    if f["moi"]:
        taches = taches.filter(technicien=request.user)
    if f["type"]:
        taches = taches.filter(type_maintenance=f["type"])
    if f["tag"]:
        taches = taches.filter(tag=f["tag"])
    if f["tech"] == "aucun":
        taches = taches.filter(technicien__isnull=True)
    elif f["tech"]:
        taches = taches.filter(technicien_id=f["tech"])

    taches = list(taches)
    if f["statut"]:
        taches = [t for t in taches if _statut_filtre(t) == f["statut"]
                  or (f["statut"] == "non_terminees" and not t.est_terminee)]
    # Recherche texte : instantanée dans la page (agenda/partials/recherche_live.html)

    # Tri (par défaut : maintenance puis immatriculation)
    cle = TRIS_AGENDA.get(f["tri"], TRIS_AGENDA["maintenance"])
    taches_triees = sorted(taches, key=lambda t: (cle(t), cle_alphabetique(t.immatriculation)),
                           reverse=f["ordre"] == "desc")
    lignes = [
        {"tache": t, "form": AgendaTacheRapideForm(instance=t, prefix=f"t{t.pk}")}
        for t in taches_triees
    ]

    # Liens : on garde les filtres en changeant de jour ou de tri
    params = request.GET.copy()
    params.pop("date", None)
    suffixe = f"?{params.urlencode()}" if params else ""
    entetes = {}
    for col in TRIS_AGENDA:
        p = params.copy()
        p["tri"] = col
        p["ordre"] = "desc" if f["tri"] == col and f["ordre"] == "asc" else "asc"
        entetes[col] = {"url": f"?{p.urlencode()}", "actif": f["tri"] == col, "ordre": f["ordre"]}

    from django.contrib.auth import get_user_model
    techniciens = get_user_model().objects.filter(
        societe=request.user.societe, is_active=True, role__in=ROLES_AGENDA).order_by("prenom", "nom")

    return render(request, "agenda/agenda_list.html", {
        "jour": jour_affiche,
        "aujourdhui": timezone.localdate(),
        "url_veille": _url_jour(jour_affiche - timedelta(days=1)) + suffixe,
        "url_lendemain": _url_jour(jour_affiche + timedelta(days=1)) + suffixe,
        "url_aujourdhui": _url_jour(timezone.localdate()) + suffixe,
        "url_sans_filtre": _url_jour(jour_affiche),
        "lignes": lignes,
        "mes_taches": f["moi"],
        "filtres": f,
        "filtres_actifs": any(f[k] for k in ("type", "tag", "tech", "statut", "q")),
        "params_caches": [(k, v) for k, v in params.items() if k not in ("date",)],
        "entetes": entetes,
        "nb_total": nb_total,
        "types_maintenance": sorted(Maintenance.TypeMaintenance.choices, key=lambda c: cle_alphabetique(c[1])),
        "tags": Maintenance.Tag.choices,
        "statuts": [("non_terminees", _("Non terminées")), ("A_FAIRE", _("À faire")),
                    ("EN_COURS", _("En cours")), ("FAIT", _("Terminées"))],
        "techniciens": techniciens,
        "peut_planifier": _peut(request.user, ROLES_PLANIFICATION),
        "nb_faites": sum(1 for t in taches if t.est_terminee),
    })


ORDRE_TAG = {"ROUGE": 0, "JAUNE": 1, "VERT": 2}
ORDRE_STATUT = {"A_FAIRE": 0, "EN_COURS": 1, "FAIT": 2}


def _statut_filtre(t):
    """Statut comparable pour toutes les tâches (checkup piste : terminé quand le tag est vert)."""
    if t.est_checkup_track:
        return "FAIT" if t.est_terminee else "A_FAIRE"
    return t.statut


TRIS_AGENDA = {
    "maintenance": lambda t: cle_alphabetique(t.get_type_maintenance_display()),
    "immatriculation": lambda t: cle_alphabetique(t.immatriculation),
    "vehicule": lambda t: cle_alphabetique(" ".join(str(x or "") for x in (
        getattr(getattr(getattr(t.voiture_exemplaire, "voiture_modele", None), "voiture_marque", None), "nom_marque", ""),
        getattr(getattr(t.voiture_exemplaire, "voiture_modele", None), "nom_modele", "")))),
    # Non assigné en premier : c'est ce qui reste à organiser
    "technicien": lambda t: cle_alphabetique(f"{t.technicien.prenom} {t.technicien.nom}") if t.technicien else "",
    "tag": lambda t: ORDRE_TAG.get(t.tag, 9),
    "statut": lambda t: ORDRE_STATUT.get(_statut_filtre(t), 9),
}


def _filtres_agenda(request):
    g = request.GET
    tri = g.get("tri", "maintenance")
    return {
        "moi": g.get("moi") == "1",
        "type": g.get("type", "") if g.get("type", "") in Maintenance.TypeMaintenance.values else "",
        "tag": g.get("tag", "") if g.get("tag", "") in Maintenance.Tag.values else "",
        "tech": g.get("tech", "") if g.get("tech", "") == "aucun" or g.get("tech", "").isdigit()
                or _est_uuid(g.get("tech", "")) else "",
        "statut": g.get("statut", "") if g.get("statut", "") in ("non_terminees", "A_FAIRE", "EN_COURS", "FAIT") else "",
        "q": g.get("q", "").strip()[:100],
        "tri": tri if tri in TRIS_AGENDA else "maintenance",
        "ordre": "desc" if g.get("ordre") == "desc" else "asc",
    }


def _est_uuid(valeur):
    import uuid
    try:
        uuid.UUID(str(valeur))
        return True
    except ValueError:
        return False


# -----------------------------
# Détail
# -----------------------------
@never_cache
@login_required
def detail_tache_view(request, tache_id):
    if not _peut(request.user, ROLES_AGENDA):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    tache = get_object_or_404(
        _taches_societe(request).select_related(
            "voiture_exemplaire",
            "voiture_exemplaire__voiture_marque",
            "voiture_exemplaire__voiture_modele",
            "technicien",
            "cree_par",
        ),
        pk=tache_id,
    )

    return render(request, "agenda/agenda_detail.html", {
        "tache": tache,
        "exemplaire": tache.voiture_exemplaire,
        "url_retour": _url_jour(tache.date),
        "peut_planifier": _peut(request.user, ROLES_PLANIFICATION),
        "peut_supprimer": _peut(request.user, ROLES_SUPPRESSION),
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
            return redirect("agenda:detail_tache", tache_id=tache.pk)
        messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = AgendaTacheForm(instance=tache, user=request.user)

    return render(request, "agenda/agenda_form.html", {
        "form": form,
        "tache": tache,
        "titre": _("Modifier la maintenance planifiée"),
        "url_retour": reverse("agenda:detail_tache", kwargs={"tache_id": tache.pk}),
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

    from django.utils.http import url_has_allowed_host_and_scheme
    retour = request.POST.get("retour", "")
    if retour and url_has_allowed_host_and_scheme(retour, allowed_hosts={request.get_host()},
                                                   require_https=request.is_secure()):
        return redirect(retour)
    url = _url_jour(tache.date)
    if request.POST.get("moi") == "1":
        url += "?moi=1"
    return redirect(url)


# -----------------------------
# Suppression (page de confirmation, comme voiture_boite / voiture_exemplaire)
# -----------------------------
ACTION_SUPPRESSION_AGENDA = gettext_noop("Suppression d'une maintenance planifiée")


@never_cache
@login_required
def delete_agenda_view(request, tache_id):
    tache = get_object_or_404(
        _taches_societe(request).select_related(
            "voiture_exemplaire",
            "voiture_exemplaire__voiture_marque",
            "voiture_exemplaire__voiture_modele",
            "technicien",
            "cree_par",
        ),
        pk=tache_id,
    )
    jour = tache.date

    if not _peut(request.user, ROLES_SUPPRESSION):
        messages.error(request, _("Accès refusé"))
        return redirect("agenda:detail_tache", tache_id=tache.pk)

    analyse = analyser_suppression(tache)
    objets_bloquants = analyse["bloquants"]
    objets_supprimes = analyse["supprimes"]

    if request.method == "POST":
        libelle = f"{tache.get_type_maintenance_display()} – {tache.immatriculation or '—'} ({jour:%d/%m/%Y})"

        if objets_bloquants:
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : elle est encore utilisée ailleurs.") % {"nom": libelle},
            )
            return redirect("agenda:delete_agenda", tache_id=tache.pk)

        # Libellé pour le log (capturé AVANT la suppression)
        nom_log = libelle
        if tache.technicien:
            nom_log += f" – {tache.technicien.prenom} {tache.technicien.nom}"

        try:
            with transaction.atomic():
                tache.delete()
                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_AGENDA} : {nom_log}",
                )
        except (ProtectedError, RestrictedError):
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : elle est encore utilisée ailleurs.") % {"nom": libelle},
            )
            return redirect("agenda:delete_agenda", tache_id=tache.pk)

        messages.success(request, _("La maintenance « %(nom)s » a bien été retirée de l'agenda.") % {"nom": libelle})
        return redirect(_url_jour(jour))

    return render(request, "agenda/delete_agenda.html", {
        "tache": tache,
        "exemplaire": tache.voiture_exemplaire,
        "objets_supprimes": objets_supprimes,
        "objets_bloquants": objets_bloquants,
        "url_annuler": reverse("agenda:detail_tache", kwargs={"tache_id": tache.pk}),
    })

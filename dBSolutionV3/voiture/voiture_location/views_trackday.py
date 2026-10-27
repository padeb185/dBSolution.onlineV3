"""Trackday : événement circuit regroupant des locations (1 véhicule = 1 location)."""
from collections import OrderedDict
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop
from django.views.decorators.cache import never_cache

from .forms import TrackdayCoutFormSet, TrackdayForm
from .models import CircuitEuropeen, Trackday
from .views import ROLES_SUPPRESSION, _autorise, _voit_tout

ZERO = Decimal("0.00")


def _refus(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _trackdays(request):
    return Trackday.objects.filter(societe=request.user.societe).prefetch_related("couts")


def _log(user, action, trackday):
    from utilisateurs.models import UserLog
    UserLog.objects.create(utilisateur=user, action=f"{action} - {trackday}"[:255])


def _annee(request):
    try:
        return int(request.GET.get("annee") or timezone.localdate().year)
    except ValueError:
        return timezone.localdate().year


# ------------------------------------------------------------------ liste
@never_cache
@login_required
def trackday_liste(request):
    if not _autorise(request.user):
        return _refus(request)
    annee = request.GET.get("annee") or ""
    trackdays = _trackdays(request)
    if annee.isdigit():
        trackdays = trackdays.filter(date_debut__year=int(annee))
    lignes = [{"t": t, **t.rentabilite()} for t in trackdays]
    return render(request, "voiture_location/trackday/liste.html", {
        "lignes": lignes, "annee": annee,
        "annees": range(timezone.localdate().year - 5, timezone.localdate().year + 2),
        "voit_rentabilite": _voit_tout(request.user),
        "aujourdhui": timezone.localdate(),
    })


# ------------------------------------------------------------------ création / modification
def _trackday_form(request, trackday=None):
    instance = trackday or Trackday(societe=request.user.societe)
    form = TrackdayForm(request.POST or None, instance=instance)
    couts_fs = TrackdayCoutFormSet(request.POST or None, instance=instance, prefix="cout")
    if request.method == "POST":
        if form.is_valid() and couts_fs.is_valid():
            with transaction.atomic():
                obj = form.save(commit=False)
                obj.societe = request.user.societe
                if not obj.cree_par_id:
                    obj.cree_par = request.user
                obj.save()
                couts_fs.instance = obj
                couts_fs.save()
            _log(request.user, gettext_noop("Trackday") if trackday is None else gettext_noop("Modification du Trackday"), obj)
            messages.success(request, _("Trackday « %(t)s » enregistré.") % {"t": obj})
            return redirect("voiture_location:trackday_detail", pk=obj.pk)
        messages.error(request, _("Le formulaire contient des erreurs."))
    return render(request, "voiture_location/trackday/form.html", {
        "form": form, "couts_fs": couts_fs, "trackday": trackday,
        "voit_couts": _voit_tout(request.user),
    })


@never_cache
@login_required
def trackday_ajouter(request):
    if not _autorise(request.user):
        return _refus(request)
    return _trackday_form(request)


@never_cache
@login_required
def trackday_modifier(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    return _trackday_form(request, get_object_or_404(_trackdays(request), pk=pk))


@login_required
def trackday_supprimer(request, pk):
    if not (request.user.is_superuser or getattr(request.user, "role", None) in ROLES_SUPPRESSION):
        return _refus(request)
    trackday = get_object_or_404(_trackdays(request), pk=pk)
    if request.method == "POST":
        libelle = str(trackday)
        trackday.locations.update(numero_course=None)
        trackday.delete()  # les locations sont conservées (ventes), sans Trackday
        from utilisateurs.models import UserLog
        UserLog.objects.create(utilisateur=request.user, action=f"Suppression du Trackday - {libelle}"[:255])
        messages.success(request, _("Trackday supprimé. Les locations sont conservées."))
        return redirect("voiture_location:trackday_liste")
    return render(request, "voiture_location/trackday/supprimer.html", {"trackday": trackday})


# ------------------------------------------------------------------ détail
def _ligne_vehicule(loc):
    """Infos d'un véhicule engagé : pilotes, box, km départ, km / tours réservés."""
    try:
        agenda = loc.agenda_location
    except Exception:
        agenda = None
    km_depart = agenda.kilometrage_avant if agenda and agenda.kilometrage_avant is not None else None
    pilote1 = loc.locataire
    if getattr(pilote1, "client_particulier", None) is not None:
        pilote1 = pilote1.client_particulier
    return {
        "loc": loc,
        "exemplaire": loc.voiture_exemplaire,
        "pilote1": pilote1,
        "pilote2": loc.deuxieme_pilote_nom if loc.deuxieme_pilote else "",
        "boxes": list(loc.boxes.all()),
        "km_depart": km_depart,
        "km_actuel": loc.voiture_exemplaire.kilometres_chassis,
        "sortie": bool(agenda and agenda.sortie_effectuee),
        "retour": bool(agenda and agenda.retour_effectue),
    }


@never_cache
@login_required
def trackday_detail(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    trackday = get_object_or_404(_trackdays(request), pk=pk)
    lignes = [_ligne_vehicule(l) for l in trackday.locations_liste()]
    sans_numero = [l for l in lignes if not l["loc"].numero_course]

    # Ventes par vendeur sur ce Trackday
    vendeurs = OrderedDict()
    for l in trackday.locations_liste():
        v = vendeurs.setdefault(l.vendeur_id, {"vendeur": l.vendeur, "nb": 0, "htva": ZERO, "tvac": ZERO})
        v["nb"] += 1
        v["htva"] += l.prix_htva
        v["tvac"] += l.prix_tvac

    return render(request, "voiture_location/trackday/detail.html", {
        "trackday": trackday, "lignes": lignes, "sans_numero": sans_numero,
        "r": trackday.rentabilite(), "plan_box": trackday.plan_box(),
        "vendeurs": sorted(vendeurs.values(), key=lambda v: v["tvac"], reverse=True),
        "voit_rentabilite": _voit_tout(request.user),
        "peut_supprimer": request.user.is_superuser or getattr(request.user, "role", None) in ROLES_SUPPRESSION,
    })


@never_cache
@login_required
def trackday_affichage(request, pk):
    """Liste des véhicules par numéro, en grand (écran du paddock / impression)."""
    if not _autorise(request.user):
        return _refus(request)
    trackday = get_object_or_404(_trackdays(request), pk=pk)
    lignes = [_ligne_vehicule(l) for l in trackday.locations_liste()]
    lignes.sort(key=lambda l: (l["loc"].numero_course is None, l["loc"].numero_course or 0))
    return render(request, "voiture_location/trackday/affichage.html", {"trackday": trackday, "lignes": lignes})


# ------------------------------------------------------------------ statistiques
@never_cache
@login_required
def trackday_statistiques(request):
    if not _voit_tout(request.user):
        return _refus(request)
    annee = _annee(request)
    trackdays = list(_trackdays(request).filter(date_debut__year=annee))
    lignes = [{"t": t, **t.rentabilite()} for t in trackdays]

    cles = ("nb_vehicules", "nb_box", "ventes_htva", "ventes_tvac", "couts_htva", "marge", "tours", "km")
    totaux = {k: sum((l[k] for l in lignes), ZERO if k in ("ventes_htva", "ventes_tvac", "couts_htva", "marge") else 0)
              for k in cles}
    totaux["nb"] = len(lignes)
    totaux["marge_pct"] = (totaux["marge"] * 100 / totaux["ventes_htva"]).quantize(Decimal("0.1")) if totaux["ventes_htva"] else None
    totaux["vehicules_moyen"] = (Decimal(totaux["nb_vehicules"]) / len(lignes)).quantize(Decimal("0.1")) if lignes else 0

    # Par circuit
    circuits = OrderedDict()
    for l in lignes:
        c = circuits.setdefault(l["t"].circuit, {"circuit": l["t"].get_circuit_display(), "nb": 0, "nb_vehicules": 0,
                                                 "ventes_htva": ZERO, "couts_htva": ZERO, "marge": ZERO})
        c["nb"] += 1
        for k in ("nb_vehicules", "ventes_htva", "couts_htva", "marge"):
            c[k] += l[k]
    par_circuit = sorted(circuits.values(), key=lambda c: c["marge"], reverse=True)
    for c in par_circuit:
        c["marge_pct"] = (c["marge"] * 100 / c["ventes_htva"]).quantize(Decimal("0.1")) if c["ventes_htva"] else None

    # Par mois
    mois = OrderedDict()
    for l in sorted(lignes, key=lambda x: x["t"].date_debut):
        m = mois.setdefault(l["t"].date_debut.month, {"date": l["t"].date_debut.replace(day=1), "nb": 0,
                                                       "nb_vehicules": 0, "ventes_htva": ZERO, "marge": ZERO})
        m["nb"] += 1
        m["nb_vehicules"] += l["nb_vehicules"]
        m["ventes_htva"] += l["ventes_htva"]
        m["marge"] += l["marge"]
    max_mois = max((m["ventes_htva"] for m in mois.values()), default=ZERO)
    for m in mois.values():
        m["largeur"] = int(m["ventes_htva"] * 100 / max_mois) if max_mois else 0

    return render(request, "voiture_location/trackday/statistiques.html", {
        "annee": annee, "annees": range(timezone.localdate().year - 5, timezone.localdate().year + 2),
        "lignes": sorted(lignes, key=lambda l: l["t"].date_debut), "totaux": totaux,
        "par_circuit": par_circuit, "par_mois": list(mois.values()),
    })

"""
Planning des coachings instructeurs : locations (pilotage) avec un instructeur, semaine par semaine.

Instructeurs : rôles instructeur / instructeur externe, et direction / vendeurs avec l'option
« Peut être instructeur » (utilisateurs.models.q_instructeurs).
- L'atelier, la direction et les vendeurs voient le planning de tous les instructeurs.
- Un instructeur voit son propre planning.
Deux coachings du même instructeur qui se chevauchent le même jour sont signalés (conflit).
"""
from datetime import time, timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache

from utilisateurs.models import Utilisateur, q_instructeurs
from voiture.voiture_location.models import Location

from .views import _jour_depuis_requete, _peut
from .views_location import ROLES_AGENDA_LOCATION, _refuser, nom_client


def acces_coachings(user):
    return _peut(user, ROLES_AGENDA_LOCATION) or bool(getattr(user, "peut_instruire", False))


def voit_tous_les_coachings(user):
    return _peut(user, ROLES_AGENDA_LOCATION)


def _url_semaine(jour):
    return reverse("agenda:agenda_coaching_date", kwargs={"annee": jour.year, "mois": jour.month, "jour": jour.day})


def coachings_periode(societe, debut, fin, instructeur=None):
    """Locations avec instructeur qui touchent la période [debut, fin] (date de fin vide = un seul jour)."""
    qs = (
        Location.objects.filter(societe=societe, instructeur__isnull=False, date_debut__lte=fin)
        .filter(Q(date_fin__gte=debut) | Q(date_fin__isnull=True, date_debut__gte=debut))
        .select_related(
            "instructeur", "voiture_exemplaire", "voiture_exemplaire__voiture_marque",
            "voiture_exemplaire__voiture_modele", "client", "societe_cliente",
            "client_pilotage", "client_pilotage__client_particulier",
        )
    )
    if instructeur is not None:
        qs = qs.filter(instructeur=instructeur)
    return list(qs)


def _se_chevauchent(a, b):
    """Même jour, même instructeur : chevauchement si les heures se recoupent (heure inconnue = conflit)."""
    la, lb = a["location"], b["location"]
    if not (la.heure_debut and la.heure_fin and lb.heure_debut and lb.heure_fin):
        return True
    return la.heure_debut < lb.heure_fin and lb.heure_debut < la.heure_fin


def lignes_du_jour(locations, jour):
    lignes = []
    for loc in locations:
        fin = loc.date_fin or loc.date_debut
        if not (loc.date_debut <= jour <= fin):
            continue
        nb_jours = (fin - loc.date_debut).days + 1
        lignes.append({
            "location": loc,
            "instructeur": loc.instructeur,
            "client": nom_client(loc),
            "nb_jours": nb_jours,
            "jour_n": (jour - loc.date_debut).days + 1,
            "conflit": False,
        })
    for i, a in enumerate(lignes):
        for b in lignes[i + 1:]:
            if a["instructeur"].pk == b["instructeur"].pk and _se_chevauchent(a, b):
                a["conflit"] = b["conflit"] = True
    lignes.sort(key=lambda l: (l["location"].heure_debut or time.min,
                               l["instructeur"].nom or "", l["instructeur"].prenom or ""))
    return lignes


def _totaux(locations):
    """Par instructeur (chaque location comptée une fois) : nombre de coachings, heures, montant TVAC."""
    par = {}
    for loc in locations:
        t = par.setdefault(loc.instructeur_id, {"instructeur": loc.instructeur, "nombre": 0,
                                                 "heures": Decimal("0"), "montant": Decimal("0")})
        t["nombre"] += 1
        t["heures"] += Decimal(str(loc.instructeur_heures or 0))
        t["montant"] += loc.total_instructeur_tvac or Decimal("0")
    return sorted(par.values(), key=lambda t: (t["instructeur"].nom or "", t["instructeur"].prenom or ""))


@never_cache
@login_required
def agenda_coaching_view(request, annee=None, mois=None, jour=None):
    user = request.user
    if not acces_coachings(user):
        return _refuser(request)

    jour_affiche = _jour_depuis_requete(request, annee, mois, jour)
    lundi = jour_affiche - timedelta(days=jour_affiche.weekday())
    dimanche = lundi + timedelta(days=6)
    aujourdhui = timezone.localdate()
    tout_voir = voit_tous_les_coachings(user)

    instructeurs = Utilisateur.objects.filter(q_instructeurs(), societe=user.societe, is_active=True) \
        .order_by("nom", "prenom")
    instructeur = None
    if not tout_voir:
        instructeur = user                                  # un instructeur : son propre planning
    elif request.GET.get("instructeur"):
        instructeur = instructeurs.filter(pk=request.GET["instructeur"]).first()

    locations = coachings_periode(user.societe, lundi, dimanche, instructeur)
    jours = [{"date": lundi + timedelta(days=i)} for i in range(7)]
    for j in jours:
        j["lignes"] = lignes_du_jour(locations, j["date"])
    nb_conflits = sum(1 for j in jours for l in j["lignes"] if l["conflit"])

    suffixe = f"?instructeur={instructeur.pk}" if tout_voir and instructeur else ""
    return render(request, "agenda/agenda_coaching.html", {
        "jour": jour_affiche,
        "lundi": lundi,
        "dimanche": dimanche,
        "aujourdhui": aujourdhui,
        "jours": jours,
        "totaux": _totaux(locations),
        "nb_coachings": len(locations),
        "nb_conflits": nb_conflits,
        "instructeurs": instructeurs if tout_voir else [],
        "instructeur": instructeur,
        "tout_voir": tout_voir,
        "url_precedente": _url_semaine(lundi - timedelta(days=7)) + suffixe,
        "url_suivante": _url_semaine(lundi + timedelta(days=7)) + suffixe,
        "url_cette_semaine": _url_semaine(aujourdhui) + suffixe,
    })

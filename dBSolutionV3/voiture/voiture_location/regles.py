"""
Règles de location :
  • une voiture ne peut pas être louée deux fois sur le même jour / créneau horaire ;
  • les interdictions de location (véhicule ou tous les véhicules, période, créneau, jours) bloquent la location.

Créneau d'une location : du (date_debut, heure_debut ou 00:00) au (date_fin ou date_debut, heure_fin ou 24:00).
Créneau d'une interdiction : chaque jour de la période (filtré sur les jours de la semaine choisis),
de heure_debut (ou 00:00) à heure_fin (ou 24:00).
"""
from datetime import datetime, time, timedelta

from django.db.models import Q
from django.utils.translation import gettext as _

MAX_JOURS = 400


def intervalle(date_debut, date_fin=None, heure_debut=None, heure_fin=None):
    debut = datetime.combine(date_debut, heure_debut or time.min)
    jour_fin = date_fin or date_debut
    fin = datetime.combine(jour_fin, heure_fin) if heure_fin else datetime.combine(jour_fin + timedelta(days=1), time.min)
    return debut, fin


def chevauche(a, b):
    return a[0] < b[1] and b[0] < a[1]


def _creneau(h1, h2):
    if not h1 and not h2:
        return _("journée entière")
    return "{}–{}".format(h1.strftime("%H:%M") if h1 else "00:00", h2.strftime("%H:%M") if h2 else "24:00")


def _intervalles_interdiction(interdiction, borne_debut, borne_fin):
    """Créneaux journaliers de l'interdiction compris entre deux dates."""
    jour = max(interdiction.date_debut, borne_debut)
    dernier = min(interdiction.date_fin or interdiction.date_debut, borne_fin)
    jours = set(interdiction.jours_liste)
    n = 0
    while jour <= dernier and n < MAX_JOURS:
        if not jours or jour.weekday() in jours:
            yield jour, intervalle(jour, None, interdiction.heure_debut, interdiction.heure_fin)
        jour += timedelta(days=1)
        n += 1


def conflits(societe, voiture, date_debut, date_fin=None, heure_debut=None, heure_fin=None, exclure_pk=None):
    """
    Liste des conflits pour une location envisagée :
    [{"type": "location" | "interdiction", "message": str, "objet": obj}]
    """
    if not (societe and voiture and date_debut):
        return []
    from .models import InterdictionLocation, Location

    voiture_id = getattr(voiture, "pk", voiture)
    souhait = intervalle(date_debut, date_fin, heure_debut, heure_fin)
    jour_fin = date_fin or date_debut
    resultat = []

    # ---- Locations du même véhicule
    locations = (Location.objects.filter(societe=societe, voiture_exemplaire_id=voiture_id, date_debut__lte=jour_fin)
                 .filter(Q(date_fin__gte=date_debut) | Q(date_fin__isnull=True, date_debut__gte=date_debut))
                 .select_related("client", "societe_cliente", "client_pilotage__client_particulier"))
    if exclure_pk:
        locations = locations.exclude(pk=exclure_pk)
    for loc in locations:
        if chevauche(souhait, intervalle(loc.date_debut, loc.date_fin, loc.heure_debut, loc.heure_fin)):
            dates = f"{loc.date_debut:%d/%m/%Y}"
            if loc.date_fin and loc.date_fin != loc.date_debut:
                dates += f" → {loc.date_fin:%d/%m/%Y}"
            resultat.append({
                "type": "location", "objet": loc,
                "message": _("Véhicule déjà loué le %(dates)s (%(creneau)s) – %(client)s, %(lieu)s.") % {
                    "dates": dates, "creneau": _creneau(loc.heure_debut, loc.heure_fin),
                    "client": loc.locataire or _("client non renseigné"), "lieu": loc.lieu or "—",
                },
            })

    # ---- Interdictions (ce véhicule ou tous les véhicules)
    interdictions = (InterdictionLocation.objects.filter(societe=societe, actif=True, date_debut__lte=jour_fin)
                     .filter(Q(voiture_exemplaire_id=voiture_id) | Q(voiture_exemplaire__isnull=True))
                     .filter(Q(date_fin__gte=date_debut) | Q(date_fin__isnull=True, date_debut__gte=date_debut)))
    for it in interdictions:
        for jour, creneau in _intervalles_interdiction(it, date_debut, jour_fin):
            if chevauche(souhait, creneau):
                resultat.append({
                    "type": "interdiction", "objet": it,
                    "message": _("Location interdite le %(jour)s (%(creneau)s) : %(motif)s%(desc)s.") % {
                        "jour": f"{jour:%d/%m/%Y}", "creneau": _creneau(it.heure_debut, it.heure_fin),
                        "motif": it.get_motif_display(),
                        "desc": f" – {it.description}" if it.description else "",
                    },
                })
                break
    return resultat

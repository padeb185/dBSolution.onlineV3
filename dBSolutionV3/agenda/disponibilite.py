"""
Disponibilité des véhicules à la location pour un jour donné.

Flotte de location : véhicules de la société (sans client) dont l'utilisation est « Location »,
plus tout véhicule de la société ayant déjà été loué.

État (tag) du véhicule pour le jour :
  ROUGE  : indisponible – loué toute la journée, interdiction de location toute la journée,
           problème signalé au dernier retour (tag rouge) sans checkup piste vert depuis,
           ou véhicule au tag rouge ;
  JAUNE  : disponible sous réserve – loué ou interdit sur un créneau seulement, départ / retour
           prévu ce jour, ou véhicule rentré (tag jaune) à contrôler (pas de checkup piste vert depuis) ;
  VERT   : disponible toute la journée.
"""
from datetime import datetime, time, timedelta

from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _

from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import TypeUtilisation, VoitureExemplaire
from voiture.voiture_location.models import InterdictionLocation, Location
from voiture.voiture_location.regles import _creneau, chevauche, intervalle

from .models import AgendaLocation, AgendaTache

ROUGE, JAUNE, VERT = Maintenance.Tag.ROUGE, Maintenance.Tag.JAUNE, Maintenance.Tag.VERT
ORDRE_TAG = {VERT: 0, JAUNE: 1, ROUGE: 2}


def flotte_location(societe):
    loues = Location.objects.filter(societe=societe).values("voiture_exemplaire_id")
    return (
        VoitureExemplaire.objects.filter(societe=societe, client__isnull=True)
        .filter(Q(type_utilisation=TypeUtilisation.LOCATION) | Q(pk__in=loues))
        .select_related("voiture_marque", "voiture_modele")
        .order_by("voiture_marque__nom_marque", "voiture_modele__nom_modele", "immatriculation")
        .distinct()
    )


def _journee(jour):
    return datetime.combine(jour, time.min), datetime.combine(jour + timedelta(days=1), time.min)


def _part_du_jour(creneau, jour):
    """Intersection d'un créneau avec la journée : None, 'TOUTE' ou 'PARTIELLE'."""
    debut_j, fin_j = _journee(jour)
    if not chevauche(creneau, (debut_j, fin_j)):
        return None
    return "TOUTE" if creneau[0] <= debut_j and creneau[1] >= fin_j else "PARTIELLE"


def _interdiction_du_jour(it, jour):
    if it.date_debut > jour or (it.date_fin or it.date_debut) < jour:
        return None
    jours = it.jours_liste
    if jours and jour.weekday() not in jours:
        return None
    return _part_du_jour(intervalle(jour, None, it.heure_debut, it.heure_fin), jour)


def disponibilites(societe, jour):
    """
    [{"exemplaire", "tag", "motifs": [str], "locations": [Location], "dernier_retour": AgendaLocation|None}]
    trié : disponibles (vert) d'abord, puis jaune, puis rouge.
    """
    vehicules = list(flotte_location(societe))
    ids = [v.pk for v in vehicules]

    locations = list(
        Location.objects.filter(societe=societe, voiture_exemplaire_id__in=ids, date_debut__lte=jour)
        .filter(Q(date_fin__gte=jour) | Q(date_fin__isnull=True, date_debut=jour))
        .select_related("client", "societe_cliente", "client_pilotage__client_particulier")
        .order_by("heure_debut")
    )
    interdictions = list(
        InterdictionLocation.objects.filter(societe=societe, actif=True, date_debut__lte=jour)
        .filter(Q(date_fin__gte=jour) | Q(date_fin__isnull=True, date_debut=jour))
        .filter(Q(voiture_exemplaire_id__in=ids) | Q(voiture_exemplaire__isnull=True))
    )

    # Dernier retour de chaque véhicule (avant ou pendant le jour)
    fin_jour = _journee(jour)[1]
    derniers_retours = {}
    for suivi in (AgendaLocation.objects.filter(societe=societe, retour_effectue=True,
                                                location__voiture_exemplaire_id__in=ids)
                  .select_related("location").order_by("retour_le")):
        if suivi.retour_le is None or timezone.localtime(suivi.retour_le).replace(tzinfo=None) < fin_jour:
            derniers_retours[suivi.location.voiture_exemplaire_id] = suivi

    # Dernier checkup piste vert de chaque véhicule (jusqu'au jour inclus)
    checkups_verts = {}
    for t in (AgendaTache.objects.filter(societe=societe, voiture_exemplaire_id__in=ids, date__lte=jour,
                                         type_maintenance=Maintenance.TypeMaintenance.CHECKUP_TRACK, tag=VERT)
              .order_by("date")):
        checkups_verts[t.voiture_exemplaire_id] = t

    resultat = []
    for v in vehicules:
        motifs_rouge, motifs_jaune = [], []

        locs = [l for l in locations if l.voiture_exemplaire_id == v.pk]
        for loc in locs:
            part = _part_du_jour(intervalle(loc.date_debut, loc.date_fin, loc.heure_debut, loc.heure_fin), jour)
            if part is None:
                continue
            texte = _("Loué (%(creneau)s) – %(client)s") % {
                "creneau": _creneau(loc.heure_debut if loc.date_debut == jour else None,
                                    loc.heure_fin if (loc.date_fin or loc.date_debut) == jour else None),
                "client": loc.locataire or _("client non renseigné"),
            }
            (motifs_rouge if part == "TOUTE" else motifs_jaune).append(texte)
            if loc.date_debut == jour and part == "TOUTE":
                motifs_jaune.append(_("Départ en location ce jour"))
            if (loc.date_fin or loc.date_debut) == jour and loc.date_debut != jour:
                motifs_jaune.append(_("Retour de location prévu ce jour"))

        for it in interdictions:
            if it.voiture_exemplaire_id not in (None, v.pk):
                continue
            part = _interdiction_du_jour(it, jour)
            if part is None:
                continue
            texte = _("Location interdite (%(creneau)s) : %(motif)s%(desc)s") % {
                "creneau": _creneau(it.heure_debut, it.heure_fin),
                "motif": it.get_motif_display(),
                "desc": f" – {it.description}" if it.description else "",
            }
            (motifs_rouge if part == "TOUTE" else motifs_jaune).append(texte)

        retour = derniers_retours.get(v.pk)
        checkup = checkups_verts.get(v.pk)
        if retour and retour.retour_le:
            controle_depuis = checkup is not None and checkup.date >= timezone.localtime(retour.retour_le).date()
            if not controle_depuis:
                if retour.tag_retour == ROUGE:
                    motifs_rouge.append(_("Problème signalé au dernier retour (tag rouge), pas de checkup piste vert depuis"))
                else:
                    motifs_jaune.append(_("Rentré de location, checkup piste à faire"))

        if v.tag == ROUGE:
            motifs_rouge.append(_("Véhicule au tag rouge"))

        if motifs_rouge:
            tag = ROUGE
        elif motifs_jaune:
            tag = JAUNE
        else:
            tag = VERT
        resultat.append({
            "exemplaire": v,
            "tag": tag,
            "motifs": motifs_rouge + motifs_jaune,
            "locations": locs,
            "dernier_retour": retour,
            "dernier_checkup_vert": checkup,
        })

    resultat.sort(key=lambda r: (ORDRE_TAG[r["tag"]], str(r["exemplaire"])))
    return resultat

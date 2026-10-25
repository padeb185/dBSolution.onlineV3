"""Dashboard de l'agenda + agenda des locations (sortie / retour)."""
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache

from maintenance.models import Maintenance
from voiture.voiture_location.models import Location

from .disponibilite import disponibilites
from .forms import AgendaLocationRetourForm, AgendaLocationSortieForm
from .models import AgendaLocation, AgendaTache
from .views import ROLES_AGENDA, _jour_depuis_requete, _peut, _taches_societe, _url_jour

# Agenda des locations : l'atelier + les vendeurs
ROLES_AGENDA_LOCATION = ROLES_AGENDA + ["vendeur"]


def _refuser(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _url_jour_location(jour):
    return reverse("agenda:agenda_location_date",
                   kwargs={"annee": jour.year, "mois": jour.month, "jour": jour.day})


def _url_jour_disponibilites(jour):
    return reverse("agenda:agenda_disponibilites_date",
                   kwargs={"annee": jour.year, "mois": jour.month, "jour": jour.day})


def _compter_tags(lignes):
    return {tag: sum(1 for l in lignes if l["tag"] == tag) for tag in ("VERT", "JAUNE", "ROUGE")}


def _locations_societe(request):
    return (
        Location.objects.filter(societe=request.user.societe)
        .select_related(
            "voiture_exemplaire", "voiture_exemplaire__voiture_marque", "voiture_exemplaire__voiture_modele",
            "client", "societe_cliente", "client_pilotage", "client_pilotage__client_particulier",
            "agenda_tache", "agenda_tache__technicien", "agenda_location",
        )
    )


def _km_vehicule(location):
    """Kilométrage châssis actuel du véhicule (mis à jour par le checkup piste)."""
    return getattr(location.voiture_exemplaire, "kilometres_chassis", None) or None


def _suivi(location):
    """
    AgendaLocation de la location (créé à la première consultation).
    Tant que la sortie n'est pas validée, le kilométrage avant location suit
    le kilométrage du véhicule : celui saisi au checkup piste de la location,
    et non celui du checkup précédent (figé à la création du suivi).
    """
    try:
        suivi = location.agenda_location
    except AgendaLocation.DoesNotExist:
        suivi, _cree = AgendaLocation.objects.get_or_create(
            location=location,
            defaults={
                "societe_id": location.societe_id,
                "kilometrage_avant": _km_vehicule(location),
            },
        )
        return suivi

    if not suivi.sortie_effectuee:
        km = _km_vehicule(location)
        if km is not None and km != suivi.kilometrage_avant:
            suivi.kilometrage_avant = km
            suivi.save(update_fields=["kilometrage_avant", "updated_at"])
    return suivi


def nom_client(location):
    if location.client_pilotage_id:
        cp = location.client_pilotage.client_particulier
        return f"{cp.prenom} {cp.nom}"
    if location.societe_cliente_id:
        return location.societe_cliente.nom_societe_cliente or "—"
    if location.client_id:
        return f"{location.client.prenom} {location.client.nom}"
    return "—"


def _filtre_jour(jour):
    """Locations qui couvrent le jour (date de fin vide = un seul jour)."""
    return (
        Q(date_debut__lte=jour, date_fin__gte=jour)
        | Q(date_debut=jour, date_fin__isnull=True)
    )


def _lignes(locations, jour):
    lignes = []
    for loc in locations:
        suivi = _suivi(loc)
        fin = loc.date_fin or loc.date_debut
        lignes.append({
            "location": loc,
            "suivi": suivi,
            "exemplaire": loc.voiture_exemplaire,
            "client": nom_client(loc),
            "checkup": suivi.checkup,
            "depart": loc.date_debut == jour,
            "retour_prevu": fin == jour,
            "en_retard": suivi.sortie_effectuee and not suivi.retour_effectue and fin < jour,
        })
    ordre = {"OK_SORTIE": 0, "PREPARATION": 1, "EN_LOCATION": 2, "PROBLEME": 3, "RETOUR": 4}
    lignes.sort(key=lambda l: (not l["en_retard"], ordre[l["suivi"].etat], l["location"].date_debut))
    return lignes


# =====================================================================
# DASHBOARD
# =====================================================================
@never_cache
@login_required
def agenda_dashboard_view(request):
    if not _peut(request.user, ROLES_AGENDA_LOCATION):
        return _refuser(request)

    aujourdhui = timezone.localdate()
    code_track = Maintenance.TypeMaintenance.CHECKUP_TRACK

    taches = _taches_societe(request).filter(date=aujourdhui)
    terminees = (
        taches.filter(type_maintenance=code_track, tag=Maintenance.Tag.VERT).count()
        + taches.exclude(type_maintenance=code_track).filter(statut=AgendaTache.Statut.FAIT).count()
    )
    nb_taches = taches.count()
    mes_taches = taches.filter(technicien=request.user)
    mes_a_faire = sum(1 for t in mes_taches if not t.est_terminee)

    locs_jour = list(_locations_societe(request).filter(_filtre_jour(aujourdhui)))
    lignes_jour = _lignes(locs_jour, aujourdhui)

    # En retard : sorties non rentrées dont la date de fin est passée
    en_retard = [
        l for l in _lignes(
            _locations_societe(request).filter(
                agenda_location__sortie_effectuee=True, agenda_location__retour_effectue=False,
            ).exclude(_filtre_jour(aujourdhui)),
            aujourdhui,
        ) if l["en_retard"]
    ]

    # 7 prochains jours : préparation des véhicules
    a_venir = _lignes(
        _locations_societe(request).filter(
            date_debut__gt=aujourdhui, date_debut__lte=aujourdhui + timedelta(days=7)
        ).order_by("date_debut"),
        aujourdhui,
    )
    a_venir.sort(key=lambda l: l["location"].date_debut)

    dispo = _compter_tags(disponibilites(request.user.societe, aujourdhui))

    def compte(etat):
        return sum(1 for l in lignes_jour if l["suivi"].etat == etat)

    return render(request, "agenda/agenda_dashboard.html", {
        "aujourdhui": aujourdhui,
        "nb_taches": nb_taches,
        "nb_terminees": terminees,
        "mes_a_faire": mes_a_faire,
        "peut_maintenances": _peut(request.user, ROLES_AGENDA),
        "nb_locations": len(lignes_jour),
        "nb_departs": sum(1 for l in lignes_jour if l["depart"]),
        "nb_ok_sortie": compte("OK_SORTIE"),
        "nb_preparation": compte("PREPARATION"),
        "nb_en_location": compte("EN_LOCATION"),
        "nb_retours": sum(1 for l in lignes_jour if l["retour_prevu"] and not l["suivi"].retour_effectue),
        "nb_problemes": compte("PROBLEME"),
        "lignes_jour": lignes_jour,
        "en_retard": en_retard,
        "a_venir": a_venir,
        "dispo": dispo,
    })


# =====================================================================
# AGENDA DES LOCATIONS (page d'un jour)
# =====================================================================
@never_cache
@login_required
def agenda_location_view(request, annee=None, mois=None, jour=None):
    if not _peut(request.user, ROLES_AGENDA_LOCATION):
        return _refuser(request)

    jour_affiche = _jour_depuis_requete(request, annee, mois, jour)
    lignes = _lignes(_locations_societe(request).filter(_filtre_jour(jour_affiche)), jour_affiche)

    return render(request, "agenda/agenda_location_list.html", {
        "jour": jour_affiche,
        "aujourdhui": timezone.localdate(),
        "url_veille": _url_jour_location(jour_affiche - timedelta(days=1)),
        "url_lendemain": _url_jour_location(jour_affiche + timedelta(days=1)),
        "url_aujourdhui": _url_jour_location(timezone.localdate()),
        "url_maintenances": _url_jour(jour_affiche),
        "lignes": lignes,
    })


# =====================================================================
# VÉHICULES DISPONIBLES À LA LOCATION (page d'un jour)
# =====================================================================
@never_cache
@login_required
def agenda_disponibilites_view(request, annee=None, mois=None, jour=None):
    if not _peut(request.user, ROLES_AGENDA_LOCATION):
        return _refuser(request)

    jour_affiche = _jour_depuis_requete(request, annee, mois, jour)
    lignes = disponibilites(request.user.societe, jour_affiche)

    return render(request, "agenda/agenda_disponibilites.html", {
        "jour": jour_affiche,
        "aujourdhui": timezone.localdate(),
        "url_veille": _url_jour_disponibilites(jour_affiche - timedelta(days=1)),
        "url_lendemain": _url_jour_disponibilites(jour_affiche + timedelta(days=1)),
        "url_aujourdhui": _url_jour_disponibilites(timezone.localdate()),
        "url_locations": _url_jour_location(jour_affiche),
        "lignes": lignes,
        "compte": _compter_tags(lignes),
    })


# =====================================================================
# SORTIE / RETOUR D'UNE LOCATION
# =====================================================================
@never_cache
@login_required
def agenda_location_controle_view(request, location_id):
    if not _peut(request.user, ROLES_AGENDA_LOCATION):
        return _refuser(request)

    location = get_object_or_404(_locations_societe(request), pk=location_id)
    suivi = _suivi(location)
    jour = _jour_depuis_requete(request)
    url_retour = _url_jour_location(jour if request.GET.get("date") else location.date_debut)

    form_sortie = form_retour = None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "sortie" and not suivi.sortie_effectuee:
            form_sortie = AgendaLocationSortieForm(request.POST, instance=suivi)
            if not suivi.checkup_vert:
                messages.error(request, _("Sortie impossible : le checkup piste n'est pas au vert dans l'agenda maintenances."))
            elif form_sortie.is_valid():
                suivi = form_sortie.save(commit=False)
                suivi.sortie_effectuee = True
                suivi.sortie_le = timezone.now()
                suivi.sortie_par = request.user
                suivi.save()
                messages.success(request, _("Sortie du véhicule enregistrée."))
                return redirect(url_retour)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))

        elif action == "retour" and suivi.sortie_effectuee:
            form_retour = AgendaLocationRetourForm(request.POST, instance=suivi)
            if form_retour.is_valid():
                with transaction.atomic():
                    suivi = form_retour.save(commit=False)
                    suivi.tag_retour = form_retour.cleaned_data["tag_retour"]
                    suivi.retour_effectue = True
                    suivi.retour_le = suivi.retour_le or timezone.now()
                    suivi.retour_par = request.user
                    suivi.save()
                    _reporter_kilometrage(location, suivi)
                    alerte_facture = _enregistrer_km_supplementaires(location, suivi, form_retour.cleaned_data,
                                                                     request.user)
                if alerte_facture:
                    messages.warning(request, alerte_facture)
                if suivi.tag_retour == Maintenance.Tag.ROUGE:
                    messages.warning(request, _("Retour enregistré : problème signalé (tag rouge)."))
                else:
                    messages.success(request, _("Retour enregistré (tag jaune)."))
                return redirect(url_retour)
            messages.error(request, _("Le formulaire contient des erreurs."))

        elif action == "annuler_sortie" and suivi.sortie_effectuee and not suivi.retour_effectue:
            suivi.sortie_effectuee = False
            suivi.sortie_le = None
            suivi.sortie_par = None
            suivi.save(update_fields=["sortie_effectuee", "sortie_le", "sortie_par", "updated_at"])
            messages.success(request, _("Sortie annulée."))
            return redirect(request.get_full_path())

    if not suivi.sortie_effectuee and form_sortie is None:
        form_sortie = AgendaLocationSortieForm(instance=suivi)
    if suivi.sortie_effectuee and form_retour is None:
        form_retour = AgendaLocationRetourForm(instance=suivi)

    return render(request, "agenda/agenda_location_controle.html", {
        "location": location,
        "suivi": suivi,
        "exemplaire": location.voiture_exemplaire,
        "client": nom_client(location),
        "checkup": suivi.checkup,
        "form_sortie": form_sortie,
        "form_retour": form_retour,
        "url_retour": url_retour,
        "calcul_km": suivi.calcul_km_supplementaires,
    })


def _enregistrer_km_supplementaires(location, suivi, donnees, user=None):
    """
    Kilomètres supplémentaires → location (prix TVAC, ajouté au prix de la location), puis facturation :
    - facture de la location en brouillon : ligne ajoutée / mise à jour ;
    - facture déjà émise : facture complémentaire (brouillon) créée avec le solde à facturer.
    Retourne un message à afficher (facture complémentaire), ou None.
    """
    from django.urls import reverse
    from django.utils.html import format_html
    from facture.services import facturer_km_supplementaires, ligne_km_supplementaires

    km = donnees.get("km_supplementaires")
    if km is None:
        km = suivi.calcul_km_supplementaires["km"]
    location.km_supplementaires = km
    if donnees.get("prix_km_supplementaire") is not None:
        location.prix_km_supplementaire = donnees["prix_km_supplementaire"]
    location.facturer_km_supplementaires = bool(donnees.get("facturer_km_supplementaires"))
    location.save(update_fields=["km_supplementaires", "prix_km_supplementaire", "facturer_km_supplementaires",
                                 "updated_at"])

    facture = location.facture
    if facture is not None and facture.statut == facture.Statut.EMISE:
        complementaire, creee, solde = facturer_km_supplementaires(location, user)
        if complementaire is None:
            if solde < 0:
                return _("Les kilomètres supplémentaires déjà facturés dépassent le nouveau total "
                         "(%(montant)s € TVAC à rembourser) : établissez une note de crédit.") % {"montant": f"{-solde:.2f}"}
            return None
        texte = (_("La facture %(numero)s est déjà émise : facture complémentaire créée (brouillon) pour les "
                   "kilomètres supplémentaires – %(montant)s € TVAC.") if creee else
                 _("La facture %(numero)s est déjà émise : facture complémentaire (brouillon) mise à jour pour les "
                   "kilomètres supplémentaires – %(montant)s € TVAC.")) % {"numero": facture.numero, "montant": f"{solde:.2f}"}
        return format_html('{} <a href="{}" class="underline font-semibold">{}</a>', texte,
                           reverse("facture:detail", kwargs={"pk": complementaire.pk}), _("Voir et émettre la facture"))
    ligne_km_supplementaires(facture, location)
    return None


def _reporter_kilometrage(location, suivi):
    """Km parcourus → location (si vide) ; km après location → compteur du véhicule."""
    if suivi.km_parcourus is not None and location.kilometrage is None:
        location.kilometrage = suivi.km_parcourus
        location.save()
    ve = location.voiture_exemplaire
    if suivi.kilometrage_apres and (ve.kilometres_chassis or 0) < suivi.kilometrage_apres:
        ve.kilometres_chassis = suivi.kilometrage_apres
        ve.save()

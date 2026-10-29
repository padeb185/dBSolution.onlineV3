from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .forms import LocationBoxFormSet, LocationForm, LocationVehiculeSupForm
from .models import Location, ObjectifVente, Trackday

ROLES_AUTORISES = ["vendeur", "direction", "chef_mecanicien"]
# Suppression : direction, chef mécanicien (+ super admin)
ROLES_SUPPRESSION = ["direction", "chef_mecanicien"]

ACTION_CREATION_LOCATION = gettext_noop("Nouvelle location")
ACTION_MODIFICATION_LOCATION = gettext_noop("Modification de la location")
ACTION_SUPPRESSION_LOCATION = gettext_noop("Suppression de la location")
ACTION_FACTURE_LOCATION = gettext_noop("Création d'une facture de location")


def _log(user, action, location):
    """Journal d'activité (même format que les maintenances : « Action - immatriculation – détail »)."""
    from utilisateurs.models import UserLog
    immatriculation = getattr(location.voiture_exemplaire, "immatriculation", "") or "-"
    detail = location.lieu or location.get_type_location_display()
    texte = f"{action} - {immatriculation}"
    if detail:
        texte += f" – {detail} ({location.date_debut:%d/%m/%Y})"
    UserLog.objects.create(utilisateur=user, action=texte[:255])


def _autorise(user):
    return user.is_superuser or getattr(user, "role", None) in ROLES_AUTORISES


def _queryset(request):
    return (
        Location.objects
        .filter(societe=request.user.societe)
        .select_related(
            "voiture_exemplaire__voiture_marque",
            "voiture_exemplaire__voiture_modele",
            "client",
            "societe_cliente",
            "client_pilotage__client_particulier",
            "societe__adresse",
            "vendeur",
            "trackday",
        )
        .prefetch_related("factures", "boxes")
    )


def _peut_facturer(user):
    from facture.views import ROLES_FACTURATION, ROLES_FACTURATION_LOCATION
    return user.is_superuser or getattr(user, "role", None) in (ROLES_FACTURATION + ROLES_FACTURATION_LOCATION)


@never_cache
@login_required
def location_liste(request):
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    return render(request, "voiture_location/location_list.html", {
        "locations": _queryset(request),
        "peut_facturer": _peut_facturer(request.user),
        "type_client": "CLIENT",
        "type_pro": "PRO",
    })


@login_required
def location_ajouter(request):
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    exemplaire_id = request.GET.get("exemplaire")
    initial = {"voiture_exemplaire": exemplaire_id} if exemplaire_id else {}

    # Ajout depuis un Trackday : circuit, dates et Trackday pré-remplis
    trackday_initial = _trackday_demande(request, request.GET.get("trackday"))
    if trackday_initial is not None:
        initial.update({
            "trackday": trackday_initial.pk, "type_location": "circuit", "circuit": trackday_initial.circuit,
            "date_debut": trackday_initial.date_debut, "date_fin": trackday_initial.date_fin,
        })

    form = LocationForm(request.POST or None, user=request.user, initial=initial)
    vehicules = form.fields["voiture_exemplaire"].queryset
    # Trackday choisi dans le formulaire (s'applique aussi aux véhicules supplémentaires)
    trackday_post = _trackday_demande(request, request.POST.get("trackday")) if request.method == "POST" else None
    # Box en pit lane : rattachés à la location du véhicule 1
    boxes_fs = LocationBoxFormSet(request.POST or None, instance=Location(), prefix="box")
    if trackday_post is not None:
        boxes_fs.limite_box = trackday_post.nombre_box

    # Véhicules supplémentaires (même client) : une location complète par véhicule
    forms_sup = []
    if request.method == "POST":
        for idx in request.POST.getlist("sup_index"):
            if idx.isdigit():
                forms_sup.append(LocationVehiculeSupForm(request.POST, prefix=f"sup-{idx}", vehicules=vehicules,
                                                         societe=request.user.societe, trackday=trackday_post))

    # Remise en % sur l'ensemble des véhicules
    remise_brute = (request.POST.get("remise_pourcent") or "0").replace(",", ".") if request.method == "POST" else "0"
    try:
        remise = Decimal(remise_brute)
    except Exception:
        remise = None

    if request.method == "POST":
        principal_ok = form.is_valid()
        if remise is None or remise < 0 or remise >= 100:
            form.add_error(None, _("La remise doit être comprise entre 0 et 99,99 %."))
            principal_ok = False
        sup_ok = all([f.is_valid() for f in forms_sup])
        principal_ok = boxes_fs.is_valid() and principal_ok
        doublons = _vehicules_en_double(form, forms_sup)
        if doublons:
            form.add_error(None, _("Le véhicule %(v)s est sélectionné plusieurs fois.") % {"v": ", ".join(doublons)})
        numeros_doubles = _numeros_en_double(form, forms_sup)
        if numeros_doubles:
            form.add_error(None, _("Le numéro de course %(n)s est utilisé plusieurs fois.") % {"n": ", ".join(numeros_doubles)})
            doublons = doublons or numeros_doubles

        if principal_ok and sup_ok and not doublons:
            from django.db import transaction
            with transaction.atomic():
                location = form.save(commit=False)
                _appliquer_remise(location, remise)
                location.save()
                boxes_fs.instance = location
                boxes_fs.save()
                _log(request.user, ACTION_CREATION_LOCATION, location)
                creees = [location]
                for f in forms_sup:
                    copie = f.save(commit=False)
                    copie.societe = location.societe
                    copie.vendeur = location.vendeur
                    copie.client = location.client
                    copie.societe_cliente = location.societe_cliente
                    copie.client_pilotage = location.client_pilotage
                    copie.remarques = location.remarques
                    copie.trackday = location.trackday
                    _appliquer_remise(copie, remise)
                    copie.save()  # crée aussi le checkup piste dans l'agenda
                    _log(request.user, ACTION_CREATION_LOCATION, copie)
                    creees.append(copie)

            if location.trackday_id:
                messages.success(request, _("%(n)s véhicule(s) ajouté(s) au Trackday.") % {"n": len(creees)})
                return redirect("voiture_location:trackday_detail", pk=location.trackday_id)
            if len(creees) == 1:
                messages.success(request, _("Location '%(loc)s' créée avec succès.") % {"loc": location})
            else:
                messages.success(request, _("%(n)s locations créées pour le même client : %(vehicules)s") % {
                    "n": len(creees),
                    "vehicules": ", ".join(l.voiture_exemplaire.immatriculation or str(l.voiture_exemplaire) for l in creees),
                })
            return redirect("voiture_location:location_liste")

        if forms_sup and not sup_ok:
            form.add_error(None, _("Vérifiez les véhicules supplémentaires : certains champs sont incorrects."))

    return render(request, "voiture_location/location_form.html", {
        "form": form, "location": None, "taux_tva": Location(societe=request.user.societe).taux_tva,
        "vehicules": vehicules,
        "forms_sup": [(f.prefix.split("-", 1)[1], f) for f in forms_sup],
        "form_sup_vide": LocationVehiculeSupForm(prefix="sup-__ID__", vehicules=vehicules),
        "trackdays_data": _trackdays_data(form),
        "champs_vehicule": CHAMPS_VEHICULE,
        "remise": remise_brute if request.method == "POST" else "0",
        "boxes_fs": boxes_fs,
        "prix_instructeurs": form.prix_instructeurs,
    })


# Champs propres à chaque véhicule loué (affichés dans la fiche de chaque véhicule)
CHAMPS_VEHICULE = ["numero_course", "type_location", "circuit", "route", "date_debut", "date_fin", "heure_debut", "heure_fin", "nombre_tours", "kilometrage", "prix"]


def _appliquer_remise(location, remise):
    """Le prix saisi est le prix TVAC avant remise ; « prix » devient le prix après remise."""
    from decimal import ROUND_HALF_UP
    if remise and remise > 0:
        location.prix_avant_remise = location.prix
        location.remise_pourcent = remise
        location.prix = (Decimal(location.prix) * (Decimal("100") - remise) / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    else:
        location.prix_avant_remise = None
        location.remise_pourcent = Decimal("0")


def _trackday_demande(request, pk):
    """Trackday de la société désigné par son identifiant (GET / POST), sinon None."""
    if not pk:
        return None
    try:
        return Trackday.objects.filter(societe=request.user.societe, pk=pk).first()
    except Exception:
        return None


def _trackdays_data(form):
    """Données des Trackdays pour le formulaire (circuit, dates, box) : rempli automatiquement en JS."""
    if "trackday" not in form.fields:
        return {}
    return {
        str(t.pk): {
            "circuit": t.circuit, "date_debut": t.date_debut.isoformat(),
            "date_fin": t.date_fin.isoformat() if t.date_fin else "", "nombre_box": t.nombre_box,
            "numeros_pris": [n for n in t.locations.exclude(numero_course=None).values_list("numero_course", flat=True)],
        }
        for t in form.fields["trackday"].queryset[:50]
    }


def _numeros_en_double(form, forms_sup):
    vus, doublons = set(), []
    for f in [form] + list(forms_sup):
        n = f.cleaned_data.get("numero_course") if hasattr(f, "cleaned_data") else None
        if n is None:
            continue
        if n in vus:
            doublons.append(str(n))
        vus.add(n)
    return doublons


def _vehicules_en_double(form, forms_sup):
    vus, doublons = set(), []
    candidats = [form.cleaned_data.get("voiture_exemplaire") if hasattr(form, "cleaned_data") else None]
    candidats += [f.cleaned_data.get("voiture_exemplaire") if hasattr(f, "cleaned_data") else None for f in forms_sup]
    for ex in candidats:
        if ex is None:
            continue
        if ex.pk in vus:
            doublons.append(ex.immatriculation or str(ex))
        vus.add(ex.pk)
    return doublons


@login_required
def location_modifier(request, location_id):
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    location = get_object_or_404(_queryset(request), id=location_id)
    form = LocationForm(request.POST or None, instance=location, user=request.user)
    boxes_fs = LocationBoxFormSet(request.POST or None, instance=location, prefix="box")
    trackday = (_trackday_demande(request, request.POST.get("trackday")) if request.method == "POST"
                else location.trackday)
    if trackday is not None:
        boxes_fs.limite_box = trackday.nombre_box
    if request.method == "POST" and all([form.is_valid(), boxes_fs.is_valid()]):
        location = form.save()
        boxes_fs.save()
        getattr(location, "_prefetched_objects_cache", {}).pop("boxes", None)  # total box à jour
        location.synchroniser_paiement_facture()
        _log(request.user, ACTION_MODIFICATION_LOCATION, location)
        messages.success(request, _("Location '%(loc)s' mise à jour.") % {"loc": location})
        return redirect("voiture_location:location_detail", location_id=location.id)

    return render(request, "voiture_location/location_form.html", {
        "form": form, "location": location, "taux_tva": location.taux_tva,
        "boxes_fs": boxes_fs,
        "trackdays_data": _trackdays_data(form),
        "prix_instructeurs": form.prix_instructeurs,
    })


@login_required
def location_supprimer(request, location_id):
    if not (request.user.is_superuser or getattr(request.user, "role", None) in ROLES_SUPPRESSION):
        messages.error(request, _("Accès refusé"))
        return redirect("voiture_location:location_detail", location_id=location_id)

    location = get_object_or_404(_queryset(request), id=location_id)
    if request.method == "POST":
        try:
            from django.db import transaction
            with transaction.atomic():
                _log(request.user, ACTION_SUPPRESSION_LOCATION, location)
                location.delete()
            messages.success(request, _("Location supprimée."))
        except ProtectedError:
            messages.error(request, _("Impossible de supprimer cette location."))
        return redirect("voiture_location:location_liste")

    return render(request, "voiture_location/location_confirm_delete.html", {"location": location})


# -----------------------------
# Facturation d'une location (prix TVAC)
# -----------------------------
@login_required
@require_POST
def location_facturer(request, location_id):
    if not _peut_facturer(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("voiture_location:location_liste")

    from facture.models import Facture
    from facture.services import creer_facture_depuis_location
    from django.db import transaction
    location = get_object_or_404(_queryset(request), id=location_id)

    type_facture = request.POST.get("type_facture")
    if type_facture not in Facture.TypeFacture.values:
        messages.error(request, _("Type de facture inconnu."))
        return redirect("voiture_location:location_liste")

    with transaction.atomic():
        # Verrou sur la location : un double clic ne crée pas deux factures
        location = _queryset(request).select_for_update(of=("self",)).get(pk=location.pk)
        existante = location.facture
        if existante is not None:
            messages.info(request, _("Cette location est déjà facturée."))
            return redirect("facture:modifier" if existante.statut == Facture.Statut.BROUILLON else "facture:detail",
                            pk=existante.pk)
        facture = creer_facture_depuis_location(location, type_facture, request.user)
        _log(request.user, ACTION_FACTURE_LOCATION, location)
    if type_facture == Facture.TypeFacture.PRO and not facture.societe_cliente_id:
        messages.warning(request, _("Sélectionnez le client professionnel avant d'émettre la facture."))
    messages.success(request, _("Brouillon de facture créé. Le prix de location est TVAC : vérifiez la ligne avant d'émettre."))
    return redirect("facture:modifier", pk=facture.pk)


@login_required
@require_POST
def location_facturer_km_supplementaires(request, location_id):
    """Facture complémentaire des kilomètres supplémentaires (la facture de la location est déjà émise)."""
    if not _peut_facturer(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("voiture_location:location_liste")

    from facture.services import facturer_km_supplementaires, ligne_km_supplementaires
    location = get_object_or_404(_queryset(request), id=location_id)
    principale = location.facture

    if principale is None:
        messages.info(request, _("Cette location n'est pas encore facturée : les kilomètres supplémentaires "
                                 "seront repris dans sa facture."))
        return redirect("voiture_location:location_detail", location_id=location.pk)
    if principale.statut != principale.Statut.EMISE:
        ligne_km_supplementaires(principale, location)
        messages.success(request, _("Kilomètres supplémentaires ajoutés à la facture brouillon."))
        return redirect("facture:modifier", pk=principale.pk)

    facture, creee, solde = facturer_km_supplementaires(location, request.user)
    if facture is None:
        if solde < 0:
            messages.warning(request, _("Les kilomètres supplémentaires déjà facturés dépassent le nouveau total "
                                        "(%(montant)s € TVAC à rembourser) : établissez une note de crédit.")
                             % {"montant": f"{-solde:.2f}"})
        else:
            messages.info(request, _("Les kilomètres supplémentaires sont déjà entièrement facturés."))
        return redirect("voiture_location:location_detail", location_id=location.pk)
    _log(request.user, ACTION_FACTURE_LOCATION, location)
    messages.success(request, _("Facture complémentaire (brouillon) : %(montant)s € TVAC de kilomètres "
                                "supplémentaires. Vérifiez-la puis émettez-la.") % {"montant": f"{solde:.2f}"})
    return redirect("facture:modifier", pk=facture.pk)


# -----------------------------
# Ventes : détail des locations (HTVA / TVA / TVAC)
# -----------------------------
TYPES_PERIODE_VENTES = ("mois", "trimestre", "annee", "tout")


@never_cache
@login_required
def ventes_detail(request):
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    from facture.tva import CalculTVA

    aujourdhui = timezone.localdate()
    type_periode = request.GET.get("periode", "annee")
    if type_periode not in TYPES_PERIODE_VENTES:
        type_periode = "annee"

    def entier(nom, defaut):
        try:
            return int(request.GET.get(nom, defaut))
        except (TypeError, ValueError):
            return defaut

    annee = entier("annee", aujourdhui.year)
    numero_defaut = aujourdhui.month if type_periode == "mois" else (aujourdhui.month - 1) // 3 + 1
    numero = entier("numero", numero_defaut)

    locations = _queryset(request)
    debut = fin = None
    if type_periode != "tout":
        debut, fin = CalculTVA.bornes(type_periode, annee, numero)
        locations = locations.filter(date_debut__range=(debut, fin))
    locations = list(locations.order_by("date_debut", "created_at"))

    zero = Decimal("0.00")

    def cumul(liste):
        return {
            "nb": len(liste),
            "htva": sum((l.prix_htva for l in liste), zero),
            "tva": sum((l.montant_tva for l in liste), zero),
            "tvac": sum((l.prix_tvac for l in liste), zero),
            "km": sum((l.kilometrage or 0 for l in liste), 0),
        }

    facturees = [l for l in locations if l.facture is not None]
    non_facturees = [l for l in locations if l.facture is None]

    return render(request, "voiture_location/ventes_detail.html", {
        "locations": locations,
        "totaux": cumul(locations),
        "totaux_circuit": cumul([l for l in locations if l.type_location == "circuit"]),
        "totaux_route": cumul([l for l in locations if l.type_location == "route"]),
        "totaux_facturees": cumul(facturees),
        "totaux_non_facturees": cumul(non_facturees),
        "type_periode": type_periode,
        "annee": annee,
        "numero": numero,
        "debut": debut,
        "fin": fin,
        "annees": range(aujourdhui.year - 5, aujourdhui.year + 1),
        "mois": range(1, 13),
        "trimestres": range(1, 5),
        "peut_facturer": _peut_facturer(request.user),
    })


# -----------------------------
# Détail d'une location + PDF
# -----------------------------
@never_cache
@login_required
def location_detail(request, location_id):
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    location = get_object_or_404(_queryset(request), id=location_id)
    # Véhicule à plusieurs propriétaires : ventilation du prix et reversements (direction / comptabilité)
    from .reversements import parts_a_reverser, ventilation
    from .views_reversements import peut_reverser
    ventil = ventilation(location) if peut_reverser(request.user) and parts_a_reverser(location) else None
    return render(request, "voiture_location/location_detail.html", {
        "ventilation": ventil,
        "aujourdhui": timezone.localdate(),
        "location": location,
        "exemplaire": location.voiture_exemplaire,
        "peut_facturer": _peut_facturer(request.user),
        "type_client": "CLIENT",
        "type_pro": "PRO",
    })


@login_required
def location_pdf(request, location_id):
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    from django.http import HttpResponse
    from django.template.loader import render_to_string
    from weasyprint import HTML

    location = get_object_or_404(_queryset(request), id=location_id)
    from facture.models import ConditionsGenerales
    cg = ConditionsGenerales.pour_societe(location.societe or request.user.societe, ConditionsGenerales.Type.LOCATION)
    html = render_to_string("voiture_location/location_detail_pdf.html", {
        "conditions_generales": [cg] if cg else [],
        "location": location,
        "societe": request.user.societe,
        "date_export": timezone.now(),
    }, request=request)
    pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()

    immatriculation = str(getattr(location.voiture_exemplaire, "immatriculation", "") or "sans_immatriculation")
    nom_fichier = f"{_('Location')}_{immatriculation}_{location.date_debut:%Y-%m-%d}.pdf".replace(" ", "_")
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{nom_fichier}"'
    return response


# -----------------------------
# Statistiques de ventes par vendeur
# -----------------------------
ROLES_STATS_TOUT = ["direction"]


def _periode(request):
    """Lit la période demandée (mois / trimestre / année / tout) : dict + bornes."""
    from facture.tva import CalculTVA

    aujourdhui = timezone.localdate()
    type_periode = request.GET.get("periode", "annee")
    if type_periode not in TYPES_PERIODE_VENTES:
        type_periode = "annee"

    def entier(nom, defaut):
        try:
            return int(request.GET.get(nom, defaut))
        except (TypeError, ValueError):
            return defaut

    annee = entier("annee", aujourdhui.year)
    numero_defaut = aujourdhui.month if type_periode == "mois" else (aujourdhui.month - 1) // 3 + 1
    numero = entier("numero", numero_defaut)
    debut = fin = None
    if type_periode != "tout":
        debut, fin = CalculTVA.bornes(type_periode, annee, numero)
    return {
        "type_periode": type_periode, "annee": annee, "numero": numero, "debut": debut, "fin": fin,
        "annees": range(aujourdhui.year - 5, aujourdhui.year + 1),
        "mois": range(1, 13), "trimestres": range(1, 5),
    }


def _cumul_ventes(liste):
    zero = Decimal("0.00")
    nb = len(liste)
    tvac = sum((l.prix_tvac for l in liste), zero)
    facturees = [l for l in liste if l.facture is not None and l.facture.est_emise]
    return {
        "nb": nb,
        "nb_circuit": sum(1 for l in liste if l.type_location == "circuit"),
        "nb_route": sum(1 for l in liste if l.type_location == "route"),
        "km": sum((l.kilometrage or 0 for l in liste), 0),
        "htva": sum((l.prix_htva for l in liste), zero),
        "tva": sum((l.montant_tva for l in liste), zero),
        "tvac": tvac,
        "nb_facturees": len(facturees),
        "tvac_facturees": sum((l.prix_tvac for l in facturees), zero),
        "panier_moyen": (tvac / nb).quantize(Decimal("0.01")) if nb else zero,
    }


def _voit_tout(user):
    return user.is_superuser or getattr(user, "role", None) in ROLES_STATS_TOUT


@never_cache
@login_required
def statistiques_ventes(request):
    """Statistiques de tous les vendeurs : direction (+ super admin) uniquement."""
    if not _voit_tout(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")
    return _statistiques(request, voit_tout=True)


@never_cache
@login_required
def mes_statistiques(request):
    """Même page, limitée aux ventes de l'utilisateur connecté."""
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")
    return _statistiques(request, voit_tout=False)


def _statistiques(request, voit_tout):
    periode = _periode(request)

    locations = _queryset(request)
    if periode["debut"]:
        locations = locations.filter(date_debut__range=(periode["debut"], periode["fin"]))
    if not voit_tout:
        locations = locations.filter(vendeur=request.user)
    locations = list(locations.order_by("date_debut"))

    totaux = _cumul_ventes(locations)

    # --- Objectifs de vente (somme des objectifs mensuels de la période) ---
    objectifs = _objectifs_periode(request.user.societe, periode, None if voit_tout else request.user)

    # --- Par vendeur ---
    groupes = {}
    for l in locations:
        groupes.setdefault(l.vendeur_id, {"vendeur": l.vendeur, "locations": []})["locations"].append(l)
    # Vendeurs avec un objectif mais sans vente sur la période
    for vid, obj in objectifs.items():
        if vid not in groupes:
            groupes[vid] = {"vendeur": obj["vendeur"], "locations": []}
    par_vendeur = []
    for g in groupes.values():
        stats = _cumul_ventes(g["locations"])
        vendeur = g["vendeur"]
        stats.update({
            "vendeur": vendeur,
            "nom": f"{vendeur.prenom} {vendeur.nom}".strip() if vendeur else _("Non attribué"),
            "role": vendeur.get_role_display() if vendeur else "",
            "part": (stats["tvac"] * 100 / totaux["tvac"]).quantize(Decimal("0.1")) if totaux["tvac"] else Decimal("0"),
        })
        stats.update(_avancement(stats, objectifs.get(g["vendeur"].pk if g["vendeur"] else None)))
        par_vendeur.append(stats)
    par_vendeur.sort(key=lambda s: s["tvac"], reverse=True)

    # Objectif global (société ou vendeur connecté)
    objectif_global = None
    if objectifs:
        objectif_global = {
            "montant": sum((o["montant"] for o in objectifs.values()), Decimal("0")),
            "nombre": sum((o["nombre"] or 0 for o in objectifs.values()), 0) or None,
        }
    avancement_global = _avancement(totaux, objectif_global)

    # --- Séries par mois, trimestre et année (tous les mois, même sans vente) ---
    series = _series_ventes(request, periode, voit_tout)
    par_mois = series["par_mois"]

    # --- Circuits / routes les plus vendus ---
    lieux = {}
    for l in locations:
        cle = l.lieu or l.get_type_location_display()
        lieux.setdefault(cle, []).append(l)
    top_lieux = sorted(
        ({"lieu": k, "type": v[0].get_type_location_display(), **_cumul_ventes(v)} for k, v in lieux.items()),
        key=lambda s: s["tvac"], reverse=True,
    )[:10]

    # --- Trackdays (locations rattachées à un Trackday) ---
    trackdays = {}
    for l in locations:
        if l.trackday_id:
            trackdays.setdefault(l.trackday_id, []).append(l)
    par_trackday = sorted(
        ({"trackday": v[0].trackday, **_cumul_ventes(v)} for v in trackdays.values()),
        key=lambda s: s["trackday"].date_debut, reverse=True,
    )

    graphiques = _graphiques_ventes(series, par_vendeur, top_lieux, totaux)

    return render(request, "voiture_location/statistiques_ventes.html", {
        **periode,
        "par_trimestre": series["par_trimestre"],
        "par_annee": series["par_annee"],
        "annee_serie": series["annee_serie"], "total_mois": series["total_mois"],
        "graphiques": graphiques,
        "par_trackday": par_trackday,
        "voit_tout": voit_tout,
        "vendeur_connecte": request.user,
        "totaux": totaux,
        "par_vendeur": par_vendeur,
        "par_mois": par_mois,
        "top_lieux": top_lieux,
        "avancement": avancement_global,
        "a_objectifs": bool(objectifs),
        "peut_objectifs": _voit_tout(request.user),
    })


def _series_ventes(request, periode, voit_tout):
    """
    Séries complètes pour les tableaux et graphiques :
      - par mois : les 12 mois de l'année de la période (tous les mois depuis la première vente pour « tout »),
        avec l'année précédente pour comparaison ; les mois de la période choisie sont marqués ;
      - par trimestre : les 4 trimestres de l'année ;
      - par année : les 6 dernières années (toutes pour « tout »).
    """
    from datetime import date as _date

    base = _queryset(request)
    if not voit_tout:
        base = base.filter(vendeur=request.user)
    toutes = list(base.order_by("date_debut"))
    par_cle = {}
    for l in toutes:
        par_cle.setdefault((l.date_debut.year, l.date_debut.month), []).append(l)

    def cumul(cles):
        liste = [l for c in cles for l in par_cle.get(c, [])]
        return _cumul_ventes(liste)

    aujourdhui = timezone.localdate()
    annee = periode["annee"] if periode["type_periode"] != "tout" else aujourdhui.year
    debut_p, fin_p = periode["debut"], periode["fin"]

    # Mois
    if periode["type_periode"] == "tout" and toutes:
        premier = toutes[0].date_debut
        mois_cles = []
        a, m = premier.year, premier.month
        while (a, m) <= (aujourdhui.year, aujourdhui.month):
            mois_cles.append((a, m))
            a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    else:
        mois_cles = [(annee, m) for m in range(1, 13)]
    par_mois = []
    for a, m in mois_cles:
        jour = _date(a, m, 1)
        par_mois.append({
            "annee": a, "mois": m, "date": jour, **cumul([(a, m)]),
            "precedent": cumul([(a - 1, m)])["htva"],
            "dans_periode": debut_p is None or (debut_p.replace(day=1) <= jour <= fin_p),
            "futur": jour > aujourdhui,
        })
    max_mois = max((m["tvac"] for m in par_mois), default=Decimal("0"))
    for m in par_mois:
        m["largeur"] = int(m["tvac"] * 100 / max_mois) if max_mois else 0

    # Trimestres de l'année
    par_trimestre = []
    for t in range(1, 5):
        c = cumul([(annee, m) for m in range(3 * t - 2, 3 * t + 1)])
        c.update({"trimestre": t, "futur": _date(annee, 3 * t - 2, 1) > aujourdhui, "precedent": cumul([(annee - 1, m) for m in range(3 * t - 2, 3 * t + 1)])["htva"],
                  "dans_periode": periode["type_periode"] in ("annee", "tout")
                  or (periode["type_periode"] == "trimestre" and periode["numero"] == t)
                  or (periode["type_periode"] == "mois" and (periode["numero"] - 1) // 3 + 1 == t)})
        par_trimestre.append(c)

    # Années
    premiere = toutes[0].date_debut.year if toutes else aujourdhui.year
    debut_annees = premiere if periode["type_periode"] == "tout" else max(premiere, annee - 5)
    par_annee = []
    for a in range(min(debut_annees, annee), max(annee, aujourdhui.year if periode["type_periode"] == "tout" else annee) + 1):
        c = cumul([(a, m) for m in range(1, 13)])
        c.update({"annee": a, "dans_periode": periode["type_periode"] == "tout" or a == annee})
        par_annee.append(c)
    def evolution(actuel, precedent):
        return ((actuel - precedent) * 100 / precedent).quantize(Decimal("0.1")) if precedent else None

    for ligne in par_mois + par_trimestre:
        # Mois / trimestre pas encore commencé : pas d'évolution (sinon -100 %)
        ligne["evolution"] = None if ligne["futur"] else evolution(ligne["htva"], ligne["precedent"])
    for i, ligne in enumerate(par_annee):
        ligne["precedent"] = par_annee[i - 1]["htva"] if i else cumul([(ligne["annee"] - 1, m) for m in range(1, 13)])["htva"]
        ligne["evolution"] = evolution(ligne["htva"], ligne["precedent"])
    total_mois = _cumul_ventes([l for a, m in mois_cles for l in par_cle.get((a, m), [])])
    # N-1 sur les mêmes mois (déjà commencés) pour une comparaison équitable
    total_mois["precedent"] = sum((m["precedent"] for m in par_mois if not m["futur"]), Decimal("0.00"))
    total_mois["evolution"] = evolution(total_mois["htva"], total_mois["precedent"])
    return {"par_mois": par_mois, "par_trimestre": par_trimestre, "par_annee": par_annee,
            "annee_serie": annee, "total_mois": total_mois}


def _graphiques_ventes(series, par_vendeur, top_lieux, totaux):
    """Données JSON pour les graphiques (Chart.js) de la page des statistiques de ventes."""
    from django.utils.formats import date_format

    f = lambda d: float(d or 0)
    multi_annees = len({m["annee"] for m in series["par_mois"]}) > 1
    return {
        "mois": {
            "labels": [date_format(m["date"], "M Y" if multi_annees else "F") for m in series["par_mois"]],
            "htva": [None if m["futur"] else f(m["htva"]) for m in series["par_mois"]],
            "precedent": [f(m["precedent"]) for m in series["par_mois"]],
            "nb": [None if m["futur"] else m["nb"] for m in series["par_mois"]],
            "periode": [m["dans_periode"] for m in series["par_mois"]],
            "comparaison": not multi_annees,
        },
        "trimestres": {
            "labels": [f"T{t['trimestre']}" for t in series["par_trimestre"]],
            "htva": [None if t["futur"] else f(t["htva"]) for t in series["par_trimestre"]],
            "precedent": [f(t["precedent"]) for t in series["par_trimestre"]],
        },
        "annees": {
            "labels": [str(a["annee"]) for a in series["par_annee"]],
            "htva": [f(a["htva"]) for a in series["par_annee"]],
            "nb": [a["nb"] for a in series["par_annee"]],
        },
        "vendeurs": {
            "labels": [v["nom"] for v in par_vendeur if v["tvac"]],
            "htva": [f(v["htva"]) for v in par_vendeur if v["tvac"]],
        },
        "lieux": {
            "labels": [str(l["lieu"]) for l in top_lieux],
            "htva": [f(l["htva"]) for l in top_lieux],
        },
        "types": {"circuit": totaux["nb_circuit"], "route": totaux["nb_route"]},
    }


# ======================================================
# OBJECTIFS DE VENTE
# ======================================================
def _objectifs_periode(societe, periode, vendeur=None):
    """{vendeur_id: {"vendeur", "montant", "nombre"}} pour les mois compris dans la période."""
    qs = ObjectifVente.objects.filter(societe=societe).select_related("vendeur")
    if vendeur is not None:
        qs = qs.filter(vendeur=vendeur)
    if periode["debut"]:
        d, f = periode["debut"], periode["fin"]
        qs = [o for o in qs if (d.year, d.month) <= (o.annee, o.mois) <= (f.year, f.month)]
    resultat = {}
    for o in qs:
        r = resultat.setdefault(o.vendeur_id, {"vendeur": o.vendeur, "montant": Decimal("0"), "nombre": None})
        r["montant"] += o.montant_htva or Decimal("0")
        if o.nombre_ventes:
            r["nombre"] = (r["nombre"] or 0) + o.nombre_ventes
    return {k: v for k, v in resultat.items() if v["montant"] or v["nombre"]}


def _avancement(stats, objectif):
    """Réalisé / objectif (montant HTVA et nombre de ventes)."""
    if not objectif:
        return {"objectif_htva": None, "objectif_nb": None, "pct_htva": None, "pct_nb": None, "reste_htva": None}
    montant = objectif["montant"] or Decimal("0")
    nombre = objectif.get("nombre")
    pct = (stats["htva"] * 100 / montant).quantize(Decimal("0.1")) if montant else None
    pct_nb = (Decimal(stats["nb"]) * 100 / nombre).quantize(Decimal("0.1")) if nombre else None
    return {
        "objectif_htva": montant or None,
        "objectif_nb": nombre,
        "pct_htva": pct,
        "pct_nb": pct_nb,
        "largeur_htva": min(int(pct), 100) if pct is not None else 0,
        "reste_htva": max(montant - stats["htva"], Decimal("0")) if montant else None,
    }


@never_cache
@login_required
def objectifs_ventes(request):
    """Saisie des objectifs mensuels par vendeur (direction + super admin)."""
    if not _voit_tout(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    from utilisateurs.models import Utilisateur
    from .forms import ROLES_VENDEUR

    societe = request.user.societe
    aujourdhui = timezone.localdate()
    try:
        annee = int(request.POST.get("annee") or request.GET.get("annee") or aujourdhui.year)
    except ValueError:
        annee = aujourdhui.year

    vendeurs = list(
        Utilisateur.objects.filter(societe=societe, is_active=True, role__in=ROLES_VENDEUR).order_by("nom", "prenom")
    )
    existants = {
        (o.vendeur_id, o.mois): o
        for o in ObjectifVente.objects.filter(societe=societe, annee=annee)
    }

    if request.method == "POST":
        erreurs = 0
        for v in vendeurs:
            for m in range(1, 13):
                brut = (request.POST.get(f"obj-{v.pk}-{m}") or "").strip().replace(",", ".")
                nb_brut = (request.POST.get(f"nb-{v.pk}-{m}") or "").strip()
                try:
                    montant = Decimal(brut) if brut else Decimal("0")
                    nombre = int(nb_brut) if nb_brut else None
                    if montant < 0 or (nombre is not None and nombre < 0):
                        raise ValueError
                except Exception:
                    erreurs += 1
                    continue
                obj = existants.get((v.pk, m))
                if not montant and not nombre:
                    if obj:
                        obj.delete()
                    continue
                if obj is None:
                    obj = ObjectifVente(societe=societe, vendeur=v, annee=annee, mois=m)
                obj.montant_htva = montant
                obj.nombre_ventes = nombre
                obj.save()
        if erreurs:
            messages.error(request, _("%(n)s valeur(s) invalide(s) ignorée(s).") % {"n": erreurs})
        else:
            messages.success(request, _("Objectifs %(annee)s enregistrés.") % {"annee": annee})
        return redirect(f"{request.path}?annee={annee}")

    lignes = []
    for v in vendeurs:
        cellules = []
        total = Decimal("0")
        total_nb = 0
        for m in range(1, 13):
            o = existants.get((v.pk, m))
            cellules.append({"mois": m, "montant": o.montant_htva if o else None, "nombre": o.nombre_ventes if o else None})
            total += (o.montant_htva if o else 0) or 0
            total_nb += (o.nombre_ventes if o else 0) or 0
        lignes.append({"vendeur": v, "cellules": cellules, "total": total, "total_nb": total_nb})

    return render(request, "voiture_location/objectifs_ventes.html", {
        "annee": annee,
        "annees": range(aujourdhui.year - 2, aujourdhui.year + 3),
        "mois": range(1, 13),
        "lignes": lignes,
        "total_societe": sum((l["total"] for l in lignes), Decimal("0")),
    })


# -----------------------------
# Règles de location : disponibilité et interdictions
# -----------------------------
def _peut_gerer_interdictions(user):
    return user.is_superuser or getattr(user, "role", None) in ROLES_SUPPRESSION


@never_cache
@login_required
def location_disponibilite(request):
    """Contrôle en direct (formulaire) : le véhicule est-il libre sur la date / le créneau ?"""
    from datetime import date as _date, time as _time
    from django.http import JsonResponse
    from .regles import conflits

    if not _autorise(request.user):
        return JsonResponse({"ok": False, "messages": [str(_("Accès refusé"))]}, status=403)

    def d(nom):
        try:
            return _date.fromisoformat(request.GET.get(nom) or "")
        except ValueError:
            return None

    def h(nom):
        try:
            return _time.fromisoformat(request.GET.get(nom) or "")
        except ValueError:
            return None

    voiture, debut = request.GET.get("voiture"), d("date_debut")
    if not voiture or not debut:
        return JsonResponse({"ok": None, "messages": []})
    exclure = request.GET.get("exclure") or None
    liste = conflits(request.user.societe, voiture, debut, d("date_fin"), h("heure_debut"), h("heure_fin"),
                     exclure_pk=exclure)
    return JsonResponse({"ok": not liste, "messages": [c["message"] for c in liste]})


@never_cache
@login_required
def interdictions_liste(request):
    from .models import InterdictionLocation
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")
    interdictions = (InterdictionLocation.objects.filter(societe=request.user.societe)
                     .select_related("voiture_exemplaire__voiture_marque", "voiture_exemplaire__voiture_modele"))
    afficher = request.GET.get("afficher") or "a_venir"
    if afficher == "a_venir":
        from django.db.models import Q
        aujourdhui = timezone.localdate()
        interdictions = interdictions.filter(Q(date_fin__gte=aujourdhui) | Q(date_fin__isnull=True, date_debut__gte=aujourdhui))
    return render(request, "voiture_location/interdictions_liste.html", {
        "interdictions": interdictions, "afficher": afficher,
        "peut_gerer": _peut_gerer_interdictions(request.user),
    })


def _interdiction_form(request, interdiction=None):
    from .forms import InterdictionLocationForm
    if not _peut_gerer_interdictions(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("voiture_location:interdictions_liste")
    form = InterdictionLocationForm(request.POST or None, instance=interdiction, societe=request.user.societe,
                                    initial={"voiture_exemplaire": request.GET.get("exemplaire")} if not interdiction else None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.societe = request.user.societe
        if not obj.cree_par_id:
            obj.cree_par = request.user
        obj.save()
        from utilisateurs.models import UserLog
        UserLog.objects.create(utilisateur=request.user, action=f"Interdiction de location – {obj}"[:255])
        # Locations déjà enregistrées qui tombent dans la nouvelle interdiction
        from .models import Location
        from .regles import conflits
        touchees = []
        qs = Location.objects.filter(societe=obj.societe, date_debut__lte=obj.date_fin or obj.date_debut)
        if obj.voiture_exemplaire_id:
            qs = qs.filter(voiture_exemplaire_id=obj.voiture_exemplaire_id)
        from django.db.models import Q
        qs = qs.filter(Q(date_fin__gte=obj.date_debut) | Q(date_fin__isnull=True, date_debut__gte=obj.date_debut))
        for loc in qs.select_related("voiture_exemplaire"):
            if any(c["type"] == "interdiction" and c["objet"].pk == obj.pk for c in
                   conflits(obj.societe, loc.voiture_exemplaire_id, loc.date_debut, loc.date_fin,
                            loc.heure_debut, loc.heure_fin, exclure_pk=loc.pk)):
                touchees.append(loc)
        messages.success(request, _("L'interdiction de location a été enregistrée."))
        if touchees:
            messages.warning(request, _("Attention : %(n)s location(s) déjà enregistrée(s) tombent dans cette interdiction : %(liste)s") % {
                "n": len(touchees), "liste": ", ".join(str(l) for l in touchees[:10])})
        return redirect("voiture_location:interdictions_liste")
    return render(request, "voiture_location/interdiction_form.html", {"form": form, "interdiction": interdiction})


@never_cache
@login_required
def interdiction_ajouter(request):
    if not _autorise(request.user):
        return redirect("utilisateurs:dashboard")
    return _interdiction_form(request)


@never_cache
@login_required
def interdiction_modifier(request, pk):
    from .models import InterdictionLocation
    if not _autorise(request.user):
        return redirect("utilisateurs:dashboard")
    return _interdiction_form(request, get_object_or_404(InterdictionLocation, societe=request.user.societe, pk=pk))


@login_required
def interdiction_supprimer(request, pk):
    from .models import InterdictionLocation
    if not _peut_gerer_interdictions(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("voiture_location:interdictions_liste")
    obj = get_object_or_404(InterdictionLocation, societe=request.user.societe, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, _("L'interdiction de location a été supprimée."))
        return redirect("voiture_location:interdictions_liste")
    return render(request, "voiture_location/interdiction_supprimer.html", {"interdiction": obj})

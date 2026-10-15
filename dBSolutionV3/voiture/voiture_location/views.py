from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .forms import LocationForm
from .models import Location

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
        )
        .prefetch_related("factures")
    )


def _peut_facturer(user):
    from facture.views import ROLES_FACTURATION
    return user.is_superuser or getattr(user, "role", None) in ROLES_FACTURATION


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

    form = LocationForm(request.POST or None, user=request.user, initial=initial)
    if request.method == "POST" and form.is_valid():
        location = form.save()
        _log(request.user, ACTION_CREATION_LOCATION, location)
        messages.success(request, _("Location '%(loc)s' créée avec succès.") % {"loc": location})
        return redirect("voiture_location:location_liste")

    return render(request, "voiture_location/location_form.html", {
        "form": form, "location": None, "taux_tva": Location(societe=request.user.societe).taux_tva,
    })


@login_required
def location_modifier(request, location_id):
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    location = get_object_or_404(_queryset(request), id=location_id)
    form = LocationForm(request.POST or None, instance=location, user=request.user)
    if request.method == "POST" and form.is_valid():
        location = form.save()
        _log(request.user, ACTION_MODIFICATION_LOCATION, location)
        messages.success(request, _("Location '%(loc)s' mise à jour.") % {"loc": location})
        return redirect("voiture_location:location_detail", location_id=location.id)

    return render(request, "voiture_location/location_form.html", {
        "form": form, "location": location, "taux_tva": location.taux_tva,
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
    location = get_object_or_404(_queryset(request), id=location_id)

    existante = location.facture
    if existante is not None:
        messages.info(request, _("Cette location est déjà facturée."))
        return redirect("facture:detail", pk=existante.pk)

    type_facture = request.POST.get("type_facture")
    if type_facture not in Facture.TypeFacture.values:
        messages.error(request, _("Type de facture inconnu."))
        return redirect("voiture_location:location_liste")

    facture = creer_facture_depuis_location(location, type_facture, request.user)
    _log(request.user, ACTION_FACTURE_LOCATION, location)
    if type_facture == Facture.TypeFacture.PRO and not facture.societe_cliente_id:
        messages.warning(request, _("Sélectionnez le client professionnel avant d'émettre la facture."))
    messages.success(request, _("Brouillon de facture créé. Le prix de location est TVAC : vérifiez la ligne avant d'émettre."))
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
    return render(request, "voiture_location/location_detail.html", {
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
    html = render_to_string("voiture_location/location_detail_pdf.html", {
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

    # --- Par vendeur ---
    groupes = {}
    for l in locations:
        groupes.setdefault(l.vendeur_id, {"vendeur": l.vendeur, "locations": []})["locations"].append(l)
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
        par_vendeur.append(stats)
    par_vendeur.sort(key=lambda s: s["tvac"], reverse=True)

    # --- Par mois ---
    mois = {}
    for l in locations:
        mois.setdefault((l.date_debut.year, l.date_debut.month), []).append(l)
    par_mois = [
        {"annee": a, "mois": m, "date": l_[0].date_debut.replace(day=1), **_cumul_ventes(l_)}
        for (a, m), l_ in sorted(mois.items())
    ]
    max_mois = max((m["tvac"] for m in par_mois), default=Decimal("0"))
    for m in par_mois:
        m["largeur"] = int(m["tvac"] * 100 / max_mois) if max_mois else 0

    # --- Circuits / routes les plus vendus ---
    lieux = {}
    for l in locations:
        cle = l.lieu or l.get_type_location_display()
        lieux.setdefault(cle, []).append(l)
    top_lieux = sorted(
        ({"lieu": k, "type": v[0].get_type_location_display(), **_cumul_ventes(v)} for k, v in lieux.items()),
        key=lambda s: s["tvac"], reverse=True,
    )[:10]

    return render(request, "voiture_location/statistiques_ventes.html", {
        **periode,
        "voit_tout": voit_tout,
        "vendeur_connecte": request.user,
        "totaux": totaux,
        "par_vendeur": par_vendeur,
        "par_mois": par_mois,
        "top_lieux": top_lieux,
    })

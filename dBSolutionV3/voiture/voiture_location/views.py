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
from .models import Location, ObjectifVente

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
        .prefetch_related("factures", "boxes")
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
    vehicules = form.fields["voiture_exemplaire"].queryset
    # Box en pit lane : rattachés à la location du véhicule 1
    boxes_fs = LocationBoxFormSet(request.POST or None, instance=Location(), prefix="box")

    # Véhicules supplémentaires (même client) : une location complète par véhicule
    forms_sup = []
    if request.method == "POST":
        for idx in request.POST.getlist("sup_index"):
            if idx.isdigit():
                forms_sup.append(LocationVehiculeSupForm(request.POST, prefix=f"sup-{idx}", vehicules=vehicules))

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
                    _appliquer_remise(copie, remise)
                    copie.save()  # crée aussi le checkup piste dans l'agenda
                    _log(request.user, ACTION_CREATION_LOCATION, copie)
                    creees.append(copie)

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
        "champs_vehicule": CHAMPS_VEHICULE,
        "remise": remise_brute if request.method == "POST" else "0",
        "boxes_fs": boxes_fs,
        "prix_instructeurs": form.prix_instructeurs,
    })


# Champs propres à chaque véhicule loué (affichés dans la fiche de chaque véhicule)
CHAMPS_VEHICULE = ["type_location", "circuit", "route", "date_debut", "date_fin", "nombre_tours", "kilometrage", "prix"]


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
        "avancement": avancement_global,
        "a_objectifs": bool(objectifs),
        "peut_objectifs": _voit_tout(request.user),
    })


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

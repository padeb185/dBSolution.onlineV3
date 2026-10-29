import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from utilisateurs.models import UserLog
from utils.securite import ROLES_ATELIER, peut_supprimer, refuser_suppression, roles_requis

from .forms import ParkingForm
from .models import (LETTRES, PAYS_DEFAUT, STYLES_PLAQUE, OccupationBox, Parking, TypeCase, cle_plaque, style_plaque,
                     normaliser_immatriculation)

# Consultation et placement des véhicules : atelier (+ vendeur) ; plan et paramètres : direction / chef mécanicien
ROLES_PARKING = tuple(ROLES_ATELIER) + ("vendeur",)
ROLES_EDITION = ("direction", "chef_mecanicien")

ACTION_PLAN = gettext_noop("Modification du plan du parking")
ACTION_BOX = gettext_noop("Parking : box")
ACTION_SUPPRESSION = gettext_noop("Suppression du parking")


def _peut_editer(user):
    return getattr(user, "is_superuser", False) or getattr(user, "role", None) in ROLES_EDITION


def _parkings(request):
    return Parking.objects.filter(societe=request.user.societe)


def _get_parking(request, pk):
    return get_object_or_404(_parkings(request), pk=pk)


def _vehicules(request):
    from voiture.voiture_exemplaire.models import VoitureExemplaire
    return (VoitureExemplaire.objects.filter(societe=request.user.societe)
            .exclude(immatriculation__isnull=True).exclude(immatriculation="")
            .select_related("voiture_marque", "voiture_modele")
            .order_by("immatriculation"))


def _vehicules_plaques(request):
    """Véhicules avec la mise en forme de leur plaque (pays de la fiche), pour le choix dans un box."""
    vehicules = list(_vehicules(request))
    for v in vehicules:
        v.pays_plaque = getattr(v, "pays", None) or PAYS_DEFAUT
        v.plaque = style_plaque(v.pays_plaque)
    return vehicules


def _log(user, action, parking, detail=""):
    UserLog.objects.create(utilisateur=user, action=f"{action} : {parking.nom}" + (f" – {detail}" if detail else ""))


# -----------------------------
# Liste / paramètres
# -----------------------------
@never_cache
@login_required
@roles_requis(*ROLES_PARKING)
def parking_liste(request):
    return render(request, "parking/liste.html", {
        "parkings": _parkings(request).prefetch_related("occupations"),
        "peut_editer": _peut_editer(request.user),
    })


@login_required
@roles_requis(*ROLES_EDITION)
def parking_form(request, pk=None):
    parking = _get_parking(request, pk) if pk else None
    if request.method == "POST":
        form = ParkingForm(request.POST, instance=parking)
        if form.is_valid():
            p = form.save(commit=False)
            p.societe = request.user.societe
            # Cases du plan hors de la nouvelle grille : supprimées
            p.plan = Parking.nettoyer_plan(p.plan, list(LETTRES[: p.nombre_lignes]), p.nombre_emplacements)
            p.save()
            messages.success(request, _("Parking « %(nom)s » enregistré.") % {"nom": p.nom})
            # Nouveau parking : on dessine tout de suite le plan
            return redirect("parking:editer" if parking is None else "parking:plan", pk=p.pk)
        messages.error(request, _("Veuillez corriger les erreurs du formulaire."))
    else:
        form = ParkingForm(instance=parking)
    return render(request, "parking/form.html", {"form": form, "parking": parking})


@login_required
def parking_supprimer(request, pk):
    if not peut_supprimer(request.user):
        return refuser_suppression(request)
    parking = _get_parking(request, pk)
    if request.method == "POST":
        nom = parking.nom
        with transaction.atomic():
            parking.delete()
            UserLog.objects.create(utilisateur=request.user, action=f"{ACTION_SUPPRESSION} : {nom}")
        messages.success(request, _("Le parking « %(nom)s » a bien été supprimé.") % {"nom": nom})
        return redirect("parking:liste")
    return render(request, "parking/delete.html", {"parking": parking})


# -----------------------------
# Plan (consultation + placement des véhicules)
# -----------------------------
@never_cache
@login_required
@roles_requis(*ROLES_PARKING)
def parking_plan(request, pk):
    parking = _get_parking(request, pk)
    return render(request, "parking/plan.html", {
        "parking": parking,
        "dessin": parking.dessin(),
        "vehicules": _vehicules_plaques(request),
        "pays_plaques": list(STYLES_PLAQUE),
        "pays_defaut": PAYS_DEFAUT,
        "peut_editer": _peut_editer(request.user),
        "recherche": (request.GET.get("q") or "").strip(),
    })


@login_required
@roles_requis(*ROLES_PARKING)
@require_POST
def parking_box(request, pk):
    """Place une immatriculation dans un box, ou libère le box. Un box = une seule immatriculation."""
    from voiture.voiture_exemplaire.models import VoitureExemplaire

    parking = _get_parking(request, pk)
    code = (request.POST.get("code") or "").strip().upper()
    if not parking.est_box(code):
        messages.error(request, _("Ce n'est pas un box : %(code)s.") % {"code": code or "-"})
        return redirect("parking:plan", pk=parking.pk)

    with transaction.atomic():
        Parking.objects.select_for_update().filter(pk=parking.pk).first()
        occupation = OccupationBox.objects.filter(parking=parking, code=code).first()

        if request.POST.get("action") == "liberer":
            if occupation:
                plaque = occupation.immatriculation
                occupation.delete()
                _log(request.user, ACTION_BOX, parking, f"{code} {_('libéré')} ({plaque})")
                messages.success(request, _("Box %(code)s libéré.") % {"code": code})
            return redirect("parking:plan", pk=parking.pk)

        vehicule = None
        vehicule_id = request.POST.get("vehicule") or ""
        if vehicule_id:
            vehicule = VoitureExemplaire.objects.filter(pk=vehicule_id, societe=request.user.societe).first()
            if vehicule is None:
                messages.error(request, _("Véhicule introuvable."))
                return redirect("parking:plan", pk=parking.pk)
        plaque = normaliser_immatriculation(vehicule.immatriculation if vehicule else request.POST.get("immatriculation"))
        if not plaque:
            messages.error(request, _("Indiquez l'immatriculation ou choisissez un véhicule."))
            return redirect("parking:plan", pk=parking.pk)
        if vehicule is None:
            # Plaque saisie à la main : rattachée au véhicule enregistré si elle existe
            cle = cle_plaque(plaque)
            vehicule = next((v for v in _vehicules(request) if cle_plaque(v.immatriculation) == cle), None)
            if vehicule is not None:
                plaque = normaliser_immatriculation(vehicule.immatriculation)   # plaque telle qu'enregistrée

        if occupation and cle_plaque(occupation.immatriculation) != cle_plaque(plaque):
            messages.error(request, _("Le box %(code)s est déjà occupé par %(plaque)s : libérez-le d'abord.")
                           % {"code": code, "plaque": occupation.immatriculation})
            return redirect("parking:plan", pk=parking.pk)

        # La même voiture n'est jamais dans deux box : elle est déplacée
        anciens = OccupationBox.objects.filter(parking__societe=request.user.societe).exclude(parking=parking, code=code)
        deplaces = [o for o in anciens.select_related("parking")
                    if (vehicule and o.vehicule_id == vehicule.pk) or cle_plaque(o.immatriculation) == cle_plaque(plaque)]
        for o in deplaces:
            messages.info(request, _("%(plaque)s quitte le box %(ancien)s (%(parking)s).")
                          % {"plaque": o.immatriculation, "ancien": o.code, "parking": o.parking.nom})
            o.delete()

        if occupation is None:
            occupation = OccupationBox(parking=parking, code=code, depuis=timezone.now())
        occupation.vehicule = vehicule
        occupation.immatriculation = plaque
        occupation.remarque = (request.POST.get("remarque") or "").strip()[:120]
        pays = request.POST.get("pays") or ""
        occupation.pays = (vehicule.pays if vehicule and vehicule.pays else
                           (pays if pays in STYLES_PLAQUE else PAYS_DEFAUT))
        occupation.modifie_par = request.user
        occupation.save()
        _log(request.user, ACTION_BOX, parking, f"{code} ← {plaque}")
    messages.success(request, _("%(plaque)s placé dans le box %(code)s.") % {"plaque": plaque, "code": code})
    return redirect("parking:plan", pk=parking.pk)


# -----------------------------
# Édition du plan (box, lignes d'accès, zones inaccessibles)
# -----------------------------
@never_cache
@login_required
@roles_requis(*ROLES_EDITION)
def parking_editer(request, pk):
    parking = _get_parking(request, pk)
    if request.method == "POST":
        try:
            donnees = json.loads(request.POST.get("plan") or "{}")
        except ValueError:
            donnees = None
        if not isinstance(donnees, dict):
            messages.error(request, _("Plan invalide."))
            return redirect("parking:editer", pk=parking.pk)
        plan = Parking.nettoyer_plan(donnees, parking.lettres, parking.nombre_emplacements)
        bloques = parking.codes_occupes_hors_box(plan=plan)
        if bloques:
            messages.error(request, _("Ces box sont occupés et ne peuvent pas devenir une ligne d'accès ou une zone "
                                      "inaccessible : %(codes)s. Libérez-les d'abord.") % {"codes": ", ".join(bloques)})
            return redirect("parking:editer", pk=parking.pk)
        parking.plan = plan
        parking.save(update_fields=["plan", "updated_at"])
        _log(request.user, ACTION_PLAN, parking, _("%(n)s box") % {"n": parking.nombre_box})
        messages.success(request, _("Plan enregistré : %(n)s box.") % {"n": parking.nombre_box})
        return redirect("parking:editer", pk=parking.pk)

    return render(request, "parking/editer.html", {
        "parking": parking,
        "grille": parking.grille(),
        "dessin": parking.dessin(),
        "plan_json": json.dumps(parking.plan or {}),
        "occupes_json": json.dumps(sorted(parking.occupations.values_list("code", flat=True))),
        "types": TypeCase,
    })


# -----------------------------
# Écran TV (grand écran, nouvelle fenêtre, rafraîchissement automatique)
# -----------------------------
@never_cache
@login_required
@roles_requis(*ROLES_PARKING)
def parking_tv(request, pk):
    parking = _get_parking(request, pk)
    return render(request, "parking/tv.html", {
        "parking": parking,
        "dessin": parking.dessin(),
        "maintenant": timezone.localtime(),
        "jeton_plan": _jeton_plan(parking),
    })


def _jeton_plan(parking):
    """Identifiant de version du plan : l'écran TV se recharge quand il change."""
    return str(int(parking.updated_at.timestamp())) if parking.updated_at else ""


@never_cache
@login_required
@roles_requis(*ROLES_PARKING)
def parking_etat(request, pk):
    """État des box en JSON (rafraîchissement de l'écran TV sans recharger la page)."""
    parking = _get_parking(request, pk)
    return JsonResponse({
        "occupes": {o.code: {"plaque": o.immatriculation, "vehicule": o.libelle_vehicule, "style": o.plaque}
                    for o in parking.occupations.select_related("vehicule__voiture_marque", "vehicule__voiture_modele")},
        "libres": parking.nombre_libres,
        "box": parking.nombre_box,
        "maj": _jeton_plan(parking),
    })


from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Max, Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from core.suppression import analyser_suppression
from maintenance.models import Maintenance
from utilisateurs.models import UserLog

from .forms import FactureForm, FactureLineFormSet, ParametresPeppolForm
from .models import Facture, ParametresPeppol
from .services import (
    appliquer_marges,
    creer_facture_depuis_maintenances,
    emettre_facture,
    erreurs_emission,
)

# Qui peut facturer (+ super admin)
ROLES_FACTURATION = ["direction", "chef_mecanicien", "comptable"]
# Qui peut supprimer un brouillon (+ super admin)
ROLES_SUPPRESSION = ["direction", "chef_mecanicien"]
# Qui peut paramétrer Peppol (+ super admin)
ROLES_PARAMETRES = ["direction"]

ACTION_CREATION_FACTURE = gettext_noop("Création d'une facture")
ACTION_EMISSION_FACTURE = gettext_noop("Émission de la facture")
ACTION_SUPPRESSION_FACTURE = gettext_noop("Suppression d'un brouillon de facture")
ACTION_PARAMETRES_PEPPOL = gettext_noop("Modification des paramètres Peppol")
ACTION_ENVOI_PEPPOL = gettext_noop("Envoi Peppol de la facture")


def _peut(user, roles):
    return user.is_superuser or getattr(user, "role", None) in roles


def _refuser(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _factures(request):
    return Facture.objects.filter(societe=request.user.societe)


def _get_facture(request, pk):
    return get_object_or_404(
        _factures(request).select_related(
            "societe", "societe__adresse", "client_particulier", "client_particulier__adresse",
            "societe_cliente", "societe_cliente__adresse", "voiture_exemplaire",
            "voiture_exemplaire__voiture_marque", "voiture_exemplaire__voiture_modele",
        ),
        pk=pk,
    )


def _log(user, action, facture):
    libelle = facture.numero or _("brouillon")
    client = facture.nom_client_courant()
    UserLog.objects.create(
        utilisateur=user,
        action=f"{action} : {libelle}" + (f" – {client}" if client else ""),
    )


# -----------------------------
# Maintenances à facturer
# -----------------------------
@never_cache
@login_required
def maintenances_a_facturer_view(request):
    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)

    maintenances = (
        Maintenance.objects.all()
        .select_related(
            "voiture_exemplaire",
            "voiture_exemplaire__voiture_marque",
            "voiture_exemplaire__voiture_modele",
            "voiture_exemplaire__client",
        )
        .prefetch_related(
            Prefetch("factures", queryset=Facture.objects.only("id_facture", "numero", "statut", "type_facture"))
        )
        .order_by("-date_intervention")
    )

    return render(request, "facture/maintenances_a_facturer.html", {
        "maintenances": maintenances,
        "type_client": Facture.TypeFacture.CLIENT,
        "type_pro": Facture.TypeFacture.PRO,
        "peut_parametrer": _peut(request.user, ROLES_PARAMETRES),
    })


@login_required
@require_POST
def creer_facture_view(request):
    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)

    type_facture = request.POST.get("type_facture")
    if type_facture not in Facture.TypeFacture.values:
        messages.error(request, _("Type de facture inconnu."))
        return redirect("facture:maintenances")

    ids = request.POST.getlist("maintenances")
    maintenances = list(
        Maintenance.objects.filter(pk__in=ids)
        .select_related("voiture_exemplaire", "voiture_exemplaire__client")
        .order_by("date_intervention")
    )
    if not maintenances:
        messages.error(request, _("Sélectionnez au moins une maintenance."))
        return redirect("facture:maintenances")

    vehicules = {m.voiture_exemplaire_id for m in maintenances}
    if len(vehicules) > 1:
        messages.error(request, _("Les maintenances sélectionnées doivent concerner le même véhicule."))
        return redirect("facture:maintenances")

    facture = creer_facture_depuis_maintenances(maintenances, type_facture, request.user)
    _log(request.user, ACTION_CREATION_FACTURE, facture)
    messages.success(request, _("Brouillon de facture créé. Vérifiez les marges et les lignes avant d'émettre."))
    return redirect("facture:modifier", pk=facture.pk)


# -----------------------------
# Liste des factures
# -----------------------------
@never_cache
@login_required
def facture_list_view(request):
    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)

    factures = _factures(request).select_related(
        "client_particulier", "societe_cliente", "voiture_exemplaire"
    )
    return render(request, "facture/facture_list.html", {"factures": factures})


# -----------------------------
# Brouillon : modification (marges, lignes, client) et émission
# -----------------------------
@never_cache
@login_required
def facture_modifier_view(request, pk):
    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)

    facture = _get_facture(request, pk)
    if not facture.est_brouillon:
        messages.info(request, _("Cette facture est émise : elle ne peut plus être modifiée."))
        return redirect("facture:detail", pk=facture.pk)

    if request.method == "POST":
        form = FactureForm(request.POST, instance=facture, user=request.user)
        formset = FactureLineFormSet(request.POST, instance=facture, prefix="lignes")
        action = request.POST.get("action", "enregistrer")

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                facture = form.save()
                ordre_max = facture.lines.aggregate(m=Max("ordre"))["m"] or 0
                lignes = formset.save(commit=False)
                for ligne in formset.deleted_objects:
                    ligne.delete()
                for ligne in lignes:
                    if not ligne.pk:
                        ordre_max += 1
                        ligne.ordre = ordre_max
                    ligne.facture = facture
                    ligne.save()

                if action == "appliquer_marges":
                    appliquer_marges(facture)
                    messages.success(request, _("Marges appliquées à toutes les lignes."))
                else:
                    facture.recalculer_totaux()

            if action == "emettre":
                erreurs = erreurs_emission(facture)
                if erreurs:
                    for erreur in erreurs:
                        messages.error(request, erreur)
                    return redirect("facture:modifier", pk=facture.pk)
                facture = emettre_facture(facture)
                _log(request.user, ACTION_EMISSION_FACTURE, facture)
                messages.success(request, _("Facture %(numero)s émise.") % {"numero": facture.numero})

                parametres = ParametresPeppol.pour_societe(request.user.societe)
                if facture.est_pro and parametres and parametres.est_configure and parametres.envoi_automatique:
                    _envoyer_peppol(request, facture, parametres)
                return redirect("facture:detail", pk=facture.pk)

            if action == "enregistrer":
                messages.success(request, _("Facture enregistrée."))
            return redirect("facture:modifier", pk=facture.pk)

        messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = FactureForm(instance=facture, user=request.user)
        formset = FactureLineFormSet(instance=facture, prefix="lignes")

    return render(request, "facture/facture_form.html", {
        "facture": facture,
        "form": form,
        "formset": formset,
        "groupes_tva": facture.totaux_par_taux(),
        "marge_totale": sum((l.marge_montant for l in facture.lines.all()), 0),
        "peut_supprimer": _peut(request.user, ROLES_SUPPRESSION),
    })


# -----------------------------
# Détail (facture émise)
# -----------------------------
@never_cache
@login_required
def facture_detail_view(request, pk):
    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)

    facture = _get_facture(request, pk)
    if facture.est_brouillon:
        return redirect("facture:modifier", pk=facture.pk)

    return render(request, "facture/facture_detail.html", {
        "facture": facture,
        "lignes": facture.lines.all(),
        "groupes_tva": facture.totaux_par_taux(),
        "marge_totale": sum((l.marge_montant for l in facture.lines.all()), 0),
        "peppol_configure": _peppol_configure(request),
        "parametres_peppol": ParametresPeppol.pour_societe(request.user.societe),
        "peut_parametrer": _peut(request.user, ROLES_PARAMETRES),
    })


# -----------------------------
# PDF (sur le modèle des PDF de maintenance)
# -----------------------------
@login_required
def facture_pdf_view(request, pk):
    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)

    from weasyprint import HTML

    facture = _get_facture(request, pk)
    html_string = render_to_string("facture/facture_pdf.html", {
        "facture": facture,
        "lignes": facture.lines.all(),
        "groupes_tva": facture.totaux_par_taux(),
        "societe": facture.societe or request.user.societe,
        "date_export": datetime.now(),
    }, request=request)

    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    nom = facture.numero or f"brouillon_{str(facture.pk)[:8]}"
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{_("Facture")}_{nom}.pdf"'
    return response


# -----------------------------
# XML UBL / Peppol (factures pro)
# -----------------------------
@login_required
def facture_xml_view(request, pk):
    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)

    facture = _get_facture(request, pk)
    if not facture.est_pro or not facture.est_emise:
        messages.error(request, _("Le XML n'est disponible que pour une facture professionnelle émise."))
        return redirect("facture:detail", pk=facture.pk)

    if not facture.xml_ubl:
        from .peppol.generator import generate_peppol_invoice
        facture.xml_ubl = generate_peppol_invoice(facture).decode("utf-8")
        facture.save(update_fields=["xml_ubl"])

    response = HttpResponse(facture.xml_ubl.encode("utf-8"), content_type="application/xml")
    response["Content-Disposition"] = f'attachment; filename="{facture.numero}.xml"'
    return response


def _peppol_configure(request):
    from django.conf import settings
    parametres = ParametresPeppol.pour_societe(request.user.societe)
    if parametres is not None:
        return parametres.est_configure
    return bool(getattr(settings, "PEPPOL_ACCESS_POINT_URL", None) and getattr(settings, "PEPPOL_API_KEY", None))


def _envoyer_peppol(request, facture, parametres):
    """Envoie la facture et enregistre le résultat. Retourne True si l'envoi a réussi."""
    from .peppol.sender import PeppolSendError, send_to_peppol

    environnement = parametres.get_environnement_display() if parametres else "settings.py"
    try:
        reponse = send_to_peppol(facture.xml_ubl.encode("utf-8"), parametres=parametres)
    except PeppolSendError as e:
        facture.peppol_reponse = f"[{environnement}] ERREUR : {e}"
        facture.save(update_fields=["peppol_reponse"])
        messages.error(request, _("Envoi Peppol impossible : %(erreur)s") % {"erreur": e})
        return False

    facture.peppol_envoyee_le = timezone.now()
    facture.peppol_reponse = f"[{environnement}] {reponse}"
    facture.save(update_fields=["peppol_envoyee_le", "peppol_reponse"])
    _log(request.user, ACTION_ENVOI_PEPPOL, facture)
    if parametres and parametres.est_test:
        messages.warning(request, _("Facture envoyée au serveur Peppol de TEST (aucune valeur légale)."))
    else:
        messages.success(request, _("Facture envoyée via Peppol."))
    return True


@login_required
@require_POST
def facture_envoyer_peppol_view(request, pk):
    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)

    facture = _get_facture(request, pk)
    if not facture.est_pro or not facture.est_emise or not facture.xml_ubl:
        messages.error(request, _("Seule une facture professionnelle émise peut être envoyée via Peppol."))
        return redirect("facture:detail", pk=facture.pk)

    _envoyer_peppol(request, facture, ParametresPeppol.pour_societe(request.user.societe))
    return redirect("facture:detail", pk=facture.pk)


# -----------------------------
# Paramètres Peppol (serveur de test / production)
# -----------------------------
@never_cache
@login_required
def parametres_peppol_view(request):
    if not _peut(request.user, ROLES_PARAMETRES):
        return _refuser(request)

    societe = request.user.societe
    parametres = ParametresPeppol.pour_societe(societe) or ParametresPeppol(societe=societe)

    if request.method == "POST":
        action = request.POST.get("action", "enregistrer")
        form = ParametresPeppolForm(request.POST, instance=parametres)

        if form.is_valid():
            parametres = form.save()
            if action == "enregistrer":
                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_PARAMETRES_PEPPOL} : {parametres.get_environnement_display()}"
                           + (" – " + _("activé") if parametres.actif else " – " + _("désactivé")),
                )
                messages.success(request, _("Paramètres Peppol enregistrés."))
            else:
                _tester_serveur(request, parametres, action)
            return redirect("facture:parametres_peppol")

        messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = ParametresPeppolForm(instance=parametres)

    from .peppol.generator import endpoint

    adresse = getattr(societe, "adresse", None)
    schema, valeur = endpoint(
        parametres.peppol_id,
        getattr(societe, "numero_tva", ""),
        (adresse.code_pays if adresse and adresse.code_pays else "BE"),
    )

    return render(request, "facture/parametres_peppol.html", {
        "form": form,
        "parametres": parametres,
        "peppol_id_effectif": f"{schema}:{valeur}" if valeur else "",
        "settings_peppol": _peppol_configure_settings(),
    })


def _peppol_configure_settings():
    from django.conf import settings
    return bool(getattr(settings, "PEPPOL_ACCESS_POINT_URL", None) and getattr(settings, "PEPPOL_API_KEY", None))


def _tester_serveur(request, parametres, action):
    from .peppol.sender import tester_connexion

    production = action == "tester_production"
    url = parametres.url_production if production else parametres.url_test
    cle = parametres.cle_api_production if production else parametres.cle_api_test
    libelle = _("production") if production else _("test")

    if not url or not cle:
        messages.error(request, _("Renseignez l'URL et la clé API du serveur de %(env)s.") % {"env": libelle})
        return

    if parametres.type_auth == ParametresPeppol.TypeAuth.ENTETE:
        entetes = {(parametres.nom_entete or "X-API-Key"): cle}
    else:
        entetes = {"Authorization": f"Bearer {cle}"}

    ok, resultat = tester_connexion(url, entetes, timeout=min(parametres.timeout or 15, 30))
    parametres.derniere_verification = timezone.now()
    parametres.dernier_resultat = f"[{libelle}] {resultat}"
    parametres.dernier_test_ok = ok
    parametres.save(update_fields=["derniere_verification", "dernier_resultat", "dernier_test_ok", "updated_at"])

    if ok:
        messages.success(request, _("Serveur de %(env)s : %(res)s") % {"env": libelle, "res": resultat})
    else:
        messages.error(request, _("Serveur de %(env)s : %(res)s") % {"env": libelle, "res": resultat})


# -----------------------------
# Suppression d'un brouillon
# -----------------------------
@never_cache
@login_required
def delete_facture_view(request, pk):
    facture = _get_facture(request, pk)

    if not _peut(request.user, ROLES_SUPPRESSION):
        messages.error(request, _("Accès refusé"))
        return redirect("facture:modifier", pk=facture.pk)

    if not facture.est_brouillon:
        messages.error(request, _("Une facture émise ne peut pas être supprimée (établissez une note de crédit)."))
        return redirect("facture:detail", pk=facture.pk)

    analyse = analyser_suppression(facture)

    if request.method == "POST":
        with transaction.atomic():
            _log(request.user, ACTION_SUPPRESSION_FACTURE, facture)
            facture.delete()
        messages.success(request, _("Le brouillon de facture a bien été supprimé."))
        return redirect("facture:maintenances")

    return render(request, "facture/delete_facture.html", {
        "facture": facture,
        "lignes": facture.lines.all(),
        "objets_supprimes": analyse["supprimes"],
        "objets_bloquants": analyse["bloquants"],
        "url_annuler": reverse("facture:modifier", kwargs={"pk": facture.pk}),
    })

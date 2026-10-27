from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

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
    creer_facture_depuis_diagnostic,
    creer_facture_depuis_maintenances,
    creer_factures_par_parts,
    emettre_facture,
    emettre_repartition,
    erreurs_emission,
    factures_existantes,
    parts_vehicule,
)

# Qui peut facturer (+ super admin)
logger = logging.getLogger(__name__)

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
ACTION_PAIEMENT_FACTURE = gettext_noop("Paiement de la facture")


def _peut(user, roles):
    return user.is_superuser or getattr(user, "role", None) in roles


# Le vendeur a accès aux factures des locations (consultation, émission, encaissement)
ROLES_FACTURATION_LOCATION = ["vendeur"]


def _vendeur_locations(user):
    """Vrai si l'utilisateur n'a accès qu'aux factures des locations."""
    return not _peut(user, ROLES_FACTURATION) and _peut(user, ROLES_FACTURATION_LOCATION)


def _peut_facture(user, facture):
    """Accès à une facture : rôles de facturation, ou vendeur pour une facture de location."""
    if _peut(user, ROLES_FACTURATION):
        return True
    return _vendeur_locations(user) and facture.locations.exists()


def _refuser(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _factures(request):
    return Facture.objects.filter(societe=request.user.societe)


def _get_facture(request, pk):
    return get_object_or_404(
        _factures(request).select_related(
            "societe", "societe__adresse", "client_particulier", "client_particulier__adresse",
            "client_atelier__client_particulier", "client_atelier__societe_cliente",
            "societe_cliente", "societe_cliente__adresse", "voiture_exemplaire",
            "proprietaire", "proprietaire__adresse", "part_proprietaire",
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

    from voiture.voiture_diagnostic.models import Diagnostic
    diagnostics = (
        Diagnostic.objects.filter(societe=request.user.societe)
        .select_related("voiture_exemplaire__voiture_marque", "voiture_exemplaire__voiture_modele",
                        "voiture_exemplaire__client")
        .prefetch_related(
            "codes",
            Prefetch("factures", queryset=Facture.objects.only("id_facture", "numero", "statut", "type_facture")),
        )
        .order_by("-date_diagnostic")
    )

    return render(request, "facture/maintenances_a_facturer.html", {
        "diagnostics": diagnostics,
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

    from voiture.voiture_diagnostic.models import Diagnostic

    ids = [i for i in request.POST.getlist("maintenances") if i]
    ids_diagnostics = [i for i in request.POST.getlist("diagnostics") if i]
    maintenances = list(
        Maintenance.objects.filter(pk__in=ids)
        .select_related("voiture_exemplaire", "voiture_exemplaire__client")
        .order_by("date_intervention")
    ) if ids else []
    diagnostics = list(
        Diagnostic.objects.filter(pk__in=ids_diagnostics, societe=request.user.societe)
        .select_related("voiture_exemplaire", "voiture_exemplaire__client")
        .prefetch_related("codes")
        .order_by("date_diagnostic")
    ) if ids_diagnostics else []
    if not maintenances and not diagnostics:
        messages.error(request, _("Sélectionnez au moins une maintenance ou un diagnostic."))
        return redirect("facture:maintenances")

    vehicules = {m.voiture_exemplaire_id for m in maintenances} | {d.voiture_exemplaire_id for d in diagnostics}
    if len(vehicules) > 1:
        messages.error(request, _("Les maintenances et diagnostics sélectionnés doivent concerner le même véhicule."))
        return redirect("facture:maintenances")
    if None in vehicules:
        messages.error(request, _("Ce diagnostic n'est lié à aucun véhicule."))
        return redirect("facture:maintenances")

    vehicule = (maintenances[0] if maintenances else diagnostics[0]).voiture_exemplaire
    with transaction.atomic():
        reponse = _deja_facture(request, maintenances, diagnostics)
        if reponse is not None:
            return reponse
        reponse = _facturer_par_parts(request, vehicule, maintenances, diagnostics)
        if reponse is not None:
            return reponse

        facture = creer_facture_depuis_maintenances(maintenances, type_facture, request.user, diagnostics=diagnostics)
        _log(request.user, ACTION_CREATION_FACTURE, facture)
    messages.success(request, _("Brouillon de facture créé. Vérifiez les marges et les lignes avant d'émettre."))
    return redirect("facture:modifier", pk=facture.pk)


def _deja_facture(request, maintenances, diagnostics):
    """
    Refuse de facturer une seconde fois une maintenance ou un diagnostic déjà repris sur une facture
    (brouillon ou émise). Retourne une redirection, ou None si tout est à facturer.
    """
    existantes = factures_existantes(maintenances, diagnostics)
    if not existantes:
        return None
    libelles = ", ".join(
        (f.numero or _("brouillon")) + (f" – {f.nom_client_courant()}" if f.nom_client_courant() else "")
        for f in existantes
    )
    messages.error(
        request,
        _("Déjà facturé : %(factures)s. Une maintenance ou un diagnostic ne peut être facturé qu'une seule fois "
          "(supprimez le brouillon pour le refaire).") % {"factures": libelles},
    )
    f = existantes[0]
    return redirect("facture:modifier" if f.est_brouillon else "facture:detail", pk=f.pk)


def _facturer_par_parts(request, vehicule, maintenances, diagnostics):
    """
    Véhicule avec des propriétaires enregistrés : une facture par propriétaire, au pourcentage de sa part
    (notre société seule propriétaire : une facture interne sans marge). None si le véhicule n'a pas de parts.
    """
    parts, _total = parts_vehicule(vehicule)
    if not parts:
        return None
    try:
        factures = creer_factures_par_parts(maintenances, request.user, diagnostics=diagnostics)
    except ValueError as erreur:
        messages.error(request, str(erreur))
        messages.info(request, _("Complétez les parts du véhicule (menu Direction › Propriétaires) puis recommencez."))
        return redirect("proprietaire:parts_vehicule", exemplaire_id=vehicule.pk)
    for f in factures:
        _log(request.user, ACTION_CREATION_FACTURE, f)
    if len(factures) == 1 and factures[0].client_est_societe:
        messages.success(request, _("Notre société est seule propriétaire : facture interne créée, sans marge (TVA des pièces récupérée)."))
    else:
        messages.success(
            request,
            _("%(n)s brouillons de facture créés, un par propriétaire, chacun au pourcentage de sa part.") % {"n": len(factures)},
        )
    return redirect("facture:modifier", pk=factures[0].pk)


@login_required
@require_POST
def creer_facture_diagnostic_view(request, diagnostic_id):
    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)
    from voiture.voiture_diagnostic.models import Diagnostic

    diagnostic = get_object_or_404(
        Diagnostic.objects.filter(societe=request.user.societe)
        .select_related("voiture_exemplaire", "voiture_exemplaire__client")
        .prefetch_related("codes"),
        id=diagnostic_id,
    )
    type_facture = request.POST.get("type_facture")
    if type_facture not in Facture.TypeFacture.values:
        messages.error(request, _("Type de facture inconnu."))
        return redirect("voiture_diagnostic:diagnostic_detail", diagnostic_id=diagnostic.id)
    if not diagnostic.voiture_exemplaire_id:
        messages.error(request, _("Ce diagnostic n'est lié à aucun véhicule."))
        return redirect("voiture_diagnostic:diagnostic_detail", diagnostic_id=diagnostic.id)

    with transaction.atomic():
        reponse = _deja_facture(request, [], [diagnostic])
        if reponse is not None:
            return reponse
        reponse = _facturer_par_parts(request, diagnostic.voiture_exemplaire, [], [diagnostic])
        if reponse is not None:
            return reponse

        facture = creer_facture_depuis_diagnostic(diagnostic, type_facture, request.user)
        _log(request.user, ACTION_CREATION_FACTURE, facture)
    if not diagnostic.taux_horaire:
        messages.warning(request, _("Aucun taux horaire sur le diagnostic : complétez le prix de la ligne avant d'émettre."))
    messages.success(request, _("Brouillon de facture créé. Vérifiez les marges et les lignes avant d'émettre."))
    return redirect("facture:modifier", pk=facture.pk)


# -----------------------------
# Liste des factures
# -----------------------------
@never_cache
@login_required
def facture_list_view(request):
    vendeur = _vendeur_locations(request.user)
    if not (_peut(request.user, ROLES_FACTURATION) or vendeur):
        return _refuser(request)

    factures = _factures(request).select_related(
        "client_particulier", "client_atelier__client_particulier", "societe_cliente", "voiture_exemplaire"
    )
    if vendeur:
        factures = factures.filter(locations__isnull=False).distinct()
    return render(request, "facture/facture_list.html", {
        "factures": factures,
        "types_facture": Facture.TypeFacture.choices,
        "statuts": Facture.Statut.choices,
        "statuts_paiement": Facture.StatutPaiement.choices,
        "vendeur_locations": vendeur,
    })


# -----------------------------
# Brouillon : modification (marges, lignes, client) et émission
# -----------------------------
@never_cache
@login_required
def facture_modifier_view(request, pk):
    if not (_peut(request.user, ROLES_FACTURATION) or _vendeur_locations(request.user)):
        return _refuser(request)

    facture = _get_facture(request, pk)

    if not _peut_facture(request.user, facture):

        return _refuser(request)
    if not facture.est_brouillon:
        messages.info(request, _("Cette facture est émise : elle ne peut plus être modifiée."))
        return redirect("facture:detail", pk=facture.pk)

    if request.method == "GET":
        # Pièces utilisées ajoutées aux maintenances depuis la création du brouillon
        from .services import synchroniser_brouillon
        # Brouillon sans client : client atelier associé au véhicule
        if (not facture.est_pro and not facture.client_est_societe and not facture.client_particulier_id
                and not facture.client_atelier_id and not facture.proprietaire_id):
            atelier = Facture.client_atelier_du_vehicule(facture.voiture_exemplaire)
            if atelier is not None:
                facture.client_atelier = atelier
                facture.save(update_fields=["client_atelier", "updated_at"])
                messages.info(request, _("Client atelier du véhicule repris sur la facture."))
        try:
            with transaction.atomic():
                synchroniser_brouillon(facture)
        except Exception:
            logger.exception("Synchronisation du brouillon %s impossible", facture.pk)

    if request.method == "POST":
        form = FactureForm(request.POST, instance=facture, user=request.user)
        formset = FactureLineFormSet(request.POST, instance=facture, prefix="lignes")
        action = request.POST.get("action", "enregistrer")

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                # Verrou : la facture a pu être émise entre-temps (double clic, autre onglet)
                if not Facture.objects.select_for_update().filter(
                        pk=facture.pk, statut=Facture.Statut.BROUILLON).exists():
                    messages.info(request, _("Cette facture est déjà émise : elle ne peut plus être modifiée ni émise à nouveau."))
                    return redirect("facture:detail", pk=facture.pk)
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
                elif action == "recharger_maintenances":
                    from .services import synchroniser_brouillon
                    synchroniser_brouillon(facture, forcer=True)
                    messages.success(request, _("Lignes des maintenances rechargées (pièces et main-d'œuvre)."))
                else:
                    facture.recalculer_totaux()

            if action == "emettre":
                erreurs = erreurs_emission(facture)
                if erreurs:
                    for erreur in erreurs:
                        messages.error(request, erreur)
                    return redirect("facture:modifier", pk=facture.pk)
                with transaction.atomic():
                    facture = emettre_facture(facture)
                if not getattr(facture, "vient_d_etre_emise", False):
                    messages.info(request, _("Cette facture est déjà émise (%(numero)s) : elle n'est pas émise une seconde fois.")
                                  % {"numero": facture.numero})
                    return redirect("facture:detail", pk=facture.pk)
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
        "vendeur_locations": _vendeur_locations(request.user),
    })


# -----------------------------
# Répartition par parts : émission de toutes les factures
# -----------------------------
@login_required
@require_POST
def emettre_repartition_view(request, pk):
    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)
    facture = _get_facture(request, pk)
    if not facture.repartition:
        return redirect("facture:modifier" if facture.est_brouillon else "facture:detail", pk=facture.pk)

    with transaction.atomic():
        emises, refusees = emettre_repartition(facture)
    for f in emises:
        _log(request.user, ACTION_EMISSION_FACTURE, f)
    if emises:
        messages.success(
            request,
            _("%(n)s facture(s) émise(s) : %(numeros)s.") % {"n": len(emises), "numeros": ", ".join(f.numero for f in emises)},
        )
        parametres = ParametresPeppol.pour_societe(request.user.societe)
        if parametres and parametres.est_configure and parametres.envoi_automatique:
            for f in emises:
                if f.est_pro:
                    _envoyer_peppol(request, f, parametres)
    for f, erreurs in refusees:
        messages.error(request, _("%(client)s : %(erreurs)s") % {
            "client": f.nom_client_courant() or _("brouillon"), "erreurs": " ".join(str(e) for e in erreurs)})
    if not emises and not refusees:
        messages.info(request, _("Toutes les factures de la répartition sont déjà émises."))
    cible = refusees[0][0] if refusees else facture
    return redirect("facture:modifier" if cible.est_brouillon else "facture:detail", pk=cible.pk)


# -----------------------------
# Détail (facture émise)
# -----------------------------
@never_cache
@login_required
def facture_detail_view(request, pk):
    if not (_peut(request.user, ROLES_FACTURATION) or _vendeur_locations(request.user)):
        return _refuser(request)

    facture = _get_facture(request, pk)

    if not _peut_facture(request.user, facture):

        return _refuser(request)
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
        "vendeur_locations": _vendeur_locations(request.user),
        **_contexte_paiement(facture),
    })


def _contexte_paiement(facture):
    from .models import PaiementFacture
    from .paiements import plafond_especes
    aujourdhui = timezone.localdate()
    pays = facture.pays_vendeur()
    return {
        "paiements": list(facture.paiements.select_related("cree_par").all()),
        "modes_paiement": PaiementFacture.Mode.choices,
        "pays_vendeur": pays,
        "plafond_especes": plafond_especes(pays, aujourdhui),
        "plafond_especes_non_resident": plafond_especes(pays, aujourdhui, non_resident=True),
        "aujourdhui": aujourdhui,
    }


# -----------------------------
# PDF (sur le modèle des PDF de maintenance)
# -----------------------------
@login_required
def facture_pdf_view(request, pk):
    if not (_peut(request.user, ROLES_FACTURATION) or _vendeur_locations(request.user)):
        return _refuser(request)

    from weasyprint import HTML

    facture = _get_facture(request, pk)

    if not _peut_facture(request.user, facture):

        return _refuser(request)
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
    if not (_peut(request.user, ROLES_FACTURATION) or _vendeur_locations(request.user)):
        return _refuser(request)

    facture = _get_facture(request, pk)

    if not _peut_facture(request.user, facture):

        return _refuser(request)
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
    if not (_peut(request.user, ROLES_FACTURATION) or _vendeur_locations(request.user)):
        return _refuser(request)

    facture = _get_facture(request, pk)

    if not _peut_facture(request.user, facture):

        return _refuser(request)
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


# -----------------------------
# TVA : à payer / à récupérer
# -----------------------------
@never_cache
@login_required
def tva_view(request):
    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)

    from maintenance.choices import TVAConfig

    from .tva import CalculTVA

    aujourdhui = timezone.localdate()
    type_periode = request.GET.get("periode", "trimestre")
    if type_periode not in CalculTVA.TYPES_PERIODE:
        type_periode = "trimestre"

    def entier(nom, defaut):
        try:
            return int(request.GET.get(nom, defaut))
        except (TypeError, ValueError):
            return defaut

    annee = entier("annee", aujourdhui.year)
    numero_defaut = aujourdhui.month if type_periode == "mois" else (aujourdhui.month - 1) // 3 + 1
    numero = entier("numero", numero_defaut)

    deductibilite = {}
    for cle in CalculTVA.SOURCES:
        valeur = request.GET.get(f"ded_{cle}")
        if valeur not in (None, ""):
            try:
                deductibilite[cle] = Decimal(valeur.replace(",", "."))
            except Exception:
                pass

    calcul = CalculTVA.pour_periode(request.user.societe, type_periode, annee, numero, deductibilite)
    pays = (request.GET.get("pays") or calcul.pays_par_defaut()).upper()
    if pays not in TVAConfig.TVA_PIECES:
        pays = calcul.pays_par_defaut()

    # Maintenances internes (factures à notre société) : coût de revient par véhicule
    z = Decimal("0.00")
    internes = []
    tot_internes = {"pieces": z, "tva_pieces": z, "main_oeuvre": z, "autres": z, "total": z}
    for f in calcul.tva_a_payer["factures_internes"]:
        c = f.couts_internes()
        internes.append({"facture": f, **c})
        for k in tot_internes:
            tot_internes[k] += c[k]

    if request.GET.get("export") == "csv":
        return _tva_csv(calcul, type_periode, annee, numero, pays, internes, tot_internes)

    return render(request, "facture/tva.html", {
        "internes": internes,
        "tot_internes": tot_internes,
        "calcul": calcul,
        "a_payer": calcul.tva_a_payer,
        "a_recuperer": calcul.tva_a_recuperer,
        "journal_a_payer": calcul.journal_a_payer,
        "journal_a_recuperer": calcul.journal_a_recuperer,
        "declaration": calcul.declaration(pays),
        "pays": pays,
        "pays_choices": TVAConfig.PAYS_CHOICES,
        "type_periode": type_periode,
        "annee": annee,
        "numero": numero,
        "annees": range(aujourdhui.year - 5, aujourdhui.year + 1),
        "mois": range(1, 13),
        "trimestres": range(1, 5),
    })


def _tva_csv(calcul, type_periode, annee, numero, pays, internes, tot_internes):
    """Export CSV (séparateur « ; », virgule décimale) de la page TVA pour le comptable."""
    import csv

    from .models import FactureLine
    from .tva import arrondi

    suffixe = {"mois": f"-{numero:02d}", "trimestre": f"-T{numero}"}.get(type_periode, "")
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="tva_{annee}{suffixe}_{pays}.csv"'
    response.write("\ufeff")
    w = csv.writer(response, delimiter=";")
    fmt = lambda x: f"{x:.2f}".replace(".", ",") if x is not None else ""
    fmt_taux = lambda x: f"{x:g}".replace(".", ",") + " %"
    a_payer, a_recuperer = calcul.tva_a_payer, calcul.tva_a_recuperer

    # En-tête
    w.writerow([_("TVA à payer et à récupérer")])
    w.writerow([_("Du"), calcul.debut.strftime("%d/%m/%Y"), _("au"), calcul.fin.strftime("%d/%m/%Y")])
    w.writerow([_("Pays de la déclaration"), pays])
    w.writerow([])

    # Résumé
    w.writerow([_("Résumé")])
    w.writerow([_("TVA à payer (ventes)"), fmt(a_payer["tva"])])
    w.writerow([_("TVA déductible"), fmt(a_recuperer["tva_deductible"])])
    w.writerow([_("Solde") + " (" + (_("à payer") if calcul.solde > 0 else _("à récupérer")) + ")", fmt(abs(calcul.solde))])
    w.writerow([])

    # Ventes : détail par facture et par taux (hors lignes de location, comptées plus bas)
    w.writerow([_("TVA à payer – détail des factures émises")])
    w.writerow([_("Date"), _("Facture"), _("Client"), _("Taux"), _("Base HTVA"), _("TVA"), _("Autoliquidation")])
    for facture in calcul.factures_periode():
        if facture.client_est_societe:
            continue
        groupes = {}
        for ligne in facture.lines.all():
            if ligne.type_ligne == FactureLine.TypeLigne.LOCATION:
                continue
            taux = Decimal("0") if facture.autoliquidation else arrondi(ligne.vat_rate)
            groupes[taux] = groupes.get(taux, Decimal("0")) + ligne.total_ht
        for taux, base in sorted(groupes.items()):
            base = arrondi(base)
            tva = Decimal("0.00") if facture.autoliquidation else arrondi(base * taux / Decimal("100"))
            w.writerow([facture.issue_date.strftime("%d/%m/%Y"), facture.numero or "", facture.nom_client_courant(),
                        fmt_taux(taux), fmt(base), fmt(tva), _("Oui") if facture.autoliquidation else ""])
    w.writerow([])

    # Locations
    locs = a_payer["locations"]
    w.writerow([_("Locations (circuit / route)")])
    w.writerow([_("Date"), _("Location"), _("Facture"), _("Nature"), _("Montant TVAC"), _("TVA")])
    for l in locs["liste"]:
        w.writerow([l["date"].strftime("%d/%m/%Y"), str(l["location"]), l["facture"].numero if l["facture"] else "",
                    _("Acompte") if l["nature"] == "acompte" else _("Prestation"), fmt(l["tvac"]), fmt(l["tva"])])
    w.writerow([_("Total"), "", "", "", "", fmt(locs["tva"])])
    w.writerow([])

    # TVA à payer par taux
    w.writerow([_("TVA à payer – par taux")])
    w.writerow([_("Taux"), _("Base HTVA"), _("TVA")])
    for l in a_payer["lignes"]:
        w.writerow([fmt_taux(l["taux"]), fmt(l["base"]), fmt(l["tva"])])
    if a_payer["base_autoliquidation"]:
        w.writerow([_("Autoliquidation"), fmt(a_payer["base_autoliquidation"]), fmt(Decimal("0"))])
    w.writerow([_("Total"), fmt(a_payer["base"]), fmt(a_payer["tva"])])
    w.writerow([])

    # TVA à récupérer par source
    w.writerow([_("TVA à récupérer – par source")])
    w.writerow([_("Source"), _("Nombre"), _("Base HTVA"), _("TVA"), _("Déductible (%)"), _("TVA déductible"), _("Remarque")])
    for l in a_recuperer["lignes"]:
        w.writerow([l["label"], l["nb"], fmt(l["base"]), fmt(l["tva"]), fmt(l["deductible"]), fmt(l["tva_deductible"]),
                    _("Informatif (hors total)") if l["informatif"] else ""])
    w.writerow([_("Total"), "", fmt(a_recuperer["base"]), fmt(a_recuperer["tva"]), "", fmt(a_recuperer["tva_deductible"]), ""])
    w.writerow([])

    # Journal des mouvements – TVA à payer
    natures = {"facture": _("Facture"), "acompte": _("Acompte location"), "location": _("Location réalisée")}
    w.writerow([_("Journal des mouvements – TVA à payer")])
    w.writerow([_("Date"), _("Pièce"), _("Client"), _("Libellé"), _("Nature"), _("Taux"), _("Base HTVA"), _("TVA"),
                _("Cumul TVA"), _("Autoliquidation")])
    for m in calcul.journal_a_payer:
        w.writerow([m["date"].strftime("%d/%m/%Y") if m["date"] else "", m["piece"], m["tiers"], m["libelle"],
                    natures.get(m["nature"], m["nature"]), fmt_taux(m["taux"]), fmt(m["base"]), fmt(m["tva"]),
                    fmt(m["cumul"]), _("Oui") if m["autoliquidation"] else ""])
    w.writerow([])

    # Journal des mouvements – TVA à récupérer
    w.writerow([_("Journal des mouvements – TVA à récupérer")])
    w.writerow([_("Date"), _("Source"), _("Pièce"), _("Fournisseur"), _("Libellé"), _("Base HTVA"), _("TVA payée"),
                _("Déductible (%)"), _("TVA à récupérer"), _("Cumul TVA"), _("Remarque")])
    for m in calcul.journal_a_recuperer:
        w.writerow([m["date"].strftime("%d/%m/%Y") if m["date"] else "", m["source"], m["piece"], m["tiers"],
                    m["libelle"], fmt(m["base"]), fmt(m["tva"]), fmt(m["deductible"]), fmt(m["tva_deductible"]),
                    fmt(m["cumul"]), _("Informatif (hors total)") if m["informatif"] else ""])
    w.writerow([])

    # Déclaration nationale
    declaration = calcul.declaration(pays)
    w.writerow([declaration["formulaire"], declaration["pays_nom"]])
    w.writerow([_("Grille"), _("Libellé"), _("Montant")])
    for l in declaration["lignes"]:
        w.writerow([l["grille"], l["libelle"], fmt(l["montant"])])
    w.writerow([])

    # Maintenances internes
    w.writerow([_("Maintenances internes : coûts à charge de la société")])
    w.writerow([_("Date"), _("Facture"), _("Véhicule"), _("Pièces au prix d'achat HTVA"), _("TVA pièces (récupérée via achats)"),
                _("Main-d'œuvre HTVA"), _("Autres HTVA"), _("Coût de revient HTVA")])
    for i in internes:
        f = i["facture"]
        w.writerow([f.issue_date.strftime("%d/%m/%Y"), f.numero or "", str(f.voiture_exemplaire) if f.voiture_exemplaire else "",
                    fmt(i["pieces"]), fmt(i["tva_pieces"]), fmt(i["main_oeuvre"]), fmt(i["autres"]), fmt(i["total"])])
    w.writerow([_("Total"), "", "", fmt(tot_internes["pieces"]), fmt(tot_internes["tva_pieces"]),
                fmt(tot_internes["main_oeuvre"]), fmt(tot_internes["autres"]), fmt(tot_internes["total"])])
    return response


# -----------------------------
# Paiements d'une facture émise (espèces = caisse, autres modes = banque)
# -----------------------------
def _synchroniser_locations(facture):
    """Locations liées : même statut de paiement que la facture."""
    for location in facture.locations.all():
        location.payee = facture.est_payee
        if facture.statut_paiement == Facture.StatutPaiement.ACOMPTE:
            location.acompte = True
            location.montant_acompte = facture.montant_paye
            location.date_acompte = location.date_acompte or facture.date_paiement
        elif facture.statut_paiement == Facture.StatutPaiement.A_PAYER:
            location.acompte = False
            location.montant_acompte = None
            location.date_acompte = None
        # Payé : l'acompte éventuel est conservé (TVA déjà due à sa réception)
        location.save(update_fields=["payee", "acompte", "montant_acompte", "date_acompte", "updated_at"])


@login_required
@require_POST
def facture_paiement_view(request, pk):
    from .models import PaiementFacture
    from .paiements import depasse_plafond, plafond_especes

    if not (_peut(request.user, ROLES_FACTURATION) or _vendeur_locations(request.user)):
        return _refuser(request)

    facture = _get_facture(request, pk)

    if not _peut_facture(request.user, facture):

        return _refuser(request)
    if not facture.est_emise:
        messages.error(request, _("Le paiement ne peut être enregistré que sur une facture émise."))
        return redirect("facture:detail", pk=facture.pk)
    if facture.client_est_societe:
        messages.info(request, _("Facture interne : aucun paiement à enregistrer."))
        return redirect("facture:detail", pk=facture.pk)

    action = request.POST.get("action", "ajouter")
    non_ventile = facture.montant_non_ventile

    try:
        with transaction.atomic():
            if action == "supprimer":
                paiement = get_object_or_404(PaiementFacture, pk=request.POST.get("paiement_id"), facture=facture)
                paiement.delete()
                message = _("Paiement supprimé.")

            elif action == "annuler_non_ventile":
                non_ventile = Decimal("0")
                message = _("Paiement antérieur annulé.")

            else:
                mode = request.POST.get("mode")
                if mode not in PaiementFacture.Mode.values:
                    raise ValueError(_("Mode de paiement inconnu."))
                try:
                    montant = Decimal((request.POST.get("montant") or "0").replace(",", ".")).quantize(Decimal("0.01"))
                except Exception:
                    raise ValueError(_("Montant invalide."))
                if montant <= 0:
                    raise ValueError(_("Le montant doit être positif."))
                if montant > facture.reste_a_payer:
                    raise ValueError(_("Le montant dépasse le reste à payer (%(reste)s €).") % {"reste": facture.reste_a_payer})
                try:
                    jour = datetime.strptime(request.POST.get("date") or "", "%Y-%m-%d").date()
                except ValueError:
                    jour = timezone.localdate()

                if mode == PaiementFacture.Mode.ESPECES:
                    plafond = plafond_especes(facture.pays_vendeur(), jour, request.POST.get("non_resident") == "1")
                    total_especes = facture.total_especes + montant
                    # Plafond légal : total des espèces reçues pour cette facture (paiements fractionnés compris)
                    if depasse_plafond(total_especes, plafond):
                        raise ValueError(_(
                            "Paiement en espèces refusé : le total en espèces (%(total)s €) dépasse le plafond "
                            "autorisé en %(pays)s (%(plafond)s €). Utilisez un virement ou une carte."
                        ) % {"total": total_especes, "pays": facture.pays_vendeur(), "plafond": plafond["montant"]})

                PaiementFacture.objects.create(
                    facture=facture, date=jour, montant=montant, mode=mode,
                    reference=(request.POST.get("reference") or "")[:100], cree_par=request.user,
                )
                message = _("Paiement enregistré.")

            facture.recalculer_paiement(non_ventile)
            facture.save(update_fields=["statut_paiement", "montant_paye", "date_paiement", "updated_at"])
            _synchroniser_locations(facture)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect("facture:detail", pk=facture.pk)

    _log(request.user, ACTION_PAIEMENT_FACTURE, facture)
    messages.success(request, "%s %s" % (message, _("Statut : %(statut)s.") % {"statut": facture.get_statut_paiement_display()}))
    return redirect("facture:detail", pk=facture.pk)


# -----------------------------
# Comptabilité : caisse et banque (encaissements des factures)
# -----------------------------
@never_cache
@login_required
def caisse_banque_view(request):
    from .models import PaiementFacture
    from .paiements import COMPTE_BANQUE, COMPTE_CAISSE, COMPTES, ecritures_paiement

    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)

    aujourdhui = timezone.localdate()
    try:
        annee = int(request.GET.get("annee") or aujourdhui.year)
    except ValueError:
        annee = aujourdhui.year
    try:
        mois = int(request.GET.get("mois") or 0)
    except ValueError:
        mois = 0

    paiements = (
        PaiementFacture.objects.filter(facture__societe=request.user.societe, date__year=annee)
        .select_related("facture", "cree_par")
        .order_by("date", "created_at")
    )
    if 1 <= mois <= 12:
        paiements = paiements.filter(date__month=mois)
    paiements = list(paiements)

    zero = Decimal("0.00")
    caisse = [p for p in paiements if p.est_especes]
    banque = [p for p in paiements if not p.est_especes]
    par_mode = {}
    for p in paiements:
        par_mode.setdefault(p.mode, {"label": p.get_mode_display(), "nb": 0, "total": zero})
        par_mode[p.mode]["nb"] += 1
        par_mode[p.mode]["total"] += p.montant

    journal = [{"paiement": p, "journal": "CAI" if p.est_especes else "BQE", "lignes": ecritures_paiement(p)} for p in paiements]

    if request.GET.get("export") == "csv":
        import csv
        nom = f"caisse_banque_{annee}{'-%02d' % mois if mois else ''}.csv"
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="{nom}"'
        response.write("\ufeff")
        w = csv.writer(response, delimiter=";")
        w.writerow([_("Date"), _("Journal"), _("Pièce"), _("Compte"), _("Intitulé du compte"), _("Libellé"),
                    _("Mode de paiement"), _("Débit"), _("Crédit")])
        fmt = lambda x: f"{x:.2f}".replace(".", ",") if x else ""
        for e in journal:
            p = e["paiement"]
            for l in e["lignes"]:
                w.writerow([p.date.strftime("%d/%m/%Y"), e["journal"], p.facture.numero or "", l["compte"], l["intitule"],
                            l["libelle"], p.get_mode_display(), fmt(l["debit"]), fmt(l["credit"])])
        return response

    return render(request, "facture/caisse_banque.html", {
        "annee": annee,
        "mois": mois,
        "annees": range(aujourdhui.year - 5, aujourdhui.year + 1),
        "mois_choix": range(1, 13),
        "paiements": paiements,
        "total_caisse": sum((p.montant for p in caisse), zero),
        "total_banque": sum((p.montant for p in banque), zero),
        "total_encaisse": sum((p.montant for p in paiements), zero),
        "nb_caisse": len(caisse),
        "nb_banque": len(banque),
        "par_mode": list(par_mode.values()),
        "journal": journal,
        "compte_caisse": COMPTE_CAISSE,
        "compte_banque": COMPTE_BANQUE,
        "intitule_caisse": COMPTES[COMPTE_CAISSE],
        "intitule_banque": COMPTES[COMPTE_BANQUE],
    })


# -----------------------------
# Factures à payer : factures d'achat fournisseurs non payées (dettes 440000)
# -----------------------------
@never_cache
@login_required
def factures_a_payer_view(request):
    from achat_mds.models import AchatMds
    from maintenance.maintenance_externe.models import CarrosserieExterne, MaintenanceExterne
    from outillage.models import Outillage

    if not _peut(request.user, ROLES_FACTURATION):
        return _refuser(request)

    societe = request.user.societe
    # Factures fournisseurs : achats MDS et outillage (mêmes propriétés : FactureAchatMixin)
    sources = {
        "achat": AchatMds.objects.filter(societe=societe).select_related("fournisseur"),
        "outillage": Outillage.objects.filter(societe=societe).select_related("fournisseur"),
        # Factures des garages officiels (maintenances externes) : le garage tient lieu de fournisseur
        "externe": MaintenanceExterne.objects.filter(societe=societe).select_related(
            "garage", "voiture_exemplaire"),
        # Carrosserie externe : uniquement les factures reçues (pas les devis)
        "carrosserie": CarrosserieExterne.objects.filter(societe=societe, facture_date__isnull=False).select_related(
            "carrossier", "voiture_exemplaire"),
    }

    def montant(obj):
        """Montant à payer : la carrosserie déduit la part payée directement par l'assurance."""
        return getattr(obj, "montant_a_payer", None) if hasattr(obj, "montant_a_payer") else obj.total_tvac
    CHAMP_FOURNISSEUR = {"externe": "garage_id", "carrosserie": "carrossier_id"}

    def detail_url(obj):
        if isinstance(obj, CarrosserieExterne):
            return reverse("maintenance_externe:carrosserie_detail", args=[obj.pk])
        if isinstance(obj, MaintenanceExterne):
            return reverse("maintenance_externe:maintenance_externe_modifier", args=[obj.pk])
        if isinstance(obj, Outillage):
            return reverse("outillage:outillage_detail", args=[obj.pk])
        return reverse("achat_mds:achat_detail", args=[obj.pk])

    def nature(obj):
        if isinstance(obj, CarrosserieExterne):
            return _("Carrosserie externe")
        if isinstance(obj, MaintenanceExterne):
            return _("Maintenance externe")
        return _("Outillage") if isinstance(obj, Outillage) else _("Achat")

    def libelle(obj):
        return getattr(obj, "libelle_facture", None) or getattr(obj, "libelle", None) or ""

    # Marquer une facture d'achat comme payée (ou annuler le paiement)
    if request.method == "POST":
        qs = sources.get(request.POST.get("type"), sources["achat"])
        achat = get_object_or_404(qs, pk=request.POST.get("achat_id"))
        nom = achat.reference_facture or achat.fournisseur.nom
        champs_maj = ["date_paiement"] if isinstance(achat, (MaintenanceExterne, CarrosserieExterne)) else None
        if request.POST.get("action") == "annuler":
            achat.date_paiement = None
            message = _("Paiement annulé : %(achat)s") % {"achat": nom}
        else:
            try:
                achat.date_paiement = datetime.strptime(request.POST.get("date") or "", "%Y-%m-%d").date()
            except ValueError:
                achat.date_paiement = timezone.localdate()
            message = _("Facture d'achat payée : %(achat)s") % {"achat": nom}
        # Maintenance externe : ne pas relancer le calcul ni les compteurs du véhicule
        achat.save(update_fields=champs_maj) if champs_maj else achat.save()
        UserLog.objects.create(utilisateur=request.user, action=str(message))
        messages.success(request, message)
        return redirect(f"{reverse('facture:a_payer')}?{request.GET.urlencode()}")

    aujourdhui = timezone.localdate()
    fournisseur_id = request.GET.get("fournisseur") or ""
    type_filtre = request.GET.get("type") or ""

    a_payer = []
    for type_, qs in sources.items():
        if type_filtre and type_filtre != type_:
            continue
        q = qs.filter(date_paiement__isnull=True)
        if fournisseur_id:
            q = q.filter(**{CHAMP_FOURNISSEUR.get(type_, "fournisseur_id"): fournisseur_id})
        a_payer += [(type_, o) for o in q]
    a_payer.sort(key=lambda t: t[1].date_facture or aujourdhui)

    z = Decimal("0.00")
    tranches = [
        {"code": "0_30", "libelle": _("0 à 30 jours"), "total": z, "nb": 0, "bordure": "border-green-500", "badge": "bg-green-100 text-green-800"},
        {"code": "31_60", "libelle": _("31 à 60 jours"), "total": z, "nb": 0, "bordure": "border-yellow-500", "badge": "bg-yellow-100 text-yellow-800"},
        {"code": "61_90", "libelle": _("61 à 90 jours"), "total": z, "nb": 0, "bordure": "border-orange-500", "badge": "bg-orange-100 text-orange-800"},
        {"code": "90", "libelle": _("Plus de 90 jours"), "total": z, "nb": 0, "bordure": "border-red-500", "badge": "bg-red-100 text-red-800"},
    ]
    lignes = []
    par_fournisseur = {}
    for type_, achat in a_payer:
        age = (aujourdhui - achat.date_facture).days if achat.date_facture else 0
        idx = 0 if age <= 30 else 1 if age <= 60 else 2 if age <= 90 else 3
        tranches[idx]["total"] += montant(achat)
        tranches[idx]["nb"] += 1
        lignes.append({"achat": achat, "type": type_, "nature": nature(achat), "libelle": libelle(achat), "a_payer": montant(achat),
                       "url": detail_url(achat), "age": age, "badge": tranches[idx]["badge"]})
        f = par_fournisseur.setdefault(achat.fournisseur_id, {"fournisseur": achat.fournisseur, "nb": 0, "total": z})
        f["nb"] += 1
        f["total"] += montant(achat)

    payees_recentes = []
    for type_, qs in sources.items():
        for o in qs.filter(date_paiement__isnull=False, date_paiement__gte=aujourdhui - timedelta(days=30)):
            payees_recentes.append({"achat": o, "type": type_, "nature": nature(o), "url": detail_url(o)})
    payees_recentes.sort(key=lambda p: p["achat"].date_paiement, reverse=True)

    fournisseurs = {}
    for qs in sources.values():
        for o in qs.filter(date_paiement__isnull=True):
            fournisseurs[o.fournisseur_id] = o.fournisseur

    return render(request, "facture/factures_a_payer.html", {
        "lignes": lignes,
        "tranches": tranches,
        "total_a_payer": sum((l["a_payer"] for l in lignes), z),
        "total_tva": sum((l["achat"].montant_tva for l in lignes), z),
        "par_fournisseur": sorted(par_fournisseur.values(), key=lambda f: -f["total"]),
        "fournisseurs": sorted(fournisseurs.values(), key=lambda f: f.nom or ""),
        "fournisseur_id": fournisseur_id,
        "type_filtre": type_filtre,
        "payees_recentes": payees_recentes,
        "aujourdhui": aujourdhui,
    })

"""
Administration web du tenant des particuliers (/tenant/<schéma particuliers>/<langue>/particuliers/) :
statistiques, comptes (activer, désactiver, supprimer) et consultation des données.
Réservée à la direction de ce tenant (et au super admin).
"""
from datetime import timedelta
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Max, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .api.base import ROLE_PARTICULIER, servir_fichier
from .comptes import activer, supprimer_compte
from . import abonnements
from .models import (AbonnementParticulier, AppareilNotification, Depense, Document, Entretien, Formule,
                     JournalAbonnement, Plein, Rappel, Vehicule)


def schema_particuliers():
    return getattr(settings, "PARTICULIERS_SCHEMA", "particuliers")


def admin_particuliers(vue):
    @wraps(vue)
    def enveloppe(request, *args, **kwargs):
        user = request.user
        tenant = getattr(request, "tenant", None)
        autorise = (user.is_superuser or getattr(user, "role", None) == "direction") \
            and getattr(tenant, "schema_name", None) == schema_particuliers()
        if not autorise:
            messages.error(request, _("Accès refusé"))
            return redirect("utilisateurs:dashboard")
        return vue(request, *args, **kwargs)
    return login_required(never_cache(enveloppe))


def _comptes():
    from utilisateurs.models import Utilisateur
    return Utilisateur.objects.filter(role=ROLE_PARTICULIER)


@admin_particuliers
def tableau(request):
    comptes = _comptes()
    il_y_a_30_jours = timezone.now() - timedelta(days=30)
    q = (request.GET.get("q") or "").strip()
    etat = request.GET.get("etat") or ""
    liste = comptes.order_by("-created_at")
    if q:
        liste = liste.filter(Q(email__icontains=q) | Q(nom__icontains=q) | Q(prenom__icontains=q))
    if etat == "actifs":
        liste = liste.filter(is_active=True)
    elif etat == "desactives":
        liste = liste.filter(is_active=False)
    page = Paginator(liste, 50).get_page(request.GET.get("page"))

    # Nombre de véhicules et dernière activité par compte (données du schéma des particuliers)
    ids = [u.pk for u in page]
    par_compte = {r["proprietaire"]: r for r in Vehicule.objects.filter(proprietaire__in=ids)
                  .values("proprietaire").annotate(nb=Count("id"), maj=Max("updated_at"))}
    dernier_plein = dict(Plein.objects.filter(vehicule__proprietaire__in=ids)
                         .values_list("vehicule__proprietaire").annotate(m=Max("created_at")))
    abos = {a.utilisateur_id: a for a in AbonnementParticulier.objects.filter(utilisateur__in=ids)}
    for u in page:
        u.formule = abonnements.formule_effective(u, abos.get(u.pk) or False)
        u.formule_libelle = Formule(u.formule).label
        r = par_compte.get(u.pk, {})
        u.nb_vehicules = r.get("nb", 0)
        u.derniere_activite = max([d for d in (r.get("maj"), dernier_plein.get(u.pk), u.last_login) if d], default=None)

    stats = {
        "comptes": comptes.count(),
        "actifs": comptes.filter(is_active=True).count(),
        "nouveaux_30j": comptes.filter(created_at__gte=il_y_a_30_jours).count(),
        "vehicules": Vehicule.objects.count(),
        "pleins": Plein.objects.count(),
        "pleins_30j": Plein.objects.filter(created_at__gte=il_y_a_30_jours).count(),
        "entretiens": Entretien.objects.count(),
        "documents": Document.objects.count(),
        "rappels_actifs": Rappel.objects.filter(actif=True).count(),
        "formules": _repartition_formules(),
    }
    return render(request, "particulier/admin/tableau.html", {
        "stats": stats, "page": page, "q": q, "etat": etat,
    })


def _repartition_formules():
    """Comptes payants par formule (abonnements en cours)."""
    maintenant = timezone.now()
    en_cours = (AbonnementParticulier.objects.exclude(formule=Formule.GRATUIT)
                .filter(Q(date_fin__isnull=True) | Q(date_fin__gt=maintenant)))
    par = dict(en_cours.values_list("formule").annotate(n=Count("id")))
    return [(Formule(f).label, par.get(f, 0)) for f in (Formule.BRONZE, Formule.SILVER, Formule.GOLD)]


@admin_particuliers
def compte(request, pk):
    user = get_object_or_404(_comptes(), pk=pk)
    vehicules = (Vehicule.objects.filter(proprietaire=user)
                 .annotate(nb_pleins=Count("pleins", distinct=True), nb_entretiens=Count("entretiens", distinct=True),
                           nb_documents=Count("documents", distinct=True), nb_rappels=Count("rappels", distinct=True))
                 .order_by("archive", "marque"))
    documents = Document.objects.filter(vehicule__proprietaire=user).select_related("vehicule").order_by("-created_at")[:20]
    pleins = Plein.objects.filter(vehicule__proprietaire=user).select_related("vehicule").order_by("-date")[:20]
    return render(request, "particulier/admin/compte.html", {
        "compte": user, "vehicules": vehicules, "documents": documents, "pleins": pleins,
        "nb_depenses": Depense.objects.filter(vehicule__proprietaire=user).count(),
        "abonnement": abonnements.abonnement(user),
        "etat_abonnement": abonnements.etat(user),
        "formules": [(f.value, f.label, abonnements.LIMITES[f]) for f in abonnements.ORDRE],
        "mode_achats": abonnements.mode_achats(),
        "journal": JournalAbonnement.objects.filter(utilisateur=user)[:20],
        "appareils": AppareilNotification.objects.filter(utilisateur=user).count(),
    })


@admin_particuliers
@require_POST
def compte_formule(request, pk):
    """Attribution d'une formule par l'administration (offerte, support, tests)."""
    from datetime import datetime, time
    user = get_object_or_404(_comptes(), pk=pk)
    formule = request.POST.get("formule")
    if formule not in abonnements.LIMITES:
        messages.error(request, _("Formule inconnue."))
        return redirect("particulier_admin:compte", pk=pk)
    date_fin = None
    if request.POST.get("date_fin"):
        try:
            jour = datetime.strptime(request.POST["date_fin"], "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, _("Date de fin invalide."))
            return redirect("particulier_admin:compte", pk=pk)
        date_fin = timezone.make_aware(datetime.combine(jour, time(23, 59, 59)))
    abonnements.attribuer(user, formule, date_fin, note=(request.POST.get("note") or "").strip()[:255])
    messages.success(request, _("Formule %(f)s attribuée.") % {"f": Formule(formule).label})
    return redirect("particulier_admin:compte", pk=pk)


@admin_particuliers
@require_POST
def compte_activer(request, pk):
    user = get_object_or_404(_comptes(), pk=pk)
    actif = request.POST.get("actif") == "1"
    activer(user, actif)
    messages.success(request, _("Compte réactivé.") if actif else _("Compte désactivé : l'utilisateur est déconnecté de l'application."))
    return redirect("particulier_admin:compte", pk=pk)


@admin_particuliers
@require_POST
def compte_supprimer(request, pk):
    user = get_object_or_404(_comptes(), pk=pk)
    if request.POST.get("confirmation", "").strip().lower() != (user.email or "").lower():
        messages.error(request, _("Recopiez l'adresse email du compte pour confirmer la suppression."))
        return redirect("particulier_admin:compte", pk=pk)
    email = user.email
    supprimer_compte(user)
    messages.success(request, _("Le compte %(email)s et toutes ses données ont été supprimés.") % {"email": email})
    return redirect("particulier_admin:tableau")


FICHIERS = {
    ("plein", "ticket"): Plein,
    ("entretien", "facture"): Entretien,
    ("document", "fichier"): Document,
    ("vehicule", "photo"): Vehicule,
}


@admin_particuliers
def fichier(request, modele, pk, champ):
    """Fichier privé d'un particulier (jamais servi par /media/)."""
    classe = FICHIERS.get((modele, champ))
    if classe is None:
        raise Http404
    return servir_fichier(getattr(get_object_or_404(classe, pk=pk), champ))


# ==================================================================
# MONITORING DU SERVEUR (vue « particuliers » : serveur + trafic de l'application)
# ==================================================================
@admin_particuliers
def monitoring(request):
    from django_tenants.utils import get_public_schema_name, schema_context
    from monitoring import activite
    from monitoring.systeme import etat_serveur, taille_media
    from monitoring.views import _alertes, _migration_manquante, _tables_pretes
    from societe.models import Societe

    if not _tables_pretes():
        return _migration_manquante(request)
    schema = schema_particuliers()
    with schema_context(get_public_schema_name()):
        societe = Societe.objects.get(schema_name=schema)
    p = activite.periode(request.GET.get("periode"))
    maintenant = timezone.now()
    etat = etat_serveur()
    base = activite.stats_base()
    cx = activite.connexions()

    tous = activite.trafic_par_schema(p["debut"])
    total_global = activite.total_trafic(tous)
    total_1h = activite.total_trafic(activite.trafic_par_schema(maintenant - timedelta(hours=1)))
    vide = activite._finaliser(activite._vide())
    tr = tous.get(schema) or vide
    resume = {
        "1h": activite.trafic_par_schema(maintenant - timedelta(hours=1), schema).get(schema) or vide,
        "24h": activite.trafic_par_schema(maintenant - timedelta(hours=24), schema).get(schema) or vide,
        "7j": activite.trafic_par_schema(maintenant - timedelta(days=7), schema).get(schema) or vide,
    }
    serveur = activite.serie_serveur(p, schema=schema)
    return render(request, "particulier/admin/monitoring.html", {
        "societe": societe, "schema": schema,
        "periode": p, "periodes": activite.PERIODES,
        "etat": etat, "base": base, "media": taille_media(), "cx": cx,
        "alertes": _alertes(etat, base, total_1h),
        "total": total_global, "total_1h": total_1h,
        "trafic": tr, "resume": resume,
        "part_charge": round(100.0 * (tr["duree_ms_total"] or 0) / total_global["duree_ms_total"], 1)
        if total_global["duree_ms_total"] else 0,
        "part_requetes": round(100.0 * (tr["requetes"] or 0) / total_global["requetes"], 1)
        if total_global["requetes"] else 0,
        "db": base["schemas"].get(schema),
        "comptes_actifs_24h": _comptes().filter(last_login__gte=maintenant - timedelta(hours=24)).count(),
        "graphiques": {"serveur": serveur, "trafic": activite.serie_trafic(p, schema=schema)},
        "en_ligne_minutes": activite.EN_LIGNE_MINUTES,
    })


@admin_particuliers
def monitoring_api(request):
    from django.http import JsonResponse
    from monitoring.views import donnees_api
    return JsonResponse(donnees_api(request))


# ==================================================================
# ABONNEMENTS ET NOTIFICATIONS (monitoring) : réglages, actions, e-mails
# ==================================================================
def _fichier_ok(chemin):
    import os
    return bool(chemin) and os.path.isfile(chemin)


def _reglages(request):
    """Réglages lus dans settings / .env (aucun secret affiché)."""
    s = settings
    backend = getattr(s, "EMAIL_BACKEND", "")
    smtp = "smtp" in backend
    url = request.build_absolute_uri
    rtdn = getattr(s, "GOOGLE_RTDN_JETON", "")
    return [
        (_("Achats intégrés"), [
            (_("Mode"), abonnements.mode_achats(), abonnements.mode_achats() == "store" or settings.DEBUG,
             _("« store » en production : seules les preuves vérifiées par Apple / Google sont acceptées.")),
            (_("Achats Sandbox acceptés"), _("oui") if abonnements.sandbox_accepte() else _("non"), None, ""),
            (_("Produits"), ", ".join(f"{p} → {f}" for p, f in abonnements.produits().items()), None, ""),
        ]),
        (_("App Store (Apple)"), [
            (_("Bundle ID"), getattr(s, "APPLE_BUNDLE_ID", "") or "—", bool(getattr(s, "APPLE_BUNDLE_ID", "")), ""),
            (_("Certificat Apple Root CA G3"), getattr(s, "APPLE_ROOT_CA_G3", "") or _("non défini"),
             _fichier_ok(getattr(s, "APPLE_ROOT_CA_G3", "")), _("Nécessaire pour vérifier les achats et notifications.")),
            (_("URL des notifications (V2)"), url("/api/v1/abonnement/notifications/apple/"), None,
             _("À saisir dans App Store Connect → App → Informations sur l'app.")),
        ]),
        (_("Google Play"), [
            (_("Package"), getattr(s, "GOOGLE_PACKAGE_NAME", "") or "—", bool(getattr(s, "GOOGLE_PACKAGE_NAME", "")), ""),
            (_("Compte de service (JSON)"), getattr(s, "GOOGLE_SERVICE_ACCOUNT_FILE", "") or _("non défini"),
             _fichier_ok(getattr(s, "GOOGLE_SERVICE_ACCOUNT_FILE", "")), ""),
            (_("Jeton des notifications (RTDN)"), _("défini") if rtdn else _("non défini"), bool(rtdn), ""),
            (_("URL des notifications (Pub/Sub push)"),
             url("/api/v1/abonnement/notifications/google/") + "?jeton=…", None,
             _("Abonnement push du sujet Pub/Sub, avec le jeton GOOGLE_RTDN_JETON.")),
        ]),
        (_("E-mail"), [
            (_("Service"), "Brevo (API)" if "brevo" in backend else ("SMTP" if smtp else _("console (pas d'envoi)")),
             "console" not in backend, backend),
            (_("Serveur SMTP"), f"{s.EMAIL_HOST}:{s.EMAIL_PORT}" if smtp and s.EMAIL_HOST else "—",
             bool(s.EMAIL_HOST) if smtp else None, _("TLS") if getattr(s, "EMAIL_USE_TLS", False) else ""),
            (_("Identifiant"), getattr(s, "EMAIL_HOST_USER", "") or "—", None, ""),
            (_("Mot de passe / clé"), _("défini") if (s.EMAIL_HOST_PASSWORD or getattr(s, "BREVO_API_KEY", ""))
             else _("non défini"), bool(s.EMAIL_HOST_PASSWORD or getattr(s, "BREVO_API_KEY", "")), ""),
            (_("Expéditeur"), s.DEFAULT_FROM_EMAIL, bool(s.DEFAULT_FROM_EMAIL), ""),
        ]),
        (_("Notifications push (Firebase)"), [
            (_("Compte de service (JSON)"), getattr(s, "FIREBASE_SERVICE_ACCOUNT_FILE", "") or _("non défini"),
             _fichier_ok(getattr(s, "FIREBASE_SERVICE_ACCOUNT_FILE", "")), _("Vide : pas de notifications push.")),
            (_("Projet"), getattr(s, "FIREBASE_PROJECT_ID", "") or _("lu dans la clé JSON"), None, ""),
        ]),
    ]


@admin_particuliers
def abonnements_monitoring(request):
    from .models import (AppareilNotification, CategorieJournal, JournalAbonnement, NotificationAbonnement,
                         StatutPaiement)
    maintenant = timezone.now()
    payants = AbonnementParticulier.objects.exclude(formule=Formule.GRATUIT).select_related("utilisateur")
    actifs = [a for a in payants if abonnements.formule_effective(a.utilisateur, a, maintenant) != Formule.GRATUIT]
    grace = [a for a in payants if a.statut_paiement == StatutPaiement.GRACE]
    echec = [a for a in payants if a.statut_paiement == StatutPaiement.ECHEC]
    renouvellements = sorted((a for a in actifs if a.renouvellement_auto and a.date_fin
                              and a.date_fin <= maintenant + timedelta(days=30)), key=lambda a: a.date_fin)
    derniere_tache = JournalAbonnement.objects.filter(categorie="tache").first()

    journal = JournalAbonnement.objects.select_related("utilisateur")
    categorie = request.GET.get("categorie") or ""
    if categorie:
        journal = journal.filter(categorie=categorie)
    q = (request.GET.get("q") or "").strip()
    if q:
        journal = journal.filter(Q(destinataire__icontains=q) | Q(utilisateur__email__icontains=q)
                                 | Q(type__icontains=q) | Q(message__icontains=q))
    if request.GET.get("erreurs") == "1":
        journal = journal.filter(succes=False)
    page = Paginator(journal, 50).get_page(request.GET.get("page"))

    il_y_a_30j = maintenant - timedelta(days=30)
    emails = JournalAbonnement.objects.filter(categorie="email", date__gte=il_y_a_30j)
    return render(request, "particulier/admin/abonnements.html", {
        "stats": {
            "actifs": len(actifs), "grace": len(grace), "echec": len(echec),
            "renouvellements_7j": sum(1 for a in renouvellements if a.date_fin <= maintenant + timedelta(days=7)),
            "notifications_30j": NotificationAbonnement.objects.filter(envoyee_le__gte=il_y_a_30j).count(),
            "emails_30j": emails.filter(succes=True).count(),
            "emails_erreurs_30j": emails.filter(succes=False).count(),
            "appareils": dict(AppareilNotification.objects.values_list("plateforme").annotate(n=Count("id"))),
        },
        "a_surveiller": grace + echec,
        "renouvellements": renouvellements[:20],
        "derniere_tache": derniere_tache,
        "tache_en_retard": not derniere_tache or derniere_tache.date < maintenant - timedelta(hours=26),
        "reglages": _reglages(request),
        "page": page, "categories": CategorieJournal.choices, "categorie": categorie, "q": q,
        "erreurs": request.GET.get("erreurs") == "1",
    })


@admin_particuliers
@require_POST
def abonnements_email_test(request):
    """E-mail de test à l'adresse saisie (par défaut : celle de l'administrateur connecté)."""
    from django.core.mail import send_mail
    from .journal import noter
    destinataire = (request.POST.get("email") or request.user.email or "").strip()
    if not destinataire:
        messages.error(request, _("Aucune adresse e-mail."))
        return redirect("particulier_admin:abonnements")
    sujet = _("CarsCosts : e-mail de test")
    try:
        send_mail(sujet, _("Cet e-mail de test confirme que l'envoi fonctionne (%(backend)s).")
                  % {"backend": settings.EMAIL_BACKEND}, None, [destinataire])
    except Exception as e:
        noter("email", "test", None, sujet, False, destinataire=destinataire, erreur=str(e)[:500],
              par=request.user.email)
        messages.error(request, _("Échec de l'envoi : %s") % e)
    else:
        noter("email", "test", None, sujet, True, destinataire=destinataire, par=request.user.email)
        messages.success(request, _("E-mail de test envoyé à %s.") % destinataire)
    return redirect("particulier_admin:abonnements")


@admin_particuliers
@require_POST
def abonnements_lancer(request):
    """Lance tout de suite la tâche quotidienne des rappels (comme le cron)."""
    from .notifications import tache_quotidienne
    n = tache_quotidienne(origine=_("manuel (%s)") % request.user.email)
    messages.success(request, _("Rappels traités : %d notification(s) envoyée(s).") % n)
    return redirect("particulier_admin:abonnements")

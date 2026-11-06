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
from .models import Depense, Document, Entretien, Plein, Rappel, Vehicule


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
    for u in page:
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
    }
    return render(request, "particulier/admin/tableau.html", {
        "stats": stats, "page": page, "q": q, "etat": etat,
    })


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
    })


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

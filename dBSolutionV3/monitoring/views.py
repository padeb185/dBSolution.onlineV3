"""
Monitoring serveur (superadministrateurs) : état du serveur, utilisateurs connectés, trafic,
base de données — pour tous les tenants et par tenant.
"""
from datetime import timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django_tenants.utils import get_public_schema_name, schema_context

from societe.models import Societe

from . import activite
from .systeme import etat_serveur, taille_media

SEUILS = {"cpu": 85, "ram": 90, "swap": 50, "disque": 85, "connexions_db": 80, "erreurs": 2}


def _tables_pretes():
    """True si la migration du monitoring est appliquée (tables du schéma public)."""
    from django.db import connection
    from .models import MesureServeur, TraficTenant
    try:
        with schema_context(get_public_schema_name()):
            tables = set(connection.introspection.table_names())
        return {TraficTenant._meta.db_table, MesureServeur._meta.db_table} <= tables
    except Exception:
        return False


def _migration_manquante(request):
    return render(request, "monitoring/migration_manquante.html", status=503)


def is_admin(user):
    return user.is_authenticated and user.is_staff and user.is_superuser


def _tenants():
    with schema_context(get_public_schema_name()):
        return list(
            Societe.objects.exclude(schema_name=get_public_schema_name())
            .annotate(nb_utilisateurs=Count("utilisateurs", distinct=True),
                      nb_actifs=Count("utilisateurs", filter=Q(utilisateurs__is_active=True), distinct=True))
            .order_by("nom")
        )


def _alertes(etat, base, total):
    alertes = []
    m, d = etat["memoire"], etat["disque"]
    if etat["cpu"] is not None and etat["cpu"] >= SEUILS["cpu"]:
        alertes.append(_("CPU élevé : %(v)s %%") % {"v": etat["cpu"]})
    if m["pourcent"] is not None and m["pourcent"] >= SEUILS["ram"]:
        alertes.append(_("Mémoire presque pleine : %(v)s %%") % {"v": m["pourcent"]})
    if m["swap_pourcent"] and m["swap_pourcent"] >= SEUILS["swap"]:
        alertes.append(_("Swap utilisé à %(v)s %% (mémoire insuffisante)") % {"v": m["swap_pourcent"]})
    if d["pourcent"] is not None and d["pourcent"] >= SEUILS["disque"]:
        alertes.append(_("Disque presque plein : %(v)s %%") % {"v": d["pourcent"]})
    if base.get("connexions") and base.get("max_connexions"):
        taux = 100 * base["connexions"] / base["max_connexions"]
        if taux >= SEUILS["connexions_db"]:
            alertes.append(_("Connexions PostgreSQL : %(n)s / %(max)s") % {"n": base["connexions"],
                                                                         "max": base["max_connexions"]})
    if total.get("taux_erreur") and total["taux_erreur"] >= SEUILS["erreurs"]:
        alertes.append(_("Taux d'erreurs serveur (5xx) : %(v)s %%") % {"v": total["taux_erreur"]})
    return alertes


# ==================================================================
# TOUS LES TENANTS
# ==================================================================
@never_cache
@login_required
@user_passes_test(is_admin)
def tableau(request):
    if not _tables_pretes():
        return _migration_manquante(request)
    p = activite.periode(request.GET.get("periode"))
    public = get_public_schema_name()
    etat = etat_serveur()
    base = activite.stats_base()
    cx = activite.connexions()
    trafic = activite.trafic_par_schema(p["debut"])
    trafic_1h = activite.trafic_par_schema(timezone.now() - timedelta(hours=1))
    total = activite.total_trafic(trafic)
    total_1h = activite.total_trafic(trafic_1h)
    duree_totale = total["duree_ms_total"] or 0

    tenants = _tenants()
    noms = {t.schema_name: t.nom for t in tenants}
    noms[public] = _("Public (connexion, administration)")

    lignes = []
    for t in tenants + [None]:
        schema = t.schema_name if t else public
        tr = trafic.get(schema) or activite._finaliser(activite._vide())
        c = cx["par_tenant"].get(schema, {"en_ligne": 0, "connectes": 0})
        lignes.append({
            "societe": t, "schema": schema, "nom": noms[schema],
            "en_ligne": c["en_ligne"], "connectes": c["connectes"],
            "utilisateurs": t.nb_utilisateurs if t else None, "actifs": t.nb_actifs if t else None,
            "trafic": tr, "requetes_1h": (trafic_1h.get(schema) or {}).get("requetes", 0),
            "part_charge": round(100.0 * (tr["duree_ms_total"] or 0) / duree_totale, 1) if duree_totale else 0,
            "db": base["schemas"].get(schema),
        })
    lignes.sort(key=lambda l: (l["societe"] is None, -l["en_ligne"], -(l["trafic"]["requetes"] or 0), l["nom"]))

    serie_t = activite.serie_trafic(p, par_tenant=True)
    serie_t["par_tenant"] = {noms.get(s, s): v for s, v in serie_t["par_tenant"].items()}

    return render(request, "monitoring/tableau.html", {
        "periode": p, "periodes": activite.PERIODES,
        "etat": etat, "base": base, "media": taille_media(),
        "cx": cx, "noms": noms,
        "total": total, "total_1h": total_1h,
        "lignes": lignes,
        "alertes": _alertes(etat, base, total_1h),
        "graphiques": {"serveur": activite.serie_serveur(p), "trafic": serie_t},
        "en_ligne_minutes": activite.EN_LIGNE_MINUTES,
    })


# ==================================================================
# UN TENANT
# ==================================================================
@never_cache
@login_required
@user_passes_test(is_admin)
def tenant(request, pk):
    if not _tables_pretes():
        return _migration_manquante(request)
    with schema_context(get_public_schema_name()):
        societe = get_object_or_404(Societe.objects.select_related("adresse"), pk=pk)
        from utilisateurs.models import Utilisateur
        utilisateurs = list(Utilisateur.objects.filter(societe=societe).order_by("-is_active", "nom", "prenom"))
    schema = societe.schema_name
    p = activite.periode(request.GET.get("periode"))
    maintenant = timezone.now()

    cx = activite.connexions()
    connectes = {str(l["utilisateur"].pk): l for l in cx["utilisateurs"] if l["schema"] == schema}
    lignes_utilisateurs = [{"utilisateur": u, "connexion": connectes.get(str(u.pk))} for u in utilisateurs]
    lignes_utilisateurs.sort(key=lambda l: (l["connexion"] is None,
                                            -(l["connexion"]["derniere_activite"].timestamp() if l["connexion"] else 0)))

    tous = activite.trafic_par_schema(p["debut"])
    total_global = activite.total_trafic(tous)
    vide = activite._finaliser(activite._vide())
    tr = tous.get(schema) or vide
    resume = {
        "1h": activite.trafic_par_schema(maintenant - timedelta(hours=1), schema).get(schema) or vide,
        "24h": activite.trafic_par_schema(maintenant - timedelta(hours=24), schema).get(schema) or vide,
        "7j": activite.trafic_par_schema(maintenant - timedelta(days=7), schema).get(schema) or vide,
    }
    base = activite.stats_base()

    return render(request, "monitoring/tenant.html", {
        "societe": societe, "schema": schema,
        "periode": p, "periodes": activite.PERIODES,
        "en_ligne": sum(1 for l in connectes.values() if l["en_ligne"]),
        "connectes": len(connectes),
        "nb_actifs": sum(1 for u in utilisateurs if u.is_active),
        "lignes_utilisateurs": lignes_utilisateurs,
        "trafic": tr, "resume": resume,
        "part_charge": round(100.0 * (tr["duree_ms_total"] or 0) / total_global["duree_ms_total"], 1)
        if total_global["duree_ms_total"] else 0,
        "part_requetes": round(100.0 * (tr["requetes"] or 0) / total_global["requetes"], 1)
        if total_global["requetes"] else 0,
        "db": base["schemas"].get(schema), "base": base,
        "graphiques": {"trafic": activite.serie_trafic(p, schema=schema),
                       "serveur": activite.serie_serveur(p, schema=schema)},
        "en_ligne_minutes": activite.EN_LIGNE_MINUTES,
    })


# ==================================================================
# API (rafraîchissement automatique des cartes)
# ==================================================================
@never_cache
@login_required
@user_passes_test(is_admin)
def api(request):
    return JsonResponse(donnees_api(request))


def donnees_api(request):
    """Mesures instantanées (cartes rafraîchies toutes les 15 s) – aussi utilisées par l'admin des particuliers."""
    etat = etat_serveur(intervalle_cpu=0.2)
    cx = activite.connexions()
    schema = request.GET.get("tenant")
    data = {
        "horodatage": timezone.localtime().strftime("%H:%M:%S"),
        "cpu": etat["cpu"], "charge": etat["charge"],
        "ram": etat["memoire"]["pourcent"], "ram_utilisee": etat["memoire"]["utilisee"],
        "swap": etat["memoire"]["swap_pourcent"], "disque": etat["disque"]["pourcent"],
        "app_memoire": etat["app_memoire"],
        "en_ligne": cx["en_ligne"], "connectes": cx["connectes"],
        "par_tenant": cx["par_tenant"],
    }
    if schema:
        data["tenant"] = {
            "en_ligne": cx["par_tenant"].get(schema, {}).get("en_ligne", 0),
            "connectes": cx["par_tenant"].get(schema, {}).get("connectes", 0),
            "utilisateurs": [
                {"id": str(l["utilisateur"].pk), "en_ligne": l["en_ligne"],
                 "derniere_activite": timezone.localtime(l["derniere_activite"]).strftime("%d/%m %H:%M")}
                for l in cx["utilisateurs"] if l["schema"] == schema
            ],
        }
    return data

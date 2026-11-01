"""
Activité : utilisateurs connectés (sessions), base de données (taille par schéma, connexions)
et trafic HTTP agrégé (tous tenants / par tenant).

Utilisateurs connectés : sessions Django non expirées et authentifiées. Avec SESSION_SAVE_EVERY_REQUEST,
expire_date = dernière requête + SESSION_COOKIE_AGE, d'où la dernière activité de chaque session.
« En ligne » = activité depuis moins de EN_LIGNE_MINUTES.
"""
from collections import OrderedDict, defaultdict
from datetime import timedelta

from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import connection
from django.db.models import Max, Sum
from django.db.models.functions import TruncDay, TruncHour
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_tenants.utils import get_public_schema_name, schema_context

from .models import MesureServeur, TraficTenant

EN_LIGNE_MINUTES = 5

PERIODES = OrderedDict([
    ("1h", {"duree": timedelta(hours=1), "pas": "5min", "libelle": _("1 heure")}),
    ("24h", {"duree": timedelta(hours=24), "pas": "heure", "libelle": _("24 heures")}),
    ("7j", {"duree": timedelta(days=7), "pas": "heure", "libelle": _("7 jours")}),
    ("30j", {"duree": timedelta(days=30), "pas": "jour", "libelle": _("30 jours")}),
])


def periode(code):
    code = code if code in PERIODES else "24h"
    p = dict(PERIODES[code], code=code)
    p["debut"] = timezone.now() - p["duree"]
    return p


# ------------------------------------------------------------------
# Utilisateurs connectés
# ------------------------------------------------------------------
def connexions():
    """
    {
      "utilisateurs": [{utilisateur, schema, derniere_activite, sessions, en_ligne}] (activité décroissante),
      "en_ligne": int, "connectes": int,
      "par_tenant": {schema: {"en_ligne": int, "connectes": int}},
    }
    """
    from utilisateurs.models import Utilisateur

    maintenant = timezone.now()
    age = timedelta(seconds=getattr(settings, "SESSION_COOKIE_AGE", 1209600))
    seuil = maintenant - timedelta(minutes=EN_LIGNE_MINUTES)

    par_uid = {}
    with schema_context(get_public_schema_name()):
        for s in Session.objects.filter(expire_date__gt=maintenant).only("session_data", "expire_date").iterator():
            try:
                data = s.get_decoded()
            except Exception:
                continue
            uid = data.get("_auth_user_id")
            if not uid:
                continue
            derniere = s.expire_date - age
            e = par_uid.setdefault(str(uid), {"derniere_activite": derniere, "sessions": 0,
                                              "schema_session": data.get("tenant_schema")})
            e["sessions"] += 1
            if derniere > e["derniere_activite"]:
                e["derniere_activite"] = derniere
                e["schema_session"] = data.get("tenant_schema") or e["schema_session"]

        utilisateurs = {str(u.pk): u for u in
                        Utilisateur.objects.filter(pk__in=list(par_uid)).select_related("societe")}

    lignes = []
    par_tenant = defaultdict(lambda: {"en_ligne": 0, "connectes": 0})
    for uid, e in par_uid.items():
        u = utilisateurs.get(uid)
        if u is None:
            continue
        schema = getattr(u.societe, "schema_name", None) or e["schema_session"] or get_public_schema_name()
        en_ligne = e["derniere_activite"] >= seuil
        lignes.append({"utilisateur": u, "schema": schema, "derniere_activite": e["derniere_activite"],
                       "sessions": e["sessions"], "en_ligne": en_ligne})
        par_tenant[schema]["connectes"] += 1
        if en_ligne:
            par_tenant[schema]["en_ligne"] += 1
    lignes.sort(key=lambda l: l["derniere_activite"], reverse=True)
    return {
        "utilisateurs": lignes,
        "en_ligne": sum(1 for l in lignes if l["en_ligne"]),
        "connectes": len(lignes),
        "par_tenant": dict(par_tenant),
    }


# ------------------------------------------------------------------
# Base de données
# ------------------------------------------------------------------
def stats_base():
    """Taille de la base, connexions et taille par schéma (PostgreSQL)."""
    res = {"taille": None, "connexions": None, "actives": None, "max_connexions": None,
           "cache_hit": None, "schemas": {}, "version": None}
    try:
        with connection.cursor() as c:
            c.execute("SELECT pg_database_size(current_database()), version()")
            res["taille"], version = c.fetchone()
            res["version"] = " ".join(version.split()[:2])
            c.execute("SELECT count(*), count(*) FILTER (WHERE state = 'active') "
                      "FROM pg_stat_activity WHERE datname = current_database()")
            res["connexions"], res["actives"] = c.fetchone()
            c.execute("SELECT setting::int FROM pg_settings WHERE name = 'max_connections'")
            res["max_connexions"] = c.fetchone()[0]
            c.execute("SELECT round(sum(blks_hit) * 100.0 / NULLIF(sum(blks_hit) + sum(blks_read), 0), 2) "
                      "FROM pg_stat_database WHERE datname = current_database()")
            hit = c.fetchone()[0]
            res["cache_hit"] = float(hit) if hit is not None else None
            c.execute(
                "SELECT n.nspname, COALESCE(SUM(pg_total_relation_size(c.oid)), 0), "
                "       COALESCE(SUM(CASE WHEN c.relkind = 'r' THEN GREATEST(c.reltuples, 0) END), 0), "
                "       COUNT(*) FILTER (WHERE c.relkind = 'r') "
                "FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace "
                "WHERE c.relkind IN ('r', 'm', 'p') "
                "  AND n.nspname NOT IN ('pg_catalog', 'information_schema') AND n.nspname NOT LIKE 'pg_toast%%' "
                "GROUP BY n.nspname"
            )
            for schema, taille, lignes, tables in c.fetchall():
                res["schemas"][schema] = {"taille": int(taille), "lignes": int(lignes), "tables": tables}
    except Exception as e:  # base non PostgreSQL ou droits insuffisants
        res["erreur"] = str(e)
    return res


# ------------------------------------------------------------------
# Trafic HTTP
# ------------------------------------------------------------------
def _vide():
    return {"requetes": 0, "erreurs_4xx": 0, "erreurs_5xx": 0, "duree_ms_total": 0, "duree_ms_max": 0}


def _finaliser(t):
    t["duree_moyenne"] = round(t["duree_ms_total"] / t["requetes"]) if t["requetes"] else None
    t["taux_erreur"] = round(100.0 * t["erreurs_5xx"] / t["requetes"], 2) if t["requetes"] else None
    return t


def trafic_par_schema(debut, schema=None):
    """{schema: {requetes, erreurs_4xx, erreurs_5xx, duree_ms_total, duree_ms_max, duree_moyenne, taux_erreur}}"""
    qs = TraficTenant.objects.filter(tranche__gte=debut)
    if schema:
        qs = qs.filter(schema_name=schema)
    with schema_context(get_public_schema_name()):
        lignes = list(qs.values("schema_name").annotate(
            requetes=Sum("requetes"), erreurs_4xx=Sum("erreurs_4xx"), erreurs_5xx=Sum("erreurs_5xx"),
            duree_ms_total=Sum("duree_ms_total"), duree_ms_max=Max("duree_ms_max"),
        ))
    return {l.pop("schema_name"): _finaliser(l) for l in lignes}


def total_trafic(par_schema):
    t = _vide()
    for v in par_schema.values():
        for k in ("requetes", "erreurs_4xx", "erreurs_5xx", "duree_ms_total"):
            t[k] += v[k] or 0
        t["duree_ms_max"] = max(t["duree_ms_max"], v["duree_ms_max"] or 0)
    return _finaliser(t)


def _cle_tranche(dt, pas):
    dt = timezone.localtime(dt)
    if pas == "jour":
        return dt.strftime("%d/%m")
    if pas == "heure":
        return dt.strftime("%d/%m %Hh")
    return dt.strftime("%H:%M")


def _tranches(p):
    """Liste ordonnée des libellés de tranches de la période (axe des graphiques)."""
    maintenant = timezone.localtime()
    debut = timezone.localtime(p["debut"])
    if p["pas"] == "jour":
        pas = timedelta(days=1)
        t = debut.replace(hour=0, minute=0, second=0, microsecond=0)
    elif p["pas"] == "heure":
        pas = timedelta(hours=1)
        t = debut.replace(minute=0, second=0, microsecond=0)
    else:
        pas = timedelta(minutes=5)
        t = debut.replace(minute=debut.minute - debut.minute % 5, second=0, microsecond=0)
    res = []
    while t <= maintenant:
        res.append(_cle_tranche(t, p["pas"]))
        t += pas
    return res


def serie_trafic(p, schema=None, par_tenant=False):
    """
    {"labels": [...], "requetes": [...], "duree_moyenne": [...], "erreurs": [...],
     "par_tenant": {schema: [...]}}  (par_tenant seulement si demandé)
    """
    qs = TraficTenant.objects.filter(tranche__gte=p["debut"])
    if schema:
        qs = qs.filter(schema_name=schema)
    tz = timezone.get_current_timezone()
    if p["pas"] == "jour":
        qs = qs.annotate(t=TruncDay("tranche", tzinfo=tz))
    elif p["pas"] == "heure":
        qs = qs.annotate(t=TruncHour("tranche", tzinfo=tz))
    else:
        from django.db.models import F
        qs = qs.annotate(t=F("tranche"))
    champs = ["t", "schema_name"] if par_tenant else ["t"]
    with schema_context(get_public_schema_name()):
        lignes = list(qs.values(*champs).annotate(
            r=Sum("requetes"), d=Sum("duree_ms_total"), e=Sum("erreurs_5xx")).order_by("t"))

    labels = _tranches(p)
    index = {l: i for i, l in enumerate(labels)}
    n = len(labels)
    req, duree, err = [0] * n, [0] * n, [0] * n
    tenants = defaultdict(lambda: [0] * n)
    for l in lignes:
        i = index.get(_cle_tranche(l["t"], p["pas"]))
        if i is None:
            continue
        req[i] += l["r"] or 0
        duree[i] += l["d"] or 0
        err[i] += l["e"] or 0
        if par_tenant:
            tenants[l["schema_name"]][i] += l["r"] or 0
    res = {
        "labels": labels,
        "requetes": req,
        "duree_moyenne": [round(duree[i] / req[i]) if req[i] else None for i in range(n)],
        "erreurs": err,
    }
    if par_tenant:
        res["par_tenant"] = dict(tenants)
    return res


def serie_serveur(p, schema=None, max_points=300):
    """Historique des mesures serveur (CPU, RAM, disque, en ligne), sous-échantillonné."""
    with schema_context(get_public_schema_name()):
        mesures = list(MesureServeur.objects.filter(horodatage__gte=p["debut"]).order_by("horodatage")
                       .values("horodatage", "cpu", "ram_pourcent", "disque_pourcent", "charge_1",
                               "app_memoire", "en_ligne", "sessions", "en_ligne_par_tenant"))
    if len(mesures) > max_points:
        pas = -(-len(mesures) // max_points)
        mesures = mesures[::pas]
    fmt = "%d/%m %H:%M" if p["duree"] > timedelta(hours=24) else "%H:%M"
    res = {
        "labels": [timezone.localtime(m["horodatage"]).strftime(fmt) for m in mesures],
        "cpu": [m["cpu"] for m in mesures],
        "ram": [m["ram_pourcent"] for m in mesures],
        "disque": [m["disque_pourcent"] for m in mesures],
        "charge": [m["charge_1"] for m in mesures],
        "app_memoire_mo": [round(m["app_memoire"] / 1048576) if m["app_memoire"] else None for m in mesures],
        "en_ligne": [m["en_ligne"] for m in mesures],
        "sessions": [m["sessions"] for m in mesures],
    }
    if schema:
        res["en_ligne_tenant"] = [(m["en_ligne_par_tenant"] or {}).get(schema, 0) for m in mesures]
    return res

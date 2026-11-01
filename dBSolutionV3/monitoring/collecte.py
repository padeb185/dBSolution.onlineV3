"""
Collecte : compteurs de requêtes en mémoire (par processus), vidés en base toutes les 30 s
(une écriture groupée au lieu d'une par requête), et mesure du serveur toutes les 5 minutes
(en arrière-plan, sans ralentir la requête). Purge des données de plus de 31 jours.
"""
import atexit
import logging
import threading
import time
from datetime import timedelta

from django.db import connection, transaction
from django.utils import timezone
from django_tenants.utils import get_public_schema_name, schema_context

logger = logging.getLogger(__name__)

INTERVALLE_VIDAGE = 30          # secondes
INTERVALLE_MESURE = 300         # secondes
RETENTION = timedelta(days=31)

_tampon = {}                    # (schema, tranche) -> [requetes, 4xx, 5xx, duree_total, duree_max]
_verrou = threading.Lock()
_dernier_vidage = time.monotonic()
_mesure_en_cours = threading.Event()


def tranche_de(dt):
    return dt.replace(minute=dt.minute - dt.minute % 5, second=0, microsecond=0)


def enregistrer(schema, statut, duree_ms):
    global _dernier_vidage
    cle = (schema or get_public_schema_name(), tranche_de(timezone.now()))
    with _verrou:
        e = _tampon.setdefault(cle, [0, 0, 0, 0, 0])
        e[0] += 1
        if 400 <= statut < 500:
            e[1] += 1
        elif statut >= 500:
            e[2] += 1
        e[3] += duree_ms
        e[4] = max(e[4], duree_ms)
        a_vider = time.monotonic() - _dernier_vidage >= INTERVALLE_VIDAGE
    if a_vider:
        vider()


def vider():
    """Écrit le tampon en base (INSERT … ON CONFLICT : les compteurs s'additionnent)."""
    global _dernier_vidage
    from .models import TraficTenant

    with _verrou:
        donnees = list(_tampon.items())
        _tampon.clear()
        _dernier_vidage = time.monotonic()
    if donnees:
        table = f'"{get_public_schema_name()}"."{TraficTenant._meta.db_table}"'
        sql = (
            f"INSERT INTO {table} AS t (schema_name, tranche, requetes, erreurs_4xx, erreurs_5xx, "
            f"duree_ms_total, duree_ms_max) VALUES (%s, %s, %s, %s, %s, %s, %s) "
            f"ON CONFLICT (schema_name, tranche) DO UPDATE SET "
            f"requetes = t.requetes + EXCLUDED.requetes, "
            f"erreurs_4xx = t.erreurs_4xx + EXCLUDED.erreurs_4xx, "
            f"erreurs_5xx = t.erreurs_5xx + EXCLUDED.erreurs_5xx, "
            f"duree_ms_total = t.duree_ms_total + EXCLUDED.duree_ms_total, "
            f"duree_ms_max = GREATEST(t.duree_ms_max, EXCLUDED.duree_ms_max)"
        )
        try:
            with transaction.atomic(), connection.cursor() as c:
                c.executemany(sql, [(s, t, *v) for (s, t), v in donnees])
        except Exception as e:
            if "does not exist" in str(e):
                logger.warning("Monitoring : tables absentes – lancez « migrate_schemas --shared ».")
                return
            logger.exception("Monitoring : écriture du trafic impossible")
    mesurer_si_necessaire()


def mesurer_si_necessaire():
    """Lance une mesure du serveur en arrière-plan si la dernière date de plus de 5 minutes."""
    from .models import MesureServeur

    if _mesure_en_cours.is_set():
        return
    try:
        with schema_context(get_public_schema_name()):
            derniere = MesureServeur.objects.order_by("-horodatage").values_list("horodatage", flat=True).first()
    except Exception:
        return
    if derniere and timezone.now() - derniere < timedelta(seconds=INTERVALLE_MESURE - 10):
        return
    _mesure_en_cours.set()
    threading.Thread(target=_mesure_thread, name="monitoring-mesure", daemon=True).start()


def _mesure_thread():
    try:
        prendre_mesure()
    except Exception:
        logger.exception("Monitoring : mesure du serveur impossible")
    finally:
        _mesure_en_cours.clear()
        connection.close()  # connexion propre à ce thread


def prendre_mesure():
    """Enregistre l'état du serveur et des connexions, puis purge les anciennes données."""
    from .activite import connexions, stats_base
    from .models import MesureServeur, TraficTenant
    from .systeme import etat_serveur

    etat = etat_serveur(intervalle_cpu=1.0)
    with schema_context(get_public_schema_name()):
        cx = connexions()
        base = stats_base()
        mesure = MesureServeur.objects.create(
            cpu=etat["cpu"],
            charge_1=etat["charge"]["1"],
            ram_pourcent=etat["memoire"]["pourcent"],
            ram_utilisee=etat["memoire"]["utilisee"],
            swap_pourcent=etat["memoire"]["swap_pourcent"],
            disque_pourcent=etat["disque"]["pourcent"],
            app_memoire=etat["app_memoire"],
            db_connexions=base.get("connexions"),
            en_ligne=cx["en_ligne"],
            sessions=cx["connectes"],
            en_ligne_par_tenant={s: v["en_ligne"] for s, v in cx["par_tenant"].items()},
        )
        limite = timezone.now() - RETENTION
        MesureServeur.objects.filter(horodatage__lt=limite).delete()
        TraficTenant.objects.filter(tranche__lt=limite).delete()
    return mesure


@atexit.register
def _vider_a_l_arret():  # pragma: no cover
    try:
        if _tampon:
            vider()
    except Exception:
        pass

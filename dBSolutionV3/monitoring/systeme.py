"""
Mesures système du serveur : CPU, charge, mémoire, swap, disque, uptime, processus.
Utilise psutil s'il est installé ; sinon lit /proc (Linux). Sur un poste sans /proc ni psutil
(ex. Mac de développement sans psutil), les valeurs indisponibles valent None.
"""
import os
import platform
import shutil
import socket
import sys
import threading
import time
from pathlib import Path

from django.conf import settings

try:  # facultatif : pip install psutil
    import psutil
except Exception:  # pragma: no cover
    psutil = None

PROC = Path("/proc")

# Familles de processus surveillées : libellé → mots-clés (nom ou ligne de commande)
FAMILLES_PROCESSUS = [
    ("app", "Application Django (gunicorn / daphne / uvicorn)", ("gunicorn", "daphne", "uvicorn", "runserver")),
    ("celery", "Celery", ("celery",)),
    ("postgres", "PostgreSQL", ("postgres",)),
    ("nginx", "Nginx", ("nginx",)),
    ("redis", "Redis", ("redis-server",)),
]


def _arrondi(x, n=1):
    return None if x is None else round(float(x), n)


# ------------------------------------------------------------------
# CPU
# ------------------------------------------------------------------
def _stat_cpu():
    with open(PROC / "stat") as f:
        valeurs = [int(v) for v in f.readline().split()[1:]]
    inactif = valeurs[3] + (valeurs[4] if len(valeurs) > 4 else 0)
    return sum(valeurs), inactif


def cpu_pourcent(intervalle=0.25):
    if psutil:
        return _arrondi(psutil.cpu_percent(interval=intervalle))
    try:
        t1, i1 = _stat_cpu()
        time.sleep(intervalle)
        t2, i2 = _stat_cpu()
        total = t2 - t1
        return _arrondi(100.0 * (total - (i2 - i1)) / total) if total else None
    except Exception:
        return None


def charge():
    try:
        c1, c5, c15 = os.getloadavg()
        return {"1": _arrondi(c1, 2), "5": _arrondi(c5, 2), "15": _arrondi(c15, 2)}
    except Exception:
        return {"1": None, "5": None, "15": None}


# ------------------------------------------------------------------
# Mémoire
# ------------------------------------------------------------------
def _meminfo():
    infos = {}
    with open(PROC / "meminfo") as f:
        for ligne in f:
            cle, _, reste = ligne.partition(":")
            infos[cle.strip()] = int(reste.split()[0]) * 1024
    return infos


def memoire():
    vide = {"total": None, "utilisee": None, "disponible": None, "pourcent": None,
            "swap_total": None, "swap_utilisee": None, "swap_pourcent": None}
    try:
        if psutil:
            vm, sw = psutil.virtual_memory(), psutil.swap_memory()
            return {"total": vm.total, "utilisee": vm.total - vm.available, "disponible": vm.available,
                    "pourcent": _arrondi(vm.percent), "swap_total": sw.total, "swap_utilisee": sw.used,
                    "swap_pourcent": _arrondi(sw.percent)}
        m = _meminfo()
        total, dispo = m.get("MemTotal"), m.get("MemAvailable", m.get("MemFree"))
        st, sf = m.get("SwapTotal", 0), m.get("SwapFree", 0)
        return {"total": total, "utilisee": total - dispo, "disponible": dispo,
                "pourcent": _arrondi(100.0 * (total - dispo) / total) if total else None,
                "swap_total": st, "swap_utilisee": st - sf,
                "swap_pourcent": _arrondi(100.0 * (st - sf) / st) if st else 0.0}
    except Exception:
        return vide


# ------------------------------------------------------------------
# Disque
# ------------------------------------------------------------------
_cache_media = {"t": 0, "taille": None, "fichiers": None}
_verrou_media = threading.Lock()


def disque():
    try:
        u = shutil.disk_usage(settings.BASE_DIR)
        return {"total": u.total, "utilise": u.used, "libre": u.free,
                "pourcent": _arrondi(100.0 * u.used / u.total) if u.total else None}
    except Exception:
        return {"total": None, "utilise": None, "libre": None, "pourcent": None}


def taille_dossier(chemin):
    total, nb = 0, 0
    for racine, _dirs, fichiers in os.walk(chemin):
        for nom in fichiers:
            try:
                total += os.path.getsize(os.path.join(racine, nom))
                nb += 1
            except OSError:
                pass
    return total, nb


def taille_media(duree_cache=600):
    """Taille du dossier media (mise en cache 10 minutes : le parcours peut être long)."""
    with _verrou_media:
        if time.time() - _cache_media["t"] > duree_cache:
            racine = getattr(settings, "MEDIA_ROOT", None)
            if racine and os.path.isdir(racine):
                _cache_media["taille"], _cache_media["fichiers"] = taille_dossier(racine)
            _cache_media["t"] = time.time()
        return {"taille": _cache_media["taille"], "fichiers": _cache_media["fichiers"]}


# ------------------------------------------------------------------
# Système
# ------------------------------------------------------------------
def uptime_secondes():
    try:
        if psutil:
            return int(time.time() - psutil.boot_time())
        with open(PROC / "uptime") as f:
            return int(float(f.read().split()[0]))
    except Exception:
        return None


def infos_systeme():
    return {
        "hote": socket.gethostname(),
        "os": f"{platform.system()} {platform.release()}",
        "python": sys.version.split()[0],
        "cpu_coeurs": os.cpu_count(),
        "uptime": uptime_secondes(),
        "pid": os.getpid(),
        "psutil": bool(psutil),
    }


# ------------------------------------------------------------------
# Processus
# ------------------------------------------------------------------
def _famille(nom, cmdline):
    texte = f"{nom} {cmdline}".lower()
    for code, libelle, mots in FAMILLES_PROCESSUS:
        if any(m in texte for m in mots):
            return code, libelle
    return None, None


def _liste_processus():
    """[(pid, nom, cmdline, rss)]"""
    res = []
    if psutil:
        for p in psutil.process_iter(["pid", "name", "cmdline", "memory_info"]):
            try:
                mi = p.info.get("memory_info")
                res.append((p.info["pid"], p.info.get("name") or "", " ".join(p.info.get("cmdline") or []),
                            mi.rss if mi else 0))
            except Exception:
                continue
        return res
    if not PROC.is_dir():
        return res
    for d in PROC.iterdir():
        if not d.name.isdigit():
            continue
        try:
            cmdline = (d / "cmdline").read_bytes().replace(b"\0", b" ").decode(errors="ignore").strip()
            nom, rss = "", 0
            for ligne in (d / "status").read_text().splitlines():
                if ligne.startswith("Name:"):
                    nom = ligne.split(":", 1)[1].strip()
                elif ligne.startswith("VmRSS:"):
                    rss = int(ligne.split()[1]) * 1024
            res.append((int(d.name), nom, cmdline, rss))
        except Exception:
            continue
    return res


def processus():
    """Mémoire (RSS) par famille de processus : [{code, libelle, nombre, memoire}]."""
    familles = {code: {"code": code, "libelle": lib, "nombre": 0, "memoire": 0}
                for code, lib, _m in FAMILLES_PROCESSUS}
    for _pid, nom, cmdline, rss in _liste_processus():
        code, _lib = _famille(nom, cmdline)
        if code:
            familles[code]["nombre"] += 1
            familles[code]["memoire"] += rss or 0
    return [f for f in familles.values() if f["nombre"]]


def memoire_processus_courant():
    try:
        if psutil:
            return psutil.Process().memory_info().rss
        for ligne in (PROC / "self" / "status").read_text().splitlines():
            if ligne.startswith("VmRSS:"):
                return int(ligne.split()[1]) * 1024
    except Exception:
        pass
    try:
        import resource
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return rss if sys.platform == "darwin" else rss * 1024
    except Exception:
        return None


def etat_serveur(intervalle_cpu=0.25):
    procs = processus()
    app = next((p for p in procs if p["code"] == "app"), None)
    return {
        "cpu": cpu_pourcent(intervalle_cpu),
        "charge": charge(),
        "memoire": memoire(),
        "disque": disque(),
        "systeme": infos_systeme(),
        "processus": procs,
        "app_memoire": app["memoire"] if app else memoire_processus_courant(),
        "worker_memoire": memoire_processus_courant(),
    }

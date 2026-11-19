"""
Référentiel véhicules d'un tenant (moteurs, boîtes de vitesses, marques, modèles) :
chargé en arrière-plan par « manage.py peupler_referentiel » (plusieurs minutes, la page ne bloque pas).
Journal : <BASE_DIR>/logs/referentiel_<schéma>.log ; PID du processus : referentiel_<schéma>.pid
"""
import os
import subprocess
import sys
from pathlib import Path

from django.conf import settings
from django_tenants.utils import schema_context


def _dossier():
    d = Path(settings.BASE_DIR) / "logs"
    d.mkdir(exist_ok=True)
    return d


def _fichiers(schema):
    d = _dossier()
    return d / f"referentiel_{schema}.log", d / f"referentiel_{schema}.pid"


def en_cours(schema):
    _log, pid_fichier = _fichiers(schema)
    try:
        pid = int(pid_fichier.read_text().strip())
        os.kill(pid, 0)          # le processus existe encore
        return True
    except (FileNotFoundError, ValueError, ProcessLookupError, PermissionError):
        return False


def lancer(societe):
    """
    Lance le chargement en arrière-plan ; False s'il est déjà en cours.
    Le processus est détaché via un shell intermédiaire (rattaché à init) : il continue même si
    le worker web redémarre, et ne reste pas en processus zombie à la fin.
    """
    schema = societe.schema_name
    if en_cours(schema):
        return False
    log, pid_fichier = _fichiers(schema)
    commande = [sys.executable, str(Path(settings.BASE_DIR) / "manage.py"), "peupler_referentiel", "--tenant", schema]
    shell = subprocess.run(
        ["/bin/sh", "-c", 'log="$1"; shift; nohup "$@" > "$log" 2>&1 < /dev/null & echo $!', "sh", str(log), *commande],
        capture_output=True, text=True, cwd=str(settings.BASE_DIR), env=os.environ.copy(), check=True,
    )
    pid_fichier.write_text(shell.stdout.strip())
    return True


def etat(societe, lignes=15):
    """Comptages du référentiel du tenant + fin du journal + chargement en cours ou non."""
    from voiture.voiture_boite.models import VoitureBoite
    from voiture.voiture_marque.models import VoitureMarque
    from voiture.voiture_modele.models import VoitureModele
    from voiture.voiture_moteur.models import MoteurVoiture

    schema = societe.schema_name
    try:
        with schema_context(schema):
            comptes = {
                "marques": VoitureMarque.objects.filter(societe=societe).count(),
                "modeles": VoitureModele.objects.count(),
                "moteurs": MoteurVoiture.objects.count(),
                "boites": VoitureBoite.objects.count(),
            }
    except Exception:
        comptes = None
    log, _pid = _fichiers(schema)
    try:
        journal = log.read_text(encoding="utf-8", errors="replace").splitlines()[-lignes:]
    except FileNotFoundError:
        journal = []
    return {"comptes": comptes, "journal": journal, "en_cours": en_cours(schema)}

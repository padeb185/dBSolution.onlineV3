#!/bin/bash
# Sauvegarde PostgreSQL de CarsCosts, un dump par tenant, dans le dépôt restic carscosts.
#   - un snapshot restic par tenant (tag tenant:<schéma>) -> restauration d'un seul tenant possible
#   - plus le schéma public (tables partagées) et les rôles (pg_dumpall --globals-only)
#   - rétention 7 jours / 4 semaines / 12 mois / 1 an, par tenant
# Configuration : /etc/carscosts-backup.conf   Journal : /var/log/carscosts-backup-tenants.log
# À lancer en root (systemd : carscosts-backup-tenants.timer).
set -euo pipefail
umask 077

CONF=/etc/carscosts-backup.conf
[ -r "$CONF" ] || { echo "Configuration introuvable : $CONF" >&2; exit 1; }
# shellcheck source=/dev/null
. "$CONF"

: "${RESTIC_REPOSITORY:?RESTIC_REPOSITORY manquant dans $CONF}"
: "${RESTIC_PASSWORD_FILE:?RESTIC_PASSWORD_FILE manquant dans $CONF}"
export RESTIC_REPOSITORY RESTIC_PASSWORD_FILE
PG_PORT="${PG_PORT:-5435}"
PG_DB="${PG_DB:-dbsolution_db}"
PG_BIN="${PG_BIN:-/usr/lib/postgresql/19/bin}"
TABLE_TENANTS="${TABLE_TENANTS:-societe_societe}"
DUMP_DIR="${DUMP_DIR:-/var/backups/carscosts/dumps}"
REPO_GROUP="${REPO_GROUP:-}"          # groupe qui doit pouvoir lire le dépôt (ex. backupreader)
KEEP="${KEEP:---keep-daily 7 --keep-weekly 4 --keep-monthly 12 --keep-yearly 1}"
TAG="carscosts-db"
HOTE="$(hostname -s)"
LOG=/var/log/carscosts-backup-tenants.log

log()   { echo "== $(date '+%F %T') $*" | tee -a "$LOG"; }
echec() { log "ÉCHEC : $*"; exit 1; }
pg()    { runuser -u postgres -- "$PG_BIN/$1" -p "$PG_PORT" "${@:2}"; }

# Une seule exécution à la fois
exec 9>/run/carscosts-backup-tenants.lock
flock -n 9 || echec "une sauvegarde est déjà en cours"

command -v restic >/dev/null || echec "restic introuvable (apt install restic)"
[ -x "$PG_BIN/pg_dump" ] || echec "pg_dump introuvable dans $PG_BIN"
restic cat config >/dev/null 2>>"$LOG" || echec "dépôt restic inaccessible : $RESTIC_REPOSITORY"

log "début (base $PG_DB, port $PG_PORT)"
mkdir -p "$DUMP_DIR"
chown postgres: "$DUMP_DIR"; chmod 700 "$DUMP_DIR"
find "$DUMP_DIR" -maxdepth 1 -name '*.dump' -delete

# Dump dans le format personnalisé SANS compression : restic déduplique d'un jour à l'autre et compresse lui-même.
dump_schema() {  # $1 = schéma, $2 = fichier
  pg pg_dump -d "$PG_DB" -Fc --compress=0 -n "$1" -f "$DUMP_DIR/$2" 2>>"$LOG"
}

envoyer() {      # $1 = fichier, $2.. = tags supplémentaires
  local f="$1"; shift
  local tags=(--tag "$TAG")
  for t in "$@"; do tags+=(--tag "$t"); done
  restic backup --host "$HOTE" "${tags[@]}" "$DUMP_DIR/$f" >>"$LOG" 2>&1
}

erreurs=0

# 1) Rôles et droits (communs à toute l'instance)
if runuser -u postgres -- "$PG_BIN/pg_dumpall" -p "$PG_PORT" --globals-only > "$DUMP_DIR/globals.sql" 2>>"$LOG" \
   && envoyer globals.sql "globals"; then
  log "rôles OK"
else
  log "rôles ÉCHEC"; erreurs=$((erreurs+1))
fi

# 2) Schéma public (tenants, domaines, utilisateurs partagés, extensions)
if dump_schema public public.dump && envoyer public.dump "tenant:public"; then
  log "public OK ($(du -h "$DUMP_DIR/public.dump" | cut -f1))"
else
  log "public ÉCHEC"; erreurs=$((erreurs+1))
fi

# 3) Un dump par tenant
mapfile -t TENANTS < <(pg psql -d "$PG_DB" -XAtc \
  "SELECT schema_name FROM public.$TABLE_TENANTS WHERE schema_name <> 'public' ORDER BY schema_name")
[ "${#TENANTS[@]}" -gt 0 ] || echec "aucun tenant trouvé dans public.$TABLE_TENANTS"

for s in "${TENANTS[@]}"; do
  [[ "$s" =~ ^[a-z0-9_]+$ ]] || { log "tenant ignoré (nom inattendu) : $s"; erreurs=$((erreurs+1)); continue; }
  if dump_schema "$s" "tenant_$s.dump" && envoyer "tenant_$s.dump" "tenant:$s"; then
    log "tenant $s OK ($(du -h "$DUMP_DIR/tenant_$s.dump" | cut -f1))"
  else
    log "tenant $s ÉCHEC"; erreurs=$((erreurs+1))
  fi
done

# 4) Schémas présents dans la base mais absents de la table des tenants (orphelins) : signalés, pas sauvegardés
mapfile -t ORPHELINS < <(pg psql -d "$PG_DB" -XAtc \
  "SELECT nspname FROM pg_namespace
    WHERE nspname NOT LIKE 'pg\_%' AND nspname NOT IN ('public','information_schema')
      AND nspname NOT IN (SELECT schema_name FROM public.$TABLE_TENANTS) ORDER BY 1")
[ "${#ORPHELINS[@]}" -eq 0 ] || log "ATTENTION schémas sans tenant (non sauvegardés) : ${ORPHELINS[*]}"

# 5) Rétention par tenant (un groupe par jeu de tags)
if restic forget --tag "$TAG" --host "$HOTE" --group-by host,tags $KEEP --prune >>"$LOG" 2>&1; then
  log "rétention OK"
else
  log "rétention ÉCHEC"; erreurs=$((erreurs+1))
fi

# 6) Vérification du dépôt le dimanche (5 % des données relues)
if [ "$(date +%u)" = 7 ]; then
  restic check --read-data-subset=5% >>"$LOG" 2>&1 && log "vérification OK" \
    || { log "vérification ÉCHEC"; erreurs=$((erreurs+1)); }
fi

# 7) Droits de lecture pour la copie vers le Mac (utilisateur backupreader)
if [ -n "$REPO_GROUP" ] && [ -d "$RESTIC_REPOSITORY" ]; then
  chgrp -R "$REPO_GROUP" "$RESTIC_REPOSITORY"
  chmod -R g+rX "$RESTIC_REPOSITORY"
fi

find "$DUMP_DIR" -maxdepth 1 \( -name '*.dump' -o -name '*.sql' \) -delete
[ "$erreurs" -eq 0 ] || echec "$erreurs erreur(s), voir $LOG"
log "terminé (${#TENANTS[@]} tenants)"

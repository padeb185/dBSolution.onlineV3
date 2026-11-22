#!/bin/bash
# Restaure UN tenant depuis le dépôt restic carscosts.
#   restaurer-tenant.sh <schéma> [snapshot|latest] [--remplacer]
# Sans --remplacer : restauration dans un schéma de contrôle <schéma>_restaure (rien n'est écrasé).
# Avec --remplacer : le schéma existant est renommé <schéma>_avant_<date>, puis le tenant est restauré à sa place.
set -euo pipefail
. /etc/carscosts-backup.conf
export RESTIC_REPOSITORY RESTIC_PASSWORD_FILE
PG_PORT="${PG_PORT:-5435}"; PG_DB="${PG_DB:-dbsolution_db}"; PG_BIN="${PG_BIN:-/usr/lib/postgresql/19/bin}"
S="${1:?schéma du tenant}"; SNAP="${2:-latest}"; MODE="${3:-}"
[[ "$S" =~ ^[a-z0-9_]+$ ]] || { echo "nom de schéma invalide"; exit 1; }
TMP=$(mktemp -d); chown postgres: "$TMP"; trap 'rm -rf "$TMP"' EXIT

restic dump --tag "tenant:$S" "$SNAP" "/var/backups/carscosts/dumps/tenant_$S.dump" > "$TMP/t.dump"
chown postgres: "$TMP/t.dump"
psql_() { runuser -u postgres -- "$PG_BIN/psql" -p "$PG_PORT" -d "$PG_DB" -v ON_ERROR_STOP=1 "$@"; }

if [ "$MODE" = "--remplacer" ]; then
  ANCIEN="${S}_avant_$(date +%Y%m%d_%H%M)"
  psql_ -c "ALTER SCHEMA \"$S\" RENAME TO \"$ANCIEN\";"
  runuser -u postgres -- "$PG_BIN/pg_restore" -p "$PG_PORT" -d "$PG_DB" --exit-on-error "$TMP/t.dump"   # propriétaires d'origine conservés
  echo "Tenant $S restauré. Ancienne version conservée dans le schéma $ANCIEN."
else
  CIBLE="${S}_restaure"
  psql_ -c "DROP SCHEMA IF EXISTS \"$CIBLE\" CASCADE;"
  runuser -u postgres -- "$PG_BIN/pg_restore" -p "$PG_PORT" -f - "$TMP/t.dump" \
    | sed -e "s/\"$S\"\./\"$CIBLE\"./g; s/^CREATE SCHEMA $S;/CREATE SCHEMA $CIBLE;/; s/ $S\./ $CIBLE./g; s/search_path = $S,/search_path = $CIBLE,/" \
    | psql_ -q >/dev/null
  echo "Copie de contrôle restaurée dans le schéma $CIBLE (à supprimer après vérification)."
fi

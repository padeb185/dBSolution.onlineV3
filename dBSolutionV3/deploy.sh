#!/bin/bash
set -e

PROJET=~/PyCharmMiscProject/dBSolution.onlineV3/dBSolutionV3
SERVEUR=padeb@187.77.163.177
DISTANT=/var/www/carscosts/dBSolutionV3

echo "1. Build Tailwind"
cd "$PROJET"
source .venv312/bin/activate
python manage.py tailwind build

echo "2. Envoi des fichiers"
rsync -avz --delete \
    --exclude='.venv/' --exclude='.venv312/' --exclude='.git/' --exclude='.idea/' \
    --exclude='__pycache__/' --exclude='*.pyc' --exclude='.env' \
    --exclude='media/' --exclude='staticfiles/' --exclude='logs/' \
    -e "ssh -p 2222" \
    "$PROJET/" "$SERVEUR:$DISTANT/"

echo "3. Déploiement serveur"
ssh -t -p 2222 "$SERVEUR" "
    set -e
    cd $DISTANT
    source /var/www/carscosts/.venv/bin/activate
    python manage.py migrate_schemas --shared
    python manage.py migrate_schemas --tenant
    python manage.py collectstatic --noinput --clear
    sudo chown -R padeb:www-data $DISTANT
    sudo find $DISTANT -type d -exec chmod 755 {} \;
    sudo find $DISTANT -type f -exec chmod 644 {} \;
    sudo systemctl restart carscosts.service
    sudo nginx -t && sudo systemctl reload nginx
"

echo "Déploiement terminé"
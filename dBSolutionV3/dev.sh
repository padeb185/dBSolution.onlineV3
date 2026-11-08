#!/bin/zsh
# Serveur Django local pour développer l'application des particuliers sans déployer.
#   ./dev.sh            migrations du tenant des particuliers puis serveur sur le port 8000
#   ./dev.sh vite       serveur seulement (sans migrations)
# Le serveur se recharge tout seul à chaque modification d'un fichier .py ;
# le catalogue des marques (particulier/donnees/marques_modeles.json) est relu sans redémarrage.
cd "${0:A:h}" || exit 1
export DEBUG=True                       # achats de test acceptés, erreurs détaillées, HTTP local
if [[ "$1" != "vite" ]]; then
  python manage.py migrate_schemas --schema=particuliers || exit 1
fi
echo "API locale : http://127.0.0.1:8000/api/v1  (émulateur Android : http://10.0.2.2:8000/api/v1)"
exec python manage.py runserver 0.0.0.0:8000

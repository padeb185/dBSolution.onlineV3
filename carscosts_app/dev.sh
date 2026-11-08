#!/bin/zsh
# Lance l'application sur l'API Django locale (démarrer d'abord dBSolutionV3/dev.sh).
#   ./dev.sh ios        simulateur iPhone
#   ./dev.sh android    émulateur Android
#   ./dev.sh macos      application Mac
#   ./dev.sh            choix de l'appareil par Flutter (simulateur iPhone par défaut)
# Pendant l'exécution : r = rechargement à chaud, R = redémarrage complet, q = quitter.
cd "${0:A:h}" || exit 1

# Identifiant du premier appareil dont le type correspond (sortie JSON de Flutter, sans espaces parasites)
appareil() {
  flutter devices --machine 2>/dev/null | python3 -c "
import json, sys
try:
    liste = json.load(sys.stdin)
except Exception:
    liste = []
for d in liste:
    if d.get('emulator') and d.get('targetPlatform', '').startswith('$1'):
        print(d['id']); break
"
}

case "$1" in
  android)
    API=http://10.0.2.2:8000/api/v1
    APPAREIL=$(appareil android)
    if [[ -z "$APPAREIL" ]]; then
      flutter emulators --launch Medium_Phone_API_37.0 && sleep 25
      APPAREIL=$(appareil android)
    fi
    ;;
  macos) API=http://127.0.0.1:8000/api/v1; APPAREIL=macos ;;
  *)
    API=http://127.0.0.1:8000/api/v1
    APPAREIL=$(appareil ios)
    if [[ -z "$APPAREIL" ]]; then
      open -a /Applications/Xcode.app/Contents/Applications/DeviceHub.app 2>/dev/null || open -a Simulator
      sleep 10
      APPAREIL=$(appareil ios)
    fi
    ;;
esac
echo "Appareil : ${APPAREIL:-choix de Flutter} · API : $API"
# zsh ne découpe pas les variables : l'option -d et l'identifiant sont deux arguments distincts
OPTIONS=()
[[ -n "$APPAREIL" ]] && OPTIONS=(-d "$APPAREIL")
exec flutter run "${OPTIONS[@]}" --dart-define=API_URL="$API"

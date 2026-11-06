# Lancer CarsCosts sur les simulateurs

Toutes les commandes : depuis `~/PyCharmMiscProject/dBSolution.onlineV3/carscosts_app`

## Voir ce qui est disponible
    flutter devices
    flutter emulators
    xcrun simctl list devices available
    flutter doctor

## Mac
    flutter run -d macos

## iPhone (Xcode 27 : l'écran s'affiche dans DeviceHub, plus dans « Simulator »)
    xcrun simctl boot 288D452A-1EE0-414F-BE53-3B0EE93601E7
    open -a DeviceHub
    flutter run -d 288D452A-1EE0-414F-BE53-3B0EE93601E7
Arrêt :
    xcrun simctl shutdown 288D452A-1EE0-414F-BE53-3B0EE93601E7

## Android
    flutter emulators --launch Pixel_9
    flutter run -d emulator-5554
Arrêt :
    adb -s emulator-5554 emu kill

## Serveur
- En ligne (défaut) : rien à ajouter
- Django local, Mac / iPhone : `--dart-define=API_URL=http://127.0.0.1:8000/api/v1`
- Django local, Android : `--dart-define=API_URL=http://10.0.2.2:8000/api/v1`
  (Django : `python manage.py runserver 0.0.0.0:8000` depuis dBSolutionV3)

## Pendant que l'application tourne
- `r` recharge le code · `R` redémarre · `q` arrête

## En cas de problème
    flutter clean
    flutter pub get
    cd ios && pod install && cd ..

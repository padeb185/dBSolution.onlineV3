# CarsCosts – application des particuliers (Flutter)

Application iOS, Android, macOS et Windows des particuliers. Elle parle à l'API Django
`/api/v1/` (app `particulier` du projet dBSolutionV3). L'application professionnelle reste le site web Django.

Fonctions : véhicules et kilométrages · pleins avec photo du ticket · entretiens et rappels ·
documents (assurance, contrôle technique, carte grise…) avec rappel d'échéance · coûts et rentabilité
(coût total, coût au km, par mois, consommation, dépenses par année) · lecture du VIN (code-barres
ou photo de la carte grise, iOS / Android).

## 1. Première installation

Ce dossier ne contient que le code (`lib/`, `test/`, `pubspec.yaml`). Les projets natifs sont générés
par Flutter (les fichiers existants ne sont pas écrasés) :

```bash
cd carscosts_app
flutter create --org com.carscosts --project-name carscosts_app --platforms=ios,android,macos,windows .
flutter pub get
flutter test
```

Puis appliquer les réglages natifs ci-dessous (§ 3).

## 2. Lancer en développement

Serveur Django local : `python manage.py runserver 0.0.0.0:8000`

```bash
# iPhone (simulateur), Mac, Windows
flutter run --dart-define=API_URL=http://127.0.0.1:8000/api/v1
# Émulateur Android (10.0.2.2 = le Mac)
flutter run --dart-define=API_URL=http://10.0.2.2:8000/api/v1
```

Sans `API_URL`, l'application utilise `https://carscosts.com/api/v1`.

## 3. Réglages natifs (après `flutter create`)

**iOS** – `ios/Runner/Info.plist` :

```xml
<key>NSCameraUsageDescription</key>
<string>L'appareil photo sert à photographier vos tickets, documents et à lire le VIN.</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>Choisir une photo de ticket, de document ou de votre véhicule.</string>
```

`ios/Podfile` : `platform :ios, '15.5'` (exigé par ML Kit).
En développement (HTTP local), ajouter une exception ATS pour `127.0.0.1`.

**Android** – `android/app/src/main/AndroidManifest.xml` (avant `<application>`) :

```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.CAMERA"/>
```

`android/app/build.gradle` : `minSdkVersion 21` (ou plus).
En développement (HTTP local) : `android:usesCleartextTraffic="true"` sur `<application>`.

**macOS** – `macos/Runner/DebugProfile.entitlements` et `Release.entitlements` :

```xml
<key>com.apple.security.network.client</key><true/>
<key>com.apple.security.files.user-selected.read-only</key><true/>
<key>com.apple.security.device.camera</key><true/>
```

et `NSCameraUsageDescription` dans `macos/Runner/Info.plist`.

**Windows** – Visual Studio avec « Développement desktop en C++ » (ATL inclus, requis par
`flutter_secure_storage`). Sur Windows et macOS, la lecture du VIN se fait par saisie
(ML Kit et l'appareil photo de `image_picker` sont propres au mobile).

## 4. Organisation du code

```
lib/
  config.dart                 adresse de l'API (--dart-define=API_URL)
  main.dart                   thème, langue, session → connexion ou accueil
  api/api_client.dart         HTTP, jeton « Token … », envoi de fichiers, erreurs DRF
  api/session.dart            connexion, inscription, déconnexion, suppression du compte
  modeles/ressources.dart     pleins, entretiens, rappels, documents, dépenses, kilométrages :
                              champs, libellés et listes (formulaire générique)
  ecrans/accueil_ecran.dart   rappels à traiter, véhicules, dépenses du mois
  ecrans/vehicule_ecran.dart  fiche : synthèse des coûts + onglets
  ecrans/vehicule_form_ecran.dart  ajout / modification d'un véhicule (+ VIN)
  ecrans/vin_ecran.dart       lecture du VIN : code-barres, OCR, saisie
  ecrans/formulaire_ecran.dart     formulaire générique (dont photos et fichiers)
  ecrans/connexion_ecran.dart, compte_ecran.dart
  widgets/                    listes, fichiers protégés, formats (€, km, dates)
```

## 5. API utilisée (Django `particulier/api/`)

| Méthode | Chemin | Rôle |
|---|---|---|
| POST | `auth/inscription/` · `auth/connexion/` · `auth/deconnexion/` | compte, jeton |
| GET / PATCH / DELETE | `moi/` | profil ; suppression du compte (mot de passe) |
| GET | `tableau-de-bord/` | véhicules, rappels proches ou en retard, dépenses du mois |
| CRUD | `vehicules/` (+ `{id}/synthese/`, `{id}/consommation/`, `{id}/photo/`) | véhicules |
| CRUD | `kilometrages/` `pleins/` `entretiens/` `documents/` `rappels/` `depenses/` (`?vehicule=<id>`) | données du véhicule |
| GET | `pleins/{id}/ticket/` · `entretiens/{id}/facture/` · `documents/{id}/fichier/` | fichiers privés |
| POST | `rappels/{id}/fait/` | rappel réalisé → prochaine échéance |
| GET | `vin/?vin=…` | décodage du VIN (marque, année) |

## 6. Prochaines étapes

- Notifications locales des rappels (`flutter_local_notifications`) puis push (APNs / FCM via Celery).
- Traductions (`flutter gen-l10n`) : nl, en, de.
- Saisie hors ligne des pleins (file d'attente locale).
- « Se connecter avec Apple » (obligatoire si une connexion Google est ajoutée).
- Publication : icônes, App Store Connect, Google Play, MSIX (Windows).

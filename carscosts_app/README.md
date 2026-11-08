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

## 2. Développer en local (sans déployer)

Deux terminaux :

```bash
cd dBSolutionV3 && ./dev.sh          # API Django locale (port 8000), rechargée à chaque modification .py
cd carscosts_app && ./dev.sh ios     # ou android / macos : l'app sur l'API locale
```

Dans le terminal de l'app : `r` rechargement à chaud (Dart), `R` redémarrage complet, `q` quitter.
Base locale (PostgreSQL du Mac, tenant « particuliers »), `DEBUG=True` : achats de test acceptés.
Téléphone réel sur le Wi-Fi : `ALLOWED_HOSTS_DEV=192.168.x.y` dans le `.env` local et
`flutter run --dart-define=API_URL=http://192.168.x.y:8000/api/v1`.
Mise en ligne seulement quand c'est prêt : `./deploy.sh` (+ `migrate_schemas` sur le serveur s'il y a des migrations).

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
  ecrans/connexion_ecran.dart connexion / inscription (choix de la langue)
  ecrans/reglages_ecran.dart  réglages : profil, email, mot de passe, langue, pays par défaut,
                              formule, déconnexion, suppression du compte
  l10n/langue.dart            langue courante, t('texte français') → traduction
  l10n/traductions.dart       traductions nl, en, de, es, it, el (clé = texte français)
  widgets/                    listes, fichiers protégés, formats (€, km, dates)
```

## 5. API utilisée (Django `particulier/api/`)

| Méthode | Chemin | Rôle |
|---|---|---|
| POST | `auth/inscription/` · `auth/connexion/` · `auth/deconnexion/` | compte, jeton |
| GET / PATCH / DELETE | `moi/` | profil, langue, pays par défaut ; suppression du compte (mot de passe) |
| POST | `moi/mot-de-passe/` · `moi/email/` | changement du mot de passe (nouveau jeton) / de l'email |
| GET | `tableau-de-bord/` | véhicules, rappels proches ou en retard, dépenses du mois |
| CRUD | `vehicules/` (+ `{id}/synthese/`, `{id}/consommation/`, `{id}/photo/`) | véhicules |
| CRUD | `kilometrages/` `pleins/` `entretiens/` `documents/` `rappels/` `depenses/` (`?vehicule=<id>`) | données du véhicule |
| GET | `pleins/{id}/ticket/` · `entretiens/{id}/facture/` · `documents/{id}/fichier/` | fichiers privés |
| POST | `rappels/{id}/fait/` | rappel réalisé → prochaine échéance |
| GET | `vin/?vin=…` | décodage du VIN (marque, année) |
| GET | `abonnement/` | formule, limite, véhicules actifs, formules et produits |
| POST | `abonnement/achat/` | preuve d'achat (`apple` / `google` / `test`) → formule |

## 6. Formules et achats intégrés

| Formule | Gratuit | Bronze | Silver | Gold |
|---|---|---|---|---|
| Véhicules actifs (non archivés) | 1 | 2 | 5 | 10 |
| Produit (App Store et Google Play) | – | `carscosts_bronze_mensuel` | `carscosts_silver_mensuel` | `carscosts_gold_mensuel` |

La limite est appliquée par le serveur (ajout et désarchivage d'un véhicule → 403 `limite_formule`) ;
l'application ouvre alors l'écran **Formules** (`lib/ecrans/formules_ecran.dart`, service `lib/achats/abonnement.dart`).

- **Développement** (`PARTICULIERS_ACHATS_MODE=test`, défaut si `DEBUG=True`) : bouton « Activer (test) »
  (formule 30 jours, sans store) + attribution dans « Particuliers – administration » ou l'admin Django.
  Les achats Sandbox (TestFlight, testeurs Google Play) sont aussi acceptés (`PARTICULIERS_ACHATS_SANDBOX`).
- **Production** (`PARTICULIERS_ACHATS_MODE=store`) : achat dans l'app ; le serveur vérifie la transaction
  StoreKit 2 signée (Apple) ou le `purchaseToken` (API Google Play Developer) avant d'activer la formule.

Configuration des stores :
1. App Store Connect : un groupe d'abonnements « CarsCosts » avec les 3 produits (Gold > Silver > Bronze, pour
   les changements de niveau) ; *App Store Server Notifications V2* →
   `https://carscosts.com/api/v1/abonnement/notifications/apple/` ; serveur : `APPLE_ROOT_CA_G3=` chemin de
   `AppleRootCA-G3.cer` (apple.com/certificateauthority).
2. Play Console : 3 abonnements (mêmes identifiants) ; compte de service avec accès « Afficher les données
   financières / gérer les commandes » → `GOOGLE_SERVICE_ACCOUNT_FILE=` chemin du JSON (hors du dossier du projet) ;
   *Real-time developer notifications* : sujet Pub/Sub avec abonnement push vers
   `https://carscosts.com/api/v1/abonnement/notifications/google/?jeton=<GOOGLE_RTDN_JETON>`.
3. Un fichier StoreKit local (Xcode) signe les achats avec un certificat local, refusé par le serveur :
   tester avec « Activer (test) », puis en Sandbox sur un vrai appareil / TestFlight.

## 7. Prochaines étapes

- Notifications locales des rappels (`flutter_local_notifications`) puis push (APNs / FCM via Celery).
- Langues : fr, nl, en, de, es, it, el. Un texte ajouté s'écrit `t('Texte en français')` et se traduit
  dans `lib/l10n/traductions.dart` (sinon il reste en français).
- Saisie hors ligne des pleins (file d'attente locale).
- « Se connecter avec Apple » (obligatoire si une connexion Google est ajoutée).
- Publication : icônes, App Store Connect, Google Play, MSIX (Windows).

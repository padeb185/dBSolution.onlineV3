import 'dart:io' show Platform;

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:local_auth/local_auth.dart';

import '../l10n/langue.dart';

/// Déverrouillage biométrique (Face ID / Touch ID sur iPhone et Mac, empreinte ou visage sur Android,
/// Windows Hello) : proposé après une connexion par mot de passe, demandé à l'ouverture de l'application
/// et au retour après [delaiVerrou] en arrière-plan. Le jeton de session reste dans le stockage sécurisé.
class Biometrie extends ChangeNotifier {
  final LocalAuthentication _auth = LocalAuthentication();
  static const FlutterSecureStorage _stockage = FlutterSecureStorage();
  static const _cleActive = 'biometrie_active';
  static const _cleProposee = 'biometrie_proposee';
  static const delaiVerrou = Duration(minutes: 5);

  /// L'appareil a une biométrie configurée
  bool disponible = false;
  /// L'utilisateur a choisi de déverrouiller l'application par biométrie
  bool active = false;
  /// L'application attend le déverrouillage
  bool verrouille = false;
  /// L'activation a déjà été proposée (on ne la repropose pas à chaque connexion)
  bool proposee = false;

  List<BiometricType> _types = const [];
  DateTime? _arrierePlanDepuis;

  Future<void> charger() async {
    try {
      disponible = await _auth.isDeviceSupported() && await _auth.canCheckBiometrics;
      if (disponible) _types = await _auth.getAvailableBiometrics();
      disponible = disponible && _types.isNotEmpty;
    } catch (_) {
      disponible = false;
    }
    active = disponible && await _stockage.read(key: _cleActive) == '1';
    proposee = await _stockage.read(key: _cleProposee) == '1';
  }

  /// Nom de la méthode affiché à l'utilisateur
  String get methode {
    if (Platform.isIOS || Platform.isMacOS) return _types.contains(BiometricType.face) ? 'Face ID' : 'Touch ID';
    if (Platform.isWindows) return 'Windows Hello';
    return t('Empreinte ou visage');
  }

  Future<bool> authentifier() async {
    try {
      return await _auth.authenticate(
        localizedReason: t('Déverrouillez CarsCosts'),
        // Échec répété de la biométrie : le code de l'appareil reste possible
        options: const AuthenticationOptions(biometricOnly: false, stickyAuth: true),
      );
    } on PlatformException {
      return false;
    }
  }

  Future<void> deverrouiller() async {
    if (await authentifier()) {
      verrouille = false;
      notifyListeners();
    }
  }

  /// Activation (après une vérification biométrique) ou désactivation.
  Future<bool> activer(bool valeur) async {
    if (valeur && !await authentifier()) return false;
    active = valeur;
    proposee = true;
    await _stockage.write(key: _cleActive, value: valeur ? '1' : '0');
    await _stockage.write(key: _cleProposee, value: '1');
    notifyListeners();
    return true;
  }

  Future<void> marquerProposee() async {
    proposee = true;
    await _stockage.write(key: _cleProposee, value: '1');
  }

  /// Ouverture de l'application avec une session enregistrée
  void auDemarrage(bool connecte) => verrouille = connecte && active;

  void arrierePlan() => _arrierePlanDepuis = DateTime.now();

  void premierPlan(bool connecte) {
    final depuis = _arrierePlanDepuis;
    _arrierePlanDepuis = null;
    if (connecte && active && depuis != null && DateTime.now().difference(depuis) >= delaiVerrou) {
      verrouille = true;
      notifyListeners();
    }
  }

  /// Déconnexion : le prochain compte connecté sur l'appareil choisira lui-même
  Future<void> reinitialiser() async {
    active = false;
    proposee = false;
    verrouille = false;
    await _stockage.delete(key: _cleActive);
    await _stockage.delete(key: _cleProposee);
    notifyListeners();
  }
}

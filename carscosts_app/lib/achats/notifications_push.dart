import 'dart:async';
import 'dart:io' show Platform;

import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/foundation.dart';

import '../api/api_client.dart';

/// Notifications push (Firebase Cloud Messaging) : paiement refusé, renouvellement proche, formule suspendue…
///
/// - iOS, Android et macOS seulement (pas Windows ni web).
/// - Sans configuration Firebase (google-services.json / GoogleService-Info.plist, voir README), l'application
///   fonctionne normalement, sans push.
/// - Le jeton de l'appareil est envoyé à l'API (`appareils/`) une fois connecté, et retiré à la déconnexion.
class NotificationsPush {
  NotificationsPush(this.api, {this.auMessage});

  final ApiClient api;

  /// Message reçu application ouverte (ex. recharger l'état de l'abonnement).
  final VoidCallback? auMessage;

  bool _pret = false;
  String? _jeton;
  StreamSubscription<String>? _rafraichissement;

  static bool get plateformeCompatible => !kIsWeb && (Platform.isIOS || Platform.isAndroid || Platform.isMacOS);

  String get _plateforme => Platform.isAndroid ? 'android' : (Platform.isIOS ? 'ios' : 'macos');

  Future<void> demarrer() async {
    if (!plateformeCompatible || _pret) return;
    try {
      await Firebase.initializeApp();
      _pret = true;
      FirebaseMessaging.onMessage.listen((_) => auMessage?.call());
      FirebaseMessaging.onMessageOpenedApp.listen((_) => auMessage?.call());
    } catch (e) {
      debugPrint('Notifications push indisponibles : $e');
    }
  }

  /// Après connexion : autorisation (iOS / Android 13+), puis enregistrement du jeton auprès de l'API.
  Future<void> enregistrer() async {
    await demarrer();
    if (!_pret || !api.connecte) return;
    try {
      final reglages = await FirebaseMessaging.instance.requestPermission();
      if (reglages.authorizationStatus == AuthorizationStatus.denied) return;
      if (Platform.isIOS || Platform.isMacOS) {
        // Le jeton FCM n'existe qu'une fois le jeton APNs obtenu
        if (await FirebaseMessaging.instance.getAPNSToken() == null) {
          await Future<void>.delayed(const Duration(seconds: 3));
        }
      }
      final jeton = await FirebaseMessaging.instance.getToken();
      if (jeton != null) await _envoyer(jeton);
      _rafraichissement ??= FirebaseMessaging.instance.onTokenRefresh.listen(_envoyer);
    } catch (e) {
      debugPrint('Enregistrement push impossible : $e');
    }
  }

  Future<void> _envoyer(String jeton) async {
    if (!api.connecte) return;
    _jeton = jeton;
    try {
      await api.post('appareils/', {'jeton': jeton, 'plateforme': _plateforme});
    } catch (e) {
      debugPrint('Jeton push non envoyé : $e');
    }
  }

  /// Avant la déconnexion : l'appareil ne reçoit plus les notifications de ce compte.
  Future<void> desinscrire() async {
    final jeton = _jeton;
    if (jeton == null || !api.connecte) return;
    try {
      await api.delete('appareils/?jeton=${Uri.encodeQueryComponent(jeton)}');
    } catch (_) {}
    _jeton = null;
  }
}

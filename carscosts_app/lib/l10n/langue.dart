import 'dart:ui' as ui;

import 'package:flutter/foundation.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import 'traductions.dart';

/// Langues de l'application (mêmes langues que le site dBSolution).
const languesApp = <String, String>{
  'fr': 'Français',
  'nl': 'Nederlands',
  'en': 'English',
  'de': 'Deutsch',
  'es': 'Español',
  'it': 'Italiano',
  'el': 'Ελληνικά',
};

/// Langue courante : choisie à l'inscription ou dans les réglages, enregistrée sur l'appareil
/// et dans le compte (le serveur répond alors dans cette langue).
class Langue extends ChangeNotifier {
  static String courante = 'fr';
  static const _cle = 'carscosts_langue';
  final FlutterSecureStorage _stockage = const FlutterSecureStorage();

  String get code => courante;

  /// Langue enregistrée sur l'appareil, sinon celle du système si elle est proposée, sinon le français.
  Future<void> charger() async {
    String? code;
    try {
      code = await _stockage.read(key: _cle);
    } catch (_) {}
    code ??= ui.PlatformDispatcher.instance.locale.languageCode;
    courante = languesApp.containsKey(code) ? code : 'fr';
  }

  Future<void> choisir(String code) async {
    if (!languesApp.containsKey(code) || code == courante) return;
    courante = code;
    try {
      await _stockage.write(key: _cle, value: code);
    } catch (_) {}
    notifyListeners();
  }
}

/// Traduction d'un texte de l'interface (clé = texte français).
/// Paramètres : t('{n} véhicule(s)', {'n': 3}).
String t(String francais, [Map<String, Object?> parametres = const {}]) {
  var texte = Langue.courante == 'fr' ? francais : (traductions[Langue.courante]?[francais] ?? francais);
  parametres.forEach((cle, valeur) => texte = texte.replaceAll('{$cle}', '${valeur ?? ''}'));
  return texte;
}

/// Locale intl (dates, nombres, montants) de la langue courante.
String get localeIntl => switch (Langue.courante) {
      'fr' => 'fr_BE',
      'nl' => 'nl_BE',
      'en' => 'en_GB',
      'de' => 'de_DE',
      'es' => 'es_ES',
      'it' => 'it_IT',
      'el' => 'el_GR',
      _ => 'fr_BE',
    };

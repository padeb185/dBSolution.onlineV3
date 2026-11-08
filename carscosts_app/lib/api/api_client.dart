import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;

import '../config.dart';
import '../l10n/langue.dart';

/// Erreur renvoyée par l'API (message lisible extrait de la réponse Django REST Framework).
class ApiException implements Exception {
  ApiException(this.statut, this.message, [this.champs = const {}]);

  final int statut;
  final String message;

  /// Erreurs par champ : {"kilometrage": "Ce champ est obligatoire."}
  final Map<String, String> champs;

  @override
  String toString() => message;
}

/// Fichier à envoyer (photo du ticket, document…).
class FichierEnvoi {
  FichierEnvoi(this.champ, this.chemin);

  final String champ;
  final String chemin;
}

/// Client HTTP de l'API particuliers : jeton « Token … », JSON, envoi de fichiers.
class ApiClient {
  ApiClient({http.Client? client}) : _http = client ?? http.Client();

  final http.Client _http;
  final FlutterSecureStorage _stockage = const FlutterSecureStorage();
  static const _cleJeton = 'carscosts_jeton';

  String? _jeton;
  String? get jeton => _jeton;
  bool get connecte => _jeton != null;

  Future<void> chargerJeton() async => _jeton = await _stockage.read(key: _cleJeton);

  Future<void> enregistrerJeton(String? jeton) async {
    _jeton = jeton;
    if (jeton == null) {
      await _stockage.delete(key: _cleJeton);
    } else {
      await _stockage.write(key: _cleJeton, value: jeton);
    }
  }

  Map<String, String> get entetesAuth => {if (_jeton != null) 'Authorization': 'Token $_jeton'};

  Uri _uri(String chemin, [Map<String, String>? params]) {
    final url = chemin.startsWith('http') ? chemin : '$apiUrl/${chemin.replaceFirst(RegExp(r'^/'), '')}';
    return Uri.parse(url).replace(queryParameters: params);
  }

  // ------------------------------------------------------------------ JSON
  Future<dynamic> get(String chemin, {Map<String, String>? params}) =>
      _envoyer(() => _http.get(_uri(chemin, params), headers: _entetes()));

  Future<dynamic> post(String chemin, [Map<String, dynamic>? donnees]) =>
      _envoyer(() => _http.post(_uri(chemin), headers: _entetes(), body: jsonEncode(donnees ?? {})));

  Future<dynamic> put(String chemin, Map<String, dynamic> donnees) =>
      _envoyer(() => _http.put(_uri(chemin), headers: _entetes(), body: jsonEncode(donnees)));

  Future<dynamic> patch(String chemin, Map<String, dynamic> donnees) =>
      _envoyer(() => _http.patch(_uri(chemin), headers: _entetes(), body: jsonEncode(donnees)));

  Future<dynamic> delete(String chemin, [Map<String, dynamic>? donnees]) => _envoyer(
      () => _http.delete(_uri(chemin), headers: _entetes(), body: donnees == null ? null : jsonEncode(donnees)));

  Map<String, String> _entetes() => {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Language': Langue.courante,
        ...entetesAuth,
      };

  // ------------------------------------------------------------------ Multipart (fichiers)
  /// POST (création) ou PATCH (modification) avec fichiers joints.
  Future<dynamic> envoyerAvecFichiers(String methode, String chemin, Map<String, dynamic> donnees,
      List<FichierEnvoi> fichiers) {
    return _envoyer(() async {
      final requete = http.MultipartRequest(methode, _uri(chemin))..headers.addAll({...entetesAuth, 'Accept-Language': Langue.courante});
      donnees.forEach((cle, valeur) {
        if (valeur != null) requete.fields[cle] = valeur.toString();
      });
      for (final f in fichiers) {
        requete.files.add(await http.MultipartFile.fromPath(f.champ, f.chemin));
      }
      return http.Response.fromStream(await _http.send(requete));
    });
  }

  /// Fichier privé (ticket, document) : téléchargé avec le jeton.
  Future<Uint8List> telecharger(String url) async {
    final reponse = await _http.get(_uri(url), headers: entetesAuth);
    if (reponse.statusCode != 200) throw ApiException(reponse.statusCode, t('Fichier indisponible.'));
    return reponse.bodyBytes;
  }

  // ------------------------------------------------------------------ Réponses
  Future<dynamic> _envoyer(Future<http.Response> Function() appel) async {
    http.Response reponse;
    try {
      reponse = await appel();
    } catch (e) {
      throw ApiException(0, t('Serveur injoignable. Vérifiez votre connexion internet.'));
    }
    final corps = reponse.body.isEmpty ? null : _decoder(reponse);
    if (reponse.statusCode >= 200 && reponse.statusCode < 300) return corps;
    if (reponse.statusCode == 401) {
      await enregistrerJeton(null);
      throw ApiException(401, t('Session expirée : reconnectez-vous.'));
    }
    throw _erreur(reponse.statusCode, corps);
  }

  dynamic _decoder(http.Response r) {
    try {
      return jsonDecode(utf8.decode(r.bodyBytes));
    } catch (_) {
      return null;
    }
  }

  ApiException _erreur(int statut, dynamic corps) {
    final champs = <String, String>{};
    String? message;
    if (corps is Map) {
      corps.forEach((cle, valeur) {
        final texte = valeur is List ? valeur.join(' ') : valeur.toString();
        if (cle == 'detail' || cle == 'non_field_errors') {
          message = texte;
        } else {
          champs[cle.toString()] = texte;
        }
      });
    }
    message ??= champs.isNotEmpty ? t('Vérifiez les champs indiqués.') : t('Erreur du serveur ({statut}).', {'statut': statut});
    return ApiException(statut, message!, champs);
  }
}

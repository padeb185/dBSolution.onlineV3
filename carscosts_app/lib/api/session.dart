import 'package:flutter/foundation.dart';

import '../l10n/langue.dart';
import 'api_client.dart';

/// Session de l'utilisateur : connexion, inscription, déconnexion, suppression du compte.
class Session extends ChangeNotifier {
  Session(this.api, this.langue);

  final ApiClient api;
  final Langue langue;
  Map<String, dynamic>? utilisateur;
  bool pret = false;

  bool get connecte => api.connecte;

  Future<void> demarrer() async {
    await api.chargerJeton();
    if (api.connecte) {
      try {
        utilisateur = Map<String, dynamic>.from(await api.get('moi/') as Map);
        await _appliquerLangue();
      } on ApiException catch (e) {
        if (e.statut == 401) await api.enregistrerJeton(null);
      }
    }
    pret = true;
    notifyListeners();
  }

  Future<void> connexion(String email, String motDePasse) =>
      _ouvrir(api.post('auth/connexion/', {'email': email, 'password': motDePasse}));

  /// Inscription dans la langue choisie sur l'écran d'accueil.
  Future<void> inscription(String email, String motDePasse, String prenom, String nom) => _ouvrir(api.post(
      'auth/inscription/',
      {'email': email, 'password': motDePasse, 'prenom': prenom, 'nom': nom, 'langue': Langue.courante}));

  Future<void> _ouvrir(Future<dynamic> requete) async {
    final reponse = Map<String, dynamic>.from(await requete as Map);
    await api.enregistrerJeton(reponse['token'] as String);
    utilisateur = Map<String, dynamic>.from(reponse['utilisateur'] as Map);
    await _appliquerLangue();
    notifyListeners();
  }

  /// La langue du compte (choisie à l'inscription ou dans les réglages) s'applique sur cet appareil.
  Future<void> _appliquerLangue() async {
    final code = utilisateur?['langue'] as String?;
    if (code != null) await langue.choisir(code);
  }

  /// Profil et préférences (prénom, nom, téléphone, langue, pays par défaut).
  Future<void> modifierProfil(Map<String, dynamic> champs) async {
    utilisateur = Map<String, dynamic>.from(await api.patch('moi/', champs) as Map);
    await _appliquerLangue();
    notifyListeners();
  }

  /// Changement du mot de passe : le serveur renvoie un nouveau jeton (les autres appareils sont déconnectés).
  Future<void> changerMotDePasse(String ancien, String nouveau) async {
    final r = Map<String, dynamic>.from(await api.post('moi/mot-de-passe/', {'ancien': ancien, 'nouveau': nouveau}) as Map);
    await api.enregistrerJeton(r['token'] as String);
  }

  Future<void> changerEmail(String email, String motDePasse) async {
    utilisateur = Map<String, dynamic>.from(await api.post('moi/email/', {'email': email, 'password': motDePasse}) as Map);
    notifyListeners();
  }

  Future<void> deconnexion() async {
    try {
      await api.post('auth/deconnexion/');
    } catch (_) {}
    await api.enregistrerJeton(null);
    utilisateur = null;
    notifyListeners();
  }

  Future<void> supprimerCompte(String motDePasse) async {
    await api.delete('moi/', {'password': motDePasse});
    await api.enregistrerJeton(null);
    utilisateur = null;
    notifyListeners();
  }

  /// Appelé quand une requête renvoie 401 (jeton révoqué).
  void sessionExpiree() {
    utilisateur = null;
    notifyListeners();
  }
}

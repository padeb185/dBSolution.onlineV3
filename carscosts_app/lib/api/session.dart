import 'package:flutter/foundation.dart';

import 'api_client.dart';

/// Session de l'utilisateur : connexion, inscription, déconnexion, suppression du compte.
class Session extends ChangeNotifier {
  Session(this.api);

  final ApiClient api;
  Map<String, dynamic>? utilisateur;
  bool pret = false;

  bool get connecte => api.connecte;

  Future<void> demarrer() async {
    await api.chargerJeton();
    if (api.connecte) {
      try {
        utilisateur = Map<String, dynamic>.from(await api.get('moi/') as Map);
      } on ApiException catch (e) {
        if (e.statut == 401) await api.enregistrerJeton(null);
      }
    }
    pret = true;
    notifyListeners();
  }

  Future<void> connexion(String email, String motDePasse) =>
      _ouvrir(api.post('auth/connexion/', {'email': email, 'password': motDePasse}));

  Future<void> inscription(String email, String motDePasse, String prenom, String nom) => _ouvrir(api.post(
      'auth/inscription/', {'email': email, 'password': motDePasse, 'prenom': prenom, 'nom': nom}));

  Future<void> _ouvrir(Future<dynamic> requete) async {
    final reponse = Map<String, dynamic>.from(await requete as Map);
    await api.enregistrerJeton(reponse['token'] as String);
    utilisateur = Map<String, dynamic>.from(reponse['utilisateur'] as Map);
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

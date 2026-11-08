import 'dart:async';
import 'dart:io' show Platform;

import 'package:flutter/foundation.dart';
import 'package:in_app_purchase/in_app_purchase.dart';

import '../api/api_client.dart';
import '../l10n/langue.dart';

/// Formule du compte (Gratuit 1 véhicule · Bronze 2 · Silver 5 · Gold 10) et achats intégrés.
///
/// - L'état vient de l'API (`abonnement/`, aussi inclus dans `tableau-de-bord/` et `moi/`).
/// - Achat App Store / Google Play : la preuve d'achat est envoyée à `abonnement/achat/`, le serveur la
///   vérifie auprès d'Apple / Google ; la transaction n'est terminée (completePurchase) qu'après sa réponse.
/// - Serveur en mode « test » (développement) : bouton « Activer (test) » sans passer par un store.
class Abonnement extends ChangeNotifier {
  Abonnement(this.api);

  final ApiClient api;

  Map<String, dynamic>? etat;
  Map<String, ProductDetails> produitsStore = {};
  bool storeDisponible = false;
  bool enCours = false;
  String? message;
  StreamSubscription<List<PurchaseDetails>>? _flux;

  /// Achats intégrés disponibles : iOS, Android et macOS (pas Windows).
  static bool get plateformeStore => !kIsWeb && (Platform.isIOS || Platform.isAndroid || Platform.isMacOS);

  String get _plateforme => Platform.isAndroid ? 'google' : 'apple';

  String get formule => etat?['formule'] as String? ?? 'gratuit';
  String get libelle => libelleFormule(formule);

  /// Nom affiché d'une formule (Bronze, Silver, Gold sont des noms de marque, non traduits).
  static String libelleFormule(String? code) => switch (code) {
        'bronze' => 'Bronze',
        'silver' => 'Silver',
        'gold' => 'Gold',
        _ => t('Gratuit'),
      };

  /// Message « limite atteinte » (détail de l'erreur 403 limite_formule de l'API, sinon état connu).
  String messageLimite([Map<String, String> erreur = const {}]) => t(
        'Votre formule {formule} permet {n} véhicule(s) actif(s). '
        'Choisissez une formule supérieure, ou archivez un véhicule vendu.',
        {'formule': libelleFormule(erreur['formule'] ?? formule), 'n': int.tryParse(erreur['limite'] ?? '') ?? limite},
      );
  int get limite => (etat?['limite'] as num?)?.toInt() ?? 1;
  int get vehiculesActifs => (etat?['vehicules_actifs'] as num?)?.toInt() ?? 0;
  bool get peutAjouter => etat == null || etat!['peut_ajouter'] == true;
  bool get modeTest => etat?['mode_achats'] == 'test';
  List<Map<String, dynamic>> get formules =>
      [for (final f in (etat?['formules'] as List? ?? [])) Map<String, dynamic>.from(f as Map)];

  /// À appeler au démarrage : les achats en attente (renouvellement, achat interrompu) arrivent par ce flux.
  void demarrer() {
    if (!plateformeStore || _flux != null) return;
    _flux = InAppPurchase.instance.purchaseStream.listen(
      _achats,
      onError: (Object e) {
        enCours = false;
        message = t('Achat impossible : {erreur}', {'erreur': e});
        notifyListeners();
      },
    );
  }

  /// État reçu avec le tableau de bord.
  void mettreAJour(dynamic nouvelEtat) {
    if (nouvelEtat is Map) {
      etat = Map<String, dynamic>.from(nouvelEtat);
      notifyListeners();
    }
  }

  Future<void> charger() async {
    etat = Map<String, dynamic>.from(await api.get('abonnement/') as Map);
    await _chargerProduits();
    notifyListeners();
  }

  Future<void> _chargerProduits() async {
    if (!plateformeStore || produitsStore.isNotEmpty) return;
    try {
      storeDisponible = await InAppPurchase.instance.isAvailable();
      if (!storeDisponible) return;
      final ids = {for (final f in formules) ...(f['produits'] as List? ?? []).cast<String>()};
      if (ids.isEmpty) return;
      final reponse = await InAppPurchase.instance.queryProductDetails(ids);
      produitsStore = {for (final p in reponse.productDetails) p.id: p};
    } catch (e) {
      storeDisponible = false;
    }
  }

  /// Produit du store pour une formule (premier identifiant configuré et trouvé dans le store).
  ProductDetails? produitDe(Map<String, dynamic> formule) {
    for (final id in (formule['produits'] as List? ?? []).cast<String>()) {
      final p = produitsStore[id];
      if (p != null) return p;
    }
    return null;
  }

  Future<void> acheter(ProductDetails produit) async {
    message = null;
    enCours = true;
    notifyListeners();
    try {
      // Abonnement auto-renouvelable : buyNonConsumable est la méthode prévue par le plugin.
      final lance = await InAppPurchase.instance.buyNonConsumable(purchaseParam: PurchaseParam(productDetails: produit));
      if (!lance) enCours = false;
    } catch (e) {
      enCours = false;
      message = t('Achat impossible : {erreur}', {'erreur': e});
    }
    notifyListeners();
  }

  /// Développement uniquement (serveur en mode « test ») : formule attribuée 30 jours, sans store.
  Future<void> acheterTest(String produit) async {
    message = null;
    enCours = true;
    notifyListeners();
    try {
      etat = Map<String, dynamic>.from(
          await api.post('abonnement/achat/', {'plateforme': 'test', 'produit': produit, 'jeton': 'test'}) as Map);
      message = t('Formule {formule} activée (achat de test).', {'formule': libelle});
    } on ApiException catch (e) {
      message = e.message;
    } finally {
      enCours = false;
      notifyListeners();
    }
  }

  /// « Restaurer mes achats » (exigé par Apple) : les achats reviennent par le flux.
  Future<void> restaurer() async {
    message = null;
    try {
      await InAppPurchase.instance.restorePurchases();
      message = t('Restauration demandée au store.');
    } catch (e) {
      message = t('Restauration impossible : {erreur}', {'erreur': e});
    }
    notifyListeners();
  }

  Future<void> _achats(List<PurchaseDetails> achats) async {
    for (final achat in achats) {
      var terminer = true;
      switch (achat.status) {
        case PurchaseStatus.pending:
          enCours = true;
          terminer = false;
          break;
        case PurchaseStatus.purchased:
        case PurchaseStatus.restored:
          if (!api.connecte) {
            terminer = false; // renvoyé au prochain lancement, une fois connecté
            break;
          }
          try {
            etat = Map<String, dynamic>.from(await api.post('abonnement/achat/', {
              'plateforme': _plateforme,
              'produit': achat.productID,
              'jeton': achat.verificationData.serverVerificationData,
            }) as Map);
            message = t('Formule {formule} active.', {'formule': libelle});
          } on ApiException catch (e) {
            message = e.message;
            // Serveur injoignable (0) ou indisponible (5xx) : la transaction reste ouverte et sera renvoyée.
            terminer = e.statut >= 400 && e.statut < 500;
          }
          enCours = false;
          break;
        case PurchaseStatus.error:
          message = achat.error?.message ?? t('Achat impossible.');
          enCours = false;
          break;
        case PurchaseStatus.canceled:
          enCours = false;
          break;
      }
      if (terminer && achat.pendingCompletePurchase) {
        await InAppPurchase.instance.completePurchase(achat);
      }
    }
    notifyListeners();
  }

  @override
  void dispose() {
    _flux?.cancel();
    super.dispose();
  }
}

import 'package:carscosts_app/achats/abonnement.dart';
import 'package:carscosts_app/api/api_client.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('Sans état : formule gratuite, ajout autorisé (le serveur tranche)', () {
    final ab = Abonnement(ApiClient());
    expect(ab.formule, 'gratuit');
    expect(ab.limite, 1);
    expect(ab.peutAjouter, isTrue);
  });

  test('État du tableau de bord : limite atteinte', () {
    final ab = Abonnement(ApiClient())
      ..mettreAJour({
        'formule': 'bronze',
        'libelle': 'Bronze',
        'limite': 2,
        'vehicules_actifs': 2,
        'peut_ajouter': false,
        'mode_achats': 'test',
        'formules': [
          {'code': 'gratuit', 'libelle': 'Gratuit', 'limite': 1, 'produits': []},
          {'code': 'bronze', 'libelle': 'Bronze', 'limite': 2, 'produits': ['carscosts_bronze_mensuel']},
        ],
      });
    expect(ab.libelle, 'Bronze');
    expect(ab.peutAjouter, isFalse);
    expect(ab.modeTest, isTrue);
    expect(ab.formules.length, 2);
    expect(ab.produitDe(ab.formules[1]), isNull); // produits du store non chargés
  });
}

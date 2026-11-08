import 'package:carscosts_app/modeles/ressources.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  List<String> onglets(String energie) => [for (final r in ressourcesDe({'energie': energie})) r.chemin];

  test('Recharges à part : électrique sans pleins, hybride rechargeable avec les deux', () {
    expect(onglets('diesel'), isNot(contains('recharges')));
    expect(onglets('diesel'), contains('pleins'));
    expect(onglets('electrique'), isNot(contains('pleins')));
    expect(onglets('electrique'), contains('recharges'));
    expect(onglets('phev'), containsAll(['pleins', 'recharges']));
  });

  test('Carburant restant au-dessus du plein complet ; électricité absente des pleins', () {
    final noms = [for (final c in pleins.champs) c.nom];
    expect(noms.indexOf('niveau_restant'), noms.indexOf('plein_complet') - 1);
    expect(carburantsPlein.containsKey('electricite'), isFalse);
    expect(niveauxCarburant.keys, ['3/4', '1/2', '1/4', 'reserve', 'fin_reserve']);
    expect(niveauxBatterie.keys, ['3/4', '1/2', '1/4', 'minimum']);
    final champsRecharge = [for (final c in recharges.champs) c.nom];
    expect(champsRecharge, isNot(contains('batterie_debut')));
    expect(champsRecharge.indexOf('niveau_restant'), champsRecharge.indexOf('plein_complet') - 1);
  });
}

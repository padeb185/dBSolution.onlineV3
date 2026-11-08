import 'package:carscosts_app/l10n/langue.dart';
import 'package:carscosts_app/widgets/champ_pays.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  tearDown(() => Langue.courante = 'fr');

  test('« L » : pays commençant par L ; « Lu » : Luxembourg', () {
    Langue.courante = 'fr';
    final l = rechercherPays('L');
    expect(l, containsAll(['LU', 'LV', 'LT', 'LB']));
    expect(rechercherPays('lu'), ['LU']);
    expect(rechercherPays('LU'), contains('LU'));
  });

  test('Sans accents et dans la langue choisie', () {
    Langue.courante = 'fr';
    expect(rechercherPays('equa'), contains('EC')); // Équateur
    Langue.courante = 'de';
    expect(rechercherPays('Lux'), ['LU']);
    expect(rechercherPays('belg'), ['BE']); // Belgien
  });
}

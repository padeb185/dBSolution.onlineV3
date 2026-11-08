import 'package:carscosts_app/modeles/catalogue.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  setUp(() => Catalogue.marques = Catalogue.lire({
        'Peugeot': {
          '208': [
            ['1.2 PureTech', 75, 'essence'],
            ['1.2 PureTech', 100, 'essence'],
            ['e-208', 156, 'electrique'],
          ],
          '308': [],
          '3008': [],
        },
        'Mercedes-Benz': {'Classe A': [], 'Classe GLC': [], 'EQA': []},
        'Citroën': ['C3', 'C4'], // ancien format (modèles sans versions)
        'Cupra': {'Born': [], 'Formentor': []},
      }));

  test('Marques selon les premières lettres', () {
    expect(Catalogue.suggestionsMarques('c'), ['Citroën', 'Cupra']);
    expect(Catalogue.suggestionsMarques('ci'), ['Citroën']);
    expect(Catalogue.suggestionsMarques('benz'), ['Mercedes-Benz']);
  });

  test('Modèles de la marque saisie', () {
    expect(Catalogue.suggestionsModeles('peugeot', '30'), ['308', '3008']);
    expect(Catalogue.suggestionsModeles('Mercedes-Benz', 'glc'), ['Classe GLC']);
    expect(Catalogue.suggestionsModeles('citroen', ''), ['C3', 'C4']);
  });

  test('Versions du modèle avec puissance et énergie', () {
    final v = Catalogue.suggestionsVersions('Peugeot', '208', '');
    expect(v.map((m) => m.libelle), ['1.2 PureTech · 75 ch', '1.2 PureTech · 100 ch', 'e-208 · 156 ch']);
    expect(Catalogue.suggestionsVersions('Peugeot', '208', 'e-').single.energie, 'electrique');
    expect(Catalogue.suggestionsVersions('Peugeot', '208', '100').single.ch, 100);
  });
}

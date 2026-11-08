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
        'Volkswagen': {
          'Golf I': [
            ['1.1', 50, 'essence', '1974-1983'],
            ['1.6 GTI', 110, 'essence', '1976-1983'],
          ],
          'Golf': [
            ['1.5 eTSI', 150, 'essence'],
            ['1.5 eHybrid', 204, 'phev', '2020-'],
          ],
        },
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

  test('Modèles depuis les années 70 : période dans le libellé et filtre par année', () {
    expect(Catalogue.suggestionsModeles('volkswagen', 'golf i'), contains('Golf I'));
    final gti = Catalogue.suggestionsVersions('Volkswagen', 'Golf I', 'gti').single;
    expect(gti.libelle, '1.6 GTI · 110 ch · 1976–1983');
    expect(Catalogue.suggestionsVersions('Volkswagen', 'Golf I', '', annee: 1975).map((m) => m.version), ['1.1']);
    expect(Catalogue.suggestionsVersions('Volkswagen', 'Golf', '', annee: 2024).length, 2); // sans période + 2020-
    expect(Catalogue.suggestionsVersions('Volkswagen', 'Golf', '', annee: 2018).map((m) => m.version), ['1.5 eTSI']);
  });
}

import 'package:carscosts_app/modeles/catalogue.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  setUp(() => Catalogue.marques = {
        'Peugeot': ['208', '2008', '308', '3008'],
        'Mercedes-Benz': ['Classe A', 'Classe GLC', 'EQA'],
        'Citroën': ['C3', 'C4'],
        'Cupra': ['Born', 'Formentor'],
      });

  test('Marques selon les premières lettres', () {
    expect(Catalogue.suggestionsMarques('c'), ['Citroën', 'Cupra']);
    expect(Catalogue.suggestionsMarques('ci'), ['Citroën']);
    expect(Catalogue.suggestionsMarques('benz'), ['Mercedes-Benz']); // début d'un mot
  });

  test('Modèles de la marque saisie', () {
    expect(Catalogue.suggestionsModeles('peugeot', '30'), ['308', '3008']);
    expect(Catalogue.suggestionsModeles('Mercedes-Benz', 'glc'), ['Classe GLC']);
    expect(Catalogue.suggestionsModeles('citroen', ''), ['C3', 'C4']);
    expect(Catalogue.suggestionsModeles('Inconnue', ''), isEmpty);
  });
}

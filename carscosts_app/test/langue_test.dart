import 'package:carscosts_app/l10n/langue.dart';
import 'package:carscosts_app/l10n/traductions.dart';
import 'package:carscosts_app/modeles/pays.dart';
import 'package:carscosts_app/modeles/ressources.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  tearDown(() => Langue.courante = 'fr');

  test('Français par défaut, paramètres remplacés', () {
    Langue.courante = 'fr';
    expect(t('Bonjour {prenom}', {'prenom': 'Anne'}), 'Bonjour Anne');
  });

  test('Traduction et repli sur le français pour un texte inconnu', () {
    Langue.courante = 'nl';
    expect(t('Bonjour {prenom}', {'prenom': 'Anne'}), 'Hallo Anne');
    expect(t('Texte absent de la table'), 'Texte absent de la table');
  });

  test('Chaque langue traduit les mêmes textes', () {
    final cles = traductions['en']!.keys.toSet();
    for (final langue in languesApp.keys.where((l) => l != 'fr')) {
      expect(traductions[langue]!.keys.toSet(), cles, reason: langue);
    }
  });

  test('Libellés des formulaires et noms de pays dans la langue choisie', () {
    Langue.courante = 'de';
    expect(pleins.titre, 'Tankfüllungen');
    expect(energies['electrique'], 'Elektrisch');
    expect(paysImmatriculation['BE'], 'Belgien');
    expect(paysImmatriculation.length, 250);
  });
}

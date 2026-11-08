import 'package:carscosts_app/modeles/pays.dart';
import 'package:carscosts_app/widgets/plaque.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Plaque belge : texte rouge foncé, bande UE avec « B »', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: Scaffold(body: Plaque(numero: '1-abc-123', pays: 'BE'))));
    final numero = tester.widget<Text>(find.text('1-ABC-123'));
    expect(numero.style?.color, const Color(0xFF8B0000));
    expect(find.text('B'), findsOneWidget);
  });

  testWidgets('Plaque suisse : écusson sans bande ; autre pays : plaque par défaut avec le code ISO', (tester) async {
    await tester.pumpWidget(const MaterialApp(
        home: Scaffold(body: Column(children: [Plaque(numero: 'VD 123456', pays: 'CH'), Plaque(numero: 'AB-123', pays: 'CI')]))));
    expect(find.text('CH'), findsNothing);
    expect(find.text('VD 123456'), findsOneWidget);
    expect(find.text('CI'), findsOneWidget);
    expect(stylePlaque('CI').nom, 'Côte d’Ivoire');
  });

  test('Tous les pays stylés font partie de la liste complète', () {
    for (final code in stylesPlaque.keys) {
      expect(paysImmatriculation.containsKey(code), isTrue, reason: code);
    }
    expect(paysImmatriculation.length, 250);
  });
}

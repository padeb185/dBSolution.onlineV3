import 'package:carscosts_app/api/api_client.dart';
import 'package:carscosts_app/api/session.dart';
import 'package:carscosts_app/ecrans/connexion_ecran.dart';
import 'package:carscosts_app/l10n/langue.dart';
import 'package:carscosts_app/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

Widget _avecSession(Widget enfant, Session session) => MultiProvider(
      providers: [
        Provider<ApiClient>.value(value: session.api),
        ChangeNotifierProvider<Langue>.value(value: session.langue),
        ChangeNotifierProvider<Session>.value(value: session),
      ],
      child: enfant,
    );

void main() {
  testWidgets('Au démarrage, attente de la session', (tester) async {
    await tester.pumpWidget(_avecSession(const CarsCostsApp(), Session(ApiClient(), Langue())));
    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });

  testWidgets('Écran de connexion : bascule vers l\'inscription', (tester) async {
    await tester.pumpWidget(_avecSession(const MaterialApp(home: ConnexionEcran()), Session(ApiClient(), Langue())));
    expect(find.text('Se connecter'), findsOneWidget);
    await tester.tap(find.text('Créer un compte'));
    await tester.pump();
    expect(find.text('Créer mon compte'), findsOneWidget);
    expect(find.text('Prénom'), findsOneWidget);
  });
}

import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:provider/provider.dart';

import 'achats/abonnement.dart';
import 'api/api_client.dart';
import 'api/session.dart';
import 'ecrans/accueil_ecran.dart';
import 'ecrans/connexion_ecran.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeDateFormatting('fr_BE');
  final api = ApiClient();
  final session = Session(api);
  final abonnement = Abonnement(api)..demarrer();
  runApp(
    MultiProvider(
      providers: [
        Provider<ApiClient>.value(value: api),
        ChangeNotifierProvider<Session>.value(value: session),
        ChangeNotifierProvider<Abonnement>.value(value: abonnement),
      ],
      child: const CarsCostsApp(),
    ),
  );
  await session.demarrer();
}

class CarsCostsApp extends StatelessWidget {
  const CarsCostsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CarsCosts',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(colorSchemeSeed: const Color(0xFF1E3A8A), useMaterial3: true),
      darkTheme: ThemeData(colorSchemeSeed: const Color(0xFF1E3A8A), brightness: Brightness.dark, useMaterial3: true),
      locale: const Locale('fr', 'BE'),
      supportedLocales: const [Locale('fr', 'BE'), Locale('fr'), Locale('en'), Locale('nl'), Locale('de')],
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      home: const Racine(),
    );
  }
}

/// Écran de connexion ou accueil selon la session.
class Racine extends StatelessWidget {
  const Racine({super.key});

  @override
  Widget build(BuildContext context) {
    final session = context.watch<Session>();
    if (!session.pret) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    return session.connecte ? const AccueilEcran() : const ConnexionEcran();
  }
}

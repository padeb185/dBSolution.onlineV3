import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:provider/provider.dart';

import 'achats/abonnement.dart';
import 'api/api_client.dart';
import 'api/session.dart';
import 'ecrans/accueil_ecran.dart';
import 'ecrans/connexion_ecran.dart';
import 'l10n/langue.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeDateFormatting(); // formats de date de toutes les langues
  final langue = Langue();
  await langue.charger();
  final api = ApiClient();
  final session = Session(api, langue);
  final abonnement = Abonnement(api)..demarrer();
  runApp(
    MultiProvider(
      providers: [
        Provider<ApiClient>.value(value: api),
        ChangeNotifierProvider<Langue>.value(value: langue),
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

  static const _locales = {
    'fr': Locale('fr', 'BE'),
    'nl': Locale('nl', 'BE'),
    'en': Locale('en', 'GB'),
    'de': Locale('de'),
    'es': Locale('es'),
    'it': Locale('it'),
    'el': Locale('el'),
  };

  @override
  Widget build(BuildContext context) {
    // Changement de langue : l'application est reconstruite entièrement (tous les textes passent par t()).
    final langue = context.watch<Langue>();
    final code = langue.code;
    return MaterialApp(
      key: ValueKey(langue.cle),
      title: 'CarsCosts',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(colorSchemeSeed: const Color(0xFF1E3A8A), useMaterial3: true),
      darkTheme: ThemeData(colorSchemeSeed: const Color(0xFF1E3A8A), brightness: Brightness.dark, useMaterial3: true),
      locale: _locales[code],
      supportedLocales: _locales.values,
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

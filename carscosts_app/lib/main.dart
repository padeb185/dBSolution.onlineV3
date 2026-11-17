import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:provider/provider.dart';

import 'achats/abonnement.dart';
import 'achats/notifications_push.dart';
import 'api/api_client.dart';
import 'api/biometrie.dart';
import 'api/session.dart';
import 'ecrans/accueil_ecran.dart';
import 'ecrans/connexion_ecran.dart';
import 'ecrans/verrou_ecran.dart';
import 'l10n/langue.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeDateFormatting(); // formats de date de toutes les langues
  final langue = Langue();
  await langue.charger();
  final api = ApiClient();
  final biometrie = Biometrie();
  await biometrie.charger();
  final session = Session(api, langue)..biometrie = biometrie;
  final abonnement = Abonnement(api)..demarrer();
  // Push : un message reçu (paiement refusé, renouvellement…) recharge l'état de l'abonnement
  session.push = NotificationsPush(api, auMessage: () {
    if (api.connecte) abonnement.charger().catchError((_) {});
  });
  runApp(
    MultiProvider(
      providers: [
        Provider<ApiClient>.value(value: api),
        ChangeNotifierProvider<Langue>.value(value: langue),
        ChangeNotifierProvider<Session>.value(value: session),
        ChangeNotifierProvider<Biometrie>.value(value: biometrie),
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

/// Écran de connexion, de déverrouillage ou accueil selon la session.
class Racine extends StatefulWidget {
  const Racine({super.key});

  @override
  State<Racine> createState() => _RacineState();
}

class _RacineState extends State<Racine> with WidgetsBindingObserver {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  /// Retour après un moment en arrière-plan : verrouillage
  @override
  void didChangeAppLifecycleState(AppLifecycleState etat) {
    final biometrie = context.read<Biometrie>();
    if (etat == AppLifecycleState.paused || etat == AppLifecycleState.hidden) biometrie.arrierePlan();
    if (etat == AppLifecycleState.resumed) biometrie.premierPlan(context.read<Session>().connecte);
  }

  /// Après une connexion par mot de passe : proposer Face ID / empreinte (une seule fois)
  Future<void> _proposerBiometrie() async {
    final session = context.read<Session>();
    final biometrie = context.read<Biometrie>();
    session.connexionParMotDePasse = false;
    if (!biometrie.disponible || biometrie.active || biometrie.proposee) return;
    await biometrie.marquerProposee();
    if (!mounted) return;
    final oui = await showDialog<bool>(
      context: context,
      builder: (c) => AlertDialog(
        icon: Icon(biometrie.methode == 'Face ID' ? Icons.face : Icons.fingerprint),
        title: Text(t('Activer {methode} ?', {'methode': biometrie.methode})),
        content: Text(t('La prochaine fois, ouvrez CarsCosts avec {methode} au lieu du mot de passe.',
            {'methode': biometrie.methode})),
        actions: [
          TextButton(onPressed: () => Navigator.pop(c, false), child: Text(t('Plus tard'))),
          FilledButton(onPressed: () => Navigator.pop(c, true), child: Text(t('Activer'))),
        ],
      ),
    );
    if (oui == true) await biometrie.activer(true);
  }

  @override
  Widget build(BuildContext context) {
    final session = context.watch<Session>();
    final biometrie = context.watch<Biometrie>();
    if (!session.pret) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    if (!session.connecte) return const ConnexionEcran();
    if (biometrie.verrouille) return const VerrouEcran();
    if (session.connexionParMotDePasse) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted && session.connexionParMotDePasse) _proposerBiometrie();
      });
    }
    return const AccueilEcran();
  }
}

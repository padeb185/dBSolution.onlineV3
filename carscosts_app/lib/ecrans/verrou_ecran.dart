import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../api/biometrie.dart';
import '../api/session.dart';
import '../l10n/langue.dart';

/// Application verrouillée : déverrouillage biométrique, ou retour à la connexion par mot de passe.
class VerrouEcran extends StatefulWidget {
  const VerrouEcran({super.key});

  @override
  State<VerrouEcran> createState() => _VerrouEcranState();
}

class _VerrouEcranState extends State<VerrouEcran> {
  @override
  void initState() {
    super.initState();
    // Demande immédiate à l'ouverture
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) context.read<Biometrie>().deverrouiller();
    });
  }

  @override
  Widget build(BuildContext context) {
    final biometrie = context.watch<Biometrie>();
    final theme = Theme.of(context);
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.lock_outline, size: 64, color: theme.colorScheme.primary),
                const SizedBox(height: 16),
                Text('CarsCosts', style: theme.textTheme.headlineSmall),
                const SizedBox(height: 32),
                FilledButton.icon(
                  icon: Icon(biometrie.methode == 'Face ID' ? Icons.face : Icons.fingerprint),
                  label: Text(t('Déverrouiller avec {methode}', {'methode': biometrie.methode})),
                  onPressed: biometrie.deverrouiller,
                ),
                const SizedBox(height: 12),
                TextButton(
                  child: Text(t('Utiliser le mot de passe')),
                  onPressed: () => context.read<Session>().deconnexion(),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

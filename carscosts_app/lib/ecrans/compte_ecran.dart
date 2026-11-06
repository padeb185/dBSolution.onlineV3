import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../api/api_client.dart';
import '../api/session.dart';
import '../config.dart';

/// Mon compte : déconnexion et suppression définitive du compte (obligatoire sur l'App Store).
class CompteEcran extends StatelessWidget {
  const CompteEcran({super.key});

  Future<void> _supprimer(BuildContext context) async {
    final session = context.read<Session>();
    final mdp = TextEditingController();
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Supprimer mon compte'),
        content: Column(mainAxisSize: MainAxisSize.min, children: [
          const Text('Votre compte, vos véhicules et tous leurs documents seront définitivement supprimés.'),
          const SizedBox(height: 12),
          TextField(controller: mdp, obscureText: true, decoration: const InputDecoration(labelText: 'Mot de passe')),
        ]),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Annuler')),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: Colors.red),
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Supprimer définitivement'),
          ),
        ],
      ),
    );
    if (ok != true) return;
    try {
      await session.supprimerCompte(mdp.text);
      if (context.mounted) Navigator.popUntil(context, (r) => r.isFirst);
    } on ApiException catch (e) {
      if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    }
  }

  @override
  Widget build(BuildContext context) {
    final session = context.watch<Session>();
    final u = session.utilisateur ?? {};
    return Scaffold(
      appBar: AppBar(title: const Text('Mon compte')),
      body: ListView(
        children: [
          ListTile(
            leading: const Icon(Icons.person),
            title: Text('${u['prenom'] ?? ''} ${u['nom'] ?? ''}'),
            subtitle: Text('${u['email'] ?? ''}'),
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.logout),
            title: const Text('Se déconnecter'),
            onTap: () async {
              await session.deconnexion();
              if (context.mounted) Navigator.popUntil(context, (r) => r.isFirst);
            },
          ),
          ListTile(
            leading: const Icon(Icons.delete_forever, color: Colors.red),
            title: const Text('Supprimer mon compte', style: TextStyle(color: Colors.red)),
            onTap: () => _supprimer(context),
          ),
          const Divider(),
          ListTile(dense: true, title: const Text('Serveur'), subtitle: Text(apiUrl)),
        ],
      ),
    );
  }
}

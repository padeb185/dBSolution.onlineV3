import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../api/api_client.dart';
import '../api/session.dart';
import '../l10n/langue.dart';
import '../l10n/unites.dart';
import '../modeles/pays.dart';
import '../widgets/champ_pays.dart';
import 'formules_ecran.dart';

/// Réglages : profil, email, mot de passe, langue, pays par défaut, formule, déconnexion, suppression du compte.
class ReglagesEcran extends StatelessWidget {
  const ReglagesEcran({super.key});

  void _message(BuildContext context, String texte) =>
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(texte)));

  // ------------------------------------------------------------------ Profil
  Future<void> _profil(BuildContext context) async {
    final session = context.read<Session>();
    final u = session.utilisateur ?? {};
    final prenom = TextEditingController(text: '${u['prenom'] ?? ''}');
    final nom = TextEditingController(text: '${u['nom'] ?? ''}');
    final telephone = TextEditingController(text: '${u['telephone'] ?? ''}');
    final ok = await _dialogue(context, t('Profil'), [
      TextField(controller: prenom, decoration: InputDecoration(labelText: t('Prénom'))),
      TextField(controller: nom, decoration: InputDecoration(labelText: t('Nom'))),
      TextField(
        controller: telephone,
        keyboardType: TextInputType.phone,
        decoration: InputDecoration(labelText: t('Téléphone')),
      ),
    ]);
    if (ok != true || !context.mounted) return;
    await _executer(context, () => session.modifierProfil({
          'prenom': prenom.text.trim(),
          'nom': nom.text.trim(),
          'telephone': telephone.text.trim(),
        }), t('Profil enregistré.'));
  }

  // ------------------------------------------------------------------ Email
  Future<void> _email(BuildContext context) async {
    final session = context.read<Session>();
    final email = TextEditingController(text: '${session.utilisateur?['email'] ?? ''}');
    final mdp = TextEditingController();
    final ok = await _dialogue(context, t('Changer d\'email'), [
      TextField(
        controller: email,
        keyboardType: TextInputType.emailAddress,
        decoration: InputDecoration(labelText: t('Nouvel email')),
      ),
      TextField(controller: mdp, obscureText: true, decoration: InputDecoration(labelText: t('Mot de passe actuel'))),
    ]);
    if (ok != true || !context.mounted) return;
    await _executer(context, () => session.changerEmail(email.text.trim(), mdp.text), t('Email modifié.'));
  }

  // ------------------------------------------------------------------ Mot de passe
  Future<void> _motDePasse(BuildContext context) async {
    final session = context.read<Session>();
    final ancien = TextEditingController();
    final nouveau = TextEditingController();
    final confirmation = TextEditingController();
    final ok = await _dialogue(context, t('Changer le mot de passe'), [
      TextField(controller: ancien, obscureText: true, decoration: InputDecoration(labelText: t('Mot de passe actuel'))),
      TextField(
        controller: nouveau,
        obscureText: true,
        decoration: InputDecoration(
          labelText: t('Nouveau mot de passe'),
          helperText: t('Au moins 12 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.'),
          helperMaxLines: 3,
        ),
      ),
      TextField(
        controller: confirmation,
        obscureText: true,
        decoration: InputDecoration(labelText: t('Confirmer le nouveau mot de passe')),
      ),
    ]);
    if (ok != true || !context.mounted) return;
    if (nouveau.text != confirmation.text) {
      _message(context, t('Les deux mots de passe ne correspondent pas.'));
      return;
    }
    await _executer(context, () => session.changerMotDePasse(ancien.text, nouveau.text),
        t('Mot de passe modifié. Vos autres appareils sont déconnectés.'));
  }

  // ------------------------------------------------------------------ Langue et pays
  Future<void> _langue(BuildContext context) async {
    final session = context.read<Session>();
    final code = await showDialog<String>(
      context: context,
      builder: (ctx) => SimpleDialog(
        title: Text(t('Langue')),
        children: [
          for (final e in languesApp.entries)
            ListTile(
              title: Text(e.value),
              trailing: e.key == Langue.courante ? const Icon(Icons.check) : null,
              onTap: () => Navigator.pop(ctx, e.key),
            ),
        ],
      ),
    );
    if (code == null || code == Langue.courante || !context.mounted) return;
    // Enregistrée dans le compte ; l'application se recharge dans la nouvelle langue.
    await _executer(context, () => session.modifierProfil({'langue': code}), null);
  }

  Future<void> _pays(BuildContext context) async {
    final session = context.read<Session>();
    final actuel = '${session.utilisateur?['pays_defaut'] ?? 'BE'}';
    final code = await showDialog<String>(
      context: context,
      builder: (ctx) => _ChoixPays(actuel: actuel),
    );
    if (code == null || code == actuel || !context.mounted) return;
    await _executer(context, () => session.modifierProfil({'pays_defaut': code}), t('Pays par défaut enregistré.'));
  }

  // ------------------------------------------------------------------ Unités
  static Map<String, String> get _distances => {'km': t('Kilomètres'), 'mi': t('Miles')};
  static Map<String, String> get _volumes =>
      {'L': t('Litres'), 'gal_us': t('Gallons US'), 'gal_uk': t('Gallons impériaux (UK)')};

  Future<void> _unite(BuildContext context, String champ, String titre, Map<String, String> choix, String actuel) async {
    final session = context.read<Session>();
    final code = await showDialog<String>(
      context: context,
      builder: (ctx) => SimpleDialog(
        title: Text(titre),
        children: [
          for (final e in choix.entries)
            ListTile(
              title: Text(e.value),
              trailing: e.key == actuel ? const Icon(Icons.check) : null,
              onTap: () => Navigator.pop(ctx, e.key),
            ),
        ],
      ),
    );
    if (code == null || code == actuel || !context.mounted) return;
    await _executer(context, () => session.modifierProfil({champ: code}), null);
  }

  // ------------------------------------------------------------------ Compte
  Future<void> _supprimer(BuildContext context) async {
    final session = context.read<Session>();
    final mdp = TextEditingController();
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(t('Supprimer mon compte')),
        content: Column(mainAxisSize: MainAxisSize.min, children: [
          Text(t('Votre compte, vos véhicules et tous leurs documents seront définitivement supprimés.')),
          const SizedBox(height: 12),
          TextField(controller: mdp, obscureText: true, decoration: InputDecoration(labelText: t('Mot de passe'))),
        ]),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: Text(t('Annuler'))),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: Colors.red),
            onPressed: () => Navigator.pop(ctx, true),
            child: Text(t('Supprimer définitivement')),
          ),
        ],
      ),
    );
    if (ok != true || !context.mounted) return;
    try {
      await session.supprimerCompte(mdp.text);
      if (context.mounted) Navigator.popUntil(context, (r) => r.isFirst);
    } on ApiException catch (e) {
      if (context.mounted) _message(context, e.message);
    }
  }

  // ------------------------------------------------------------------ Outils
  Future<bool?> _dialogue(BuildContext context, String titre, List<Widget> champs) => showDialog<bool>(
        context: context,
        builder: (ctx) => AlertDialog(
          title: Text(titre),
          content: SingleChildScrollView(child: Column(mainAxisSize: MainAxisSize.min, children: champs)),
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx, false), child: Text(t('Annuler'))),
            FilledButton(onPressed: () => Navigator.pop(ctx, true), child: Text(t('Enregistrer'))),
          ],
        ),
      );

  Future<void> _executer(BuildContext context, Future<void> Function() action, String? succes) async {
    final messager = ScaffoldMessenger.of(context);
    try {
      await action();
      if (succes != null) messager.showSnackBar(SnackBar(content: Text(succes)));
    } on ApiException catch (e) {
      final detail = e.champs.values.isEmpty ? e.message : e.champs.values.join('\n');
      messager.showSnackBar(SnackBar(content: Text(detail)));
    }
  }

  Widget _titre(BuildContext context, String texte) => Padding(
        padding: const EdgeInsets.fromLTRB(16, 20, 16, 4),
        child: Text(texte,
            style: Theme.of(context).textTheme.titleSmall?.copyWith(color: Theme.of(context).colorScheme.primary)),
      );

  @override
  Widget build(BuildContext context) {
    final session = context.watch<Session>();
    final abonnement = context.watch<Abonnement>();
    final u = session.utilisateur ?? {};
    final pays = '${u['pays_defaut'] ?? 'BE'}';
    return Scaffold(
      appBar: AppBar(title: Text(t('Réglages'))),
      body: ListView(
        children: [
          _titre(context, t('Compte')),
          ListTile(
            leading: const Icon(Icons.person),
            title: Text('${u['prenom'] ?? ''} ${u['nom'] ?? ''}'.trim()),
            subtitle: Text(t('Profil : prénom, nom, téléphone')),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _profil(context),
          ),
          ListTile(
            leading: const Icon(Icons.email),
            title: Text(t('Email')),
            subtitle: Text('${u['email'] ?? ''}'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _email(context),
          ),
          ListTile(
            leading: const Icon(Icons.lock),
            title: Text(t('Mot de passe')),
            subtitle: Text(t('Changer le mot de passe')),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _motDePasse(context),
          ),
          _titre(context, t('Préférences')),
          ListTile(
            leading: const Icon(Icons.language),
            title: Text(t('Langue')),
            subtitle: Text(languesApp[Langue.courante] ?? ''),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _langue(context),
          ),
          ListTile(
            leading: const Icon(Icons.flag),
            title: Text(t('Pays d\'immatriculation par défaut')),
            subtitle: Text(paysImmatriculation[pays] ?? pays),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _pays(context),
          ),
          ListTile(
            leading: const Icon(Icons.straighten),
            title: Text(t('Distances')),
            subtitle: Text(_distances[Unites.compte.distance] ?? ''),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _unite(context, 'unite_distance', t('Distances'), _distances, Unites.compte.distance),
          ),
          ListTile(
            leading: const Icon(Icons.local_gas_station),
            title: Text(t('Volumes de carburant')),
            subtitle: Text(_volumes[Unites.compte.volume] ?? ''),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _unite(context, 'unite_volume', t('Volumes de carburant'), _volumes, Unites.compte.volume),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Text(t('Modifiables pour chaque véhicule (fiche du véhicule).'),
                style: Theme.of(context).textTheme.bodySmall),
          ),
          _titre(context, t('Formule')),
          ListTile(
            leading: const Icon(Icons.workspace_premium),
            title: Text(t('Formule {formule}', {'formule': abonnement.libelle})),
            subtitle: Text(t('Gratuit 1 véhicule · Bronze 2 · Silver 5 · Gold 10')),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const FormulesEcran())),
          ),
          const Divider(height: 32),
          ListTile(
            leading: const Icon(Icons.logout),
            title: Text(t('Se déconnecter')),
            onTap: () async {
              await session.deconnexion();
              if (context.mounted) Navigator.popUntil(context, (r) => r.isFirst);
            },
          ),
          ListTile(
            leading: const Icon(Icons.delete_forever, color: Colors.red),
            title: Text(t('Supprimer mon compte'), style: const TextStyle(color: Colors.red)),
            onTap: () => _supprimer(context),
          ),
        ],
      ),
    );
  }
}

/// Choix d'un pays (liste complète) avec recherche.
class _ChoixPays extends StatefulWidget {
  const _ChoixPays({required this.actuel});

  final String actuel;

  @override
  State<_ChoixPays> createState() => _ChoixPaysState();
}

class _ChoixPaysState extends State<_ChoixPays> {
  String _filtre = '';

  @override
  Widget build(BuildContext context) {
    // Même recherche que la saisie d'un pays : « L » → pays commençant par L, « Lu » → Luxembourg
    final liste = [for (final code in rechercherPays(_filtre)) MapEntry(code, paysImmatriculation[code] ?? code)];
    return AlertDialog(
      title: Text(t('Pays d\'immatriculation par défaut')),
      contentPadding: const EdgeInsets.fromLTRB(16, 12, 16, 0),
      content: SizedBox(
        width: 400,
        height: 460,
        child: Column(children: [
          TextField(
            autofocus: true,
            decoration: InputDecoration(prefixIcon: const Icon(Icons.search), hintText: t('Tapez les premières lettres')),
            onChanged: (v) => setState(() => _filtre = v.trim()),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: liste.length,
              itemBuilder: (context, i) => ListTile(
                dense: true,
                title: Text(liste[i].value),
                trailing: liste[i].key == widget.actuel ? const Icon(Icons.check) : null,
                onTap: () => Navigator.pop(context, liste[i].key),
              ),
            ),
          ),
        ]),
      ),
      actions: [TextButton(onPressed: () => Navigator.pop(context), child: Text(t('Annuler')))],
    );
  }
}

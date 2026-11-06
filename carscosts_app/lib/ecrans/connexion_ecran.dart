import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../api/api_client.dart';
import '../api/session.dart';

/// Connexion ou création d'un compte particulier.
class ConnexionEcran extends StatefulWidget {
  const ConnexionEcran({super.key});

  @override
  State<ConnexionEcran> createState() => _ConnexionEcranState();
}

class _ConnexionEcranState extends State<ConnexionEcran> {
  final _cle = GlobalKey<FormState>();
  final _email = TextEditingController();
  final _motDePasse = TextEditingController();
  final _prenom = TextEditingController();
  final _nom = TextEditingController();
  bool _inscription = false;
  bool _envoi = false;
  bool _masque = true;
  Map<String, String> _erreurs = {};

  @override
  void dispose() {
    for (final c in [_email, _motDePasse, _prenom, _nom]) {
      c.dispose();
    }
    super.dispose();
  }

  Future<void> _valider() async {
    if (!_cle.currentState!.validate()) return;
    final session = context.read<Session>();
    setState(() {
      _envoi = true;
      _erreurs = {};
    });
    try {
      if (_inscription) {
        await session.inscription(_email.text.trim(), _motDePasse.text, _prenom.text.trim(), _nom.text.trim());
      } else {
        await session.connexion(_email.text.trim(), _motDePasse.text);
      }
    } on ApiException catch (e) {
      if (!mounted) return;
      setState(() => _erreurs = e.champs);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    } finally {
      if (mounted) setState(() => _envoi = false);
    }
  }

  String? _obligatoire(String? v) => v == null || v.trim().isEmpty ? 'Champ obligatoire' : null;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 420),
            child: Form(
              key: _cle,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Icon(Icons.directions_car_filled, size: 64, color: theme.colorScheme.primary),
                  const SizedBox(height: 8),
                  Text('CarsCosts', textAlign: TextAlign.center, style: theme.textTheme.headlineMedium),
                  Text('Le suivi de vos véhicules', textAlign: TextAlign.center, style: theme.textTheme.bodyMedium),
                  const SizedBox(height: 32),
                  if (_inscription) ...[
                    TextFormField(
                      controller: _prenom,
                      decoration: InputDecoration(labelText: 'Prénom', errorText: _erreurs['prenom']),
                      validator: _obligatoire,
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: _nom,
                      decoration: InputDecoration(labelText: 'Nom', errorText: _erreurs['nom']),
                      validator: _obligatoire,
                    ),
                    const SizedBox(height: 12),
                  ],
                  TextFormField(
                    controller: _email,
                    keyboardType: TextInputType.emailAddress,
                    autofillHints: const [AutofillHints.email],
                    decoration: InputDecoration(labelText: 'Email', errorText: _erreurs['email']),
                    validator: _obligatoire,
                  ),
                  const SizedBox(height: 12),
                  TextFormField(
                    controller: _motDePasse,
                    obscureText: _masque,
                    autofillHints: [_inscription ? AutofillHints.newPassword : AutofillHints.password],
                    decoration: InputDecoration(
                      labelText: 'Mot de passe',
                      errorText: _erreurs['password'],
                      helperText: _inscription
                          ? 'Au moins 12 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.'
                          : null,
                      helperMaxLines: 2,
                      suffixIcon: IconButton(
                        icon: Icon(_masque ? Icons.visibility : Icons.visibility_off),
                        onPressed: () => setState(() => _masque = !_masque),
                      ),
                    ),
                    validator: _obligatoire,
                    onFieldSubmitted: (_) => _valider(),
                  ),
                  const SizedBox(height: 24),
                  FilledButton(
                    onPressed: _envoi ? null : _valider,
                    child: _envoi
                        ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2))
                        : Text(_inscription ? 'Créer mon compte' : 'Se connecter'),
                  ),
                  const SizedBox(height: 8),
                  TextButton(
                    onPressed: () => setState(() {
                      _inscription = !_inscription;
                      _erreurs = {};
                    }),
                    child: Text(_inscription ? 'J\'ai déjà un compte' : 'Créer un compte'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

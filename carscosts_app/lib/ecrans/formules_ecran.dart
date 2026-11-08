import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../widgets/format.dart';

/// Formules : Gratuit (1 véhicule), Bronze (2), Silver (5), Gold (10). Achat dans l'application.
class FormulesEcran extends StatefulWidget {
  const FormulesEcran({super.key, this.raison});

  /// Message affiché en tête (ex. limite de véhicules atteinte).
  final String? raison;

  @override
  State<FormulesEcran> createState() => _FormulesEcranState();
}

class _FormulesEcranState extends State<FormulesEcran> {
  late Future<void> _chargement;
  String? _dernierMessage;

  static const _couleurs = {
    'gratuit': Color(0xFF6B7280),
    'bronze': Color(0xFFB26A2E),
    'silver': Color(0xFF8A94A6),
    'gold': Color(0xFFD4A017),
  };

  @override
  void initState() {
    super.initState();
    _chargement = context.read<Abonnement>().charger();
  }

  @override
  Widget build(BuildContext context) {
    final ab = context.watch<Abonnement>();
    if (ab.message != null && ab.message != _dernierMessage) {
      _dernierMessage = ab.message;
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(ab.message!)));
      });
    }
    return Scaffold(
      appBar: AppBar(title: const Text('Formules')),
      body: FutureBuilder<void>(
        future: _chargement,
        builder: (context, snap) {
          if (snap.connectionState != ConnectionState.done) return const Center(child: CircularProgressIndicator());
          if (snap.hasError) return Padding(padding: const EdgeInsets.all(24), child: Text('${snap.error}'));
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              if (widget.raison != null)
                Card(
                  color: Theme.of(context).colorScheme.errorContainer,
                  child: Padding(padding: const EdgeInsets.all(12), child: Text(widget.raison!)),
                ),
              ListTile(
                contentPadding: EdgeInsets.zero,
                leading: Icon(Icons.workspace_premium, color: _couleurs[ab.formule], size: 36),
                title: Text('Formule actuelle : ${ab.libelle}', style: const TextStyle(fontWeight: FontWeight.bold)),
                subtitle: Text([
                  '${ab.vehiculesActifs} véhicule(s) actif(s) sur ${ab.limite}',
                  if (ab.etat?['date_fin'] != null)
                    '${ab.etat?['renouvellement_auto'] == true ? 'renouvellement le' : 'jusqu\'au'} '
                        '${dateFr(ab.etat!['date_fin'])}',
                  if (ab.etat?['echue'] == true) 'abonnement échu',
                ].join(' · ')),
              ),
              const SizedBox(height: 8),
              for (final f in ab.formules) _carte(ab, f),
              const SizedBox(height: 12),
              if (Abonnement.plateformeStore && ab.storeDisponible)
                OutlinedButton.icon(
                  onPressed: ab.enCours ? null : ab.restaurer,
                  icon: const Icon(Icons.restore),
                  label: const Text('Restaurer mes achats'),
                ),
              if (!Abonnement.plateformeStore)
                const Text('Les formules s\'achètent depuis l\'application iPhone, iPad, Android ou Mac.'),
              if (Abonnement.plateformeStore && !ab.storeDisponible && !ab.modeTest)
                const Text('Le store n\'est pas disponible sur cet appareil.'),
              const SizedBox(height: 12),
              Text(
                'Abonnement mensuel renouvelé automatiquement, résiliable à tout moment dans les réglages '
                'de votre compte App Store ou Google Play. Les véhicules archivés (vendus) ne comptent pas '
                'dans la limite ; si vous changez pour une formule inférieure, vos véhicules restent consultables '
                'mais vous ne pourrez plus en ajouter au-delà de la limite.',
                style: Theme.of(context).textTheme.bodySmall,
              ),
              if (ab.modeTest) ...[
                const SizedBox(height: 8),
                Text('Serveur de développement : les achats de test sont acceptés.',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Colors.orange.shade800)),
              ],
            ],
          );
        },
      ),
    );
  }

  Widget _carte(Abonnement ab, Map<String, dynamic> f) {
    final code = f['code'] as String;
    final actuelle = code == ab.formule;
    final produits = (f['produits'] as List? ?? []).cast<String>();
    final produit = ab.produitDe(f);
    final couleur = _couleurs[code] ?? Colors.blueGrey;
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: actuelle ? couleur : Colors.transparent, width: 2),
      ),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(children: [
          CircleAvatar(backgroundColor: couleur, foregroundColor: Colors.white, child: Text('${f['limite']}')),
          const SizedBox(width: 12),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('${f['libelle']}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              Text(f['limite'] == 1 ? '1 véhicule' : 'Jusqu\'à ${f['limite']} véhicules'),
              if (produit != null) Text('${produit.price} / mois', style: TextStyle(color: couleur, fontWeight: FontWeight.w600)),
            ]),
          ),
          if (actuelle)
            const Chip(label: Text('Actuelle'))
          else if (code != 'gratuit')
            Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
              if (produit != null)
                FilledButton(onPressed: ab.enCours ? null : () => ab.acheter(produit), child: const Text('Choisir')),
              if (ab.modeTest && produits.isNotEmpty)
                TextButton(
                  onPressed: ab.enCours ? null : () => ab.acheterTest(produits.first),
                  child: const Text('Activer (test)'),
                ),
            ]),
        ]),
      ),
    );
  }
}

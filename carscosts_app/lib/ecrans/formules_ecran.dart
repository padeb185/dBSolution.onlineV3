import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../l10n/langue.dart';
import '../widgets/bandeau_abonnement.dart';
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
  bool _annuel = false;

  static const _couleurs = {
    'gratuit': Color(0xFF6B7280),
    'bronze': Color(0xFFB26A2E),
    'silver': Color(0xFF8A94A6),
    'gold': Color(0xFFD4A017),
  };

  @override
  void initState() {
    super.initState();
    final ab = context.read<Abonnement>();
    _annuel = ab.periode == 'annuel';
    _chargement = ab.charger();
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
      appBar: AppBar(title: Text(t('Formules'))),
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
              const BandeauAbonnement(cliquable: false),
              ListTile(
                contentPadding: EdgeInsets.zero,
                leading: Icon(Icons.workspace_premium, color: _couleurs[ab.formule], size: 36),
                title: Text(t('Formule actuelle : {formule}', {'formule': ab.libelle}), style: const TextStyle(fontWeight: FontWeight.bold)),
                subtitle: Text([
                  t('{n} véhicule(s) actif(s) sur {limite}', {'n': ab.vehiculesActifs, 'limite': ab.limite}),
                  if (ab.etat?['echue'] == true) t('abonnement échu'),
                ].join(' · ')),
              ),
              if (ab.periode != null || ab.dateFin != null) _facturation(ab),
              const SizedBox(height: 8),
              if (ab.formules.any((f) => Abonnement.produitsDe(f, annuel: true).isNotEmpty))
                Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: SegmentedButton<bool>(
                    segments: [
                      ButtonSegment(value: false, label: Text(t('Mensuel'))),
                      ButtonSegment(value: true, label: Text(t('Annuel'))),
                    ],
                    selected: {_annuel},
                    onSelectionChanged: (v) => setState(() => _annuel = v.first),
                  ),
                ),
              for (final f in ab.formules) _carte(ab, f),
              const SizedBox(height: 12),
              if (Abonnement.plateformeStore && ab.storeDisponible)
                OutlinedButton.icon(
                  onPressed: ab.enCours ? null : ab.restaurer,
                  icon: const Icon(Icons.restore),
                  label: Text(t('Restaurer mes achats')),
                ),
              if (!Abonnement.plateformeStore)
                Text(t('Les formules s\'achètent depuis l\'application iPhone, iPad, Android ou Mac.')),
              if (Abonnement.plateformeStore && !ab.storeDisponible && !ab.modeTest)
                Text(t('Le store n\'est pas disponible sur cet appareil.')),
              const SizedBox(height: 12),
              Text(
                t('Abonnement mensuel ou annuel renouvelé automatiquement, résiliable à tout moment dans les réglages '
                    'de votre compte App Store ou Google Play. Les véhicules archivés (vendus) ne comptent pas '
                    'dans la limite. Si le paiement est refusé, la formule reste active pendant le délai de grâce du '
                    'store ; ensuite, les véhicules au-delà de la limite passent en lecture seule (rien n\'est supprimé).'),
                style: Theme.of(context).textTheme.bodySmall,
              ),
              if (ab.modeTest) ...[
                const SizedBox(height: 8),
                Text(t('Serveur de développement : les achats de test sont acceptés.'),
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Colors.orange.shade800)),
              ],
            ],
          );
        },
      ),
    );
  }

  /// Détail de la facturation : période, dates de facturation et de renouvellement, statut du paiement.
  Widget _facturation(Abonnement ab) {
    final (statut, couleur) = switch (ab.statutPaiement) {
      'grace' => (t('Paiement refusé – délai de grâce jusqu\'au {date}', {'date': dateFr(ab.dateFinGrace)}),
          Colors.orange.shade800),
      'echec' => (t('Paiement refusé – accès limité'), Theme.of(context).colorScheme.error),
      _ => (t('Paiement à jour'), Colors.green.shade700),
    };
    Widget ligne(String libelle, String valeur, [Color? c]) => Padding(
          padding: const EdgeInsets.symmetric(vertical: 3),
          child: Row(children: [
            Expanded(child: Text(libelle)),
            Flexible(
                child: Text(valeur,
                    textAlign: TextAlign.end, style: TextStyle(fontWeight: FontWeight.w600, color: c))),
          ]),
        );
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(children: [
          if (ab.periode != null) ligne(t('Période de facturation'), Abonnement.libellePeriode(ab.periode)),
          if (ab.dateDebut != null) ligne(t('Date de facturation (début)'), dateFr(ab.dateDebut)),
          if (ab.dateDerniereFacturation != null) ligne(t('Dernière facturation'), dateFr(ab.dateDerniereFacturation)),
          if (ab.dateRenouvellement != null)
            ligne(t('Date de renouvellement'), dateFr(ab.dateRenouvellement))
          else if (ab.dateFin != null)
            ligne(t('Fin de la formule'), dateFr(ab.dateFin)),
          if (ab.periode != null) ligne(t('Paiement'), statut, couleur),
        ]),
      ),
    );
  }

  Widget _carte(Abonnement ab, Map<String, dynamic> f) {
    final code = f['code'] as String;
    // Même formule mais autre période (mensuel ↔ annuel) : proposée comme un changement
    final actuelle = code == ab.formule && (ab.periode == null || (ab.periode == 'annuel') == _annuel);
    final produits = Abonnement.produitsDe(f, annuel: _annuel);
    final produit = ab.produitDe(f, annuel: _annuel);
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
              Text(Abonnement.libelleFormule(code), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              Text(f['limite'] == 1 ? t('1 véhicule') : t('Jusqu\'à {n} véhicules', {'n': f['limite']})),
              if (produit != null)
                Text(_annuel ? t('{prix} / an', {'prix': produit.price}) : t('{prix} / mois', {'prix': produit.price}),
                    style: TextStyle(color: couleur, fontWeight: FontWeight.w600)),
            ]),
          ),
          if (actuelle)
            Chip(label: Text(t('Actuelle')))
          else if (code != 'gratuit')
            Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
              if (produit != null)
                FilledButton(onPressed: ab.enCours ? null : () => ab.acheter(produit), child: Text(t('Choisir'))),
              if (ab.modeTest && produits.isNotEmpty)
                TextButton(
                  onPressed: ab.enCours ? null : () => ab.acheterTest(produits.first),
                  child: Text(t('Activer (test)')),
                ),
            ]),
        ]),
      ),
    );
  }
}

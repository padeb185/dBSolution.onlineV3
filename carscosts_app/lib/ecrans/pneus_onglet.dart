import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../api/api_client.dart';
import '../l10n/langue.dart';
import '../l10n/unites.dart';
import '../modeles/ressources.dart';
import '../widgets/format.dart';
import 'formulaire_ecran.dart';
import 'formules_ecran.dart';

/// Pneus du véhicule par train (avant / arrière) : première et seconde monte (ex. été / hiver),
/// kilométrage mémorisé par train, changement de monte, remplacements (historique).
class PneusOnglet extends StatefulWidget {
  const PneusOnglet({super.key, required this.vehicule, this.auChangement});

  final Map<String, dynamic> vehicule;
  final VoidCallback? auChangement;

  @override
  State<PneusOnglet> createState() => _PneusOngletState();
}

class _PneusOngletState extends State<PneusOnglet> with AutomaticKeepAliveClientMixin {
  late Future<List<Map<String, dynamic>>> _trains;

  String get _id => widget.vehicule['id'] as String;
  Unites get _u => Unites.de(widget.vehicule);

  @override
  bool get wantKeepAlive => true;

  @override
  void initState() {
    super.initState();
    _charger();
  }

  bool _chargeVerrouille = false;

  void _charger() {
    _chargeVerrouille = context.read<Abonnement>().formule == 'gratuit';
    if (_chargeVerrouille) {
      _trains = Future.value(const []);   // formule gratuite : pas d'appel, écran « Bronze »
      return;
    }
    _trains = context.read<ApiClient>().get('pneus/', params: {'vehicule': _id}).then(
        (r) => [for (final e in r as List) Map<String, dynamic>.from(e as Map)]);
  }

  void _recharger() {
    setState(_charger);
    widget.auChangement?.call();
  }

  Future<void> _ouvrir([Map<String, dynamic>? train]) async {
    final ok = await Navigator.push<bool>(
      context,
      MaterialPageRoute(
        builder: (_) => FormulaireEcran(ressource: pneus, vehiculeId: _id, element: train, vehicule: widget.vehicule),
      ),
    );
    if (ok == true) _recharger();
  }

  Future<void> _changerMonte(List<Map<String, dynamic>> actifs) async {
    final kmCtrl = TextEditingController();
    var jour = DateTime.now();
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setD) => AlertDialog(
          title: Text(t('Changer de monte')),
          content: Column(mainAxisSize: MainAxisSize.min, children: [
            Text(t('Les pneus montés sont démontés (leurs kilomètres sont mémorisés) et ceux de l\'autre monte sont montés.')),
            const SizedBox(height: 12),
            TextField(
              controller: kmCtrl,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                labelText: t('Kilométrage actuel'),
                suffixText: _u.symboleDistance,
                helperText: t('Vide : kilométrage actuel du véhicule.'),
              ),
            ),
            const SizedBox(height: 8),
            ListTile(
              contentPadding: EdgeInsets.zero,
              leading: const Icon(Icons.calendar_today),
              title: Text(dateFr(dateIso(jour))),
              onTap: () async {
                final d = await showDatePicker(
                    context: ctx, initialDate: jour, firstDate: DateTime(2000), lastDate: DateTime(2100));
                if (d != null) setD(() => jour = d);
              },
            ),
          ]),
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx, false), child: Text(t('Annuler'))),
            FilledButton(onPressed: () => Navigator.pop(ctx, true), child: Text(t('Valider'))),
          ],
        ),
      ),
    );
    if (ok != true || !mounted) return;
    final saisie = double.tryParse(kmCtrl.text.replaceAll(',', '.'));
    try {
      await context.read<ApiClient>().post('pneus/changer_monte/', {
        'vehicule': _id,
        'date': dateIso(jour),
        if (saisie != null) 'kilometrage': _u.versKm(saisie).round(),
      });
      _recharger();
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(t('Monte changée.'))));
    } on ApiException catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    }
  }

  // ------------------------------------------------------------------ Mise en page
  String _nom(Map<String, dynamic> p) {
    final nom = [p['marque'], p['modele']].where((x) => (x ?? '').toString().isNotEmpty).join(' ');
    return nom.isEmpty ? (typesPneus[p['type_pneus']] ?? '') : nom;
  }

  IconData _icone(String? type) => switch (type) {
        'hiver' => Icons.ac_unit,
        'ete' => Icons.wb_sunny_outlined,
        '4saisons' => Icons.all_inclusive,
        'pluie' => Icons.water_drop_outlined,
        _ => Icons.tire_repair,
      };

  Widget _train(Map<String, dynamic> p, {bool historique = false}) {
    final details = [
      positionsPneus[p['position']] ?? '',
      typesPneus[p['type_pneus']] ?? '',
      if ((p['taille'] ?? '') != '') p['taille'],
      t('train n°{n}', {'n': p['numero']}),
    ].join(' · ');
    final dates = historique
        ? t('du {debut} au {fin}', {'debut': dateFr(p['date_achat'] ?? p['date_montage']), 'fin': dateFr(p['date_remplacement'])})
        : t('monté le {date}', {'date': dateFr(p['date_montage'])});
    return ListTile(
      leading: CircleAvatar(
        backgroundColor: p['est_monte'] == true ? Theme.of(context).colorScheme.primaryContainer : null,
        child: Icon(_icone(p['type_pneus'] as String?)),
      ),
      title: Text(_nom(p)),
      subtitle: Text('$details\n$dates'),
      isThreeLine: true,
      trailing: Column(mainAxisAlignment: MainAxisAlignment.center, crossAxisAlignment: CrossAxisAlignment.end, children: [
        Text(km(p['km_effectues'], _u), style: const TextStyle(fontWeight: FontWeight.bold)),
        if (p['prix'] != null) Text(euros(p['prix']), style: Theme.of(context).textTheme.bodySmall),
      ]),
      onTap: () => _ouvrir(p),
    );
  }

  Widget _section(String titre, List<Map<String, dynamic>> trains, {bool historique = false, Widget? action}) => Card(
        margin: const EdgeInsets.only(bottom: 12),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 8, 0),
            child: Row(children: [
              Expanded(child: Text(titre, style: Theme.of(context).textTheme.titleMedium)),
              if (action != null) action,
            ]),
          ),
          for (final p in trains) _train(p, historique: historique),
          const SizedBox(height: 4),
        ]),
      );

  /// Formule gratuite : les pneus sont réservés aux formules payantes (Bronze minimum)
  Widget _verrou() => ListView(padding: const EdgeInsets.all(24), children: [
        const Icon(Icons.lock_outline, size: 48),
        const SizedBox(height: 12),
        Text(t('« {titre} » est disponible à partir de la formule Bronze.', {'titre': t('Pneus')}),
            textAlign: TextAlign.center, style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: 8),
        Text(t('Première et seconde monte (ex. été / hiver), kilomètres mémorisés par train, historique des remplacements.'),
            textAlign: TextAlign.center),
        const SizedBox(height: 16),
        Center(
          child: FilledButton.icon(
            icon: const Icon(Icons.workspace_premium),
            label: Text(t('Voir les formules')),
            onPressed: () async {
              await Navigator.push(context, MaterialPageRoute(builder: (_) => const FormulesEcran()));
              if (mounted) setState(_charger);
            },
          ),
        ),
      ]);

  @override
  Widget build(BuildContext context) {
    super.build(context);
    if (context.watch<Abonnement>().formule == 'gratuit') return _verrou();
    if (_chargeVerrouille) _charger();   // formule payante prise entre-temps : chargement des pneus
    return Scaffold(
      floatingActionButton: FloatingActionButton.extended(
        heroTag: 'pneus',
        onPressed: () => _ouvrir(),
        icon: const Icon(Icons.add),
        label: Text(t('Pneus')),
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          setState(_charger);
          await _trains;
        },
        child: FutureBuilder<List<Map<String, dynamic>>>(
          future: _trains,
          builder: (context, snap) {
            if (snap.connectionState != ConnectionState.done) return const Center(child: CircularProgressIndicator());
            if (snap.hasError) {
              return ListView(children: [Padding(padding: const EdgeInsets.all(24), child: Text('${snap.error}'))]);
            }
            final trains = snap.data!;
            if (trains.isEmpty) {
              return ListView(padding: const EdgeInsets.all(32), children: [
                const Icon(Icons.tire_repair, size: 48, color: Colors.grey),
                const SizedBox(height: 8),
                Text(
                  t('Enregistrez vos pneus (première monte) puis, par exemple, vos pneus hiver (seconde monte) : '
                      'les kilomètres de chaque train sont mémorisés.'),
                  textAlign: TextAlign.center,
                ),
              ]);
            }
            final actifs = trains.where((p) => p['actif'] == true).toList();
            final montes = actifs.where((p) => p['est_monte'] == true).toList()
              ..sort((a, b) => '${a['position']}'.compareTo('${b['position']}'));
            final deuxMontes = actifs.map((p) => p['monte']).toSet().length > 1;
            List<Map<String, dynamic>> de(String monte) =>
                actifs.where((p) => p['monte'] == monte).toList()..sort((a, b) => '${a['position']}'.compareTo('${b['position']}'));
            final historique = trains.where((p) => p['actif'] != true).toList();
            return ListView(
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 96),
              children: [
                if (montes.isNotEmpty)
                  _section(t('Montés actuellement'), montes,
                      action: deuxMontes
                          ? TextButton.icon(
                              onPressed: () => _changerMonte(actifs),
                              icon: const Icon(Icons.swap_horiz),
                              label: Text(t('Changer de monte')),
                            )
                          : null),
                if (de('premiere').isNotEmpty) _section(t('Première monte'), de('premiere')),
                if (de('seconde').isNotEmpty) _section(t('Seconde monte'), de('seconde')),
                if (historique.isNotEmpty) _section(t('Historique (pneus remplacés)'), historique, historique: true),
              ],
            );
          },
        ),
      ),
    );
  }
}

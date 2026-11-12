import 'package:fl_chart/fl_chart.dart';
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
  Future<Map<String, dynamic>?> _stats = Future.value(null);

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
      _stats = Future.value(null);
      return;
    }
    final api = context.read<ApiClient>();
    _trains = api.get('pneus/', params: {'vehicule': _id}).then(
        (r) => [for (final e in r as List) Map<String, dynamic>.from(e as Map)]);
    // Statistiques facultatives : une erreur n'empêche pas d'afficher les pneus
    _stats = api
        .get('pneus/statistiques/', params: {'vehicule': _id})
        .then<Map<String, dynamic>?>((r) => Map<String, dynamic>.from(r as Map))
        .catchError((_) => null);
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
        'slick' => Icons.sports_score,
        'semi_slick' => Icons.speed,
        _ => Icons.tire_repair,
      };

  // ------------------------------------------------------------------ Statistiques (sous les pneus)
  static const _couleurs = {
    'ete': Color(0xFFF59E0B),
    'hiver': Color(0xFF3B82F6),
    '4saisons': Color(0xFF10B981),
    'pluie': Color(0xFF06B6D4),
    'semi_slick': Color(0xFFF97316),
    'slick': Color(0xFFDC2626),
  };

  Color _couleur(dynamic type) => _couleurs[type] ?? Colors.blueGrey;

  /// Nombre de trains par type (été, hiver, slick…), graphiques et statistiques : km, coût, durée de vie.
  List<Widget> _statistiques(Map<String, dynamic> s, List<Map<String, dynamic>> trains) {
    final types = [
      for (final e in (s['par_type'] as List? ?? [])) Map<String, dynamic>.from(e as Map)
    ].where((e) => (e['trains'] as num? ?? 0) > 0).toList();
    if (types.isEmpty) return const [];
    final total = Map<String, dynamic>.from(s['total'] as Map? ?? {});
    final marques = [
      for (final m in (s['par_marque'] as List? ?? [])) Map<String, dynamic>.from(m as Map)
    ];
    final style = Theme.of(context).textTheme.bodySmall;
    final titre = Theme.of(context).textTheme.titleSmall;
    String nomType(Map<String, dynamic> ty) => typesPneus[ty['type']] ?? '${ty['libelle']}';

    final avecCout = types.where((ty) => ty['cout_1000_km'] != null).toList();
    final parTrain = [...trains]..sort((a, b) => (enDouble(b['km_effectues']) ?? 0).compareTo(enDouble(a['km_effectues']) ?? 0));

    return [
      Padding(
        padding: const EdgeInsets.fromLTRB(4, 8, 4, 8),
        child: Text(t('Statistiques des pneus'), style: Theme.of(context).textTheme.titleLarge),
      ),
      // Nombre de trains par type + totaux
      Card(
        margin: const EdgeInsets.only(bottom: 12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(t('Mes trains de pneus'), style: titre),
            const SizedBox(height: 8),
            Wrap(spacing: 8, runSpacing: 8, children: [
              for (final ty in types)
                Chip(
                  avatar: Icon(_icone(ty['type'] as String?), size: 18, color: _couleur(ty['type'])),
                  label: Text('${nomType(ty)} · ${ty['trains']}'),
                ),
              Chip(avatar: const Icon(Icons.functions, size: 18), label: Text(t('Total · {n}', {'n': total['trains'] ?? 0}))),
            ]),
            const SizedBox(height: 12),
            Wrap(spacing: 24, runSpacing: 8, children: [
              _chiffre(t('Kilomètres'), km(total['km'], _u)),
              if ((total['cout'] as num? ?? 0) > 0) _chiffre(t('Coût total'), euros(total['cout'])),
              if (total['cout_1000_km'] != null) _chiffre(t('Coût aux 1 000 {unite}', {'unite': _u.symboleDistance}),
                  euros(_u.coutParDistance(enDouble(total['cout_1000_km']) ?? 0))),
              if (total['km_moyen_remplacement'] != null) _chiffre(t('Durée de vie moyenne'), km(total['km_moyen_remplacement'], _u)),
            ]),
            const SizedBox(height: 8),
            Text(t('Un train = les pneus d\'un essieu (avant ou arrière).'), style: style),
          ]),
        ),
      ),
      // Graphiques
      Card(
        margin: const EdgeInsets.only(bottom: 12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(t('Répartition des trains par type'), style: titre),
            const SizedBox(height: 8),
            Row(children: [
              SizedBox(
                width: 140,
                height: 140,
                child: PieChart(PieChartData(
                  sectionsSpace: 2,
                  centerSpaceRadius: 34,
                  sections: [
                    for (final ty in types)
                      PieChartSectionData(
                        value: (ty['trains'] as num).toDouble(),
                        color: _couleur(ty['type']),
                        radius: 30,
                        title: '${ty['trains']}',
                        titleStyle: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
                      ),
                  ],
                )),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  for (final ty in types) _legende(_couleur(ty['type']), '${nomType(ty)} : ${ty['trains']}'),
                ]),
              ),
            ]),
            const Divider(height: 32),
            Text(t('Kilomètres par type'), style: titre),
            const SizedBox(height: 8),
            _barres([for (final ty in types) (nomType(ty), _u.depuisKm(enDouble(ty['km']) ?? 0), _couleur(ty['type']))],
                (v) => km(_u.versKm(v), _u)),
            if (avecCout.isNotEmpty) ...[
              const Divider(height: 32),
              Text(t('Coût aux 1 000 {unite} par type', {'unite': _u.symboleDistance}), style: titre),
              const SizedBox(height: 8),
              _barres([
                for (final ty in avecCout)
                  (nomType(ty), _u.coutParDistance(enDouble(ty['cout_1000_km']) ?? 0), _couleur(ty['type']))
              ], (v) => euros(v)),
            ],
            if (parTrain.length > 1) ...[
              const Divider(height: 32),
              Text(t('Kilomètres par train'), style: titre),
              const SizedBox(height: 8),
              _barres([
                for (final p in parTrain.take(12))
                  ('${p['position'] == 'avant' ? t('AV') : t('AR')}${p['numero']}${p['actif'] == true ? '' : ' ✝'}',
                      _u.depuisKm(enDouble(p['km_effectues']) ?? 0), _couleur(p['type_pneus']))
              ], (v) => km(_u.versKm(v), _u)),
              Text(t('AV / AR : essieu avant / arrière, suivi du numéro du train. ✝ : remplacé.'), style: style),
            ],
          ]),
        ),
      ),
      // Détail par type et par marque
      Card(
        margin: const EdgeInsets.only(bottom: 12),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(t('Détail par type'), style: titre),
            for (final ty in types) _ligneStat(nomType(ty), ty, _icone(ty['type'] as String?), _couleur(ty['type'])),
            if (marques.length > 1 || (marques.isNotEmpty && marques.first['marque'] != '—')) ...[
              const Divider(),
              Text(t('Par marque'), style: titre),
              for (final m in marques.take(5)) _ligneStat('${m['marque']}', m, Icons.label_outline, null),
            ],
            const SizedBox(height: 4),
            Text(t('Coût aux 1 000 km : uniquement les pneus dont le prix est connu. Durée de vie : pneus remplacés.'),
                style: style),
          ]),
        ),
      ),
    ];
  }

  Widget _chiffre(String libelle, String valeur) => Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(libelle, style: Theme.of(context).textTheme.bodySmall),
        Text(valeur, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
      ]);

  Widget _legende(Color couleur, String texte) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 2),
        child: Row(children: [
          Container(width: 12, height: 12, decoration: BoxDecoration(color: couleur, borderRadius: BorderRadius.circular(3))),
          const SizedBox(width: 8),
          Expanded(child: Text(texte)),
        ]),
      );

  /// Barres verticales : (étiquette, valeur, couleur) ; `format` pour l'axe et l'info-bulle.
  Widget _barres(List<(String, double, Color)> valeurs, String Function(double) format) {
    if (valeurs.every((v) => v.$2 == 0)) {
      return Padding(padding: const EdgeInsets.all(8), child: Text(t('Aucune donnée.')));
    }
    return SizedBox(
      height: 190,
      child: BarChart(BarChartData(
        gridData: const FlGridData(show: true, drawVerticalLine: false),
        borderData: FlBorderData(show: false),
        titlesData: FlTitlesData(
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          leftTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              reservedSize: 48,
              getTitlesWidget: (v, meta) => Text(nombre(v, decimales: 0), style: const TextStyle(fontSize: 9)),
            ),
          ),
          bottomTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              reservedSize: 28,
              interval: 1,
              getTitlesWidget: (v, meta) {
                final i = v.toInt();
                if (i < 0 || i >= valeurs.length) return const SizedBox.shrink();
                return Padding(
                  padding: const EdgeInsets.only(top: 4),
                  child: Text(valeurs[i].$1, style: const TextStyle(fontSize: 9), overflow: TextOverflow.ellipsis),
                );
              },
            ),
          ),
        ),
        barTouchData: BarTouchData(
          touchTooltipData: BarTouchTooltipData(
            getTooltipItem: (groupe, _, barre, __) => BarTooltipItem(
              '${valeurs[groupe.x].$1}\n${format(barre.toY)}',
              const TextStyle(color: Colors.white, fontSize: 11),
            ),
          ),
        ),
        barGroups: [
          for (var i = 0; i < valeurs.length; i++)
            BarChartGroupData(x: i, barRods: [
              BarChartRodData(toY: valeurs[i].$2, color: valeurs[i].$3, width: 18, borderRadius: BorderRadius.circular(3)),
            ]),
        ],
      )),
    );
  }

  /// Coût aux 1 000 km (ou aux 1 000 miles).
  String _coutDistance(dynamic coutKm) =>
      t('{prix} / 1 000 {unite}', {'prix': euros(_u.coutParDistance(enDouble(coutKm) ?? 0)), 'unite': _u.symboleDistance});

  Widget _ligneStat(String titre, Map<String, dynamic> st, IconData icone, Color? couleur) {
    final comptes = [
      t('{n} train(s)', {'n': st['trains']}),
      if ((st['montes'] as num? ?? 0) > 0) t('{n} monté(s)', {'n': st['montes']}),
      if ((st['en_service'] as num? ?? 0) - (st['montes'] as num? ?? 0) > 0)
        t('{n} en réserve', {'n': (st['en_service'] as num) - (st['montes'] as num? ?? 0)}),
      if ((st['remplaces'] as num? ?? 0) > 0) t('{n} remplacé(s)', {'n': st['remplaces']}),
    ].join(' · ');
    final valeurs = [
      km(st['km'], _u),
      if ((st['cout'] as num? ?? 0) > 0) euros(st['cout']),
      if (st['cout_1000_km'] != null) _coutDistance(st['cout_1000_km']),
    ].join(' · ');
    final vie = [
      if (st['km_moyen_remplacement'] != null) km(st['km_moyen_remplacement'], _u),
      if (st['duree_moyenne_mois'] != null) t('{n} mois', {'n': nombre(st['duree_moyenne_mois'], decimales: 1)}),
    ].join(' · ');
    return ListTile(
      contentPadding: EdgeInsets.zero,
      dense: true,
      leading: Icon(icone, color: couleur),
      title: Text('$titre — $comptes'),
      subtitle: Text([valeurs, if (vie.isNotEmpty) t('Durée de vie moyenne : {vie}', {'vie': vie})].join('\n')),
    );
  }

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
        child: Icon(_icone(p['type_pneus'] as String?), color: _couleur(p['type_pneus'])),
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
          await Future.wait([_trains, _stats]);
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
                // Statistiques et graphiques sous les pneus
                FutureBuilder<Map<String, dynamic>?>(
                  future: _stats,
                  builder: (context, st) => st.data == null
                      ? const SizedBox.shrink()
                      : Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: _statistiques(st.data!, trains)),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}

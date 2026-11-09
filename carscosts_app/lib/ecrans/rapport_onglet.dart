import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../api/api_client.dart';
import '../l10n/langue.dart';
import '../l10n/unites.dart';
import '../modeles/pays.dart';
import '../modeles/ressources.dart';
import '../widgets/format.dart';
import '../widgets/format.dart' as format;
import 'financement_ecran.dart' show typesAchat;
import 'formules_ecran.dart';

/// Rapport d'un véhicule : coûts par mois, carburant, électricité, financement (payé / reste à payer),
/// kilomètres ; statistiques et graphiques sur une période (12 mois, année en cours, tout).
class RapportOnglet extends StatefulWidget {
  const RapportOnglet({super.key, required this.vehicule});

  final Map<String, dynamic> vehicule;

  @override
  State<RapportOnglet> createState() => _RapportOngletState();
}

class _RapportOngletState extends State<RapportOnglet> with AutomaticKeepAliveClientMixin {
  String _periode = '12m';
  late Future<Map<String, dynamic>> _rapport;

  Unites get _u => Unites.de(widget.vehicule);

  static const _couleurs = {
    'energie': Color(0xFF2563EB),
    'electricite': Color(0xFF06B6D4),
    'entretiens': Color(0xFFF59E0B),
    'documents': Color(0xFF10B981),
    'autres': Color(0xFF8B5CF6),
    'financement': Color(0xFFEF4444),
  };

  Map<String, String> get _libelles => {
        'energie': t('Carburant'),
        'electricite': t('Électricité'),
        'entretiens': t('Entretiens et réparations'),
        'documents': t('Documents / assurance'),
        'autres': t('Autres'),
        'financement': t('Financement'),
      };

  @override
  bool get wantKeepAlive => true;

  @override
  void initState() {
    super.initState();
    _charger();
  }

  void _charger() {
    if (context.read<Abonnement>().formule == 'gratuit') {
      _rapport = Future.value(const {});   // formule gratuite : pas d'appel, écran « Bronze »
      return;
    }
    _rapport = context
        .read<ApiClient>()
        .get('vehicules/${widget.vehicule['id']}/rapport/', params: {'periode': _periode}).then(
            (r) => Map<String, dynamic>.from(r as Map));
  }

  // ------------------------------------------------------------------ Mise en page
  /// Formule gratuite : le rapport est réservé aux formules payantes (Bronze minimum)
  Widget _verrou() => ListView(padding: const EdgeInsets.all(24), children: [
        const Icon(Icons.lock_outline, size: 48),
        const SizedBox(height: 12),
        Text(t('Le rapport est disponible à partir de la formule Bronze.'),
            textAlign: TextAlign.center, style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: 8),
        Text(
          t('Coûts par mois, carburant, électricité, financement (payé, reste à payer), kilomètres : '
              'statistiques et graphiques.'),
          textAlign: TextAlign.center,
        ),
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
    return RefreshIndicator(
      onRefresh: () async {
        setState(_charger);
        await _rapport;
      },
      child: FutureBuilder<Map<String, dynamic>>(
        future: _rapport,
        builder: (context, snap) {
          if (snap.connectionState != ConnectionState.done) return const Center(child: CircularProgressIndicator());
          if (snap.hasError) {
            return ListView(children: [Padding(padding: const EdgeInsets.all(24), child: Text('${snap.error}'))]);
          }
          final r = snap.data!;
          if (r.isEmpty) {
            // Passage à une formule payante depuis un autre écran : chargement du rapport
            WidgetsBinding.instance.addPostFrameCallback((_) {
              if (mounted) setState(_charger);
            });
            return const Center(child: CircularProgressIndicator());
          }
          final carburant = Map<String, dynamic>.from(r['carburant'] as Map);
          final electricite = Map<String, dynamic>.from(r['electricite'] as Map);
          final couts = Map<String, dynamic>.from(r['couts'] as Map);
          final kms = Map<String, dynamic>.from(r['kilometres'] as Map);
          final fin = (r['financement'] as Map?)?.cast<String, dynamic>();
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              _choixPeriode(),
              const SizedBox(height: 12),
              _syntheseCouts(couts, kms),
              _carte(t('Coûts par mois'), _graphiqueCouts(couts), legende: true),
              if ((carburant['nombre'] as num? ?? 0) > 0) _blocCarburant(carburant),
              if ((electricite['nombre'] as num? ?? 0) > 0) _blocElectricite(electricite),
              if (((r['maintenances'] as Map?)?['nombre'] as num? ?? 0) > 0)
                _blocMaintenances(Map<String, dynamic>.from(r['maintenances'] as Map)),
              if (fin != null && fin['type_achat'] != 'comptant') _blocFinancement(fin, r['echeancier'] as List? ?? []),
              _carte(t('Kilomètres par mois'), _graphiqueBarres(
                [for (final m in kms['par_mois'] as List) (m['mois'] as String, _u.depuisKm(enDouble(m['km']) ?? 0))],
                const Color(0xFF64748B),
              )),
            ],
          );
        },
      ),
    );
  }

  Widget _choixPeriode() {
    final choix = {'12m': t('12 derniers mois'), 'annee': t('Cette année'), 'tout': t('Depuis l\'achat')};
    return Wrap(spacing: 8, children: [
      for (final e in choix.entries)
        ChoiceChip(
          label: Text(e.value),
          selected: _periode == e.key,
          onSelected: (_) => setState(() {
            _periode = e.key;
            _charger();
          }),
        ),
    ]);
  }

  Widget _carte(String titre, Widget contenu, {bool legende = false}) => Card(
        margin: const EdgeInsets.only(bottom: 12),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(titre, style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 12),
            contenu,
            if (legende) ...[
              const SizedBox(height: 8),
              Wrap(spacing: 12, runSpacing: 4, children: [
                for (final e in _couleurs.entries)
                  Row(mainAxisSize: MainAxisSize.min, children: [
                    Container(width: 10, height: 10, color: e.value),
                    const SizedBox(width: 4),
                    Text(_libelles[e.key]!, style: const TextStyle(fontSize: 12)),
                  ]),
              ]),
            ],
          ]),
        ),
      );

  Widget _ligne(String libelle, String valeur, {bool gras = false}) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 3),
        child: Row(children: [
          Expanded(child: Text(libelle)),
          Text(valeur, style: gras ? const TextStyle(fontWeight: FontWeight.bold) : null),
        ]),
      );

  // ------------------------------------------------------------------ Synthèse
  Widget _syntheseCouts(Map<String, dynamic> couts, Map<String, dynamic> kms) {
    final totaux = Map<String, dynamic>.from(couts['totaux'] as Map);
    final coutKm = enDouble(couts['cout_km']);
    return _carte(t('Synthèse de la période'), Column(children: [
      _ligne(t('Dépenses de la période'), euros(couts['total']), gras: true),
      _ligne(t('Moyenne par mois'), euros(couts['moyenne_mois'])),
      _ligne(t('Kilomètres parcourus'), km(kms['total'], _u)),
      if (coutKm != null)
        _ligne(_u.miles ? t('Coût au mile') : t('Coût au km'),
            '${nombre(_u.coutParDistance(coutKm), decimales: 3)} €'),
      const Divider(),
      for (final e in _couleurs.keys)
        if ((enDouble(totaux[e]) ?? 0) > 0)
          Row(children: [
            Container(width: 10, height: 10, color: _couleurs[e]),
            const SizedBox(width: 8),
            Expanded(child: _ligne(_libelles[e]!, euros(totaux[e]))),
          ]),
      Padding(
        padding: const EdgeInsets.only(top: 6),
        child: Text(t('Prix d\'achat non compris (voir Résumé).'), style: Theme.of(context).textTheme.bodySmall),
      ),
    ]));
  }

  // ------------------------------------------------------------------ Maintenances (pièces / main-d'œuvre)
  static const _couleurPieces = Color(0xFFF59E0B);
  static const _couleurMainOeuvre = Color(0xFF7C3AED);

  Widget _blocMaintenances(Map<String, dynamic> m) {
    final parMois = [for (final x in m['par_mois'] as List) Map<String, dynamic>.from(x as Map)];
    final mois = [for (final x in parMois) x['mois'] as String];
    final pieces = enDouble(m['pieces']) ?? 0, mo = enDouble(m['main_oeuvre']) ?? 0;
    final total = pieces + mo;
    Widget pastille(Color c, String texte) => Row(mainAxisSize: MainAxisSize.min, children: [
          Container(width: 10, height: 10, color: c),
          const SizedBox(width: 4),
          Text(texte, style: const TextStyle(fontSize: 12)),
        ]);
    return _carte(t('Maintenances : pièces et main-d\'œuvre'), Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      _ligne(t('Nombre de maintenances'), '${m['nombre']}'),
      _ligne(t('Total TVAC'), euros(m['total']), gras: true),
      _ligne(t('dont TVA'), euros(m['total_tva'])),
      const SizedBox(height: 8),
      // Répartition pièces / main-d'œuvre
      if (total > 0)
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: SizedBox(
            height: 14,
            child: Row(children: [
              if (pieces > 0) Expanded(flex: (pieces * 1000 / total).round().clamp(1, 1000).toInt(), child: Container(color: _couleurPieces)),
              if (mo > 0) Expanded(flex: (mo * 1000 / total).round().clamp(1, 1000).toInt(), child: Container(color: _couleurMainOeuvre)),
            ]),
          ),
        ),
      const SizedBox(height: 6),
      Row(children: [
        Expanded(child: _ligne(t('Pièces'), '${euros(pieces)} · ${total > 0 ? nombre(pieces * 100 / total, decimales: 0) : 0} %')),
      ]),
      _ligne(t('Main-d\'œuvre'), '${euros(mo)} · ${total > 0 ? nombre(mo * 100 / total, decimales: 0) : 0} %'),
      const SizedBox(height: 12),
      SizedBox(
        height: 200,
        child: BarChart(BarChartData(
          gridData: const FlGridData(show: true, drawVerticalLine: false),
          borderData: FlBorderData(show: false),
          titlesData: _titres(mois),
          barTouchData: BarTouchData(
            touchTooltipData: BarTouchTooltipData(
              getTooltipItem: (groupe, _, barre, __) => BarTooltipItem(
                '${_etiquetteMois(mois[groupe.x])}\n${format.euros(barre.toY)}',
                const TextStyle(color: Colors.white, fontSize: 11),
              ),
            ),
          ),
          barGroups: [
            for (var i = 0; i < parMois.length; i++)
              () {
                final p = enDouble(parMois[i]['pieces']) ?? 0, o = enDouble(parMois[i]['main_oeuvre']) ?? 0;
                return BarChartGroupData(x: i, barRods: [
                  BarChartRodData(toY: p + o, width: 14, borderRadius: BorderRadius.circular(3), rodStackItems: [
                    if (p > 0) BarChartRodStackItem(0, p, _couleurPieces),
                    if (o > 0) BarChartRodStackItem(p, p + o, _couleurMainOeuvre),
                  ]),
                ]);
              }(),
          ],
        )),
      ),
      const SizedBox(height: 8),
      Wrap(spacing: 12, children: [pastille(_couleurPieces, t('Pièces')), pastille(_couleurMainOeuvre, t('Main-d\'œuvre'))]),
      const Divider(height: 24),
      Text(t('Par type'), style: Theme.of(context).textTheme.titleSmall),
      const SizedBox(height: 4),
      for (final x in (m['par_type'] as List).cast<Map>())
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 4),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            _ligne('${x['libelle']} (${x['nombre']})', euros(x['total']), gras: true),
            Text(t('pièces {pieces} · main-d\'œuvre {mo}', {'pieces': euros(x['pieces']), 'mo': euros(x['main_oeuvre'])}),
                style: Theme.of(context).textTheme.bodySmall),
          ]),
        ),
    ]));
  }

  // ------------------------------------------------------------------ Carburant / électricité
  Widget _blocCarburant(Map<String, dynamic> c) {
    // Carburant liquide (L / gallons) ou GNC (kg)
    final type = c['consommation_unite'] == 'kg' ? 'gnc' : 'sp95';
    final unite = _u.symboleQuantite(type);
    final quantite = _u.depuisQuantite(enDouble(c['total_quantite']) ?? 0, type);
    final prix = enDouble(c['prix_moyen']);
    final conso = enDouble(c['consommation_moyenne']);
    return _carte(t('Carburant'), Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      _ligne(t('Pleins'), '${c['nombre']}'),
      _ligne(t('Quantité'), '${nombre(quantite)} $unite'),
      _ligne(t('Montant'), euros(c['total_montant']), gras: true),
      if (prix != null) _ligne(t('Prix moyen'), '${nombre(_u.prixParQuantite(prix, type), decimales: 3)} €/$unite'),
      if (conso != null)
        _ligne(t('Consommation moyenne'), () {
          final v = _u.consommation(conso, '${c['consommation_unite'] ?? 'L'}');
          return '${nombre(v.$1)} ${v.$2}';
        }()),
      if ((enDouble(c['total_tva']) ?? 0) > 0) _ligne(t('dont TVA'), euros(c['total_tva'])),
      const SizedBox(height: 12),
      _graphiqueBarres([for (final m in c['par_mois'] as List) (m['mois'] as String, enDouble(m['montant']) ?? 0)],
          _couleurs['energie']!, euros: true),
      const SizedBox(height: 12),
      Text(t('Par carburant'), style: Theme.of(context).textTheme.titleSmall),
      for (final g in c['par_type'] as List)
        _ligne('${carburants[g['code']] ?? g['code']} · ${g['nombre']}', euros(g['montant'])),
      if ((c['par_pays'] as List).length > 1 || (c['par_pays'] as List).any((p) => p['pays'] != widget.vehicule['pays_immatriculation'])) ...[
        const SizedBox(height: 8),
        Text(t('Par pays (TVA)'), style: Theme.of(context).textTheme.titleSmall),
        for (final p in c['par_pays'] as List)
          _ligne('${paysImmatriculation[p['pays']] ?? p['pays']}', '${euros(p['montant'])} · ${t('TVA')} ${euros(p['tva'])}'),
      ],
    ]));
  }

  Widget _blocElectricite(Map<String, dynamic> e) {
    final prix = enDouble(e['prix_moyen']);
    final conso = enDouble(e['consommation_moyenne']);
    return _carte(t('Électricité'), Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      _ligne(t('Recharges'), '${e['nombre']}'),
      _ligne(t('Énergie rechargée'), '${nombre(e['total_quantite'])} kWh'),
      _ligne(t('Montant'), euros(e['total_montant']), gras: true),
      if (prix != null) _ligne(t('Prix moyen'), '${nombre(prix, decimales: 3)} €/kWh'),
      if (conso != null)
        _ligne(t('Consommation moyenne'), () {
          final v = _u.consommation(conso, 'kWh');
          return '${nombre(v.$1)} ${v.$2}';
        }()),
      const SizedBox(height: 12),
      _graphiqueBarres([for (final m in e['par_mois'] as List) (m['mois'] as String, enDouble(m['montant']) ?? 0)],
          _couleurs['electricite']!, euros: true),
      const SizedBox(height: 12),
      Text(t('Par lieu de recharge'), style: Theme.of(context).textTheme.titleSmall),
      for (final g in e['par_type'] as List)
        _ligne('${lieuxRecharge[g['code']] ?? t('Autre')} · ${nombre(g['quantite'])} kWh', euros(g['montant'])),
    ]));
  }

  // ------------------------------------------------------------------ Financement
  Widget _blocFinancement(Map<String, dynamic> f, List echeancier) {
    return _carte('${t('Financement')} · ${typesAchat[f['type_achat']] ?? ''}', Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (f['mensualite'] != null) _ligne(t('Mensualité'), euros(f['mensualite'])),
        _ligne(t('Payé à ce jour'), euros(f['paye_a_ce_jour']), gras: true),
        if (f['reste_a_payer'] != null) _ligne(t('Reste à payer'), euros(f['reste_a_payer']), gras: true),
        _ligne(t('Mois payés'), '${f['mois_payes']}${f['duree_mois'] != null ? ' / ${f['duree_mois']}' : ''}'),
        if (f['date_fin'] != null) _ligne(t('Fin du contrat'), dateFr(f['date_fin'])),
        if (f['capital_restant'] != null) _ligne(t('Capital restant dû'), euros(f['capital_restant'])),
        if (f['interets_a_ce_jour'] != null) _ligne(t('Intérêts payés à ce jour'), euros(f['interets_a_ce_jour'])),
        if (f['interets_totaux'] != null) _ligne(t('Coût total du crédit (intérêts)'), euros(f['interets_totaux'])),
        if (f['cout_total_contrat'] != null) _ligne(t('Coût total du contrat'), euros(f['cout_total_contrat'])),
        if ((enDouble(f['depassement_km']) ?? 0) > 0)
          _ligne(t('Dépassement à ce jour : {km}', {'km': km(f['depassement_km'], _u)}),
              f['cout_depassement'] == null ? '' : euros(f['cout_depassement'])),
        if (echeancier.isNotEmpty) ...[
          const SizedBox(height: 12),
          Text(t('Payé et reste à payer'), style: Theme.of(context).textTheme.titleSmall),
          const SizedBox(height: 8),
          SizedBox(height: 200, child: _graphiqueEcheancier(echeancier)),
          const SizedBox(height: 4),
          Wrap(spacing: 12, children: [
            _pastille(const Color(0xFF16A34A), t('Payé')),
            _pastille(const Color(0xFFEF4444), t('Reste à payer')),
          ]),
        ],
      ],
    ));
  }

  Widget _pastille(Color c, String texte) => Row(mainAxisSize: MainAxisSize.min, children: [
        Container(width: 10, height: 10, color: c),
        const SizedBox(width: 4),
        Text(texte, style: const TextStyle(fontSize: 12)),
      ]);

  // ------------------------------------------------------------------ Graphiques
  String _etiquetteMois(String mois) {
    final parties = mois.split('-');
    return parties.length == 2 ? '${parties[1]}/${parties[0].substring(2)}' : mois;
  }

  SideTitles _axeMois(List<String> mois) => SideTitles(
        showTitles: true,
        reservedSize: 22,
        interval: 1,
        getTitlesWidget: (v, meta) {
          final i = v.toInt();
          // Une étiquette sur deux au-delà de 8 mois (lisibilité)
          if (i < 0 || i >= mois.length || (mois.length > 8 && i % 2 == 1)) return const SizedBox.shrink();
          return Padding(
            padding: const EdgeInsets.only(top: 4),
            child: Text(_etiquetteMois(mois[i]), style: const TextStyle(fontSize: 9)),
          );
        },
      );

  FlTitlesData _titres(List<String> mois) => FlTitlesData(
        topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        leftTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            reservedSize: 44,
            getTitlesWidget: (v, meta) => Text(nombre(v, decimales: 0), style: const TextStyle(fontSize: 9)),
          ),
        ),
        bottomTitles: AxisTitles(sideTitles: _axeMois(mois)),
      );

  Widget _graphiqueBarres(List<(String, double)> valeurs, Color couleur, {bool euros = false}) {
    if (valeurs.every((v) => v.$2 == 0)) {
      return Padding(padding: const EdgeInsets.all(12), child: Text(t('Aucune donnée sur la période.')));
    }
    final mois = [for (final v in valeurs) v.$1];
    return SizedBox(
      height: 180,
      child: BarChart(BarChartData(
        gridData: const FlGridData(show: true, drawVerticalLine: false),
        borderData: FlBorderData(show: false),
        titlesData: _titres(mois),
        barTouchData: BarTouchData(
          touchTooltipData: BarTouchTooltipData(
            getTooltipItem: (groupe, _, barre, __) => BarTooltipItem(
              '${_etiquetteMois(mois[groupe.x])}\n${euros ? format.euros(barre.toY) : nombre(barre.toY, decimales: 0)}',
              const TextStyle(color: Colors.white, fontSize: 11),
            ),
          ),
        ),
        barGroups: [
          for (var i = 0; i < valeurs.length; i++)
            BarChartGroupData(x: i, barRods: [
              BarChartRodData(toY: valeurs[i].$2, color: couleur, width: 12, borderRadius: BorderRadius.circular(3)),
            ]),
        ],
      )),
    );
  }

  Widget _graphiqueCouts(Map<String, dynamic> couts) {
    final parMois = [for (final m in couts['par_mois'] as List) Map<String, dynamic>.from(m as Map)];
    if (parMois.every((m) => (enDouble(m['total']) ?? 0) == 0)) {
      return Padding(padding: const EdgeInsets.all(12), child: Text(t('Aucune donnée sur la période.')));
    }
    final mois = [for (final m in parMois) m['mois'] as String];
    return SizedBox(
      height: 220,
      child: BarChart(BarChartData(
        gridData: const FlGridData(show: true, drawVerticalLine: false),
        borderData: FlBorderData(show: false),
        titlesData: _titres(mois),
        barTouchData: BarTouchData(
          touchTooltipData: BarTouchTooltipData(
            getTooltipItem: (groupe, _, barre, __) => BarTooltipItem(
              '${_etiquetteMois(mois[groupe.x])}\n${format.euros(barre.toY)}',
              const TextStyle(color: Colors.white, fontSize: 11),
            ),
          ),
        ),
        barGroups: [
          for (var i = 0; i < parMois.length; i++)
            () {
              var cumul = 0.0;
              final segments = <BarChartRodStackItem>[];
              for (final e in _couleurs.entries) {
                final v = enDouble(parMois[i][e.key]) ?? 0;
                if (v > 0) segments.add(BarChartRodStackItem(cumul, cumul + v, e.value));
                cumul += v;
              }
              return BarChartGroupData(x: i, barRods: [
                BarChartRodData(toY: cumul, rodStackItems: segments, width: 14, borderRadius: BorderRadius.circular(3)),
              ]);
            }(),
        ],
      )),
    );
  }

  Widget _graphiqueEcheancier(List echeancier) {
    final points = [for (final e in echeancier) Map<String, dynamic>.from(e as Map)];
    final dates = [for (final p in points) DateTime.tryParse('${p['date']}') ?? DateTime.now()];
    final premier = dates.first;
    double x(DateTime d) => (d.year - premier.year) * 12.0 + d.month - premier.month;
    LineChartBarData courbe(String cle, Color c) => LineChartBarData(
          spots: [for (var i = 0; i < points.length; i++) FlSpot(x(dates[i]), enDouble(points[i][cle]) ?? 0)],
          color: c,
          barWidth: 3,
          dotData: const FlDotData(show: false),
          belowBarData: BarAreaData(show: true, color: c.withValues(alpha: 0.12)),
        );
    final maintenant = x(DateTime.now());
    return LineChart(LineChartData(
      gridData: const FlGridData(show: true, drawVerticalLine: false),
      borderData: FlBorderData(show: false),
      extraLinesData: ExtraLinesData(verticalLines: [
        VerticalLine(x: maintenant, color: Colors.grey, strokeWidth: 1, dashArray: [4, 4]),
      ]),
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
            reservedSize: 22,
            interval: 12,
            getTitlesWidget: (v, meta) => Text('${premier.year + (premier.month - 1 + v.toInt()) ~/ 12}',
                style: const TextStyle(fontSize: 9)),
          ),
        ),
      ),
      lineBarsData: [courbe('paye', const Color(0xFF16A34A)), courbe('reste', const Color(0xFFEF4444))],
    ));
  }
}

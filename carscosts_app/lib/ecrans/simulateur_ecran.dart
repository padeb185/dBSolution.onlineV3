import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../api/api_client.dart';
import '../api/session.dart';
import '../l10n/langue.dart';
import '../modeles/ressources.dart';
import '../widgets/format.dart';
import 'formules_ecran.dart';

/// Ouvre le simulateur d'achat (formule Bronze minimum).
Future<void> ouvrirSimulateur(BuildContext context) async {
  if (context.read<Abonnement>().formule == 'gratuit') {
    await Navigator.push(context, MaterialPageRoute(
        builder: (_) => FormulesEcran(raison: t('Le simulateur d\'achat est disponible à partir de la formule Bronze.'))));
    return;
  }
  await Navigator.push(context, MaterialPageRoute(builder: (_) => const SimulateurEcran()));
}

/// Simulateur d'achat : prêt auto, taxes de mise en circulation, taxe de roulage, immatriculation et plaques,
/// rapport financier de l'éventuel achat (BE, FR, LU, NL, DE).
class SimulateurEcran extends StatefulWidget {
  const SimulateurEcran({super.key});

  @override
  State<SimulateurEcran> createState() => _SimulateurEcranState();
}

class _SimulateurEcranState extends State<SimulateurEcran> {
  static const _champs = [
    'prix', 'co2', 'kw', 'cylindree', 'masse', 'age', 'cv_fiscaux', 'apport', 'duree_mois', 'taux', 'annees_detention',
    'km_an', 'conso', 'prix_energie', 'assurance_an', 'entretien_an', 'valeur_revente',
  ];
  static const _defauts = {
    'duree_mois': '60', 'taux': '4.9', 'annees_detention': '5', 'km_an': '15000', 'conso': '6', 'prix_energie': '1.75',
    'age': '0', 'apport': '0',
  };

  final Map<String, TextEditingController> _c = {
    for (final n in _champs) n: TextEditingController(text: _defauts[n] ?? ''),
  };
  String _pays = 'BE';
  String _region = 'wallonie';
  String _energie = 'essence';
  bool _plaquePerso = false;
  bool _envoi = false;
  /// Montants imposés à la main : code de la ligne (tmc, carte_grise, malus, bpm, plaques…) ou « annuel » → montant
  final Map<String, String> _forces = {};
  Map<String, dynamic>? _resultat;

  static const _pays5 = {'BE': 'Belgique', 'FR': 'France', 'LU': 'Luxembourg', 'NL': 'Pays-Bas', 'DE': 'Allemagne'};

  Map<String, String> get _regionsBe =>
      {'wallonie': t('Wallonie'), 'bruxelles': t('Bruxelles'), 'flandre': t('Flandre')};

  @override
  void initState() {
    super.initState();
    final p = '${context.read<Session>().utilisateur?['pays_defaut'] ?? 'BE'}'.toUpperCase();
    if (_pays5.containsKey(p)) _pays = p;
    _region = _pays == 'FR' ? 'IDF' : 'wallonie';
  }

  @override
  void dispose() {
    for (final c in _c.values) {
      c.dispose();
    }
    super.dispose();
  }

  Future<void> _calculer() async {
    FocusScope.of(context).unfocus();
    setState(() => _envoi = true);
    try {
      final r = await context.read<ApiClient>().post('simulateur/', {
        for (final n in _champs)
          if (_c[n]!.text.trim().isNotEmpty) n: _c[n]!.text.trim().replaceAll(',', '.').replaceAll(' ', ''),
        'pays': _pays,
        'region': _region,
        'energie': _energie,
        'plaque_personnalisee': _plaquePerso,
        for (final e in _forces.entries) 'force_${e.key}': e.value,
      });
      if (mounted) setState(() => _resultat = Map<String, dynamic>.from(r as Map));
    } on ApiException catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    } finally {
      if (mounted) setState(() => _envoi = false);
    }
  }

  // ------------------------------------------------------------------ Saisie
  Widget _champ(String nom, String libelle, {String? suffixe, String? aide}) => Padding(
        padding: const EdgeInsets.only(bottom: 10),
        child: TextField(
          controller: _c[nom],
          keyboardType: const TextInputType.numberWithOptions(decimal: true),
          decoration: InputDecoration(
              labelText: libelle, suffixText: suffixe, helperText: aide, helperMaxLines: 2,
              border: const OutlineInputBorder(), isDense: true),
        ),
      );

  Widget _deux(Widget a, Widget b) => Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Expanded(child: a),
        const SizedBox(width: 10),
        Expanded(child: b),
      ]);

  Widget _liste(String libelle, String valeur, Map<String, String> options, ValueChanged<String> choisir) => Padding(
        padding: const EdgeInsets.only(bottom: 10),
        child: DropdownButtonFormField<String>(
          key: ValueKey('$libelle-$valeur'),
          initialValue: options.containsKey(valeur) ? valeur : options.keys.first,
          isExpanded: true,
          decoration: InputDecoration(labelText: libelle, border: const OutlineInputBorder(), isDense: true),
          items: [for (final e in options.entries) DropdownMenuItem(value: e.key, child: Text(e.value, overflow: TextOverflow.ellipsis))],
          onChanged: (v) => choisir(v ?? options.keys.first),
        ),
      );

  Widget _titre(String texte) => Padding(
        padding: const EdgeInsets.fromLTRB(0, 12, 0, 8),
        child: Text(texte, style: Theme.of(context).textTheme.titleMedium),
      );

  /// Imposer un montant (ex. taxe lue sur le calculateur officiel) ; vide : montant calculé.
  Future<void> _imposer(String code, String libelle, dynamic actuel) async {
    final ctrl = TextEditingController(text: _forces[code] ?? '${enDouble(actuel) ?? ''}');
    final choix = await showDialog<String>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(libelle),
        content: Column(mainAxisSize: MainAxisSize.min, children: [
          Text(t('Montant imposé (par exemple lu sur le calculateur officiel).')),
          const SizedBox(height: 12),
          TextField(
            controller: ctrl,
            autofocus: true,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            decoration: const InputDecoration(suffixText: '€', border: OutlineInputBorder()),
          ),
        ]),
        actions: [
          if (_forces.containsKey(code))
            TextButton(onPressed: () => Navigator.pop(ctx, ''), child: Text(t('Montant calculé'))),
          TextButton(onPressed: () => Navigator.pop(ctx), child: Text(t('Annuler'))),
          FilledButton(onPressed: () => Navigator.pop(ctx, ctrl.text.trim()), child: Text(t('Appliquer'))),
        ],
      ),
    );
    if (choix == null || !mounted) return;
    setState(() {
      final valeur = choix.replaceAll(',', '.').replaceAll(' ', '');
      if (valeur.isEmpty || double.tryParse(valeur) == null) {
        _forces.remove(code);
      } else {
        _forces[code] = valeur;
      }
    });
    await _calculer();
  }

  /// Ligne de taxe modifiable : montant (imposé ou calculé) + crayon
  Widget _ligneModifiable(String code, String libelle, dynamic montant) {
    final impose = _forces.containsKey(code);
    return InkWell(
      onTap: () => _imposer(code, libelle, montant),
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 3),
        child: Row(children: [
          Expanded(
            child: Text.rich(TextSpan(children: [
              TextSpan(text: libelle),
              if (impose)
                TextSpan(text: '  ${t('imposé')}',
                    style: TextStyle(fontSize: 11, color: Theme.of(context).colorScheme.primary, fontWeight: FontWeight.w600)),
            ])),
          ),
          Text(euros(montant), style: TextStyle(fontWeight: impose ? FontWeight.bold : null)),
          const SizedBox(width: 6),
          Icon(Icons.edit, size: 16, color: Theme.of(context).colorScheme.outline),
        ]),
      ),
    );
  }

  // ------------------------------------------------------------------ Résultats
  Widget _ligne(String libelle, dynamic montant, {bool gras = false, Color? couleur}) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 3),
        child: Row(children: [
          Expanded(child: Text(libelle, style: gras ? const TextStyle(fontWeight: FontWeight.bold) : null)),
          Text(montant is String ? montant : euros(montant),
              style: TextStyle(fontWeight: gras ? FontWeight.bold : null, color: couleur)),
        ]),
      );

  Widget _carte(String titre, List<Widget> enfants) => Card(
        margin: const EdgeInsets.only(bottom: 12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(titre, style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            ...enfants,
          ]),
        ),
      );

  static const _palette = [
    Color(0xFF2563EB), Color(0xFFF59E0B), Color(0xFFEF4444), Color(0xFF8B5CF6), Color(0xFF10B981),
    Color(0xFF06B6D4), Color(0xFFEC4899),
  ];

  List<Widget> _resultats() {
    final r = _resultat!;
    final taxes = Map<String, dynamic>.from(r['taxes_achat'] as Map);
    final pret = (r['pret'] as Map?)?.cast<String, dynamic>();
    final rap = Map<String, dynamic>.from(r['rapport'] as Map);
    final postes = (rap['postes'] as List).cast<Map>();
    final total = postes.fold<double>(0, (s, p) => s + (enDouble(p['montant']) ?? 0));
    return [
      // Avertissement : montants indicatifs, modifiables
      Card(
        color: Colors.amber.shade50,
        margin: const EdgeInsets.only(bottom: 12),
        child: ListTile(
          leading: Icon(Icons.info_outline, color: Colors.amber.shade900),
          title: Text(t('Montants indicatifs (règles 2026)')),
          subtitle: Text(t('Vérifiez sur les calculateurs officiels. Touchez une taxe pour imposer votre propre montant.')),
        ),
      ),
      _carte(t('À l\'achat : taxes, immatriculation et plaques'), [
        for (final l in (taxes['lignes'] as List).cast<Map>())
          _ligneModifiable('${l['code']}', '${l['libelle']}', l['montant']),
        const Divider(),
        _ligne(t('Total'), taxes['total'], gras: true),
        _ligne(t('À payer à l\'achat (apport ou prix + taxes)'), rap['a_payer_achat'], gras: true),
      ]),
      _carte(t('Chaque année'), [
        _ligneModifiable('annuel', t('Taxe de circulation'), r['taxe_annuelle']),
        _ligne(t('Carburant / énergie'), rap['energie_an']),
        _ligne(t('Budget mensuel (mensualité + frais annuels / 12)'), rap['budget_mensuel'], gras: true),
      ]),
      if (pret != null)
        _carte(t('Prêt auto'), [
          _ligne(t('Montant emprunté'), pret['capital']),
          _ligne(t('Mensualité ({n} mois à {taux} %)', {'n': pret['duree_mois'], 'taux': nombre(pret['taux'], decimales: 2)}),
              pret['mensualite'], gras: true),
          _ligne(t('Total remboursé'), pret['total_rembourse']),
          _ligne(t('Coût du crédit (intérêts)'), pret['cout_credit'], couleur: Colors.red),
          const SizedBox(height: 8),
          Text(t('Capital restant dû'), style: Theme.of(context).textTheme.labelLarge),
          for (final a in (pret['tableau'] as List).cast<Map>())
            _ligne(t('Après {n} mois', {'n': a['mois']}), a['capital_restant']),
        ]),
      _carte(t('Rapport financier sur {n} ans', {'n': nombre(rap['annees'], decimales: 0)}), [
        if (total > 0)
          SizedBox(
            height: 200,
            child: PieChart(PieChartData(
              sectionsSpace: 2,
              centerSpaceRadius: 50,
              sections: [
                for (var i = 0; i < postes.length; i++)
                  PieChartSectionData(
                    value: enDouble(postes[i]['montant']) ?? 0,
                    color: _palette[i % _palette.length],
                    radius: 44,
                    title: (enDouble(postes[i]['montant']) ?? 0) * 100 / total >= 6
                        ? '${((enDouble(postes[i]['montant']) ?? 0) * 100 / total).round()} %'
                        : '',
                    titleStyle: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.white),
                  ),
              ],
            )),
          ),
        const SizedBox(height: 8),
        for (var i = 0; i < postes.length; i++)
          Row(children: [
            Container(width: 10, height: 10, decoration: BoxDecoration(color: _palette[i % _palette.length], shape: BoxShape.circle)),
            const SizedBox(width: 8),
            Expanded(child: _ligne('${postes[i]['libelle']}', postes[i]['montant'])),
          ]),
        const Divider(),
        _ligne(t('Coût total'), rap['cout_total'], gras: true),
        _ligne(t('Valeur de revente estimée'), '− ${euros(rap['valeur_revente'])}', couleur: Colors.green),
        _ligne(t('Coût net'), rap['cout_net'], gras: true),
        _ligne(t('Coût net / mois'), rap['cout_mois']),
        if (rap['cout_km'] != null) _ligne(t('Coût net au km'), '${nombre(rap['cout_km'], decimales: 3)} €'),
        _ligne(t('Kilomètres sur la période'), km(rap['km_total'])),
      ]),
      for (final n in (r['notes'] as List)) Padding(
        padding: const EdgeInsets.only(bottom: 4),
        child: Text('• $n', style: Theme.of(context).textTheme.bodySmall),
      ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    final regionsFr = ((_resultat?['regions_fr'] as Map?) ?? {
      'ARA': 'Auvergne-Rhône-Alpes', 'BFC': 'Bourgogne-Franche-Comté', 'BRE': 'Bretagne', 'CVL': 'Centre-Val de Loire',
      'COR': 'Corse', 'GES': 'Grand Est', 'HDF': 'Hauts-de-France', 'IDF': 'Île-de-France', 'NOR': 'Normandie',
      'NAQ': 'Nouvelle-Aquitaine', 'OCC': 'Occitanie', 'PDL': 'Pays de la Loire', 'PAC': 'Provence-Alpes-Côte d\'Azur',
    }).map((k, v) => MapEntry('$k', '$v'));
    return Scaffold(
      appBar: AppBar(title: Text(t('Simulateur d\'achat'))),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        _titre(t('Véhicule')),
        _liste(t('Pays d\'immatriculation'), _pays, _pays5, (v) => setState(() {
              _pays = v;
              _forces.clear();
              _region = v == 'FR' ? 'IDF' : 'wallonie';
            })),
        if (_pays == 'BE') _liste(t('Région'), _region, _regionsBe, (v) => setState(() => _region = v)),
        if (_pays == 'FR') _liste(t('Région'), _region, regionsFr, (v) => setState(() => _region = v)),
        _liste(t('Énergie'), _energie, energies, (v) => setState(() => _energie = v)),
        _champ('prix', t('Prix d\'achat TVAC'), suffixe: '€'),
        _deux(_champ('co2', t('CO2 (WLTP)'), suffixe: 'g/km'), _champ('kw', t('Puissance'), suffixe: 'kW')),
        _deux(_champ('cylindree', t('Cylindrée'), suffixe: 'cm³'), _champ('masse', t('Masse'), suffixe: 'kg')),
        _deux(
          _champ('age', t('Âge du véhicule'), suffixe: t('ans'), aide: t('0 : neuf')),
          _pays == 'FR' ? _champ('cv_fiscaux', t('CV fiscaux'), aide: t('Vide : calculés')) : const SizedBox(),
        ),
        SwitchListTile(
          contentPadding: EdgeInsets.zero,
          title: Text(t('Plaque personnalisée')),
          value: _plaquePerso,
          onChanged: (v) => setState(() => _plaquePerso = v),
        ),
        _titre(t('Prêt auto')),
        _champ('apport', t('Apport'), suffixe: '€'),
        _deux(_champ('duree_mois', t('Durée (mois)')), _champ('taux', t('Taux annuel (TAEG, %)'), suffixe: '%')),
        _titre(t('Utilisation')),
        _deux(_champ('annees_detention', t('Durée de détention'), suffixe: t('ans')), _champ('km_an', t('Km par an'), suffixe: 'km')),
        _deux(_champ('conso', _energie == 'electrique' ? t('kWh / 100 km') : t('L / 100 km')),
            _champ('prix_energie', _energie == 'electrique' ? t('Prix du kWh') : t('Prix du litre'), suffixe: '€')),
        _deux(_champ('assurance_an', t('Assurance / an'), suffixe: '€'), _champ('entretien_an', t('Entretien / an'), suffixe: '€')),
        _champ('valeur_revente', t('Valeur de revente estimée'), suffixe: '€',
            aide: t('Vide : −20 % la première année puis −15 % par an.')),
        const SizedBox(height: 8),
        FilledButton.icon(
          onPressed: _envoi ? null : _calculer,
          icon: _envoi
              ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2))
              : const Icon(Icons.calculate),
          label: Text(t('Calculer')),
        ),
        const SizedBox(height: 16),
        if (_resultat != null) ..._resultats(),
        const SizedBox(height: 24),
      ]),
    );
  }
}

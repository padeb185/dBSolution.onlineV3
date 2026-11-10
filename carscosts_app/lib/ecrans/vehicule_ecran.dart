import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../api/api_client.dart';
import '../l10n/langue.dart';
import '../l10n/unites.dart';
import '../modeles/ressources.dart';
import '../widgets/fichiers.dart';
import '../widgets/format.dart';
import '../widgets/liste_ressource.dart';
import '../widgets/logo_marque.dart';
import '../widgets/plaque.dart';
import 'deductibilite_onglet.dart';
import 'financement_ecran.dart';
import 'formulaire_ecran.dart';
import 'pneus_onglet.dart';
import 'vente_ecran.dart';
import 'rapport_onglet.dart';
import 'vehicule_form_ecran.dart';

/// Fiche d'un véhicule : synthèse des coûts et onglets (pleins, entretiens, rappels, documents…).
class VehiculeEcran extends StatefulWidget {
  const VehiculeEcran({super.key, required this.vehicule});

  final Map<String, dynamic> vehicule;

  @override
  State<VehiculeEcran> createState() => _VehiculeEcranState();
}

class _VehiculeEcranState extends State<VehiculeEcran> {
  late Map<String, dynamic> _vehicule = widget.vehicule;
  late Future<Map<String, dynamic>> _synthese;

  String get _id => _vehicule['id'] as String;

  @override
  void initState() {
    super.initState();
    _chargerSynthese();
  }

  void _chargerSynthese() {
    _synthese = context
        .read<ApiClient>()
        .get('vehicules/$_id/synthese/')
        .then((r) => Map<String, dynamic>.from(r as Map));
  }

  Future<void> _modifier() async {
    final ok = await Navigator.push<bool>(
        context, MaterialPageRoute(builder: (_) => VehiculeFormEcran(vehicule: _vehicule)));
    if (ok == true && mounted) {
      final v = await context.read<ApiClient>().get('vehicules/$_id/');
      setState(() {
        _vehicule = Map<String, dynamic>.from(v as Map);
        _chargerSynthese();
      });
    }
  }

  Future<void> _ajouter(Ressource r) async {
    final ok = await Navigator.push<bool>(
        context, MaterialPageRoute(builder: (_) => FormulaireEcran(ressource: r, vehiculeId: _id, vehicule: _vehicule)));
    if (ok == true) setState(_chargerSynthese);
  }

  @override
  Widget build(BuildContext context) {
    final titre = '${_vehicule['marque']} ${_vehicule['modele']}';
    return DefaultTabController(
      length: ressourcesDe(_vehicule).length + 4,
      child: Scaffold(
        appBar: AppBar(
          title: Row(children: [
            LogoMarque(marque: _vehicule['marque'] as String?, taille: 32),
            const SizedBox(width: 10),
            Expanded(child: Text(titre, overflow: TextOverflow.ellipsis)),
          ]),
          actions: [IconButton(icon: const Icon(Icons.edit), tooltip: t('Modifier'), onPressed: _modifier)],
          bottom: TabBar(
            isScrollable: true,
            tabAlignment: TabAlignment.start,
            tabs: [
              Tab(icon: const Icon(Icons.insights), text: t('Résumé')),
              Tab(icon: const Icon(Icons.bar_chart), text: t('Rapport')),
              Tab(icon: const Icon(Icons.account_balance_wallet), text: t('Déductibilité')),
              for (final r in ressourcesDe(_vehicule)) Tab(icon: Icon(r.icone), text: r.titre),
              Tab(icon: const Icon(Icons.tire_repair), text: t('Pneus')),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            _resume(),
            RapportOnglet(key: ValueKey('rapport-${_vehicule['updated_at']}'), vehicule: _vehicule),
            DeductibiliteOnglet(key: ValueKey('deductibilite-${_vehicule['updated_at']}'), vehicule: _vehicule),
            for (final r in ressourcesDe(_vehicule))
              ListeRessource(
                  ressource: r, vehiculeId: _id, vehicule: _vehicule, auChangement: () => setState(_chargerSynthese)),
            PneusOnglet(vehicule: _vehicule, auChangement: () => setState(_chargerSynthese)),
          ],
        ),
      ),
    );
  }

  // ------------------------------------------------------------------ Résumé
  Widget _resume() {
    return RefreshIndicator(
      onRefresh: () async {
        setState(_chargerSynthese);
        await _synthese;
      },
      child: FutureBuilder<Map<String, dynamic>>(
        future: _synthese,
        builder: (context, snap) {
          if (snap.connectionState != ConnectionState.done) return const Center(child: CircularProgressIndicator());
          if (snap.hasError) return ListView(children: [Padding(padding: const EdgeInsets.all(24), child: Text('${snap.error}'))]);
          final s = snap.data!;
          final u = Unites.de(_vehicule);
          String conso(dynamic valeur, String uniteServeur) {
            final c = u.consommation(enDouble(valeur) ?? 0, uniteServeur);
            return '${nombre(c.$1)} ${c.$2}';
          }
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              if (_vehicule['photo'] != null) ImageProtegee(url: _vehicule['photo'] as String, hauteur: 180),
              const SizedBox(height: 8),
              if ((_vehicule['immatriculation'] ?? '').toString().isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: Plaque(
                        numero: _vehicule['immatriculation'].toString(),
                        pays: _vehicule['pays_immatriculation'] as String?,
                        hauteur: 34),
                  ),
                ),
              Text([
                if ((_vehicule['vin'] ?? '').toString().isNotEmpty) 'VIN ${_vehicule['vin']}',
                energies[_vehicule['energie']],
              ].join(' · ')),
              const SizedBox(height: 12),
              Wrap(spacing: 8, runSpacing: 8, children: [
                if (_vehicule['energie'] != 'electrique')
                  FilledButton.tonalIcon(
                    onPressed: () => _ajouter(pleins),
                    icon: const Icon(Icons.local_gas_station),
                    label: Text(t('Plein')),
                  ),
                if (_vehicule['energie'] == 'electrique' || _vehicule['energie'] == 'phev')
                  FilledButton.tonalIcon(
                    onPressed: () => _ajouter(recharges),
                    icon: const Icon(Icons.ev_station),
                    label: Text(t('Recharge')),
                  ),
                FilledButton.tonalIcon(
                  onPressed: () => _ajouter(kilometrages),
                  icon: const Icon(Icons.speed),
                  label: Text(t('Kilométrage')),
                ),
                FilledButton.tonalIcon(
                  onPressed: () => _ajouter(entretiens),
                  icon: const Icon(Icons.build),
                  label: Text(t('Entretien')),
                ),
              ]),
              const SizedBox(height: 12),
              // Type d'achat (formule Bronze minimum) : comptant, prêt, leasing, renting
              Card(
                child: ListTile(
                  leading: const Icon(Icons.account_balance),
                  title: Text(t('Type d\'achat : {type}', {'type': typesAchat[s['type_achat']] ?? t('Comptant')})),
                  subtitle: (s['financement'] as Map?)?['mensualite'] == null
                      ? null
                      : Text(t('Mensualité {montant} · reste {reste}', {
                          'montant': euros((s['financement'] as Map)['mensualite']),
                          'reste': euros((s['financement'] as Map)['reste_a_payer']),
                        })),
                  trailing: context.watch<Abonnement>().formule == 'gratuit'
                      ? const Chip(label: Text('Bronze'))
                      : const Icon(Icons.chevron_right),
                  onTap: () async {
                    if (await ouvrirFinancement(context, _vehicule) && mounted) setState(_chargerSynthese);
                  },
                ),
              ),
              // (Re)vente (formule Bronze minimum) : acheteur, prix, documents, bilan, certificat de cession
              Card(
                child: ListTile(
                  leading: Icon(_vehicule['archive'] == true ? Icons.verified : Icons.sell),
                  title: Text(_vehicule['archive'] == true ? t('Vente du véhicule (vendu)') : t('Vendre le véhicule')),
                  subtitle: Text(t('Acheteur, prix, documents remis, bilan, certificat de cession')),
                  trailing: context.watch<Abonnement>().formule == 'gratuit'
                      ? const Chip(label: Text('Bronze'))
                      : const Icon(Icons.chevron_right),
                  onTap: () async {
                    if (await ouvrirVente(context, _vehicule) && mounted) {
                      final v = await context.read<ApiClient>().get('vehicules/$_id/');
                      if (mounted) {
                        setState(() {
                          _vehicule = Map<String, dynamic>.from(v as Map);
                          _chargerSynthese();
                        });
                      }
                    }
                  },
                ),
              ),
              const SizedBox(height: 12),
              GridView.count(
                crossAxisCount: MediaQuery.sizeOf(context).width > 700 ? 4 : 2,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                childAspectRatio: 2.2,
                mainAxisSpacing: 8,
                crossAxisSpacing: 8,
                children: [
                  _kpi(t('Kilométrage'), km(s['kilometrage_actuel'], u)),
                  _kpi(t('Coût total'), euros(s['cout_total'])),
                  _kpi(t('Coût net'), euros(s['cout_net'])),
                  _kpi(u.miles ? t('Coût net au mile') : t('Coût net au km'),
                      s['cout_total_km'] == null
                          ? '—'
                          : '${nombre(u.coutParDistance(enDouble(s['cout_total_km']) ?? 0), decimales: 3)} €'),
                  _kpi(t('Coût net / mois'), euros(s['cout_mois'])),
                  _kpi(t('Consommation'), s['consommation_moyenne'] == null
                      ? '—'
                      : conso(s['consommation_moyenne'], '${s['consommation_unite'] ?? 'L'}')),
                  if (s['consommation_electrique'] != null)
                    _kpi(t('Consommation électrique'), conso(s['consommation_electrique'], 'kWh')),
                  _kpi(t('Valeur de revente'), euros(s['valeur_revente'])),
                ],
              ),
              const SizedBox(height: 16),
              Text(t('Répartition des coûts'), style: Theme.of(context).textTheme.titleMedium),
              Card(
                child: Column(children: [
                  for (final p in (s['postes'] as List).cast<Map>())
                    ListTile(dense: true, title: Text(_libellePoste(p, s)), trailing: Text(euros(p['montant']))),
                  ListTile(
                    title: Text(t('Coût total'), style: const TextStyle(fontWeight: FontWeight.bold)),
                    trailing: Text(euros(s['cout_total']), style: const TextStyle(fontWeight: FontWeight.bold)),
                  ),
                  ListTile(
                    dense: true,
                    title: Text(t('Valeur de revente estimée')),
                    subtitle: s['valeur_revente'] == null ? Text(t('À renseigner dans la fiche du véhicule')) : null,
                    trailing: Text(s['valeur_revente'] == null ? '—' : '− ${euros(s['valeur_revente'])}'),
                  ),
                  ListTile(
                    title: Text(t('Coût net'), style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text(t('Coût total − valeur de revente')),
                    trailing: Text(euros(s['cout_net']), style: const TextStyle(fontWeight: FontWeight.bold)),
                  ),
                ]),
              ),
              const SizedBox(height: 16),
              if ((s['par_annee'] as List).isNotEmpty) ...[
                Text(t('Dépenses par année'), style: Theme.of(context).textTheme.titleMedium),
                const SizedBox(height: 8),
                SizedBox(height: 220, child: _graphique((s['par_annee'] as List).cast<Map>())),
                const SizedBox(height: 8),
                Wrap(spacing: 12, children: [
                  for (final l in _legende) Row(mainAxisSize: MainAxisSize.min, children: [
                    Container(width: 12, height: 12, color: l.$2),
                    const SizedBox(width: 4),
                    Text(l.$1, style: const TextStyle(fontSize: 12)),
                  ]),
                ]),
              ],
            ],
          );
        },
      ),
    );
  }

  Widget _kpi(String libelle, String valeur) => Card(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisAlignment: MainAxisAlignment.center, children: [
            // Une seule ligne : un libellé trop long est raccourci (évite « BOTTOM OVERFLOWED »)
            Text(libelle, maxLines: 1, overflow: TextOverflow.ellipsis, style: Theme.of(context).textTheme.bodySmall),
            const SizedBox(height: 2),
            FittedBox(child: Text(valeur, style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold))),
          ]),
        ),
      );

  static const _cles = ['energie', 'entretiens', 'documents', 'autres'];
  static List<(String, Color)> get _legende => [
        (t('Énergie'), const Color(0xFF2563EB)),
        (t('Entretiens'), const Color(0xFFF59E0B)),
        (t('Documents / assurance'), const Color(0xFF10B981)),
        (t('Autres'), const Color(0xFF8B5CF6)),
      ];

  /// Libellé d'un poste de coût, traduit d'après son code (achat, energie, depense_taxe…).
  String _libellePoste(Map p, Map s) {
    final code = '${p['code']}';
    if (code.startsWith('depense_')) return categoriesDepense[code.substring(8)] ?? '${p['libelle']}';
    return switch (code) {
      'achat' => s['type_achat'] == 'leasing' ? t('Option d\'achat levée') : t('Prix d\'achat'),
      'interets' => t('Intérêts du prêt (à ce jour)'),
      'loyers' => t('Loyers payés (à ce jour)'),
      'energie' => t('Carburant / énergie'),
      'entretiens' => t('Entretiens et réparations'),
      'documents' => t('Assurance, contrôle technique, documents'),
      _ => '${p['libelle']}',
    };
  }

  Widget _graphique(List<Map> annees) {
    return BarChart(
      BarChartData(
        gridData: const FlGridData(show: true, drawVerticalLine: false),
        borderData: FlBorderData(show: false),
        titlesData: FlTitlesData(
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          leftTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              reservedSize: 48,
              getTitlesWidget: (v, meta) => Text(nombre(v, decimales: 0), style: const TextStyle(fontSize: 10)),
            ),
          ),
          bottomTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              getTitlesWidget: (v, meta) => Text('${v.toInt()}', style: const TextStyle(fontSize: 11)),
            ),
          ),
        ),
        barGroups: [
          for (final a in annees)
            () {
              var cumul = 0.0;
              final segments = <BarChartRodStackItem>[];
              for (var i = 0; i < _cles.length; i++) {
                final v = enDouble(a[_cles[i]]) ?? 0;
                segments.add(BarChartRodStackItem(cumul, cumul + v, _legende[i].$2));
                cumul += v;
              }
              return BarChartGroupData(
                x: (a['annee'] as num).toInt(),
                barRods: [
                  BarChartRodData(toY: cumul, rodStackItems: segments, width: 22, borderRadius: BorderRadius.circular(4)),
                ],
              );
            }(),
        ],
      ),
    );
  }
}

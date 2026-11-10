import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../api/api_client.dart';
import '../l10n/langue.dart';
import '../modeles/pays.dart';
import '../modeles/ressources.dart';
import '../widgets/format.dart';
import 'formules_ecran.dart';

/// Déductibilité des frais du véhicule (TVA récupérable, frais déductibles à l'impôt)
/// selon les règles du pays d'immatriculation. Formule Bronze minimum.
class DeductibiliteOnglet extends StatefulWidget {
  const DeductibiliteOnglet({super.key, required this.vehicule});

  final Map<String, dynamic> vehicule;

  @override
  State<DeductibiliteOnglet> createState() => _DeductibiliteOngletState();
}

class _DeductibiliteOngletState extends State<DeductibiliteOnglet> with AutomaticKeepAliveClientMixin {
  int _annee = DateTime.now().year;
  late Future<Map<String, dynamic>> _donnees;

  // TVA à récupérer (usage professionnel) : par trimestre ou par mois
  String _periodeTva = 'trimestre';
  Future<Map<String, dynamic>>? _journal;

  // Profil fiscal en cours de saisie
  String _statut = 'independant';
  double _usage = 100;
  final _co2 = TextEditingController();
  final _tvaManuel = TextEditingController();
  final _impotManuel = TextEditingController();
  int _duree = 5;
  String? _dateCommande;
  bool _profilCharge = false;
  bool _envoi = false;
  Map<String, String> _erreurs = {};

  String get _chemin => 'vehicules/${widget.vehicule['id']}/deductibilite/';

  @override
  bool get wantKeepAlive => true;

  Map<String, String> get _statuts => {
        'particulier': t('Particulier (usage privé)'),
        'independant': t('Indépendant / profession libérale'),
        'societe': t('Société (voiture de société)'),
      };

  Map<String, String> get _libelles => {
        'carburant': t('Carburant'),
        'electricite': t('Électricité'),
        'entretien': t('Entretiens et réparations'),
        'maintenances': t('Maintenances (garage)'),
        'assurances_taxes': t('Assurances et taxes (sans TVA)'),
        'amendes': t('Amendes (non déductibles)'),
        'autres': t('Autres frais (parking, lavage, accessoires…)'),
        'achat_tva': t('Achat du véhicule (TVA)'),
        'amortissement': t('Amortissement de l\'achat'),
        'interets': t('Intérêts du prêt'),
        'location': t('Loyers leasing / renting'),
      };

  Map<String, String> get _familles => {
        'essence': t('Essence'),
        'diesel': t('Diesel'),
        'gpl': t('GPL'),
        'gnc': t('GNC'),
      };

  @override
  void initState() {
    super.initState();
    _charger();
  }

  @override
  void dispose() {
    _co2.dispose();
    _tvaManuel.dispose();
    _impotManuel.dispose();
    super.dispose();
  }

  void _chargerJournal() {
    _journal = context
        .read<ApiClient>()
        .get('vehicules/${widget.vehicule['id']}/tva/', params: {'annee': '$_annee', 'periode': _periodeTva})
        .then((r) => Map<String, dynamic>.from(r as Map));
  }

  String _libellePeriode(String p) {
    // « 2026-T2 » → « 2e trimestre 2026 » ; « 2026-05 » → « mai 2026 »
    final m = RegExp(r'^(\d{4})-T(\d)$').firstMatch(p);
    if (m != null) return t('Trimestre {n} {annee}', {'n': m.group(2), 'annee': m.group(1)});
    final d = DateTime.tryParse('$p-01');
    return d == null ? p : DateFormat.yMMMM(localeIntl).format(d);
  }

  Widget _tvaARecuperer() {
    return _carte(t('TVA à récupérer'), [
      Wrap(spacing: 8, children: [
        for (final e in {'trimestre': t('Par trimestre'), 'mois': t('Par mois')}.entries)
          ChoiceChip(
            label: Text(e.value),
            selected: _periodeTva == e.key,
            onSelected: (_) => setState(() {
              _periodeTva = e.key;
              _chargerJournal();
            }),
          ),
      ]),
      const SizedBox(height: 8),
      FutureBuilder<Map<String, dynamic>>(
        future: _journal,
        builder: (context, snap) {
          if (snap.connectionState != ConnectionState.done) {
            return const Padding(padding: EdgeInsets.all(16), child: Center(child: CircularProgressIndicator()));
          }
          if (snap.hasError || snap.data == null) return Text('${snap.error ?? ''}');
          final j = snap.data!;
          final periodes = (j['periodes'] as List? ?? []).cast<Map>();
          if (periodes.isEmpty) return Text(t('Aucune dépense avec TVA sur cette année.'));
          final style = Theme.of(context).textTheme.bodySmall;
          final totaux = Map<String, dynamic>.from(j['totaux'] as Map);
          return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            for (final p in periodes)
              ExpansionTile(
                tilePadding: EdgeInsets.zero,
                title: Text(_libellePeriode('${p['periode']}'), style: const TextStyle(fontWeight: FontWeight.w600)),
                subtitle: Text(t('TVA {tva} · à récupérer {recup}', {'tva': euros(p['tva']), 'recup': euros(p['tva_recuperable'])})),
                trailing: Text(euros(p['tva_recuperable']), style: const TextStyle(fontWeight: FontWeight.bold)),
                children: [
                  for (final o in (p['operations'] as List).cast<Map>())
                    ListTile(
                      dense: true,
                      contentPadding: const EdgeInsets.only(left: 8),
                      title: Text([dateFr(o['date']), _libelles[o['code']] ?? (o['code'] == 'pneus' ? t('Pneus') : '${o['code']}'),
                        if ('${o['libelle']}'.isNotEmpty) o['libelle']].join(' · ')),
                      subtitle: Text(
                          t('TTC {ttc} · HTVA {htva} · TVA {tva} ({pct} récupérable)', {
                            'ttc': euros(o['montant']), 'htva': euros(o['htva']), 'tva': euros(o['tva']),
                            'pct': _pct(o['taux_recuperable'])}),
                          style: style),
                      trailing: Text(euros(o['tva_recuperable'])),
                    ),
                ],
              ),
            const Divider(),
            Row(children: [
              Expanded(child: Text(t('Total {annee}', {'annee': _annee}), style: const TextStyle(fontWeight: FontWeight.bold))),
              Text(euros(totaux['tva_recuperable']), style: const TextStyle(fontWeight: FontWeight.bold)),
            ]),
            Text(t('TVA payée {tva} · HTVA {htva}', {'tva': euros(totaux['tva']), 'htva': euros(totaux['htva'])}), style: style),
          ]);
        },
      ),
    ]);
  }

  void _charger() {
    if (context.read<Abonnement>().formule == 'gratuit') {
      _donnees = Future.value(const {});
      return;
    }
    _chargerJournal();
    _donnees = context
        .read<ApiClient>()
        .get(_chemin, params: {'annee': '$_annee'})
        .then((r) => Map<String, dynamic>.from(r as Map))
        .then((d) {
      if (!_profilCharge) _remplirProfil(d);
      return d;
    });
  }

  String _texte(dynamic v) {
    if (v == null) return '';
    final d = enDouble(v);
    if (d == null) return '$v';
    return d == d.roundToDouble() ? d.toInt().toString() : d.toString();
  }

  void _remplirProfil(Map<String, dynamic> d) {
    final p = Map<String, dynamic>.from(d['profil'] as Map);
    _statut = p['statut'] as String? ?? 'independant';
    _usage = (enDouble(p['usage_pro']) ?? 100).clamp(0, 100).toDouble();
    _co2.text = _texte(p['co2']);
    _tvaManuel.text = _texte(p['taux_tva_manuel']);
    _impotManuel.text = _texte(p['taux_impot_manuel']);
    _duree = (p['duree_amortissement'] as num?)?.toInt() ?? 5;
    _dateCommande = p['date_commande'] as String?;
    _profilCharge = true;
  }

  Future<void> _enregistrer() async {
    String? nombreOuNull(TextEditingController c) => c.text.trim().isEmpty ? null : c.text.trim().replaceAll(',', '.');
    setState(() {
      _envoi = true;
      _erreurs = {};
    });
    try {
      final r = await context.read<ApiClient>().put('$_chemin?annee=$_annee', {
        'statut': _statut,
        'usage_pro': _usage.round(),
        'co2': int.tryParse(_co2.text.trim()),
        'date_commande': _dateCommande,
        'duree_amortissement': _duree,
        'taux_tva_manuel': nombreOuNull(_tvaManuel),
        'taux_impot_manuel': nombreOuNull(_impotManuel),
      });
      if (!mounted) return;
      setState(() {
        _donnees = Future.value(Map<String, dynamic>.from(r as Map));
        _chargerJournal();   // usage professionnel ou statut changé : TVA à récupérer recalculée
      });
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(t('Profil fiscal enregistré.'))));
    } on ApiException catch (e) {
      if (!mounted) return;
      setState(() => _erreurs = e.champs);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    } finally {
      if (mounted) setState(() => _envoi = false);
    }
  }

  // ------------------------------------------------------------------ Mise en page
  Widget _verrou() => ListView(padding: const EdgeInsets.all(24), children: [
        const Icon(Icons.lock_outline, size: 48),
        const SizedBox(height: 12),
        Text(t('La déductibilité est disponible à partir de la formule Bronze.'),
            textAlign: TextAlign.center, style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: 8),
        Text(t('TVA récupérable et frais déductibles selon les règles du pays d\'immatriculation.'),
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

  Widget _carte(String titre, List<Widget> enfants) => Card(
        margin: const EdgeInsets.only(bottom: 12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(titre, style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 12),
            ...enfants,
          ]),
        ),
      );

  Widget _kpi(String libelle, String valeur, {String? detail}) => Expanded(
        child: Card(
          margin: const EdgeInsets.only(right: 8, bottom: 12),
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(libelle, style: Theme.of(context).textTheme.bodySmall, maxLines: 2),
              const SizedBox(height: 4),
              FittedBox(
                fit: BoxFit.scaleDown,
                alignment: Alignment.centerLeft,
                child: Text(valeur, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
              ),
              if (detail != null) Text(detail, style: Theme.of(context).textTheme.bodySmall, maxLines: 3),
            ]),
          ),
        ),
      );

  Widget _choixAnnee() {
    final maintenant = DateTime.now().year;
    return Wrap(spacing: 8, children: [
      for (final a in [maintenant, maintenant - 1, maintenant - 2])
        ChoiceChip(
          label: Text('$a'),
          selected: _annee == a,
          onSelected: (_) => setState(() {
            _annee = a;
            _charger();
          }),
        ),
    ]);
  }

  String _pct(dynamic v) => '${nombre(v, decimales: 0)} %';

  Widget _profil() {
    final champ = (TextEditingController c, String libelle, String nom, {String suffixe = '%'}) => Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: TextField(
            controller: c,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            decoration: InputDecoration(
                labelText: libelle, suffixText: suffixe, errorText: _erreurs[nom], border: const OutlineInputBorder()),
          ),
        );
    return _carte(t('Profil fiscal du véhicule'), [
      DropdownButtonFormField<String>(
        key: ValueKey('statut-$_statut'),
        initialValue: _statut,
        isExpanded: true,
        decoration: InputDecoration(labelText: t('Statut'), border: const OutlineInputBorder()),
        items: [for (final e in _statuts.entries) DropdownMenuItem(value: e.key, child: Text(e.value))],
        onChanged: (v) => setState(() => _statut = v ?? 'independant'),
      ),
      const SizedBox(height: 12),
      if (_statut != 'particulier') ...[
        Text(t('Usage professionnel : {n} %', {'n': _usage.round()})),
        Slider(value: _usage, min: 0, max: 100, divisions: 20, label: '${_usage.round()} %',
            onChanged: (v) => setState(() => _usage = v)),
        champ(_co2, t('Émissions CO2 (g/km, WLTP)'), 'co2', suffixe: 'g/km'),
        InkWell(
          onTap: () async {
            final d = await showDatePicker(
              context: context,
              initialDate: DateTime.tryParse(_dateCommande ?? '') ?? DateTime.now(),
              firstDate: DateTime(2000),
              lastDate: DateTime(2100),
            );
            if (d != null) setState(() => _dateCommande = dateIso(d));
          },
          child: InputDecorator(
            decoration: InputDecoration(
              labelText: t('Date de commande / signature du contrat'),
              helperText: t('Belgique : détermine le régime (avant ou après le 01/07/2023). Vide : date d\'achat.'),
              helperMaxLines: 2,
              border: const OutlineInputBorder(),
              suffixIcon: _dateCommande == null
                  ? const Icon(Icons.calendar_today)
                  : IconButton(icon: const Icon(Icons.clear), onPressed: () => setState(() => _dateCommande = null)),
            ),
            child: Text(_dateCommande == null ? '—' : dateFr(_dateCommande)),
          ),
        ),
        const SizedBox(height: 12),
        DropdownButtonFormField<int>(
          key: ValueKey('duree-$_duree'),
          initialValue: _duree,
          decoration: InputDecoration(labelText: t('Amortissement de l\'achat'), border: const OutlineInputBorder()),
          items: [for (var n = 1; n <= 10; n++) DropdownMenuItem(value: n, child: Text(t('{n} ans', {'n': n})))],
          onChanged: (v) => setState(() => _duree = v ?? 5),
        ),
        const SizedBox(height: 4),
        ExpansionTile(
          tilePadding: EdgeInsets.zero,
          title: Text(t('Taux imposés (avis de votre comptable)')),
          children: [
            champ(_tvaManuel, t('TVA déductible imposée (%)'), 'taux_tva_manuel'),
            champ(_impotManuel, t('Frais déductibles imposés (%)'), 'taux_impot_manuel'),
          ],
        ),
      ],
      Align(
        alignment: Alignment.centerRight,
        child: FilledButton.icon(
          onPressed: _envoi ? null : _enregistrer,
          icon: const Icon(Icons.check),
          label: Text(t('Enregistrer')),
        ),
      ),
    ]);
  }

  Widget _tableau(List lignes) {
    if (lignes.isEmpty) return Text(t('Aucun frais sur cette année.'));
    final style = Theme.of(context).textTheme.bodySmall;
    return Column(children: [
      for (final l in lignes.cast<Map>())
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 6),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              Expanded(
                child: Text(
                  [
                    _libelles[l['code']] ?? '${l['code']}',
                    if (l['code'] == 'carburant' && _familles[l['detail']] != null) _familles[l['detail']]!,
                    if (l['code'] == 'amortissement') t('{n} ans', {'n': l['detail']}),
                  ].join(' · '),
                  style: const TextStyle(fontWeight: FontWeight.w600),
                ),
              ),
              Text(euros(l['montant'])),
            ]),
            if (l['code'] != 'amortissement' && (enDouble(l['tva']) ?? 0) > 0)
              Text(t('TVA {tva} · récupérable {pct} : {montant}',
                  {'tva': euros(l['tva']), 'pct': _pct(l['taux_tva_deductible']), 'montant': euros(l['tva_deductible'])}),
                  style: style),
            if (l['code'] != 'achat_tva')
              Text(t('Déductible impôt {pct} : {montant}',
                  {'pct': _pct(l['taux_impot']), 'montant': euros(l['deductible_impot'])}), style: style),
          ]),
        ),
    ]);
  }

  @override
  Widget build(BuildContext context) {
    super.build(context);
    if (context.watch<Abonnement>().formule == 'gratuit') return _verrou();
    return RefreshIndicator(
      onRefresh: () async {
        setState(_charger);
        await _donnees;
      },
      child: FutureBuilder<Map<String, dynamic>>(
        future: _donnees,
        builder: (context, snap) {
          if (snap.connectionState != ConnectionState.done) return const Center(child: CircularProgressIndicator());
          if (snap.hasError) {
            return ListView(children: [Padding(padding: const EdgeInsets.all(24), child: Text('${snap.error}'))]);
          }
          final d = snap.data!;
          if (d.isEmpty) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              if (mounted) setState(_charger);
            });
            return const Center(child: CircularProgressIndicator());
          }
          final totaux = Map<String, dynamic>.from(d['totaux'] as Map);
          final pays = d['pays'] as String? ?? '';
          final prive = (d['profil'] as Map)['statut'] == 'particulier';
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              _choixAnnee(),
              const SizedBox(height: 12),
              Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  leading: const Icon(Icons.flag),
                  title: Text(t('Règles : {pays}', {'pays': paysImmatriculation[pays] ?? pays})),
                  subtitle: Text(d['regles_disponibles'] == true
                      ? '${t('Pays d\'immatriculation du véhicule')} · ${typesVehicule[d['type_vehicule']] ?? ''}'
                      : t('Pas de règles détaillées pour ce pays : la part professionnelle est retenue.')),
                ),
              ),
              if (prive)
                Card(
                  color: Theme.of(context).colorScheme.surfaceContainerHighest,
                  margin: const EdgeInsets.only(bottom: 12),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Text(t('Un particulier ne peut rien déduire. Choisissez « Indépendant » ou « Société » si le '
                        'véhicule sert à une activité professionnelle.')),
                  ),
                ),
              Row(children: [
                _kpi(t('TVA récupérable'), euros(totaux['tva_deductible'])),
                _kpi(t('Frais déductibles (impôt)'), euros(totaux['deductible_impot']),
                    detail: d['taux_impot'] == null
                        ? d['explication_impot'] as String?
                        : '${_pct(d['taux_impot'])} · ${d['explication_impot']}'),
              ]),
              _carte(t('Détail {annee}', {'annee': _annee}), [_tableau(d['lignes'] as List? ?? [])]),
              if (!prive) _tvaARecuperer(),
              _profil(),
              if ((d['notes'] as List? ?? []).isNotEmpty)
                _carte(t('Règles du pays'), [
                  for (final n in d['notes'] as List)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 8),
                      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        const Text('•  '),
                        Expanded(child: Text('$n')),
                      ]),
                    ),
                ]),
              Text(
                t('Estimation indicative selon les règles générales du pays : vérifiez avec votre comptable.'),
                style: Theme.of(context).textTheme.bodySmall,
              ),
            ],
          );
        },
      ),
    );
  }
}

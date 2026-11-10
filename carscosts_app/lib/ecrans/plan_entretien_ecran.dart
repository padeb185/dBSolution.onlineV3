import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../api/api_client.dart';
import '../l10n/langue.dart';
import '../l10n/unites.dart';
import '../modeles/pays.dart';
import '../widgets/format.dart';

/// Plan d'entretien : rappel d'entretien (normal 1 an / Long Life 2 ans + kilométrage),
/// rappel de contrôle technique (règle du pays) et échéance d'assurance.
class PlanEntretienEcran extends StatefulWidget {
  const PlanEntretienEcran({super.key, required this.vehicule});

  final Map<String, dynamic> vehicule;

  @override
  State<PlanEntretienEcran> createState() => _PlanEntretienEcranState();
}

class _PlanEntretienEcranState extends State<PlanEntretienEcran> {
  Map<String, dynamic>? _plan;
  String? _erreur;
  bool _envoi = false;

  // Saisie
  bool _entretienActif = true;
  bool _longLife = false;
  int? _intervalleKm;
  bool _ctActif = true;

  String get _chemin => 'vehicules/${widget.vehicule['id']}/plan_entretien/';
  Unites get _u => Unites.de(widget.vehicule);

  @override
  void initState() {
    super.initState();
    _charger();
  }

  Future<void> _charger() async {
    try {
      final r = Map<String, dynamic>.from(await context.read<ApiClient>().get(_chemin) as Map);
      if (mounted) setState(() => _remplir(r));
    } on ApiException catch (e) {
      if (mounted) setState(() => _erreur = e.message);
    }
  }

  /// Rappel absent : proposé activé (plan pas encore configuré) ; sinon l'état enregistré.
  void _remplir(Map<String, dynamic> p) {
    _plan = p;
    final e = Map<String, dynamic>.from(p['entretien'] as Map);
    final ct = Map<String, dynamic>.from(p['controle_technique'] as Map);
    final configure = e['rappel'] != null || ct['rappel'] != null;
    _entretienActif = e['rappel'] != null || !configure;
    _ctActif = ct['rappel'] != null || !configure;
    _longLife = e['long_life'] == true;
    _intervalleKm = (e['intervalle_km'] as num?)?.toInt();
  }

  Future<void> _enregistrer() async {
    setState(() => _envoi = true);
    try {
      final r = await context.read<ApiClient>().put(_chemin, {
        'entretien': {'actif': _entretienActif, 'long_life': _longLife, 'intervalle_km': _intervalleKm},
        'controle_technique': {'actif': _ctActif},
      });
      if (!mounted) return;
      setState(() => _remplir(Map<String, dynamic>.from(r as Map)));
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(t('Rappels enregistrés.'))));
      Navigator.pop(context, true);
    } on ApiException catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    } finally {
      if (mounted) setState(() => _envoi = false);
    }
  }

  // ------------------------------------------------------------------ Mise en page
  Widget _carte(IconData icone, String titre, List<Widget> enfants) => Card(
        margin: const EdgeInsets.only(bottom: 12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              Icon(icone),
              const SizedBox(width: 8),
              Expanded(child: Text(titre, style: Theme.of(context).textTheme.titleMedium)),
            ]),
            const SizedBox(height: 12),
            ...enfants,
          ]),
        ),
      );

  /// « dans 230 jours ou 8 500 km » (en retard : « dépassé de … »)
  String _restant({String? echeanceDate, num? echeanceKm}) {
    final parties = <String>[];
    if (echeanceDate != null) {
      final jours = DateTime.parse(echeanceDate).difference(DateTime.now()).inDays;
      parties.add(jours >= 0 ? t('dans {n} jours', {'n': jours}) : t('dépassé de {n} jours', {'n': -jours}));
    }
    if (echeanceKm != null) {
      final reste = echeanceKm - (enDouble(widget.vehicule['kilometrage_actuel']) ?? 0);
      parties.add(reste >= 0 ? t('dans {km}', {'km': km(reste, _u)}) : t('dépassé de {km}', {'km': km(-reste, _u)}));
    }
    return parties.join(t(' ou '));
  }

  Widget _entretien(Map<String, dynamic> e) {
    final base = Map<String, dynamic>.from(e['base'] as Map);
    final mois = _longLife ? 24 : 12;
    final baseDate = DateTime.parse('${base['date']}');
    final echeanceDate = dateIso(DateTime(baseDate.year, baseDate.month + mois, baseDate.day));
    final baseKm = enDouble(base['km']);
    final echeanceKm = _intervalleKm != null && baseKm != null ? baseKm + _intervalleKm! : null;
    final electrique = _plan!['electrique'] == true;
    final source = switch (base['source']) {
      'entretien' => t('dernier entretien ({libelle}) du {date}', {'libelle': base['libelle'], 'date': dateFr(base['date'])}),
      'achat' => t('achat du {date}', {'date': dateFr(base['date'])}),
      _ => t('aujourd\'hui'),
    };
    return _carte(Icons.build, t('Entretien'), [
      SwitchListTile(
        contentPadding: EdgeInsets.zero,
        title: Text(t('Rappel d\'entretien')),
        value: _entretienActif,
        onChanged: (v) => setState(() => _entretienActif = v),
      ),
      if (_entretienActif) ...[
        Text(t('Type de service'), style: Theme.of(context).textTheme.labelLarge),
        const SizedBox(height: 6),
        SegmentedButton<bool>(
          segments: [
            ButtonSegment(value: false, label: Text(t('Normal · 1 an'))),
            ButtonSegment(value: true, label: Text(t('Long Life · 2 ans'))),
          ],
          selected: {_longLife},
          onSelectionChanged: (s) => setState(() => _longLife = s.first),
        ),
        const SizedBox(height: 12),
        Text(electrique ? t('Kilométrage (moteur électrique)') : t('Kilométrage (moteur thermique)'),
            style: Theme.of(context).textTheme.labelLarge),
        const SizedBox(height: 6),
        Wrap(spacing: 8, runSpacing: 4, children: [
          for (final n in (e['options_km'] as List).cast<num>())
            ChoiceChip(
              label: Text(km(n, _u)),
              selected: _intervalleKm == n.toInt(),
              onSelected: (_) => setState(() => _intervalleKm = n.toInt()),
            ),
          ChoiceChip(
            label: Text(t('Date seule')),
            selected: _intervalleKm == null,
            onSelected: (_) => setState(() => _intervalleKm = null),
          ),
        ]),
        const SizedBox(height: 12),
        Text(t('Depuis : {source}', {'source': source}) +
            (baseKm != null ? ' · ${km(baseKm, _u)}' : ''), style: Theme.of(context).textTheme.bodySmall),
        const SizedBox(height: 8),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest, borderRadius: BorderRadius.circular(8)),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(t('Prochain entretien : le {date}', {'date': dateFr(echeanceDate)}) +
                (echeanceKm != null ? ' ${t('ou à {km}', {'km': km(echeanceKm, _u)})}' : ''),
                style: const TextStyle(fontWeight: FontWeight.w600)),
            Text(t('Le premier des deux · {restant}',
                {'restant': _restant(echeanceDate: echeanceDate, echeanceKm: echeanceKm)})),
          ]),
        ),
      ],
    ]);
  }

  Widget _controle(Map<String, dynamic> ct) {
    final regle = (ct['regle'] as Map?)?.cast<String, dynamic>();
    final pays = '${widget.vehicule['pays_immatriculation'] ?? ''}';
    final doc = ct['document_echeance'] as String?;
    final echeance = doc ?? ct['echeance'] as String?;
    return _carte(Icons.fact_check, t('Contrôle technique'), [
      if (regle != null)
        Text(
          regle['annuel_a_partir_de'] == null
              ? t('{pays} : premier contrôle après {premier} ans, puis tous les {periode} ans.',
                  {'pays': paysImmatriculation[pays] ?? pays, 'premier': regle['premier'], 'periode': regle['periode']})
              : t('{pays} : premier contrôle après {premier} ans, puis tous les {periode} ans, chaque année dès {annuel} ans.',
                  {'pays': paysImmatriculation[pays] ?? pays, 'premier': regle['premier'], 'periode': regle['periode'],
                    'annuel': regle['annuel_a_partir_de']}),
        )
      else
        Text(t('Pas de règle pour ce pays : ajoutez le certificat de contrôle dans Documents (rappel à son échéance).')),
      const SizedBox(height: 8),
      if (echeance != null)
        Text(t('Prochain contrôle : le {date} · {restant}', {'date': dateFr(echeance), 'restant': _restant(echeanceDate: echeance)}),
            style: const TextStyle(fontWeight: FontWeight.w600))
      else if (ct['source'] == 'mise_en_circulation_inconnue')
        Text(t('Indiquez la date de première mise en circulation du véhicule pour calculer l\'échéance.')),
      if (doc != null)
        Text(t('Échéance reprise du certificat de contrôle (Documents).'), style: Theme.of(context).textTheme.bodySmall)
      else if (ct['source'] == 'mise_en_circulation')
        Text(t('Calculé depuis la mise en circulation : encodez votre dernier contrôle (Entretiens ou Documents) pour plus de précision.'),
            style: Theme.of(context).textTheme.bodySmall),
      if (regle != null && doc == null && echeance != null)
        SwitchListTile(
          contentPadding: EdgeInsets.zero,
          title: Text(t('Rappel de contrôle technique')),
          value: _ctActif,
          onChanged: (v) => setState(() => _ctActif = v),
        ),
    ]);
  }

  Widget _assurance(Map<String, dynamic>? a) => _carte(Icons.shield, t('Assurance'), [
        if (a == null)
          Text(t('Aucune assurance avec date d\'échéance : ajoutez-la dans Documents (type Assurance) ; '
              'un rappel est créé automatiquement.'))
        else ...[
          Text([if ((a['titre'] ?? '').toString().isNotEmpty) a['titre'], if ((a['organisme'] ?? '').toString().isNotEmpty && a['organisme'] != a['titre']) a['organisme']].join(' · ')),
          Text(t('Échéance : le {date} · {restant}', {'date': dateFr(a['date_expiration']), 'restant': _restant(echeanceDate: a['date_expiration'] as String)}),
              style: const TextStyle(fontWeight: FontWeight.w600)),
          if (a['montant'] != null && a['mode_paiement'] == 'mensuel')
            Text(t('{montant} / mois', {'montant': euros(a['montant'])}), style: Theme.of(context).textTheme.bodySmall),
          if (a['montant'] != null && a['mode_paiement'] == 'annuel')
            Text(t('{montant} / an', {'montant': euros(a['montant'])}), style: Theme.of(context).textTheme.bodySmall),
        ],
      ]);

  @override
  Widget build(BuildContext context) {
    final p = _plan;
    return Scaffold(
      appBar: AppBar(title: Text(t('Plan d\'entretien'))),
      body: p == null
          ? Center(child: _erreur == null ? const CircularProgressIndicator() : Text(_erreur!))
          : ListView(padding: const EdgeInsets.all(16), children: [
              _entretien(Map<String, dynamic>.from(p['entretien'] as Map)),
              _controle(Map<String, dynamic>.from(p['controle_technique'] as Map)),
              _assurance((p['assurance'] as Map?)?.cast<String, dynamic>()),
              Text(t('Règles indicatives : vérifiez le carnet d\'entretien du constructeur. Les échéances restent modifiables dans Rappels.'),
                  style: Theme.of(context).textTheme.bodySmall),
              const SizedBox(height: 16),
              FilledButton.icon(
                onPressed: _envoi ? null : _enregistrer,
                icon: const Icon(Icons.check),
                label: Text(t('Enregistrer les rappels')),
              ),
            ]),
    );
  }
}

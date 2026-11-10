import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../api/api_client.dart';
import '../l10n/langue.dart';
import '../l10n/unites.dart';
import '../modeles/pays.dart';
import '../widgets/format.dart';

/// Plan d'entretien : rappel d'entretien (normal 1 an / Long Life 2 ans, ou 15 000 / 20 000 / 25 000 km / autre),
/// rappel de contrôle technique (premier au 4e anniversaire de la mise en circulation, règle du pays),
/// courroie de distribution (années ou km, remise à zéro du kilométrage courroie) et échéance d'assurance.
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
  bool _modifie = false;

  // Entretien
  bool _entretienActif = true;
  bool _longLife = false;
  int? _intervalleKm;          // null : date seule
  bool _kmAutre = false;
  final _kmAutreCtrl = TextEditingController();

  // Contrôle technique : échéance modifiable à la main
  bool _ctActif = true;
  String? _ctEcheance;
  bool _ctRecalculer = false;

  // Courroie de distribution
  bool _courroieActif = false;
  int? _courroieKm;
  bool _courroieKmAutre = false;
  final _courroieKmCtrl = TextEditingController();
  int? _courroieAns;
  bool _courroieAnsAutre = false;
  final _courroieAnsCtrl = TextEditingController();

  String get _chemin => 'vehicules/${widget.vehicule['id']}/plan_entretien/';
  Unites get _u => Unites.de(widget.vehicule);

  @override
  void initState() {
    super.initState();
    _charger();
  }

  @override
  void dispose() {
    _kmAutreCtrl.dispose();
    _courroieKmCtrl.dispose();
    _courroieAnsCtrl.dispose();
    super.dispose();
  }

  Future<void> _charger() async {
    try {
      final r = Map<String, dynamic>.from(await context.read<ApiClient>().get(_chemin) as Map);
      if (mounted) setState(() => _remplir(r));
    } on ApiException catch (e) {
      if (mounted) setState(() => _erreur = e.message);
    }
  }

  /// Rappel absent : entretien et contrôle technique proposés activés (plan pas encore configuré).
  void _remplir(Map<String, dynamic> p) {
    _plan = p;
    final e = Map<String, dynamic>.from(p['entretien'] as Map);
    final ct = Map<String, dynamic>.from(p['controle_technique'] as Map);
    final configure = e['rappel'] != null || ct['rappel'] != null;
    _entretienActif = e['rappel'] != null || !configure;
    _ctActif = ct['rappel'] != null || !configure;
    _ctEcheance = ct['echeance'] as String?;
    _ctRecalculer = false;
    _longLife = e['long_life'] == true;
    _intervalleKm = (e['intervalle_km'] as num?)?.toInt();
    final options = (e['options_km'] as List).cast<num>().map((n) => n.toInt()).toList();
    _kmAutre = _intervalleKm != null && !options.contains(_intervalleKm);
    if (_kmAutre) _kmAutreCtrl.text = _u.depuisKm(_intervalleKm!).round().toString();

    final c = (p['courroie'] as Map?)?.cast<String, dynamic>();
    if (c != null) {
      _courroieActif = c['rappel'] != null;
      _courroieKm = (c['intervalle_km'] as num?)?.toInt();
      _courroieAns = (c['intervalle_ans'] as num?)?.toInt();
      final optKm = (c['options_km'] as List).cast<num>().map((n) => n.toInt()).toList();
      final optAns = (c['options_ans'] as List).cast<num>().map((n) => n.toInt()).toList();
      _courroieKmAutre = _courroieKm != null && !optKm.contains(_courroieKm);
      if (_courroieKmAutre) _courroieKmCtrl.text = _u.depuisKm(_courroieKm!).round().toString();
      _courroieAnsAutre = _courroieAns != null && !optAns.contains(_courroieAns);
      if (_courroieAnsAutre) _courroieAnsCtrl.text = '$_courroieAns';
    }
  }

  int? _lireKm(TextEditingController c) {
    final v = double.tryParse(c.text.trim().replaceAll(',', '.').replaceAll(' ', ''));
    return v == null || v <= 0 ? null : _u.versKm(v).round();
  }

  int? get _kmEntretien => _kmAutre ? _lireKm(_kmAutreCtrl) : _intervalleKm;
  int? get _kmCourroie => _courroieKmAutre ? _lireKm(_courroieKmCtrl) : _courroieKm;
  int? get _ansCourroie => _courroieAnsAutre ? int.tryParse(_courroieAnsCtrl.text.trim()) : _courroieAns;

  Map<String, dynamic> _donnees({Map<String, dynamic>? remplacee}) => {
        'entretien': {'actif': _entretienActif, 'long_life': _longLife, 'intervalle_km': _kmEntretien},
        'controle_technique': {
          'actif': _ctActif,
          if (_ctRecalculer) 'recalculer': true else if (_ctEcheance != null) 'echeance': _ctEcheance,
        },
        if (_plan?['courroie'] != null)
          'courroie': {
            'actif': _courroieActif || remplacee != null,
            'intervalle_km': _kmCourroie,
            'intervalle_ans': _ansCourroie,
            if (remplacee != null) 'remplacee': remplacee,
          },
      };

  Future<void> _enregistrer({Map<String, dynamic>? remplacee, bool fermer = true}) async {
    setState(() => _envoi = true);
    try {
      final r = await context.read<ApiClient>().put(_chemin, _donnees(remplacee: remplacee));
      if (!mounted) return;
      _modifie = true;
      setState(() => _remplir(Map<String, dynamic>.from(r as Map)));
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(remplacee != null ? t('Kilométrage courroie remis à zéro.') : t('Rappels enregistrés.'))));
      if (fermer) Navigator.pop(context, true);
    } on ApiException catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    } finally {
      if (mounted) setState(() => _envoi = false);
    }
  }

  /// Courroie remplacée : date et kilométrage du remplacement, le kilométrage courroie repart de zéro.
  Future<void> _courroieRemplacee() async {
    final kmCtrl = TextEditingController(text: _u.depuisKm(enDouble(widget.vehicule['kilometrage_actuel']) ?? 0).round().toString());
    var jour = DateTime.now();
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setD) => AlertDialog(
          title: Text(t('Courroie remplacée')),
          content: Column(mainAxisSize: MainAxisSize.min, children: [
            Text(t('Le kilométrage courroie repart de zéro à cette date et à ce kilométrage.')),
            const SizedBox(height: 12),
            TextField(
              controller: kmCtrl,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: t('Kilométrage au remplacement'), suffixText: _u.symboleDistance),
            ),
            ListTile(
              contentPadding: EdgeInsets.zero,
              leading: const Icon(Icons.calendar_today),
              title: Text(dateFr(dateIso(jour))),
              onTap: () async {
                final d = await showDatePicker(context: ctx, initialDate: jour, firstDate: DateTime(1990), lastDate: DateTime(2100));
                if (d != null) setD(() => jour = d);
              },
            ),
          ]),
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx, false), child: Text(t('Annuler'))),
            FilledButton(onPressed: () => Navigator.pop(ctx, true), child: Text(t('Remettre à zéro'))),
          ],
        ),
      ),
    );
    if (ok != true || !mounted) return;
    _courroieActif = true;
    await _enregistrer(remplacee: {'date': dateIso(jour), 'km': _lireKm(kmCtrl)}, fermer: false);
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

  Widget _encadre(List<Widget> lignes) => Container(
        width: double.infinity,
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surfaceContainerHighest, borderRadius: BorderRadius.circular(8)),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: lignes),
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

  String _ajouterMois(String iso, int mois) {
    final d = DateTime.parse(iso);
    return dateIso(DateTime(d.year, d.month + mois, d.day));
  }

  /// Puces de kilométrage + « Autre » (saisie libre) [+ « Date seule »]
  Widget _choixKm(List<int> options, int? valeur, bool autre, TextEditingController ctrl,
      {required ValueChanged<int?> choisir, required VoidCallback choisirAutre, bool dateSeule = false}) {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Wrap(spacing: 8, runSpacing: 4, children: [
        for (final n in options)
          ChoiceChip(label: Text(km(n, _u)), selected: !autre && valeur == n, onSelected: (_) => choisir(n)),
        ChoiceChip(label: Text(t('Autre')), selected: autre, onSelected: (_) => choisirAutre()),
        if (dateSeule)
          ChoiceChip(label: Text(t('Date seule')), selected: !autre && valeur == null, onSelected: (_) => choisir(null)),
      ]),
      if (autre)
        Padding(
          padding: const EdgeInsets.only(top: 8),
          child: TextField(
            controller: ctrl,
            keyboardType: TextInputType.number,
            decoration: InputDecoration(
                labelText: t('Kilométrage'), suffixText: _u.symboleDistance, border: const OutlineInputBorder(), isDense: true),
            onChanged: (_) => setState(() {}),
          ),
        ),
    ]);
  }

  Widget _entretien(Map<String, dynamic> e) {
    final base = Map<String, dynamic>.from(e['base'] as Map);
    final mois = _longLife ? 24 : 12;
    final echeanceDate = _ajouterMois('${base['date']}', mois);
    final baseKm = enDouble(base['km']);
    final kmE = _kmEntretien;
    final echeanceKm = kmE != null && baseKm != null ? baseKm + kmE : null;
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
            ButtonSegment(value: false, label: Text(t('Autre · 1 an'))),
            ButtonSegment(value: true, label: Text(t('Long Life · 2 ans'))),
          ],
          selected: {_longLife},
          onSelectionChanged: (s) => setState(() => _longLife = s.first),
        ),
        const SizedBox(height: 4),
        Text(_longLife
            ? t('Deux ans après l\'entretien précédent, ou au kilométrage choisi.')
            : t('Un an après le dernier entretien, ou au kilométrage choisi.'),
            style: Theme.of(context).textTheme.bodySmall),
        const SizedBox(height: 12),
        Text(t('Kilométrage'), style: Theme.of(context).textTheme.labelLarge),
        const SizedBox(height: 6),
        _choixKm((e['options_km'] as List).cast<num>().map((n) => n.toInt()).toList(), _intervalleKm, _kmAutre, _kmAutreCtrl,
            choisir: (n) => setState(() {
                  _kmAutre = false;
                  _intervalleKm = n;
                }),
            choisirAutre: () => setState(() => _kmAutre = true),
            dateSeule: true),
        const SizedBox(height: 12),
        Text(t('Depuis : {source}', {'source': source}) + (baseKm != null ? ' · ${km(baseKm, _u)}' : ''),
            style: Theme.of(context).textTheme.bodySmall),
        const SizedBox(height: 8),
        _encadre([
          Text(t('Prochain entretien : le {date}', {'date': dateFr(echeanceDate)}) +
              (echeanceKm != null ? ' ${t('ou à {km}', {'km': km(echeanceKm, _u)})}' : ''),
              style: const TextStyle(fontWeight: FontWeight.w600)),
          Text(t('Le premier des deux · {restant}', {'restant': _restant(echeanceDate: echeanceDate, echeanceKm: echeanceKm)})),
        ]),
      ],
    ]);
  }

  Widget _courroie(Map<String, dynamic> c) {
    final base = Map<String, dynamic>.from(c['base'] as Map);
    final baseKm = enDouble(base['km']);
    final ans = _ansCourroie;
    final kmC = _kmCourroie;
    final echeanceDate = ans != null ? _ajouterMois('${base['date']}', ans * 12) : null;
    final echeanceKm = kmC != null && baseKm != null ? baseKm + kmC : null;
    final kmCourroie = baseKm != null ? (enDouble(widget.vehicule['kilometrage_actuel']) ?? 0) - baseKm : null;
    final source = switch (base['source']) {
      'remplacement' => t('remplacement du {date}', {'date': dateFr(base['date'])}),
      'remise_a_zero' => t('remise à zéro du {date}', {'date': dateFr(base['date'])}),
      'origine' => t('origine (mise en circulation du {date})', {'date': dateFr(base['date'])}),
      'achat' => t('achat du {date}', {'date': dateFr(base['date'])}),
      _ => t('aujourd\'hui'),
    };
    return _carte(Icons.settings, t('Courroie de distribution'), [
      SwitchListTile(
        contentPadding: EdgeInsets.zero,
        title: Text(t('Rappel de courroie')),
        subtitle: Text(t('Désactivez pour un moteur à chaîne de distribution.')),
        value: _courroieActif,
        onChanged: (v) => setState(() => _courroieActif = v),
      ),
      if (kmCourroie != null)
        Padding(
          padding: const EdgeInsets.only(bottom: 8),
          child: Text(t('Kilométrage courroie : {km}', {'km': km(kmCourroie < 0 ? 0 : kmCourroie, _u)}),
              style: const TextStyle(fontWeight: FontWeight.w600)),
        ),
      Text(t('Depuis : {source}', {'source': source}), style: Theme.of(context).textTheme.bodySmall),
      if (_courroieActif) ...[
        const SizedBox(height: 12),
        Text(t('Remplacement tous les'), style: Theme.of(context).textTheme.labelLarge),
        const SizedBox(height: 6),
        _choixKm((c['options_km'] as List).cast<num>().map((n) => n.toInt()).toList(), _courroieKm, _courroieKmAutre,
            _courroieKmCtrl,
            choisir: (n) => setState(() {
                  _courroieKmAutre = false;
                  _courroieKm = n;
                }),
            choisirAutre: () => setState(() => _courroieKmAutre = true)),
        const SizedBox(height: 8),
        Wrap(spacing: 8, runSpacing: 4, children: [
          for (final n in (c['options_ans'] as List).cast<num>().map((n) => n.toInt()))
            ChoiceChip(
              label: Text(t('{n} ans', {'n': n})),
              selected: !_courroieAnsAutre && _courroieAns == n,
              onSelected: (_) => setState(() {
                _courroieAnsAutre = false;
                _courroieAns = n;
              }),
            ),
          ChoiceChip(
              label: Text(t('Autre')),
              selected: _courroieAnsAutre,
              onSelected: (_) => setState(() => _courroieAnsAutre = true)),
        ]),
        if (_courroieAnsAutre)
          Padding(
            padding: const EdgeInsets.only(top: 8),
            child: TextField(
              controller: _courroieAnsCtrl,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                  labelText: t('Années'), suffixText: t('ans'), border: const OutlineInputBorder(), isDense: true),
              onChanged: (_) => setState(() {}),
            ),
          ),
        const SizedBox(height: 12),
        if (echeanceDate != null || echeanceKm != null)
          _encadre([
            Text(
                [
                  if (echeanceDate != null) t('Prochain remplacement : le {date}', {'date': dateFr(echeanceDate)}),
                  if (echeanceKm != null) t('à {km}', {'km': km(echeanceKm, _u)}),
                ].join(t(' ou ')),
                style: const TextStyle(fontWeight: FontWeight.w600)),
            Text(t('Le premier des deux · {restant}', {'restant': _restant(echeanceDate: echeanceDate, echeanceKm: echeanceKm)})),
          ]),
      ],
      const SizedBox(height: 8),
      OutlinedButton.icon(
        onPressed: _envoi ? null : _courroieRemplacee,
        icon: const Icon(Icons.restart_alt),
        label: Text(t('Courroie remplacée : remise à zéro')),
      ),
    ]);
  }

  Widget _controle(Map<String, dynamic> ct) {
    final regle = (ct['regle'] as Map?)?.cast<String, dynamic>();
    final pays = '${widget.vehicule['pays_immatriculation'] ?? ''}';
    final nomPays = ct['regle_pays'] == true ? (paysImmatriculation[pays] ?? pays) : t('Règle générale');
    final doc = ct['document_echeance'] as String?;
    final echeance = doc ?? ct['echeance'] as String?;
    final premier = ct['premier_controle'] as String?;
    return _carte(Icons.fact_check, t('Contrôle technique'), [
      if (regle != null)
        Text(
          regle['annuel_a_partir_de'] == null
              ? t('{pays} : premier contrôle après {premier} ans, puis tous les {periode} ans.',
                  {'pays': nomPays, 'premier': regle['premier'], 'periode': regle['periode']})
              : t('{pays} : premier contrôle après {premier} ans, puis tous les {periode} ans, chaque année dès {annuel} ans.',
                  {'pays': nomPays, 'premier': regle['premier'], 'periode': regle['periode'], 'annuel': regle['annuel_a_partir_de']}),
        ),
      if (premier != null && regle != null)
        Padding(
          padding: const EdgeInsets.only(top: 4),
          child: Text(t('Premier contrôle : {n}e anniversaire de la mise en circulation, le {date}',
              {'n': regle['premier'], 'date': dateFr(premier)})),
        ),
      const SizedBox(height: 8),
      if (doc != null)
        _encadre([
          Text(t('Prochain contrôle : le {date} · {restant}', {'date': dateFr(doc), 'restant': _restant(echeanceDate: doc)}),
              style: const TextStyle(fontWeight: FontWeight.w600)),
        ])
      else ...[
        // Date du prochain contrôle : calculée, modifiable (sélecteur de date)
        InkWell(
          borderRadius: BorderRadius.circular(8),
          onTap: () async {
            final d = await showDatePicker(
              context: context,
              initialDate: DateTime.tryParse(_ctEcheance ?? '') ?? DateTime.now(),
              firstDate: DateTime(2000),
              lastDate: DateTime(2100),
              helpText: t('Date du prochain contrôle technique'),
            );
            if (d != null) {
              setState(() {
                _ctEcheance = dateIso(d);
                _ctRecalculer = false;
                _ctActif = true;
              });
            }
          },
          child: _encadre([
            Row(children: [
              Expanded(
                child: Text(
                    _ctEcheance == null
                        ? t('Choisir la date du prochain contrôle')
                        : t('Prochain contrôle : le {date} · {restant}',
                            {'date': dateFr(_ctEcheance), 'restant': _restant(echeanceDate: _ctEcheance)}),
                    style: const TextStyle(fontWeight: FontWeight.w600)),
              ),
              const Icon(Icons.edit_calendar),
            ]),
          ]),
        ),
        if (_ctEcheance != null && ct['echeance_calculee'] != null && _ctEcheance != ct['echeance_calculee'])
          Row(children: [
            Expanded(
              child: Text(t('Date modifiée (calculée : {date})', {'date': dateFr(ct['echeance_calculee'])}),
                  style: Theme.of(context).textTheme.bodySmall),
            ),
            TextButton(
              onPressed: () => setState(() {
                _ctEcheance = ct['echeance_calculee'] as String;
                _ctRecalculer = true;
              }),
              child: Text(t('Recalculer')),
            ),
          ]),
      ],
      if (echeance == null && ct['source'] == 'mise_en_circulation_inconnue' && _ctEcheance == null)
        Text(t('Indiquez la date de première mise en circulation du véhicule pour calculer l\'échéance.')),
      if (doc != null)
        Text(t('Échéance reprise du certificat de contrôle : modifiez-la dans Documents.'), style: Theme.of(context).textTheme.bodySmall)
      else if (ct['source'] == 'mise_en_circulation')
        Text(t('Calculé depuis la mise en circulation : encodez votre dernier contrôle (Entretiens ou Documents) pour plus de précision.'),
            style: Theme.of(context).textTheme.bodySmall),
      if (doc == null && _ctEcheance != null)
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
          Text([
            if ((a['titre'] ?? '').toString().isNotEmpty) a['titre'],
            if ((a['organisme'] ?? '').toString().isNotEmpty && a['organisme'] != a['titre']) a['organisme'],
          ].join(' · ')),
          Text(t('Échéance : le {date} · {restant}',
                  {'date': dateFr(a['date_expiration']), 'restant': _restant(echeanceDate: a['date_expiration'] as String)}),
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
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (pop, _) {
        if (!pop) Navigator.pop(context, _modifie);
      },
      child: Scaffold(
        appBar: AppBar(title: Text(t('Plan d\'entretien'))),
        body: p == null
            ? Center(child: _erreur == null ? const CircularProgressIndicator() : Text(_erreur!))
            : ListView(padding: const EdgeInsets.all(16), children: [
                _entretien(Map<String, dynamic>.from(p['entretien'] as Map)),
                _controle(Map<String, dynamic>.from(p['controle_technique'] as Map)),
                if (p['courroie'] != null) _courroie(Map<String, dynamic>.from(p['courroie'] as Map)),
                _assurance((p['assurance'] as Map?)?.cast<String, dynamic>()),
                Text(t('Règles indicatives : vérifiez le carnet d\'entretien du constructeur. Les échéances restent modifiables dans Rappels.'),
                    style: Theme.of(context).textTheme.bodySmall),
                const SizedBox(height: 16),
                FilledButton.icon(
                  onPressed: _envoi ? null : () => _enregistrer(),
                  icon: const Icon(Icons.check),
                  label: Text(t('Enregistrer les rappels')),
                ),
                const SizedBox(height: 24),
              ]),
      ),
    );
  }
}

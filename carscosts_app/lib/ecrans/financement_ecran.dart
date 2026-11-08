import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../api/api_client.dart';
import '../l10n/langue.dart';
import '../l10n/unites.dart';
import '../widgets/format.dart';
import 'formules_ecran.dart';

/// Types d'achat d'un véhicule
Map<String, String> get typesAchat => {
      'comptant': t('Comptant'),
      'pret': t('Prêt (crédit auto)'),
      'leasing': t('Leasing avec option d\'achat (LOA)'),
      'renting': t('Renting / location longue durée (LLD)'),
    };

/// Ouvre le type d'achat, ou les formules si la formule ne le permet pas (Bronze minimum).
Future<bool> ouvrirFinancement(BuildContext context, Map<String, dynamic> vehicule) async {
  final ab = context.read<Abonnement>();
  if (ab.formule == 'gratuit') {
    await Navigator.push(context, MaterialPageRoute(
        builder: (_) => FormulesEcran(raison: t('Le type d\'achat est disponible à partir de la formule Bronze.'))));
    return false;
  }
  final ok = await Navigator.push<bool>(
      context, MaterialPageRoute(builder: (_) => FinancementEcran(vehicule: vehicule)));
  return ok == true;
}

/// Type d'achat : comptant, prêt (taux, durée, mensualité), leasing (loyers, option d'achat,
/// kilométrage autorisé), renting. Les mensualités entrent dans les coûts du véhicule.
class FinancementEcran extends StatefulWidget {
  const FinancementEcran({super.key, required this.vehicule});

  final Map<String, dynamic> vehicule;

  @override
  State<FinancementEcran> createState() => _FinancementEcranState();
}

class _FinancementEcranState extends State<FinancementEcran> {
  final _cle = GlobalKey<FormState>();
  static const _champs = [
    'organisme', 'duree_mois', 'apport', 'montant_emprunte', 'taux_annuel', 'mensualite', 'premier_loyer',
    'valeur_residuelle', 'km_annuels', 'prix_km_supplementaire', 'services_inclus',
  ];
  final Map<String, TextEditingController> _c = {for (final n in _champs) n: TextEditingController()};
  String _type = 'comptant';
  String? _dateDebut;
  bool _optionLevee = false;
  Map<String, dynamic>? _calculs;
  Map<String, String> _erreurs = {};
  bool _chargement = true;
  bool _envoi = false;

  String get _id => widget.vehicule['id'] as String;
  Unites get _u => Unites.de(widget.vehicule);

  @override
  void initState() {
    super.initState();
    _charger();
  }

  @override
  void dispose() {
    for (final c in _c.values) {
      c.dispose();
    }
    super.dispose();
  }

  String _texte(dynamic v) => v == null ? '' : '$v'.replaceFirst(RegExp(r'\.0+$'), '');

  Future<void> _charger() async {
    try {
      final r = Map<String, dynamic>.from(await context.read<ApiClient>().get('vehicules/$_id/financement/') as Map);
      _remplir(r);
    } on ApiException catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    }
    if (mounted) setState(() => _chargement = false);
  }

  void _remplir(Map<String, dynamic> r) {
    final d = (r['donnees'] as Map?)?.cast<String, dynamic>() ?? {};
    _calculs = (r['calculs'] as Map?)?.cast<String, dynamic>();
    _type = (d['type_achat'] as String?) ?? 'comptant';
    _dateDebut = d['date_debut'] as String? ?? widget.vehicule['date_achat'] as String?;
    _optionLevee = d['option_levee'] == true;
    for (final n in _champs) {
      _c[n]!.text = _texte(d[n]);
    }
    // Kilométrage autorisé et prix du km supplémentaire dans l'unité du véhicule (km ou miles)
    final kmAn = enDouble(d['km_annuels']);
    if (kmAn != null) _c['km_annuels']!.text = _u.depuisKm(kmAn).round().toString();
    final prixKm = enDouble(d['prix_km_supplementaire']);
    if (prixKm != null) _c['prix_km_supplementaire']!.text = _u.coutParDistance(prixKm).toStringAsFixed(3);
  }

  Future<void> _enregistrer() async {
    if (!_cle.currentState!.validate()) return;
    String? v(String n) => _c[n]!.text.trim().isEmpty ? null : _c[n]!.text.trim().replaceAll(',', '.');
    final kmAn = double.tryParse(v('km_annuels') ?? '');
    final prixKm = double.tryParse(v('prix_km_supplementaire') ?? '');
    final donnees = <String, dynamic>{
      'type_achat': _type,
      'organisme': _c['organisme']!.text.trim(),
      'date_debut': _dateDebut,
      'duree_mois': int.tryParse(v('duree_mois') ?? ''),
      for (final n in ['apport', 'montant_emprunte', 'taux_annuel', 'mensualite', 'premier_loyer', 'valeur_residuelle'])
        n: v(n),
      'option_levee': _optionLevee,
      'km_annuels': kmAn == null ? null : _u.versKm(kmAn).round(),
      'prix_km_supplementaire': prixKm == null ? null : (prixKm / _u.coutParDistance(1)).toStringAsFixed(3),
      'services_inclus': _c['services_inclus']!.text.trim(),
    };
    setState(() {
      _envoi = true;
      _erreurs = {};
    });
    try {
      final r = Map<String, dynamic>.from(
          await context.read<ApiClient>().put('vehicules/$_id/financement/', donnees) as Map);
      setState(() => _remplir(r));
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(t('Type d\'achat enregistré.'))));
      }
    } on ApiException catch (e) {
      if (!mounted) return;
      setState(() => _erreurs = e.champs);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    } finally {
      if (mounted) setState(() => _envoi = false);
    }
  }

  Widget _champ(String nom, String libelle, {String? suffixe, String? aide, bool entier = false, bool texte = false}) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: TextFormField(
        controller: _c[nom],
        keyboardType: texte
            ? TextInputType.text
            : TextInputType.numberWithOptions(decimal: !entier),
        decoration: InputDecoration(
          labelText: libelle,
          suffixText: suffixe,
          helperText: aide,
          helperMaxLines: 2,
          errorText: _erreurs[nom],
          border: const OutlineInputBorder(),
        ),
      ),
    );
  }

  Widget _date() => Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: InkWell(
          onTap: () async {
            final d = await showDatePicker(
              context: context,
              initialDate: DateTime.tryParse(_dateDebut ?? '') ?? DateTime.now(),
              firstDate: DateTime(1970),
              lastDate: DateTime(2100),
            );
            if (d != null) setState(() => _dateDebut = dateIso(d));
          },
          child: InputDecorator(
            decoration: InputDecoration(
              labelText: t('Début du contrat'),
              border: const OutlineInputBorder(),
              suffixIcon: const Icon(Icons.calendar_today),
            ),
            child: Text(_dateDebut == null ? '—' : dateFr(_dateDebut)),
          ),
        ),
      );

  /// Résultats calculés par le serveur (mensualité, payé, reste à payer, kilomètres…)
  Widget _resultats() {
    final c = _calculs;
    if (c == null || _type == 'comptant') return const SizedBox.shrink();
    final lignes = <(String, String)>[
      if (c['mensualite'] != null) (t('Mensualité'), euros(c['mensualite'])),
      if (c['date_fin'] != null) (t('Fin du contrat'), dateFr(c['date_fin'])),
      (t('Mois payés'), '${c['mois_payes']}${c['duree_mois'] != null ? ' / ${c['duree_mois']}' : ''}'),
      (t('Payé à ce jour'), euros(c['paye_a_ce_jour'])),
      if (c['reste_a_payer'] != null) (t('Reste à payer'), euros(c['reste_a_payer'])),
      if (c['capital_restant'] != null) (t('Capital restant dû'), euros(c['capital_restant'])),
      if (c['interets_a_ce_jour'] != null) (t('Intérêts payés à ce jour'), euros(c['interets_a_ce_jour'])),
      if (c['interets_totaux'] != null) (t('Coût total du crédit (intérêts)'), euros(c['interets_totaux'])),
      if (c['cout_total_contrat'] != null) (t('Coût total du contrat'), euros(c['cout_total_contrat'])),
      if (c['km_autorises_a_ce_jour'] != null) (t('Kilométrage autorisé à ce jour'), km(c['km_autorises_a_ce_jour'], _u)),
      if (c['km_parcourus'] != null) (t('Kilométrage parcouru'), km(c['km_parcourus'], _u)),
    ];
    final depassement = (enDouble(c['depassement_km']) ?? 0) > 0;
    final depassementFin = (enDouble(c['depassement_km_fin']) ?? 0) > 0;
    return Card(
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 8),
        child: Column(children: [
          for (final l in lignes) ListTile(dense: true, title: Text(l.$1), trailing: Text(l.$2)),
          if (depassement)
            ListTile(
              dense: true,
              leading: const Icon(Icons.warning_amber, color: Colors.orange),
              title: Text(t('Dépassement à ce jour : {km}', {'km': km(c['depassement_km'], _u)})),
              trailing: c['cout_depassement'] == null ? null : Text(euros(c['cout_depassement'])),
            ),
          if (depassementFin)
            ListTile(
              dense: true,
              leading: const Icon(Icons.trending_up, color: Colors.orange),
              title: Text(t('Au rythme actuel, fin de contrat : {km} de trop', {'km': km(c['depassement_km_fin'], _u)})),
              trailing: c['cout_depassement_fin'] == null ? null : Text(euros(c['cout_depassement_fin'])),
            ),
        ]),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final location = _type == 'leasing' || _type == 'renting';
    return Scaffold(
      appBar: AppBar(title: Text(t('Type d\'achat'))),
      body: _chargement
          ? const Center(child: CircularProgressIndicator())
          : Form(
              key: _cle,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  Wrap(spacing: 8, runSpacing: 8, children: [
                    for (final e in typesAchat.entries)
                      ChoiceChip(
                        label: Text(e.value),
                        selected: _type == e.key,
                        onSelected: (_) => setState(() => _type = e.key),
                      ),
                  ]),
                  const Divider(height: 24),
                  if (_type == 'comptant')
                    Text(t('Le prix d\'achat de la fiche du véhicule est compté dans le coût total.'),
                        style: Theme.of(context).textTheme.bodySmall)
                  else ...[
                    _champ('organisme', t('Organisme (banque, société de leasing)'), texte: true),
                    _date(),
                    _champ('duree_mois', t('Durée'), suffixe: t('mois'), entier: true),
                  ],
                  if (_type == 'pret') ...[
                    _champ('apport', t('Apport'), suffixe: '€'),
                    _champ('montant_emprunte', t('Montant emprunté'), suffixe: '€',
                        aide: t('Vide : prix d\'achat − apport.')),
                    _champ('taux_annuel', t('Taux annuel (TAEG)'), suffixe: '%'),
                    _champ('mensualite', t('Mensualité'), suffixe: '€', aide: t('Vide : calculée d\'après le taux et la durée.')),
                  ],
                  if (location) ...[
                    _champ('premier_loyer', t('Premier loyer majoré / acompte'), suffixe: '€'),
                    _champ('mensualite', t('Loyer mensuel'), suffixe: '€'),
                    if (_type == 'leasing') ...[
                      _champ('valeur_residuelle', t('Option d\'achat (valeur résiduelle)'), suffixe: '€'),
                      SwitchListTile(
                        contentPadding: EdgeInsets.zero,
                        title: Text(t('Option d\'achat levée')),
                        subtitle: Text(t('Le véhicule vous appartient : l\'option est ajoutée aux coûts.')),
                        value: _optionLevee,
                        onChanged: (v) => setState(() => _optionLevee = v),
                      ),
                    ],
                    _champ('km_annuels', t('Kilométrage autorisé par an'), suffixe: _u.symboleDistance, entier: true),
                    _champ('prix_km_supplementaire', t('Prix par {unite} supplémentaire', {'unite': _u.symboleDistance}),
                        suffixe: '€'),
                    if (_type == 'renting')
                      _champ('services_inclus', t('Services inclus (entretien, assurance, pneus…)'), texte: true),
                  ],
                  const SizedBox(height: 8),
                  _resultats(),
                  const SizedBox(height: 16),
                  FilledButton.icon(
                    onPressed: _envoi ? null : _enregistrer,
                    icon: const Icon(Icons.check),
                    label: Text(t('Enregistrer')),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    t('Prêt : le prix d\'achat et les intérêts payés entrent dans le coût total. Leasing et renting : '
                        'les loyers payés, sans prix d\'achat ni valeur de revente (sauf option d\'achat levée). '
                        'Ne saisissez pas aussi les mensualités dans « Autres dépenses ».'),
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ),
    );
  }
}

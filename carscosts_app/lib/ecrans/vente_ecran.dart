import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../api/api_client.dart';
import '../l10n/langue.dart';
import '../l10n/unites.dart';
import '../widgets/champ_pays.dart';
import '../widgets/fichiers.dart';
import '../widgets/format.dart';
import 'formules_ecran.dart';

Map<String, String> get regimesTvaVente => {
      'PRIVE': t('Vente entre particuliers (sans TVA)'),
      'NORMAL': t('Régime normal (TVA sur le prix de vente)'),
      'MARGE': t('Régime de la marge (biens d\'occasion)'),
      'INTRACOM': t('Livraison intracommunautaire exonérée (acheteur assujetti UE)'),
      'EXPORT': t('Exportation hors Union européenne (exonérée)'),
      'EXONERE': t('Exonéré (TVA non déduite à l\'achat)'),
    };

/// Documents remis à l'acheteur (cases du certificat de cession)
Map<String, String> get documentsVente => {
      'doc_certificat_immatriculation': t('Certificat d\'immatriculation'),
      'doc_coc': t('Certificat de conformité (COC)'),
      'doc_carnet_entretien': t('Carnet d\'entretien / historique'),
      'doc_car_pass': t('Car-Pass (Belgique)'),
      'doc_controle_technique': t('Certificat de contrôle technique'),
      'doc_ct_occasion': t('Contrôle technique occasion (vente)'),
    };

/// Ouvre la vente du véhicule (formule Bronze minimum). Renvoie vrai si quelque chose a changé.
Future<bool> ouvrirVente(BuildContext context, Map<String, dynamic> vehicule) async {
  if (context.read<Abonnement>().formule == 'gratuit') {
    await Navigator.push(context,
        MaterialPageRoute(builder: (_) => FormulesEcran(raison: t('La vente est disponible à partir de la formule Bronze.'))));
    return false;
  }
  final ok = await Navigator.push<bool>(context, MaterialPageRoute(builder: (_) => VenteEcran(vehicule: vehicule)));
  return ok == true;
}

/// (Re)vente du véhicule, comme dans dBSolution : acheteur, prix (TVA si usage professionnel), frais,
/// documents et clés remis, paiement ; alertes, bilan financier, certificat de cession (PDF) et finalisation.
class VenteEcran extends StatefulWidget {
  const VenteEcran({super.key, required this.vehicule});

  final Map<String, dynamic> vehicule;

  @override
  State<VenteEcran> createState() => _VenteEcranState();
}

class _VenteEcranState extends State<VenteEcran> {
  static const _textes = [
    'kilometrage_vente', 'vendeur_nom', 'vendeur_adresse', 'vendeur_tva', 'acheteur_nom', 'acheteur_adresse',
    'acheteur_tva', 'acheteur_email', 'acheteur_telephone', 'montant_saisi', 'taux_tva', 'pourcentage_taxable',
    'frais_vente', 'nombre_cles', 'etat_vehicule', 'garantie_mois', 'remarques',
  ];

  final Map<String, TextEditingController> _c = {for (final n in _textes) n: TextEditingController()};
  final Map<String, dynamic> _v = {};
  Map<String, dynamic>? _etat; // vente, alertes, bilan, mention
  String? _statut;
  bool _charge = false;
  bool _envoi = false;
  bool _modifie = false;
  Map<String, String> _erreurs = {};

  String get _chemin => 'vehicules/${widget.vehicule['id']}/vente/';
  Unites get _u => Unites.de(widget.vehicule);
  bool get _vendue => _statut == 'vendue';

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

  Future<void> _charger() async {
    try {
      _appliquer(Map<String, dynamic>.from(await context.read<ApiClient>().get(_chemin) as Map));
    } on ApiException catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    }
  }

  String _texte(dynamic v) {
    if (v == null) return '';
    final d = enDouble(v);
    if (d == null) return v.toString();
    return d == d.roundToDouble() ? d.toInt().toString() : d.toString();
  }

  void _appliquer(Map<String, dynamic> r) {
    final vente = (r['vente'] as Map?)?.cast<String, dynamic>();
    final source = vente ?? (r['proposition'] as Map?)?.cast<String, dynamic>() ?? <String, dynamic>{};
    setState(() {
      for (final n in _textes) {
        final valeur = source[n];
        _c[n]!.text = n == 'kilometrage_vente' && valeur != null
            ? _u.depuisKm(enDouble(valeur) ?? 0).round().toString()
            : _texte(valeur);
      }
      if (vente == null) {
        _c['nombre_cles']!.text = '2';
        _c['garantie_mois']!.text = '0';
        _c['pourcentage_taxable']!.text = '100';
      }
      _v
        ..['date_vente'] = source['date_vente'] ?? dateIso(DateTime.now())
        ..['date_livraison'] = source['date_livraison']
        ..['date_paiement'] = source['date_paiement']
        ..['acheteur_type'] = source['acheteur_type'] ?? 'particulier'
        ..['acheteur_pays'] = source['acheteur_pays'] ?? widget.vehicule['pays_immatriculation']
        ..['regime_tva'] = source['regime_tva'] ?? 'PRIVE'
        ..['saisie_tvac'] = source['saisie_tvac'] ?? true
        ..['mode_paiement'] = source['mode_paiement'] ?? 'virement';
      for (final d in documentsVente.keys) {
        _v[d] = source[d] ?? (d != 'doc_car_pass' && d != 'doc_controle_technique' && d != 'doc_ct_occasion');
      }
      _statut = vente?['statut'] as String?;
      _etat = vente == null ? null : r;
      _charge = true;
    });
  }

  Map<String, dynamic> _donnees() {
    String? n(String c) => _c[c]!.text.trim().isEmpty ? null : _c[c]!.text.trim().replaceAll(',', '.');
    final km = double.tryParse(n('kilometrage_vente') ?? '');
    return {
      for (final c in const ['vendeur_nom', 'vendeur_adresse', 'vendeur_tva', 'acheteur_nom', 'acheteur_adresse',
        'acheteur_tva', 'acheteur_email', 'acheteur_telephone', 'etat_vehicule', 'remarques'])
        c: _c[c]!.text.trim(),
      'kilometrage_vente': km == null ? null : _u.versKm(km).round(),
      'montant_saisi': n('montant_saisi') ?? '0',
      'taux_tva': n('taux_tva'),
      'pourcentage_taxable': n('pourcentage_taxable') ?? '100',
      'frais_vente': n('frais_vente') ?? '0',
      'nombre_cles': int.tryParse(n('nombre_cles') ?? '') ?? 2,
      'garantie_mois': int.tryParse(n('garantie_mois') ?? '') ?? 0,
      ..._v,
    };
  }

  Future<bool> _enregistrer({bool silencieux = false}) async {
    setState(() {
      _envoi = true;
      _erreurs = {};
    });
    try {
      _appliquer(Map<String, dynamic>.from(await context.read<ApiClient>().put(_chemin, _donnees()) as Map));
      _modifie = true;
      if (!silencieux && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(t('Vente enregistrée (brouillon).'))));
      }
      return true;
    } on ApiException catch (e) {
      if (mounted) {
        setState(() => _erreurs = e.champs);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
      }
      return false;
    } finally {
      if (mounted) setState(() => _envoi = false);
    }
  }

  Future<void> _action(String action, String confirmation, String succes) async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        content: Text(confirmation),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: Text(t('Annuler'))),
          FilledButton(onPressed: () => Navigator.pop(ctx, true), child: Text(t('Confirmer'))),
        ],
      ),
    );
    if (ok != true || !mounted) return;
    if (!_vendue && !await _enregistrer(silencieux: true)) return;
    if (!mounted) return;
    try {
      _appliquer(Map<String, dynamic>.from(await context.read<ApiClient>().post('$_chemin$action/', {}) as Map));
      _modifie = true;
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(succes)));
    } on ApiException catch (e) {
      if (!mounted) return;
      if (e.statut == 403 && e.champs['code'] == 'limite_formule') {
        final raison = context.read<Abonnement>().messageLimite(e.champs);
        await Navigator.push(context, MaterialPageRoute(builder: (_) => FormulesEcran(raison: raison)));
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    }
  }

  Future<void> _supprimer() async {
    try {
      await context.read<ApiClient>().delete(_chemin);
      if (mounted) Navigator.pop(context, true);
    } on ApiException catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    }
  }

  // ------------------------------------------------------------------ Champs
  Widget _champ(String nom, String libelle, {TextInputType? clavier, String? suffixe, int lignes = 1, String? aide}) =>
      Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: TextField(
          controller: _c[nom],
          enabled: !_vendue,
          keyboardType: clavier,
          maxLines: lignes,
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

  Widget _date(String nom, String libelle) {
    final valeur = _v[nom] as String?;
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        onTap: _vendue
            ? null
            : () async {
                final d = await showDatePicker(
                    context: context,
                    initialDate: DateTime.tryParse(valeur ?? '') ?? DateTime.now(),
                    firstDate: DateTime(2000),
                    lastDate: DateTime(2100));
                if (d != null) setState(() => _v[nom] = dateIso(d));
              },
        child: InputDecorator(
          decoration: InputDecoration(
              labelText: libelle, border: const OutlineInputBorder(), suffixIcon: const Icon(Icons.calendar_today)),
          child: Text(valeur == null ? '—' : dateFr(valeur)),
        ),
      ),
    );
  }

  Widget _choix(String nom, String libelle, Map<String, String> options) => Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: DropdownButtonFormField<String>(
          key: ValueKey('$nom-${_v[nom]}'),
          initialValue: options.containsKey(_v[nom]) ? _v[nom] as String : options.keys.first,
          isExpanded: true,
          decoration: InputDecoration(labelText: libelle, border: const OutlineInputBorder()),
          items: [
            for (final e in options.entries)
              DropdownMenuItem(value: e.key, child: Text(e.value, overflow: TextOverflow.ellipsis)),
          ],
          onChanged: _vendue ? null : (v) => setState(() => _v[nom] = v),
        ),
      );

  Widget _titre(String texte) => Padding(
        padding: const EdgeInsets.fromLTRB(0, 8, 0, 8),
        child: Text(texte, style: Theme.of(context).textTheme.titleMedium),
      );

  Widget _alertes() {
    final alertes = ((_etat?['alertes'] as List?) ?? []).cast<Map>();
    if (alertes.isEmpty) return const SizedBox.shrink();
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Column(children: [
        for (final a in alertes)
          ListTile(
            dense: true,
            leading: Icon(
              switch (a['niveau']) { 'erreur' => Icons.error, 'attention' => Icons.warning_amber, _ => Icons.info_outline },
              color: switch (a['niveau']) { 'erreur' => Colors.red, 'attention' => Colors.orange, _ => Colors.blueGrey },
            ),
            title: Text('${a['message']}'),
          ),
      ]),
    );
  }

  Widget _bilan() {
    final b = (_etat?['bilan'] as Map?)?.cast<String, dynamic>();
    if (b == null) return const SizedBox.shrink();
    Widget ligne(String l, dynamic v, {bool gras = false}) => Padding(
          padding: const EdgeInsets.symmetric(vertical: 3),
          child: Row(children: [
            Expanded(child: Text(l)),
            Text(v is String ? v : euros(v), style: gras ? const TextStyle(fontWeight: FontWeight.bold) : null),
          ]),
        );
    final pv = enDouble(b['plus_value']);
    final ecart = enDouble(b['ecart_estimation']);
    final coutKm = enDouble(b['cout_km']);
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(t('Bilan de la vente'), style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          ligne(t('Prix de vente'), b['prix_vente'], gras: true),
          ligne(t('Frais de vente'), b['frais_vente']),
          if (b['prix_achat'] != null) ligne(t('Prix d\'achat'), b['prix_achat']),
          if (pv != null) ligne(pv >= 0 ? t('Plus-value') : t('Moins-value'), pv.abs()),
          if (ecart != null)
            ligne(t('Écart avec la valeur estimée ({valeur})', {'valeur': euros(b['valeur_estimee'])}),
                '${ecart >= 0 ? '+' : '−'}${euros(ecart.abs())}'),
          const Divider(),
          ligne(t('Coût total (achat + usage)'), b['cout_total']),
          ligne(t('Coût net (ce que le véhicule a coûté)'), b['cout_net'], gras: true),
          if (b['mois'] != null)
            ligne(t('Coût net / mois ({n} mois)', {'n': nombre(b['mois'], decimales: 1)}), b['cout_mois']),
          if (coutKm != null)
            ligne(_u.miles ? t('Coût net au mile') : t('Coût net au km'),
                '${nombre(_u.coutParDistance(coutKm), decimales: 3)} €'),
          if ((b['km'] as num? ?? 0) > 0) ligne(t('Kilomètres parcourus'), km(b['km'], _u)),
        ]),
      ),
    );
  }

  static const _palette = [
    Color(0xFF2563EB), Color(0xFFF59E0B), Color(0xFF10B981), Color(0xFFEF4444), Color(0xFF8B5CF6),
    Color(0xFF06B6D4), Color(0xFFEC4899), Color(0xFF84CC16), Color(0xFF64748B), Color(0xFFF97316),
    Color(0xFF14B8A6), Color(0xFFA855F7),
  ];

  /// Rapport final : répartition du coût total (camembert), puis coût total − revente = coût net.
  Widget _rapportFinal() {
    final b = (_etat?['bilan'] as Map?)?.cast<String, dynamic>();
    final postes = ((b?['postes'] as List?) ?? []).cast<Map>();
    if (b == null || postes.isEmpty) return const SizedBox.shrink();
    final total = postes.fold<double>(0, (s, p) => s + (enDouble(p['montant']) ?? 0));
    if (total <= 0) return const SizedBox.shrink();
    Color couleur(int i) => _palette[i % _palette.length];
    final revente = enDouble(b['prix_vente']) ?? 0;
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(_vendue ? t('Rapport final') : t('Rapport final (estimation avant la vente)'),
              style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 12),
          SizedBox(
            height: 220,
            child: Stack(alignment: Alignment.center, children: [
              PieChart(PieChartData(
                sectionsSpace: 2,
                centerSpaceRadius: 58,
                sections: [
                  for (var i = 0; i < postes.length; i++)
                    () {
                      final v = enDouble(postes[i]['montant']) ?? 0;
                      final pct = v * 100 / total;
                      return PieChartSectionData(
                        value: v,
                        color: couleur(i),
                        radius: 46,
                        title: pct >= 6 ? '${pct.round()} %' : '',
                        titleStyle: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.white),
                      );
                    }(),
                ],
              )),
              Column(mainAxisSize: MainAxisSize.min, children: [
                Text(t('Coût total'), style: Theme.of(context).textTheme.bodySmall),
                Text(euros(total), style: const TextStyle(fontWeight: FontWeight.bold)),
              ]),
            ]),
          ),
          const SizedBox(height: 12),
          for (var i = 0; i < postes.length; i++)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 3),
              child: Row(children: [
                Container(width: 12, height: 12, decoration: BoxDecoration(color: couleur(i), shape: BoxShape.circle)),
                const SizedBox(width: 8),
                Expanded(child: Text('${postes[i]['libelle']}')),
                Text('${nombre((enDouble(postes[i]['montant']) ?? 0) * 100 / total, decimales: 1)} %  ',
                    style: Theme.of(context).textTheme.bodySmall),
                Text(euros(postes[i]['montant'])),
              ]),
            ),
          const Divider(height: 24),
          Row(children: [Expanded(child: Text(t('Coût total'))), Text(euros(total))]),
          Row(children: [
            Expanded(child: Text(t('Revente'))),
            Text('− ${euros(revente)}', style: const TextStyle(color: Colors.green)),
          ]),
          const SizedBox(height: 4),
          Row(children: [
            Expanded(child: Text(t('Coût net'), style: const TextStyle(fontWeight: FontWeight.bold))),
            Text(euros(total - revente), style: const TextStyle(fontWeight: FontWeight.bold)),
          ]),
          // Barre : part revendue / part réellement dépensée
          if (revente > 0 && revente < total) ...[
            const SizedBox(height: 8),
            ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: SizedBox(
                height: 12,
                child: Row(children: [
                  Expanded(flex: ((total - revente) * 1000 / total).round().clamp(1, 1000).toInt(),
                      child: Container(color: const Color(0xFFEF4444))),
                  Expanded(flex: (revente * 1000 / total).round().clamp(1, 1000).toInt(),
                      child: Container(color: const Color(0xFF10B981))),
                ]),
              ),
            ),
            const SizedBox(height: 4),
            Text(t('{pct} % du coût total récupéré par la revente', {'pct': nombre(revente * 100 / total, decimales: 0)}),
                style: Theme.of(context).textTheme.bodySmall),
          ],
        ]),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    const nombres = TextInputType.numberWithOptions(decimal: true);
    final regime = _v['regime_tva'] as String? ?? 'PRIVE';
    final vente = (_etat?['vente'] as Map?)?.cast<String, dynamic>();
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (pop, _) {
        if (!pop) Navigator.pop(context, _modifie);
      },
      child: Scaffold(
        appBar: AppBar(
          title: Text(t('Vente du véhicule')),
          actions: [
            if (_statut == 'brouillon')
              IconButton(icon: const Icon(Icons.delete_outline), tooltip: t('Supprimer le brouillon'), onPressed: _supprimer),
          ],
        ),
        body: !_charge
            ? const Center(child: CircularProgressIndicator())
            : ListView(padding: const EdgeInsets.all(16), children: [
                if (_vendue)
                  Card(
                    color: Colors.green.shade50,
                    child: ListTile(
                      leading: const Icon(Icons.verified, color: Colors.green),
                      title: Text(t('Vendu le {date}', {'date': dateFr(_v['date_vente'])})),
                      subtitle: Text(t('Le véhicule est archivé ; annulez la vente pour la modifier.')),
                    ),
                  ),
                _alertes(),
                _bilan(),
                _rapportFinal(),
                _titre(t('Vente')),
                _date('date_vente', t('Date de la vente')),
                _date('date_livraison', t('Date de livraison')),
                _champ('kilometrage_vente', t('Kilométrage à la vente'),
                    clavier: TextInputType.number, suffixe: _u.symboleDistance),
                _titre(t('Acheteur')),
                _choix('acheteur_type', t('Type d\'acheteur'),
                    {'particulier': t('Particulier'), 'professionnel': t('Professionnel')}),
                _champ('acheteur_nom', t('Nom de l\'acheteur')),
                _champ('acheteur_adresse', t('Adresse de l\'acheteur'), lignes: 2),
                Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: IgnorePointer(
                    ignoring: _vendue,
                    child: ChampPays(
                      valeur: _v['acheteur_pays'] as String?,
                      libelle: t('Pays de l\'acheteur'),
                      erreur: _erreurs['acheteur_pays'],
                      onChanged: (code) => setState(() => _v['acheteur_pays'] = code),
                    ),
                  ),
                ),
                if (_v['acheteur_type'] == 'professionnel' || regime == 'INTRACOM')
                  _champ('acheteur_tva', t('N° de TVA de l\'acheteur')),
                _champ('acheteur_email', t('Email de l\'acheteur'), clavier: TextInputType.emailAddress),
                _champ('acheteur_telephone', t('Téléphone de l\'acheteur'), clavier: TextInputType.phone),
                _titre(t('Prix')),
                _choix('regime_tva', t('Régime de TVA'), regimesTvaVente),
                _champ('montant_saisi', t('Prix de vente'),
                    clavier: nombres,
                    suffixe: '€',
                    aide: regime == 'PRIVE'
                        ? null
                        : t('Régime normal : HTVA (ou TVAC si la case est cochée). Autres régimes : montant total payé par l\'acheteur.')),
                if (regime == 'NORMAL') ...[
                  SwitchListTile(
                    contentPadding: EdgeInsets.zero,
                    title: Text(t('Prix encodé TVA comprise')),
                    value: _v['saisie_tvac'] == true,
                    onChanged: _vendue ? null : (v) => setState(() => _v['saisie_tvac'] = v),
                  ),
                  _champ('pourcentage_taxable', t('Pourcentage taxable (%)'),
                      clavier: nombres,
                      suffixe: '%',
                      aide: t('Base imposable limitée au pourcentage de TVA déduit à l\'achat (ex. 50 % en Belgique).')),
                ],
                if (regime == 'NORMAL' || regime == 'MARGE')
                  _champ('taux_tva', t('Taux de TVA (%)'), clavier: nombres, suffixe: '%', aide: t('Vide : taux du pays.')),
                if (vente != null && regime != 'PRIVE')
                  Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                    child: Text(t('HTVA {htva} · TVA {tva} · total {total}', {
                      'htva': euros(vente['prix_htva']),
                      'tva': euros(vente['montant_tva']),
                      'total': euros(vente['prix_tvac']),
                    })),
                  ),
                _champ('frais_vente', t('Frais de vente TVAC'),
                    clavier: nombres, suffixe: '€', aide: t('Annonce, nettoyage, contrôle technique, Car-Pass…')),
                _titre(t('Vendeur')),
                _champ('vendeur_nom', t('Nom du vendeur')),
                _champ('vendeur_adresse', t('Adresse du vendeur'), lignes: 2),
                if (regime != 'PRIVE') _champ('vendeur_tva', t('N° de TVA du vendeur')),
                _titre(t('Paiement')),
                _choix('mode_paiement', t('Mode de paiement'),
                    {'virement': t('Virement'), 'especes': t('Espèces'), 'autre': t('Autre')}),
                _date('date_paiement', t('Date du paiement')),
                _titre(t('Documents remis')),
                for (final d in documentsVente.entries)
                  CheckboxListTile(
                    contentPadding: EdgeInsets.zero,
                    title: Text(d.value),
                    value: _v[d.key] == true,
                    onChanged: _vendue ? null : (v) => setState(() => _v[d.key] = v == true),
                  ),
                _champ('nombre_cles', t('Nombre de clés'), clavier: TextInputType.number),
                _champ('etat_vehicule', t('État du véhicule / défauts connus'), lignes: 3),
                _champ('garantie_mois', t('Garantie (mois)'),
                    clavier: TextInputType.number, aide: t('0 : aucune garantie commerciale')),
                _champ('remarques', t('Remarques'), lignes: 2),
                const SizedBox(height: 8),
                if (!_vendue)
                  FilledButton.tonalIcon(
                    onPressed: _envoi ? null : () => _enregistrer(),
                    icon: const Icon(Icons.save),
                    label: Text(t('Enregistrer le brouillon')),
                  ),
                if (_statut != null)
                  Align(
                    alignment: Alignment.centerLeft,
                    child: OuvrirFichierBouton(url: '${_chemin}pdf/', libelle: t('Certificat de cession (PDF)')),
                  ),
                // Avant d'archiver : récapitulatif imprimable du véhicule et des coûts totaux
                Align(
                  alignment: Alignment.centerLeft,
                  child: TextButton.icon(
                    onPressed: () => ouvrirRecapitulatif(context, widget.vehicule),
                    icon: const Icon(Icons.print),
                    label: Text(t('Récapitulatif du véhicule (PDF)')),
                  ),
                ),
                const SizedBox(height: 8),
                if (!_vendue)
                  FilledButton.icon(
                    onPressed: _envoi
                        ? null
                        : () => _action(
                            'finaliser',
                            t('Finaliser la vente ? Le véhicule sera archivé et sa valeur de revente deviendra le prix de vente.'),
                            t('Vente finalisée.')),
                    icon: const Icon(Icons.sell),
                    label: Text(t('Finaliser la vente')),
                  )
                else
                  OutlinedButton.icon(
                    onPressed: () =>
                        _action('annuler', t('Annuler la vente ? Le véhicule redeviendra actif.'), t('Vente annulée.')),
                    icon: const Icon(Icons.undo),
                    label: Text(t('Annuler la vente')),
                  ),
                const SizedBox(height: 24),
              ]),
      ),
    );
  }
}

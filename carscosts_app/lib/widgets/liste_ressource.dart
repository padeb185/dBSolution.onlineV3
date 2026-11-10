import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../api/api_client.dart';
import '../l10n/langue.dart';
import '../l10n/unites.dart';
import '../ecrans/formulaire_ecran.dart';
import '../ecrans/formules_ecran.dart';
import '../ecrans/plan_entretien_ecran.dart';
import '../modeles/ressources.dart';
import 'fichiers.dart';
import 'format.dart';

/// Pastille de statut d'un rappel (en retard / proche / à venir).
class StatutRappel extends StatelessWidget {
  const StatutRappel({super.key, required this.statut, this.unites});

  final Map<String, dynamic>? statut;

  /// Unités du véhicule du rappel (km restants affichés en km ou en miles)
  final Unites? unites;

  @override
  Widget build(BuildContext context) {
    final s = statut?['statut'] as String? ?? 'a_venir';
    final (texte, couleur) = switch (s) {
      'en_retard' => (t('En retard'), Colors.red),
      'proche' => (t('Bientôt'), Colors.orange),
      'inactif' => (t('Terminé'), Colors.grey),
      _ => (t('À venir'), Colors.green),
    };
    final details = [
      if (statut?['jours_restants'] != null) t('{n} j', {'n': statut!['jours_restants']}),
      if (statut?['km_restants'] != null) km(statut!['km_restants'], unites),
    ].join(' · ');
    return Chip(
      visualDensity: VisualDensity.compact,
      backgroundColor: couleur.shade50,
      side: BorderSide(color: couleur.shade200),
      label: Text(details.isEmpty ? texte : '$texte · $details', style: TextStyle(color: couleur.shade900, fontSize: 12)),
    );
  }
}

/// Liste des éléments d'une ressource pour un véhicule, avec ajout / modification.
class ListeRessource extends StatefulWidget {
  const ListeRessource(
      {super.key, required this.ressource, required this.vehiculeId, this.auChangement, this.vehicule});

  final Ressource ressource;
  final String vehiculeId;
  final Map<String, dynamic>? vehicule;
  final VoidCallback? auChangement;

  @override
  State<ListeRessource> createState() => _ListeRessourceState();
}

class _ListeRessourceState extends State<ListeRessource> with AutomaticKeepAliveClientMixin {
  late Future<List<Map<String, dynamic>>> _elements;

  @override
  bool get wantKeepAlive => true;

  @override
  void initState() {
    super.initState();
    _charger();
  }

  bool get _verrouillee => widget.ressource.bronze && context.read<Abonnement>().formule == 'gratuit';

  bool _chargeeVerrouillee = false;

  void _charger() {
    _chargeeVerrouillee = _verrouillee;
    if (_chargeeVerrouillee) {
      _elements = Future.value(const []);
      return;
    }
    _elements = context
        .read<ApiClient>()
        .get('${widget.ressource.chemin}/', params: {...widget.ressource.params, 'vehicule': widget.vehiculeId}).then(
            (r) => [for (final e in r as List) Map<String, dynamic>.from(e as Map)]);
  }

  Future<void> _ouvrir([Map<String, dynamic>? element]) async {
    final modifie = await Navigator.push<bool>(
      context,
      MaterialPageRoute(
        builder: (_) => FormulaireEcran(
            ressource: widget.ressource, vehiculeId: widget.vehiculeId, element: element, vehicule: widget.vehicule),
      ),
    );
    if (modifie == true) {
      setState(_charger);
      widget.auChangement?.call();
    }
  }

  Future<void> _rappelFait(Map<String, dynamic> rappel) async {
    final api = context.read<ApiClient>();
    final kmCtrl = TextEditingController();
    final u = Unites.de(widget.vehicule);
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(t('« {libelle} » réalisé', {'libelle': rappel['libelle']})),
        content: TextField(
          controller: kmCtrl,
          keyboardType: TextInputType.number,
          decoration: InputDecoration(labelText: t('Kilométrage actuel'), suffixText: u.symboleDistance),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: Text(t('Annuler'))),
          FilledButton(onPressed: () => Navigator.pop(ctx, true), child: Text(t('Valider'))),
        ],
      ),
    );
    if (ok != true) return;
    try {
      await api.post('rappels/${rappel['id']}/fait/', {
        'date': dateIso(DateTime.now()),
        if (double.tryParse(kmCtrl.text.replaceAll(',', '.')) != null)
          'kilometrage': u.versKm(double.parse(kmCtrl.text.replaceAll(',', '.'))).round(),
      });
      setState(_charger);
      widget.auChangement?.call();
    } on ApiException catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    }
  }

  /// Rappels : accès au plan d'entretien (entretien, contrôle technique, assurance)
  Widget _planEntretien() => Card(
        margin: const EdgeInsets.fromLTRB(12, 12, 12, 4),
        color: Theme.of(context).colorScheme.primaryContainer,
        child: ListTile(
          leading: const Icon(Icons.event_repeat),
          title: Text(t('Plan d\'entretien')),
          subtitle: Text(t('Entretien (1 ou 2 ans + km), contrôle technique, assurance')),
          trailing: const Icon(Icons.chevron_right),
          onTap: () async {
            final ok = await Navigator.push<bool>(
                context, MaterialPageRoute(builder: (_) => PlanEntretienEcran(vehicule: widget.vehicule ?? {'id': widget.vehiculeId})));
            if (ok == true && mounted) {
              setState(_charger);
              widget.auChangement?.call();
            }
          },
        ),
      );

  /// Ressource réservée aux formules payantes (Bronze minimum)
  Widget _verrou() => ListView(padding: const EdgeInsets.all(24), children: [
        const Icon(Icons.lock_outline, size: 48),
        const SizedBox(height: 12),
        Text(t('« {titre} » est disponible à partir de la formule Bronze.', {'titre': widget.ressource.titre}),
            textAlign: TextAlign.center, style: Theme.of(context).textTheme.titleMedium),
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
    final r = widget.ressource;
    if (r.bronze && context.watch<Abonnement>().formule == 'gratuit') return _verrou();
    if (_chargeeVerrouillee) _charger();   // formule payante prise entre-temps : chargement de la liste
    return Scaffold(
      floatingActionButton: FloatingActionButton.extended(
        heroTag: r.chemin,
        onPressed: () => _ouvrir(),
        icon: const Icon(Icons.add),
        label: Text(t('Ajouter')),
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          setState(_charger);
          await _elements;
        },
        child: FutureBuilder<List<Map<String, dynamic>>>(
          future: _elements,
          builder: (context, snap) {
            if (snap.connectionState != ConnectionState.done) {
              return const Center(child: CircularProgressIndicator());
            }
            if (snap.hasError) {
              return ListView(children: [Padding(padding: const EdgeInsets.all(24), child: Text('${snap.error}'))]);
            }
            final elements = snap.data!;
            if (elements.isEmpty) {
              return ListView(children: [
                if (r.chemin == 'rappels') _planEntretien(),
                Padding(
                  padding: const EdgeInsets.all(32),
                  child: Column(children: [
                    Icon(r.icone, size: 48, color: Colors.grey),
                    const SizedBox(height: 8),
                    Text(r.texteVide, textAlign: TextAlign.center),
                  ]),
                ),
              ]);
            }
            final entete = r.chemin == 'rappels' ? 1 : 0;
            return ListView.separated(
              padding: const EdgeInsets.only(bottom: 88),
              itemCount: elements.length + entete,
              separatorBuilder: (_, __) => const Divider(height: 1),
              itemBuilder: (context, index) {
                if (index < entete) return _planEntretien();
                final i = index - entete;
                final e = elements[i];
                final montant = r.montantLigne?.call(e) ?? '';
                final u = Unites.de(widget.vehicule);
                final ticket = e['ticket'] as String?;
                return ListTile(
                  leading: ticket != null
                      ? SizedBox(width: 48, height: 48, child: ImageProtegee(url: ticket, hauteur: 48))
                      : CircleAvatar(child: Icon(r.iconeLigne?.call(e) ?? r.icone)),
                  title: Text(r.titreLigne(e, u)),
                  subtitle: r.chemin == 'rappels'
                      ? Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                          Text(r.sousTitreLigne(e, u)),
                          StatutRappel(statut: (e['statut'] as Map?)?.cast<String, dynamic>(), unites: u),
                        ])
                      : Text(r.sousTitreLigne(e, u)),
                  trailing: r.chemin == 'rappels' && e['actif'] == true
                      ? IconButton(icon: const Icon(Icons.task_alt), tooltip: t('Marquer comme fait'), onPressed: () => _rappelFait(e))
                      : (montant.isEmpty ? null : Text(montant, style: const TextStyle(fontWeight: FontWeight.w600))),
                  onTap: () {
                    if (r.modifiable?.call(e) ?? true) {
                      _ouvrir(e);
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                          content: Text(t('Ce kilométrage vient d\'un plein, d\'une recharge, d\'un entretien ou de l\'achat : modifiez-le à sa source.'))));
                    }
                  },
                );
              },
            );
          },
        ),
      ),
    );
  }
}

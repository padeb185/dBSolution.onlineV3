import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../api/api_client.dart';
import '../ecrans/formulaire_ecran.dart';
import '../modeles/ressources.dart';
import 'fichiers.dart';
import 'format.dart';

/// Pastille de statut d'un rappel (en retard / proche / à venir).
class StatutRappel extends StatelessWidget {
  const StatutRappel({super.key, required this.statut});

  final Map<String, dynamic>? statut;

  @override
  Widget build(BuildContext context) {
    final s = statut?['statut'] as String? ?? 'a_venir';
    final (texte, couleur) = switch (s) {
      'en_retard' => ('En retard', Colors.red),
      'proche' => ('Bientôt', Colors.orange),
      'inactif' => ('Terminé', Colors.grey),
      _ => ('À venir', Colors.green),
    };
    final details = [
      if (statut?['jours_restants'] != null) '${statut!['jours_restants']} j',
      if (statut?['km_restants'] != null) km(statut!['km_restants']),
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
  const ListeRessource({super.key, required this.ressource, required this.vehiculeId, this.auChangement});

  final Ressource ressource;
  final String vehiculeId;
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

  void _charger() {
    _elements = context
        .read<ApiClient>()
        .get('${widget.ressource.chemin}/', params: {'vehicule': widget.vehiculeId}).then(
            (r) => [for (final e in r as List) Map<String, dynamic>.from(e as Map)]);
  }

  Future<void> _ouvrir([Map<String, dynamic>? element]) async {
    final modifie = await Navigator.push<bool>(
      context,
      MaterialPageRoute(
        builder: (_) => FormulaireEcran(ressource: widget.ressource, vehiculeId: widget.vehiculeId, element: element),
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
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('« ${rappel['libelle']} » réalisé'),
        content: TextField(
          controller: kmCtrl,
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(labelText: 'Kilométrage actuel', suffixText: 'km'),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Annuler')),
          FilledButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Valider')),
        ],
      ),
    );
    if (ok != true) return;
    try {
      await api.post('rappels/${rappel['id']}/fait/', {
        'date': dateIso(DateTime.now()),
        if (int.tryParse(kmCtrl.text) != null) 'kilometrage': int.parse(kmCtrl.text),
      });
      setState(_charger);
      widget.auChangement?.call();
    } on ApiException catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    }
  }

  @override
  Widget build(BuildContext context) {
    super.build(context);
    final r = widget.ressource;
    return Scaffold(
      floatingActionButton: FloatingActionButton.extended(
        heroTag: r.chemin,
        onPressed: () => _ouvrir(),
        icon: const Icon(Icons.add),
        label: Text('Ajouter'),
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
                Padding(
                  padding: const EdgeInsets.all(32),
                  child: Column(children: [
                    Icon(r.icone, size: 48, color: Colors.grey),
                    const SizedBox(height: 8),
                    Text('Aucun ${r.titreSingulier} pour l\'instant.', textAlign: TextAlign.center),
                  ]),
                ),
              ]);
            }
            return ListView.separated(
              padding: const EdgeInsets.only(bottom: 88),
              itemCount: elements.length,
              separatorBuilder: (_, __) => const Divider(height: 1),
              itemBuilder: (context, i) {
                final e = elements[i];
                final montant = r.montantLigne?.call(e) ?? '';
                final ticket = e['ticket'] as String?;
                return ListTile(
                  leading: ticket != null
                      ? SizedBox(width: 48, height: 48, child: ImageProtegee(url: ticket, hauteur: 48))
                      : CircleAvatar(child: Icon(r.icone)),
                  title: Text(r.titreLigne(e)),
                  subtitle: r.chemin == 'rappels'
                      ? Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                          Text(r.sousTitreLigne(e)),
                          StatutRappel(statut: (e['statut'] as Map?)?.cast<String, dynamic>()),
                        ])
                      : Text(r.sousTitreLigne(e)),
                  trailing: r.chemin == 'rappels' && e['actif'] == true
                      ? IconButton(icon: const Icon(Icons.task_alt), tooltip: 'Marquer comme fait', onPressed: () => _rappelFait(e))
                      : (montant.isEmpty ? null : Text(montant, style: const TextStyle(fontWeight: FontWeight.w600))),
                  onTap: () => _ouvrir(e),
                );
              },
            );
          },
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../api/api_client.dart';
import '../api/session.dart';
import '../widgets/fichiers.dart';
import '../widgets/format.dart';
import '../widgets/liste_ressource.dart';
import 'compte_ecran.dart';
import 'vehicule_ecran.dart';
import 'vehicule_form_ecran.dart';

/// Accueil : rappels à traiter, véhicules et dépenses du mois.
class AccueilEcran extends StatefulWidget {
  const AccueilEcran({super.key});

  @override
  State<AccueilEcran> createState() => _AccueilEcranState();
}

class _AccueilEcranState extends State<AccueilEcran> {
  late Future<Map<String, dynamic>> _tableau;

  @override
  void initState() {
    super.initState();
    _charger();
  }

  void _charger() {
    _tableau = context.read<ApiClient>().get('tableau-de-bord/').then((r) => Map<String, dynamic>.from(r as Map));
    _tableau.catchError((Object e) {
      if (e is ApiException && e.statut == 401 && mounted) context.read<Session>().sessionExpiree();
      return <String, dynamic>{};
    });
  }

  Future<void> _ajouterVehicule() async {
    final ok = await Navigator.push<bool>(context, MaterialPageRoute(builder: (_) => const VehiculeFormEcran()));
    if (ok == true) setState(_charger);
  }

  Future<void> _ouvrir(Map<String, dynamic> v) async {
    await Navigator.push(context, MaterialPageRoute(builder: (_) => VehiculeEcran(vehicule: v)));
    if (mounted) setState(_charger);
  }

  @override
  Widget build(BuildContext context) {
    final session = context.watch<Session>();
    return Scaffold(
      appBar: AppBar(
        title: Text('Bonjour ${session.utilisateur?['prenom'] ?? ''}'),
        actions: [
          IconButton(
            icon: const Icon(Icons.account_circle),
            tooltip: 'Mon compte',
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const CompteEcran())),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _ajouterVehicule,
        icon: const Icon(Icons.add),
        label: const Text('Véhicule'),
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          setState(_charger);
          await _tableau;
        },
        child: FutureBuilder<Map<String, dynamic>>(
          future: _tableau,
          builder: (context, snap) {
            if (snap.connectionState != ConnectionState.done) return const Center(child: CircularProgressIndicator());
            if (snap.hasError) {
              return ListView(children: [Padding(padding: const EdgeInsets.all(24), child: Text('${snap.error}'))]);
            }
            final t = snap.data!;
            final vehicules = [for (final v in (t['vehicules'] as List? ?? [])) Map<String, dynamic>.from(v as Map)];
            final rappels = [for (final r in (t['rappels'] as List? ?? [])) Map<String, dynamic>.from(r as Map)];
            final noms = {for (final v in vehicules) v['id']: '${v['marque']} ${v['modele']}'};
            return ListView(
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 96),
              children: [
                if (rappels.isNotEmpty) ...[
                  Text('À traiter', style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 8),
                  Card(
                    child: Column(children: [
                      for (final r in rappels)
                        ListTile(
                          leading: const Icon(Icons.notifications_active),
                          title: Text(r['libelle'].toString()),
                          subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                            Text(noms[r['vehicule']] ?? ''),
                            StatutRappel(statut: (r['statut'] as Map?)?.cast<String, dynamic>()),
                          ]),
                          onTap: () {
                            final v = vehicules.where((x) => x['id'] == r['vehicule']);
                            if (v.isNotEmpty) _ouvrir(v.first);
                          },
                        ),
                    ]),
                  ),
                  const SizedBox(height: 16),
                ],
                Row(children: [
                  Expanded(child: Text('Mes véhicules', style: Theme.of(context).textTheme.titleMedium)),
                  Text('Ce mois-ci : ${euros(t['depenses_mois'])}'),
                ]),
                const SizedBox(height: 8),
                if (vehicules.isEmpty)
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(children: [
                        const Icon(Icons.directions_car, size: 48),
                        const SizedBox(height: 8),
                        const Text('Ajoutez votre premier véhicule pour suivre ses pleins, entretiens et coûts.',
                            textAlign: TextAlign.center),
                        const SizedBox(height: 12),
                        FilledButton.icon(
                            onPressed: _ajouterVehicule, icon: const Icon(Icons.add), label: const Text('Ajouter un véhicule')),
                      ]),
                    ),
                  ),
                for (final v in vehicules)
                  Card(
                    clipBehavior: Clip.antiAlias,
                    child: ListTile(
                      contentPadding: const EdgeInsets.all(12),
                      leading: v['photo'] != null
                          ? SizedBox(width: 64, height: 64, child: ImageProtegee(url: v['photo'] as String, hauteur: 64))
                          : const CircleAvatar(radius: 28, child: Icon(Icons.directions_car)),
                      title: Text('${v['marque']} ${v['modele']}', style: const TextStyle(fontWeight: FontWeight.w600)),
                      subtitle: Text([
                        if ((v['immatriculation'] ?? '').toString().isNotEmpty) v['immatriculation'],
                        km(v['kilometrage_actuel']),
                      ].join(' · ')),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: () => _ouvrir(v),
                    ),
                  ),
              ],
            );
          },
        ),
      ),
    );
  }
}

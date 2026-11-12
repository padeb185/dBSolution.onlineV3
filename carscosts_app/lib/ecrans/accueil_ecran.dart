import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../api/api_client.dart';
import '../api/session.dart';
import '../l10n/langue.dart';
import '../l10n/unites.dart';
import '../widgets/bandeau_abonnement.dart';
import '../widgets/fichiers.dart';
import '../widgets/format.dart';
import '../widgets/liste_ressource.dart';
import '../modeles/catalogue.dart';
import '../widgets/logo_marque.dart';
import '../widgets/plaque.dart';
import 'carte_ecran.dart';
import 'formules_ecran.dart';
import 'reglages_ecran.dart';
import 'vehicule_ecran.dart';
import 'vehicule_form_ecran.dart';
import 'simulateur_ecran.dart';
import 'vehicules_vendus_ecran.dart';

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

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // Logos des marques (catalogue téléchargé une fois par session)
    Catalogue.charger(context.read<ApiClient>()).then((_) {
      if (mounted) setState(() {});
    });
  }

  void _charger() {
    final abonnement = context.read<Abonnement>();
    _tableau = context.read<ApiClient>().get('tableau-de-bord/').then((r) {
      final d = Map<String, dynamic>.from(r as Map);
      abonnement.mettreAJour(d['abonnement']);
      return d;
    });
    _tableau.catchError((Object e) {
      if (e is ApiException && e.statut == 401 && mounted) context.read<Session>().sessionExpiree();
      return <String, dynamic>{};
    });
  }

  Future<void> _ajouterVehicule() async {
    final ab = context.read<Abonnement>();
    if (!ab.peutAjouter) {
      await _formules(ab.messageLimite());
      return;
    }
    if (!mounted) return;
    final ok = await Navigator.push<bool>(context, MaterialPageRoute(builder: (_) => const VehiculeFormEcran()));
    if (ok == true) setState(_charger);
  }

  Future<void> _formules([String? raison]) async {
    await Navigator.push(context, MaterialPageRoute(builder: (_) => FormulesEcran(raison: raison)));
    if (mounted) setState(_charger);
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
        title: Text(t('Bonjour {prenom}', {'prenom': session.utilisateur?['prenom'] ?? ''})),
        actions: [
          IconButton(
            icon: const Icon(Icons.map_outlined),
            tooltip: t('Carte'),
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const CarteEcran())),
          ),
          IconButton(
            icon: const Icon(Icons.calculate_outlined),
            tooltip: t('Simulateur d\'achat'),
            onPressed: () => ouvrirSimulateur(context),
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            tooltip: t('Réglages'),
            onPressed: () async {
              await Navigator.push(context, MaterialPageRoute(builder: (_) => const ReglagesEcran()));
              if (mounted) setState(_charger);
            },
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _ajouterVehicule,
        icon: const Icon(Icons.add),
        label: Text(t('Véhicule')),
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
            final tableau = snap.data!;
            final vehicules = [for (final v in (tableau['vehicules'] as List? ?? [])) Map<String, dynamic>.from(v as Map)];
            final rappels = [for (final r in (tableau['rappels'] as List? ?? [])) Map<String, dynamic>.from(r as Map)];
            final noms = {for (final v in vehicules) v['id']: '${v['marque']} ${v['modele']}'};
            final abonnement = context.watch<Abonnement>();
            return ListView(
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 96),
              children: [
                BandeauAbonnement(apresRetour: () {
                  if (mounted) setState(_charger);
                }),
                if (rappels.isNotEmpty) ...[
                  Text(t('À traiter'), style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 8),
                  Card(
                    child: Column(children: [
                      for (final r in rappels)
                        ListTile(
                          leading: const Icon(Icons.notifications_active),
                          title: Text(r['libelle'].toString()),
                          subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                            Text(noms[r['vehicule']] ?? ''),
                            StatutRappel(
                              statut: (r['statut'] as Map?)?.cast<String, dynamic>(),
                              unites: Unites.de(vehicules.where((x) => x['id'] == r['vehicule']).firstOrNull),
                            ),
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
                  Expanded(child: Text(t('Mes véhicules'), style: Theme.of(context).textTheme.titleMedium)),
                  Text(t('Ce mois-ci : {montant}', {'montant': euros(tableau['depenses_mois'])})),
                ]),
                const SizedBox(height: 8),
                if (vehicules.isEmpty)
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(children: [
                        const Icon(Icons.directions_car, size: 48),
                        const SizedBox(height: 8),
                        Text(t('Ajoutez votre premier véhicule pour suivre ses pleins, entretiens et coûts.'),
                            textAlign: TextAlign.center),
                        const SizedBox(height: 12),
                        FilledButton.icon(
                            onPressed: _ajouterVehicule, icon: const Icon(Icons.add), label: Text(t('Ajouter un véhicule'))),
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
                          : LogoMarque(marque: v['marque'] as String?),
                      title: Text('${v['marque']} ${v['modele']}', style: const TextStyle(fontWeight: FontWeight.w600)),
                      subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        if ((v['immatriculation'] ?? '').toString().isNotEmpty)
                          Padding(
                            padding: const EdgeInsets.symmetric(vertical: 4),
                            child: Plaque(
                                numero: v['immatriculation'].toString(),
                                pays: v['pays_immatriculation'] as String?,
                                hauteur: 24),
                          ),
                        Text(km(v['kilometrage_actuel'], Unites.de(v))),
                      ]),
                      trailing: abonnement.estEnLectureSeule(v['id'])
                          ? Tooltip(message: t('Lecture seule'), child: const Icon(Icons.lock_outline))
                          : const Icon(Icons.chevron_right),
                      onTap: () => _ouvrir(v),
                    ),
                  ),
                const SizedBox(height: 8),
                // Carte : stations, bornes de recharge, garages, dépanneurs, monteurs de pneus
                Card(
                  child: ListTile(
                    leading: const Icon(Icons.map),
                    title: Text(t('Carte')),
                    subtitle: Text(t('Stations, bornes de recharge, garages, dépanneurs et pneus autour de vous')),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const CarteEcran())),
                  ),
                ),
                // Simulateur d'achat (formule Bronze) : prêt, taxes, immatriculation, rapport financier
                Card(
                  child: ListTile(
                    leading: const Icon(Icons.calculate),
                    title: Text(t('Simulateur d\'achat')),
                    subtitle: Text(t('Prêt, taxes de mise en circulation et de roulage, immatriculation, plaques, coût total')),
                    trailing: context.watch<Abonnement>().formule == 'gratuit'
                        ? const Chip(label: Text('Bronze'))
                        : const Icon(Icons.chevron_right),
                    onTap: () => ouvrirSimulateur(context),
                  ),
                ),
                Align(
                  alignment: Alignment.centerLeft,
                  child: TextButton.icon(
                    icon: const Icon(Icons.inventory_2_outlined),
                    label: Text(t('Véhicules vendus ou archivés')),
                    onPressed: () async {
                      await Navigator.push(context, MaterialPageRoute(builder: (_) => const VehiculesVendusEcran()));
                      if (mounted) setState(_charger);
                    },
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

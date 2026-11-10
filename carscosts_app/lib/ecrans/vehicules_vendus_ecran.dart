import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../api/api_client.dart';
import '../l10n/langue.dart';
import '../widgets/format.dart';
import '../widgets/logo_marque.dart';
import 'vehicule_ecran.dart';

/// Véhicules vendus ou archivés : la fiche reste consultable (bilan, certificat de cession, annulation).
class VehiculesVendusEcran extends StatefulWidget {
  const VehiculesVendusEcran({super.key});

  @override
  State<VehiculesVendusEcran> createState() => _VehiculesVendusEcranState();
}

class _VehiculesVendusEcranState extends State<VehiculesVendusEcran> {
  late Future<List<Map<String, dynamic>>> _vehicules;
  bool _modifie = false;

  @override
  void initState() {
    super.initState();
    _charger();
  }

  void _charger() {
    _vehicules = context.read<ApiClient>().get('vehicules/', params: {'archives': '1'}).then((r) => [
          for (final v in r as List)
            if ((v as Map)['archive'] == true) Map<String, dynamic>.from(v),
        ]);
  }

  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (pop, _) {
        if (!pop) Navigator.pop(context, _modifie);
      },
      child: Scaffold(
        appBar: AppBar(title: Text(t('Véhicules vendus ou archivés'))),
        body: FutureBuilder<List<Map<String, dynamic>>>(
          future: _vehicules,
          builder: (context, snap) {
            if (snap.connectionState != ConnectionState.done) return const Center(child: CircularProgressIndicator());
            if (snap.hasError) return Center(child: Text('${snap.error}'));
            final vehicules = snap.data!;
            if (vehicules.isEmpty) return Center(child: Text(t('Aucun véhicule vendu ou archivé.')));
            return ListView(padding: const EdgeInsets.all(16), children: [
              for (final v in vehicules)
                Card(
                  child: ListTile(
                    leading: LogoMarque(marque: v['marque'] as String?, taille: 40),
                    title: Text('${v['marque']} ${v['modele']}'),
                    subtitle: Text([
                      if ((v['immatriculation'] ?? '').toString().isNotEmpty) v['immatriculation'],
                      km(v['kilometrage_actuel']),
                    ].join(' · ')),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () async {
                      await Navigator.push(context, MaterialPageRoute(builder: (_) => VehiculeEcran(vehicule: v)));
                      if (mounted) {
                        _modifie = true;
                        setState(_charger);
                      }
                    },
                  ),
                ),
            ]);
          },
        ),
      ),
    );
  }
}

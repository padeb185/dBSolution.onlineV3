import 'dart:io' show Platform;

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';

import '../api/api_client.dart';
import '../l10n/langue.dart';
import '../l10n/unites.dart';

/// Catégorie de lieu affichée sur la carte.
class CategorieLieu {
  const CategorieLieu(this.code, this.icone, this.couleur);

  final String code;
  final IconData icone;
  final Color couleur;

  String get libelle => switch (code) {
        'carburant' => t('Carburant'),
        'recharge' => t('Recharge électrique'),
        'garage' => t('Garages'),
        'depannage' => t('Dépanneurs'),
        'pneus' => t('Pneus'),
        _ => code,
      };
}

const categoriesCarte = [
  CategorieLieu('carburant', Icons.local_gas_station, Color(0xFFEA580C)),
  CategorieLieu('recharge', Icons.ev_station, Color(0xFF16A34A)),
  CategorieLieu('garage', Icons.build, Color(0xFF2563EB)),
  CategorieLieu('depannage', Icons.car_crash, Color(0xFFDC2626)),
  CategorieLieu('pneus', Icons.tire_repair, Color(0xFF7C3AED)),
];

CategorieLieu categorieCarte(String? code) =>
    categoriesCarte.firstWhere((c) => c.code == code, orElse: () => categoriesCarte.first);

/// Carte : stations de carburant, bornes de recharge, garages, dépanneurs et monteurs de pneus autour de vous
/// (données OpenStreetMap, via l'API CarsCosts).
class CarteEcran extends StatefulWidget {
  const CarteEcran({super.key, this.categoriesInitiales});

  /// Catégories cochées à l'ouverture (toutes par défaut).
  final Set<String>? categoriesInitiales;

  @override
  State<CarteEcran> createState() => _CarteEcranState();
}

class _CarteEcranState extends State<CarteEcran> {
  static const _bruxelles = LatLng(50.8466, 4.3528);
  static const _rayon = 5000;

  final _carte = MapController();
  late Set<String> _categories = widget.categoriesInitiales ?? {for (final c in categoriesCarte) c.code};
  LatLng? _position;               // position de l'utilisateur
  LatLng _centreRecherche = _bruxelles;
  List<Map<String, dynamic>> _lieux = [];
  bool _chargement = false;
  bool _deplacee = false;          // carte déplacée depuis la dernière recherche : « Rechercher ici »
  String? _erreur;

  @override
  void initState() {
    super.initState();
    _localiser();
  }

  Future<void> _localiser() async {
    try {
      if (!await Geolocator.isLocationServiceEnabled()) throw t('Localisation désactivée sur cet appareil.');
      var permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied || permission == LocationPermission.deniedForever) {
        throw t('Autorisez la localisation pour voir les lieux autour de vous.');
      }
      final p = await Geolocator.getCurrentPosition(
          locationSettings: const LocationSettings(accuracy: LocationAccuracy.medium, timeLimit: Duration(seconds: 15)));
      _position = LatLng(p.latitude, p.longitude);
      _centreRecherche = _position!;
      if (mounted) {
        try {
          _carte.move(_position!, 14);
        } catch (_) {}   // carte pas encore affichée : centrée au prochain « Ma position »
      }
    } catch (e) {
      // Sans position : recherche autour du centre de la carte (Bruxelles par défaut)
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e is String ? e : t('Position introuvable.'))));
      }
    }
    await _rechercher(_centreRecherche);
  }

  Future<void> _rechercher(LatLng centre) async {
    setState(() {
      _chargement = true;
      _erreur = null;
      _deplacee = false;
      _centreRecherche = centre;
    });
    try {
      final r = await context.read<ApiClient>().get('carte/', params: {
        'lat': centre.latitude.toStringAsFixed(5),
        'lon': centre.longitude.toStringAsFixed(5),
        'rayon': '$_rayon',
        'types': categoriesCarte.map((c) => c.code).join(','),
      });
      final lieux = [for (final l in (r as Map)['lieux'] as List) Map<String, dynamic>.from(l as Map)];
      if (mounted) setState(() => _lieux = lieux);
    } on ApiException catch (e) {
      if (mounted) setState(() => _erreur = e.message);
    } finally {
      if (mounted) setState(() => _chargement = false);
    }
  }

  List<Map<String, dynamic>> get _visibles => _lieux.where((l) => _categories.contains(l['categorie'])).toList();

  // ------------------------------------------------------------------ actions
  Future<void> _ouvrirUrl(Uri uri) async {
    if (!await launchUrl(uri, mode: LaunchMode.externalApplication) && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(t('Impossible d\'ouvrir {url}', {'url': '$uri'}))));
    }
  }

  void _itineraire(Map<String, dynamic> l) {
    final dest = '${l['lat']},${l['lon']}';
    final apple = !kIsWeb && (Platform.isIOS || Platform.isMacOS);
    _ouvrirUrl(apple
        ? Uri.parse('https://maps.apple.com/?daddr=$dest')
        : Uri.parse('https://www.google.com/maps/dir/?api=1&destination=$dest'));
  }

  String _distance(dynamic metres) {
    final u = Unites.compte;
    final km = (metres as num? ?? 0) / 1000;
    if (!u.miles && km < 1) return '${(km * 1000).round()} m';
    final v = u.depuisKm(km);
    return '${v.toStringAsFixed(v < 10 ? 1 : 0)} ${u.symboleDistance}';
  }

  String _titre(Map<String, dynamic> l) {
    final nom = (l['nom'] ?? '').toString();
    return nom.isEmpty ? categorieCarte(l['categorie'] as String?).libelle : nom;
  }

  void _fiche(Map<String, dynamic> l) {
    final cat = categorieCarte(l['categorie'] as String?);
    final prises = [for (final p in (l['prises'] as List? ?? [])) Map<String, dynamic>.from(p as Map)];
    final carburants = (l['carburants'] as List? ?? []).cast<String>();
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      builder: (ctx) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 0, 20, 16),
          child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              CircleAvatar(backgroundColor: cat.couleur, foregroundColor: Colors.white, child: Icon(cat.icone)),
              const SizedBox(width: 12),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(_titre(l), style: Theme.of(ctx).textTheme.titleLarge),
                  Text([cat.libelle, _distance(l['distance'])].join(' · ')),
                ]),
              ),
            ]),
            const SizedBox(height: 12),
            if ((l['adresse'] ?? '') != '') _info(Icons.place_outlined, l['adresse'].toString()),
            if ((l['exploitant'] ?? '') != '' && l['exploitant'] != l['nom']) _info(Icons.business, l['exploitant'].toString()),
            if ((l['horaires'] ?? '') != '') _info(Icons.schedule, l['horaires'].toString()),
            if (carburants.isNotEmpty) _info(Icons.local_gas_station_outlined, carburants.join(' · ')),
            if (prises.isNotEmpty)
              _info(Icons.electrical_services, [
                for (final p in prises) '${p['type']} ×${p['nombre']}',
                if ((l['puissance_max'] ?? '') != '') t('jusqu\'à {p}', {'p': l['puissance_max']}),
              ].join(' · ')),
            if (l['points_de_charge'] != null) _info(Icons.ev_station_outlined, t('{n} point(s) de charge', {'n': l['points_de_charge']})),
            if (l['payant'] != null) _info(Icons.euro, l['payant'] == true ? t('Payant') : t('Gratuit')),
            if ((l['services'] as List? ?? []).isNotEmpty)
              _info(Icons.check_circle_outline, [
                for (final s in (l['services'] as List))
                  switch (s) {
                    'pneus' => t('Pneus'),
                    'depannage' => t('Dépannage'),
                    'lavage' => t('Lavage'),
                    'boutique' => t('Boutique'),
                    _ => '$s',
                  }
              ].join(' · ')),
            const SizedBox(height: 12),
            Wrap(spacing: 8, runSpacing: 8, children: [
              FilledButton.icon(
                onPressed: () => _itineraire(l),
                icon: const Icon(Icons.directions),
                label: Text(t('Itinéraire')),
              ),
              if ((l['telephone'] ?? '') != '')
                OutlinedButton.icon(
                  onPressed: () => _ouvrirUrl(Uri(scheme: 'tel', path: l['telephone'].toString().replaceAll(' ', ''))),
                  icon: const Icon(Icons.phone),
                  label: Text(t('Appeler')),
                ),
              if ((l['site'] ?? '') != '')
                OutlinedButton.icon(
                  onPressed: () {
                    final site = l['site'].toString();
                    _ouvrirUrl(Uri.parse(site.startsWith('http') ? site : 'https://$site'));
                  },
                  icon: const Icon(Icons.language),
                  label: Text(t('Site web')),
                ),
            ]),
          ]),
        ),
      ),
    );
  }

  Widget _info(IconData icone, String texte) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 3),
        child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Icon(icone, size: 18, color: Colors.grey.shade700),
          const SizedBox(width: 10),
          Expanded(child: Text(texte)),
        ]),
      );

  /// Liste des lieux visibles, du plus proche au plus loin.
  void _liste() {
    final lieux = _visibles;
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      builder: (ctx) => DraggableScrollableSheet(
        expand: false,
        initialChildSize: 0.6,
        maxChildSize: 0.95,
        builder: (ctx, defilement) => lieux.isEmpty
            ? Center(child: Text(t('Aucun lieu dans cette zone.')))
            : ListView.separated(
                controller: defilement,
                itemCount: lieux.length,
                separatorBuilder: (_, __) => const Divider(height: 1),
                itemBuilder: (ctx, i) {
                  final l = lieux[i];
                  final cat = categorieCarte(l['categorie'] as String?);
                  return ListTile(
                    leading: CircleAvatar(backgroundColor: cat.couleur, foregroundColor: Colors.white, child: Icon(cat.icone, size: 20)),
                    title: Text(_titre(l)),
                    subtitle: Text([cat.libelle, if ((l['adresse'] ?? '') != '') l['adresse']].join(' · ')),
                    trailing: Text(_distance(l['distance']), style: const TextStyle(fontWeight: FontWeight.w600)),
                    onTap: () {
                      Navigator.pop(ctx);
                      _carte.move(LatLng((l['lat'] as num).toDouble(), (l['lon'] as num).toDouble()), 16);
                      _fiche(l);
                    },
                  );
                },
              ),
      ),
    );
  }

  // ------------------------------------------------------------------ écran
  Marker _marqueur(Map<String, dynamic> l) {
    final cat = categorieCarte(l['categorie'] as String?);
    return Marker(
      point: LatLng((l['lat'] as num).toDouble(), (l['lon'] as num).toDouble()),
      width: 36,
      height: 36,
      child: GestureDetector(
        onTap: () => _fiche(l),
        child: Container(
          decoration: BoxDecoration(
            color: cat.couleur,
            shape: BoxShape.circle,
            border: Border.all(color: Colors.white, width: 2),
            boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 3, offset: Offset(0, 1))],
          ),
          child: Icon(cat.icone, color: Colors.white, size: 18),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final visibles = _visibles;
    return Scaffold(
      appBar: AppBar(
        title: Text(t('Carte')),
        actions: [
          IconButton(
            icon: const Icon(Icons.list),
            tooltip: t('Liste ({n})', {'n': visibles.length}),
            onPressed: _liste,
          ),
        ],
      ),
      body: Stack(children: [
        FlutterMap(
          mapController: _carte,
          options: MapOptions(
            initialCenter: _bruxelles,
            initialZoom: 13,
            onPositionChanged: (camera, geste) {
              if (geste && !_deplacee && const Distance().as(LengthUnit.Meter, camera.center, _centreRecherche) > _rayon / 3) {
                setState(() => _deplacee = true);
              }
            },
          ),
          children: [
            TileLayer(
              urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
              userAgentPackageName: 'com.carscosts.carscosts_app',
            ),
            MarkerLayer(markers: [
              for (final l in visibles) _marqueur(l),
              if (_position != null)
                Marker(
                  point: _position!,
                  width: 22,
                  height: 22,
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.blue,
                      shape: BoxShape.circle,
                      border: Border.all(color: Colors.white, width: 3),
                      boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 4)],
                    ),
                  ),
                ),
            ]),
            RichAttributionWidget(attributions: [
              TextSourceAttribution('OpenStreetMap contributors',
                  onTap: () => _ouvrirUrl(Uri.parse('https://www.openstreetmap.org/copyright'))),
            ]),
          ],
        ),
        // Filtres par catégorie
        Positioned(
          top: 8,
          left: 0,
          right: 0,
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 8),
            child: Row(children: [
              for (final c in categoriesCarte)
                Padding(
                  padding: const EdgeInsets.only(right: 6),
                  child: FilterChip(
                    avatar: Icon(c.icone, size: 18, color: _categories.contains(c.code) ? Colors.white : c.couleur),
                    label: Text(c.libelle),
                    selected: _categories.contains(c.code),
                    showCheckmark: false,
                    selectedColor: c.couleur,
                    labelStyle: TextStyle(color: _categories.contains(c.code) ? Colors.white : null),
                    backgroundColor: Theme.of(context).colorScheme.surface,
                    elevation: 2,
                    onSelected: (oui) => setState(() => oui ? _categories.add(c.code) : _categories.remove(c.code)),
                  ),
                ),
            ]),
          ),
        ),
        if (_deplacee && !_chargement)
          Positioned(
            top: 60,
            left: 0,
            right: 0,
            child: Center(
              child: FilledButton.icon(
                onPressed: () => _rechercher(_carte.camera.center),
                icon: const Icon(Icons.search),
                label: Text(t('Rechercher dans cette zone')),
              ),
            ),
          ),
        if (_chargement) const Positioned(top: 60, left: 0, right: 0, child: Center(child: CircularProgressIndicator())),
        if (_erreur != null)
          Positioned(
            bottom: 24,
            left: 16,
            right: 16,
            child: Card(
              color: Theme.of(context).colorScheme.errorContainer,
              child: ListTile(
                title: Text(_erreur!),
                trailing: TextButton(onPressed: () => _rechercher(_centreRecherche), child: Text(t('Réessayer'))),
              ),
            ),
          ),
      ]),
      floatingActionButton: FloatingActionButton(
        tooltip: t('Ma position'),
        onPressed: () async {
          if (_position != null) {
            _carte.move(_position!, 14);
            await _rechercher(_position!);
          } else {
            await _localiser();
          }
        },
        child: const Icon(Icons.my_location),
      ),
    );
  }
}

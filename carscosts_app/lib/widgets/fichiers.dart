import 'dart:io';

import 'package:flutter/material.dart';
import 'package:open_filex/open_filex.dart';
import 'package:path_provider/path_provider.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../api/api_client.dart';
import '../ecrans/formules_ecran.dart';
import '../l10n/langue.dart';

/// Image privée servie par l'API (ticket, photo) : chargée avec le jeton.
class ImageProtegee extends StatelessWidget {
  const ImageProtegee({super.key, required this.url, this.hauteur = 120});

  final String url;
  final double hauteur;

  @override
  Widget build(BuildContext context) {
    final api = context.read<ApiClient>();
    return GestureDetector(
      onTap: () => Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => Scaffold(
            appBar: AppBar(),
            body: InteractiveViewer(child: Center(child: Image.network(url, headers: api.entetesAuth))),
          ),
        ),
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(8),
        child: Image.network(
          url,
          headers: api.entetesAuth,
          height: hauteur,
          fit: BoxFit.cover,
          errorBuilder: (_, __, ___) => const Icon(Icons.broken_image, size: 48),
        ),
      ),
    );
  }
}

/// Télécharge un fichier privé (PDF, photo) avec le jeton et l'ouvre avec l'application du système
/// (aperçu iOS / lecteur PDF Android : imprimer, enregistrer, partager).
Future<void> ouvrirFichierProtege(BuildContext context, String url, {String? nom}) async {
  final api = context.read<ApiClient>();
  final messager = ScaffoldMessenger.of(context);
  try {
    final octets = await api.telecharger(url);
    final dossier = await getTemporaryDirectory();
    final base = nom ?? Uri.parse(url).pathSegments.where((s) => s.isNotEmpty).join('_');
    final fichier = File('${dossier.path}${Platform.pathSeparator}$base${_extension(octets)}');
    await fichier.writeAsBytes(octets);
    await OpenFilex.open(fichier.path);
  } on ApiException catch (e) {
    messager.showSnackBar(SnackBar(content: Text(e.message)));
  }
}

/// Extension d'après la signature du fichier (PDF, JPEG, PNG).
String _extension(List<int> o) {
  if (o.length > 4 && o[0] == 0x25 && o[1] == 0x50 && o[2] == 0x44 && o[3] == 0x46) return '.pdf';
  if (o.length > 3 && o[0] == 0xFF && o[1] == 0xD8) return '.jpg';
  if (o.length > 4 && o[0] == 0x89 && o[1] == 0x50) return '.png';
  return '';
}

/// Récapitulatif du véhicule et de ses coûts totaux (PDF à imprimer ou télécharger), formule Bronze minimum.
Future<void> ouvrirRecapitulatif(BuildContext context, Map<String, dynamic> vehicule) async {
  if (context.read<Abonnement>().formule == 'gratuit') {
    await Navigator.push(context, MaterialPageRoute(
        builder: (_) => FormulesEcran(raison: t('Le récapitulatif PDF est disponible à partir de la formule Bronze.'))));
    return;
  }
  final nom = 'recapitulatif_${vehicule['marque']}_${vehicule['modele']}'.replaceAll(RegExp(r'[^A-Za-z0-9_-]'), '_');
  await ouvrirFichierProtege(context, 'vehicules/${vehicule['id']}/recapitulatif/pdf/', nom: nom);
}

/// Télécharge un fichier privé (PDF, photo) et l'ouvre avec l'application du système.
class OuvrirFichierBouton extends StatelessWidget {
  const OuvrirFichierBouton({super.key, required this.url, this.libelle});

  final String url;
  final String? libelle;

  Future<void> _ouvrir(BuildContext context) => ouvrirFichierProtege(context, url);

  @override
  Widget build(BuildContext context) => TextButton.icon(
        onPressed: () => _ouvrir(context),
        icon: const Icon(Icons.open_in_new),
        label: Text(libelle ?? t('Ouvrir le fichier joint')),
      );
}

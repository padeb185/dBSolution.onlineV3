import 'package:flutter/material.dart';

import '../modeles/catalogue.dart';

/// Logo de la marque (logos de dBSolution, servis par le serveur) à la place de l'icône véhicule ;
/// marque sans logo ou hors ligne : icône véhicule.
class LogoMarque extends StatelessWidget {
  const LogoMarque({super.key, required this.marque, this.taille = 56});

  final String? marque;
  final double taille;

  @override
  Widget build(BuildContext context) {
    final url = Catalogue.logo(marque ?? '');
    final repli = CircleAvatar(radius: taille / 2, child: Icon(Icons.directions_car, size: taille * 0.5));
    if (url == null) return repli;
    // Logo seul, sans fond ni cercle
    return SizedBox(
      width: taille,
      height: taille,
      child: Image.network(
        url,
        fit: BoxFit.contain,
        errorBuilder: (_, __, ___) => Icon(Icons.directions_car, size: taille * 0.6, color: Colors.grey),
      ),
    );
  }
}

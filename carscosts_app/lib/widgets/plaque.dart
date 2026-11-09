import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../l10n/langue.dart';
import '../modeles/pays.dart';

/// Style d'une plaque : code sur la bande, fond, texte, bordure, étoiles UE.
/// Mêmes couleurs que dBSolution (parking/models.py STYLES_PLAQUE, components/plaque.html).
class StylePlaque {
  const StylePlaque(this.nom, this.code, this.fond, this.texte, this.bordure, {this.etoiles = true});

  final String nom;
  final String code;
  final Color fond;
  final Color texte;
  final Color bordure;
  final bool etoiles;

  bool get suisse => code == 'CH';
  bool get bande => code.isNotEmpty && !suisse;
}

const _blanc = Color(0xFFFFFFFF);
const _noir = Color(0xFF000000);
const _rouge = Color(0xFFC8102E);

/// Pays dont la plaque a un style propre (code ISO enregistré par l'API).
/// Les autres pays (liste complète : modeles/pays.dart) reçoivent la plaque par défaut.
const stylesPlaque = <String, StylePlaque>{
  'BE': StylePlaque('Belgique', 'B', _blanc, Color(0xFF8B0000), Color(0xFF8B0000)),
  'LU': StylePlaque('Luxembourg', 'L', Color(0xFFFFEB3B), _noir, _noir),
  'NL': StylePlaque('Pays-Bas', 'NL', Color(0xFFF7C600), _noir, _noir),
  'FR': StylePlaque('France', 'F', _blanc, _noir, _noir),
  'DE': StylePlaque('Allemagne', 'D', _blanc, _noir, _noir),
  'AT': StylePlaque('Autriche', 'A', _blanc, _noir, _rouge),
  'IE': StylePlaque('Irlande', 'IRL', _blanc, _noir, _noir),
  'IT': StylePlaque('Italie', 'I', _blanc, _noir, _noir),
  'ES': StylePlaque('Espagne', 'E', _blanc, _noir, _noir),
  'PT': StylePlaque('Portugal', 'P', _blanc, _noir, _noir),
  'GR': StylePlaque('Grèce', 'GR', _blanc, _noir, _noir),
  'CY': StylePlaque('Chypre', 'CY', _blanc, _noir, _noir),
  'MT': StylePlaque('Malte', 'M', _blanc, _noir, _noir),
  'DK': StylePlaque('Danemark', 'DK', _blanc, _noir, _rouge),
  'SE': StylePlaque('Suède', 'S', _blanc, _noir, _noir),
  'FI': StylePlaque('Finlande', 'FIN', _blanc, _noir, _noir),
  'EE': StylePlaque('Estonie', 'EST', _blanc, _noir, _noir),
  'LV': StylePlaque('Lettonie', 'LV', _blanc, _noir, _noir),
  'LT': StylePlaque('Lituanie', 'LT', _blanc, _noir, _noir),
  'PL': StylePlaque('Pologne', 'PL', _blanc, _noir, _noir),
  'CZ': StylePlaque('Tchéquie', 'CZ', _blanc, _noir, _noir),
  'SK': StylePlaque('Slovaquie', 'SK', _blanc, _noir, _noir),
  'HU': StylePlaque('Hongrie', 'H', _blanc, _noir, _noir),
  'SI': StylePlaque('Slovénie', 'SLO', _blanc, _noir, Color(0xFF00843D)),
  'HR': StylePlaque('Croatie', 'HR', _blanc, _noir, _noir),
  'RO': StylePlaque('Roumanie', 'RO', _blanc, _noir, _noir),
  'BG': StylePlaque('Bulgarie', 'BG', _blanc, _noir, _noir),
  'GB': StylePlaque('Royaume-Uni', 'UK', _blanc, _noir, _noir, etoiles: false),
  'NO': StylePlaque('Norvège', 'N', _blanc, _noir, _noir, etoiles: false),
  'CH': StylePlaque('Suisse', 'CH', _blanc, _noir, _noir, etoiles: false),
};

/// Plaque par défaut (pays sans style propre) : fond blanc, texte et bordure noirs,
/// bande gris foncé avec le code ISO du pays.
const _grisBande = Color(0xFF374151);

StylePlaque stylePlaque(String? pays) {
  final code = (pays ?? '').toUpperCase();
  return stylesPlaque[code] ?? StylePlaque(paysImmatriculation[code] ?? code, code, _blanc, _noir, _noir, etoiles: false);
}

/// Plaque d'immatriculation dessinée comme dans dBSolution : bande bleue UE (étoiles + code pays)
/// ou écusson suisse, fond, couleur du texte et bordure propres au pays.
/// Nombre de caractères réservés sur la plaque (les numéros plus courts sont centrés)
const caracteresPlaque = 9;

double _largeurTexte(String texte, TextStyle style, TextScaler echelle) {
  final tp = TextPainter(
      text: TextSpan(text: texte, style: style), textDirection: TextDirection.ltr, maxLines: 1, textScaler: echelle)
    ..layout();
  return tp.width.ceilToDouble();
}

class Plaque extends StatelessWidget {
  const Plaque({super.key, required this.numero, this.pays, this.hauteur = 28});

  final String numero;
  final String? pays;
  final double hauteur;

  @override
  Widget build(BuildContext context) {
    final s = stylePlaque(pays);
    final defaut = !stylesPlaque.containsKey((pays ?? '').toUpperCase());
    final h = hauteur;
    final texte = numero.toUpperCase();
    final echelle = MediaQuery.textScalerOf(context);
    final style = TextStyle(
      color: s.texte,
      fontWeight: FontWeight.w700,
      fontSize: h * 0.58,
      letterSpacing: h * 0.02,
      height: 1,
      fontFamily: 'Arial',
      fontFamilyFallback: const ['Helvetica', 'Roboto'],
    );
    return Semantics(
      label: t('Plaque {pays} {numero}', {'pays': paysImmatriculation[(pays ?? '').toUpperCase()] ?? s.nom, 'numero': numero}),
      child: Container(
        height: h,
        decoration: BoxDecoration(
          color: s.fond,
          border: Border.all(color: s.bordure, width: math.max(1, h * 0.06)),
          borderRadius: BorderRadius.circular(h * 0.12),
          boxShadow: const [BoxShadow(color: Color(0x40000000), blurRadius: 2, offset: Offset(0, 1))],
        ),
        clipBehavior: Clip.antiAlias,
        child: Row(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          if (s.bande)
            Container(
              width: h * 0.62,
              color: defaut ? _grisBande : const Color(0xFF003399),
              child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                if (s.etoiles) SizedBox.square(dimension: h * 0.4, child: const CustomPaint(painter: _EtoilesUe())),
                SizedBox(height: h * 0.02),
                Text(s.code,
                    style: TextStyle(
                        color: _blanc, fontWeight: FontWeight.bold, fontSize: h * 0.27, height: 1)),
              ]),
            )
          else if (s.suisse)
            SizedBox(
              width: h * 0.62,
              child: Center(
                child: SizedBox(width: h * 0.45, height: h * 0.53, child: const CustomPaint(painter: _EcussonSuisse())),
              ),
            ),
          Padding(
            padding: EdgeInsets.symmetric(horizontal: h * 0.2),
            // Largeur fixe de 9 caractères (même plaque pour tous les numéros), numéro centré ;
            // un numéro plus long élargit la plaque.
            child: SizedBox(
              width: math.max(_largeurTexte('H' * caracteresPlaque, style, echelle), _largeurTexte(texte, style, echelle)),
              child: Center(child: Text(texte, maxLines: 1, softWrap: false, textAlign: TextAlign.center, style: style)),
            ),
          ),
        ]),
      ),
    );
  }
}

/// Cercle de 12 étoiles jaunes (rendues en points, comme dans dBSolution).
class _EtoilesUe extends CustomPainter {
  const _EtoilesUe();

  @override
  void paint(Canvas canvas, Size taille) {
    final p = Paint()..color = const Color(0xFFFFDD00);
    final c = taille.center(Offset.zero);
    final r = taille.width * 0.35;
    for (var i = 0; i < 12; i++) {
      final a = -math.pi / 2 + i * math.pi / 6;
      canvas.drawCircle(c + Offset(math.cos(a) * r, math.sin(a) * r), taille.width * 0.065, p);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter ancien) => false;
}

/// Écusson rouge à croix blanche (plaques suisses).
class _EcussonSuisse extends CustomPainter {
  const _EcussonSuisse();

  @override
  void paint(Canvas canvas, Size t) {
    final sx = t.width / 32, sy = t.height / 38;
    final ecusson = Path()
      ..moveTo(2 * sx, 2 * sy)
      ..lineTo(30 * sx, 2 * sy)
      ..lineTo(30 * sx, 17 * sy)
      ..cubicTo(30 * sx, 27 * sy, 23 * sx, 33 * sy, 16 * sx, 36 * sy)
      ..cubicTo(9 * sx, 33 * sy, 2 * sx, 27 * sy, 2 * sx, 17 * sy)
      ..close();
    canvas.drawPath(ecusson, Paint()..color = const Color(0xFFDA291C));
    final blanc = Paint()..color = _blanc;
    canvas.drawRect(Rect.fromLTWH(13.25 * sx, 8 * sy, 5.5 * sx, 18 * sy), blanc);
    canvas.drawRect(Rect.fromLTWH(7 * sx, 14.25 * sy, 18 * sx, 5.5 * sy), blanc);
  }

  @override
  bool shouldRepaint(covariant CustomPainter ancien) => false;
}

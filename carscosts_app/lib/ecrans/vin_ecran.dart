import 'dart:io';

import 'package:flutter/material.dart';
import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';
import 'package:image_picker/image_picker.dart';
import 'package:mobile_scanner/mobile_scanner.dart';

/// Extraction d'un VIN (17 caractères, sans I, O ni Q) dans un texte lu par OCR ou un code-barres.
/// Les confusions fréquentes de l'OCR sont corrigées : O → 0, I → 1, Q → 0.
String? extraireVin(String texte) {
  final vinExact = RegExp(r'^[A-HJ-NPR-Z0-9]{17}$');
  String corriger(String t) => t.replaceAll('O', '0').replaceAll('I', '1').replaceAll('Q', '0');
  final majuscules = texte.toUpperCase();

  // 1) Un mot de 17 caractères (cas courant : VIN isolé sur sa ligne ou après « E »)
  final mots = [
    for (final m in majuscules.split(RegExp(r'[\s:;,.*\-]+'))) corriger(m),
  ].where(vinExact.hasMatch).toList();
  if (mots.isNotEmpty) return mots.firstWhere(cleVinValide, orElse: () => mots.first);

  // 2) VIN coupé par des espaces : fenêtres de 17 caractères dans chaque ligne compactée
  final fenetres = <String>[];
  for (final ligne in majuscules.split(RegExp(r'[\n\r]'))) {
    final compacte = corriger(ligne.replaceAll(RegExp(r'[^A-Z0-9]'), ''));
    for (var i = 0; i + 17 <= compacte.length; i++) {
      final f = compacte.substring(i, i + 17);
      if (vinExact.hasMatch(f)) fenetres.add(f);
    }
  }
  if (fenetres.isEmpty) return null;
  return fenetres.firstWhere(cleVinValide, orElse: () => fenetres.first);
}

/// Clé de contrôle ISO 3779 (obligatoire en Amérique du Nord, souvent présente ailleurs).
bool cleVinValide(String vin) {
  const valeurs = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5,
    'P': 7, 'R': 9, 'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9,
  };
  const poids = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2];
  if (vin.length != 17) return false;
  var somme = 0;
  for (var i = 0; i < 17; i++) {
    final c = vin[i];
    final v = int.tryParse(c) ?? valeurs[c];
    if (v == null) return false;
    somme += v * poids[i];
  }
  final reste = somme % 11;
  return vin[8] == (reste == 10 ? 'X' : '$reste');
}

/// Lecture du VIN : code-barres (pare-brise, montant de porte) ou photo du certificat d'immatriculation (OCR).
/// Renvoie le VIN lu (Navigator.pop).
class VinEcran extends StatefulWidget {
  const VinEcran({super.key});

  @override
  State<VinEcran> createState() => _VinEcranState();
}

class _VinEcranState extends State<VinEcran> {
  final _saisie = TextEditingController();
  MobileScannerController? _scanner;
  bool _lecture = false;
  String? _message;

  bool get _mobile => Platform.isIOS || Platform.isAndroid;

  @override
  void initState() {
    super.initState();
    if (_mobile) {
      _scanner = MobileScannerController(
        formats: const [BarcodeFormat.code39, BarcodeFormat.code128, BarcodeFormat.dataMatrix, BarcodeFormat.qrCode],
      );
    }
  }

  @override
  void dispose() {
    _scanner?.dispose();
    _saisie.dispose();
    super.dispose();
  }

  void _trouve(String vin) {
    if (!mounted || _lecture) return;
    _lecture = true;
    Navigator.pop(context, vin);
  }

  void _codeBarres(BarcodeCapture capture) {
    for (final code in capture.barcodes) {
      final vin = extraireVin(code.rawValue ?? '');
      if (vin != null) return _trouve(vin);
    }
  }

  Future<void> _photoOcr() async {
    final photo = await ImagePicker().pickImage(source: ImageSource.camera, maxWidth: 2400);
    if (photo == null) return;
    setState(() => _message = 'Lecture en cours…');
    final lecteur = TextRecognizer(script: TextRecognitionScript.latin);
    try {
      final resultat = await lecteur.processImage(InputImage.fromFilePath(photo.path));
      final vin = extraireVin(resultat.text);
      if (vin != null) {
        _trouve(vin);
      } else {
        setState(() => _message = 'Aucun VIN trouvé : cadrez la ligne du numéro de châssis (case E de la carte grise).');
      }
    } finally {
      await lecteur.close();
    }
  }

  void _valider() {
    final vin = _saisie.text.toUpperCase().replaceAll(' ', '');
    if (RegExp(r'^[A-HJ-NPR-Z0-9]{17}$').hasMatch(vin)) {
      _trouve(vin);
    } else {
      setState(() => _message = 'Le VIN compte 17 caractères (lettres I, O et Q exclues).');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Lire le VIN')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (_scanner != null) ...[
            const Text('Visez le code-barres du VIN (bas du pare-brise ou montant de porte).'),
            const SizedBox(height: 8),
            ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: SizedBox(height: 260, child: MobileScanner(controller: _scanner!, onDetect: _codeBarres)),
            ),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: _photoOcr,
              icon: const Icon(Icons.document_scanner),
              label: const Text('Photographier la carte grise (lecture du texte)'),
            ),
            const Divider(height: 32),
          ],
          TextField(
            controller: _saisie,
            textCapitalization: TextCapitalization.characters,
            maxLength: 17,
            decoration: const InputDecoration(labelText: 'Ou saisissez le VIN', border: OutlineInputBorder()),
            onSubmitted: (_) => _valider(),
          ),
          FilledButton(onPressed: _valider, child: const Text('Valider')),
          if (_message != null) Padding(padding: const EdgeInsets.only(top: 12), child: Text(_message!)),
        ],
      ),
    );
  }
}

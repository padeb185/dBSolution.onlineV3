import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';

import '../api/api_client.dart';
import '../modeles/ressources.dart';
import '../widgets/fichiers.dart';
import '../widgets/format.dart';
import '../modeles/pays.dart';
import '../widgets/plaque.dart';
import 'formules_ecran.dart';
import 'vin_ecran.dart';

/// Création / modification d'un véhicule (avec lecture du VIN).
class VehiculeFormEcran extends StatefulWidget {
  const VehiculeFormEcran({super.key, this.vehicule});

  final Map<String, dynamic>? vehicule;

  @override
  State<VehiculeFormEcran> createState() => _VehiculeFormEcranState();
}

class _VehiculeFormEcranState extends State<VehiculeFormEcran> {
  final _cle = GlobalKey<FormState>();
  static const _textes = [
    'marque', 'modele', 'version', 'immatriculation', 'vin', 'annee', 'prix_achat', 'kilometrage_achat',
    'valeur_estimee', 'couleur',
  ];
  final Map<String, TextEditingController> _c = {};
  String _energie = 'essence';
  String _pays = 'BE';
  String? _miseEnCirculation;
  String? _dateAchat;
  bool _archive = false;
  String? _photo;
  Map<String, String> _erreurs = {};
  bool _envoi = false;
  String? _infoVin;

  bool get _modification => widget.vehicule != null;

  @override
  void initState() {
    super.initState();
    final v = widget.vehicule ?? {};
    for (final n in _textes) {
      _c[n] = TextEditingController(text: v[n]?.toString() ?? '');
    }
    _energie = (v['energie'] as String?) ?? 'essence';
    final pays = (v['pays_immatriculation'] as String?)?.toUpperCase();
    _pays = paysImmatriculation.containsKey(pays) ? pays! : 'BE';
    _miseEnCirculation = v['date_mise_en_circulation'] as String?;
    _dateAchat = v['date_achat'] as String?;
    _archive = v['archive'] == true;
  }

  @override
  void dispose() {
    for (final c in _c.values) {
      c.dispose();
    }
    super.dispose();
  }

  Future<void> _lireVin() async {
    final vin = await Navigator.push<String>(context, MaterialPageRoute(builder: (_) => const VinEcran()));
    if (vin == null || !mounted) return;
    _c['vin']!.text = vin;
    try {
      final d = Map<String, dynamic>.from(await context.read<ApiClient>().get('vin/', params: {'vin': vin}) as Map);
      setState(() {
        if (_c['marque']!.text.isEmpty && d['brand'] != null) _c['marque']!.text = _titre(d['brand'].toString());
        final annee = d['model_year'] ?? d['production_year'];
        if (_c['annee']!.text.isEmpty && annee != null) _c['annee']!.text = annee.toString();
        _infoVin = [if (d['brand'] != null) d['brand'], if (annee != null) 'année $annee'].join(' – ');
      });
    } on ApiException catch (e) {
      setState(() => _infoVin = e.message);
    }
  }

  String _titre(String s) => s.isEmpty ? s : s[0].toUpperCase() + s.substring(1).toLowerCase();

  Future<void> _enregistrer() async {
    if (!_cle.currentState!.validate()) return;
    final api = context.read<ApiClient>();
    String? t(String n) => _c[n]!.text.trim().isEmpty ? null : _c[n]!.text.trim().replaceAll(',', '.');
    final donnees = <String, dynamic>{
      for (final n in ['marque', 'modele', 'version', 'immatriculation', 'couleur']) n: _c[n]!.text.trim(),
      'vin': _c['vin']!.text.trim().toUpperCase(),
      'annee': int.tryParse(t('annee') ?? ''),
      'prix_achat': t('prix_achat'),
      'kilometrage_achat': int.tryParse(t('kilometrage_achat') ?? ''),
      'valeur_estimee': t('valeur_estimee'),
      'energie': _energie,
      'pays_immatriculation': _pays,
      'date_mise_en_circulation': _miseEnCirculation,
      'date_achat': _dateAchat,
      'archive': _archive,
    };
    final chemin = _modification ? 'vehicules/${widget.vehicule!['id']}/' : 'vehicules/';
    setState(() {
      _envoi = true;
      _erreurs = {};
    });
    try {
      if (_photo == null) {
        _modification ? await api.patch(chemin, donnees) : await api.post(chemin, donnees);
      } else {
        await api.envoyerAvecFichiers(_modification ? 'PATCH' : 'POST', chemin, donnees, [FichierEnvoi('photo', _photo!)]);
      }
      if (mounted) Navigator.pop(context, true);
    } on ApiException catch (e) {
      if (!mounted) return;
      if (e.statut == 403 && e.champs['code'] == 'limite_formule') {
        // Limite de la formule atteinte (ajout ou désarchivage) : proposer une formule supérieure
        await Navigator.push(context, MaterialPageRoute(builder: (_) => FormulesEcran(raison: e.message)));
        return;
      }
      setState(() => _erreurs = e.champs);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    } finally {
      if (mounted) setState(() => _envoi = false);
    }
  }

  Widget _texte(String nom, String libelle,
      {bool obligatoire = false, TextInputType? clavier, String? suffixe, Widget? bouton}) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: TextFormField(
        controller: _c[nom],
        keyboardType: clavier,
        textCapitalization: nom == 'vin' || nom == 'immatriculation' ? TextCapitalization.characters : TextCapitalization.sentences,
        decoration: InputDecoration(
          labelText: libelle + (obligatoire ? ' *' : ''),
          suffixText: suffixe,
          suffixIcon: bouton,
          errorText: _erreurs[nom],
          border: const OutlineInputBorder(),
        ),
        validator: (v) => obligatoire && (v == null || v.trim().isEmpty) ? 'Champ obligatoire' : null,
      ),
    );
  }

  Widget _date(String libelle, String? valeur, ValueChanged<String?> choisir) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        onTap: () async {
          final d = await showDatePicker(
            context: context,
            initialDate: DateTime.tryParse(valeur ?? '') ?? DateTime.now(),
            firstDate: DateTime(1950),
            lastDate: DateTime(2100),
          );
          if (d != null) setState(() => choisir(dateIso(d)));
        },
        child: InputDecorator(
          decoration: InputDecoration(labelText: libelle, border: const OutlineInputBorder(), suffixIcon: const Icon(Icons.calendar_today)),
          child: Text(valeur == null ? '—' : dateFr(valeur)),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    const nombres = TextInputType.numberWithOptions(decimal: true);
    final mobile = Platform.isIOS || Platform.isAndroid;
    return Scaffold(
      appBar: AppBar(title: Text(_modification ? 'Modifier le véhicule' : 'Nouveau véhicule')),
      body: Form(
        key: _cle,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _texte('vin', 'VIN (numéro de châssis)',
                bouton: IconButton(icon: const Icon(Icons.qr_code_scanner), tooltip: 'Lire le VIN', onPressed: _lireVin)),
            if (_infoVin != null) Padding(padding: const EdgeInsets.only(bottom: 12), child: Text(_infoVin!)),
            _texte('marque', 'Marque', obligatoire: true),
            _texte('modele', 'Modèle', obligatoire: true),
            _texte('version', 'Version / finition'),
            _texte('immatriculation', 'Immatriculation'),
            // Aperçu de la plaque (pays choisi ci-dessous)
            ValueListenableBuilder<TextEditingValue>(
              valueListenable: _c['immatriculation']!,
              builder: (context, valeur, _) => valeur.text.trim().isEmpty
                  ? const SizedBox.shrink()
                  : Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: Align(
                        alignment: Alignment.centerLeft,
                        child: Plaque(numero: valeur.text.trim(), pays: _pays, hauteur: 36),
                      ),
                    ),
            ),
            Padding(
              padding: const EdgeInsets.only(bottom: 12),
              child: DropdownButtonFormField<String>(
                initialValue: _energie,
                decoration: const InputDecoration(labelText: 'Énergie', border: OutlineInputBorder()),
                items: [for (final e in energies.entries) DropdownMenuItem(value: e.key, child: Text(e.value))],
                onChanged: (v) => setState(() => _energie = v ?? 'essence'),
              ),
            ),
            Padding(
              padding: const EdgeInsets.only(bottom: 12),
              child: DropdownButtonFormField<String>(
                initialValue: _pays,
                decoration: const InputDecoration(labelText: 'Pays d\'immatriculation', border: OutlineInputBorder()),
                isExpanded: true,
                menuMaxHeight: 420,
                items: [
                  for (final e in paysImmatriculation.entries)
                    DropdownMenuItem(value: e.key, child: Text(e.value, overflow: TextOverflow.ellipsis)),
                ],
                onChanged: (v) => setState(() => _pays = v ?? 'BE'),
              ),
            ),
            _texte('annee', 'Année du modèle', clavier: TextInputType.number),
            _date('Première mise en circulation', _miseEnCirculation, (v) => _miseEnCirculation = v),
            _texte('couleur', 'Couleur'),
            const Divider(height: 24),
            Text('Achat', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            _date('Date d\'achat', _dateAchat, (v) => _dateAchat = v),
            _texte('prix_achat', 'Prix d\'achat', clavier: nombres, suffixe: '€'),
            _texte('kilometrage_achat', 'Kilométrage à l\'achat', clavier: TextInputType.number, suffixe: 'km'),
            _texte('valeur_estimee', 'Valeur de revente estimée', clavier: nombres, suffixe: '€'),
            const Divider(height: 24),
            if (_photo != null)
              ClipRRect(borderRadius: BorderRadius.circular(8), child: Image.file(File(_photo!), height: 160, fit: BoxFit.cover))
            else if (widget.vehicule?['photo'] != null)
              ImageProtegee(url: widget.vehicule!['photo'] as String, hauteur: 160),
            Wrap(spacing: 8, children: [
              if (mobile)
                OutlinedButton.icon(
                  onPressed: () async {
                    final p = await ImagePicker().pickImage(source: ImageSource.camera, maxWidth: 1600, imageQuality: 85);
                    if (p != null) setState(() => _photo = p.path);
                  },
                  icon: const Icon(Icons.photo_camera),
                  label: const Text('Photo du véhicule'),
                ),
              OutlinedButton.icon(
                onPressed: () async {
                  final p = await ImagePicker().pickImage(source: ImageSource.gallery, maxWidth: 1600, imageQuality: 85);
                  if (p != null) setState(() => _photo = p.path);
                },
                icon: const Icon(Icons.photo_library),
                label: const Text('Choisir une photo'),
              ),
            ]),
            if (_modification)
              SwitchListTile(
                contentPadding: EdgeInsets.zero,
                title: const Text('Véhicule vendu (archivé)'),
                value: _archive,
                onChanged: (v) => setState(() => _archive = v),
              ),
            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: _envoi ? null : _enregistrer,
              icon: const Icon(Icons.check),
              label: const Text('Enregistrer'),
            ),
          ],
        ),
      ),
    );
  }
}

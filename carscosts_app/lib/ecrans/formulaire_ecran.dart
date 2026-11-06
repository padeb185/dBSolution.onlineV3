import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';

import '../api/api_client.dart';
import '../modeles/ressources.dart';
import '../widgets/fichiers.dart';
import '../widgets/format.dart';

bool get estMobile => Platform.isIOS || Platform.isAndroid;

/// Formulaire générique (création / modification) d'une ressource rattachée à un véhicule.
class FormulaireEcran extends StatefulWidget {
  const FormulaireEcran({super.key, required this.ressource, required this.vehiculeId, this.element});

  final Ressource ressource;
  final String vehiculeId;
  final Map<String, dynamic>? element; // null : création

  @override
  State<FormulaireEcran> createState() => _FormulaireEcranState();
}

class _FormulaireEcranState extends State<FormulaireEcran> {
  final _cle = GlobalKey<FormState>();
  final Map<String, dynamic> _valeurs = {};
  final Map<String, TextEditingController> _textes = {};
  final Map<String, String> _fichiers = {}; // champ → chemin local choisi
  Map<String, String> _erreurs = {};
  bool _envoi = false;

  bool get _modification => widget.element != null;

  @override
  void initState() {
    super.initState();
    for (final c in widget.ressource.champs) {
      final existant = widget.element?[c.nom];
      if (c.estFichier) continue;
      if (c.type == TypeChamp.texte || c.type == TypeChamp.entier || c.type == TypeChamp.decimal) {
        _textes[c.nom] = TextEditingController(text: (existant ?? c.parDefaut ?? '').toString());
      } else if (c.type == TypeChamp.date) {
        _valeurs[c.nom] = existant ?? (c.obligatoire ? dateIso(DateTime.now()) : null);
      } else {
        _valeurs[c.nom] = existant ?? c.parDefaut;
      }
    }
  }

  @override
  void dispose() {
    for (final t in _textes.values) {
      t.dispose();
    }
    super.dispose();
  }

  // ------------------------------------------------------------------ Envoi
  Future<void> _enregistrer() async {
    if (!_cle.currentState!.validate()) return;
    final api = context.read<ApiClient>();
    final donnees = <String, dynamic>{'vehicule': widget.vehiculeId};
    for (final c in widget.ressource.champs) {
      if (c.estFichier) continue;
      if (_textes.containsKey(c.nom)) {
        final t = _textes[c.nom]!.text.trim().replaceAll(',', '.');
        donnees[c.nom] = t.isEmpty ? null : (c.type == TypeChamp.entier ? int.tryParse(t) : t);
        if (c.type == TypeChamp.texte && t.isEmpty) donnees[c.nom] = '';
      } else {
        donnees[c.nom] = _valeurs[c.nom];
      }
    }
    final chemin = _modification
        ? '${widget.ressource.chemin}/${widget.element!['id']}/'
        : '${widget.ressource.chemin}/';
    setState(() {
      _envoi = true;
      _erreurs = {};
    });
    try {
      if (_fichiers.isEmpty) {
        _modification ? await api.patch(chemin, donnees) : await api.post(chemin, donnees);
      } else {
        await api.envoyerAvecFichiers(
          _modification ? 'PATCH' : 'POST',
          chemin,
          donnees,
          [for (final e in _fichiers.entries) FichierEnvoi(e.key, e.value)],
        );
      }
      if (mounted) Navigator.pop(context, true);
    } on ApiException catch (e) {
      if (!mounted) return;
      setState(() => _erreurs = e.champs);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    } finally {
      if (mounted) setState(() => _envoi = false);
    }
  }

  Future<void> _supprimer() async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Supprimer ce ${widget.ressource.titreSingulier} ?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Annuler')),
          FilledButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Supprimer')),
        ],
      ),
    );
    if (ok != true || !mounted) return;
    try {
      await context.read<ApiClient>().delete('${widget.ressource.chemin}/${widget.element!['id']}/');
      if (mounted) Navigator.pop(context, true);
    } on ApiException catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    }
  }

  // ------------------------------------------------------------------ Fichiers
  Future<void> _choisirImage(Champ c, ImageSource source) async {
    final image = await ImagePicker().pickImage(source: source, maxWidth: 2000, imageQuality: 85);
    if (image != null) setState(() => _fichiers[c.nom] = image.path);
  }

  Future<void> _choisirFichier(Champ c) async {
    final resultat = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'jpg', 'jpeg', 'png', 'heic'],
    );
    final chemin = resultat?.files.single.path;
    if (chemin != null) setState(() => _fichiers[c.nom] = chemin);
  }

  // ------------------------------------------------------------------ Champs
  Widget _champ(Champ c) {
    final erreur = _erreurs[c.nom];
    final decoration = InputDecoration(
      labelText: c.libelle + (c.obligatoire ? ' *' : ''),
      suffixText: c.suffixe,
      helperText: c.aide,
      helperMaxLines: 2,
      errorText: erreur,
      border: const OutlineInputBorder(),
    );
    switch (c.type) {
      case TypeChamp.texte:
      case TypeChamp.entier:
      case TypeChamp.decimal:
        return TextFormField(
          controller: _textes[c.nom],
          decoration: decoration,
          keyboardType: c.type == TypeChamp.texte
              ? TextInputType.text
              : TextInputType.numberWithOptions(decimal: c.type == TypeChamp.decimal),
          validator: (v) => c.obligatoire && (v == null || v.trim().isEmpty) ? 'Champ obligatoire' : null,
        );
      case TypeChamp.date:
        final valeur = _valeurs[c.nom] as String?;
        return InkWell(
          onTap: () async {
            final choisie = await showDatePicker(
              context: context,
              initialDate: DateTime.tryParse(valeur ?? '') ?? DateTime.now(),
              firstDate: DateTime(1950),
              lastDate: DateTime(2100),
            );
            if (choisie != null) setState(() => _valeurs[c.nom] = dateIso(choisie));
          },
          child: InputDecorator(
            decoration: decoration.copyWith(
              suffixIcon: valeur != null && !c.obligatoire
                  ? IconButton(
                      icon: const Icon(Icons.clear),
                      onPressed: () => setState(() => _valeurs[c.nom] = null),
                    )
                  : const Icon(Icons.calendar_today),
            ),
            child: Text(valeur == null ? '—' : dateFr(valeur)),
          ),
        );
      case TypeChamp.booleen:
        return SwitchListTile(
          contentPadding: EdgeInsets.zero,
          title: Text(c.libelle),
          subtitle: c.aide == null ? null : Text(c.aide!),
          value: _valeurs[c.nom] == true,
          onChanged: (v) => setState(() => _valeurs[c.nom] = v),
        );
      case TypeChamp.choix:
        return DropdownButtonFormField<String>(
          initialValue: _valeurs[c.nom] as String?,
          isExpanded: true,
          decoration: decoration,
          items: [
            if (!c.obligatoire) const DropdownMenuItem(value: null, child: Text('—')),
            for (final e in c.choix.entries) DropdownMenuItem(value: e.key, child: Text(e.value)),
          ],
          onChanged: (v) => setState(() => _valeurs[c.nom] = v),
          validator: (v) => c.obligatoire && v == null ? 'Champ obligatoire' : null,
        );
      case TypeChamp.image:
      case TypeChamp.fichier:
        return _champFichier(c, erreur);
    }
  }

  Widget _champFichier(Champ c, String? erreur) {
    final local = _fichiers[c.nom];
    final distant = widget.element?[c.nom] as String?;
    final image = c.type == TypeChamp.image;
    return InputDecorator(
      decoration: InputDecoration(labelText: c.libelle, errorText: erreur, border: const OutlineInputBorder()),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (local != null)
            image
                ? ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.file(File(local), height: 160, fit: BoxFit.cover),
                  )
                : Text(local.split(Platform.pathSeparator).last)
          else if (distant != null)
            image ? ImageProtegee(url: distant, hauteur: 160) : OuvrirFichierBouton(url: distant),
          Wrap(
            spacing: 8,
            children: [
              if (image && estMobile)
                OutlinedButton.icon(
                  onPressed: () => _choisirImage(c, ImageSource.camera),
                  icon: const Icon(Icons.photo_camera),
                  label: const Text('Photo'),
                ),
              if (image)
                OutlinedButton.icon(
                  onPressed: () => _choisirImage(c, ImageSource.gallery),
                  icon: const Icon(Icons.photo_library),
                  label: Text(estMobile ? 'Galerie' : 'Choisir une image'),
                )
              else ...[
                if (estMobile)
                  OutlinedButton.icon(
                    onPressed: () => _choisirImage(c, ImageSource.camera),
                    icon: const Icon(Icons.document_scanner),
                    label: const Text('Photographier'),
                  ),
                OutlinedButton.icon(
                  onPressed: () => _choisirFichier(c),
                  icon: const Icon(Icons.attach_file),
                  label: const Text('Choisir un fichier'),
                ),
              ],
            ],
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final r = widget.ressource;
    return Scaffold(
      appBar: AppBar(
        title: Text(_modification ? 'Modifier le ${r.titreSingulier}' : 'Nouveau ${r.titreSingulier}'),
        actions: [
          if (_modification) IconButton(icon: const Icon(Icons.delete_outline), onPressed: _supprimer),
        ],
      ),
      body: Form(
        key: _cle,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            for (final c in r.champs) Padding(padding: const EdgeInsets.only(bottom: 14), child: _champ(c)),
            FilledButton.icon(
              onPressed: _envoi ? null : _enregistrer,
              icon: _envoi
                  ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2))
                  : const Icon(Icons.check),
              label: const Text('Enregistrer'),
            ),
          ],
        ),
      ),
    );
  }
}

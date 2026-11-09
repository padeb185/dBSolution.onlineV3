import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';

import '../api/api_client.dart';
import '../l10n/langue.dart';
import '../l10n/unites.dart';
import '../modeles/ressources.dart';
import '../modeles/tva.dart';
import '../widgets/champ_pays.dart';
import '../widgets/fichiers.dart';
import '../widgets/format.dart';

bool get estMobile => Platform.isIOS || Platform.isAndroid;

/// Formulaire générique (création / modification) d'une ressource rattachée à un véhicule.
class FormulaireEcran extends StatefulWidget {
  const FormulaireEcran({super.key, required this.ressource, required this.vehiculeId, this.element, this.vehicule});

  final Ressource ressource;
  final String vehiculeId;

  /// Véhicule (énergie : carburant proposé pour un nouveau plein)
  final Map<String, dynamic>? vehicule;
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

  /// Choix chargés depuis l'API (Champ.choixDistants) : champ → {code: libellé}
  final Map<String, Map<String, String>> _choixCharges = {};

  bool get _modification => widget.element != null;

  Future<void> _chargerChoix(Champ c) async {
    try {
      final r = await context.read<ApiClient>().get(c.choixDistants!);
      if (!mounted) return;
      setState(() => _choixCharges[c.nom] = {
            for (final e in r as List) '${(e as Map)['code']}': '${e['libelle']}',
          });
    } on ApiException catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
    }
  }

  /// Unités du véhicule (km / mi, L / gal) : conversion à l'affichage et à l'enregistrement
  Unites get _unites => Unites.de(widget.vehicule);

  bool _estDistance(Champ c) => c.suffixe == 'km';

  /// Carburant du plein (recharge : électricité, quantité en kWh, jamais convertie en gallons)
  String? get _carburant =>
      widget.ressource.chemin == 'recharges' ? 'electricite' : _valeurs['carburant'] as String?;

  /// Valeur du serveur (km, litres) → texte dans l'unité du véhicule
  String _texteInitial(Champ c, dynamic existant) {
    if (existant == null) return (c.parDefaut ?? '').toString();
    final v = enDouble(existant);
    if (v == null) return existant.toString();
    if (_estDistance(c) && _unites.miles) return _unites.depuisKm(v).round().toString();
    if (c.nom == 'quantite') {
      final q = _unites.depuisQuantite(v, widget.ressource.chemin == 'recharges' ? 'electricite' : widget.element?['carburant'] as String?);
      return q.toStringAsFixed(2).replaceFirst(RegExp(r'\.?0+$'), '');
    }
    return existant.toString();
  }

  @override
  void initState() {
    super.initState();
    for (final c in widget.ressource.champs) {
      final existant = widget.element?[c.nom];
      if (c.estFichier) continue;
      if (c.type == TypeChamp.texte || c.type == TypeChamp.entier || c.type == TypeChamp.decimal) {
        _textes[c.nom] = TextEditingController(text: _texteInitial(c, existant));
      } else if (c.type == TypeChamp.date) {
        _valeurs[c.nom] = existant ?? (c.obligatoire ? dateIso(DateTime.now()) : null);
      } else {
        _valeurs[c.nom] = existant ?? c.parDefaut;
      }
    }
    if (widget.ressource.champs.any((c) => c.nom == 'carburant') && _valeurs['carburant'] == null) {
      _valeurs['carburant'] = carburantParDefaut(widget.vehicule?['energie'] as String?);
    }
    // Plein : pays de la station (par défaut celui de la plaque) et taux de TVA de ce pays
    if (widget.ressource.champs.any((c) => c.nom == 'pays') && _valeurs['pays'] == null) {
      _valeurs['pays'] = (widget.vehicule?['pays_immatriculation'] as String?)?.toUpperCase() ?? 'BE';
    }
    final taux = _textes['taux_tva'];
    if (taux != null && taux.text.isEmpty && !_modification) _proposerTaux();
    for (final c in widget.ressource.champs) {
      if (c.choixDistants != null) _chargerChoix(c);
    }
  }

  /// Maintenance : pièces / main-d'œuvre TVAC et total (mis à jour pendant la saisie).
  Widget _totauxMaintenance() {
    final pieces = _textes['pieces_htva'], mo = _textes['main_oeuvre_htva'], taux = _textes['taux_tva'];
    if (pieces == null || mo == null || taux == null) return const SizedBox.shrink();
    return AnimatedBuilder(
      animation: Listenable.merge([pieces, mo, taux]),
      builder: (context, _) {
        double lire(TextEditingController c) => double.tryParse(c.text.trim().replaceAll(',', '.')) ?? 0;
        final k = 1 + lire(taux) / 100;
        final p = lire(pieces) * k, m = lire(mo) * k;
        return Padding(
          padding: const EdgeInsets.only(left: 12, top: 4),
          child: Text(
              t('Pièces TVAC {pieces} · main-d\'œuvre TVAC {mo} · total {total}',
                  {'pieces': euros(p), 'mo': euros(m), 'total': euros(p + m)}),
              style: Theme.of(context).textTheme.bodySmall),
        );
      },
    );
  }

  /// Taux de TVA du pays choisi (vide si le pays n'est pas dans la table : à saisir).
  void _proposerTaux() {
    final taux = tvaCarburant[_valeurs['pays']];
    _textes['taux_tva']?.text = taux == null ? '' : nombre(taux, decimales: taux % 1 == 0 ? 0 : 1).replaceAll(' ', '');
  }

  /// Ventilation du montant TVAC : HTVA et TVA (mise à jour pendant la saisie).
  Widget _ventilationTva() {
    final montant = _textes['montant'];
    final taux = _textes['taux_tva'];
    if (montant == null || taux == null) return const SizedBox.shrink();
    return AnimatedBuilder(
      animation: Listenable.merge([montant, taux]),
      builder: (context, _) {
        double? lire(TextEditingController c) => double.tryParse(c.text.trim().replaceAll(',', '.'));
        final v = ventilerTva(lire(montant), lire(taux));
        if (v == null) return const SizedBox.shrink();
        return Padding(
          padding: const EdgeInsets.only(left: 12, top: 4),
          child: Text(t('HTVA {htva} · TVA {tva}', {'htva': euros(v.$1), 'tva': euros(v.$2)}),
              style: Theme.of(context).textTheme.bodySmall),
        );
      },
    );
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
        // Saisie en miles / gallons : envoyée en km / litres
        final n = double.tryParse(t);
        if (n != null && _estDistance(c)) donnees[c.nom] = _unites.versKm(n).round();
        if (n != null && c.nom == 'quantite') {
          donnees[c.nom] = _unites.versQuantite(n, _carburant).toStringAsFixed(2);
        }
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
        title: Text(widget.ressource.texteSupprimer),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: Text(t('Annuler'))),
          FilledButton(onPressed: () => Navigator.pop(ctx, true), child: Text(t('Supprimer'))),
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
      // Quantité d'un plein : unité du carburant choisi (L, kWh, kg)
      suffixText: c.nom == 'quantite' && _valeurs.containsKey('carburant')
          ? _unites.symboleQuantite(_valeurs['carburant'] as String?)
          : (_estDistance(c) ? _unites.symboleDistance : c.suffixe),
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
          validator: (v) => c.obligatoire && (v == null || v.trim().isEmpty) ? t('Champ obligatoire') : null,
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
      case TypeChamp.choix when c.nom == 'pays':
        // Pays : saisie filtrée (« Lu » → Luxembourg)
        return ChampPays(
          valeur: _valeurs[c.nom] as String?,
          libelle: c.libelle + (c.obligatoire ? ' *' : ''),
          erreur: erreur,
          onChanged: (code) => setState(() {
            _valeurs[c.nom] = code;
            _proposerTaux();
          }),
        );
      case TypeChamp.choix:
        final options = c.choixDistants != null ? (_choixCharges[c.nom] ?? <String, String>{}) : c.choix;
        return DropdownButtonFormField<String>(
          // Choix distants : reconstruit une fois la liste chargée (la valeur doit exister dans la liste)
          key: c.choixDistants != null ? ValueKey('${c.nom}-${options.length}') : null,
          initialValue: options.containsKey(_valeurs[c.nom]) ? _valeurs[c.nom] as String? : null,
          isExpanded: true,
          decoration: decoration,
          menuMaxHeight: 420,
          items: [
            if (!c.obligatoire) const DropdownMenuItem(value: null, child: Text('—')),
            for (final e in options.entries)
              DropdownMenuItem(value: e.key, child: Text(e.value, overflow: TextOverflow.ellipsis)),
          ],
          onChanged: (v) => setState(() {
            _valeurs[c.nom] = v;
            if (c.nom == 'pays') _proposerTaux();
          }),
          validator: (v) => c.obligatoire && v == null ? t('Champ obligatoire') : null,
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
                  label: Text(t('Photo')),
                ),
              if (image)
                OutlinedButton.icon(
                  onPressed: () => _choisirImage(c, ImageSource.gallery),
                  icon: const Icon(Icons.photo_library),
                  label: Text(estMobile ? t('Galerie') : t('Choisir une image')),
                )
              else ...[
                if (estMobile)
                  OutlinedButton.icon(
                    onPressed: () => _choisirImage(c, ImageSource.camera),
                    icon: const Icon(Icons.document_scanner),
                    label: Text(t('Photographier')),
                  ),
                OutlinedButton.icon(
                  onPressed: () => _choisirFichier(c),
                  icon: const Icon(Icons.attach_file),
                  label: Text(t('Choisir un fichier')),
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
        title: Text(_modification ? r.titreModifier : r.titreNouveau),
        actions: [
          if (_modification) IconButton(icon: const Icon(Icons.delete_outline), onPressed: _supprimer),
        ],
      ),
      body: Form(
        key: _cle,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            for (final c in r.champs)
              Padding(
                padding: const EdgeInsets.only(bottom: 14),
                child: c.nom == 'taux_tva'
                    ? Column(crossAxisAlignment: CrossAxisAlignment.start,
                        children: [_champ(c), _ventilationTva(), _totauxMaintenance()])
                    : _champ(c),
              ),
            FilledButton.icon(
              onPressed: _envoi ? null : _enregistrer,
              icon: _envoi
                  ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2))
                  : const Icon(Icons.check),
              label: Text(t('Enregistrer')),
            ),
          ],
        ),
      ),
    );
  }
}

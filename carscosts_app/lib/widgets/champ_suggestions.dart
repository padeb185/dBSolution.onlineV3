import 'package:flutter/material.dart';

import '../l10n/langue.dart';

/// Champ texte libre avec suggestions sous le champ, filtrées pendant la saisie (marque, modèle…).
class ChampSuggestions extends StatefulWidget {
  const ChampSuggestions({
    super.key,
    required this.controleur,
    required this.libelle,
    required this.suggestions,
    this.obligatoire = false,
    this.erreur,
    this.onChoisi,
    this.icone,
  });

  final TextEditingController controleur;
  final String libelle;
  final List<String> Function(String saisie) suggestions;
  final bool obligatoire;
  final String? erreur;
  final ValueChanged<String>? onChoisi;

  /// Icône devant chaque suggestion et devant la saisie (ex. logo de la marque)
  final Widget? Function(String texte)? icone;

  @override
  State<ChampSuggestions> createState() => _ChampSuggestionsState();
}

class _ChampSuggestionsState extends State<ChampSuggestions> {
  final _focus = FocusNode();

  @override
  void dispose() {
    _focus.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return RawAutocomplete<String>(
      textEditingController: widget.controleur,
      focusNode: _focus,
      optionsBuilder: (v) {
        final liste = widget.suggestions(v.text);
        // Rien à proposer si la saisie correspond déjà exactement à la seule suggestion
        if (liste.length == 1 && liste.first == v.text) return const [];
        return liste;
      },
      onSelected: (choix) {
        widget.onChoisi?.call(choix);
        _focus.unfocus();
      },
      fieldViewBuilder: (context, controleur, focus, valider) => TextFormField(
        controller: controleur,
        focusNode: focus,
        textCapitalization: TextCapitalization.words,
        decoration: InputDecoration(
          prefixIcon: widget.icone == null
              ? null
              : ValueListenableBuilder<TextEditingValue>(
                  valueListenable: controleur,
                  builder: (context, v, _) =>
                      Padding(padding: const EdgeInsets.all(8), child: widget.icone!(v.text) ?? const SizedBox()),
                ),
          labelText: widget.libelle + (widget.obligatoire ? ' *' : ''),
          errorText: widget.erreur,
          border: const OutlineInputBorder(),
        ),
        validator: (v) => widget.obligatoire && (v == null || v.trim().isEmpty) ? t('Champ obligatoire') : null,
      ),
      optionsViewBuilder: (context, choisir, options) => Align(
        alignment: Alignment.topLeft,
        child: Material(
          elevation: 4,
          borderRadius: BorderRadius.circular(8),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxHeight: 280, maxWidth: 420),
            child: ListView.builder(
              padding: EdgeInsets.zero,
              shrinkWrap: true,
              itemCount: options.length,
              itemBuilder: (context, i) => ListTile(
                dense: true,
                leading: widget.icone?.call(options.elementAt(i)),
                title: Text(options.elementAt(i)),
                onTap: () => choisir(options.elementAt(i)),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

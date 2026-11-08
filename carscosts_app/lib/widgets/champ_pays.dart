import 'package:flutter/material.dart';

import '../l10n/langue.dart';
import '../modeles/pays.dart';

/// Texte sans accents ni majuscules (recherche : « lu » trouve « Luxembourg », « e » trouve « Érythrée »).
String normaliserRecherche(String texte) {
  const accents = {
    'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a', 'æ': 'ae', 'ç': 'c', 'è': 'e', 'é': 'e',
    'ê': 'e', 'ë': 'e', 'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'ñ': 'n', 'ò': 'o', 'ó': 'o', 'ô': 'o',
    'õ': 'o', 'ö': 'o', 'ø': 'o', 'œ': 'oe', 'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u', 'ý': 'y', 'ÿ': 'y',
    'ß': 'ss', 'ά': 'α', 'έ': 'ε', 'ή': 'η', 'ί': 'ι', 'ϊ': 'ι', 'ΐ': 'ι', 'ό': 'ο', 'ύ': 'υ', 'ϋ': 'υ',
    'ΰ': 'υ', 'ώ': 'ω', 'ς': 'σ', '’': "'",
  };
  final b = StringBuffer();
  for (final c in texte.toLowerCase().split('')) {
    b.write(accents[c] ?? c);
  }
  return b.toString().trim();
}

/// Pays dont le nom commence par le texte saisi (« L » → Laos, Lettonie, Liban… ; « Lu » → Luxembourg).
/// Le code ISO exact est aussi reconnu (« LU »). Sans résultat : pays dont le nom contient le texte.
List<String> rechercherPays(String saisie) {
  final q = normaliserRecherche(saisie);
  final pays = paysImmatriculation;
  if (q.isEmpty) return pays.keys.toList();
  final debut = [
    for (final e in pays.entries)
      if (normaliserRecherche(e.value).startsWith(q) || e.key.toLowerCase() == q) e.key,
  ];
  if (debut.isNotEmpty) return debut;
  return [for (final e in pays.entries) if (normaliserRecherche(e.value).contains(q)) e.key];
}

/// Champ « pays » à saisie filtrée : on tape les premières lettres et on choisit dans la liste.
class ChampPays extends StatefulWidget {
  const ChampPays({super.key, required this.valeur, required this.onChanged, required this.libelle, this.erreur});

  /// Code ISO (BE, LU…)
  final String? valeur;
  final ValueChanged<String> onChanged;
  final String libelle;
  final String? erreur;

  @override
  State<ChampPays> createState() => _ChampPaysState();
}

class _ChampPaysState extends State<ChampPays> {
  TextEditingController? _texte;
  FocusNode? _focus;

  String _nom(String? code) => code == null ? '' : (paysImmatriculation[code] ?? code);

  /// Entrée dans le champ : tout le texte est sélectionné (la saisie remplace le pays affiché) ;
  /// sortie sans choix valide : le pays enregistré est réaffiché.
  void _focusChange() {
    final texte = _texte, focus = _focus;
    if (texte == null || focus == null) return;
    if (focus.hasFocus) {
      texte.selection = TextSelection(baseOffset: 0, extentOffset: texte.text.length);
    } else if (!paysImmatriculation.values.contains(texte.text)) {
      texte.text = _nom(widget.valeur);
    }
  }

  @override
  void dispose() {
    _focus?.removeListener(_focusChange);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Autocomplete<String>(
      initialValue: TextEditingValue(text: _nom(widget.valeur)),
      optionsBuilder: (v) => rechercherPays(v.text == _nom(widget.valeur) ? '' : v.text),
      displayStringForOption: _nom,
      onSelected: (code) {
        widget.onChanged(code);
        FocusScope.of(context).unfocus();
      },
      optionsViewBuilder: (context, choisir, options) => Align(
        alignment: Alignment.topLeft,
        child: Material(
          elevation: 4,
          borderRadius: BorderRadius.circular(8),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxHeight: 300, maxWidth: 420),
            child: ListView.builder(
              padding: EdgeInsets.zero,
              shrinkWrap: true,
              itemCount: options.length,
              itemBuilder: (context, i) {
                final code = options.elementAt(i);
                return ListTile(
                  dense: true,
                  title: Text(_nom(code)),
                  trailing: Text(code, style: Theme.of(context).textTheme.bodySmall),
                  selected: code == widget.valeur,
                  onTap: () => choisir(code),
                );
              },
            ),
          ),
        ),
      ),
      fieldViewBuilder: (context, texte, focus, valider) {
        if (_focus != focus) {
          _focus?.removeListener(_focusChange);
          focus.addListener(_focusChange);
        }
        _texte = texte;
        _focus = focus;
        return TextFormField(
          controller: texte,
          focusNode: focus,
          textCapitalization: TextCapitalization.words,
          decoration: InputDecoration(
            labelText: widget.libelle,
            hintText: t('Tapez les premières lettres'),
            errorText: widget.erreur,
            border: const OutlineInputBorder(),
            suffixIcon: const Icon(Icons.arrow_drop_down),
          ),
          onFieldSubmitted: (_) {
            // Entrée : premier pays de la liste filtrée
            final trouves = rechercherPays(texte.text);
            if (trouves.isNotEmpty) {
              texte.text = _nom(trouves.first);
              widget.onChanged(trouves.first);
            }
          },
          validator: (v) => paysImmatriculation.values.contains(v) ? null : t('Choisissez un pays dans la liste'),
        );
      },
    );
  }
}

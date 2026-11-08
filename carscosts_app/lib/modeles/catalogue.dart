import '../api/api_client.dart';
import '../widgets/champ_pays.dart' show normaliserRecherche;

/// Version d'un modèle : libellé, puissance (ch) et énergie (codes de l'API : essence, diesel, phev…).
class Motorisation {
  const Motorisation(this.version, this.ch, this.energie);

  final String version;
  final int? ch;
  final String? energie;

  /// Libellé de la suggestion : « 1.2 PureTech · 100 ch »
  String get libelle => ch == null ? version : '$version · $ch ch';
}

/// Marques, modèles et versions proposés à la saisie d'un véhicule (fichier du serveur, API catalogue/).
/// Téléchargé une fois par session ; la saisie reste libre (suggestions seulement).
class Catalogue {
  /// marque → modèle → versions
  static Map<String, Map<String, List<Motorisation>>> marques = {};
  static Future<void>? _chargement;

  static Future<void> charger(ApiClient api) => _chargement ??= () async {
        try {
          final r = Map<String, dynamic>.from(await api.get('catalogue/') as Map);
          marques = lire(Map<String, dynamic>.from(r['marques'] as Map));
        } catch (_) {
          _chargement = null; // nouvel essai à la prochaine ouverture du formulaire
        }
      }();

  /// Format 2 : {"Peugeot": {"208": [["1.2 PureTech", 100, "essence"], …]}} ; format 1 : {"Peugeot": ["208", …]}
  static Map<String, Map<String, List<Motorisation>>> lire(Map<String, dynamic> brut) => {
        for (final m in brut.entries)
          m.key: m.value is Map
              ? {
                  for (final mo in (m.value as Map).entries)
                    mo.key.toString(): [
                      for (final v in mo.value as List)
                        if (v is List && v.isNotEmpty)
                          Motorisation(v[0].toString(), v.length > 1 ? (v[1] as num?)?.toInt() : null,
                              v.length > 2 ? v[2]?.toString() : null),
                    ],
                }
              : {for (final mo in m.value as List) mo.toString(): const <Motorisation>[]},
      };

  /// Le texte commence par la saisie, ou l'un de ses mots (« glc » → « Classe GLC »)
  static bool correspond(String texte, String saisie) {
    final q = normaliserRecherche(saisie);
    if (q.isEmpty) return true;
    final t = normaliserRecherche(texte);
    return t.startsWith(q) || t.split(RegExp(r'[\s\-]+')).any((mot) => mot.startsWith(q));
  }

  static List<String> suggestionsMarques(String saisie) =>
      [for (final m in marques.keys) if (correspond(m, saisie)) m];

  static Map<String, List<Motorisation>> _modelesDe(String marque) {
    final cle = normaliserRecherche(marque);
    return marques.entries.where((e) => normaliserRecherche(e.key) == cle).firstOrNull?.value ?? const {};
  }

  /// Modèles de la marque saisie (sans tenir compte des majuscules ni des accents)
  static List<String> suggestionsModeles(String marque, String saisie) =>
      [for (final m in _modelesDe(marque).keys) if (correspond(m, saisie)) m];

  /// Versions (motorisations) du modèle saisi
  static List<Motorisation> motorisations(String marque, String modele) {
    final cle = normaliserRecherche(modele);
    return _modelesDe(marque).entries.where((e) => normaliserRecherche(e.key) == cle).firstOrNull?.value ??
        const [];
  }

  /// Versions dont le libellé (ou la puissance) correspond à la saisie
  static List<Motorisation> suggestionsVersions(String marque, String modele, String saisie) =>
      [for (final v in motorisations(marque, modele)) if (correspond(v.libelle, saisie) || '${v.ch}'.startsWith(saisie.trim())) v];
}

import '../api/api_client.dart';
import '../widgets/champ_pays.dart' show normaliserRecherche;

/// Marques et modèles proposés à la saisie d'un véhicule (fichier du serveur, API catalogue/).
/// Téléchargé une fois par session ; la saisie reste libre (suggestions seulement).
class Catalogue {
  static Map<String, List<String>> marques = {};
  static Future<void>? _chargement;

  static Future<void> charger(ApiClient api) => _chargement ??= () async {
        try {
          final r = Map<String, dynamic>.from(await api.get('catalogue/') as Map);
          marques = {
            for (final e in Map<String, dynamic>.from(r['marques'] as Map).entries)
              e.key: [for (final m in e.value as List) m.toString()],
          };
        } catch (_) {
          _chargement = null; // nouvel essai à la prochaine ouverture du formulaire
        }
      }();

  /// Le texte commence par la saisie, ou l'un de ses mots (« glc » → « Classe GLC »)
  static bool correspond(String texte, String saisie) {
    final q = normaliserRecherche(saisie);
    if (q.isEmpty) return true;
    final t = normaliserRecherche(texte);
    return t.startsWith(q) || t.split(RegExp(r'[\s\-]+')).any((mot) => mot.startsWith(q));
  }

  static List<String> suggestionsMarques(String saisie) =>
      [for (final m in marques.keys) if (correspond(m, saisie)) m];

  /// Modèles de la marque saisie (sans tenir compte des majuscules ni des accents)
  static List<String> suggestionsModeles(String marque, String saisie) {
    final cle = normaliserRecherche(marque);
    final modeles = marques.entries.where((e) => normaliserRecherche(e.key) == cle).firstOrNull?.value ?? const [];
    return [for (final m in modeles) if (correspond(m, saisie)) m];
  }
}

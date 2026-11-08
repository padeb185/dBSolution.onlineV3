import '../api/api_client.dart';
import '../widgets/champ_pays.dart' show normaliserRecherche;

/// Version d'un modèle : libellé, puissance (ch) et énergie (codes de l'API : essence, diesel, phev…).
class Motorisation {
  const Motorisation(this.version, this.ch, this.energie, [this.periode]);

  final String version;
  final int? ch;
  final String? energie;

  /// Années de production : « 1976-1983 », « 2019- » (facultatif)
  final String? periode;

  /// Libellé de la suggestion : « 1.6 GTI · 110 ch · 1976–1983 »
  String get libelle => [
        version,
        if (ch != null) '$ch ch',
        if (periode != null && periode!.isNotEmpty) periode!.replaceAll('-', '–'),
      ].join(' · ');

  /// Version produite l'année donnée (sans période connue : toujours vrai)
  bool produiteEn(int annee) {
    final p = periode;
    if (p == null || p.isEmpty) return true;
    final m = RegExp(r'^(\d{4})(?:-(\d{4})?)?$').firstMatch(p);
    if (m == null) return true;
    final debut = int.parse(m.group(1)!);
    final fin = m.group(2) == null ? (p.contains('-') ? 9999 : debut) : int.parse(m.group(2)!);
    return annee >= debut && annee <= fin;
  }
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
                              v.length > 2 ? v[2]?.toString() : null, v.length > 3 ? v[3]?.toString() : null),
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

  /// Versions dont le libellé (ou la puissance) correspond à la saisie ;
  /// année du modèle connue : versions produites cette année-là (toutes si aucune ne correspond).
  static List<Motorisation> suggestionsVersions(String marque, String modele, String saisie, {int? annee}) {
    final liste = [
      for (final v in motorisations(marque, modele))
        if (correspond(v.libelle, saisie) || '${v.ch}'.startsWith(saisie.trim())) v,
    ];
    if (annee == null) return liste;
    final deLAnnee = liste.where((v) => v.produiteEn(annee)).toList();
    return deLAnnee.isEmpty ? liste : deLAnnee;
  }
}

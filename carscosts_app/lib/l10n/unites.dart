/// Unités d'affichage et de saisie : kilomètres ou miles, litres ou gallons (US / impériaux).
///
/// Le serveur enregistre toujours en km et en litres : l'application convertit à l'affichage
/// et à la saisie. Unités du compte (réglages, proposées selon le pays à l'inscription),
/// remplaçables par véhicule (ex. voiture importée des États-Unis, compteur en miles).
class Unites {
  const Unites(this.distance, this.volume);

  /// 'km' ou 'mi'
  final String distance;

  /// 'L', 'gal_us' ou 'gal_uk'
  final String volume;

  /// Unités du compte (réglages)
  static Unites compte = const Unites('km', 'L');

  /// Unités d'un véhicule : les siennes si elles sont renseignées, sinon celles du compte.
  static Unites de(Map? vehicule) {
    final d = vehicule?['unite_distance'];
    final v = vehicule?['unite_volume'];
    return Unites(
      d is String && d.isNotEmpty ? d : compte.distance,
      v is String && v.isNotEmpty ? v : compte.volume,
    );
  }

  static const kmParMile = 1.609344;
  static const litresParGallonUs = 3.785411784;
  static const litresParGallonUk = 4.54609;

  bool get miles => distance == 'mi';
  String get symboleDistance => miles ? 'mi' : 'km';
  double get _kmParUnite => miles ? kmParMile : 1;

  /// km (serveur) → unité affichée
  double depuisKm(num km) => km / _kmParUnite;

  /// unité saisie → km (serveur)
  double versKm(num valeur) => valeur * _kmParUnite;

  double get _litresParUnite => switch (volume) {
        'gal_us' => litresParGallonUs,
        'gal_uk' => litresParGallonUk,
        _ => 1,
      };
  String get symboleVolume => switch (volume) {
        'gal_us' => 'gal',
        'gal_uk' => 'gal UK',
        _ => 'L',
      };

  /// Unité de la quantité d'un plein : volume (liquides), kWh (électricité) ou kg (GNC).
  String symboleQuantite(String? carburant) {
    final u = uniteCarburant(carburant);
    return u == 'L' ? symboleVolume : u;
  }

  bool _liquide(String? carburant) => uniteCarburant(carburant) == 'L';

  /// litres (serveur) → unité affichée (kWh et kg inchangés)
  double depuisQuantite(num q, String? carburant) => _liquide(carburant) ? q / _litresParUnite : q.toDouble();

  /// unité saisie → litres (serveur)
  double versQuantite(num q, String? carburant) => _liquide(carburant) ? q * _litresParUnite : q.toDouble();

  /// prix par litre (serveur) → prix par unité affichée
  double prixParQuantite(num prix, String? carburant) => _liquide(carburant) ? prix * _litresParUnite : prix.toDouble();

  /// coût par km (serveur) → coût par km ou par mile
  double coutParDistance(num coutKm) => coutKm * _kmParUnite;

  /// Consommation (serveur : quantité / 100 km, unité L, kWh ou kg) → valeur et unité affichées.
  /// Miles + carburant liquide : mpg (gallons US si le volume est en gallons US, sinon impériaux).
  (double, String) consommation(num par100km, String uniteServeur) {
    if (uniteServeur == 'L') {
      if (miles) {
        return volume == 'gal_us' ? (235.214583 / par100km, 'mpg') : (282.480936 / par100km, 'mpg UK');
      }
      return (par100km / _litresParUnite, '$symboleVolume/100 km');
    }
    return miles ? (par100km * kmParMile, '$uniteServeur/100 mi') : (par100km.toDouble(), '$uniteServeur/100 km');
  }
}

/// Unité serveur de la quantité d'un plein selon le carburant.
String uniteCarburant(String? carburant) => switch (carburant) {
      'electricite' => 'kWh',
      'gnc' => 'kg',
      _ => 'L',
    };

/// Unités proposées selon le pays (mêmes règles que le serveur, particulier/models.py).
/// États-Unis : miles et gallons US ; Royaume-Uni : miles et litres (consommation en mpg UK).
Unites unitesParDefaut(String? pays) {
  const miles = {'US', 'GB', 'LR', 'MM', 'PR', 'GU', 'VI', 'AS', 'MP', 'UM'};
  const gallonsUs = {'US', 'LR', 'PR', 'GU', 'VI', 'AS', 'MP', 'UM'};
  final p = (pays ?? '').toUpperCase();
  return Unites(miles.contains(p) ? 'mi' : 'km', gallonsUs.contains(p) ? 'gal_us' : 'L');
}

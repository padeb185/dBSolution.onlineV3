/// Taux de TVA (taux normal, %) du carburant et de la recharge par pays de la station.
/// Mêmes taux que le serveur (particulier/tva.py). Pays absent : taux à saisir.
const tvaCarburant = <String, double>{
  'AT': 20, 'BE': 21, 'BG': 20, 'HR': 25, 'CY': 19, 'CZ': 21, 'DK': 25, 'EE': 24, 'FI': 25.5,
  'FR': 20, 'DE': 19, 'GR': 24, 'HU': 27, 'IE': 23, 'IT': 22, 'LV': 21, 'LT': 21, 'LU': 17,
  'MT': 18, 'NL': 21, 'PL': 23, 'PT': 23, 'RO': 21, 'SK': 23, 'SI': 22, 'ES': 21, 'SE': 25,
  'GB': 20, 'CH': 8.1, 'NO': 25,
};

/// Montant TVAC → (HTVA, TVA), arrondis au cent ; null si un des deux est inconnu.
(double, double)? ventilerTva(double? montantTtc, double? taux) {
  if (montantTtc == null || taux == null) return null;
  final htva = (montantTtc / (1 + taux / 100) * 100).roundToDouble() / 100;
  return (htva, ((montantTtc - htva) * 100).roundToDouble() / 100);
}

import 'package:carscosts_app/l10n/unites.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  tearDown(() => Unites.compte = const Unites('km', 'L'));

  test('Unités proposées selon le pays', () {
    expect(unitesParDefaut('US').distance, 'mi');
    expect(unitesParDefaut('US').volume, 'gal_us');
    expect(unitesParDefaut('GB').distance, 'mi');
    expect(unitesParDefaut('GB').volume, 'L');
    expect(unitesParDefaut('LU').distance, 'km');
  });

  test('Conversions miles / gallons (serveur en km et litres)', () {
    const us = Unites('mi', 'gal_us');
    expect(us.depuisKm(160.9344), closeTo(100, 1e-9));
    expect(us.versKm(100), closeTo(160.9344, 1e-9));
    expect(us.depuisQuantite(37.85411784, 'sp95'), closeTo(10, 1e-9));
    expect(us.depuisQuantite(50, 'electricite'), 50); // kWh inchangés
    final (mpg, unite) = us.consommation(7.84, 'L'); // 7,84 L/100 km ≈ 30 mpg US
    expect(mpg, closeTo(30, 0.01));
    expect(unite, 'mpg');
  });

  test('Unités du véhicule prioritaires sur celles du compte', () {
    Unites.compte = const Unites('km', 'L');
    expect(Unites.de({'unite_distance': 'mi', 'unite_volume': ''}).distance, 'mi');
    expect(Unites.de({'unite_distance': '', 'unite_volume': ''}).distance, 'km');
    expect(Unites.de(null).volume, 'L');
  });
}

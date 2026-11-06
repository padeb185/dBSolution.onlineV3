import 'package:carscosts_app/ecrans/vin_ecran.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('extrait un VIN d\'un texte OCR et corrige O / I', () {
    expect(extraireVin('E  WP0ZZZ98ZKK123456\nautre texte'), 'WP0ZZZ98ZKK123456');
    expect(extraireVin('VIN: WPOZZZ98ZKK123456'), 'WP0ZZZ98ZKK123456');
    expect(extraireVin('pas de vin ici'), isNull);
  });

  test('clé de contrôle ISO 3779', () {
    expect(cleVinValide('1M8GDM9AXKP042788'), isTrue);
    expect(cleVinValide('1M8GDM9A1KP042788'), isFalse);
  });
}

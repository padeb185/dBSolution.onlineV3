import 'package:intl/intl.dart';

final _euros = NumberFormat.currency(locale: 'fr_BE', symbol: '€', decimalDigits: 2);
final _nombre = NumberFormat.decimalPattern('fr_BE');
final _date = DateFormat('dd/MM/yyyy', 'fr_BE');

double? enDouble(dynamic v) => v == null ? null : (v is num ? v.toDouble() : double.tryParse(v.toString()));

String euros(dynamic v) => v == null ? '—' : _euros.format(enDouble(v) ?? 0);

String km(dynamic v) => v == null ? '—' : '${_nombre.format(enDouble(v) ?? 0)} km';

String nombre(dynamic v, {int decimales = 2}) =>
    v == null ? '—' : NumberFormat.decimalPatternDigits(locale: 'fr_BE', decimalDigits: decimales).format(enDouble(v) ?? 0);

/// "2026-11-06" → "06/11/2026"
String dateFr(dynamic iso) {
  if (iso == null || iso.toString().isEmpty) return '—';
  final d = DateTime.tryParse(iso.toString());
  return d == null ? iso.toString() : _date.format(d);
}

/// DateTime → "2026-11-06" (format de l'API)
String dateIso(DateTime d) => DateFormat('yyyy-MM-dd').format(d);

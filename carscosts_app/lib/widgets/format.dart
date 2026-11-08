import 'package:intl/intl.dart';

import '../l10n/langue.dart';
import '../l10n/unites.dart';

double? enDouble(dynamic v) => v == null ? null : (v is num ? v.toDouble() : double.tryParse(v.toString()));

/// Formats selon la langue choisie (montants en €, kilomètres, dates).
String euros(dynamic v) =>
    v == null ? '—' : NumberFormat.currency(locale: localeIntl, symbol: '€', decimalDigits: 2).format(enDouble(v) ?? 0);

/// Distance (serveur : km) dans l'unité du véhicule ou du compte : « 12 345 km » / « 7 671 mi ».
String km(dynamic v, [Unites? unites]) {
  if (v == null) return '—';
  final u = unites ?? Unites.compte;
  return '${NumberFormat.decimalPatternDigits(locale: localeIntl, decimalDigits: 0).format(u.depuisKm(enDouble(v) ?? 0))} '
      '${u.symboleDistance}';
}

String nombre(dynamic v, {int decimales = 2}) => v == null
    ? '—'
    : NumberFormat.decimalPatternDigits(locale: localeIntl, decimalDigits: decimales).format(enDouble(v) ?? 0);

/// "2026-11-06" → date courte de la langue (06/11/2026, 06.11.2026…)
String dateFr(dynamic iso) {
  if (iso == null || iso.toString().isEmpty) return '—';
  final d = DateTime.tryParse(iso.toString());
  return d == null ? iso.toString() : DateFormat.yMd(localeIntl).format(d.toLocal());
}

/// DateTime → "2026-11-06" (format de l'API)
String dateIso(DateTime d) => DateFormat('yyyy-MM-dd').format(d);

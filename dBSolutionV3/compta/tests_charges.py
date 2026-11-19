"""Tests : ventilation du chiffre d'affaires et échéances des primes d'assurance."""
from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from django.test import SimpleTestCase


def _facture(total, lignes):
    return SimpleNamespace(total_ht=Decimal(total), lines=SimpleNamespace(
        all=lambda: [SimpleNamespace(type_ligne=t, total_ht=Decimal(m)) for t, m in lignes]))


class VentilationVentesTests(SimpleTestCase):
    def test_types_de_lignes(self):
        from .journal import ventilation_ventes
        v = ventilation_ventes(_facture("300.00", [("PIECE", "100"), ("MAIN_OEUVRE", "150"), ("LOCATION", "50")]))
        self.assertEqual([(c, m) for c, _i, m in v],
                         [("700100", Decimal("100.00")), ("700200", Decimal("150.00")), ("700300", Decimal("50.00"))])

    def test_quote_part_et_arrondi(self):
        from .journal import ventilation_ventes
        v = ventilation_ventes(_facture("100.00", [("PIECE", "100"), ("MAIN_OEUVRE", "100"), ("AUTRE", "100")]))
        self.assertEqual(sum(m for _c, _i, m in v), Decimal("100.00"))

    def test_sans_ligne(self):
        from .journal import ventilation_ventes
        self.assertEqual(ventilation_ventes(_facture("80.00", []))[0][0], "700000")


class EcheancesAssuranceTests(SimpleTestCase):
    def _police(self, **kw):
        base = dict(date_debut=date(2026, 1, 31), date_fin=None, frequence_paiement="mensuel",
                    prime_mensuelle=Decimal("50"), prime_annuelle=None, actif=True, updated_at=None)
        base.update(kw)
        return SimpleNamespace(**base)

    def test_mensuel(self):
        from .charges_vehicules import echeances_police
        e = echeances_police(self._police(), date(2026, 4, 15))
        self.assertEqual([d for d, _m in e], [date(2026, 1, 31), date(2026, 2, 28), date(2026, 3, 31)])

    def test_annuel_et_date_de_fin(self):
        from .charges_vehicules import echeances_police
        p = self._police(frequence_paiement="annuel", prime_mensuelle=None, prime_annuelle=Decimal("900"),
                         date_debut=date(2024, 3, 1), date_fin=date(2026, 2, 28))
        self.assertEqual(echeances_police(p, date(2026, 12, 31)),
                         [(date(2024, 3, 1), Decimal("900.00")), (date(2025, 3, 1), Decimal("900.00"))])

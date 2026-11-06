from datetime import date
from types import SimpleNamespace

from django.test import SimpleTestCase

from . import calculs


class CalculsTests(SimpleTestCase):
    def test_ajouter_mois(self):
        self.assertEqual(calculs.ajouter_mois(date(2026, 1, 31), 1), date(2026, 2, 28))
        self.assertEqual(calculs.ajouter_mois(date(2026, 11, 15), 12), date(2027, 11, 15))

    def test_statut_rappel(self):
        r = SimpleNamespace(actif=True, echeance_date=date(2026, 6, 1), echeance_km=None)
        self.assertEqual(calculs.statut_rappel(r, 0, date(2026, 6, 2))["statut"], "en_retard")
        self.assertEqual(calculs.statut_rappel(r, 0, date(2026, 5, 15))["statut"], "proche")
        self.assertEqual(calculs.statut_rappel(r, 0, date(2026, 1, 1))["statut"], "a_venir")
        r = SimpleNamespace(actif=True, echeance_date=None, echeance_km=50000)
        self.assertEqual(calculs.statut_rappel(r, 49500)["statut"], "proche")
        self.assertEqual(calculs.statut_rappel(r, 50001)["statut"], "en_retard")

    def test_mois_entre(self):
        self.assertEqual(calculs.mois_entre(date(2024, 3, 15), date(2026, 3, 14)), 23)

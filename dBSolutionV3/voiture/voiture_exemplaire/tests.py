from django.test import TestCase

# Create your tests here.


from decimal import Decimal as _D

from django.test import SimpleTestCase as _SimpleTestCase


class RapportVoituresTests(_SimpleTestCase):
    """Rapport des voitures (Direction) : parts des camemberts."""

    def test_parts_ignore_les_valeurs_nulles(self):
        from .rapport import _parts
        self.assertEqual(_parts([("A", _D("10")), ("B", _D("0")), ("C", None)]), [{"label": "A", "valeur": 10.0}])

    def test_top_regroupe_au_dela_de_sept_vehicules(self):
        from .rapport import TOP_VEHICULES, _top
        items = [{"label": f"V{i}", "total": _D(i)} for i in range(1, 11)]
        parts = _top(items, "total", "label")
        self.assertEqual(len(parts), TOP_VEHICULES + 1)
        self.assertEqual(parts[0]["label"], "V10")
        self.assertEqual(parts[-1]["valeur"], 1.0 + 2.0 + 3.0)

    def test_url(self):
        from django.urls import reverse
        self.assertTrue(reverse("voiture_exemplaire:rapport_voitures").endswith("/rapport/"))

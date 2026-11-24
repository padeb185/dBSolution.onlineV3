from django.test import TestCase

# Create your tests here.


from django.test import SimpleTestCase as _SimpleTestCase


class ArborescenceModelesTests(_SimpleTestCase):
    def test_production(self):
        from .arborescence import production
        self.assertEqual(production(3, 2019, 12, 2023), "03/2019 → 12/2023")
        self.assertTrue(production(9, 2024, None, None).startswith("09/2024 → "))
        self.assertEqual(production(None, None, None, None), "—")
        self.assertEqual(production(None, 2019, None, 2023), "2019 → 2023")

    def test_lien_autoscout(self):
        from .arborescence import lien_autoscout
        self.assertEqual(lien_autoscout("Porsche", "911"), "https://www.autoscout24.be/fr/lst/porsche/911")
        self.assertEqual(lien_autoscout("Mercedes-Benz", "Classe C"), "https://www.autoscout24.be/fr/lst/mercedes-benz/classe-c")

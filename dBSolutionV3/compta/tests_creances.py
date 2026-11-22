from django.test import SimpleTestCase


class CreancesClientsTests(SimpleTestCase):
    """Créances clients : tranches d'ancienneté et source « locations à facturer » du journal."""

    def test_tranches(self):
        from .creances import tranche
        self.assertEqual(tranche(-5), "non_echu")
        self.assertEqual(tranche(0), "non_echu")
        self.assertEqual(tranche(1), "j30")
        self.assertEqual(tranche(30), "j30")
        self.assertEqual(tranche(31), "j60")
        self.assertEqual(tranche(90), "j90")
        self.assertEqual(tranche(91), "plus90")

    def test_source_journal(self):
        from .journal import SOURCES
        self.assertIn("a_facturer", SOURCES)

    def test_compte_produits_a_recevoir_au_bilan(self):
        # 404000 au débit : créances commerciales (actif)
        from decimal import Decimal
        from .bilan import rubrique_bilan
        self.assertEqual(rubrique_bilan("404000", Decimal("100")), ("A", "creances_commerciales"))

    def test_correspondance_skr03(self):
        from .plans_comptables import SKR03
        self.assertIn("404000", SKR03)

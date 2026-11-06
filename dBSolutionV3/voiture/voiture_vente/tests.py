from datetime import date
from decimal import Decimal as D
from types import SimpleNamespace

from django.test import SimpleTestCase

from . import calculs


class CalculPrixTests(SimpleTestCase):
    def test_regime_normal_htva(self):
        p = calculs.calculer_prix("NORMAL", D("10000"), False, D("21"))
        self.assertEqual((p["htva"], p["tva"], p["tvac"]), (D("10000.00"), D("2100.00"), D("12100.00")))

    def test_regime_normal_tvac(self):
        p = calculs.calculer_prix("NORMAL", D("12100"), True, D("21"))
        self.assertEqual((p["htva"], p["tva"], p["tvac"]), (D("10000.00"), D("2100.00"), D("12100.00")))

    def test_regime_normal_base_limitee_50(self):
        # Tolérance belge : base imposable limitée au pourcentage de déduction (50 %)
        p = calculs.calculer_prix("NORMAL", D("10000"), False, D("21"), D("50"))
        self.assertEqual((p["base_tva"], p["tva"], p["tvac"]), (D("5000.00"), D("1050.00"), D("11050.00")))

    def test_regime_marge(self):
        p = calculs.calculer_prix("MARGE", D("15000"), False, D("21"), prix_achat_marge=D("12000"))
        self.assertEqual(p["marge"], D("3000.00"))
        self.assertEqual(p["tva"], D("520.66"))          # 3000 × 21 / 121
        self.assertEqual(p["htva"], D("14479.34"))
        self.assertEqual(p["tvac"], D("15000.00"))

    def test_regime_marge_negative(self):
        p = calculs.calculer_prix("MARGE", D("9000"), False, D("21"), prix_achat_marge=D("12000"))
        self.assertEqual((p["tva"], p["htva"], p["base_tva"]), (D("0.00"), D("9000.00"), D("0.00")))

    def test_exoneres(self):
        for regime in ("INTRACOM", "EXPORT", "EXONERE"):
            p = calculs.calculer_prix(regime, D("8000"), True, D("21"))
            self.assertEqual((p["htva"], p["tva"], p["tvac"]), (D("8000.00"), D("0.00"), D("8000.00")))


class MentionsTests(SimpleTestCase):
    def test_mentions_par_pays(self):
        self.assertIn("39bis", str(calculs.mention_legale("INTRACOM", "BE")))
        self.assertIn("25a", str(calculs.mention_legale("MARGE", "DE")))
        self.assertIn("2006/112", str(calculs.mention_legale("EXPORT", "IT")))
        self.assertEqual(calculs.mention_legale("NORMAL", "BE"), "")


class OutilsTests(SimpleTestCase):
    def test_mois_entre(self):
        self.assertEqual(calculs.mois_entre(date(2024, 3, 15), date(2026, 3, 14)), 23)
        self.assertEqual(calculs.mois_entre(date(2024, 3, 15), date(2026, 3, 15)), 24)

    def test_revision_tva(self):
        immo = SimpleNamespace(tva_recuperable=D("4200"), tva_deductible=D("100"), date_acquisition=date(2024, 5, 1))
        vente = SimpleNamespace(regime_tva="EXONERE", immobilisation=immo, exemplaire=None, exemplaire_id=None,
                                date_vente=date(2026, 6, 1))
        r = calculs.revision_tva(vente, "BE")
        # Période 2024–2028 : vente en 2026 → 2027 et 2028 restent (2/5)
        self.assertEqual((r["annees_restantes"], r["montant"]), (2, D("1680.00")))
        vente.regime_tva = "NORMAL"
        self.assertIsNone(calculs.revision_tva(vente, "BE"))

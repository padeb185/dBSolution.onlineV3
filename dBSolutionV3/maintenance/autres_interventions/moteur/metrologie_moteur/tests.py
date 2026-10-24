from decimal import Decimal

from django.test import SimpleTestCase

from .models import calcul_cylindree


class CalculCylindreeTests(SimpleTestCase):
    def test_cylindree_depuis_alesage_et_course(self):
        # 4 cylindres, 82,50 × 92,80 mm → 1984,4 cm³ (moteur 2.0 l)
        _, _, cyl = calcul_cylindree(Decimal("82.50"), Decimal("92.80"), None, 4)
        self.assertEqual(cyl, Decimal("1984.3"))

    def test_course_depuis_cylindree(self):
        d, c, _ = calcul_cylindree(Decimal("82.50"), None, Decimal("1984.3"), 4)
        self.assertEqual(c, Decimal("92.80"))

    def test_alesage_depuis_cylindree(self):
        d, c, _ = calcul_cylindree(None, Decimal("92.80"), Decimal("1984.3"), 4)
        self.assertEqual(d, Decimal("82.50"))

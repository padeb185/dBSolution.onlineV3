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


class NombrePaliersTests(SimpleTestCase):
    """Manetons / tourillons selon l'architecture."""

    def test_en_ligne_et_a_plat(self):
        from .models import ArchitectureMoteur, nombre_paliers
        self.assertEqual(nombre_paliers(ArchitectureMoteur.EN_LIGNE, 4), (4, 5))
        self.assertEqual(nombre_paliers(ArchitectureMoteur.EN_LIGNE, 6), (6, 7))
        self.assertEqual(nombre_paliers(ArchitectureMoteur.PLAT, 4), (4, 5))
        self.assertEqual(nombre_paliers(ArchitectureMoteur.PLAT, 6), (6, 7))

    def test_en_v_et_en_w(self):
        from .models import ArchitectureMoteur, nombre_paliers
        self.assertEqual(nombre_paliers(ArchitectureMoteur.V, 6), (3, 4))
        self.assertEqual(nombre_paliers(ArchitectureMoteur.V, 8), (4, 5))
        self.assertEqual(nombre_paliers(ArchitectureMoteur.V, 12), (6, 7))
        self.assertEqual(nombre_paliers(ArchitectureMoteur.W, 12), (6, 7))
        self.assertEqual(nombre_paliers(ArchitectureMoteur.W, 16), (8, 9))

    def test_cylindres_du_maneton(self):
        from .models import ArchitectureMoteur, cylindres_du_maneton
        self.assertEqual(cylindres_du_maneton(ArchitectureMoteur.EN_LIGNE, 4, 2), "2")
        self.assertEqual(cylindres_du_maneton(ArchitectureMoteur.V, 8, 1), "1 / 5")
        self.assertEqual(cylindres_du_maneton(ArchitectureMoteur.W, 12, 6), "6 / 12")

from django.test import TestCase

# Create your tests here.


from django.test import SimpleTestCase as _SimpleTestCase

from .architecture import architecture_par_defaut


class ArchitectureParDefautTests(_SimpleTestCase):
    def test_cas_courants(self):
        self.assertEqual(architecture_par_defaut("Volkswagen", "EA888-2.0TSI", 4, "TURBO"), "EN_LIGNE")
        self.assertEqual(architecture_par_defaut("Peugeot", "DV6TED4", 4, "TURBO"), "EN_LIGNE")
        self.assertEqual(architecture_par_defaut("BMW", "N54B30", 6, "TURBO"), "EN_LIGNE")
        self.assertEqual(architecture_par_defaut("Audi", "3.0TDI", 6, "TURBO"), "V")
        self.assertEqual(architecture_par_defaut("Nissan", "VR38DETT", 6, "TURBO"), "V")
        self.assertEqual(architecture_par_defaut("Volkswagen", "VR6-2.8", 6, "ATM"), "VR")
        self.assertEqual(architecture_par_defaut("Bentley", "W12_6.0_TwinTurbo", 12, "TURBO"), "W")
        self.assertEqual(architecture_par_defaut("Subaru", "EJ-20", 4, "ATM"), "PLAT")
        self.assertEqual(architecture_par_defaut("Porsche", "9A2-992S", 6, "TURBO"), "PLAT")
        self.assertEqual(architecture_par_defaut("Porsche", "Panamera-EH", 6, "HYB_TE"), "V")
        self.assertEqual(architecture_par_defaut("Mazda", "RX8-1.3-Rotary", 2, "WANKEL"), "ROTATIF")
        self.assertEqual(architecture_par_defaut("Tesla", "Model3", 0, "ELEC"), "SANS")
        self.assertEqual(architecture_par_defaut("Ford", "5.0_Coyote_V8", 8, "ATM"), "V")

from django.test import SimpleTestCase

from . import modules as M
from dBSolutionV3.middleware.modules_tenant import chemin_relatif


class ModulesTenantTests(SimpleTestCase):
    def test_module_de_chemin(self):
        self.assertEqual(M.module_de_chemin("location/trackdays/"), "trackday")
        self.assertEqual(M.module_de_chemin("location/"), "location")
        self.assertEqual(M.module_de_chemin("location/reversements/"), "proprietaires")
        self.assertIsNone(M.module_de_chemin("maintenance/"))
        self.assertEqual(M.module_de_chemin("voiture/exemplaires/finances/"), "finances_vehicules")
        self.assertIsNone(M.module_de_chemin("voiture/exemplaires/modele/x/"))

    def test_normaliser_et_profils(self):
        self.assertIsNone(M.normaliser(M.TOUS))
        self.assertEqual(M.normaliser(["revente"]), [])
        self.assertEqual(M.profil_de(None), "complet")
        for code, (_l, mods) in M.PROFILS.items():
            self.assertEqual(M.profil_de(mods), code)

    def test_chemin_relatif(self):
        self.assertEqual(chemin_relatif("/tenant/campus/fr/location/trackdays/"), "location/trackdays/")
        self.assertIsNone(chemin_relatif("/fr/connexion/"))

    def test_modules_actifs(self):
        class S:
            modules = ["location"]
        m = M.ModulesActifs(S())
        self.assertTrue(m.location)
        self.assertFalse(m.trackday)
        self.assertTrue(M.ModulesActifs(None).trackday)

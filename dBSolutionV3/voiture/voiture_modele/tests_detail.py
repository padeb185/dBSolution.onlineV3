from collections import Counter

from django.test import SimpleTestCase

from voiture.voiture_modele.data.detail import detail
from voiture.voiture_modele.data.modeles import MODELES


class DetailReferentielTests(SimpleTestCase):
    def test_lignes_valides(self):
        for marque, lignes in detail().items():
            for d in lignes:
                with self.subTest(marque=marque, ligne=d):
                    self.assertTrue(d["modele"] and d["generation"] and d["variante"])
                    self.assertLessEqual(len(d["variante"]), 100)
                    self.assertIn(d["portes"], (0, 2, 3, 4, 5))
                    self.assertGreaterEqual(d["reservoir"], 0)
                    self.assertTrue(1900 < d["annee_debut"] < 2100)
                    for cle in ("mois_debut", "mois_fin"):
                        if cle in d:
                            self.assertTrue(1 <= d[cle] <= 12)
                    if "annee_fin" in d:
                        debut = (d["annee_debut"], d.get("mois_debut", 1))
                        fin = (d["annee_fin"], d.get("mois_fin", 12))
                        self.assertLessEqual(debut, fin)
                    if "batterie" in d:
                        self.assertIsInstance(d["batterie"], int)

    def test_pas_de_doublon(self):
        for marque, lignes in MODELES.items():
            cles = Counter((d["modele"].lower(), (d.get("generation") or "").lower(), (d.get("phase") or "").lower(),
                            (d.get("variante") or "").lower()) for d in lignes)
            doublons = [c for c, n in cles.items() if n > 1]
            with self.subTest(marque=marque):
                self.assertEqual(doublons, [])

    def test_fusion_dans_modeles(self):
        for marque, lignes in detail().items():
            self.assertTrue(all(d in MODELES[marque] for d in lignes))

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


class RentabiliteVenteTests(_SimpleTestCase):
    """Après la vente : prix de vente réel, frais de vente et libellé de la facture dans les postes."""

    def _r(self, vente):
        from types import SimpleNamespace as N
        z = _D("0.00")
        e = lambda ht: {"ht": _D(ht)}
        return {
            "acquisition": {"prix_achat": _D("20000"), "taxe_mise_en_circulation": z, "frais_achat": z, "total": _D("20000")},
            "energie": {"carburant": e("1000"), "electricite": e("0"), "adblue": e("0")},
            "maintenances": {"total_internes": _D("500"), "total_externes": z, "total_carrosseries": z,
                             "total_pieces": _D("300"), "total_main_oeuvre": _D("200"), "total": _D("500")},
            "couts_annuels": {"annees": []}, "locations": {"htva": _D("3000"), "nb": 2}, "km": 10000,
            "valeur_revente": _D("15000") if vente else _D("12000"),
            "frais_vente": _D("400") if vente else z,
            "vente": ({"numero": "VH20260001", "date": __import__("datetime").date(2026, 11, 2), "prix_htva": _D("15000"),
                       "frais": _D("400"), "km": 12000, "objet": N(pk=1)} if vente else None),
        }

    def test_postes_apres_vente(self):
        from types import SimpleNamespace as N
        from .rapport import _postes_vehicule
        p = _postes_vehicule(N(), self._r(True))
        self.assertEqual(p["couts"]["cession"][1]["frais_vente"][1], _D("400"))
        libelle, montant = p["gains"]["revente"]
        self.assertIn("VH20260001", str(libelle))
        self.assertEqual(montant, _D("15000"))

    def test_postes_sans_vente(self):
        from types import SimpleNamespace as N
        from .rapport import _postes_vehicule
        p = _postes_vehicule(N(), self._r(False))
        self.assertEqual(p["couts"]["cession"][1]["frais_vente"][1], _D("0.00"))
        self.assertNotIn("VH", str(p["gains"]["revente"][0]))

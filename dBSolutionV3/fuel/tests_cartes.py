from datetime import date
from decimal import Decimal as D

from unittest.mock import patch

from django.test import SimpleTestCase


def _carte(**kw):
    from .models import CarteCarburant
    return CarteCarburant(nom="Total Golf", **kw)


def _op(jour, ttc, carte, famille="carburant"):
    return {"famille": famille, "categorie_label": "Diesel", "immatriculation": "1-ABC-123", "pays": "BE",
            "date": jour, "ttc": D(ttc), "ht": (D(ttc) / D("1.21")).quantize(D("0.01")),
            "tva": D(ttc) - (D(ttc) / D("1.21")).quantize(D("0.01")), "taux": D("21"), "carte": carte}


@patch("fuel.totaux_energie.pays_societe_courant", return_value="BE")   # pas d'accès à la base
class CartesCarburantTests(SimpleTestCase):

    def test_periode_hebdomadaire_lundi_dimanche(self, _pays):
        c = _carte(mode_paiement="HEBDOMADAIRE", delai_paiement_jours=3)
        self.assertEqual(c.periode_de(date(2026, 11, 19)), (date(2026, 11, 16), date(2026, 11, 22)))  # jeudi
        self.assertEqual(c.date_prelevement(date(2026, 11, 22)), date(2026, 11, 25))

    def test_periode_mensuelle(self, _pays):
        c = _carte(mode_paiement="MENSUEL", delai_paiement_jours=10)
        self.assertEqual(c.periode_de(date(2026, 2, 14)), (date(2026, 2, 1), date(2026, 2, 28)))
        self.assertTrue(c.est_periodique)
        self.assertFalse(_carte(mode_paiement="INSTANTANE").est_periodique)

    def test_types_acceptes(self, _pays):
        self.assertTrue(_carte(type_carte="CARBURANT").accepte("adblue"))
        self.assertFalse(_carte(type_carte="CARBURANT").accepte("electricite"))
        self.assertTrue(_carte(type_carte="RECHARGE").accepte("electricite"))
        self.assertTrue(_carte(type_carte="MIXTE").accepte("carburant"))

    def test_ecriture_carte_mensuelle_credite_fournisseur(self, _pays):
        from . import totaux_energie as te
        c = _carte(mode_paiement="MENSUEL")
        lignes = te.ecritures(_op(date(2026, 11, 3), "121.00", c))
        credit = [l for l in lignes if l["credit"]]
        self.assertEqual([l["compte"] for l in credit], ["440000"])
        self.assertEqual(sum(l["debit"] for l in lignes), sum(l["credit"] for l in lignes))

    def test_ecriture_carte_instantanee_credite_banque(self, _pays):
        from . import totaux_energie as te
        lignes = te.ecritures(_op(date(2026, 11, 3), "60.50", _carte(mode_paiement="INSTANTANE")))
        self.assertEqual([l["compte"] for l in lignes if l["credit"]], ["550000"])

    def test_sans_carte_banque(self, _pays):
        from . import totaux_energie as te
        lignes = te.ecritures(_op(date(2026, 11, 3), "60.50", None))
        self.assertEqual([l["compte"] for l in lignes if l["credit"]], ["550000"])

    def test_releves_mensuels(self, _pays):
        from . import totaux_energie as te
        c = _carte(mode_paiement="MENSUEL", delai_paiement_jours=5)
        ops = [_op(date(2025, 10, 2), "100.00", c), _op(date(2025, 10, 20), "50.00", c), _op(date(2025, 11, 4), "30.00", c)]
        r = te.releves_carte(c, ops)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[-1]["ttc"], D("150.00"))          # octobre
        self.assertEqual(r[-1]["prelevement"], date(2025, 11, 5))
        self.assertTrue(r[-1]["paye"])

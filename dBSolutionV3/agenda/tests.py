from django.test import TestCase

# Create your tests here.


from datetime import date, time
from types import SimpleNamespace

from django.test import SimpleTestCase


def _loc(instructeur, debut=None, fin=None, d=date(2026, 11, 20), d_fin=None):
    return SimpleNamespace(instructeur=instructeur, instructeur_id=instructeur.pk, date_debut=d, date_fin=d_fin,
                           heure_debut=debut, heure_fin=fin, client_pilotage_id=None, societe_cliente_id=None,
                           client_id=None)


class PlanningCoachingTests(SimpleTestCase):
    def setUp(self):
        self.a = SimpleNamespace(pk=1, nom="A", prenom="Anne")
        self.b = SimpleNamespace(pk=2, nom="B", prenom="Bob")

    def test_conflit_meme_instructeur_heures_qui_se_recoupent(self):
        from .views_coaching import lignes_du_jour
        lignes = lignes_du_jour([_loc(self.a, time(9), time(11)), _loc(self.a, time(10), time(12))], date(2026, 11, 20))
        self.assertTrue(all(l["conflit"] for l in lignes))

    def test_pas_de_conflit(self):
        from .views_coaching import lignes_du_jour
        lignes = lignes_du_jour([_loc(self.a, time(9), time(10)), _loc(self.a, time(10), time(12)),
                                 _loc(self.b, time(9), time(12))], date(2026, 11, 20))
        self.assertFalse(any(l["conflit"] for l in lignes))

    def test_location_sur_plusieurs_jours(self):
        from .views_coaching import lignes_du_jour
        loc = _loc(self.a, d=date(2026, 11, 20), d_fin=date(2026, 11, 22))
        lignes = lignes_du_jour([loc], date(2026, 11, 21))
        self.assertEqual((lignes[0]["jour_n"], lignes[0]["nb_jours"]), (2, 3))
        self.assertEqual(lignes_du_jour([loc], date(2026, 11, 23)), [])

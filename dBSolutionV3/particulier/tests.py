from datetime import date
from types import SimpleNamespace

from django.test import SimpleTestCase

from . import calculs


class CalculsTests(SimpleTestCase):
    def test_ajouter_mois(self):
        self.assertEqual(calculs.ajouter_mois(date(2026, 1, 31), 1), date(2026, 2, 28))
        self.assertEqual(calculs.ajouter_mois(date(2026, 11, 15), 12), date(2027, 11, 15))

    def test_statut_rappel(self):
        r = SimpleNamespace(actif=True, echeance_date=date(2026, 6, 1), echeance_km=None)
        self.assertEqual(calculs.statut_rappel(r, 0, date(2026, 6, 2))["statut"], "en_retard")
        self.assertEqual(calculs.statut_rappel(r, 0, date(2026, 5, 15))["statut"], "proche")
        self.assertEqual(calculs.statut_rappel(r, 0, date(2026, 1, 1))["statut"], "a_venir")
        r = SimpleNamespace(actif=True, echeance_date=None, echeance_km=50000)
        self.assertEqual(calculs.statut_rappel(r, 49500)["statut"], "proche")
        self.assertEqual(calculs.statut_rappel(r, 50001)["statut"], "en_retard")

    def test_mois_entre(self):
        self.assertEqual(calculs.mois_entre(date(2024, 3, 15), date(2026, 3, 14)), 23)


class JwsAppleTests(SimpleTestCase):
    """Vérification d'une transaction StoreKit 2 avec une chaîne de certificats générée (racine de test)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        import tempfile
        from datetime import datetime, timedelta, timezone
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.x509.oid import NameOID, ObjectIdentifier

        def cert(nom, cle, emetteur_nom, emetteur_cle, oid=None, ca=False):
            maintenant = datetime.now(timezone.utc)
            b = (x509.CertificateBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, nom)]))
                 .issuer_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, emetteur_nom)]))
                 .public_key(cle.public_key()).serial_number(x509.random_serial_number())
                 .not_valid_before(maintenant - timedelta(days=1)).not_valid_after(maintenant + timedelta(days=30))
                 .add_extension(x509.BasicConstraints(ca=ca, path_length=None), critical=True))
            if oid:
                b = b.add_extension(x509.UnrecognizedExtension(ObjectIdentifier(oid), b"\x05\x00"), critical=False)
            return b.sign(emetteur_cle, hashes.SHA256())

        cls.cle_racine, cle_inter, cls.cle_feuille = (ec.generate_private_key(ec.SECP256R1()) for _ in range(3))
        racine = cert("Racine test", cls.cle_racine, "Racine test", cls.cle_racine, ca=True)
        inter = cert("Inter", cle_inter, "Racine test", cls.cle_racine, "1.2.840.113635.100.6.2.1", ca=True)
        feuille = cert("Feuille", cls.cle_feuille, "Inter", cle_inter, "1.2.840.113635.100.6.11.1")
        cls.x5c = [__import__("base64").b64encode(c.public_bytes(serialization.Encoding.DER)).decode()
                   for c in (feuille, inter, racine)]
        cls.fichier_racine = tempfile.NamedTemporaryFile(suffix=".cer", delete=False)
        cls.fichier_racine.write(racine.public_bytes(serialization.Encoding.DER))
        cls.fichier_racine.close()

    def _jws(self, contenu, cle=None):
        import jwt
        return jwt.encode(contenu, cle or self.cle_feuille, algorithm="ES256", headers={"x5c": self.x5c})

    def test_transaction_valide(self):
        from django.test import override_settings
        from . import abonnements
        contenu = {"bundleId": "com.carscosts.carscostsApp", "productId": "carscosts_silver_mensuel",
                   "originalTransactionId": "2000000123", "expiresDate": 1893456000000, "environment": "Sandbox"}
        with override_settings(APPLE_ROOT_CA_G3=self.fichier_racine.name, APPLE_BUNDLE_ID="com.carscosts.carscostsApp"):
            achat = abonnements.transaction_apple(self._jws(contenu))
            self.assertEqual(achat["reference"], "2000000123")
            self.assertEqual(achat["date_fin"].year, 2030)
            self.assertEqual(abonnements.formule_du_produit(achat["produit"]), "silver")
            # Signature d'une autre clé → refus
            from cryptography.hazmat.primitives.asymmetric import ec
            with self.assertRaises(abonnements.AchatRefuse):
                abonnements.transaction_apple(self._jws(contenu, ec.generate_private_key(ec.SECP256R1())))
            # Autre application → refus
            with self.assertRaises(abonnements.AchatRefuse):
                abonnements.transaction_apple(self._jws({**contenu, "bundleId": "com.autre"}))

    def test_racine_differente(self):
        import tempfile
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.x509.oid import NameOID
        from datetime import datetime, timedelta, timezone
        from django.test import override_settings
        from . import abonnements
        cle = ec.generate_private_key(ec.SECP256R1())
        nom = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Autre racine")])
        autre = (x509.CertificateBuilder().subject_name(nom).issuer_name(nom).public_key(cle.public_key())
                 .serial_number(1).not_valid_before(datetime.now(timezone.utc) - timedelta(days=1))
                 .not_valid_after(datetime.now(timezone.utc) + timedelta(days=1)).sign(cle, hashes.SHA256()))
        with tempfile.NamedTemporaryFile(suffix=".cer", delete=False) as f:
            f.write(autre.public_bytes(serialization.Encoding.DER))
        with override_settings(APPLE_ROOT_CA_G3=f.name):
            with self.assertRaises(abonnements.AchatRefuse):
                abonnements.transaction_apple(self._jws({"productId": "carscosts_gold_mensuel", "originalTransactionId": "1"}))


class LimitesTests(SimpleTestCase):
    def test_limites(self):
        from . import abonnements
        self.assertEqual([abonnements.LIMITES[f] for f in abonnements.ORDRE], [1, 2, 5, 10])

    def test_formule_echue(self):
        from datetime import timedelta
        from django.utils import timezone
        from . import abonnements
        ab = SimpleNamespace(formule="gold", date_fin=timezone.now() - timedelta(minutes=1), statut_paiement="ok",
                             date_fin_grace=None)
        self.assertEqual(abonnements.formule_effective(None, ab), "gratuit")
        ab.date_fin = None
        self.assertEqual(abonnements.formule_effective(None, ab), "gold")
        self.assertEqual(abonnements.formule_effective(None, False), "gratuit")


class FacturationTests(SimpleTestCase):
    """Période, délai de grâce, échec de paiement, bandeau et notifications (sans base de données)."""

    def _ab(self, **kw):
        from django.utils import timezone
        from datetime import timedelta
        d = dict(formule="silver", date_fin=timezone.now() + timedelta(days=10), statut_paiement="ok",
                 date_fin_grace=None, renouvellement_auto=True, source="apple", periode="mensuel")
        d.update(kw)
        return SimpleNamespace(**d)

    def test_periode_du_produit(self):
        from . import abonnements
        self.assertEqual(abonnements.periode_du_produit("carscosts_gold_annuel"), "annuel")
        self.assertEqual(abonnements.periode_du_produit("carscosts_gold_mensuel"), "mensuel")
        self.assertEqual(abonnements.periode_du_produit(""), "")
        self.assertEqual(abonnements.formule_du_produit("carscosts_bronze_annuel"), "bronze")

    def test_moins_une_periode(self):
        from datetime import datetime, timezone
        from . import abonnements
        fin = datetime(2026, 3, 31, 10, tzinfo=timezone.utc)
        self.assertEqual(abonnements._moins_une_periode(fin, "mensuel"), datetime(2026, 2, 28, 10, tzinfo=timezone.utc))
        self.assertEqual(abonnements._moins_une_periode(fin, "annuel"), datetime(2025, 3, 31, 10, tzinfo=timezone.utc))
        self.assertIsNone(abonnements._moins_une_periode(None, "mensuel"))

    def test_grace_puis_echec(self):
        from datetime import timedelta
        from django.utils import timezone
        from . import abonnements
        maintenant = timezone.now()
        # Échéance passée mais délai de grâce en cours : formule conservée
        ab = self._ab(date_fin=maintenant - timedelta(days=1), statut_paiement="grace",
                      date_fin_grace=maintenant + timedelta(days=5))
        self.assertEqual(abonnements.formule_effective(None, ab), "silver")
        # Délai de grâce dépassé : gratuit
        ab.date_fin_grace = maintenant - timedelta(minutes=1)
        self.assertEqual(abonnements.formule_effective(None, ab), "gratuit")
        # Échec (compte suspendu par le store) : gratuit même si la date de fin est future
        ab = self._ab(statut_paiement="echec")
        self.assertEqual(abonnements.formule_effective(None, ab), "gratuit")

    def test_statut_apple(self):
        import time
        from . import abonnements
        futur = int((time.time() + 3 * 86400) * 1000)
        passe = int((time.time() - 86400) * 1000)
        self.assertEqual(abonnements.statut_paiement_apple({"gracePeriodExpiresDate": futur})["statut_paiement"], "grace")
        self.assertEqual(abonnements.statut_paiement_apple({"gracePeriodExpiresDate": passe,
                                                            "isInBillingRetryPeriod": True})["statut_paiement"], "echec")
        self.assertEqual(abonnements.statut_paiement_apple({"autoRenewStatus": 1})["statut_paiement"], "ok")

    def test_statut_google(self):
        from django.utils import timezone
        from . import abonnements
        fin = timezone.now()
        self.assertEqual(abonnements.statut_paiement_google("SUBSCRIPTION_STATE_IN_GRACE_PERIOD", fin),
                         {"statut_paiement": "grace", "date_fin_grace": fin})
        self.assertEqual(abonnements.statut_paiement_google("SUBSCRIPTION_STATE_ON_HOLD", fin)["statut_paiement"], "echec")
        self.assertEqual(abonnements.statut_paiement_google("SUBSCRIPTION_STATE_ACTIVE", fin)["statut_paiement"], "ok")

    def test_alerte(self):
        from datetime import timedelta
        from django.utils import timezone
        from . import abonnements
        maintenant = timezone.now()
        ab = self._ab(statut_paiement="grace", date_fin=maintenant - timedelta(days=1),
                      date_fin_grace=maintenant + timedelta(days=5))
        self.assertEqual(abonnements.alerte(ab, "silver", 5, [])["code"], "paiement_refuse")
        ab = self._ab(statut_paiement="echec")
        a = abonnements.alerte(ab, "gratuit", 1, ["v2"])
        self.assertEqual((a["code"], a["niveau"]), ("acces_limite", "erreur"))
        self.assertIn("lecture seule", a["message"])
        ab = self._ab(renouvellement_auto=False, date_fin=maintenant + timedelta(days=3))
        self.assertEqual(abonnements.alerte(ab, "silver", 5, [])["code"], "fin_proche")
        self.assertIsNone(abonnements.alerte(self._ab(), "silver", 5, []))
        self.assertIsNone(abonnements.alerte(None, "gratuit", 1, []))

    def test_messages_notifications(self):
        from datetime import timedelta
        from django.utils import timezone, translation
        from . import notifications
        ab = self._ab(statut_paiement="grace", date_fin_grace=timezone.now() + timedelta(days=5))
        with translation.override("fr"):
            for type_ in ("paiement_refuse", "grace_fin_proche", "acces_limite", "expiree", "paiement_retabli",
                          "renouvellement_proche", "fin_proche"):
                sujet, texte = notifications.message(ab, type_)
                self.assertIn("Silver", sujet + texte)
                self.assertNotIn("%(", sujet + texte)
        self.assertEqual(notifications.cle_echeance(ab, "paiement_refuse"), ab.date_fin_grace.date().isoformat())


class StatistiquesPneusTests(SimpleTestCase):
    def test_statistiques(self):
        from decimal import Decimal
        from . import calculs
        def train(**kw):
            from .models import TrainPneus
            d = dict(position="avant", type_pneus="ete", marque="michelin", prix=Decimal("200"),
                     actif=True, est_monte=False, km_montage=0, km_cumules=0, date_achat=date(2024, 1, 1),
                     date_montage=date(2024, 1, 1), date_remplacement=None)
            d.update(kw)
            t = TrainPneus(**d)
            t.km_effectues = lambda km_actuel=None, t=t: TrainPneus.km_effectues(t, 60000)   # véhicule à 60 000 km
            return t

        trains = [
            # Été remplacé après 30 000 km et 12 mois
            train(actif=False, km_cumules=30000, date_remplacement=date(2025, 1, 1)),
            # Été monté depuis 40 000 km : 20 000 km
            train(est_monte=True, km_montage=40000, date_achat=date(2025, 1, 1)),
            # Hiver démonté, 10 000 km cumulés, sans prix
            train(type_pneus="hiver", position="arriere", marque="Pirelli", prix=None, km_cumules=10000),
            train(type_pneus="slick", marque="", prix=Decimal("600"), km_cumules=1000),
        ]
        s = calculs.statistiques_pneus(trains)
        types = {t["type"]: t for t in s["par_type"]}
        self.assertEqual([t["type"] for t in s["par_type"]], ["ete", "hiver", "4saisons", "pluie", "semi_slick", "slick"])
        self.assertEqual((types["ete"]["trains"], types["ete"]["en_service"], types["ete"]["remplaces"]), (2, 1, 1))
        self.assertEqual(types["ete"]["montes"], 1)
        self.assertEqual(types["ete"]["km"], 50000)
        self.assertEqual(types["ete"]["cout"], Decimal("400.00"))
        self.assertEqual(types["ete"]["cout_1000_km"], Decimal("8.00"))
        self.assertEqual(types["ete"]["km_moyen_remplacement"], 30000)
        self.assertEqual(types["ete"]["duree_moyenne_mois"], 12.0)
        self.assertEqual(types["hiver"]["cout_1000_km"], None)        # prix inconnu
        self.assertEqual(types["4saisons"]["trains"], 0)
        self.assertEqual(s["total"]["trains"], 4)
        self.assertEqual(s["total"]["km"], 61000)
        # Coût aux 1 000 km du total : seulement les km des trains au prix connu (51 000 km pour 1 000 €)
        self.assertEqual(s["total"]["cout_1000_km"], Decimal("19.61"))
        marques = [m["marque"] for m in s["par_marque"]]
        self.assertEqual(marques[0], "Michelin")
        self.assertIn("—", marques)


class CarteTests(SimpleTestCase):
    def test_categories(self):
        from . import carte
        self.assertEqual(carte.categorie({"amenity": "fuel"}), "carburant")
        self.assertEqual(carte.categorie({"amenity": "charging_station"}), "recharge")
        self.assertEqual(carte.categorie({"shop": "car_repair"}), "garage")
        self.assertEqual(carte.categorie({"shop": "car_repair", "service:vehicle:towing": "yes"}), "depannage")
        self.assertEqual(carte.categorie({"shop": "tyres"}), "pneus")
        self.assertEqual(carte.categorie({"shop": "car_repair", "service:vehicle:tyres": "yes"}), "garage")
        self.assertIsNone(carte.categorie({"shop": "bakery"}))

    def test_lieu(self):
        from . import carte
        borne = carte.lieu({"type": "node", "id": 1, "lat": 50.85, "lon": 4.36, "tags": {
            "amenity": "charging_station", "operator": "Allego", "socket:type2": "2", "socket:type2_combo": "1",
            "socket:ccs": "1", "socket:type2_combo:output": "150 kW", "socket:type2:output": "22 kW",
            "capacity": "3", "fee": "yes"}}, 50.85, 4.35)
        self.assertEqual(borne["id"], "n1")
        self.assertEqual(borne["nom"], "Allego")
        self.assertEqual({p["type"]: p["nombre"] for p in borne["prises"]}, {"Type 2": 2, "CCS": 2})
        self.assertEqual(borne["puissance_max"], "150 kW")
        self.assertEqual(borne["points_de_charge"], 3)
        self.assertTrue(borne["payant"])
        self.assertTrue(600 < borne["distance"] < 800)
        station = carte.lieu({"type": "way", "id": 2, "center": {"lat": 50.86, "lon": 4.35}, "tags": {
            "amenity": "fuel", "brand": "TotalEnergies", "fuel:diesel": "yes", "fuel:e10": "yes",
            "addr:street": "Rue Haute", "addr:housenumber": "1", "addr:postcode": "1000", "addr:city": "Bruxelles"}},
            50.85, 4.35)
        self.assertEqual((station["id"], station["categorie"]), ("w2", "carburant"))
        self.assertEqual(station["carburants"], ["Diesel", "E10"])
        self.assertEqual(station["adresse"], "Rue Haute 1, 1000 Bruxelles")
        self.assertIsNone(carte.lieu({"type": "node", "id": 3, "tags": {"amenity": "fuel"}}, 50, 4))

    def test_requete(self):
        from . import carte
        q = carte.requete(50.85, 4.35, 5000, ["carburant", "pneus"])
        self.assertIn('nwr["amenity"="fuel"](around:5000,50.85,4.35);', q)
        self.assertIn('nwr["shop"="tyres"]', q)
        self.assertNotIn("charging_station", q)

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
        ab = SimpleNamespace(formule="gold", date_fin=timezone.now() - timedelta(minutes=1))
        self.assertEqual(abonnements.formule_effective(None, ab), "gratuit")
        ab.date_fin = None
        self.assertEqual(abonnements.formule_effective(None, ab), "gold")
        self.assertEqual(abonnements.formule_effective(None, False), "gratuit")

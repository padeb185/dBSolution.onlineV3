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

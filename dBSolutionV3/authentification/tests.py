import pyotp
from django.test import TestCase
from django.contrib.auth import get_user_model


Utilisateur = get_user_model()


class TOTPTest(TestCase):

    def test_valid_totp_code(self):
        utilisateur = Utilisateur.objects.create_utilisateur(
            email="test@test.com",
            password="secret123"
        )

        utilisateur.totp_secret = pyotp.random_base32()
        utilisateur.save()

        totp = pyotp.TOTP(user.totp_secret)
        code = totp.now()

        self.assertTrue(totp.verify(code))



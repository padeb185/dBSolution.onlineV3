from django.test import TestCase

# Create your tests here.


from django.test import SimpleTestCase
from django.urls import resolve, reverse


class AdministrateurTenantTests(SimpleTestCase):
    """Ajout d'un administrateur de tenant depuis le tableau de bord admin."""

    def test_role_administrateur_est_un_role_valide(self):
        from .models import Utilisateur
        from .views_tenants import ROLE_ADMIN_TENANT
        self.assertIn(ROLE_ADMIN_TENANT, dict(Utilisateur.ROLE_CHOICES))

    def test_urls(self):
        url = reverse("utilisateurs:tenant_admin_choisir")
        self.assertEqual(resolve(url).url_name, "tenant_admin_choisir")
        url = reverse("utilisateurs:tenant_utilisateur_admin",
                      args=[1, "6f1c2b9e-0000-4000-8000-000000000001"])
        self.assertTrue(url.endswith("/administrateur/"))

"""Gestion des comptes particuliers (API et page d'administration)."""
import shutil

from django.conf import settings
from django.db import transaction
from rest_framework.authtoken.models import Token


def supprimer_compte(user):
    """Supprime le compte, ses véhicules, toutes leurs données et ses fichiers (RGPD, App Store)."""
    from .models import AbonnementParticulier, PreferencesParticulier, Vehicule
    dossier = settings.MEDIA_ROOT / "particuliers" / str(user.pk)
    with transaction.atomic():
        Vehicule.objects.filter(proprietaire=user).delete()
        AbonnementParticulier.objects.filter(utilisateur=user).delete()
        PreferencesParticulier.objects.filter(utilisateur=user).delete()
        Token.objects.filter(user=user).delete()
        user.delete()
    shutil.rmtree(dossier, ignore_errors=True)


def activer(user, actif):
    """Active / désactive un compte ; désactivé, son jeton est révoqué (déconnexion de l'application)."""
    user.is_active = actif
    user.save(update_fields=["is_active", "updated_at"])
    if not actif:
        Token.objects.filter(user=user).delete()

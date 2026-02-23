#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script pour supprimer les doublons de VoitureModele dans un tenant spécifique.
Usage : python manage.py runscript supprimer_doublons_voiture_modele
ou python supprimer_doublons_voiture_modele.py (si configuré avec django.setup())
"""

import os
import django

# ⚡ Configuration Django si tu exécutes directement le script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dBSolutionV3.settings")
django.setup()

from societe.models import Societe  # ou ton modèle tenant exact
from voiture.voiture_modele.models import VoitureModele
from django.db.models import Count
from django_tenants.utils import tenant_context

# -----------------------------
# ⚙️ Paramètres
SCHEMA_NAME = "dbsolution"  # nom du tenant à traiter
# -----------------------------

def supprimer_doublons():
    # 1️⃣ Récupérer le tenant
    tenant = Societe.objects.get(schema_name=SCHEMA_NAME)
    print(f"Traitement du tenant : {tenant.schema_name}")

    # 2️⃣ Lancer dans le contexte tenant
    with tenant_context(tenant):
        # Identifier les doublons
        doublons = (
            VoitureModele.objects
            .values("voiture_marque", "nom_modele", "nom_variante")
            .annotate(c=Count("id"))
            .filter(c__gt=1)
        )

        print(f"Nombre de doublons trouvés : {doublons.count()}")

        # 3️⃣ Corriger chaque doublon
        for d in doublons:
            qs = VoitureModele.objects.filter(
                voiture_marque=d['voiture_marque'],
                nom_modele=d['nom_modele'],
                nom_variante=d['nom_variante']
            ).order_by('id')  # garder le plus ancien

            garder = qs.first()
            for obj in qs[1:]:
                # Renommer le doublon pour éviter l'index unique
                obj.nom_variante = f"{obj.nom_variante or 'Variante'}_dup_{obj.id}"
                obj.save()
            print(f"Doublon renommé pour: {d}")

            garder = qs.first()
            for obj in qs[1:]:
                obj.delete()  # supprimer les doublons
            print(f"Doublon corrigé pour: {d}")

    print("✅ Tous les doublons ont été corrigés.")


if __name__ == "__main__":
    supprimer_doublons()
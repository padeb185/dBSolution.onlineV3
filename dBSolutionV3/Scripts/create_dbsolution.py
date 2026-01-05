import os
import sys
import django
from django.utils.text import slugify

# 🔹 Racine du projet (contient manage.py)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# 🔹 Configuration Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dBSolutionV3.settings")
django.setup()

# 🔹 Imports des modèles
from societe.models import Societe, Domain
from adresse.models import Adresse


def create_societe_dbsolution():
    schema_name = "dbsolution"
    nom = "dB Solution"
    domain_url = "dbsolution.localhost"
    directeur = "Pierre-André de Bournonville"
    numero_tva = "BE0123456789"
    site = "https://dbsolution.localhost"

    # ❌ Vérifie si la société existe déjà
    if Societe.objects.filter(schema_name=schema_name).exists():
        print(f"❌ La société '{schema_name}' existe déjà")
        return

    # 🔹 Récupération de l'adresse EXISTANTE
    try:
        adresse = Adresse.objects.get(
            rue__iexact="Place de Cochem",
            code_postal="4960",
            ville__iexact="Malmedy"
        )
    except Adresse.DoesNotExist:
        print("❌ Adresse 'Place de Cochem, 4000 Liège' introuvable")
        print("➡️ Crée l’adresse avant de lancer ce script")
        return
    except Adresse.MultipleObjectsReturned:
        print("❌ Plusieurs adresses 'Place de Cochem' trouvées")
        print("➡️ Précise la recherche (numéro, id)")
        return

    # 🔹 Génération du slug unique
    slug = slugify(nom)
    original_slug = slug
    i = 1
    while Societe.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{i}"
        i += 1

    # 🏗️ Création du tenant (schéma auto)
    societe = Societe.objects.create(
        schema_name=schema_name,
        nom=nom,
        slug=slug,
        directeur=directeur,
        numero_tva=numero_tva,
        site=site,
        adresse=adresse
    )

    # 🌐 Domaine principal
    Domain.objects.create(
        domain=domain_url,
        tenant=societe,
        is_primary=True
    )

    print("✅ Société créée avec succès")
    print(f"   Nom     : {societe.nom}")
    print(f"   Slug    : {societe.slug}")
    print(f"   Schéma  : {societe.schema_name}")
    print(f"   Adresse : {adresse}")
    print(f"   Domaine : {domain_url}")


if __name__ == "__main__":
    create_societe_dbsolution()

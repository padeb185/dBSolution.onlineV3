import os
import sys
import django
from django.utils.text import slugify

# 🔹 Chemin vers la racine du projet (celui qui contient manage.py)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

# 🔹 Paramétrage Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dBSolutionV3.settings")
django.setup()

# 🔹 Import des modèles
from societe.models import Societe, Domain
from adresse.models import Adresse  # si tu veux passer une adresse existante

# 🔹 Fonction pour créer un tenant
def create_tenant(schema_name, nom, domain_url, directeur, numero_tva, adresse_id=None):
    if Societe.objects.filter(schema_name=schema_name).exists():
        print(f"Le tenant '{schema_name}' existe déjà !")
        return

    # Génère un slug unique
    slug = slugify(nom)
    original_slug = slug
    i = 1
    while Societe.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{i}"
        i += 1

    # Récupère l'adresse si fournie
    adresse = None
    if adresse_id:
        try:
            adresse = Adresse.objects.get(pk=adresse_id)
        except Adresse.DoesNotExist:
            print(f"Adresse avec id {adresse_id} introuvable. Ignorée.")

    tenant = Societe(
        schema_name=schema_name,
        nom=nom,
        slug=slug,
        directeur=directeur,
        numero_tva=numero_tva,
        adresse=adresse
    )
    tenant.save()  # crée le tenant et le schéma

    # Crée le domaine associé
    domain = Domain(domain=domain_url, tenant=tenant, is_primary=True)
    domain.save()

    print(f"Tenant '{schema_name}' créé avec succès ! (slug={slug})")

# 🔹 Point d'entrée
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python script_tenant.py <schema_name> <nom> <domain_url> <directeur> <numero_tva> [adresse_id]")
        sys.exit(1)

    schema_name = sys.argv[1]
    nom = sys.argv[2]
    domain_url = sys.argv[3]
    directeur = sys.argv[4]
    numero_tva = sys.argv[5]
    adresse_id = sys.argv[6] if len(sys.argv) > 6 else None

    create_tenant(schema_name, nom, domain_url, directeur, numero_tva, adresse_id)



#python Scripts\script_tenant.py RSRSpa "RSR Spa" dbsolution.rsrspa.localhost "Jean Dupont" BE0123456789

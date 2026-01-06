from django.core.management.base import BaseCommand
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele
from django.db import connection

TENANTS_SCHEMAS = ["dbsolution"]
#TENANTS_SCHEMAS = ["dbsolution", "rsrspa", "rsrnurburg"]

class Command(BaseCommand):
    help = "Créer les modèles Porsche pour tous les tenants (schémas)"

    def set_schema(self, schema_name):
        with connection.cursor() as cursor:
            cursor.execute(f'SET search_path TO {schema_name}, public;')
        self.stdout.write(self.style.NOTICE(f"Schéma actif : {schema_name}"))

    def handle(self, *args, **options):
        modeles_porsche = [
            {"nom_modele": "911", "nom_variante": "Carrera S", "nombre_portes": 2, "nbre_places": 4, "taille_reservoir": 67},
            {"nom_modele": "Cayenne", "nom_variante": "S", "nombre_portes": 5, "nbre_places": 5, "taille_reservoir": 75},
            {"nom_modele": "Panamera", "nom_variante": "4S", "nombre_portes": 5, "nbre_places": 5, "taille_reservoir": 75},
            {"nom_modele": "Macan", "nom_variante": None, "nombre_portes": 5, "nbre_places": 5, "taille_reservoir": 60},
        ]

        for schema in TENANTS_SCHEMAS:
            self.set_schema(schema)

            # Création de la marque Porsche
            marque, created = VoitureMarque.objects.get_or_create(nom_marque="Porsche")
            self.stdout.write(self.style.SUCCESS(
                f"Marque : {marque.nom_marque} ({'créée' if created else 'existante'}) dans {schema}"
            ))

            # Création des modèles
            for m in modeles_porsche:
                modele_obj, created = VoitureModele.objects.get_or_create(
                    voiture_marque=marque,
                    nom_modele=m["nom_modele"],
                    nom_variante=m.get("nom_variante"),
                    defaults={
                        "nombre_portes": m["nombre_portes"],
                        "nbre_places": m["nbre_places"],
                        "taille_reservoir": m["taille_reservoir"]
                    }
                )
                self.stdout.write(self.style.SUCCESS(
                    f"Modèle : {modele_obj} ({'créé' if created else 'existant'}) dans {schema}"
                ))

        self.stdout.write(self.style.SUCCESS("\nTous les modèles Porsche ont été créés pour tous les tenants !"))

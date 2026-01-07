from django.core.management.base import BaseCommand
from django.db import connection
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele

# Liste des tenants/schémas
TENANTS_SCHEMAS = ["dbsolution"]  # Ajouter d'autres tenants si besoin

class Command(BaseCommand):
    help = "Créer tous les modèles Porsche (depuis la 550 Spyder) pour tous les tenants, incluant GT3, GT3 RS, GT2 RS, sans doublons"

    def set_schema(self, schema_name):
        """Active le schéma pour le tenant."""
        with connection.cursor() as cursor:
            cursor.execute(f'SET search_path TO {schema_name}, public;')
        self.stdout.write(self.style.NOTICE(f"Schéma actif : {schema_name}"))

    def handle(self, *args, **options):
        # Liste des modèles Porsche
        modeles_porsche = [
            # Historiques
            {"nom_modele": "550 Spyder", "nom_variante": None, "nombre_portes": 2, "nbre_places": 2, "taille_reservoir": 60},

            # 911 classiques
            {"nom_modele": "911", "nom_variante": "Carrera S", "nombre_portes": 2, "nbre_places": 4, "taille_reservoir": 67},
            {"nom_modele": "911", "nom_variante": "Turbo", "nombre_portes": 2, "nbre_places": 4, "taille_reservoir": 67},

            # 911 GT spéciaux
            {"nom_modele": "911", "nom_variante": "GT3", "nombre_portes": 2, "nbre_places": 2, "taille_reservoir": 64},
            {"nom_modele": "911", "nom_variante": "GT3 RS", "nombre_portes": 2, "nbre_places": 2, "taille_reservoir": 64},
            {"nom_modele": "911", "nom_variante": "GT2 RS", "nombre_portes": 2, "nbre_places": 2, "taille_reservoir": 64},

            # SUV et berlines
            {"nom_modele": "Cayenne", "nom_variante": "S", "nombre_portes": 5, "nbre_places": 5, "taille_reservoir": 75},
            {"nom_modele": "Macan", "nom_variante": None, "nombre_portes": 5, "nbre_places": 5, "taille_reservoir": 60},
            {"nom_modele": "Panamera", "nom_variante": "4S", "nombre_portes": 5, "nbre_places": 5, "taille_reservoir": 75},
        ]

        for schema in TENANTS_SCHEMAS:
            # Activer le schéma du tenant
            self.set_schema(schema)

            # Création de la marque Porsche si elle n'existe pas
            marque, created = VoitureMarque.objects.get_or_create(nom_marque="Porsche")
            status_marque = "créée" if created else "existante"
            self.stdout.write(self.style.SUCCESS(f"Marque {marque.nom_marque} ({status_marque}) dans le schema {schema}"))

            # Création des modèles Porsche sans doublon
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
                status_modele = "créé" if created else "existant"
                self.stdout.write(self.style.SUCCESS(f"Modèle {modele_obj} ({status_modele}) dans {schema}"))

        self.stdout.write(self.style.SUCCESS("\nTous les modèles Porsche ont été créés pour tous les tenants !"))

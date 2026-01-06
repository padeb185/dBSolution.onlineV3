from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele


class Command(BaseCommand):
    help = "Ajoute des modèles automobiles pour chaque marque pour le tenant 'db-solution'"

    def handle(self, *args, **options):
        try:
            tenant = Societe.objects.get(slug='db-solution')
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'db-solution' introuvable !"))
            return

        # Marques avec modèles (exemple de quelques modèles par marque)
        marques_modeles = {
            "Peugeot": ["208", "308", "508", "2008", "3008", "5008"],
            "Renault": ["Clio", "Megane", "Talisman", "Captur", "Koleos", "Espace"],
            "Citroën": ["C1", "C3", "C4", "C5", "C5 Aircross", "C4 Cactus"],
            "Volkswagen": ["Golf", "Polo", "Passat", "T-Roc", "Tiguan", "Arteon"],
            "BMW": ["Serie 1", "Serie 2", "Serie 3", "Serie 4", "Serie 5", "X1", "X3"],
            "Mercedes-Benz": ["A-Class", "C-Class", "E-Class", "S-Class", "GLA", "GLC", "GLE"],
            "Toyota": ["Corolla", "Yaris", "Camry", "RAV4", "Prius", "Land Cruiser"],
            "Ford": ["Fiesta", "Focus", "Mondeo", "Mustang", "Explorer", "F-150"],
            "Tesla": ["Model S", "Model 3", "Model X", "Model Y", "Cybertruck"],
            "Nissan": ["Micra", "Juke", "Qashqai", "X-Trail", "Leaf"],
            "Honda": ["Civic", "Accord", "CR-V", "HR-V", "Jazz"],
            # tu peux ajouter les autres marques ici comme Hyundai, Kia, etc.
        }

        created_count = 0

        with tenant_context(tenant):
            for marque_nom, modeles in marques_modeles.items():
                try:
                    marque_obj = VoitureMarque.objects.get(nom_marque=marque_nom)
                except VoitureMarque.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Marque '{marque_nom}' non trouvée."))
                    continue

                for modele_nom in modeles:
                    # Crée le modèle avec valeurs par défaut pour les champs obligatoires
                    _, created = VoitureModele.objects.get_or_create(
                        nom_modele=modele_nom,
                        voiture_marque=marque_obj,
                        nombre_portes=VoitureModele.NombrePortes.CINQ,  # valeur par défaut 5 portes
                        nbre_places=5,                                   # valeur par défaut
                        taille_reservoir=50.0,                           # valeur par défaut en litres
                    )
                    if created:
                        created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} modèles ajoutés avec succès pour le tenant '{tenant.schema_name}'"
        ))

#python manage.py create_voitures_modeles
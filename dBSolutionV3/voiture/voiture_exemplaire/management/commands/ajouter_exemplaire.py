# voiture/voiture_exemplaire/management/commands/add_exemplaire.py
import uuid
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_exemplaire.models import VoitureExemplaire

class Command(BaseCommand):
    help = "Ajoute un exemplaire pour un modèle donné dans le tenant choisi"

    def add_arguments(self, parser):
        parser.add_argument(
            "--tenant", type=str, required=True, help="Slug du tenant (ex: db-solution)"
        )
        parser.add_argument(
            "--modele_id", type=str, required=True, help="ID du modèle pour lequel créer l'exemplaire"
        )
        parser.add_argument(
            "--pays", type=str, choices=["Belgique", "Luxembourg"], default="Belgique",
            help="Pays pour la plaque"
        )
        parser.add_argument(
            "--immatriculation", type=str, default=None, help="Immatriculation (optionnel)"
        )
        parser.add_argument(
            "--type_utilisation", type=str, choices=["societe", "client", "prive", "location", "interne", "utilitaire"],
            default="prive", help="Type d'utilisation de l'exemplaire"
        )

    def handle(self, *args, **options):
        # Récupération du tenant
        try:
            tenant = Societe.objects.get(slug=options["tenant"])
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Tenant '{options['tenant']}' introuvable !"))
            return

        with tenant_context(tenant):
            # Récupération du modèle
            try:
                modele = VoitureModele.objects.get(id=options["modele_id"])
            except VoitureModele.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Modèle '{options['modele_id']}' introuvable !"))
                return



# 🔹 Paramètres
tenant_slug = "db-solution"
voiture_marque = "Mini" # Ton tenant
modele_nom = "One"      # Nom du modèle
pays = "Luxembourg"              # Pour la plaque
type_utilisation = "prive"       # Exemple
immatriculation = "HT-6544"           # Générée automatiquement

# Récupérer le tenant
tenant = Societe.objects.get(slug=tenant_slug)

with tenant_context(tenant):
    # Récupérer le modèle Mini One R50
    modele = VoitureModele.objects.get(nom_modele=modele_nom)
    marque = modele.voiture_marque

    # Générer immatriculation luxembourgeoise si nécessaire
    if not immatriculation:
        immatriculation = f"L-{uuid.uuid4().hex[:6].upper()}"

    # Créer l'exemplaire
    exemplaire = VoitureExemplaire.objects.create(
        voiture_marque=marque,
        voiture_modele=modele,
        immatriculation=immatriculation,
        pays=pays,
        type_utilisation=type_utilisation,
        annee_production=timezone.now().year,
        mois_production=timezone.now().month,
        date_mise_en_circulation=timezone.now().date(),
    )

    print(f"Exemplaire créé ! ID={exemplaire.id}, Immatriculation={exemplaire.immatriculation}, Pays={exemplaire.pays}")
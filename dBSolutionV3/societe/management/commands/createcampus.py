from django.core.management.base import BaseCommand
from django.utils.text import slugify
from societe.models import Societe, Domain
from adresse.models import Adresse

class Command(BaseCommand):
    help = "Créer le tenant Campus"

    def handle(self, *args, **kwargs):
        schema_name = "campus"
        nom = "campus"
        domain_url = "CarsCosts/Campus"
        directeur = "Pierre-André de Bournonville"
        numero_tva = "BE0123456787"
        site = "https://wwww.carscosts.com"

        # 🔹 Vérifie si la société existe déjà
        if Societe.objects.filter(schema_name=schema_name).exists():
            self.stdout.write(self.style.WARNING(f"La société '{schema_name}' existe déjà"))
            return

        # 🔹 Création ou récupération de l'adresse
        adresse, created = Adresse.objects.get_or_create(
            rue="Route du circuit",
            numero= 60,
            boite= 1,
            code_postal="4970",
            ville="Francorchamps",
            defaults={
                "pays": "Belgique"  # Ajouter d'autres champs si nécessaire
            },
            code_pays="BE",
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Adresse créée : {adresse}"))
        else:
            self.stdout.write(self.style.WARNING(f"Adresse existante utilisée : {adresse}"))

        # 🔹 Génération du slug unique
        slug = slugify(nom)
        original_slug = slug
        i = 1
        while Societe.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{i}"
            i += 1

        # 🔹 Création du tenant
        societe = Societe.objects.create(
            schema_name=schema_name,
            nom=nom,
            slug=slug,
            directeur=directeur,
            numero_tva=numero_tva,
            site=site,
            adresse=adresse  # ⚠️ juste l'objet Adresse
        )

        # 🔹 Domaine principal
        Domain.objects.create(
            domain=domain_url,
            tenant=societe,
            is_primary=True
        )

        self.stdout.write(self.style.SUCCESS(f"Société '{nom}' créée avec succès"))

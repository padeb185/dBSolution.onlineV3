from django.core.management.base import BaseCommand
from django.utils.text import slugify
from societe.models import Societe, Domain
from adresse.models import Adresse

class Command(BaseCommand):
    help = "Créer le tenant RSR Nurburg"

    def handle(self, *args, **kwargs):
        schema_name = "rsrnurburg"
        nom = "RSR Nurburg"
        domain_url = "dbsolution.localhost/rsrnurburg"
        directeur = "Ron Simons"
        numero_tva = "DE814467844"
        site = "https://dbsolution.localhost/rsrnurburg"

        # 🔹 Vérifie si la société existe déjà
        if Societe.objects.filter(schema_name=schema_name).exists():
            self.stdout.write(self.style.WARNING(f"❌ La société '{schema_name}' existe déjà"))
            return

        # 🔹 Création ou récupération de l'adresse
        adresse, created = Adresse.objects.get_or_create(
            rue="Antoniusweg",
            numero= 1,
            boite= 1,
            code_postal="53520",
            ville="Nürburg",
            defaults={
                "pays": "Allemagne"
            },
            code_pays ="DE"
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Adresse créée : {adresse}"))
        else:
            self.stdout.write(self.style.WARNING(f"ℹ️ Adresse existante utilisée : {adresse}"))

        # 🔹 Génération du slug unique
        slug = slugify(nom)
        original_slug = slug
        i = 1
        while Societe.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{i}"
            i += 1

        # 🔹 Création du tenant (schéma auto)
        societe = Societe.objects.create(
            schema_name=schema_name,
            nom=nom,
            slug=slug,
            directeur=directeur,
            numero_tva=numero_tva,
            site=site,
            adresse=adresse
        )

        # 🔹 Domaine principal
        Domain.objects.create(
            domain=domain_url,
            tenant=societe,
            is_primary=True
        )

        self.stdout.write(self.style.SUCCESS(f"✅ Société '{nom}' créée avec succès"))

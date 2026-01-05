from django.core.management.base import BaseCommand
from adresse.models import Adresse

class Command(BaseCommand):
    help = "Ajoute des adresses de test"

    def handle(self, *args, **options):
        adresses = [
            {
                "rue": "Place de Cochem",
                "numero": "3",
                "code_postal": "4960",
                "ville": "Malmedy",
                "pays": "Belgique",
                "code_pays": "BE"
            },
            {
                "rue": "Rue du Pouhon",
                "numero": "2",
                "code_postal": "4970",
                "ville": "Stavelot",
                "pays": "Belgique",
                "code_pays": "BE"
            },
            {
                "rue": "Antoniusweg",
                "numero": "1",
                "code_postal": "53520",
                "ville": "Nürburg",
                "pays": "Germany",
                "code_pays": "DE"
            },
        ]

        for data in adresses:
            adresses, created = Adresse.objects.get_or_create(**data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Créée : {adresses}"))
            else:
                self.stdout.write(self.style.WARNING(f"Existe déjà : {adresses}"))




# python manage.py script_adresses
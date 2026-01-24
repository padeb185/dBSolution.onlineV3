from django.core.management.base import BaseCommand
from django.utils.text import slugify
from societe.models import Societe, Domain
from adresse.models import Adresse
from datetime import date
import uuid


class Command(BaseCommand):
    help = "Créer une société (tenant) avec son domaine et son adresse"

    def add_arguments(self, parser):
        parser.add_argument('--nom', type=str, required=True, help="Nom de la société")
        parser.add_argument('--directeur', type=str, required=True, help="Nom du directeur")
        parser.add_argument('--numero_tva', type=str, required=True, help="Numéro de TVA")
        parser.add_argument('--site', type=str, required=False, help="Site web de la société")
        parser.add_argument('--domaine', type=str, required=True, help="Domaine du tenant (ex: societe.localhost)")

        # Champs adresse
        parser.add_argument('--rue', type=str, required=True, help="Rue")
        parser.add_argument('--numero', type=str, required=True, help="Numéro")
        parser.add_argument('--code_postal', type=str, required=True, help="Code postal")
        parser.add_argument('--ville', type=str, required=True, help="Ville")
        parser.add_argument('--pays', type=str, default="Belgique", help="Pays")
        parser.add_argument('--code_pays', type=str, default="BE", help="Code pays")

    def handle(self, *args, **options):
        # Création de l'adresse
        adresse = Adresse.objects.create(
            rue=options['rue'],
            numero=options['numero'],
            code_postal=options['code_postal'],
            ville=options['ville'],
            pays=options['pays'],
            code_pays=options['code_pays']
        )

        self.stdout.write(self.style.SUCCESS(f"Adresse créée : {adresse}"))

        # Création du tenant (société)
        societe = Societe(
            nom=options['nom'],
            directeur=options['directeur'],
            numero_tva=options['numero_tva'],
            site=options.get('site'),
            adresse=adresse
        )
        societe.slug = slugify(options['nom'])
        societe.save()  # Crée le schema automatiquement grâce à auto_create_schema

        # Création du domaine
        Domain.objects.create(
            tenant=societe,
            domain=options['domaine'],
            is_primary=True
        )

        self.stdout.write(self.style.SUCCESS(
            f"Société '{societe.nom}' créée avec succès, domaine : {options['domaine']}"
        ))




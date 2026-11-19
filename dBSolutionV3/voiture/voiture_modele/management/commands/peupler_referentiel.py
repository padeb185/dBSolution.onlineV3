"""
Référentiel véhicules complet d'un ou plusieurs tenants, dans l'ordre :
  1. moteurs              (create_moteur)
  2. boîtes de vitesses   (create_boite_vitesse)
  3. marques + modèles + liens modèle → moteurs (populate_voitures)

Lancé automatiquement à la création d'un tenant (en arrière-plan), ou à la main :
    python manage.py peupler_referentiel --tenant carscosts
    python manage.py peupler_referentiel --all
Idempotent : relancer ne crée pas de doublons (les éléments existants sont mis à jour).
"""
import time

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django_tenants.utils import get_public_schema_name

from societe.models import Societe


class Command(BaseCommand):
    help = "Charge le référentiel véhicules (moteurs, boîtes, marques, modèles) d'un ou plusieurs tenants."

    def add_arguments(self, parser):
        parser.add_argument("--tenant", action="append", dest="tenants", default=[])
        parser.add_argument("--all", action="store_true", help="Tous les tenants (hors public)")

    def handle(self, *args, **opts):
        if opts["all"]:
            schemas = list(Societe.objects.exclude(schema_name=get_public_schema_name())
                           .values_list("schema_name", flat=True))
        elif opts["tenants"]:
            schemas = opts["tenants"]
        else:
            raise CommandError("Préciser --tenant <schema> ou --all")

        for schema in schemas:
            debut = time.monotonic()
            self.stdout.write(f"=== Référentiel véhicules : {schema}")
            for etape, commande in (("Moteurs", "create_moteur"), ("Boîtes de vitesses", "create_boite_vitesse"),
                                    ("Marques et modèles", "populate_voitures")):
                self.stdout.write(f"--- {etape}")
                self.stdout.flush()
                call_command(commande, tenants=[schema], stdout=self.stdout, stderr=self.stderr)
            self.stdout.write(self.style.SUCCESS(
                f"=== Terminé : {schema} ({time.monotonic() - debut:.0f} s)"))

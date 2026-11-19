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
        parser.add_argument("--tenant", action="append", dest="tenants", default=[],
                            help="Schéma du tenant (ou son slug, ou son nom entre guillemets)")
        parser.add_argument("--all", action="store_true", help="Tous les tenants (hors public)")

    def handle(self, *args, **opts):
        if opts["all"]:
            schemas = list(Societe.objects.exclude(schema_name=get_public_schema_name())
                           .values_list("schema_name", flat=True))
        elif opts["tenants"]:
            schemas = [self._schema(t) for t in opts["tenants"]]
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

    @staticmethod
    def _schema(valeur):
        """Schéma d'un tenant donné par son schéma, son slug ou son nom (sans tenir compte de la casse)."""
        v = (valeur or "").strip()
        for champ in ("schema_name", "slug", "nom"):
            t = Societe.objects.filter(**{f"{champ}__iexact": v}).first()
            if t:
                return t.schema_name
        disponibles = ", ".join(
            f"{s} ({n})" for s, n in Societe.objects.exclude(schema_name=get_public_schema_name())
            .order_by("schema_name").values_list("schema_name", "nom"))
        raise CommandError(f"Tenant « {v} » introuvable dans cette base. Tenants disponibles : {disponibles or 'aucun'}")


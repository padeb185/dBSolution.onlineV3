"""
Reprise des données : liaison des interventions boîte existantes à la boîte du véhicule.

Même règle que pour le moteur (migrations 0065/0066 de remplacement_moteur) :
une intervention est liée à la boîte actuellement montée si elle est postérieure au dernier
remplacement de boîte du véhicule (ou si le véhicule n'a jamais changé de boîte).
Le dernier remplacement de chaque véhicule reçoit la boîte actuelle comme « nouvelle boîte ».
Les interventions plus anciennes restent sans boîte (l'ancienne boîte n'est pas connue).

Multi-sociétés (django-tenants) : la commande traite chaque société dans son schéma.

Usage : python manage.py lier_interventions_boite [--simulation] [--schema nom_du_schema]
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django_tenants.utils import get_public_schema_name, get_tenant_model, schema_context

from maintenance.autres_interventions.boite_de_vitesse.boite_liee import (
    boite_actuelle, modeles_interventions_boite,
)


class Command(BaseCommand):
    help = "Lie les interventions boîte / embrayage existantes à la boîte du véhicule."

    def add_arguments(self, parser):
        parser.add_argument("--simulation", action="store_true", help="Affiche le résultat sans rien enregistrer.")
        parser.add_argument("--schema", help="Ne traiter que cette société (nom du schéma).")

    def handle(self, *args, **options):
        # Chaque société a son propre schéma : on les parcourt toutes (sauf « public »)
        societes = get_tenant_model().objects.exclude(schema_name=get_public_schema_name())
        if options.get("schema"):
            societes = societes.filter(schema_name=options["schema"])
        for societe in societes.order_by("schema_name"):
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n=== {societe.schema_name} ==="))
            with schema_context(societe.schema_name):
                self.traiter_schema(options)

    def traiter_schema(self, options):
        from voiture.voiture_exemplaire.models import VoitureExemplaire
        from maintenance.autres_interventions.boite_de_vitesse.remplacement_boite.models import RemplacementBoite
        from maintenance.autres_interventions.bte_vitesse_auto.remplacement_bte_auto.models import RemplacementBteAuto

        simulation = options["simulation"]
        boites = {}
        for ex_id in VoitureExemplaire.objects.values_list("pk", flat=True):
            b = boite_actuelle(ex_id)
            if b:
                boites[ex_id] = b.pk
        self.stdout.write(f"Véhicules avec une boîte : {len(boites)}")

        # Dernier remplacement (manuel ou automatique) de chaque véhicule
        dernier = {}
        for Modele in (RemplacementBoite, RemplacementBteAuto):
            for r in Modele.objects.filter(voiture_exemplaire_id__in=boites.keys()).order_by("date", "pk"):
                actuel = dernier.get(r.voiture_exemplaire_id)
                if actuel is None or (r.date and actuel.date and r.date >= actuel.date):
                    dernier[r.voiture_exemplaire_id] = r

        total = 0
        with transaction.atomic():
            for ex_id, r in dernier.items():
                if r.nouvelle_boite_id is None and r.boite_liee_id != boites[ex_id]:
                    type(r).objects.filter(pk=r.pk).update(nouvelle_boite_id=boites[ex_id])

            for Modele in modeles_interventions_boite():
                n = 0
                for obj in Modele.objects.filter(boite_liee__isnull=True, voiture_exemplaire_id__in=boites.keys()).only(
                        "pk", "voiture_exemplaire_id", "date"):
                    r = dernier.get(obj.voiture_exemplaire_id)
                    if r is not None and r.pk == obj.pk:
                        continue  # le remplacement lui-même : l'ancienne boîte n'est pas connue
                    if r is None or (obj.date and r.date and obj.date >= r.date):
                        Modele.objects.filter(pk=obj.pk).update(boite_liee_id=boites[obj.voiture_exemplaire_id])
                        n += 1
                total += n
                self.stdout.write(f"  {Modele._meta.verbose_name} : {n}")
            if simulation:
                transaction.set_rollback(True)
        self.stdout.write(self.style.SUCCESS(
            f"{total} intervention(s) liée(s){' (simulation, rien enregistré)' if simulation else ''}."))

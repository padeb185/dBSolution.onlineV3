"""
Rattache les interventions qui ont perdu leur maintenance (ou n'y ont jamais été liées).

    python manage.py reparer_maintenances            # toutes les sociétés
    python manage.py reparer_maintenances --dry-run  # simulation
"""
from django.core.management.base import BaseCommand
from django_tenants.utils import get_tenant_model, schema_context

from piece.rattachement import modeles_intervention, rattacher_maintenance, score, types_du_modele


class Command(BaseCommand):
    help = "Rattache les interventions sans maintenance à leur maintenance."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--schema", help="Une seule société (schema_name)")

    def handle(self, *args, **opts):
        societes = get_tenant_model().objects.exclude(schema_name="public")
        if opts.get("schema"):
            societes = societes.filter(schema_name=opts["schema"])
        for societe in societes:
            with schema_context(societe.schema_name):
                self._reparer(societe.schema_name, opts["dry_run"])

    def _reparer(self, schema, dry):
        from maintenance.models import Maintenance
        total = 0
        for modele in modeles_intervention():
            try:
                orphelins = list(modele.objects.filter(maintenance__isnull=True).exclude(voiture_exemplaire__isnull=True))
            except Exception:
                continue
            types = types_du_modele(modele)
            for obj in orphelins:
                qs = Maintenance.objects.filter(voiture_exemplaire_id=obj.voiture_exemplaire_id)
                if types:
                    qs = qs.filter(type_maintenance__in=types)
                libres = [m for m in qs if not modele.objects.filter(maintenance=m).exists()]
                if not libres:
                    self.stdout.write(f"[{schema}] {modele.__name__} #{obj.pk} : aucune maintenance libre")
                    continue
                libres.sort(key=lambda m: score(obj, m), reverse=True)
                m = libres[0]
                self.stdout.write(f"[{schema}] {modele.__name__} #{obj.pk} -> maintenance {m.pk} "
                                  f"({m.immatriculation} {m.date_intervention} {m.get_type_maintenance_display()})")
                if not dry:
                    modele.objects.filter(pk=obj.pk).update(maintenance=m)
                total += 1
        self.stdout.write(self.style.SUCCESS(f"[{schema}] {total} intervention(s) rattachée(s)" + (" (simulation)" if dry else "")))

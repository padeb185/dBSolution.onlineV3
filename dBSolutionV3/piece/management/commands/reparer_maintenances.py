"""
Répare les interventions qui ont perdu leur maintenance (champ caché « maintenance » vidé par les
formulaires « modifier »). L'intervention est rattachée à la maintenance orpheline du même véhicule
et du même type, en privilégiant le même kilométrage puis la même date.

    python manage.py reparer_maintenances            # toutes les sociétés
    python manage.py reparer_maintenances --dry-run  # simulation
"""
import re
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from django_tenants.utils import get_tenant_model, schema_context


def _modeles_intervention():
    from maintenance.models import Maintenance
    for rel in Maintenance._meta.related_objects:
        m = rel.related_model
        if hasattr(m, "generer_rapport_remplacement") and rel.field.name == "maintenance":
            yield m, rel


def _types_du_modele(modele):
    """Types de maintenance créés par l'app du modèle (lus dans ses vues)."""
    app = apps.get_containing_app_config(modele.__module__)
    types = set()
    for f in Path(app.path).glob("*.py"):
        try:
            texte = f.read_text(encoding="utf-8")
        except Exception:
            continue
        types.update(re.findall(r"TypeMaintenance\.([A-Z0-9_]+)", texte))
    return types


def _kilometrages(obj):
    vals = set()
    for f in obj._meta.concrete_fields:
        if f.name.startswith(("kilometrage", "km_")) and "variation" not in f.name:
            v = getattr(obj, f.name, None)
            if isinstance(v, (int, float)) or (v is not None and str(v).isdigit()):
                vals.add(int(v))
    return vals


def _date(obj):
    for nom in ("date", "date_intervention", "created_at", "date_creation"):
        v = getattr(obj, nom, None)
        if v:
            return v.date() if hasattr(v, "date") else v
    return None


class Command(BaseCommand):
    help = "Rattache les interventions sans maintenance à leur maintenance (après le bug des formulaires « modifier »)."

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
        modeles = list(_modeles_intervention())
        for modele, rel in modeles:
            try:
                orphelins = list(modele.objects.filter(maintenance__isnull=True).exclude(voiture_exemplaire__isnull=True))
            except Exception:
                continue  # table absente dans ce schéma
            if not orphelins:
                continue
            types = {t for t in _types_du_modele(modele) if hasattr(Maintenance.TypeMaintenance, t)}
            types = {getattr(Maintenance.TypeMaintenance, t) for t in types}
            for obj in orphelins:
                candidates = Maintenance.objects.filter(voiture_exemplaire_id=obj.voiture_exemplaire_id)
                if types:
                    candidates = candidates.filter(type_maintenance__in=types)
                # maintenance encore libre pour ce type d'intervention
                candidates = [m for m in candidates if not modele.objects.filter(maintenance=m).exists()]
                if not candidates:
                    self.stdout.write(f"[{schema}] {modele.__name__} #{obj.pk} : aucune maintenance libre")
                    continue
                kms, d = _kilometrages(obj), _date(obj)

                def score(m):
                    s = 0
                    if kms & {m.kilometres_chassis or -1, m.kilometres_total or -1}:
                        s += 2
                    if d and m.date_intervention == d:
                        s += 1
                    return s
                candidates.sort(key=score, reverse=True)
                m = candidates[0]
                self.stdout.write(f"[{schema}] {modele.__name__} #{obj.pk} -> maintenance {m.pk} "
                                  f"({m.immatriculation} {m.date_intervention} {m.get_type_maintenance_display()})")
                if not dry:
                    with transaction.atomic():
                        modele.objects.filter(pk=obj.pk).update(maintenance=m)
                total += 1
        self.stdout.write(self.style.SUCCESS(f"[{schema}] {total} intervention(s) rattachée(s)" + (" (simulation)" if dry else "")))

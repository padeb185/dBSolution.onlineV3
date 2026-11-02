from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, ForeignKey, ManyToManyField, OneToOneField
from django_tenants.utils import get_public_schema_name, tenant_context

from societe.models import Societe
from voiture.voiture_modele.models import VoitureModele

CLE = ("voiture_marque", "nom_modele", "generation", "phase", "nom_variante")


class Command(BaseCommand):
    help = ("Supprime les doublons de VoitureModele (marque, modèle, génération, phase, variante) "
            "en réassignant les FK et les liens M2M (moteurs…) vers le modèle conservé.")

    def add_arguments(self, parser):
        parser.add_argument("--tenant", action="append", dest="tenants", default=[])
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        fk, m2m = [], []
        for model in apps.get_models():
            for field in model._meta.get_fields():
                if getattr(field, "related_model", None) is not VoitureModele or field.auto_created:
                    continue
                if isinstance(field, (ForeignKey, OneToOneField)):
                    fk.append((model, field.name))
                elif isinstance(field, ManyToManyField):
                    m2m.append((model, field.name))
        self.stdout.write(f"{len(fk)} FK et {len(m2m)} M2M vers VoitureModele")

        tenants = Societe.objects.exclude(schema_name=get_public_schema_name())
        if opts["tenants"]:
            tenants = tenants.filter(schema_name__in=opts["tenants"])

        for tenant in tenants:
            with tenant_context(tenant), transaction.atomic():
                total = 0
                groupes = (VoitureModele.objects.values(*CLE).annotate(nb=Count("id")).filter(nb__gt=1))
                for g in groupes:
                    ids = list(
                        VoitureModele.objects.filter(**{
                            (f"{c}__isnull" if g[c] is None else c): (True if g[c] is None else g[c]) for c in CLE
                        }).order_by("created_at", "id").values_list("id", flat=True)
                    )
                    keep, doublons = ids[0], ids[1:]
                    for dup in doublons:
                        for model, name in fk:
                            model.objects.filter(**{f"{name}_id": dup}).update(**{name: keep})
                        for model, name in m2m:
                            through = getattr(model, name).through
                            src = [f.name for f in through._meta.fields
                                   if f.is_relation and f.related_model is model][0]
                            proprietaires = through.objects.filter(**{self._col(through): dup}) \
                                .values_list(f"{src}_id", flat=True)
                            for obj_id in list(proprietaires):
                                getattr(model.objects.only("pk").get(pk=obj_id), name).add(keep)
                        VoitureModele.objects.filter(id=dup).only("id").delete()
                        total += 1
                if opts["dry_run"]:
                    transaction.set_rollback(True)
                self.stdout.write(self.style.SUCCESS(
                    f"[{tenant.schema_name}] doublons supprimés : {total}" + (" (simulation)" if opts["dry_run"] else "")
                ))

    @staticmethod
    def _col(through):
        f = [f for f in through._meta.fields if f.is_relation and f.related_model is VoitureModele][0]
        return f"{f.name}_id"

"""
Supprime une ou plusieurs marques (et leurs modèles) dans les tenants choisis.

Une marque n'est PAS supprimée si elle ou l'un de ses modèles est encore utilisé (véhicule, recharge, pièce,
garage, etc.) : les liens sont listés pour être réaffectés d'abord. Les favoris et les liens moteur/embrayage
(tables de liaison) sont supprimés avec elle.

    python manage.py supprimer_marque --marque "Bugatti (ancien)" --all --dry-run
    python manage.py supprimer_marque --marque "Bugatti (ancien)" --all
"""
from django.contrib.admin.utils import NestedObjects
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django_tenants.utils import get_public_schema_name, tenant_context

from societe.models import Societe
from voiture.voiture_marque.models import MarqueFavorite, VoitureMarque
from voiture.voiture_modele.models import VoitureModele

AUTORISES = {m._meta.label for m in (VoitureMarque, VoitureModele, MarqueFavorite)}


class _DryRun(Exception):
    pass


class Command(BaseCommand):
    help = "Supprime une ou plusieurs marques et leurs modèles (refuse si elles sont encore utilisées)."

    def add_arguments(self, parser):
        parser.add_argument("--marque", action="append", dest="marques", default=[], required=True,
                            help="Nom exact de la marque, casse ignorée (répétable)")
        parser.add_argument("--tenant", action="append", dest="tenants", default=[], help="schema_name (répétable)")
        parser.add_argument("--all", action="store_true", help="Tous les tenants (hors public)")
        parser.add_argument("--dry-run", action="store_true", help="Simulation : rien n'est supprimé")

    def handle(self, *args, **opts):
        if opts["all"]:
            tenants = list(Societe.objects.exclude(schema_name=get_public_schema_name()))
        elif opts["tenants"]:
            tenants = list(Societe.objects.filter(schema_name__in=opts["tenants"]))
            if len(tenants) != len(set(opts["tenants"])):
                raise CommandError("Tenant introuvable")
        else:
            raise CommandError("Préciser --tenant <schema> ou --all")

        for tenant in tenants:
            with tenant_context(tenant):
                try:
                    with transaction.atomic():
                        for nom in opts["marques"]:
                            marques = list(VoitureMarque.objects.filter(nom_marque__iexact=nom))
                            if not marques:
                                self.stdout.write(f"[{tenant.schema_name}] « {nom} » : absente")
                            for marque in marques:
                                self._supprimer(tenant, marque)
                        if opts["dry_run"]:
                            raise _DryRun
                except _DryRun:
                    self.stdout.write(self.style.WARNING(f"[{tenant.schema_name}] Simulation : rien n'est supprimé."))

    @staticmethod
    def _liens(objets):
        """Objets extérieurs (hors marque, modèles, favoris et tables de liaison) touchés par la suppression."""
        if not objets:
            return set()
        collecteur = NestedObjects(using="default")
        collecteur.collect(objets)
        liens = {f"{p._meta.verbose_name} ({p._meta.label})" for p in collecteur.protected
                 if p._meta.label not in AUTORISES}
        for model in collecteur.model_objs:
            if model._meta.label not in AUTORISES and not model._meta.auto_created:
                liens.add(f"{model._meta.verbose_name} ({model._meta.label}, {len(collecteur.data.get(model, ()))})")
        return liens

    def _supprimer(self, tenant, marque):
        # Le lien modèle -> marque est en PROTECT : on vérifie puis supprime d'abord les modèles, ensuite la marque.
        modeles = list(VoitureModele.objects.filter(voiture_marque=marque))
        liens = self._liens(modeles) | self._liens([marque])
        if liens:
            self.stdout.write(self.style.ERROR(
                f"[{tenant.schema_name}] « {marque.nom_marque} » conservée, encore utilisée : {', '.join(sorted(liens))}"))
            return
        for modele in modeles:
            modele.delete()
        marque.delete()
        self.stdout.write(self.style.SUCCESS(
            f"[{tenant.schema_name}] « {marque.nom_marque} » supprimée ({len(modeles)} modèles)"))

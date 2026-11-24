"""
Supprime les modèles d'une ou plusieurs marques qui n'ont pas de date de production (annee_debut vide),
ou, avec --nom-commence-par, ceux dont le nom de modèle commence par un texte donné (dates ou non),
ou, avec --modele, ceux dont le nom de modèle est exactement celui donné (dates ou non, casse ignorée).

Un modèle encore utilisé (véhicule, recharge ou tout autre lien autre qu'un simple lien moteur/embrayage)
n'est PAS supprimé : il est listé pour être réaffecté à la bonne version puis supprimé à la main.

    python manage.py supprimer_modeles_sans_date --marque BMW --all --dry-run
    python manage.py supprimer_modeles_sans_date --marque BMW --all
    python manage.py supprimer_modeles_sans_date --marque Peugeot --nom-commence-par "Peugeot " --all
    python manage.py supprimer_modeles_sans_date --marque Mercedes-Benz --modele A-Class --modele B-Class --all
"""
from django.contrib.admin.utils import NestedObjects
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q
from django_tenants.utils import get_public_schema_name, tenant_context

from societe.models import Societe
from voiture.voiture_modele.models import VoitureModele


class _DryRun(Exception):
    pass


class Command(BaseCommand):
    help = "Supprime les modèles sans date de production d'une ou plusieurs marques (hors modèles utilisés)."

    def add_arguments(self, parser):
        parser.add_argument("--marque", action="append", dest="marques", default=[], required=True,
                            help="Nom de la marque (répétable), ex. --marque BMW")
        parser.add_argument("--tenant", action="append", dest="tenants", default=[], help="schema_name (répétable)")
        parser.add_argument("--all", action="store_true", help="Tous les tenants (hors public)")
        parser.add_argument("--nom-commence-par", dest="prefixe", default="",
                            help="Cibler les modèles dont le nom commence par ce texte (au lieu de « sans date »)")
        parser.add_argument("--modele", action="append", dest="modeles", default=[],
                            help="Nom exact du modèle à supprimer (répétable, casse ignorée), dates ou non")
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

        filtre_marque = Q()
        for m in opts["marques"]:
            filtre_marque |= Q(voiture_marque__nom_marque__iexact=m)

        if opts["prefixe"] and opts["modeles"]:
            raise CommandError("Utiliser --nom-commence-par ou --modele, pas les deux")
        filtre_noms = Q()
        for nom in opts["modeles"]:
            filtre_noms |= Q(nom_modele__iexact=nom)

        for tenant in tenants:
            supprimes, gardes = 0, []
            with tenant_context(tenant):
                if opts["prefixe"]:
                    critere = Q(nom_modele__istartswith=opts["prefixe"])
                elif opts["modeles"]:
                    critere = filtre_noms
                else:
                    critere = Q(annee_debut__isnull=True)
                qs = (VoitureModele.objects.filter(filtre_marque, critere)
                      .select_related("voiture_marque").order_by("nom_modele", "nom_variante"))
                try:
                    with transaction.atomic():
                        for modele in qs:
                            liens = self._liens_bloquants(modele)
                            if liens:
                                gardes.append(f"{modele.nom_modele} {modele.nom_variante or ''} ({', '.join(liens)})")
                                continue
                            modele.delete()
                            supprimes += 1
                        if opts["dry_run"]:
                            raise _DryRun
                except _DryRun:
                    self.stdout.write(self.style.WARNING(f"[{tenant.schema_name}] Simulation : rien n'est supprimé."))
            self.stdout.write(self.style.SUCCESS(
                f"[{tenant.schema_name}] supprimés : {supprimes} | conservés car utilisés : {len(gardes)}"))
            for ligne in gardes:
                self.stdout.write(f"   à réaffecter : {ligne}")

    @staticmethod
    def _liens_bloquants(modele):
        """Objets qui seraient supprimés ou bloqueraient la suppression (hors tables de liaison M2M)."""
        collecteur = NestedObjects(using="default")
        collecteur.collect([modele])
        liens = {p._meta.verbose_name for p in collecteur.protected}
        for model in collecteur.model_objs:
            if model is not VoitureModele and not model._meta.auto_created:
                liens.add(str(model._meta.verbose_name))
        return sorted(liens)

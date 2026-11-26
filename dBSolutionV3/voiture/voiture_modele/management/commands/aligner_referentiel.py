"""
Aligne la base d'un ou plusieurs tenants sur le référentiel des fichiers de données
(voiture/voiture_modele/data/marques.py, modeles.py et data/detail/).

Pour chaque marque présente dans MODELES, supprime les modèles de la base qui ne correspondent plus à aucune
ligne du référentiel (même nom de modèle, génération, phase et variante, casse ignorée). Un modèle encore utilisé
(véhicule, recharge ou tout autre lien autre qu'un lien moteur/embrayage) n'est PAS supprimé : il est listé
pour être réaffecté.

Avec --supprimer-marques-absentes, supprime aussi les marques qui ne figurent plus ni dans MARQUES ni dans MODELES
(et leurs modèles), sauf si elles sont encore utilisées.

Ensuite, lancer create_moteur puis populate_voitures pour créer les modèles et liens manquants.

    python manage.py aligner_referentiel --all --dry-run
    python manage.py aligner_referentiel --all --supprimer-marques-absentes
    python manage.py aligner_referentiel --tenant carscosts --marque Toyota --dry-run
"""
from django.contrib.admin.utils import NestedObjects
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django_tenants.utils import get_public_schema_name, tenant_context

from societe.models import Societe
from voiture.voiture_marque.models import MarqueFavorite, VoitureMarque
from voiture.voiture_modele.data.marques import MARQUES
from voiture.voiture_modele.data.modeles import MODELES
from voiture.voiture_modele.models import VoitureModele

AUTORISES = {m._meta.label for m in (VoitureMarque, VoitureModele, MarqueFavorite)}


class _DryRun(Exception):
    pass


def _t(valeur):
    return (valeur or "").strip().casefold()


class Command(BaseCommand):
    help = "Supprime les modèles (et, en option, les marques) absents du référentiel, hors éléments utilisés."

    def add_arguments(self, parser):
        parser.add_argument("--tenant", action="append", dest="tenants", default=[], help="schema_name (répétable)")
        parser.add_argument("--all", action="store_true", help="Tous les tenants (hors public)")
        parser.add_argument("--marque", action="append", dest="marques", default=[],
                            help="Limiter à une ou plusieurs marques (répétable)")
        parser.add_argument("--supprimer-marques-absentes", action="store_true",
                            help="Supprimer aussi les marques absentes du référentiel (hors marques utilisées)")
        parser.add_argument("--detail", action="store_true", help="Lister chaque modèle supprimé")
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

        filtre = {m.casefold() for m in opts["marques"]}
        cles = {}
        for marque, lignes in MODELES.items():
            if filtre and marque.casefold() not in filtre:
                continue
            cles.setdefault(marque.casefold(), set()).update(
                (_t(d["modele"]), _t(d.get("generation")), _t(d.get("phase")), _t(d.get("variante"))) for d in lignes)
        connues = {m.casefold() for m in MARQUES} | {m.casefold() for m in MODELES}

        for tenant in tenants:
            st = {"modeles": 0, "marques": 0}
            gardes = []
            with tenant_context(tenant):
                try:
                    with transaction.atomic():
                        for marque in VoitureMarque.objects.order_by("nom_marque"):
                            nom = marque.nom_marque.casefold()
                            if nom in cles:
                                self._aligner_marque(marque, cles[nom], st, gardes, opts["detail"])
                            elif (opts["supprimer_marques_absentes"] and not filtre and nom not in connues):
                                self._supprimer_marque(marque, st, gardes)
                        if opts["dry_run"]:
                            raise _DryRun
                except _DryRun:
                    self.stdout.write(self.style.WARNING(f"[{tenant.schema_name}] Simulation : rien n'est supprimé."))
            self.stdout.write(self.style.SUCCESS(
                f"[{tenant.schema_name}] modèles supprimés : {st['modeles']} | marques supprimées : {st['marques']} "
                f"| conservés car utilisés : {len(gardes)}"))
            for ligne in gardes:
                self.stdout.write(f"   à réaffecter : {ligne}")

    def _aligner_marque(self, marque, cles, st, gardes, detail):
        for modele in VoitureModele.objects.filter(voiture_marque=marque).order_by("nom_modele", "nom_variante"):
            cle = (_t(modele.nom_modele), _t(modele.generation), _t(modele.phase), _t(modele.nom_variante))
            if cle in cles:
                continue
            liens = self._liens([modele])
            libelle = f"{marque.nom_marque} {modele.nom_modele} {modele.generation or ''} {modele.nom_variante or ''}".strip()
            if liens:
                gardes.append(f"{libelle} ({', '.join(sorted(liens))})")
                continue
            modele.delete()
            st["modeles"] += 1
            if detail:
                self.stdout.write(f"   supprimé : {libelle}")

    def _supprimer_marque(self, marque, st, gardes):
        modeles = list(VoitureModele.objects.filter(voiture_marque=marque))
        liens = self._liens(modeles) | self._liens([marque])
        if liens:
            gardes.append(f"marque « {marque.nom_marque} » ({', '.join(sorted(liens))})")
            return
        for modele in modeles:
            modele.delete()
        st["modeles"] += len(modeles)
        marque.delete()
        st["marques"] += 1
        self.stdout.write(f"   marque supprimée : {marque.nom_marque} ({len(modeles)} modèles)")

    @staticmethod
    def _liens(objets):
        """Objets extérieurs (hors marque, modèles, favoris et tables de liaison) touchés par la suppression."""
        if not objets:
            return set()
        collecteur = NestedObjects(using="default")
        collecteur.collect(objets)
        liens = {str(p._meta.verbose_name) for p in collecteur.protected if p._meta.label not in AUTORISES}
        for model in collecteur.model_objs:
            if model._meta.label not in AUTORISES and not model._meta.auto_created:
                liens.add(str(model._meta.verbose_name))
        return liens

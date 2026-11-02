"""
Script UNIQUE de peuplement du référentiel voitures : marques + modèles + liens moteurs.

Remplace : populate_marques / populate_carscosts / populate_campus / populate_rsrnurburg /
populatersrspa et create_modele / _all / _suite / _sup / _abarth (+ copies par tenant).

Données : voiture/voiture_modele/data/marques.py et voiture/voiture_modele/data/modeles.py

Exemples :
    python manage.py populate_voitures --tenant carscosts
    python manage.py populate_voitures --tenant campus --tenant rsrspa
    python manage.py populate_voitures --all
    python manage.py populate_voitures --tenant carscosts --marque Mini --dry-run

Les moteurs doivent exister dans le tenant (create_moteur) pour être liés ;
sinon ils sont signalés et le modèle est créé sans lien.
"""
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, ProgrammingError, connection, transaction
from django.db.models import Q
from django_tenants.utils import get_public_schema_name, tenant_context

from societe.models import Societe
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.data.marques import MARQUES
from voiture.voiture_modele.data.modeles import MODELES
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_moteur.models import MoteurVoiture

CHAMPS = {
    # clé des données -> champ du modèle
    "portes": "nombre_portes",
    "places": "nbre_places",
    "reservoir": "taille_reservoir",
    "batterie": "capacite_batterie",
    "annee_debut": "annee_debut",
    "mois_debut": "mois_debut",
    "annee_fin": "annee_fin",
    "mois_fin": "mois_fin",
    "remarques": "remarques",
}
DEFAUTS_CREATION = {"nombre_portes": 5, "nbre_places": 5, "taille_reservoir": 0}


def _filtre_texte(champ, valeur):
    if valeur:
        return Q(**{f"{champ}__iexact": valeur})
    return Q(**{f"{champ}__isnull": True}) | Q(**{champ: ""})


class Command(BaseCommand):
    help = "Peuple marques, modèles (génération, phase, variante, années) et liens moteurs pour un ou plusieurs tenants."

    def add_arguments(self, parser):
        parser.add_argument("--tenant", action="append", dest="tenants", default=[],
                            help="schema_name du tenant (répétable)")
        parser.add_argument("--all", action="store_true", help="Tous les tenants (hors public)")
        parser.add_argument("--marque", action="append", dest="marques", default=[],
                            help="Limiter à une ou plusieurs marques")
        parser.add_argument("--sans-moteurs", action="store_true", help="Ne pas lier les moteurs")
        parser.add_argument("--dry-run", action="store_true", help="Simulation : tout est annulé à la fin")

    def handle(self, *args, **opts):
        if opts["all"]:
            tenants = list(Societe.objects.exclude(schema_name=get_public_schema_name()))
        elif opts["tenants"]:
            tenants = []
            for s in opts["tenants"]:
                try:
                    tenants.append(Societe.objects.get(schema_name=s))
                except Societe.DoesNotExist:
                    raise CommandError(f"Tenant '{s}' introuvable")
        else:
            raise CommandError("Préciser --tenant <schema> ou --all")

        filtre = {m.casefold() for m in opts["marques"]}
        marques = [m for m in MARQUES if not filtre or m.casefold() in filtre]
        modeles = {m: L for m, L in MODELES.items() if not filtre or m.casefold() in filtre}

        for tenant in tenants:
            with tenant_context(tenant):
                with connection.cursor() as c:
                    colonnes = {col.name for col in connection.introspection.get_table_description(
                        c, VoitureModele._meta.db_table)}
                if not {"generation", "phase"} <= colonnes:
                    raise CommandError(
                        f"[{tenant.schema_name}] migration 0014 non appliquée (colonnes generation/phase absentes). "
                        "Lancer d'abord : python manage.py migrate_schemas"
                    )
                try:
                    with transaction.atomic():
                        stats = self._peupler(tenant, marques, modeles, not opts["sans_moteurs"])
                        if opts["dry_run"]:
                            raise _DryRun(stats)
                except _DryRun as d:
                    stats = d.stats
                    self.stdout.write(self.style.WARNING("Simulation : aucune modification enregistrée."))
            self.stdout.write(self.style.SUCCESS(
                f"[{tenant.schema_name}] marques +{stats['marques']} | modèles +{stats['crees']} "
                f"/ maj {stats['maj']} | liens moteurs +{stats['liens']} | erreurs {stats['erreurs']}"
            ))
            if stats["moteurs_absents"]:
                self.stdout.write(self.style.WARNING(
                    f"  Moteurs introuvables (lancer create_moteur ?) : {', '.join(sorted(stats['moteurs_absents']))}"
                ))

    def _peupler(self, tenant, marques, modeles, lier_moteurs):
        st = {"marques": 0, "crees": 0, "maj": 0, "liens": 0, "erreurs": 0, "moteurs_absents": set()}

        # 1) Marques
        cache_marques = {}
        for nom in sorted(set(marques) | set(modeles)):
            obj = VoitureMarque.objects.filter(nom_marque__iexact=nom, societe=tenant).first()
            if obj is None:
                obj = VoitureMarque.objects.create(nom_marque=nom, societe=tenant)
                st["marques"] += 1
            cache_marques[nom] = obj

        # 2) Modèles
        for nom_marque, liste in modeles.items():
            marque = cache_marques[nom_marque]
            for d in liste:
                try:
                    with transaction.atomic():
                        self._modele(tenant, marque, d, st, lier_moteurs)
                except (ValidationError, IntegrityError) as e:
                    st["erreurs"] += 1
                    self.stdout.write(self.style.ERROR(f"  {nom_marque} {d.get('modele')} {d.get('variante') or ''} : {e}"))
        return st

    def _modele(self, tenant, marque, d, st, lier_moteurs):
        qs = VoitureModele.objects.filter(voiture_marque=marque, nom_modele__iexact=d["modele"])
        for cle, champ in (("generation", "generation"), ("phase", "phase"), ("variante", "nom_variante")):
            qs = qs.filter(_filtre_texte(champ, d.get(cle)))
        obj = qs.first()

        valeurs = {champ: d[cle] for cle, champ in CHAMPS.items() if d.get(cle) is not None}
        if obj is None:
            obj = VoitureModele(
                voiture_marque=marque, societe=tenant, nom_modele=d["modele"],
                generation=d.get("generation"), phase=d.get("phase"), nom_variante=d.get("variante"),
                **{**DEFAUTS_CREATION, **valeurs},
            )
            obj.save()
            st["crees"] += 1
        else:
            change = [c for c, v in valeurs.items() if getattr(obj, c) != v]
            if change:
                for c in change:
                    setattr(obj, c, valeurs[c])
                obj.save()
                st["maj"] += 1

        if lier_moteurs:
            for motoriste, code in d.get("moteurs", []):
                moteur = MoteurVoiture.objects.filter(motoriste__iexact=motoriste, code_moteur__iexact=code).first()
                if moteur is None:
                    st["moteurs_absents"].add(f"{motoriste} {code}")
                    continue
                if not moteur.voitures_modeles.filter(pk=obj.pk).exists():
                    moteur.voitures_modeles.add(obj)
                    st["liens"] += 1


class _DryRun(Exception):
    def __init__(self, stats):
        self.stats = stats

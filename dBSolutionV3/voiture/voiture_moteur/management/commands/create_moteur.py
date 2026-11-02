"""
Crée / met à jour le référentiel moteurs pour un ou plusieurs tenants.

Données : voiture/voiture_moteur/data/moteurs.py (trié, dédoublonné, valeurs normalisées).

Exemples :
    python manage.py create_moteur --all
    python manage.py create_moteur --tenant carscosts --dry-run
    python manage.py create_moteur --tenant campus --motoriste Porsche

Ensuite : python manage.py populate_voitures --all  (pour créer les liens modèle → moteur)
"""
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django_tenants.utils import get_public_schema_name, tenant_context

from societe.models import Societe
from voiture.voiture_moteur.data.moteurs import MOTEURS
from voiture.voiture_moteur.models import MoteurVoiture, TypeCarburant, TypeDistribution, TypeMoteur
from maintenance.choices import HuileEtat

SPECS = ["type_moteur", "carburant", "cylindree_l", "distribution", "nombre_cylindres", "puissance_ch",
         "puissance_tr_min", "couple_nm", "couple_tr_min", "qualite_huile", "quantite_huile_l",
         "intervalle_km_entretien"]
CHOIX = {
    "type_moteur": set(TypeMoteur.values),
    "carburant": set(TypeCarburant.values),
    "distribution": set(TypeDistribution.values),
    "qualite_huile": set(HuileEtat.values) | {"10W30"},
}


class _DryRun(Exception):
    pass


class Command(BaseCommand):
    help = "Crée ou met à jour les moteurs du référentiel pour un ou plusieurs tenants."

    def add_arguments(self, parser):
        parser.add_argument("--tenant", action="append", dest="tenants", default=[])
        parser.add_argument("--all", action="store_true", help="Tous les tenants (hors public)")
        parser.add_argument("--motoriste", action="append", dest="motoristes", default=[])
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        if opts["all"]:
            tenants = list(Societe.objects.exclude(schema_name=get_public_schema_name()))
        elif opts["tenants"]:
            tenants = list(Societe.objects.filter(schema_name__in=opts["tenants"]))
            manquants = set(opts["tenants"]) - {t.schema_name for t in tenants}
            if manquants:
                raise CommandError(f"Tenant(s) introuvable(s) : {', '.join(sorted(manquants))}")
        else:
            raise CommandError("Préciser --tenant <schema> ou --all")

        filtre = {m.casefold() for m in opts["motoristes"]}
        donnees = {m: L for m, L in MOTEURS.items() if not filtre or m.casefold() in filtre}

        for tenant in tenants:
            st = {"crees": 0, "maj": 0, "corriges": 0}
            with tenant_context(tenant):
                try:
                    with transaction.atomic():
                        self._peupler(donnees, st)
                        if opts["dry_run"]:
                            raise _DryRun
                except _DryRun:
                    self.stdout.write(self.style.WARNING("Simulation : aucune modification enregistrée."))
            self.stdout.write(self.style.SUCCESS(
                f"[{tenant.schema_name}] moteurs +{st['crees']} | maj {st['maj']} | "
                f"valeurs invalides corrigées sur moteurs d'exemplaires {st['corriges']}"
            ))

    def _peupler(self, donnees, st):
        for motoriste, liste in donnees.items():
            for d in liste:
                specs = {k: d[k] for k in SPECS}
                if specs["quantite_huile_l"] is not None:
                    specs["quantite_huile_l"] = Decimal(str(specs["quantite_huile_l"])).quantize(Decimal("0.01"))
                tous = MoteurVoiture.objects.filter(motoriste__iexact=motoriste, code_moteur__iexact=d["code_moteur"])
                catalogue = tous.filter(voitures_exemplaires__isnull=True).order_by("date_creation").first()

                if catalogue is None:
                    # bulk_create : contourne save() qui recopierait les specs d'un moteur d'exemplaire existant
                    MoteurVoiture.objects.bulk_create([MoteurVoiture(motoriste=motoriste, code_moteur=d["code_moteur"], **specs)])
                    st["crees"] += 1
                else:
                    diff = {k: v for k, v in specs.items() if getattr(catalogue, k) != v}
                    if diff:
                        MoteurVoiture.objects.filter(pk=catalogue.pk).update(**diff)
                        st["maj"] += 1

                # moteurs liés à des exemplaires : on ne corrige que les valeurs hors choix
                for champ, valides in CHOIX.items():
                    n = tous.exclude(**{f"{champ}__in": valides}).update(**{champ: specs[champ]})
                    st["corriges"] += n

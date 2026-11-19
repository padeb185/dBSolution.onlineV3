"""
Crée / met à jour le référentiel des boîtes de vitesses pour un ou plusieurs tenants.

Données : voiture/voiture_boite/data/boites.py (dédoublonné, valeurs normalisées).
Les boîtes du référentiel ne sont liées à aucun modèle ni exemplaire : le lien se fait à la
saisie d'un véhicule (ou plus tard via populate_voitures).

Exemples :
    python manage.py create_boite_vitesse --all
    python manage.py create_boite_vitesse --tenant carscosts --dry-run
    python manage.py create_boite_vitesse --tenant campus --fabricant ZF
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django_tenants.utils import get_public_schema_name, tenant_context

from maintenance.choices import HuileBoiteEtat
from societe.models import Societe
from voiture.voiture_boite.data.boites import BOITES
from voiture.voiture_boite.models import TypeBoite, VoitureBoite

SPECS = ["type_de_boite", "nombre_rapport", "qualite_huile", "quantite_huile_l", "intervalle_entretien_km", "remarques"]
CHOIX = {
    "type_de_boite": set(TypeBoite.values),
    "qualite_huile": set(HuileBoiteEtat.values),
}


class _DryRun(Exception):
    pass


class Command(BaseCommand):
    help = "Crée ou met à jour les boîtes de vitesses du référentiel pour un ou plusieurs tenants."

    def add_arguments(self, parser):
        parser.add_argument("--tenant", action="append", dest="tenants", default=[])
        parser.add_argument("--all", action="store_true", help="Tous les tenants (hors public)")
        parser.add_argument("--fabricant", action="append", dest="fabricants", default=[])
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

        filtre = {f.casefold() for f in opts["fabricants"]}
        donnees = {f: L for f, L in BOITES.items() if not filtre or f.casefold() in filtre}

        for tenant in tenants:
            st = {"crees": 0, "maj": 0}
            with tenant_context(tenant):
                try:
                    with transaction.atomic():
                        self._peupler(donnees, st)
                        if opts["dry_run"]:
                            raise _DryRun
                except _DryRun:
                    self.stdout.write(self.style.WARNING("Simulation : aucune modification enregistrée."))
            self.stdout.write(self.style.SUCCESS(
                f"[{tenant.schema_name}] boîtes de vitesses +{st['crees']} | maj {st['maj']}"
            ))

    def _peupler(self, donnees, st):
        for fabricant, liste in donnees.items():
            for d in liste:
                specs = {k: d.get(k) for k in SPECS}
                specs["remarques"] = specs["remarques"] or None
                for champ, valides in CHOIX.items():
                    if specs[champ] not in valides:
                        specs[champ] = "CONSTRUCTEUR" if champ == "qualite_huile" else TypeBoite.AUTOMATIQUE
                # Boîte du référentiel = boîte non liée à un exemplaire
                catalogue = (VoitureBoite.objects
                             .filter(fabricant__iexact=fabricant, nom_du_type__iexact=d["nom_du_type"],
                                     voitures_exemplaires__isnull=True)
                             .order_by("date_creation").first())
                if catalogue is None:
                    VoitureBoite.objects.create(fabricant=fabricant, nom_du_type=d["nom_du_type"], numero_boite=1,
                                                **specs)
                    st["crees"] += 1
                else:
                    diff = {k: v for k, v in specs.items() if getattr(catalogue, k) != v and v is not None}
                    # Les remarques saisies par le garage ne sont pas écrasées
                    if catalogue.remarques:
                        diff.pop("remarques", None)
                    if diff:
                        VoitureBoite.objects.filter(pk=catalogue.pk).update(**diff)
                        st["maj"] += 1

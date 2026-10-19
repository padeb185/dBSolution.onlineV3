"""
Rattachement des interventions orphelines (sans maintenance) à leur maintenance.
Cause : certaines vues de création ne liaient pas l'intervention (boîte auto, ABS, boîte manuelle)
et les formulaires « modifier » vidaient le lien. Utilisé par la commande reparer_maintenances
et automatiquement à la facturation d'une maintenance sans intervention liée.
"""
import re
from functools import lru_cache
from pathlib import Path

from django.apps import apps


def modeles_intervention():
    from maintenance.models import Maintenance
    for rel in Maintenance._meta.related_objects:
        m = rel.related_model
        if hasattr(m, "generer_rapport_remplacement") and rel.field.name == "maintenance":
            yield m


@lru_cache(maxsize=None)
def types_du_modele(modele):
    """Types de maintenance créés par l'app du modèle (lus dans ses fichiers Python)."""
    from maintenance.models import Maintenance
    app = apps.get_containing_app_config(modele.__module__)
    noms = set()
    for f in Path(app.path).glob("*.py"):
        try:
            noms.update(re.findall(r"TypeMaintenance\.([A-Z0-9_]+)", f.read_text(encoding="utf-8")))
        except Exception:
            pass
    return frozenset(getattr(Maintenance.TypeMaintenance, n) for n in noms if hasattr(Maintenance.TypeMaintenance, n))


def _kilometrages(obj):
    vals = set()
    for f in obj._meta.concrete_fields:
        if (f.name.startswith(("kilometrage", "km_")) or f.name == "kilometres_chassis") and "variation" not in f.name:
            v = getattr(obj, f.name, None)
            try:
                vals.add(int(v))
            except (TypeError, ValueError):
                pass
    return vals


def _date(obj):
    for nom in ("date", "date_intervention", "created_at", "date_creation"):
        v = getattr(obj, nom, None)
        if v:
            return v.date() if hasattr(v, "date") else v
    return None


def score(obj, maintenance):
    s = 0
    if _kilometrages(obj) & {maintenance.kilometres_chassis or -1, maintenance.kilometres_total or -1}:
        s += 2
    d = _date(obj)
    if d and maintenance.date_intervention == d:
        s += 1
    return s


def rattacher_maintenance(maintenance, dry=False):
    """Maintenance sans intervention : rattache l'intervention orpheline correspondante. Retourne les objets liés."""
    lies = []
    if not maintenance.voiture_exemplaire_id:
        return lies
    for modele in modeles_intervention():
        types = types_du_modele(modele)
        if types and maintenance.type_maintenance not in types:
            continue
        try:
            if modele.objects.filter(maintenance=maintenance).exists():
                continue
            orphelins = list(modele.objects.filter(maintenance__isnull=True,
                                                    voiture_exemplaire_id=maintenance.voiture_exemplaire_id))
        except Exception:
            continue
        if not orphelins:
            continue
        orphelins.sort(key=lambda o: score(o, maintenance), reverse=True)
        meilleur = orphelins[0]
        if score(meilleur, maintenance) == 0 and len(orphelins) > 1:
            continue  # ambigu : on ne devine pas
        if not dry:
            modele.objects.filter(pk=meilleur.pk).update(maintenance=maintenance)
            meilleur.maintenance_id = maintenance.pk
        lies.append(meilleur)
    return lies

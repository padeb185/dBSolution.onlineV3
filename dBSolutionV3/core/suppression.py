from django.db import router
from django.db.models import ProtectedError, RestrictedError
from django.db.models.deletion import Collector


def _grouper(objets_par_modele):
    return [
        (model._meta.verbose_name_plural, objs)
        for model, objs in objets_par_modele.items()
        if objs
    ]


def analyser_suppression(obj):
    """
    Simule la suppression de `obj` et retourne un dict :
    - bloquants : objets en PROTECT / RESTRICT qui empêchent la suppression
    - supprimes : objets qui seraient supprimés en cascade
    - modifies  : objets conservés mais dont le lien sera mis à NULL (SET_NULL)
    Chaque valeur est une liste de (verbose_name_plural, [objets]).
    """
    collector = Collector(using=router.db_for_write(obj.__class__, instance=obj))

    try:
        collector.collect([obj])
    except (ProtectedError, RestrictedError) as e:
        bloquants = getattr(e, "protected_objects", None) or getattr(e, "restricted_objects", [])
        groupes = {}
        for o in bloquants:
            groupes.setdefault(o.__class__, []).append(o)
        return {"bloquants": _grouper(groupes), "supprimes": [], "modifies": []}

    # Cascade : collector.data + collector.fast_deletes
    supprimes = {}
    for model, instances in collector.data.items():
        if model is obj.__class__:
            continue
        supprimes.setdefault(model, []).extend(instances)

    for qs in collector.fast_deletes:
        model = qs.model
        if model._meta.auto_created:  # tables intermédiaires M2M : seulement des liens
            continue
        supprimes.setdefault(model, []).extend(qs)

    # SET_NULL / SET_DEFAULT / SET(...)
    modifies = {}
    for (field, _value), lots in collector.field_updates.items():
        for lot in lots:
            modifies.setdefault(field.model, []).extend(lot)

    return {
        "bloquants": [],
        "supprimes": _grouper(supprimes),
        "modifies": _grouper(modifies),
    }
"""
Étiquette (VERT / JAUNE / ROUGE) figée au moment de la maintenance.

Chaque intervention (check-up, polish, freins…) porte son propre champ « tag »
(ou « tag_xxx ») et une ForeignKey « maintenance ». L'étiquette de l'intervention
peut être modifiée plus tard ; on veut garder celle enregistrée au moment de la
maintenance. Au premier enregistrement d'une intervention liée, on copie donc son
étiquette dans Maintenance.tag_enregistre — une seule fois : si une valeur est
déjà présente, elle n'est plus jamais écrasée.
"""
from django.db.models import ForeignKey


def _champ_tag(model):
    for champ in model._meta.concrete_fields:
        if champ.name == "tag" or champ.name.startswith("tag_"):
            return champ.name
    return None


def modeles_interventions():
    """[(modèle, nom du champ tag)] des interventions liées à une Maintenance."""
    from django.apps import apps
    from .models import Maintenance

    resultat = []
    for model in apps.get_models():
        if model is Maintenance:
            continue
        try:
            champ = model._meta.get_field("maintenance")
        except Exception:
            continue
        if not isinstance(champ, ForeignKey) or champ.related_model is not Maintenance:
            continue
        nom_tag = _champ_tag(model)
        if nom_tag:
            resultat.append((model, nom_tag))
    return resultat


def figer_tag(instance, nom_tag):
    """Copie l'étiquette de l'intervention sur sa maintenance si elle n'est pas encore figée."""
    from .models import Maintenance

    maintenance_id = getattr(instance, "maintenance_id", None)
    valeur = getattr(instance, nom_tag, None)
    if not maintenance_id or valeur not in Maintenance.Tag.values:
        return
    # update() : pas de signal ; le filtre isnull garantit qu'on ne réécrit jamais
    Maintenance.objects.filter(pk=maintenance_id, tag_enregistre__isnull=True).update(tag_enregistre=valeur)


def connecter_signaux():
    from django.db.models.signals import post_save

    for model, nom_tag in modeles_interventions():
        def _apres_sauvegarde(sender, instance, _nom_tag=nom_tag, **kwargs):
            try:
                figer_tag(instance, _nom_tag)
            except Exception:
                # ne jamais bloquer l'enregistrement d'une intervention
                pass

        post_save.connect(
            _apres_sauvegarde, sender=model, weak=False,
            dispatch_uid=f"maintenance_tag_fige_{model._meta.label_lower}",
        )


def remplir_existantes():
    """Remplit tag_enregistre des maintenances existantes avec l'étiquette actuelle de leur intervention."""
    from django.db import transaction
    from .models import Maintenance

    total = 0
    for model, nom_tag in modeles_interventions():
        try:
            with transaction.atomic():  # savepoint : un modèle en erreur n'annule pas les autres
                lignes = list(
                    model._default_manager
                    .filter(maintenance__isnull=False, maintenance__tag_enregistre__isnull=True)
                    .order_by("pk")
                    .values_list("maintenance_id", nom_tag)
                )
                for maintenance_id, valeur in lignes:
                    if valeur in Maintenance.Tag.values:
                        total += Maintenance.objects.filter(
                            pk=maintenance_id, tag_enregistre__isnull=True
                        ).update(tag_enregistre=valeur)
        except Exception:
            continue
    return total

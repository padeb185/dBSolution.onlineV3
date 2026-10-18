"""
Liaison entre une fiche main-d'œuvre et l'intervention qui l'a créée.

Les interventions (check-up, freins, culasse, ESP…) créent leur fiche MainDoeuvre avec
seulement le technicien, le temps et le taux : le véhicule et le kilométrage restaient vides.
On les reprend de l'intervention liée (champ ForeignKey « main_oeuvre » de l'intervention).
"""
from django.db.models import ForeignKey


def modeles_interventions():
    """Modèles qui ont un ForeignKey « main_oeuvre » vers MainDoeuvre et un véhicule."""
    from django.apps import apps
    from .models import MainDoeuvre

    modeles = []
    for model in apps.get_models():
        try:
            champ = model._meta.get_field("main_oeuvre")
            model._meta.get_field("voiture_exemplaire")
        except Exception:
            continue
        if isinstance(champ, ForeignKey) and champ.related_model is MainDoeuvre:
            modeles.append(model)
    return modeles


def intervention_liee(main_oeuvre):
    """Première intervention qui pointe vers cette fiche main-d'œuvre (ou None)."""
    for model in modeles_interventions():
        obj = model._default_manager.filter(main_oeuvre=main_oeuvre).first()
        if obj is not None:
            return obj
    return None


def kilometrage_intervention(obj):
    """Kilométrage saisi pour l'intervention (kilometrage_xxx), sinon kilomètres châssis."""
    for champ in obj._meta.concrete_fields:
        nom = champ.name
        if nom.startswith("kilometrage_") and nom != "kilometrage_variation":
            valeur = getattr(obj, nom, None)
            if valeur:
                return int(valeur)
    valeur = getattr(obj, "kilometres_chassis", None)
    return int(valeur) if valeur else None


def libelle_intervention(obj):
    maintenance = getattr(obj, "maintenance", None)
    if maintenance is not None and getattr(maintenance, "type_maintenance", None):
        return maintenance.get_type_maintenance_display()
    return str(obj._meta.verbose_name)


def synchroniser(main_oeuvre, obj=None):
    """Reprend véhicule, kilométrage et société de l'intervention. Retourne l'intervention."""
    from .models import MainDoeuvre

    if main_oeuvre is None:
        return None
    obj = obj or intervention_liee(main_oeuvre)
    if obj is None:
        return None

    valeurs = {}
    vehicule_id = getattr(obj, "voiture_exemplaire_id", None)
    if vehicule_id and main_oeuvre.voiture_exemplaire_id != vehicule_id:
        valeurs["voiture_exemplaire_id"] = vehicule_id
    km = kilometrage_intervention(obj)
    if km and main_oeuvre.kilometres_chassis != km:
        valeurs["kilometres_chassis"] = km
    if not main_oeuvre.societe_id:
        societe_id = getattr(obj, "tech_societe_id", None) or getattr(obj, "societe_id", None)
        if societe_id:
            valeurs["societe_id"] = societe_id

    if valeurs:
        # update() : pas de signal, pas de boucle avec la sauvegarde de l'intervention
        MainDoeuvre.objects.filter(pk=main_oeuvre.pk).update(**valeurs)
        for cle, valeur in valeurs.items():
            setattr(main_oeuvre, cle, valeur)
    return obj


def _apres_sauvegarde_intervention(sender, instance, **kwargs):
    mo_id = getattr(instance, "main_oeuvre_id", None)
    if not mo_id:
        return
    try:
        synchroniser(instance.main_oeuvre, instance)
    except Exception:
        # ne jamais bloquer l'enregistrement d'une intervention
        pass


def connecter_signaux():
    from django.db.models.signals import post_save

    for model in modeles_interventions():
        post_save.connect(
            _apres_sauvegarde_intervention, sender=model,
            dispatch_uid=f"maindoeuvre_sync_{model._meta.label_lower}",
        )


def tag_intervention(obj):
    """Libellé du tag (VERT / JAUNE / ROUGE) de l'intervention, quel que soit le nom du champ."""
    if obj is None:
        return ""
    for champ in obj._meta.concrete_fields:
        if champ.name == "tag" or champ.name.startswith("tag_"):
            methode = getattr(obj, f"get_{champ.name}_display", None)
            if methode:
                return methode()
    return ""

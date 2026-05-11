def sync_maintenance(instance, maintenance_type):
    if not instance.maintenance:
        return

    instance.maintenance.type_maintenance = maintenance_type

    if instance.voiture_exemplaire:
        instance.maintenance.voiture_exemplaire = instance.voiture_exemplaire

    instance.maintenance.save(update_fields=[
        "type_maintenance",
        "voiture_exemplaire"
    ])
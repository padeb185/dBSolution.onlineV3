def sync_maintenance(instance, maintenance_type):
    maintenance = getattr(instance, "maintenance", None)

    if maintenance is None:
        return

    maintenance.type_maintenance = maintenance_type

    if getattr(instance, "voiture_exemplaire", None):
        maintenance.voiture_exemplaire = instance.voiture_exemplaire

    maintenance.save(
        update_fields=[
            "type_maintenance",
            "voiture_exemplaire",
        ]
    )
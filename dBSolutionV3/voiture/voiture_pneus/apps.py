from django.apps import AppConfig


class VoiturePneusConfig(AppConfig):
    name = 'voiture.voiture_pneus'

    def ready(self):
        # Remplacements de trains enregistrés depuis les maintenances
        from django.apps import apps
        from django.db.models.signals import post_save, pre_delete
        from . import services_trains

        def _apres_enregistrement(sender, instance, raw=False, **kwargs):
            if not raw:
                services_trains.synchroniser_depuis_maintenance(instance)

        def _avant_suppression(sender, instance, **kwargs):
            services_trains.annuler_depuis_maintenance(instance)

        for label in services_trains.MAINTENANCES_PNEUS:
            try:
                modele = apps.get_model(label)
            except LookupError:
                continue
            post_save.connect(_apres_enregistrement, sender=modele, weak=False,
                              dispatch_uid=f"trains_pneus_save_{label}")
            pre_delete.connect(_avant_suppression, sender=modele, weak=False,
                               dispatch_uid=f"trains_pneus_delete_{label}")

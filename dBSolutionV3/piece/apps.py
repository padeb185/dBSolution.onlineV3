from django.apps import AppConfig


class PieceConfig(AppConfig):
    name = 'piece'

    def ready(self):
        from . import intervention  # noqa: F401  (signal post_save des codes OEM / EAN)

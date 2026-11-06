"""Compte chaque requête (tenant, statut HTTP, durée) pour le monitoring."""
import logging
import time

logger = logging.getLogger(__name__)


class MonitoringMiddleware:
    IGNORES = ("/static/", "/media/", "/favicon", "/__reload__/", "/monitoring/api/")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        chemin = request.path_info or "/"
        if any(p in chemin for p in self.IGNORES):
            return self.get_response(request)

        debut = time.perf_counter()
        response = self.get_response(request)
        try:
            from .collecte import enregistrer
            schema = getattr(getattr(request, "tenant", None), "schema_name", None)
            if chemin.startswith("/api/v1/"):
                # Application des particuliers : requêtes servies dans leur tenant (hors préfixe /tenant/)
                from django.conf import settings
                schema = getattr(settings, "PARTICULIERS_SCHEMA", "particuliers")
            enregistrer(schema, response.status_code, int((time.perf_counter() - debut) * 1000))
        except Exception:
            logger.exception("Monitoring : enregistrement de la requête impossible")
        return response

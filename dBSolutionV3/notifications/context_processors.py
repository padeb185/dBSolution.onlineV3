def notifications(request):
    """Nombre de notifications non lues (badge de l'en-tête)."""
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {}
    from django.db import connection
    from django_tenants.utils import get_public_schema_name
    if getattr(connection, "schema_name", None) == get_public_schema_name():
        return {}
    try:
        from .models import Notification
        return {"notifications_non_lues": Notification.objects.filter(destinataire=user, lue=False).count()}
    except Exception:
        return {}

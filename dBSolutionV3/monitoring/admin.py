from django.contrib import admin
from django.db import connection

from .models import MesureServeur, TraficTenant


class _PublicSeulement(admin.ModelAdmin):
    def has_module_permission(self, request):
        return connection.schema_name == "public" and request.user.is_superuser

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(TraficTenant)
class TraficTenantAdmin(_PublicSeulement):
    list_display = ("tranche", "schema_name", "requetes", "erreurs_4xx", "erreurs_5xx", "duree_ms_max")
    list_filter = ("schema_name",)
    date_hierarchy = "tranche"


@admin.register(MesureServeur)
class MesureServeurAdmin(_PublicSeulement):
    list_display = ("horodatage", "cpu", "ram_pourcent", "disque_pourcent", "charge_1", "en_ligne", "sessions")
    date_hierarchy = "horodatage"

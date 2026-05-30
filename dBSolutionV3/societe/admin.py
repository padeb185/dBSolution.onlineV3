from django.contrib import admin
from django.db import connection
from .models import Societe
from .admin_forms import SocieteAdminForm


@admin.register(Societe)
class SocieteAdmin(admin.ModelAdmin):
    form = SocieteAdminForm
    list_display = ("nom", "directeur", "numero_tva", "site")
    search_fields = ("nom", "directeur", "numero_tva")
    ordering = ("nom",)
    readonly_fields = ("id_societe",)


    def has_module_permission(self, request):
        return connection.schema_name == "public"

    def has_view_permission(self, request, obj=None):
        return connection.schema_name == "public"

    def has_add_permission(self, request):
        return connection.schema_name == "public"

    def has_change_permission(self, request, obj=None):
        return connection.schema_name == "public"

    def has_delete_permission(self, request, obj=None):
        return connection.schema_name == "public"
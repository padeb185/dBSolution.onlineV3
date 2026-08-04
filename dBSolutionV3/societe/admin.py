from django.contrib import admin
from django.db import connection

from .models import Societe
from .admin_forms import SocieteAdminForm


@admin.register(Societe)
class SocieteAdmin(admin.ModelAdmin):
    form = SocieteAdminForm

    list_display = (
        "nom",
        "directeur",
        "adresse",
        "numero_tva",
        "iban",
        "site",
        "schema_name",
        "max_utilisateurs",
        "nombre_utilisateurs",
        "paid_until",
        "on_trial",
    )

    list_display_links = (
        "nom",
    )

    list_editable = (
        "directeur",
        "adresse",
        "numero_tva",
        "iban",
        "site",
        "max_utilisateurs",
        "paid_until",
        "on_trial",
    )

    search_fields = (
        "nom",
        "directeur__username",
        "numero_tva",
        "iban",
        "schema_name",
    )

    ordering = ("nom",)

    readonly_fields = (
        "id_societe",
        "nombre_utilisateurs",
    )

    fieldsets = (
        ("Informations société", {
            "fields": (
                "id_societe",
                "nom",
                "directeur",
                "adresse",
                "numero_tva",
                "iban",
                "site",
            )
        }),

        ("Tenant", {
            "fields": (
                "schema_name",
                "max_utilisateurs",
                "nombre_utilisateurs",
                "paid_until",
                "on_trial",
            )
        }),
    )

    def nombre_utilisateurs(self, obj):
        if not obj.pk:
            return 0

        return obj.utilisateurs.count()

    nombre_utilisateurs.short_description = "Utilisateurs"

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
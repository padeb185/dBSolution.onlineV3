from django.contrib import admin
from .models import VoiturePneusHistorique
from .admin_forms import VoiturePneusHistoriqueAdminForm


@admin.register(VoiturePneusHistorique)
class VoiturePneusHistoriqueAdmin(admin.ModelAdmin):
    form = VoiturePneusHistoriqueAdminForm

    list_display = (
        "voiture_pneus",
        "type_pneus",
        "pneus_avant",
        "pneus_arriere",
        "kilometres_effectues",
        "numero_remplacement",
        "date_remplacement",
    )

    list_filter = (
        "type_pneus",
        "date_remplacement",
    )

    search_fields = (
        "voiture_pneus__voiture__immatriculation",
        "pneus_avant",
        "pneus_arriere",
    )

    ordering = (
        "-date_remplacement",
        "voiture_pneus",
    )

    readonly_fields = (
        "date_remplacement",
    )

    fieldsets = (
        ("Véhicule", {
            "fields": (
                "voiture_pneus",
            )
        }),
        ("Pneumatiques", {
            "fields": (
                "type_pneus",
                "pneus_avant",
                "pneus_arriere",
            )
        }),
        ("Historique d'utilisation", {
            "fields": (
                "kilometres_effectues",
                "numero_remplacement",
                "date_remplacement",
            )
        }),
    )

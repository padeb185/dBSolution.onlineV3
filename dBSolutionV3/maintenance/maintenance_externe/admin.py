from django.contrib import admin

from .models import MaintenanceExterne


@admin.register(MaintenanceExterne)
class MaintenanceExterneAdmin(admin.ModelAdmin):
    list_display = ("date_facture", "voiture_exemplaire", "type_maintenance", "garage", "total_htva", "total_tva", "total_tvac")
    list_filter = ("type_maintenance", "pays", "garage")
    search_fields = ("numero_facture", "voiture_exemplaire__immatriculation", "garage__nom")
    readonly_fields = ("tva_pieces", "tva_main_oeuvre", "total_pieces_tvac", "total_main_oeuvre_tvac",
                       "total_htva", "total_tva", "total_tvac")

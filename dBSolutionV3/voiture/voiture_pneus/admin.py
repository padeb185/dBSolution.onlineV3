from django.contrib import admin
from .models import VoiturePneus


@admin.register(VoiturePneus)
class VoiturePneusAdmin(admin.ModelAdmin):
    list_display = (
        "manufacturier",
        "emplacement",
        "type_pneus",
        "pneus_largeur",
        "pneus_hauteur",
        "pneus_jante",
        "kilometre_pneus_av",
        "kilometre_pneus_ar",
        "date_remplacement",
    )
    list_filter = ("type_pneus", "emplacement")
    search_fields = ("manufacturier",)

    fieldsets = (
        ("Informations générales", {
            "fields": ("manufacturier", "emplacement", "type_pneus")
        }),
        ("Dimensions", {
            "fields": ("pneus_largeur", "pneus_hauteur", "pneus_jante")
        }),
        ("Kilométrage", {
            "fields": ("kilometre_pneus_av", "kilometre_pneus_ar", "date_remplacement")
        }),
        ("Statistiques", {
            "fields": ("nombre_trains_av", "nombre_trains_ar")
        }),
        ("Système", {
            "fields": ("created_at",)
        }),
    )
    readonly_fields = ("kilometre_pneus_av", "kilometre_pneus_ar", "date_remplacement", "created_at")

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


from .models import TrainPneus


@admin.register(TrainPneus)
class TrainPneusAdmin(admin.ModelAdmin):
    list_display = (
        "voiture_exemplaire", "position", "numero", "monte", "type_pneus",
        "libelle_pneus", "actif", "est_monte", "km_effectues", "date_montage", "date_remplacement",
    )
    list_filter = ("position", "monte", "actif", "est_monte", "type_pneus")
    search_fields = ("voiture_exemplaire__immatriculation", "libelle_pneus")
    autocomplete_fields = ()
    readonly_fields = ("km_effectues", "created_at", "updated_at")

from django.contrib import admin
from .models import VoiturePneus
from voiture.voiture_pneus_historique.models import VoiturePneusHistorique  # import direct du modèle

class VoiturePneusHistoriqueInline(admin.TabularInline):
    model = VoiturePneusHistorique  # obligatoire
    extra = 0
    can_delete = False
    readonly_fields = (
        "numero_remplacement",
        "type_pneus",
        "pneus_avant",
        "pneus_arriere",
        "kilometres_effectues",
        "date_remplacement",
    )


@admin.register(VoiturePneus)
class VoiturePneusAdmin(admin.ModelAdmin):
    list_display = (
        "type_pneus",
        "pneus_avant",
        "pneus_arriere",
        "kilometre_pneus",
        "date_remplacement",
    )
    list_filter = ("type_pneus", "fournisseur")
    search_fields = (
        "voiture_exemplaire__immatriculation",
        "voiture_modele__nom",
    )
    readonly_fields = (
        "kilometre_pneus",
        "date_remplacement",
        "created_at",
    )
    inlines = [VoiturePneusHistoriqueInline]

    fieldsets = (
        ("Véhicule", {
            "fields": ("voiture_modele", "voiture_exemplaire", "fournisseur")
        }),
        ("Monte actuelle", {
            "fields": ("type_pneus", "pneus_avant", "pneus_arriere")
        }),
        ("Kilométrage", {
            "fields": ("kilometre_pneus", "date_remplacement", "kilometre_remplacement")
        }),
        ("Statistiques", {
            "fields": ("nombre_trains_av", "nombre_trains_ar")
        }),
        ("Système", {
            "fields": ("created_at",)
        }),
    )

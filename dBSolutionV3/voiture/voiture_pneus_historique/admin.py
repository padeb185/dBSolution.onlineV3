from django.contrib import admin
from .models import VoiturePneusHistorique

@admin.register(VoiturePneusHistorique)
class VoiturePneusHistoriqueAdmin(admin.ModelAdmin):
    list_display = (
        "voiture_pneus",
        "type_pneus",
        "get_emplacement",
        "get_pneus_largeur",
        "kilometres_effectues",
        "numero_remplacement",
        "date_remplacement",
    )

    list_filter = (
        "type_pneus",
        "voiture_pneus__emplacement",  # filtre via relation
        "date_remplacement",
    )

    search_fields = (
        "voiture_pneus__voitures_exemplaires__immatriculation",
        "voiture_pneus__pneus_largeur",
    )

    readonly_fields = (
        "date_remplacement",
    )

    fieldsets = (
        ("Véhicule", {
            "fields": ("voiture_pneus",)
        }),
        ("Pneumatiques", {
            "fields": (
                "type_pneus",
                "pneus_avant_largeur",
                "pneus_arriere_largeur",
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

    # Méthodes pour afficher champs du modèle lié
    def get_emplacement(self, obj):
        return obj.voiture_pneus.emplacement
    get_emplacement.short_description = "Emplacement"

    def get_pneus_largeur(self, obj):
        # Retourne la largeur selon l’emplacement
        if obj.voiture_pneus.emplacement == "avant":
            return obj.pneus_avant_largeur
        elif obj.voiture_pneus.emplacement == "arriere":
            return obj.pneus_arriere_largeur
        else:  # avant et arrière
            return f"{obj.pneus_avant_largeur} / {obj.pneus_arriere_largeur}"
    get_pneus_largeur.short_description = "Largeur"

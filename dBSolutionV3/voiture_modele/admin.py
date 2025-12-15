from django.contrib import admin
from .models import VoitureModele
from .admin_forms import VoitureModeleAdminForm


@admin.register(VoitureModele)
class VoitureModeleAdmin(admin.ModelAdmin):
    form = VoitureModeleAdminForm

    list_display = (
        "nom_modele",
        "nom_variante",
        "voiture_marque",
        "societe",
        "nombre_portes",
        "nbre_places",
        "taille_reservoir",
        "created_at",
    )

    list_filter = (
        "voiture_marque",
        "societe",
        "nombre_portes",
        "nbre_places",
    )

    search_fields = (
        "nom_modele",
        "nom_variante",
        "voiture_marque__nom",
    )

    ordering = (
        "voiture_marque",
        "nom_modele",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Relations", {
            "fields": (
                "voiture_marque",
                "societe",
            )
        }),
        ("Informations du modèle", {
            "fields": (
                "nom_modele",
                "nom_variante",
                "nombre_portes",
                "nbre_places",
                "couleur",
                "taille_reservoir",
            )
        }),
        ("Audit", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

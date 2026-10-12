from django.contrib import admin

from .models import Diagnostic


@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ("code_defaut", "piece_libelle", "voiture_exemplaire")
    list_filter = ("piece_defaut",)
    search_fields = (
        "code_defaut", "piece_defaut_autre",
        "voiture_exemplaire__immatriculation",
        "voiture_exemplaire__voiture_marque__nom_marque",
        "voiture_exemplaire__voiture_modele__nom_modele",
    )

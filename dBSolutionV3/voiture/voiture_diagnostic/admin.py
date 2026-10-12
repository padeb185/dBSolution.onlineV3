from django.contrib import admin

from .models import Diagnostic


@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ("code_defaut", "piece_defaut", "voiture_marque", "voiture_modele")
    list_filter = ("voiture_marque",)
    search_fields = ("code_defaut", "piece_defaut", "voiture_modele__nom_modele", "voiture_marque__nom_marque")

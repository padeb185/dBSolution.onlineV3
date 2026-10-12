from django.contrib import admin

from .models import Diagnostic, DiagnosticCode


class DiagnosticCodeInline(admin.TabularInline):
    model = DiagnosticCode
    extra = 1
    fields = ("code_defaut", "piece_defaut", "piece_defaut_autre")


@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ("voiture_exemplaire", "date_diagnostic", "kilometrage", "liste_codes")
    list_filter = ("date_diagnostic",)
    search_fields = (
        "codes__code_defaut", "codes__piece_defaut_autre",
        "voiture_exemplaire__immatriculation",
        "voiture_exemplaire__voiture_marque__nom_marque",
        "voiture_exemplaire__voiture_modele__nom_modele",
    )
    inlines = [DiagnosticCodeInline]

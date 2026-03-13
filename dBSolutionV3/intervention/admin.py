from django.contrib import admin
from .models import Intervention, InterventionItem, MainOeuvre, Peinture

# Inline pour les pièces
class InterventionItemInline(admin.TabularInline):
    model = InterventionItem
    extra = 1

# Inline pour la main d'oeuvre
class MainOeuvreInline(admin.TabularInline):
    model = MainOeuvre
    extra = 1

# Inline pour la peinture
class PeintureInline(admin.TabularInline):
    model = Peinture
    extra = 1

# Admin pour l'intervention
@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ("id", "societe", "voiture_exemplaire", "total_htva", "total_tva", "total_tvac")
    inlines = [InterventionItemInline, MainOeuvreInline, PeintureInline]
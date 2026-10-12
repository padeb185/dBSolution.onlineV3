from django.contrib import admin

from .models import GarageOfficiel


@admin.register(GarageOfficiel)
class GarageOfficielAdmin(admin.ModelAdmin):
    list_display = ("nom", "voiture_marque", "groupe", "numero_tva", "telephone", "email")
    list_filter = ("groupe", "voiture_marque")
    search_fields = ("nom", "numero_tva", "email", "adresse__ville")

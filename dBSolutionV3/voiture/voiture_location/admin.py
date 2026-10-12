from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("voiture_exemplaire", "type_location", "lieu", "date_debut", "kilometrage", "prix")
    list_filter = ("type_location", "circuit")
    search_fields = ("voiture_exemplaire__immatriculation", "route")

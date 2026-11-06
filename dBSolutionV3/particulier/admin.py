from django.contrib import admin

from .models import Depense, Document, Entretien, Plein, Rappel, ReleveKilometrique, Vehicule


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ("marque", "modele", "immatriculation", "proprietaire", "archive")
    search_fields = ("marque", "modele", "immatriculation", "vin", "proprietaire__email")


for modele in (ReleveKilometrique, Plein, Entretien, Document, Rappel, Depense):
    admin.site.register(modele)

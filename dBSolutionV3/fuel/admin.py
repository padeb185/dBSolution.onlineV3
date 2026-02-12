from django.contrib import admin
from django.db.models import Sum
from .models import Fuel


@admin.register(Fuel)
class FuelAdmin(admin.ModelAdmin):
    list_display = ('voiture_exemplaire', 'date', 'litres', 'total_litres_vehicule')

    # Méthode pour afficher le total des litres pour ce véhicule
    def total_litres_vehicule(self, obj):
        return Fuel.total_litres_mois(obj.voiture_exemplaire)

    total_litres_vehicule.short_description = "Total Litres"

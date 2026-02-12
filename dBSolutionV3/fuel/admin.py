from django.contrib import admin
from django.db.models import Sum
from .models import Fuel

@admin.register(Fuel)
class FuelAdmin(admin.ModelAdmin):
    list_display = ('voiture_exemplaire', 'date', 'litres', 'total_litres_vehicule', 'total_prix_all')

    # Total des litres pour ce véhicule
    def total_litres_vehicule(self, obj):
        return Fuel.total_litres_mois(obj.voiture_exemplaire)
    total_litres_vehicule.short_description = "Total Litres"

    # Total du prix pour ce véhicule
    def total_prix_all(self, obj):
        return Fuel.objects.filter(voiture_exemplaire=obj.voiture_exemplaire).aggregate(total=Sum('prix_refuelling'))['total'] or 0
    total_prix_all.short_description = "Total Prix Litres"

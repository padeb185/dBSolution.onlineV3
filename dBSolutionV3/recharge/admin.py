from django.contrib import admin
from django.db.models import Sum
from recharge.models import Electricite


# Register your models here.
@admin.register(Electricite)
class ElectriciteAdmin(admin.ModelAdmin):
    list_display = ('voiture_exemplaire', 'date', 'kW', 'total_kW_vehicule', 'total_prix_all')

    # Total des litres pour ce véhicule
    def total_kW_vehicule(self, obj):
        return Electricite.total_kW_mois(obj.voiture_exemplaire)
    total_kW_vehicule.short_description = "Total Kilos Watts"

    # Total du prix pour ce véhicule
    def total_prix_all(self, obj):
        return Electricite.objects.filter(voiture_exemplaire=obj.voiture_exemplaire).aggregate(total=Sum('prix_recharge'))['total'] or 0
    total_prix_all.short_description = "Total Prix Kilos Watts"

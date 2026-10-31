from django.contrib import admin

from .models import Remorque


@admin.register(Remorque)
class RemorqueAdmin(admin.ModelAdmin):
    list_display = ("immatriculation", "nom", "type_remorque", "essieux", "freinee", "mma_kg", "actif")
    list_filter = ("type_remorque", "essieux", "freinee", "actif")
    search_fields = ("immatriculation", "nom", "marque", "modele", "numero_chassis")

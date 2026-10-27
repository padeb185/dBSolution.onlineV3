from django.contrib import admin

from .models import OccupationBox, Parking


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ("nom", "societe", "largeur_m", "longueur_m", "nombre_lignes", "nombre_emplacements")


@admin.register(OccupationBox)
class OccupationBoxAdmin(admin.ModelAdmin):
    list_display = ("parking", "code", "immatriculation", "vehicule", "depuis")

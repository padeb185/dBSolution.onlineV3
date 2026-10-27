from django.contrib import admin

from .models import VoitureJante


@admin.register(VoitureJante)
class VoitureJanteAdmin(admin.ModelAdmin):
    list_display = ("__str__", "matiere", "construction", "origine", "competition", "societe")
    list_filter = ("fabricant", "matiere", "construction", "origine", "competition")
    search_fields = ("nom_modele", "reference", "reference_ar")
    filter_horizontal = ("voitures_exemplaires", "voitures_modeles")

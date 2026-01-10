from django.contrib import admin
from .models import MoteurVoiture

@admin.register(MoteurVoiture)
class MoteurVoitureAdmin(admin.ModelAdmin):
    list_display = ("code_moteur", "motoriste", "cylindree_l", "type_moteur")
    search_fields = ("code_moteur", "motoriste")
    filter_horizontal = ("voitures_exemplaires", "voitures_modeles")

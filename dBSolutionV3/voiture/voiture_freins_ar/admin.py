from django.contrib import admin
from .models import VoitureFreinsAR

@admin.register(VoitureFreinsAR)
class VoitureFreinsARAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_voitures',
        'marque_disques_ar',
        'marque_plaquettes_ar',
        'taille_disque_ar',
        'epaisseur_disque_ar',
        'epaisseur_min_disque_ar',
        'plaquettes_ar',
    )
    search_fields = (
        'marque_disques_ar',
        'marque_plaquettes_ar',
        'voitures_exemplaires__nom',  # suppose que VoitureExemplaire a un champ 'nom'
    )
    list_filter = (
        'marque_disques_ar',
        'marque_plaquettes_ar',
    )
    filter_horizontal = ('voitures_exemplaires',)  # pratique pour M2M

    # Fonction pour afficher les voitures liées dans list_display
    def get_voitures(self, obj):
        return ", ".join([str(v) for v in obj.voitures_exemplaires.all()])
    get_voitures.short_description = "Voitures liées"

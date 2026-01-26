from django.contrib import admin
from .models import VoitureFreins

@admin.register(VoitureFreins)
class VoitureFreinsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_voitures',
        'marque_disques_av',
        'marque_plaquettes_av',
        'taille_disque_av',
        'epaisseur_disque_av',
        'epaisseur_min_disque_av',
        'plaquettes_av',
    )
    search_fields = (
        'marque_disques_av',
        'marque_plaquettes_av',
        'voitures_exemplaires__nom',  # suppose que VoitureExemplaire a un champ 'nom'
    )
    list_filter = (
        'marque_disques_av',
        'marque_plaquettes_av',
    )
    filter_horizontal = ('voitures_exemplaires',)  # pratique pour les M2M

    # Fonction pour afficher les voitures liées dans list_display
    def get_voitures(self, obj):
        return ", ".join([str(v) for v in obj.voitures_exemplaires.all()])
    get_voitures.short_description = "Voitures liées"


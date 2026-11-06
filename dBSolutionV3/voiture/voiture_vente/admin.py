from django.contrib import admin

from .models import VenteVehicule


@admin.register(VenteVehicule)
class VenteVehiculeAdmin(admin.ModelAdmin):
    list_display = ("numero", "exemplaire", "date_vente", "acheteur_nom", "regime_tva", "prix_htva", "prix_tvac", "statut")
    list_filter = ("statut", "regime_tva", "societe")
    search_fields = ("numero", "acheteur_nom", "exemplaire__immatriculation", "exemplaire__numero_vin")
    readonly_fields = ("numero", "statut", "prix_htva", "base_tva", "montant_tva", "prix_tvac",
                       "numero_note_credit", "date_annulation", "motif_annulation", "emise_le")

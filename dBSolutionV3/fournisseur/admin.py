from django.contrib import admin
from .models import Fournisseur, Facture
from .admin_forms import FournisseurForm, FactureForm

class FactureInline(admin.TabularInline):
    """Permet d’ajouter/modifier les factures directement depuis la page fournisseur"""
    model = Facture
    form = FactureForm
    extra = 1  # nombre de lignes vides supplémentaires
    readonly_fields = ('tva_a_payer', 'total_ttc')  # calcul automatique

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    form = FournisseurForm
    list_display = ('nom', 'pays', 'numero_tva', 'taux_tva', 'total_htva', 'total_tva', 'total_ttc')
    search_fields = ('nom', 'numero_tva', 'pays')
    ordering = ('nom',)
    inlines = [FactureInline]  # affiche les factures liées directement

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    form = FactureForm
    list_display = ('reference', 'fournisseur', 'montant_htva', 'tva_a_payer', 'total_ttc', 'date_facture')
    list_filter = ('fournisseur', 'date_facture')
    search_fields = ('reference', 'fournisseur__nom')
    readonly_fields = ('tva_a_payer', 'total_ttc')

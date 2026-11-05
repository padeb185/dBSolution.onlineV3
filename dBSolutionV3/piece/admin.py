from django.contrib import admin

from .models import FactureAchatStock, InventaireStock, LigneFactureAchatStock, LigneInventaire, MouvementStock, PieceUtilisee


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ("date", "piece", "type_mouvement", "quantite", "stock_apres", "facture")
    list_filter = ("type_mouvement",)


@admin.register(PieceUtilisee)
class PieceUtiliseeAdmin(admin.ModelAdmin):
    list_display = ("maintenance", "piece", "quantite", "prix_unitaire", "mouvement", "facture")


class LigneInventaireInline(admin.TabularInline):
    model = LigneInventaire
    extra = 0


@admin.register(InventaireStock)
class InventaireStockAdmin(admin.ModelAdmin):
    list_display = ("date", "categorie", "statut")
    inlines = [LigneInventaireInline]


class LigneFactureAchatStockInline(admin.TabularInline):
    model = LigneFactureAchatStock
    extra = 0
    readonly_fields = ("montant_htva", "montant_tva", "montant_tvac", "mouvement")


@admin.register(FactureAchatStock)
class FactureAchatStockAdmin(admin.ModelAdmin):
    list_display = ("date_facture", "numero_facture", "fournisseur", "total_htva", "total_tva", "total_tvac")
    readonly_fields = ("total_htva", "total_tva", "total_tvac")
    inlines = [LigneFactureAchatStockInline]

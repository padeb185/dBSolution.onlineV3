from django.contrib import admin

from .models import InventaireStock, LigneInventaire, MouvementStock, PieceUtilisee


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

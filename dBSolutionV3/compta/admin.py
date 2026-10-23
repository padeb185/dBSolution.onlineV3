from django.contrib import admin

from .models import (CompteTresorerie, FactureInstructeur, LigneFactureInstructeur, MouvementTresorerie,
                     ProfilInstructeur)


@admin.register(CompteTresorerie)
class CompteTresorerieAdmin(admin.ModelAdmin):
    list_display = ("nom", "type", "compte_pcmn", "iban", "date_ouverture", "solde_ouverture", "par_defaut", "actif")
    list_filter = ("type", "actif", "par_defaut")
    search_fields = ("nom", "iban", "compte_pcmn")


@admin.register(MouvementTresorerie)
class MouvementTresorerieAdmin(admin.ModelAdmin):
    list_display = ("date", "compte", "sens", "montant", "libelle", "compte_contrepartie", "piece")
    list_filter = ("sens", "compte")
    search_fields = ("libelle", "piece")
    date_hierarchy = "date"


@admin.register(ProfilInstructeur)
class ProfilInstructeurAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "nom_commercial", "numero_entreprise", "regime_tva", "accord_autofacturation")


class LigneFactureInstructeurInline(admin.TabularInline):
    model = LigneFactureInstructeur
    extra = 0


@admin.register(FactureInstructeur)
class FactureInstructeurAdmin(admin.ModelAdmin):
    list_display = ("numero", "reference_instructeur", "instructeur", "date_facture", "montant_tvac", "statut")
    list_filter = ("statut", "autofacturation")
    inlines = [LigneFactureInstructeurInline]

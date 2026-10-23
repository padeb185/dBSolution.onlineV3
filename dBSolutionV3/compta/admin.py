from django.contrib import admin

from .models import CompteTresorerie, MouvementTresorerie


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

from django.contrib import admin

from .models import AgendaTache


@admin.register(AgendaTache)
class AgendaTacheAdmin(admin.ModelAdmin):
    list_display = ("date", "type_maintenance", "voiture_exemplaire", "technicien", "tag", "statut", "prete_pour")
    list_filter = ("date", "type_maintenance", "tag", "statut")
    search_fields = ("voiture_exemplaire__immatriculation", "technicien__nom", "technicien__prenom", "prete_pour")
    date_hierarchy = "date"

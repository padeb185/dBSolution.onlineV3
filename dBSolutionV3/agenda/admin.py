from django.contrib import admin

from .models import AgendaTache


@admin.register(AgendaTache)
class AgendaTacheAdmin(admin.ModelAdmin):
    list_display = ("date", "type_maintenance", "voiture_exemplaire", "technicien", "tag", "statut", "prete_pour")
    list_filter = ("date", "type_maintenance", "tag", "statut")
    search_fields = ("voiture_exemplaire__immatriculation", "technicien__nom", "technicien__prenom", "prete_pour")
    date_hierarchy = "date"


from .models import AgendaLocation  # noqa: E402


@admin.register(AgendaLocation)
class AgendaLocationAdmin(admin.ModelAdmin):
    list_display = ("location", "kilometrage_avant", "kilometrage_apres", "sortie_effectuee", "retour_effectue", "tag_retour")
    list_filter = ("sortie_effectuee", "retour_effectue", "tag_retour")

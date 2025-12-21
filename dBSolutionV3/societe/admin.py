from django.contrib import admin
from .models import Societe
from .admin_forms import SocieteAdminForm

class SocieteAdmin(admin.ModelAdmin):
    form = SocieteAdminForm
    list_display = ('nom', 'directeur', 'numero_tva', 'site', 'adresse')
    search_fields = ('nom', 'directeur', 'numero_tva', 'adresse__ville')
    ordering = ('nom',)
    readonly_fields = ('id_societe',)  # UUID ne doit pas être modifiable
    list_filter = ('adresse__ville',)

# Enregistrement de l'admin


from django.contrib import admin
from .models import SocieteCliente
from .admin_forms import SocieteClienteForm

@admin.register(SocieteCliente)
class SocieteClienteAdmin(admin.ModelAdmin):
    form = SocieteClienteForm
    list_display = ('nom', 'directeur', 'numero_tva', 'societe', 'adresse', 'site')
    list_filter = ('societe', 'adresse')
    search_fields = ('nom', 'directeur', 'numero_tva')
    ordering = ('nom',)

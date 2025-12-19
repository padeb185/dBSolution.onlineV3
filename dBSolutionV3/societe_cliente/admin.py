from django.contrib import admin
from .models import SocieteCliente
from .admin_forms import SocieteClienteForm

@admin.register(SocieteCliente)
class SocieteClienteAdmin(admin.ModelAdmin):
    form = SocieteClienteForm
    list_display = ("nom", "numero_tva", "peppol_id", "code_pays", "is_active", "created_at")
    list_filter = ("is_active", "code_pays")
    search_fields = ("nom", "numero_tva", "peppol_id", "directeur", "email")
    ordering = ("nom",)
    readonly_fields = ("created_at",)

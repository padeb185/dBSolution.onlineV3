from django.contrib import admin

# Register your models here.


from .models import PaiementFacture  # noqa: E402


@admin.register(PaiementFacture)
class PaiementFactureAdmin(admin.ModelAdmin):
    list_display = ("facture", "date", "mode", "montant", "reference")
    list_filter = ("mode", "date")

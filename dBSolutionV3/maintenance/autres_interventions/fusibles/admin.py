from django.contrib import admin

from .models import FabricantFusible

# Fusibles et FusibleDetail sont enregistrés dans dBSolutionV3/admin.py


@admin.register(FabricantFusible)
class FabricantFusibleAdmin(admin.ModelAdmin):
    list_display = ("nom", "oem", "actif", "ordre")
    list_editable = ("oem", "actif", "ordre")
    search_fields = ("nom",)
    ordering = ("nom",)

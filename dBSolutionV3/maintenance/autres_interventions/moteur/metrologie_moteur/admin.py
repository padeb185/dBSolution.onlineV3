from django.contrib import admin

from .models import MesureCylindre, MesureTourillon, MetrologieMoteur


class MesureCylindreInline(admin.TabularInline):
    model = MesureCylindre
    extra = 0


class MesureTourillonInline(admin.TabularInline):
    model = MesureTourillon
    extra = 0


@admin.register(MetrologieMoteur)
class MetrologieMoteurAdmin(admin.ModelAdmin):
    list_display = ("id", "voiture_exemplaire", "kilometrage_metrologie", "nombre_cylindres", "cylindree_cm3", "tech_nom_technicien", "date")
    search_fields = ("voiture_exemplaire__immatriculation", "tech_nom_technicien")
    inlines = [MesureCylindreInline, MesureTourillonInline]

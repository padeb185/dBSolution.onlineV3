from django.contrib import admin

from .models import CasseMoteur, EssaiCylindre, PieceCassee


class PieceCasseeInline(admin.TabularInline):
    model = PieceCassee
    extra = 0


class EssaiCylindreInline(admin.TabularInline):
    model = EssaiCylindre
    extra = 0


@admin.register(CasseMoteur)
class CasseMoteurAdmin(admin.ModelAdmin):
    list_display = ("id", "voiture_exemplaire", "kilometrage_casse", "cause_probable", "decision", "tech_nom_technicien", "date")
    list_filter = ("cause_probable", "decision")
    search_fields = ("voiture_exemplaire__immatriculation", "tech_nom_technicien")
    inlines = [PieceCasseeInline, EssaiCylindreInline]

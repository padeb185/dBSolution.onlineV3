from django.contrib import admin

from .models import CasseBoite, EssaiRapport, PieceCasseeBoite


class PieceCasseeInline(admin.TabularInline):
    model = PieceCasseeBoite
    extra = 0


class EssaiRapportInline(admin.TabularInline):
    model = EssaiRapport
    extra = 0


@admin.register(CasseBoite)
class CasseBoiteAdmin(admin.ModelAdmin):
    list_display = ("id", "voiture_exemplaire", "kilometrage_casse", "cause_probable", "decision", "tech_nom_technicien", "date")
    list_filter = ("cause_probable", "decision")
    search_fields = ("voiture_exemplaire__immatriculation", "tech_nom_technicien")
    inlines = [PieceCasseeInline, EssaiRapportInline]

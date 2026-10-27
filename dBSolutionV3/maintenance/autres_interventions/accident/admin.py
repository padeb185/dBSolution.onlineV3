from django.contrib import admin

from .models import PieceAccident, RapportAccident


class PieceAccidentInline(admin.TabularInline):
    model = PieceAccident
    extra = 0


@admin.register(RapportAccident)
class RapportAccidentAdmin(admin.ModelAdmin):
    inlines = [PieceAccidentInline]
    list_display = ("voiture_exemplaire", "date_accident", "type_choc", "decision", "tag")
    list_filter = ("type_choc", "decision", "sur_piste")

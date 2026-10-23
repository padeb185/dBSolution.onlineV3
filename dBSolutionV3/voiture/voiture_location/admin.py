from django.contrib import admin

from .models import Location, LocationBox


class LocationBoxInline(admin.TabularInline):
    model = LocationBox
    extra = 0


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = [LocationBoxInline]
    list_display = ("voiture_exemplaire", "type_location", "lieu", "date_debut", "kilometrage", "prix")
    list_filter = ("type_location", "circuit")
    search_fields = ("voiture_exemplaire__immatriculation", "route")


from .models import ObjectifVente  # noqa: E402


@admin.register(ObjectifVente)
class ObjectifVenteAdmin(admin.ModelAdmin):
    list_display = ("vendeur", "annee", "mois", "montant_htva", "nombre_ventes")
    list_filter = ("annee", "vendeur")


from .models import InterdictionLocation  # noqa: E402


@admin.register(InterdictionLocation)
class InterdictionLocationAdmin(admin.ModelAdmin):
    list_display = ("motif", "voiture_exemplaire", "date_debut", "date_fin", "heure_debut", "heure_fin", "jours_semaine", "actif")
    list_filter = ("motif", "actif")

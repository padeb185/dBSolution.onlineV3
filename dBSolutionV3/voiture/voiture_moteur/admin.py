from django.contrib import admin
from .models import MoteurVoiture


@admin.register(MoteurVoiture)
class MoteurVoitureAdmin(admin.ModelAdmin):

    list_display = (
        "code_moteur",
        "motoriste",
        "type_moteur",
        "carburant",
        "cylindree_l",
        "puissance_ch",
        "boite",
        "numero_moteur",
        "intervalle_km_entretien",
        "created_at",
    )

    list_filter = (
        "type_moteur",
        "carburant",
        "distribution",
        "boite",
        "created_at",
    )

    search_fields = (
        "code_moteur",
        "motoriste",
    )

    ordering = ("-created_at",)

    filter_horizontal = (
        "voitures_modeles",
        "voitures_exemplaires",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Identification", {
            "fields": (
                "motoriste",
                "code_moteur",
                "type_moteur",
                "carburant",
            )
        }),

        ("Caractéristiques", {
            "fields": (
                "cylindree_l",
                "nombre_cylindres",
                "puissance_ch",
                "puissance_tr_min",
                "couple_nm",
                "couple_tr_min",
            )
        }),

        ("Technique", {
            "fields": (
                "distribution",
                "boite",
            )
        }),

        ("Huile", {
            "fields": (
                "qualite_huile",
                "quantite_huile_l",
            )
        }),

        ("Suivi moteur", {
            "fields": (
                "numero_moteur",
                "kilometres_chassis",
                "intervalle_km_entretien",
            )
        }),

        ("Relations", {
            "fields": (
                "voitures_modeles",
                "voitures_exemplaires",
            )
        }),

        ("Divers", {
            "fields": (
                "remarques",
                "created_at",
                "updated_at",
            )
        }),
    )
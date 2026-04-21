from django.contrib import admin
from .models import VoitureExemplaire


@admin.register(VoitureExemplaire)
class VoitureExemplaireAdmin(admin.ModelAdmin):
    list_display = (
        "immatriculation",
        "voiture_marque",
        "voiture_modele",
        "pays",
        "kilometres_chassis",
        "tag",
        "societe",
        "created_at",
    )

    list_filter = (
        "pays",
        "tag",
        "societe",
        "type_utilisation",
        "created_at",
    )

    search_fields = (
        "immatriculation",
        "numero_vin",
        "vin_simplifie",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "vin_simplifie",
        "annee_production",
        "variation_kilometres",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Identification", {
            "fields": (
                "societe",
                "voiture_marque",
                "voiture_modele",
                "immatriculation",
                "pays",
                "type_utilisation",
            )
        }),

        ("VIN & Production", {
            "fields": (
                "numero_vin",
                "vin_simplifie",
                "annee_production",
                "mois_production",
                "est_apres_2010",
            )
        }),

        ("Kilométrage", {
            "fields": (
                "kilometres_chassis",
                "kilometres_dernier_entretien",
                "variation_kilometres",
                "date_derniere_intervention",
            )
        }),

        ("Composants", {
            "fields": (
                "kilometres_moteur",
                "kilometres_remplacement_moteur",
                "kilometres_boite",
                "kilometres_remplacement_boite",
                "kilometres_embrayage",
                "kilometres_remplacement_embrayage",
            )
        }),

        ("Technique", {
            "fields": (
                "voiture_moteur",
                "voiture_boite",
                "voiture_embrayage",
                "numero_moteur",
            )
        }),

        ("Financier", {
            "fields": (
                "prix_achat",
                "assurance",
                "taxe_mise_en_circulation",
                "taxe_roulage",
            )
        }),

        ("Propriétaire", {
            "fields": (
                "client",
                "nombre_proprietaires",
                "part_proprietaires_pourcent",
            )
        }),

        ("Suivi", {
            "fields": (
                "last_maintained_by",
                "tag",
                "created_at",
                "updated_at",
            )
        }),
    )
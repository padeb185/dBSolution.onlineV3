from django.contrib import admin
from .models import VoitureExemplaire
from .admin_forms import VoitureExemplaireAdminForm


@admin.register(VoitureExemplaire)
class VoitureExemplaireAdmin(admin.ModelAdmin):
    form = VoitureExemplaireAdminForm

    list_display = (
        "immatriculation",
        "voiture_marque",
        "voiture_modele",
        "type_utilisation",
        "kilometres_total",
        "variation_kilometres",
        "date_derniere_intervention",
    )

    list_filter = (
        "voiture_marque",
        "type_utilisation",
        "annee_production",
    )

    search_fields = (
        "immatriculation",
        "numero_vin",
        "numero_moteur",
    )

    ordering = (
        "immatriculation",
    )

    readonly_fields = (
        "variation_kilometres",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "voiture_marque",
        "voiture_modele",
    )

    fieldsets = (
        ("Identification", {
            "fields": (
                "immatriculation",
                "numero_vin",
                "type_utilisation",

            )
        }),
        ("Marque & Modèle", {
            "fields": (
                "voiture_marque",
                "voiture_modele",
            )
        }),
        ("Kilométrage", {
            "fields": (
                "kilometres_chassis",
                "kilometres_total",
                "kilometres_derniere_intervention",
                "variation_kilometres",
                "date_derniere_intervention",
            )
        }),
        ("Production & Mise en circulation", {
            "fields": (
                "annee_production",
                "mois_production",
                "date_mise_en_circulation",
            )
        }),
        ("Moteur & Transmission", {
            "fields": (
                "numero_moteur",
                "kilometres_moteur",
                "nombre_moteurs",
                "kilometres_boite_vitesse",
                "nombre_boites_vitesse",
                "kilometres_embrayage",
                "nombre_embrayages",
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
        ("Propriété", {
            "fields": (
                "nombre_proprietaires",
                "part_proprietaires_pourcent",
            )
        }),
        ("Audit", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

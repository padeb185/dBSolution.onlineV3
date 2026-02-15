from django.contrib import admin
from django.utils.html import format_html


class AssurancePoliceAdmin(admin.ModelAdmin):

    list_display = (
        'numero_contrat',
        'voiture_exemplaire',
        'assurance',
        'type_couverture',
        'date_fin',
        'statut_couleur',
    )

    def statut_couleur(self, obj):
        if obj.est_expiree:
            color = "red"
            label = "Expirée"
        elif obj.expire_bientot:
            color = "orange"
            label = "Expire bientôt"
        else:
            color = "green"
            label = "Active"

        return format_html(
            '<span style="color:white;background-color:{};padding:3px 8px;border-radius:8px;">{}</span>',
            color,
            label
        )

    statut_couleur.short_description = "Statut"

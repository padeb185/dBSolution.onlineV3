# admin.py
from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ControleGeneral

# ---------------------------
# Formulaire Admin
# ---------------------------
class ControleGeneralForm(forms.ModelForm):
    class Meta:
        model = ControleGeneral
        fields = "__all__"
        widgets = {
            "remarques": forms.Textarea(attrs={"rows": 4, "cols": 40}),
        }

    def clean_kilometrage_checkup(self):
        km = self.cleaned_data.get("kilometrage_checkup")
        voiture = self.cleaned_data.get("voiture_exemplaire")
        if km is not None and voiture and km < voiture.kilometres_chassis:
            raise forms.ValidationError(_(
                f"Le kilométrage du check-up ({km}) "
                f"ne peut pas être inférieur au kilométrage actuel de la voiture ({voiture.kilometres_chassis})."
            ))
        return km

# ---------------------------
# Admin
# ---------------------------
@admin.register(ControleGeneral)
class ControleGeneralAdmin(admin.ModelAdmin):
    form = ControleGeneralForm

    list_display = (
        "maintenance",
        "voiture_exemplaire",
        "kilometrage_checkup",
        "date",
        "tech_nom_technicien",
        "tag",
    )
    list_filter = (
        "date",
        "tag",
        "tech_societe",
    )
    search_fields = (
        "maintenance__id",
        "voiture_exemplaire__immat",
        "tech_nom_technicien",
    )
    readonly_fields = ("date", "kilometres_chassis")

    fieldsets = (
        (_("Général"), {
            "fields": (
                "maintenance",
                "voiture_exemplaire",
                "kilometrage_checkup",
                "kilometres_chassis",
                "remarques",
                "tag",
            )
        }),
        (_("Technicien"), {
            "fields": (
                "tech_technicien",
                "tech_nom_technicien",
                "tech_role_technicien",
                "tech_societe",
            )
        }),
        (_("Essuie-glaces & Pare-brise"), {
            "fields": (
                "essuie_glace_av",
                "essuie_glace_ar",
                "balais_essuie_av",
                "balais_essuie_ar",
                "pare_brise_coups",
                "pare_brise_remplacer",
            )
        }),
        (_("Moteur & Transmission"), {
            "fields": (
                "moteur_fuite",
                "moteur_bruit",
                "moteur_perte",
                "moteur_casse",
                "moteur_niveau_huile_etat",
                "moteur_niveau_huile_quantite",
                "moteur_niveau_huile_qualite",
                "boite_fuite",
                "boite_bruit",
                "boite_embrayage",
                "boite_niveau_huile_etat",
                "boite_niveau_huile_quantite",
                "boite_niveau_huile_qualite",
            )
        }),
        (_("Pont"), {
            "fields": (
                "pont_fuite",
                "pont_bruit",
                "pont_jeu",
                "pont_niveau_huile_etat",
                "pont_niveau_huile_quantite",
                "pont_niveau_huile_qualite",
            )
        }),
        (_("Refroidissement"), {
            "fields": (
                "refroidissement_radiateur",
                "refroidissement_quantite",
                "refroidissement_qualite",
            )
        }),
        (_("Freins"), {
            "fields": (
                "freins_usure_plaquettes_av",
                "freins_plaquettes_remplacer_av",
                "freins_epaisseur_disques_av",
                "freins_fentes_disques_av",
                "freins_disques_remplacer_av",
                "freins_usure_plaquettes_ar",
                "freins_plaquettes_remplacer_ar",
                "freins_epaisseur_disques_ar",
                "freins_fentes_disques_ar",
                "freins_disques_remplacer_ar",
                "freins_fuites",
                "frein_liquide_frein_etat",
                "freins_remplacement_liquide_frein",
                "freins_specif_liquide_frein",
                "freins_quantite_liquide_frein",
            )
        }),
        (_("Direction"), {
            "fields": ("direction_fuite", "niveau_direction")
        }),
        (_("Bruits & Jeux"), {
            "fields": (
                "bruit_roulement_avd",
                "bruit_roulement_avg",
                "bruit_roulement_ard",
                "bruit_roulement_arg",
                "jeu_rotule_direction_avd",
                "jeu_rotule_direction_avg",
                "jeu_rotule_direction_ard",
                "jeu_rotule_direction_arg",
                # tu peux continuer avec tous les jeux de suspension
            )
        }),
        (_("Pneus & Pression"), {
            "fields": (
                "pneu_epaisseur_avd",
                "pneu_epaisseur_avg",
                "pneu_epaisseur_ard",
                "pneu_epaisseur_arg",
                "pneu_sidewall_avd",
                "pneu_sidewall_avg",
                "pneu_sidewall_ard",
                "pneu_sidewall_arg",
                "pneu_pression_bar_avd",
                "pneu_pression_bar_avg",
                "pneu_pression_bar_ard",
                "pneu_pression_bar_arg",
                "pneu_train_av",
                "pneu_train_ar",
            )
        }),
        (_("Phares"), {
            "fields": (
                "phares_reglages",
                "phares_avant",
                "phares_gros_phares",
                "phares_clignotants",
                "phares_recul",
                "phares_anti_brouillard_avant",
                "phares_anti_brouillard_arriere",
            )
        }),
        (_("Nettoyage extérieur"), {
            "fields": (
                "nettoyage_exterieur_traces_gomme",
                "nettoyage_exterieur_carrosserie",
                "nettoyage_exterieur_jantes",
                "nettoyage_exterieur_sechage",
            )
        }),
        (_("Nettoyage intérieur"), {
            "fields": (
                "nettoyage_interieur_vitres",
                "nettoyage_interieur_pare_brise",
                "nettoyage_interieur_aspirateur",
                "nettoyage_interieur_portes",
                "nettoyage_interieur_sieges",
                "nettoyage_interieur_carpettes",
                "nettoyage_interieur_tableau_de_bord",
                "nettoyage_interieur_plastiques",
            )
        }),
    )
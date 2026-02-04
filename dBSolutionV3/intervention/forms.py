# forms.py
from django import forms
from intervention.models import Intervention
from django.utils.translation import gettext_lazy as _

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        # On inclut tous les champs sauf l'ID automatique
        fields = [
            'carrosserie',
            'voiture_exemplaire',

            # Pièces carrosserie
            'pare_chocs', 'pare_chocs_prix', 'pare_chocs_quantite',
            'bouclier_av', 'bouclier_av_prix', 'bouclier_av_quantite',
            'bouclier_ar', 'bouclier_ar_prix', 'bouclier_ar_quantite',
            'pare_brise', 'pare_brise_prix', 'pare_brise_quantite',
            'vitre_porte_avd', 'vitre_porte_avd_prix', 'vitre_porte_avd_quantite',
            'vitre_porte_avg', 'vitre_porte_avg_prix', 'vitre_porte_avg_quantite',
            'vitre_porte_ard', 'vitre_porte_ard_prix', 'vitre_porte_ard_quantite',
            'vitre_porte_arg', 'vitre_porte_arg_prix', 'vitre_porte_arg_quantite',
            'lunette', 'lunette_prix', 'lunette_quantite',
            'retroviseur_d', 'retroviseur_d_prix', 'retroviseur_d_quantite',
            'retroviseur_g', 'retroviseur_g_prix', 'retroviseur_g_quantite',
            'aile_avd', 'aile_avd_prix', 'aile_avd_quantite',
            'aile_avg', 'aile_avg_prix', 'aile_avg_quantite',
            'aile_ard', 'aile_ard_prix', 'aile_ard_quantite',
            'aile_arg', 'aile_arg_prix', 'aile_arg_quantite',
            'elargisseur_aile_avd', 'elargisseur_aile_avd_prix', 'elargisseur_aile_avd_quantite',
            'elargisseur_aile_avg', 'elargisseur_aile_avg_prix', 'elargisseur_aile_avg_quantite',
            'elargisseur_aile_ard', 'elargisseur_aile_ard_prix', 'elargisseur_aile_ard_quantite',
            'elargisseur_aile_arg', 'elargisseur_aile_arg_prix', 'elargisseur_aile_arg_quantite',
            'bas_de_caisse_d', 'bas_de_caisse_d_prix', 'bas_de_caisse_d_quantite',
            'bas_de_caisse_g', 'bas_de_caisse_g_prix', 'bas_de_caisse_g_quantite',
            'support_radiateur', 'support_radiateur_prix', 'support_radiateur_quantite',
            'support_pare_choc', 'support_pare_choc_prix', 'support_pare_choc_quantite',
            'calandre', 'calandre_prix', 'calandre_quantite',
            'porte_avd', 'porte_avd_prix', 'porte_avd_quantite',
            'porte_avg', 'porte_avg_prix', 'porte_avg_quantite',
            'porte_ard', 'porte_ard_prix', 'porte_ard_quantite',
            'porte_arg', 'porte_arg_prix', 'porte_arg_quantite',
            'poignee_porte', 'poignee_porte_prix', 'poignee_porte_quantite',
            'coffre_haillon', 'coffre_haillon_prix', 'coffre_haillon_quantite',
            'joint_coffre', 'joint_coffre_prix', 'joint_coffre_quantite',
            'joint_porte_avd', 'joint_porte_avd_prix', 'joint_porte_avd_quantite',
            'joint_porte_avg', 'joint_porte_avg_prix', 'joint_porte_avg_quantite',
            'joint_porte_ard', 'joint_porte_ard_prix', 'joint_porte_ard_quantite',
            'joint_porte_arg', 'joint_porte_arg_prix', 'joint_porte_arg_quantite',
            'coquille_aile_avd', 'coquille_aile_avd_prix', 'coquille_aile_avd_quantite',
            'coquille_aile_avg', 'coquille_aile_avg_prix', 'coquille_aile_avg_quantite',
            'coquille_aile_ard', 'coquille_aile_ard_prix', 'coquille_aile_ard_quantite',
            'coquille_aile_arg', 'coquille_aile_arg_prix', 'coquille_aile_arg_quantite',
            'clips', 'clips_prix', 'clips_quantite',
            'visserie', 'visserie_prix', 'visserie_quantite',
            'capot', 'capot_prix', 'capot_quantite',
            'peinture_avant_gauche', 'peinture_avant_gauche_prix', 'peinture_avant_gauche_quantite',
            'peinture_avant_droite', 'peinture_avant_droite_prix', 'peinture_avant_droite_quantite',
            'peinture_arriere_gauche', 'peinture_arriere_gauche_prix', 'peinture_arriere_gauche_quantite',
            'peinture_face_avant', 'peinture_face_avant_prix', 'peinture_face_avant_quantite',
            'peinture_capot', 'peinture_capot_prix', 'peinture_capot_quantite',
            'peinture_arriere', 'peinture_arriere_prix', 'peinture_arriere_quantite',
            'peinture_complete', 'peinture_complete_prix', 'peinture_complete_quantite',
            'phare_avd', 'phare_avd_prix', 'phare_avd_quantite',
            'phare_avg', 'phare_avg_prix', 'phare_avg_quantite',
            'phare_ard', 'phare_ard_prix', 'phare_ard_quantite',
            'phare_arg', 'phare_arg_prix', 'phare_arg_quantite',
            'clignotant_avd', 'clignotant_avd_prix', 'clignotant_avd_quantite',
            'clignotant_avg', 'clignotant_avg_prix', 'clignotant_avg_quantite',
            'clignotant_ard', 'clignotant_ard_prix', 'clignotant_ard_quantite',
            'anti_brouillard_avd', 'anti_brouillard_avd_prix', 'anti_brouillard_avd_quantite',
            'anti_brouillard_avg', 'anti_brouillard_avg_prix', 'anti_brouillard_avg_quantite',
            'troisieme_feux_stop', 'troisieme_feux_stop_prix', 'troisieme_feux_stop_quantite',
            'capteur_recul', 'capteur_recul_prix', 'capteur_recul_quantite',

            # Montants
            'montant_devis',
            'montant_facture',
            'montant_total',
        ]

        widgets = {
            'carrosserie': forms.Select(attrs={'class': 'border rounded px-4 py-2 w-full'}),
            'voiture_exemplaire': forms.Select(attrs={'class': 'border rounded px-4 py-2 w-full'}),
        }

    # Optionnel : on peut ajouter une validation pour recalculer total
    def clean(self):
        cleaned_data = super().clean()
        total = 0
        for field in self.Meta.model._meta.fields:
            if field.name.endswith("_prix"):
                base = field.name.replace("_prix", "")
                if cleaned_data.get(base):
                    prix = cleaned_data.get(field.name) or 0
                    qty = cleaned_data.get(f"{base}_quantite") or 0
                    total += prix * qty
        cleaned_data['montant_total'] = total
        return cleaned_data

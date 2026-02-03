# carrosserie/forms.py
from django import forms
from .models import Carrosserie

class CarrosserieForm(forms.ModelForm):
    class Meta:
        model = Carrosserie
        fields = [
            'nom_societe', 'responsable_nom', 'responsable_prenom',
            'adresse', 'pays', 'telephone', 'email', 'numero_tva'
        ]



from django import forms
from .models import Intervention

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        # Inclure tous les champs sauf id (auto)
        fields = [
            "carrosserie",
            "pare_chocs", "pare_chocs_prix", "pare_chocs_quantite",
            "bouclier", "bouclier_prix", "bouclier_quantite",
            "pare_brise", "pare_brise_prix", "pare_brise_quantite",
            "vitre_porte", "vitre_porte_prix", "vitre_porte_quantite",
            "lunette", "lunette_prix", "lunette_quantite",
            "retroviseur", "retroviseur_prix", "retroviseur_quantite",
            "aile", "aile_prix", "aile_quantite",
            "elargisseur_aile", "elargisseur_aile_prix", "elargisseur_aile_quantite",
            "bas_de_caisse", "bas_de_caisse_prix", "bas_de_caisse_quantite",
            "support_radiateur", "support_radiateur_prix", "support_radiateur_quantite",
            "support_pare_choc", "support_pare_choc_prix", "support_pare_choc_quantite",
            "porte", "porte_prix", "porte_quantite",
            "poignee_porte", "poignee_porte_prix", "poignee_porte_quantite",
            "coffre_haillon", "coffre_haillon_prix", "coffre_haillon_quantite",
            "joint_coffre", "joint_coffre_prix", "joint_coffre_quantite",
            "joint_porte", "joint_porte_prix", "joint_porte_quantite",
            "coquille_aile", "coquille_aile_prix", "coquille_aile_quantite",
            "clips", "clips_prix", "clips_quantite",
            "visserie", "visserie_prix", "visserie_quantite",
            "capot", "capot_prix", "capot_quantite",
            "peinture_avant_gauche", "peinture_avant_gauche_prix", "peinture_avant_gauche_quantite",
            "peinture_avant_droite", "peinture_avant_droite_prix", "peinture_avant_droite_quantite",
            "peinture_arriere_gauche", "peinture_arriere_gauche_prix", "peinture_arriere_gauche_quantite",
            "peinture_face_avant", "peinture_face_avant_prix", "peinture_face_avant_quantite",
            "peinture_capot", "peinture_capot_prix", "peinture_capot_quantite",
            "peinture_arriere", "peinture_arriere_prix", "peinture_arriere_quantite",
            "peinture_complete", "peinture_complete_prix", "peinture_complete_quantite",
            "montant_devis", "montant_facture", "montant_total"
        ]
        widgets = {
            "carrosserie": forms.Select(attrs={"class": "form-select"}),
            **{f"{field}": forms.NumberInput(attrs={"class": "form-control"}) for field in [
                "pare_chocs_prix", "pare_chocs_quantite",
                "bouclier_prix", "bouclier_quantite",
                "pare_brise_prix", "pare_brise_quantite",
                # … tu peux répéter pour tous les _prix et _quantite
            ]}
        }

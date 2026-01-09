# moteur/forms.py
from django import forms
from .models import MoteurVoiture

class MoteurVoitureForm(forms.ModelForm):
    class Meta:
        model = MoteurVoiture
        # Tous les champs sauf id, voiture_modele, voiture_exemplaire, date_creation
        fields = [
            "type_moteur", "carburant", "cylindree_l", "distribution",
            "nombre_cylindres", "puissance_ch", "puissance_tr_min",
            "couple_nm", "couple_tr_min", "qualite_huile", "quantite_huile_l",
            "kilometrage_moteur", "numero_moteur", "intervalle_km_entretien"
        ]

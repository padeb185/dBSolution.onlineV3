from django import forms
from .models import VoitureMarque, MarqueFavorite
from django.conf import settings

class VoitureMarqueForm(forms.ModelForm):
    class Meta:
        model = VoitureMarque
        fields = ['nom_marque']
        widgets = {
            'nom_marque': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la marque',
            }),
        }
        error_messages = {
            'nom_marque': {
                'unique': "Cette marque existe déjà.",
                'max_length': "Le nom ne peut pas dépasser 50 caractères.",
                'min_length': "Le nom doit contenir au moins 2 caractères.",
            },
        }


class MarqueFavoriteForm(forms.ModelForm):
    class Meta:
        model = MarqueFavorite
        fields = ['marque']
        widgets = {
            'marque': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Permet de filtrer les marques disponibles selon l'utilisateur.
        """
        self.societe = kwargs.pop('societe', None)
        super().__init__(*args, **kwargs)
        if self.user and hasattr(self.user, "societe"):
            self.fields["voiture_marque"].queryset = VoitureMarque.objects.filter(
                societe=self.user.societe
            )
        else:
            self.fields["voiture_marque"].queryset = VoitureMarque.objects.none()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.societe:
            instance.societe = self.societe
        if commit:
            instance.save()
        return instance
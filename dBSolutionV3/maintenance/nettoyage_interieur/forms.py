from django import forms
from django.utils import timezone
from .models import NettoyageInterieur


class NettoyageInterieurForm(forms.ModelForm):
    date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'readonly': 'readonly', 'class': 'form-input'},
            format='%Y-%m-%d %H:%M:%S'
        )
    )

    class Meta:
        model = NettoyageInterieur
        exclude = ['maintenance', 'voiture_exemplaire']
        widgets = {
            'remarques': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "Ajoutez des remarques ici..."
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.exemplaire = kwargs.pop('exemplaire', None)
        super().__init__(*args, **kwargs)

        # Pré-remplir la date si elle existe
        if self.instance and self.instance.pk and self.instance.date:
            local_dt = timezone.localtime(self.instance.date)
            self.fields['date'].initial = local_dt.strftime('%Y-%m-%d %H:%M:%S')

        # Initialiser les champs technicien et société si présents
        if self.user:
            if "tech_technicien" in self.fields:
                self.fields["tech_technicien"].initial = self.user
                self.fields["tech_technicien"].disabled = True

            if "tech_societe" in self.fields:
                self.fields["tech_societe"].initial = self.user.societe
                self.fields["tech_societe"].disabled = True

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Assignation automatique du technicien
        if self.user and not instance.tech_technicien:
            instance.assign_technicien(self.user)

        # Associer l'exemplaire si fourni
        if self.exemplaire and not instance.voiture_exemplaire:
            instance.voiture_exemplaire = self.exemplaire

        if commit:
            instance.save()
        return instance